from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . forms import MyUserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.template.loader import render_to_string
from . scripts.producer import mail_to_queue
from django.core.validators import validate_email


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'sendmail/index.html')


class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    @staticmethod
    def take_mail(username, email):
        msg = {}
        username = username
        msg['subject'] = 'Добро пожаловать, {0}'.format(username)
        msg['message'] = 'Добро пожаловать, {0}'.format(username)
        msg['from_email'] = settings.DEFAULT_FROM_EMAIL
        msg['recipient_list'] = [email]
        msg['html_message'] = render_to_string('sendmail/send_mail.html',
                                               {'username': username})
        return msg

    def form_valid(self, form):
        form.save()
        username = form.instance.username
        validate_email(form.instance.email)
        email = form.instance.email
        mail_to_queue(self.take_mail(username, email))
        return super(SignUpView, self).form_valid(form)
