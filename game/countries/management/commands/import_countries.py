import os

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand

from countries.models import Country


class Command(BaseCommand):
    def handle(self, **options):
        shapefile = os.path.join(settings.HERE, os.pardir, 'data',
                                 'TM_WORLD_BORDERS-0.3.shp')

        ds = DataSource(shapefile)
        print len(ds), "layer"
        layer = ds[0]
        print '%s contains %s geometries (type: %s)' % (layer, len(layer),
                                                        layer.geom_type)
        print layer.srs

        #for feature in layer:
        #    print feature.get('NAME'), feature.geom.num_points

        mapping = {
            'fips': 'FIPS',
            'iso2': 'ISO2',
            'iso3': 'ISO3',
            'un': 'UN',
            'name': 'NAME',
            'area': 'AREA',
            'pop2005': 'POP2005',
            'region': 'REGION',
            'subregion': 'SUBREGION',
            'lon': 'LON',
            'lat': 'LAT',
            'mpoly': 'MULTIPOLYGON',
        }

        lm = LayerMapping(Country, shapefile, mapping,
                          transform=True, encoding='iso-8859-1')
        # Antartica doesn't convert to Spherical Mercator
        lm.save(fid_range=(1, 144), verbose=True)
        lm.save(fid_range=(146, 246), verbose=True)
