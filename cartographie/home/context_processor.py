from django.utils.functional import lazy

from auf.django.references import models as ref

from cartographie.formation.models import Formation
from cartographie.formation.constants import StatutsFormation

def stats(request):
    def _formations():
        return str(Formation.objects.exclude(statut=StatutsFormation.supprimee).count())

    def _etablissements():
        return str(ref.Etablissement.objects.all().count())

    def _disciplines():
        return str(ref.Discipline.objects.all().count())

    def _pays():
        return str(ref.Pays.objects.all().count())

    return {
        'stats_formations': lazy(_formations, str),
        'stats_etablissements': lazy(_etablissements, str),
        'stats_disciplines': lazy(_disciplines, str),
        'stats_pays': lazy(_pays, str),
        }
