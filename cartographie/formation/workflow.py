#coding: utf-8
from cartographie.formation.constants import statuts_formation as STATUTS, statut2label
from collections import defaultdict

# Admin is implicit.
TRANSITIONS = {
    STATUTS.en_redaction: {
        STATUTS.supprimee: { 'roles': ['token'] },
        STATUTS.validee: {'roles': ['token'] },
        },

    STATUTS.validee: {
        STATUTS.publiee: {'roles': ['editeur'] },
        STATUTS.en_redaction: {'retro': True,
                               'roles': ['editeur', 'token'] },
        STATUTS.supprimee: {'roles': ['token'] },
        },
    
    STATUTS.publiee: {
        STATUTS.validee: {'retro': True,
                          'roles': ['editeur'] },
        STATUTS.en_redaction: {'retro': True,
                               'roles': ['editeur'] },
        STATUTS.supprimee: {'roles': [] },
        },
    
    STATUTS.supprimee: {
        STATUTS.en_redaction: {'roles': [] }
        }
    }
