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
