#coding: utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from cartographie.formation.constants import statuts_formation as STATUTS


def formation_is_valider(sender, instance, signal, *args, **kwargs):
    """
        Envoi de courriel lorsque la formation (@instance) possède
        le statut "validée"
    """
    formation_courante = instance

    if formation_courante.statut == STATUTS.validee:
        plaintext = get_template('cartographie/email/formation_validee.txt')
        htmly = get_template('cartographie/email/formation_validee.html')

        # TODO: obtenir l'éditeur de la formation courante
        # TODO: obtenir le super utilisateur
        # TODO: obtenir le token

        d = Context({
            'formation': formation_courante,
            "token": "le token de l'établissement de la formation"
        })

        subject = 'Formation %i validée: %s' % (
            formation_courante.id, formation_courante.nom
        )
        from_email = 'from@example.com'
        to = 'to@example.com'

        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
