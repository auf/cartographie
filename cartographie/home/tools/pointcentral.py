import csv
import json
from lxml import etree

pays_ref = []
filename = 'ref_pays.csv'


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

tree = etree.parse(open('coordonnees_pays.xml'))
root = tree.getroot()
countries = {}
load_pays_ref()

for country in root:
    countryCode = country.findtext('isoAlpha3')
    west = float(country.findtext('west'))
    east = float(country.findtext('east'))
    north = float(country.findtext('north'))
    south = float(country.findtext('south'))
    latitude = (north + south) / 2
    longitude = (east + west) / 2
    countries[countryCode] = {
        'lat': latitude,
        'lon': longitude,
        'nom': get_nom_for_id(countryCode)
    }

print(json.dumps(countries))
