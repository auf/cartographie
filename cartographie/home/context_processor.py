from django.utils.functional import lazy

from auf.django.references import models as ref

from cartographie.formation.models import Formation
from cartographie.formation.constants import StatutsFormation

def stats(request):
    def _formations():
        return str(Formation.objects.exclude(statut=StatutsFormation.supprimee).count())

    def _etablissements():
        formations = Formation.objects.exclude(statut=StatutsFormation.supprimee)
        etablissements = set()
        for f in formations:
            etablissements.add(f.etablissement)
        return str(len(etablissements))

    def _disciplines():
        formations = Formation.objects.exclude(statut=StatutsFormation.supprimee)
        disciplines = set()
        for f in formations:
            disciplines.add(f.discipline_1)
            disciplines.add(f.discipline_2)
            disciplines.add(f.discipline_3)
        return str(len(disciplines))

    def _pays():
        formations = Formation.objects.exclude(statut=StatutsFormation.supprimee)
        pays = set()
        for f in formations:
            pays.add(f.etablissement.pays)
        return str(len(pays))

    return {
        'stats_formations': lazy(_formations, str),
        'stats_etablissements': lazy(_etablissements, str),
        'stats_disciplines': lazy(_disciplines, str),
        'stats_pays': lazy(_pays, str),
        }
