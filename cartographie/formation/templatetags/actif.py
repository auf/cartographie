from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter
def contacts_actifs(formation):
    return formation.contacts.filter(actif=True)


@register.filter
def disciplines_actives(formation):
    def discipline2nom(discipline):
        return discipline.nom

    def index2discipline(i):
        return getattr(formation, 'discipline_' + str(i))

    def is_active(obj):
        return obj and obj.actif

    disciplines = [
        discipline2nom(index2discipline(x))
        for x in [1, 2, 3]
        if is_active(index2discipline(x))
    ]

    return ', '.join(disciplines)


@register.filter
def langues_actives(formation):
    return formation.langue.filter(actif=True)


@register.filter
def niveaux_entrees_actifs(formation):
    return formation.niveau_entree.filter(actif=True)


@register.filter
def responsables_actifs(formation):
    return formation.responsables.filter(actif=True)


@register.filter
def vocations_actives(formation):
    return formation.vocation.filter(actif=True)
