import codecs
import csv
import simplejson

pays_ref = []
filename = 'ref_pays.csv'
pays_file = 'world.json'


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def load_pays_ref():
    reader = unicode_csv_reader(open(filename))
    for r in reader:
        pays_ref.append(r)


def get_nom_for_id(pays_id):
    for ref in pays_ref:
        if ref[2] == pays_id:
            return ref[3]


def replace_in_json():
    json = simplejson.loads("".join(open(pays_file).readlines()))
    manuellement = []
    new_json = dict(features=[])
    for pays in json['features']:
        if pays['properties']['NAME'] != 'Canada':
            pass
        else:
            pays_id = pays['properties']['ISO3']
            new_name = get_nom_for_id(pays_id)
            if new_name:
                pays['properties']['NAME'] = new_name
                print(new_name)
            else:
                print(pays['properties']['NAME'])
            new_json['features'].append(pays)
    f = codecs.open('test', 'w', 'utf-8')
    print(simplejson.dumps(new_json, indent=' '))
    f.write(simplejson.dumps(new_json))

if __name__ == '__main__':
    load_pays_ref()
    replace_in_json()
    print(get_nom_for_id('CHE'))
