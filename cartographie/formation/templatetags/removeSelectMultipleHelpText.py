# -*- coding: utf-8 -*-

from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def removeSelectMultipleHelpText(value):
    """Permet de supprimer le message tannant pour les selects à choix
    multiple"""

    msg = unicode(
        _('Hold down "Control", or "Command" on a Mac, to select more than ' +
            'one.'))

    return value.replace(msg, "")
