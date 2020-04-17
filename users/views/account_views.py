from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from project.utils import generate_unique_username
from users.forms import (RegistrationForm, ProfileChangeForm,
    ProfileDeleteForm, ProfileChangeRegistryForm, ProfileChangeAddressForm,
    ProfileChangeCourseForm, ProfileChangeNoCourseForm, ProfileAddChildForm)
from users.models import User, Profile, CourseSchedule

def registration_message( username, password ):
    #TODO have some info in settings
    message = f"""
        Ciao {username}! \n
        Abbiamo ricevuto la tua registrazione al sito {settings.WEBSITE_NAME}.\n
        Puoi effettuare il Login al seguente link: \n
        {settings.BASE_URL}/accounts/login/ \n
        Usa il nome utente da te scelto: {username}
        e questa password: {password} (possibilmente da cambiare).
        Una volta effettuato il login potrai gestire il tuo profilo.
        Grazie.
        Lo staff di {settings.WEBSITE_NAME} \n
        Link utili:
        Informativa per la privacy: {settings.BASE_URL}/docs/privacy/
        Cambio password: {settings.BASE_URL}/accounts/password_change/
        """
    return message

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

class RegistrationFormView(GetMixin, FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = '/registration?submitted=True'

    def form_valid(self, form):
        user = form.save(commit=False)
        password = User.objects.make_random_password()
        user.password = make_password(password)
        user.save()
        subject = f'Credenziali di accesso a {settings.WEBSITE_ACRO}'
        body = registration_message(user.username, password)
        mailto = [ user.email, ]
        email = EmailMessage(subject, body, settings.SERVER_EMAIL, mailto)
        email.send()
        return super(RegistrationFormView, self).form_valid(form)

class ProfileAddChildView(LoginRequiredMixin, FormView):
    form_class = ProfileAddChildForm
    template_name = 'users/profile_add_child.html'
    success_url = '/accounts/profile/?child_created=True'

    def get(self, request, *args, **kwargs):
        usr = self.request.user
        if usr.profile.sector == '0-NO' or not usr.profile.is_trusted:
            raise Http404("User is not authorized to add children")
        return super(ProfileAddChildView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        usr = self.request.user
        child = form.save(commit=False)
        username = (child.first_name + '.' + child.last_name).lower()
        child.username = generate_unique_username(username)
        child.is_active = False
        child.password = usr.password
        child.email = usr.email
        child.save()
        #we have to create profile since child is an inactive user
        child_profile = Profile.objects.create(user = child)
        child_profile.parent = usr
        child_profile.sector = '1-YC'
        child_profile.save()
        return super(ProfileAddChildView, self).form_valid(form)

class TemplateAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        if 'child_created' in request.GET:
            context['child_created'] = request.GET['child_created']
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usr = self.request.user
        if not usr.profile.sector == '0-NO' and usr.profile.is_trusted:
            context['can_add_child'] = True
        context['children'] = usr.get_children()
        return context

    def get_template_names(self):
        sector = self.request.user.profile.sector
        if sector == '1-YC':
            return ['users/account_1.html']
        elif sector == '2-NC':
            return ['users/account_2.html']
        elif sector == '3-FI':
            return ['users/account_3.html']
        return super(TemplateAccountView, self).get_template_names()

class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'users/profile_change.html'

    def get(self, request, *args, **kwargs):
        if 'parent' in request.GET:
            child = get_object_or_404(Profile, user_id = kwargs['pk'],
                parent_id = request.user.id)
        elif request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeView, self).get(request, *args, **kwargs)

    def get_initial(self):
        user = get_object_or_404(User, id = self.kwargs['pk'])
        initial = super(ProfileChangeView, self).get_initial()
        initial.update({'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'avatar': user.profile.avatar,
            'bio': user.profile.bio,
            'yes_spam': user.profile.yes_spam,
            'sector': user.profile.sector,
            })
        return initial

    def form_valid(self, form):
        user = get_object_or_404(User, id = self.kwargs['pk'])
        profile = Profile.objects.get(pk = user.id)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        profile.avatar = form.cleaned_data['avatar']
        profile.bio = form.cleaned_data['bio']
        profile.yes_spam = form.cleaned_data['yes_spam']
        profile.sector = form.cleaned_data['sector']
        user.save()
        profile.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get_success_url(self):
        user = get_object_or_404(User, id = self.kwargs['pk'])
        return f'/accounts/profile/?submitted={user.get_full_name()}'

class ProfileChangeRegistryView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileChangeRegistryForm
    template_name = 'users/profile_change_registry.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeRegistryView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileChangeAddressView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileChangeAddressForm
    template_name = 'users/profile_change_address.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeAddressView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileChangeCourseView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileChangeCourseForm
    template_name = 'users/profile_change_course.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeCourseView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileChangeNoCourseView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileChangeNoCourseForm
    template_name = 'users/profile_change_no_course.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeNoCourseView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileDeleteView(LoginRequiredMixin, FormView):
    form_class = ProfileDeleteForm
    template_name = 'users/profile_delete.html'
    success_url = '/accounts/profile/deleted'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileDeleteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(id = self.request.user.id )
        user.is_active = False
        user.first_name = ''
        user.last_name = ''
        user.email = ''
        user.save()
        profile = Profile.objects.get(pk = user.id)
        profile.delete()
        return super(ProfileDeleteView, self).form_valid(form)

class TemplateDeletedView(TemplateView):
    template_name = 'users/profile_deleted.html'
