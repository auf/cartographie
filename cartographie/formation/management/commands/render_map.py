from ..generate_tiles import render_tiles
from   django.core.management.base import BaseCommand
import os
import re
import shutil

def purge(dir, pattern):
    for f in os.listdir(dir):
    	if re.search(pattern, f):
            path = os.path.join(dir, f)
            if os.path.isdir(path):
                shutil.rmtree(path)

# Usage: ./bin/django render_map data/ cartographie/static/tiles/

class Command(BaseCommand):
    def handle(self, data_dir, tile_dir, **kwargs):
        print "Removing tiles in '%s'... " % tile_dir
        purge(tile_dir, re.compile("^[0-9]{1,2}$"))
        print "Done"

        mapfile = os.path.join(data_dir, 'cartographie.xml')
        bbox = (-180.0,-90.0, 180.0,90.0)
        render_tiles(bbox, mapfile, tile_dir, 2, 5, "World")
