from django.utils.functional import lazy

from auf.django.references import models as ref

from cartographie.formation.models import Formation
from cartographie.formation.constants import StatutsFormation

def stats(request):
    def _formations():
        return str(Formation.objects.exclude(statut=StatutsFormation.supprimee).count())

    def _etablissements():
        data = Formation.objects.exclude(statut=StatutsFormation.supprimee) \
            .values('etablissement')
        etablissements = set()
        for d in data:
            etablissements.add(d['etablissement'])
        return str(len(etablissements))

    def _disciplines():
        data = Formation.objects.exclude(statut=StatutsFormation.supprimee) \
            .values('discipline_1', 'discipline_2', 'discipline_3')
        disciplines = set()
        for d in data:
            disciplines.add(d['discipline_1'])
            disciplines.add(d['discipline_2'])
            disciplines.add(d['discipline_3'])
        return str(len(disciplines))

    def _pays():
        data = Formation.objects.exclude(statut=StatutsFormation.supprimee).values('etablissement__pays')
        pays = set()
        for d in data:
            pays.add(d['etablissement__pays'])
        return str(len(pays))

    return {
        'stats_formations': lazy(_formations, str),
        'stats_etablissements': lazy(_etablissements, str),
        'stats_disciplines': lazy(_disciplines, str),
        'stats_pays': lazy(_pays, str),
        }
