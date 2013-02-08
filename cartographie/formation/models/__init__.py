#coding: utf-8

# Étant donné que j'ai séparé les models dans différents fichiers,
# les imports suivants sont nécessaires pour que l'on puisse faire
# from models import [whatever].
from userRole import UserRole
from personne import Personne
from acces import Acces
from etablissement import EtablissementComposante, EtablissementAutre
from formation import Formation, FormationModification, FormationCommentaire, \
                      FormationComposante
from configuration import Discipline, NiveauDiplome, TypeDiplome, \
                          DelivranceDiplome, NiveauUniversitaire, \
                          Vocation, TypeFormation

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
