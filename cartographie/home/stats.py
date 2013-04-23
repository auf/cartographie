
class Statistiques(object):

    def __init__(self, request):
        pass
    
    def get_data(self):
        return { 'stats' : { 'formations': 10,
                             'disciplines': 30,
                             'etablissements': 500,
                             'pays': 20 }}
