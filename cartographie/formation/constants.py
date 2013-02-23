#coding: utf-8


class SessionConstants(object):
    """
    Classe servant de conteneur pour les noms de variable Session.

    L'idée est de pouvoir les modifier en une seul et même place
    et de ne pas passer une string à l'objet request.session
    """

    eta_id = "espace_formation_etablissement_id"
    erreur = "espace_formation_erreur"

session_const = SessionConstants()


class StatutsFormation(object):
    """
        Les différents statuts possibles pour une fiche formation
    """
    abandonnee = -1
    abandonnee_label = u"Abandonnée"

    archivee = -2
    archivee_label = u"Archivée"

    en_redaction = 1
    en_redaction_label = u"En rédaction"

    validee = 2
    validee_lable = u"Validée"

    publiee = 3
    publiee_label = u"Publiée"

statuts_formation = StatutsFormation()
