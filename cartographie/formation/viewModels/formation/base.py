#coding: utf-8
from cartographie.formation.models import Acces, Formation, UserRole
from cartographie.formation.workflow import TRANSITIONS
from cartographie.formation.constants import statuts_formation as STATUTS
from django.core.urlresolvers import reverse

class BaseModifierViewModel(object):
    def __init__(self, request, token, formation_id):
        self.token = token
        self.formation = Formation.objects.get(pk=formation_id)
        self.statuts_valides = UserRole.valid_status(request.user, self.token, self.formation)
        self.transitions = TRANSITIONS[self.formation.statut]
        self.boutons = {}

        for statut, nom, label_si_retro, label in \
                [(STATUTS.en_redaction, 'redaction', u"Retour en rédaction", u"Retour en rédaction"),
                 (STATUTS.validee, 'valider', u"Retour à validée", u"Valider"),
                 (STATUTS.publiee, 'publier', u"Retour à publiée", u"Publier"),
                 (STATUTS.supprimee, 'supprimer', u"Retour à supprimée", u"Supprimer")]:
            if statut in self.statuts_valides:
                retro = self.transitions[statut].get('retro', False)
                if retro:
                    view_name = 'formation_commentaire_avant_changement_statut'
                else:
                    view_name = 'formation_modifier_workflow'
                self.boutons[nom] = { 'retro': retro,
                                      'url': reverse(view_name, 
                                                     args=[self.token,
                                                           self.formation.id,
                                                           statut]),
                                      'class': 'modal-commentaire' if retro else '',
                                      'label': label_si_retro if retro else label }

    def get_data(self):
        return {
            'boutons': self.boutons,
            }

