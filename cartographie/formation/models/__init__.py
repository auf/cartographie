#coding: utf-8

# Étant donné que j'ai séparé les models dans différents fichiers,
# les imports suivants sont nécessaires pour que l'on puisse faire
# from models import [whatever].

# http://paltman.com/2008/01/29/breaking-apart-models-in-django/
from userRole import UserRole
from personne import Personne
from acces import Acces
from configuration import Discipline, NiveauDiplome, \
                          TypeDiplome, DelivranceDiplome, \
                          NiveauUniversitaire, Vocation, TypeFormation, \
                          Langue, EtablissementCoordonnees

from etablissement import EtablissementComposante, EtablissementAutre

from formation import Formation, FormationModification, \
                      FormationCommentaire, FormationComposante, \
                      FormationPartenaireAutre, FormationPartenaireAUF

from workflow import WorkflowMixin

# il faut absolument rajouter nos Model importés dans cette liste
# http://stackoverflow.com/questions/44834/can-someone-explain-all-in-python
__all__ = [
    "UserRole", "Personne", "Acces", "Discipline", "NiveauDiplome",
    "TypeDiplome", "DelivranceDiplome", "NiveauUniversitaire", "Vocation",
    "TypeFormation", "EtablissementComposante", "EtablissementAutre",
    "Formation", "FormationModification", "FormationCommentaire",
    "FormationComposante", "FormationPartenaireAutre", "FormationPartenaireAUF",
    "Langue", "WorkflowMixin", "EtablissementCoordonnees"
]

if __name__ == '__main__':
    """
        Ce qui se trouve plus bas ne sert à rien à part arrêter mon éditeur
        de code de se plaindre que les import plus haut ne sont pas utilisé
        dans ce fichier.

        Damné sois-tu ô plugin de vérification PEP8 !

        Bernard Chhun <bernard.chhun@savoirfairelinux.com>
    """
    u = UserRole()
    p = Personne()
    a = Acces()
    ec = EtablissementComposante()
    ea = EtablissementAutre()
    f = Formation()
    fm = FormationModification()
    fc = FormationCommentaire()
    fcc = FormationComposante()
    d = Discipline()
    nd = NiveauDiplome()
    tp = TypeDiplome()
    dd = DelivranceDiplome()
    nu = NiveauUniversitaire()
    v = Vocation()
    tf = TypeFormation()
    wf = Workflow()
