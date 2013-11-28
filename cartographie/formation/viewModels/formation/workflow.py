# -*- coding: utf-8 -*-

from copy import copy

from django.contrib import messages
from django.core.urlresolvers import reverse

from cartographie.formation.constants import statut2label
from cartographie.formation.models import Acces, Formation, Personne
from cartographie.formation.models.workflow import ETATS
from cartographie.formation.viewModels.baseAjouterViewModel import (
    BaseAjouterViewModel)
from cartographie.formation.workflow import TRANSITIONS


class WorkflowViewModel(BaseAjouterViewModel):

    def __init__(self, request, token, formation_id, statut_id):
        super(WorkflowViewModel, self).__init__(request, token)

        statut_id = int(statut_id)

        # Vérifier que le statut existe
        if statut_id in map(lambda st: st[0], ETATS):

            # Obtenir la formation courante
            formation_courante = Formation.objects.get(pk=formation_id)
            source_statut = formation_courante.statut

            self.necessite_commentaire = (
                formation_courante.changement_necessite_commentaire(
                    statut_id))

            pas_de_probleme = False

            # Modifier le statut avec les fonctions de WorkflowMixin
            statut_modifie = formation_courante.set_statut(
                request.user, token, statut_id)

            if statut_modifie:
                pas_de_probleme = True
            else:
                messages.error(
                    request,
u"""Vous ne pouvez pas attribuer le statut '%s'à cette fiche."""\
                    % (statut2label[statut_id], ))

            if pas_de_probleme:
                statut_labels = filter(lambda st: st[0] == statut_id, ETATS)
                statut_label = statut_labels.pop()

                messages.success(
                    request, u"Le statut '%s' a été appliqué à la fiche" % (
                        statut_label[1], ))

                if source_statut == 3 and statut_id == 1:
                    # La formation va de 'publiée' à 'rédaction'
                    self._brouillon(formation_courante)
                elif statut_id == 3:
                    # La formation va à 'publiée'
                    self._publication(formation_courante)

                self._envoie_courriel(
                    formation_courante, source_statut, statut_id)

                formation_courante.save()
                formation_courante.save_modification(request)
        else:
            messages.warning(request, u"Ce statut n'existe pas")

    def get_data(self):
        data = super(WorkflowViewModel, self).get_data()

        return data

    def _brouillon(self, formation):
        '''Crée un clone en rédaction et garde la fiche courante publiée'''

        print('brouillon')

        clone = copy(formation)
        clone.pk = None
        clone.save()

        formation.brouillon = clone
        formation.statut = 3  # Garde la formation originale publiée
        formation.save()

    def _publication(self, formation):
        '''Écrase la formation publiée avec les modifications'''

        try:
            original = formation.publication_originale

            if original:
                try:
                    formation.publication_originale = None
                    formation.save()
                except AttributeError:
                    # FIXME vraiment désagréable ça.
                    pass
                original.brouillon = None
                original.save()
                original.delete()
        except Formation.DoesNotExist:
            pass

    # C'est moche, mais c'est pour avoir des étiquettes personnalisées pour
    # mettre dans les courriels. Sinon, utiliser les labels originaux.
    STATES = {
        1: u'rédaction',
        2: u'validée',
        3: u'publiée',
        999: u'supprimée',
    }

    def _envoie_courriel(self, formation, source_id, target_id):
        from cartographie.formation.models.formation import EnveloppeParams
        from auf.django.mailing.models import envoyer

        personnes = Personne.objects.filter(
            etablissement=formation.etablissement, role='referent')
        source = self.STATES[source_id]
        target = self.STATES[target_id]

        token = Acces.token_for_etablissement(formation.etablissement)

        for personne in personnes:
            params = EnveloppeParams.creer_depuis_modele('modform')
            params.formation = formation.nom
            params.source = source
            params.target = target
            params.url = reverse('formation_modifier', args=[token, formation.id])
            params.courriel_destinataire = personne.courriel
            params.save()

        envoyer('modform', 'cartographie@auf.org')
