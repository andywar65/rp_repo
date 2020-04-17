from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic.edit import FormView
from users.forms import (ContactForm, ContactLogForm, )
from users.models import User

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

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
