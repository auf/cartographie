# -*- coding: utf-8 -*-

from cartographie.formation.constants import statuts_formation as STATUTS

# Admin is implicit.
TRANSITIONS = {
    STATUTS.en_redaction: {
        STATUTS.supprimee: {'retro': True, 'roles': ['token', 'referent']},
        STATUTS.validee: {'roles': ['referent', 'token']},

        },

    STATUTS.validee: {
        STATUTS.publiee: {'roles': ['editeur']},
        STATUTS.en_redaction: {'retro': True,
                               'roles': ['editeur', 'referent', 'token']},
        STATUTS.supprimee: {'retro': True, 'roles': ['token']},
        },

    STATUTS.publiee: {
        STATUTS.validee: {'retro': True,
                          'roles': ['editeur']},
        STATUTS.en_redaction: {'retro': True,
                               'roles': ['editeur', 'referent']},
        STATUTS.supprimee: {'retro': True, 'roles': []},
        },

    STATUTS.supprimee: {
        STATUTS.en_redaction: {'roles': []}
        }
    }
