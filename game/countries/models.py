from django.contrib.gis.db import models

WGS84 = 4326
SPHERICAL_MERCATOR = 3857

REGIONS = (
    (0, 'None'),
    (2, 'Africa'),
    (9, 'Oceania'),
    (19, 'Americas'),
    (142, 'Asia'),
    (150, 'Europe'),
)

SUBREGIONS = (
    (0, 'None'),
    (5, 'South America'),
    (11, 'Western Africa'),
    (13, 'Central America'),
    (14, 'Eastern Africa'),
    (15, 'Northern Africa'),
    (17, 'Middle Africa'),
    (18, 'Southern Africa'),
    (21, 'Northern America'),
    (29, 'Carribean'),
    (30, 'Eastern Asia'),
    (34, 'Southern Asia'),
    (35, 'South-Eastern Asia'),
    (39, 'Southern Europe'),
    (53, 'Australia and New Zealand'),
    (54, 'Melanesia'),
    (57, 'Micronesia'),
    (61, 'Polynesia'),
    (143, 'Central Asia'),
    (145, 'Western Asia'),
    (151, 'Eastern Europe'),
    (154, 'Northern Europe'),
    (155, 'Western Europe'),
)


class Country(models.Model):
    fips = models.CharField('FIPS Code', max_length=2)
    # http://www.unc.edu/~rowlett/units/codes/country.htm
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    name = models.CharField('Name', max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population in 2005')
    region = models.IntegerField('Region Code', choices=REGIONS)
    subregion = models.IntegerField('Sub-Region Code', choices=SUBREGIONS)
    lon = models.FloatField()
    lat = models.FloatField()
    mpoly = models.MultiPolygonField(srid=WGS84)
    #mpoly = models.MultiPolygonField(srid=SPHERICAL_MERCATOR)

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'%s' % self.name
