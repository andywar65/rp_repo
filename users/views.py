from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from .forms import (RegistrationForm, ContactForm,
    ContactLogForm, FrontAuthenticationForm, FrontPasswordResetForm,
    FrontSetPasswordForm, FrontPasswordChangeForm, ProfileChangeForm,
    ProfileDeleteForm, ProfileChangeRegistryForm, ProfileChangeAddressForm,
    ProfileChangeCourseForm, )
from .models import User, Profile, CourseSchedule

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

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

class ContactFormView(GetMixin, FormView):
    form_class = ContactForm
    template_name = 'users/message.html'
    success_url = '/contacts?submitted=True'

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        if 'subject' in self.request.GET:
            initial.update({'subject': self.request.GET['subject']})
        return initial

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return ContactLogForm
        return super(ContactFormView, self).get_form_class()

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'users/message_log.html'
        return super(ContactFormView, self).get_template_names()

    def form_valid(self, form):
        message = form.save(commit=False)
        if self.request.user.is_authenticated:
            message.user = self.request.user
            message.email = self.request.user.email
            if 'recipient' in self.request.GET:
                try:
                    recip = User.objects.get(id=self.request.GET['recipient'])
                    message.recipient = recip.email
                except:
                    pass
        message.save()
        if not message.recipient:
            message.recipient = settings.DEFAULT_RECIPIENT
        subject = message.subject
        msg = (message.body + '\n\nDa: '+ message.get_full_name() +
            ' (' + message.get_email() + ')')
        mailto = [message.recipient, ]
        email = EmailMessage(subject, msg, settings.SERVER_EMAIL,
            mailto)
        if message.attachment:
            email.attach_file(message.attachment.path)
        email.send()
        return super(ContactFormView, self).form_valid(form)

class FrontLoginView(LoginView):
    template_name = 'users/front_login.html'
    form_class = FrontAuthenticationForm

    def get_redirect_url(self):
        """Avoid going from login to logout and other ambiguous situations"""
        redirect_to = super(FrontLoginView, self).get_redirect_url()
        if redirect_to == reverse('front_logout'):
            return reverse('profile')
        elif redirect_to == reverse('password_reset_done'):
            return reverse('profile')
        elif redirect_to == reverse('profile_deleted'):
            return reverse('profile')
        elif redirect_to == reverse('registration'):
            return reverse('profile')
        return redirect_to

class FrontLogoutView(LogoutView):
    template_name = 'users/front_logout.html'

class FrontPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = FrontPasswordResetForm

class TemplateResetView(TemplateView):
    template_name = 'users/reset_password_done.html'

class FrontPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_password_confirm.html'
    form_class = FrontSetPasswordForm

class TemplateResetDoneView(TemplateView):
    template_name = 'users/reset_done.html'

class TemplateAccountView(LoginRequiredMixin, GetMixin, TemplateView):
    template_name = 'users/account.html'

    def get_template_names(self):
        sector = self.request.user.profile.sector
        if sector == '1-YC':
            return ['users/account_1.html']
        elif sector == '2-NC':
            return ['users/account_2.html']
        elif sector == '3-FI':
            return ['users/account_3.html']
        return super(TemplateAccountView, self).get_template_names()

class FrontPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = FrontPasswordChangeForm

class FrontPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'users/profile_change.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()
        initial.update({'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'avatar': self.request.user.profile.avatar,
            'bio': self.request.user.profile.bio,
            'yes_spam': self.request.user.profile.yes_spam,
            'sector': self.request.user.profile.sector,
            })
        return initial

    def form_valid(self, form):
        user = User.objects.get(id = self.request.user.id )
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
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileChangeRegistryView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeRegistryForm
    template_name = 'users/profile_change_registry.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeRegistryView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeRegistryView, self).get_initial()
        profile = self.request.user.profile
        initial.update({'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
            'place_of_birth': profile.place_of_birth,
            'nationality': profile.nationality,
            'fiscal_code': profile.fiscal_code,
            })
        return initial

    def form_valid(self, form):
        profile = Profile.objects.get(pk = self.request.user.id)
        profile.gender = form.cleaned_data['gender']
        profile.date_of_birth = form.cleaned_data['date_of_birth']
        profile.place_of_birth = form.cleaned_data['place_of_birth']
        profile.nationality = form.cleaned_data['nationality']
        profile.fiscal_code = form.cleaned_data['fiscal_code']
        profile.save()
        return super(ProfileChangeRegistryView, self).form_valid(form)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileChangeAddressView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeAddressForm
    template_name = 'users/profile_change_address.html'

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeAddressView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeAddressView, self).get_initial()
        profile = self.request.user.profile
        initial.update({'fiscal_code': profile.fiscal_code,
            'address': profile.address,
            'phone': profile.phone,
            'email_2': profile.email_2,
            })
        return initial

    def form_valid(self, form):
        profile = Profile.objects.get(pk = self.request.user.id)
        profile.fiscal_code = form.cleaned_data['fiscal_code']
        profile.address = form.cleaned_data['address']
        profile.phone = form.cleaned_data['phone']
        profile.email_2 = form.cleaned_data['email_2']
        profile.save()
        return super(ProfileChangeAddressView, self).form_valid(form)

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

    #def get_initial(self):
        #initial = super(ProfileChangeCourseView, self).get_initial()
        #profile = self.request.user.profile
        #initial.update({'course': profile.course,
            #'course_alt': profile.course_alt,
            #'course_membership': profile.course_membership,
            #'sign_up': profile.sign_up,
            #'privacy': profile.privacy,
            #'med_cert': profile.med_cert,
            #})
        #return initial

    #def form_valid(self, form):
        #profile = Profile.objects.get(pk = self.request.user.id)
        #profile.course.set(form.cleaned_data['course'])
        #xlb = profile.course
        #profile.course_alt = form.cleaned_data['course_alt']
        #profile.course_membership = form.cleaned_data['course_membership']
        #profile.sign_up = form.cleaned_data['sign_up']
        #profile.privacy = form.cleaned_data['privacy']
        #profile.med_cert = form.cleaned_data['med_cert']
        #profile.save()
        #assert False
        #return super(ProfileChangeCourseView, self).form_valid(form)

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
