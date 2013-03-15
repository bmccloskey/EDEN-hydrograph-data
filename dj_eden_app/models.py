from django.db import models

class VerticalDatum(models.Model):
    vertical_datum_id = models.IntegerField(primary_key=True)
    vertical_datum = models.CharField(max_length=30)
    definition = models.CharField(max_length=120)
    class Meta:
        db_table = u'vertical_datum'
        managed = False

class Station(models.Model):
    '''
    List of EDEN stations
    '''
    station_id = models.IntegerField(primary_key=True)
    station_name = models.CharField(max_length=72)
    operating_agency_id = models.IntegerField()
    database_agency_id = models.IntegerField()
    station_name_2005 = models.CharField(max_length=30, blank=True)
    station_name_2004 = models.CharField(max_length=30, blank=True)
    usgs_nwis_agency_id = models.IntegerField()
    usgs_nwis_id = models.CharField(max_length=45, blank=True)
    longitude = models.CharField(max_length=36)
    latitude = models.CharField(max_length=36)
    utm_easting = models.FloatField()
    utm_northing = models.FloatField()
    location_id = models.IntegerField()
    location_description = models.CharField(max_length=150, blank=True)
    master_id = models.IntegerField(null=True, blank=True)
    funding_agency_id = models.IntegerField(null=True, blank=True)
    funding_program_id = models.IntegerField(null=True, blank=True)
    station_name_web = models.CharField(max_length=105)
    edenapps = models.IntegerField()
    edenmaster = models.IntegerField(null=True, blank=True)
    daily_download = models.IntegerField()
    upload_device = models.IntegerField(null=True, blank=True)
    dd = models.IntegerField()
    vertical_datum = models.ForeignKey(VerticalDatum)
    display = models.IntegerField()
    short_name = models.CharField(max_length=105)
    label_shift = models.CharField(max_length=21)
    comments = models.CharField(max_length=810, blank=True)
    param = models.CharField(max_length=15)
    edenmaster_new = models.IntegerField(null=True, blank=True)
    retrdaily = models.IntegerField(null=True, blank=True)
    dry_elevation = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)
    duration_elevation = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    realtime = models.IntegerField()
    edenmaster_start = models.CharField(max_length=18, blank=True)
    edenmaster_end = models.CharField(max_length=18, blank=True)
    coastal = models.CharField(max_length=24, blank=True)

    def __unicode__(self):
        return self.station_name_web

    class Meta:
        db_table = u'station'
        managed = False
        ordering = ['station_name_web', 'station_id']

class StationDatum(models.Model):
    # legacy fields are commented out
    station = models.OneToOneField(Station, primary_key=True)
    # vertical_conversion = models.FloatField(null=True, blank=True)
    datum_survey_history = models.CharField(max_length=120, blank=True)
    convert_to_navd88_feet = models.FloatField()
    # convert_to_navd88_feet_pre2003 = models.FloatField(null=True, blank=True)
    # convert_to_navd88_feet_pre2004 = models.FloatField(null=True, blank=True)
    # conversion_id = models.IntegerField()
    # conversion_year = models.TextField(blank=True)  # This field type is a guess.
    class Meta:
        db_table = u'station_datum'
        managed = False


