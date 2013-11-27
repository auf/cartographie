# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from cartographie.home.forms.feedback import FeedbackForm


class FeedbackViewModel(object):

    def __init__(self, request, *args, **kwargs):
        self.form = FeedbackForm()

        if request.method == 'POST':
            self.form = FeedbackForm(request.POST)
            if self.form.is_valid():
                feedback = self.form.save()
                if self._envoyer_courriel(feedback):
                    messages.success(
                        request,
                        u"Votre message nous a bien été envoyé. Merci!")
                    self.form = FeedbackForm()
                else:
                    messages.error(
                        request, u"Votre message n'a pu être envoyé.")

    def _envoyer_courriel(self, feedback):
        plaintext = get_template('cartographie/email/feedback.txt')

        subject = "AUF - Cartographie: Nouveau feedback"

        context = Context({'feedback': feedback})

        text_content = plaintext.render(context)
        from_email = 'cartographie@auf.org'
        to = settings.EMAIL_FEEDBACK

        msg = EmailMessage(subject, text_content, from_email, to)

        return msg.send()

    def get_data(self):
        return {'form': self.form}
