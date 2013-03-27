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
    supprimee = 999
    supprimee_label = u"Supprimée"
    supprimee_msg_confirmation = u"Voulez-vous vraiment supprimer cette fiche ?"

    archivee = 888
    archivee_label = u"Archivée"
    archivee_msg_confirmation = u"Voulez-vous vraiment archiver cette fiche ?"

    en_redaction = 1
    en_redaction_label = u"En rédaction"
    en_redaction_msg_confirmation = u"Voulez-vous vraiment mettre cette fiche en rédaction ?"

    validee = 2
    validee_label = u"Validée"
    validee_msg_confirmation = u"Voulez-vous vraiment valider cette fiche ?"

    publiee = 3
    publiee_label = u"Publiée"
    publiee_msg_confirmation = u"Voulez-vous vraiment publier cette fiche ?"

statuts_formation = StatutsFormation()
