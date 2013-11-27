#coding: utf-8

from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.models import User

from cartographie.formation.constants import statuts_formation as STATUTS
from cartographie.formation.models import Acces, UserRole


def formation_is_valider(sender, instance, signal, *args, **kwargs):
    """
        Envoi de courriel lorsque la formation (@instance) possède
        le statut "validée"
    """
    formation_courante = instance

    if formation_courante.statut == STATUTS.validee:
        plaintext = get_template('cartographie/email/formation_validee.txt')
        htmly = get_template('cartographie/email/formation_validee.html')

        # obtention du token d'acces à injecter dans le courriel
        acces = Acces.objects.get(
            etablissement__id=formation_courante.etablissement.id
        )

        d = Context({
            'formation': formation_courante,
            "token": acces.token
        })

        subject = u'Formation %i validée: %s' % (
            formation_courante.id, formation_courante.nom
        )

        from_email = 'cartographie@auf.org'
        to = []
        bcc = []

        # obtenir le(s) courriel(s) de(s) éditeur(s) de la formation courante
        user_roles = UserRole.objects.filter(type="editeur").values_list(
            "regions", "user__email"
        )
        for region_id, editeur_email in user_roles:
            if region_id == formation_courante.etablissement.region.id:
                if editeur_email:
                    to.append(editeur_email)

        # obtenir courriel du super utilisateur
        for u in User.objects.filter(is_superuser=True):
            if u.email:
                bcc.append(u.email)

        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, to, bcc)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
