#coding: utf-8

# Étant donné que j'ai séparé les models dans différents fichiers,
# les imports suivants sont nécessaires pour que l'on puisse faire
# from models import [whatever].
from userRole import UserRole
from discipline import Discipline
from personne import Personne
from acces import Acces
from etablissement import EtablissementComposante, EtablissementAutre
from formation import Formation, FormationModification, FormationCommentaire, \
                      FormationComposante, RoleComposante


if __name__ == '__main__':
    """
        Ce qui se trouve plus bas ne sert à rien à part arrêter mon éditeur
        de code de se plaindre que les import plus haut ne sont pas utilisé
        dans ce fichier.

        Damné sois-tu ô plugin de vérification PEP8 !

        Bernard Chhun <bernard.chhun@savoirfairelinux.com>
    """
    u = UserRole()
    d = Discipline()
    p = Personne()
    a = Acces()
    ec = EtablissementComposante()
    ea = EtablissementAutre()
    f = Formation()
    fm = FormationModification()
    fc = FormationCommentaire()
    fcc = FormationComposante()
    rc = RoleComposante()
