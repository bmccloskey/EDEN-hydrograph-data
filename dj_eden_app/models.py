from django.db import models

# Create your models here.        
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
    vertical_datum_id = models.IntegerField()
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
        
class Stage(models.Model):
    '''
    EDEN timeseries data. This not used at present.
    '''
    datetime = models.DateTimeField(primary_key=True)
    stage_2a300 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_2A300', blank=True) # Field name made lowercase.
    flag_2a300 = models.CharField(max_length=3, db_column='flag_2A300', blank=True) # Field name made lowercase.
    stage_3a_5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3A-5', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_3a_5 = models.CharField(max_length=3, db_column='flag_3A-5', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_3a10 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3A10', blank=True) # Field name made lowercase.
    flag_3a10 = models.CharField(max_length=3, db_column='flag_3A10', blank=True) # Field name made lowercase.
    stage_3a11 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3A11', blank=True) # Field name made lowercase.
    flag_3a11 = models.CharField(max_length=3, db_column='flag_3A11', blank=True) # Field name made lowercase.
    stage_3a12 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3A12', blank=True) # Field name made lowercase.
    flag_3a12 = models.CharField(max_length=3, db_column='flag_3A12', blank=True) # Field name made lowercase.
    stage_3a9 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3A9', blank=True) # Field name made lowercase.
    flag_3a9 = models.CharField(max_length=3, db_column='flag_3A9', blank=True) # Field name made lowercase.
    stage_3an1w1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3AN1W1', blank=True) # Field name made lowercase.
    flag_3an1w1 = models.CharField(max_length=3, db_column='flag_3AN1W1', blank=True) # Field name made lowercase.
    stage_3ane = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3ANE', blank=True) # Field name made lowercase.
    flag_3ane = models.CharField(max_length=3, db_column='flag_3ANE', blank=True) # Field name made lowercase.
    stage_3anw = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3ANW', blank=True) # Field name made lowercase.
    flag_3anw = models.CharField(max_length=3, db_column='flag_3ANW', blank=True) # Field name made lowercase.
    stage_3as = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3AS', blank=True) # Field name made lowercase.
    flag_3as = models.CharField(max_length=3, db_column='flag_3AS', blank=True) # Field name made lowercase.
    stage_3as3w1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3AS3W1', blank=True) # Field name made lowercase.
    flag_3as3w1 = models.CharField(max_length=3, db_column='flag_3AS3W1', blank=True) # Field name made lowercase.
    stage_3asw = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3ASW', blank=True) # Field name made lowercase.
    flag_3asw = models.CharField(max_length=3, db_column='flag_3ASW', blank=True) # Field name made lowercase.
    stage_3b_se = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3B-SE', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_3b_se = models.CharField(max_length=3, db_column='flag_3B-SE', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_3bs1w1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3BS1W1', blank=True) # Field name made lowercase.
    flag_3bs1w1 = models.CharField(max_length=3, db_column='flag_3BS1W1', blank=True) # Field name made lowercase.
    stage_a13 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_A13', blank=True) # Field name made lowercase.
    flag_a13 = models.CharField(max_length=3, db_column='flag_A13', blank=True) # Field name made lowercase.
    stage_barw4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BARW4', blank=True) # Field name made lowercase.
    flag_barw4 = models.CharField(max_length=3, db_column='flag_BARW4', blank=True) # Field name made lowercase.
    stage_barw6a = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BARW6A', blank=True) # Field name made lowercase.
    flag_barw6a = models.CharField(max_length=3, db_column='flag_BARW6A', blank=True) # Field name made lowercase.
    stage_bca1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA1', blank=True) # Field name made lowercase.
    flag_bca1 = models.CharField(max_length=3, db_column='flag_BCA1', blank=True) # Field name made lowercase.
    stage_bca10 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA10', blank=True) # Field name made lowercase.
    flag_bca10 = models.CharField(max_length=3, db_column='flag_BCA10', blank=True) # Field name made lowercase.
    stage_bca11 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA11', blank=True) # Field name made lowercase.
    flag_bca11 = models.CharField(max_length=3, db_column='flag_BCA11', blank=True) # Field name made lowercase.
    stage_bca12 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA12', blank=True) # Field name made lowercase.
    flag_bca12 = models.CharField(max_length=3, db_column='flag_BCA12', blank=True) # Field name made lowercase.
    stage_bca13 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA13', blank=True) # Field name made lowercase.
    flag_bca13 = models.CharField(max_length=3, db_column='flag_BCA13', blank=True) # Field name made lowercase.
    stage_bca14 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA14', blank=True) # Field name made lowercase.
    flag_bca14 = models.CharField(max_length=3, db_column='flag_BCA14', blank=True) # Field name made lowercase.
    stage_bca15 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA15', blank=True) # Field name made lowercase.
    flag_bca15 = models.CharField(max_length=3, db_column='flag_BCA15', blank=True) # Field name made lowercase.
    stage_bca16 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA16', blank=True) # Field name made lowercase.
    flag_bca16 = models.CharField(max_length=3, db_column='flag_BCA16', blank=True) # Field name made lowercase.
    stage_bca17 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA17', blank=True) # Field name made lowercase.
    flag_bca17 = models.CharField(max_length=3, db_column='flag_BCA17', blank=True) # Field name made lowercase.
    stage_bca18 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA18', blank=True) # Field name made lowercase.
    flag_bca18 = models.CharField(max_length=3, db_column='flag_BCA18', blank=True) # Field name made lowercase.
    stage_bca19 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA19', blank=True) # Field name made lowercase.
    flag_bca19 = models.CharField(max_length=3, db_column='flag_BCA19', blank=True) # Field name made lowercase.
    stage_bca2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA2', blank=True) # Field name made lowercase.
    flag_bca2 = models.CharField(max_length=3, db_column='flag_BCA2', blank=True) # Field name made lowercase.
    stage_bca20 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA20', blank=True) # Field name made lowercase.
    flag_bca20 = models.CharField(max_length=3, db_column='flag_BCA20', blank=True) # Field name made lowercase.
    stage_bca3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA3', blank=True) # Field name made lowercase.
    flag_bca3 = models.CharField(max_length=3, db_column='flag_BCA3', blank=True) # Field name made lowercase.
    stage_bca4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA4', blank=True) # Field name made lowercase.
    flag_bca4 = models.CharField(max_length=3, db_column='flag_BCA4', blank=True) # Field name made lowercase.
    stage_bca5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA5', blank=True) # Field name made lowercase.
    flag_bca5 = models.CharField(max_length=3, db_column='flag_BCA5', blank=True) # Field name made lowercase.
    stage_bca6 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA6', blank=True) # Field name made lowercase.
    flag_bca6 = models.CharField(max_length=3, db_column='flag_BCA6', blank=True) # Field name made lowercase.
    stage_bca7 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA7', blank=True) # Field name made lowercase.
    flag_bca7 = models.CharField(max_length=3, db_column='flag_BCA7', blank=True) # Field name made lowercase.
    stage_bca8 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA8', blank=True) # Field name made lowercase.
    flag_bca8 = models.CharField(max_length=3, db_column='flag_BCA8', blank=True) # Field name made lowercase.
    stage_bca9 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BCA9', blank=True) # Field name made lowercase.
    flag_bca9 = models.CharField(max_length=3, db_column='flag_BCA9', blank=True) # Field name made lowercase.
    stage_bottle_creek_at_rookery_branch = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Bottle_Creek_at_Rookery_Branch', blank=True) # Field name made lowercase.
    flag_bottle_creek_at_rookery_branch = models.CharField(max_length=3, db_column='flag_Bottle_Creek_at_Rookery_Branch', blank=True) # Field name made lowercase.
    stage_br = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BR', blank=True) # Field name made lowercase.
    flag_br = models.CharField(max_length=3, db_column='flag_BR', blank=True) # Field name made lowercase.
    stage_broad_river_near_the_cutoff = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Broad_River_near_the_Cutoff', blank=True) # Field name made lowercase.
    flag_broad_river_near_the_cutoff = models.CharField(max_length=3, db_column='flag_Broad_River_near_the_Cutoff', blank=True) # Field name made lowercase.
    stage_upstream_broad_river = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Upstream_Broad_River', blank=True) # Field name made lowercase.
    flag_upstream_broad_river = models.CharField(max_length=3, db_column='flag_Upstream_Broad_River', blank=True) # Field name made lowercase.
    stage_bsc = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_BSC', blank=True) # Field name made lowercase.
    flag_bsc = models.CharField(max_length=3, db_column='flag_BSC', blank=True) # Field name made lowercase.
    stage_c111_wetland_east_of_fiu_lter_tsph5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_C111_wetland_east_of_FIU_LTER_TSPH5', blank=True) # Field name made lowercase.
    flag_c111_wetland_east_of_fiu_lter_tsph5 = models.CharField(max_length=3, db_column='flag_C111_wetland_east_of_FIU_LTER_TSPH5', blank=True) # Field name made lowercase.
    stage_chatham_river_near_the_watson_place = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Chatham_River_near_the_Watson_Place', blank=True) # Field name made lowercase.
    flag_chatham_river_near_the_watson_place = models.CharField(max_length=3, db_column='flag_Chatham_River_near_the_Watson_Place', blank=True) # Field name made lowercase.
    stage_cn = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CN', blank=True) # Field name made lowercase.
    flag_cn = models.CharField(max_length=3, db_column='flag_CN', blank=True) # Field name made lowercase.
    stage_cp = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CP', blank=True) # Field name made lowercase.
    flag_cp = models.CharField(max_length=3, db_column='flag_CP', blank=True) # Field name made lowercase.
    stage_cr2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CR2', blank=True) # Field name made lowercase.
    flag_cr2 = models.CharField(max_length=3, db_column='flag_CR2', blank=True) # Field name made lowercase.
    stage_cr3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CR3', blank=True) # Field name made lowercase.
    flag_cr3 = models.CharField(max_length=3, db_column='flag_CR3', blank=True) # Field name made lowercase.
    stage_ct27r = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CT27R', blank=True) # Field name made lowercase.
    flag_ct27r = models.CharField(max_length=3, db_column='flag_CT27R', blank=True) # Field name made lowercase.
    stage_ct50r = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CT50R', blank=True) # Field name made lowercase.
    flag_ct50r = models.CharField(max_length=3, db_column='flag_CT50R', blank=True) # Field name made lowercase.
    stage_cv5nr = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CV5NR', blank=True) # Field name made lowercase.
    flag_cv5nr = models.CharField(max_length=3, db_column='flag_CV5NR', blank=True) # Field name made lowercase.
    stage_cy2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CY2', blank=True) # Field name made lowercase.
    flag_cy2 = models.CharField(max_length=3, db_column='flag_CY2', blank=True) # Field name made lowercase.
    stage_cy3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CY3', blank=True) # Field name made lowercase.
    flag_cy3 = models.CharField(max_length=3, db_column='flag_CY3', blank=True) # Field name made lowercase.
    stage_do1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_DO1', blank=True) # Field name made lowercase.
    flag_do1 = models.CharField(max_length=3, db_column='flag_DO1', blank=True) # Field name made lowercase.
    stage_do2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_DO2', blank=True) # Field name made lowercase.
    flag_do2 = models.CharField(max_length=3, db_column='flag_DO2', blank=True) # Field name made lowercase.
    stage_e112 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_E112', blank=True) # Field name made lowercase.
    flag_e112 = models.CharField(max_length=3, db_column='flag_E112', blank=True) # Field name made lowercase.
    stage_e146 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_E146', blank=True) # Field name made lowercase.
    flag_e146 = models.CharField(max_length=3, db_column='flag_E146', blank=True) # Field name made lowercase.
    stage_eden_1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_1', blank=True) # Field name made lowercase.
    flag_eden_1 = models.CharField(max_length=3, db_column='flag_EDEN_1', blank=True) # Field name made lowercase.
    stage_eden_10 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_10', blank=True) # Field name made lowercase.
    flag_eden_10 = models.CharField(max_length=3, db_column='flag_EDEN_10', blank=True) # Field name made lowercase.
    stage_eden_11 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_11', blank=True) # Field name made lowercase.
    flag_eden_11 = models.CharField(max_length=3, db_column='flag_EDEN_11', blank=True) # Field name made lowercase.
    stage_eden_12 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_12', blank=True) # Field name made lowercase.
    flag_eden_12 = models.CharField(max_length=3, db_column='flag_EDEN_12', blank=True) # Field name made lowercase.
    stage_eden_13 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_13', blank=True) # Field name made lowercase.
    flag_eden_13 = models.CharField(max_length=3, db_column='flag_EDEN_13', blank=True) # Field name made lowercase.
    stage_eden_14 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_14', blank=True) # Field name made lowercase.
    flag_eden_14 = models.CharField(max_length=3, db_column='flag_EDEN_14', blank=True) # Field name made lowercase.
    stage_eden_3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_3', blank=True) # Field name made lowercase.
    flag_eden_3 = models.CharField(max_length=3, db_column='flag_EDEN_3', blank=True) # Field name made lowercase.
    stage_eden_4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_4', blank=True) # Field name made lowercase.
    flag_eden_4 = models.CharField(max_length=3, db_column='flag_EDEN_4', blank=True) # Field name made lowercase.
    stage_eden_5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_5', blank=True) # Field name made lowercase.
    flag_eden_5 = models.CharField(max_length=3, db_column='flag_EDEN_5', blank=True) # Field name made lowercase.
    stage_eden_6 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_6', blank=True) # Field name made lowercase.
    flag_eden_6 = models.CharField(max_length=3, db_column='flag_EDEN_6', blank=True) # Field name made lowercase.
    stage_eden_7 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_7', blank=True) # Field name made lowercase.
    flag_eden_7 = models.CharField(max_length=3, db_column='flag_EDEN_7', blank=True) # Field name made lowercase.
    stage_eden_8 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_8', blank=True) # Field name made lowercase.
    flag_eden_8 = models.CharField(max_length=3, db_column='flag_EDEN_8', blank=True) # Field name made lowercase.
    stage_eden_9 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EDEN_9', blank=True) # Field name made lowercase.
    flag_eden_9 = models.CharField(max_length=3, db_column='flag_EDEN_9', blank=True) # Field name made lowercase.
    stage_ep1r = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EP1R', blank=True) # Field name made lowercase.
    flag_ep1r = models.CharField(max_length=3, db_column='flag_EP1R', blank=True) # Field name made lowercase.
    stage_epsw = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EPSW', blank=True) # Field name made lowercase.
    flag_epsw = models.CharField(max_length=3, db_column='flag_EPSW', blank=True) # Field name made lowercase.
    stage_ever4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER4', blank=True) # Field name made lowercase.
    flag_ever4 = models.CharField(max_length=3, db_column='flag_EVER4', blank=True) # Field name made lowercase.
    stage_ever5a = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER5A', blank=True) # Field name made lowercase.
    flag_ever5a = models.CharField(max_length=3, db_column='flag_EVER5A', blank=True) # Field name made lowercase.
    stage_ever5b = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER5B', blank=True) # Field name made lowercase.
    flag_ever5b = models.CharField(max_length=3, db_column='flag_EVER5B', blank=True) # Field name made lowercase.
    stage_ever6 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER6', blank=True) # Field name made lowercase.
    flag_ever6 = models.CharField(max_length=3, db_column='flag_EVER6', blank=True) # Field name made lowercase.
    stage_ever7 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER7', blank=True) # Field name made lowercase.
    flag_ever7 = models.CharField(max_length=3, db_column='flag_EVER7', blank=True) # Field name made lowercase.
    stage_ever8 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_EVER8', blank=True) # Field name made lowercase.
    flag_ever8 = models.CharField(max_length=3, db_column='flag_EVER8', blank=True) # Field name made lowercase.
    stage_g_1251 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-1251', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_1251 = models.CharField(max_length=3, db_column='flag_G-1251', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_1502 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-1502', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_1502 = models.CharField(max_length=3, db_column='flag_G-1502', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3272 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3272', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3272 = models.CharField(max_length=3, db_column='flag_G-3272', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3273 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3273', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3273 = models.CharField(max_length=3, db_column='flag_G-3273', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_620 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-620', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_620 = models.CharField(max_length=3, db_column='flag_G-620', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g119_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G119_H', blank=True) # Field name made lowercase.
    flag_g119_h = models.CharField(max_length=3, db_column='flag_G119_H', blank=True) # Field name made lowercase.
    stage_g119_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G119_T', blank=True) # Field name made lowercase.
    flag_g119_t = models.CharField(max_length=3, db_column='flag_G119_T', blank=True) # Field name made lowercase.
    stage_g211_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G211_H', blank=True) # Field name made lowercase.
    flag_g211_h = models.CharField(max_length=3, db_column='flag_G211_H', blank=True) # Field name made lowercase.
    stage_g211_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G211_T', blank=True) # Field name made lowercase.
    flag_g211_t = models.CharField(max_length=3, db_column='flag_G211_T', blank=True) # Field name made lowercase.
    stage_g251_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G251_T', blank=True) # Field name made lowercase.
    flag_g251_t = models.CharField(max_length=3, db_column='flag_G251_T', blank=True) # Field name made lowercase.
    stage_g300_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G300_T', blank=True) # Field name made lowercase.
    flag_g300_t = models.CharField(max_length=3, db_column='flag_G300_T', blank=True) # Field name made lowercase.
    stage_g301_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G301_T', blank=True) # Field name made lowercase.
    flag_g301_t = models.CharField(max_length=3, db_column='flag_G301_T', blank=True) # Field name made lowercase.
    stage_g338_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G338_T', blank=True) # Field name made lowercase.
    flag_g338_t = models.CharField(max_length=3, db_column='flag_G338_T', blank=True) # Field name made lowercase.
    stage_g339_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G339_H', blank=True) # Field name made lowercase.
    flag_g339_h = models.CharField(max_length=3, db_column='flag_G339_H', blank=True) # Field name made lowercase.
    stage_g339_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G339_T', blank=True) # Field name made lowercase.
    flag_g339_t = models.CharField(max_length=3, db_column='flag_G339_T', blank=True) # Field name made lowercase.
    stage_harney_river = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Harney_River', blank=True) # Field name made lowercase.
    flag_harney_river = models.CharField(max_length=3, db_column='flag_Harney_River', blank=True) # Field name made lowercase.
    stage_joe_bay_2e = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Joe_Bay_2E', blank=True) # Field name made lowercase.
    flag_joe_bay_2e = models.CharField(max_length=3, db_column='flag_Joe_Bay_2E', blank=True) # Field name made lowercase.
    stage_l28_gap = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L28_GAP', blank=True) # Field name made lowercase.
    flag_l28_gap = models.CharField(max_length=3, db_column='flag_L28_GAP', blank=True) # Field name made lowercase.
    stage_l28s1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L28S1', blank=True) # Field name made lowercase.
    flag_l28s1 = models.CharField(max_length=3, db_column='flag_L28S1', blank=True) # Field name made lowercase.
    stage_l28s2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L28S2', blank=True) # Field name made lowercase.
    flag_l28s2 = models.CharField(max_length=3, db_column='flag_L28S2', blank=True) # Field name made lowercase.
    stage_l31nn = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31NN', blank=True) # Field name made lowercase.
    flag_l31nn = models.CharField(max_length=3, db_column='flag_L31NN', blank=True) # Field name made lowercase.
    stage_l31ns = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31NS', blank=True) # Field name made lowercase.
    flag_l31ns = models.CharField(max_length=3, db_column='flag_L31NS', blank=True) # Field name made lowercase.
    stage_l31n_1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31N_1', blank=True) # Field name made lowercase.
    flag_l31n_1 = models.CharField(max_length=3, db_column='flag_L31N_1', blank=True) # Field name made lowercase.
    stage_l31n_3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31N_3', blank=True) # Field name made lowercase.
    flag_l31n_3 = models.CharField(max_length=3, db_column='flag_L31N_3', blank=True) # Field name made lowercase.
    stage_l31n_4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31N_4', blank=True) # Field name made lowercase.
    flag_l31n_4 = models.CharField(max_length=3, db_column='flag_L31N_4', blank=True) # Field name made lowercase.
    stage_l31n_5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31N_5', blank=True) # Field name made lowercase.
    flag_l31n_5 = models.CharField(max_length=3, db_column='flag_L31N_5', blank=True) # Field name made lowercase.
    stage_l31n_7 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31N_7', blank=True) # Field name made lowercase.
    flag_l31n_7 = models.CharField(max_length=3, db_column='flag_L31N_7', blank=True) # Field name made lowercase.
    stage_l31w = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_L31W', blank=True) # Field name made lowercase.
    flag_l31w = models.CharField(max_length=3, db_column='flag_L31W', blank=True) # Field name made lowercase.
    stage_lo1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LO1', blank=True) # Field name made lowercase.
    flag_lo1 = models.CharField(max_length=3, db_column='flag_LO1', blank=True) # Field name made lowercase.
    stage_lo2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LO2', blank=True) # Field name made lowercase.
    flag_lo2 = models.CharField(max_length=3, db_column='flag_LO2', blank=True) # Field name made lowercase.
    stage_lo3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LO3', blank=True) # Field name made lowercase.
    flag_lo3 = models.CharField(max_length=3, db_column='flag_LO3', blank=True) # Field name made lowercase.
    stage_loop1_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LOOP1_H', blank=True) # Field name made lowercase.
    flag_loop1_h = models.CharField(max_length=3, db_column='flag_LOOP1_H', blank=True) # Field name made lowercase.
    stage_loop1_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LOOP1_T', blank=True) # Field name made lowercase.
    flag_loop1_t = models.CharField(max_length=3, db_column='flag_LOOP1_T', blank=True) # Field name made lowercase.
    stage_loop2_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LOOP2_H', blank=True) # Field name made lowercase.
    flag_loop2_h = models.CharField(max_length=3, db_column='flag_LOOP2_H', blank=True) # Field name made lowercase.
    stage_loop2_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_LOOP2_T', blank=True) # Field name made lowercase.
    flag_loop2_t = models.CharField(max_length=3, db_column='flag_LOOP2_T', blank=True) # Field name made lowercase.
    stage_lopez_river_near_lopez_campsite = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Lopez_River_Near_Lopez_Campsite', blank=True) # Field name made lowercase.
    flag_lopez_river_near_lopez_campsite = models.CharField(max_length=3, db_column='flag_Lopez_River_Near_Lopez_Campsite', blank=True) # Field name made lowercase.
    stage_lostmans_river_below_second_bay = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Lostmans_River_below_Second_Bay', blank=True) # Field name made lowercase.
    flag_lostmans_river_below_second_bay = models.CharField(max_length=3, db_column='flag_Lostmans_River_below_Second_Bay', blank=True) # Field name made lowercase.
    stage_upstream_lostmans_river = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Upstream_Lostmans_River', blank=True) # Field name made lowercase.
    flag_upstream_lostmans_river = models.CharField(max_length=3, db_column='flag_Upstream_Lostmans_River', blank=True) # Field name made lowercase.
    stage_mccormick_creek_at_mouth = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_McCormick_Creek_at_mouth', blank=True) # Field name made lowercase.
    flag_mccormick_creek_at_mouth = models.CharField(max_length=3, db_column='flag_McCormick_Creek_at_mouth', blank=True) # Field name made lowercase.
    stage_met_1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_MET-1', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_met_1 = models.CharField(max_length=3, db_column='flag_MET-1', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_mud_creek_at_mouth = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Mud_Creek_at_mouth', blank=True) # Field name made lowercase.
    flag_mud_creek_at_mouth = models.CharField(max_length=3, db_column='flag_Mud_Creek_at_mouth', blank=True) # Field name made lowercase.
    stage_ncl = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NCL', blank=True) # Field name made lowercase.
    flag_ncl = models.CharField(max_length=3, db_column='flag_NCL', blank=True) # Field name made lowercase.
    stage_nesrs1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NESRS1', blank=True) # Field name made lowercase.
    flag_nesrs1 = models.CharField(max_length=3, db_column='flag_NESRS1', blank=True) # Field name made lowercase.
    stage_nesrs2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NESRS2', blank=True) # Field name made lowercase.
    flag_nesrs2 = models.CharField(max_length=3, db_column='flag_NESRS2', blank=True) # Field name made lowercase.
    stage_nesrs4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NESRS4', blank=True) # Field name made lowercase.
    flag_nesrs4 = models.CharField(max_length=3, db_column='flag_NESRS4', blank=True) # Field name made lowercase.
    stage_nesrs5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NESRS5', blank=True) # Field name made lowercase.
    flag_nesrs5 = models.CharField(max_length=3, db_column='flag_NESRS5', blank=True) # Field name made lowercase.
    stage_nesrs3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NESRS3', blank=True) # Field name made lowercase.
    flag_nesrs3 = models.CharField(max_length=3, db_column='flag_NESRS3', blank=True) # Field name made lowercase.
    stage_new_river_at_sunday_bay = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_New_River_at_Sunday_Bay', blank=True) # Field name made lowercase.
    flag_new_river_at_sunday_bay = models.CharField(max_length=3, db_column='flag_New_River_at_Sunday_Bay', blank=True) # Field name made lowercase.
    stage_nmp = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NMP', blank=True) # Field name made lowercase.
    flag_nmp = models.CharField(max_length=3, db_column='flag_NMP', blank=True) # Field name made lowercase.
    stage_north_ca1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NORTH_CA1', blank=True) # Field name made lowercase.
    flag_north_ca1 = models.CharField(max_length=3, db_column='flag_NORTH_CA1', blank=True) # Field name made lowercase.
    stage_north_river_upstream_of_cutoff = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_North_River_Upstream_of_Cutoff', blank=True) # Field name made lowercase.
    flag_north_river_upstream_of_cutoff = models.CharField(max_length=3, db_column='flag_North_River_Upstream_of_Cutoff', blank=True) # Field name made lowercase.
    stage_upstream_north_river = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Upstream_North_River', blank=True) # Field name made lowercase.
    flag_upstream_north_river = models.CharField(max_length=3, db_column='flag_Upstream_North_River', blank=True) # Field name made lowercase.
    stage_np201 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP201', blank=True) # Field name made lowercase.
    flag_np201 = models.CharField(max_length=3, db_column='flag_NP201', blank=True) # Field name made lowercase.
    stage_np202 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP202', blank=True) # Field name made lowercase.
    flag_np202 = models.CharField(max_length=3, db_column='flag_NP202', blank=True) # Field name made lowercase.
    stage_np203 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP203', blank=True) # Field name made lowercase.
    flag_np203 = models.CharField(max_length=3, db_column='flag_NP203', blank=True) # Field name made lowercase.
    stage_np205 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP205', blank=True) # Field name made lowercase.
    flag_np205 = models.CharField(max_length=3, db_column='flag_NP205', blank=True) # Field name made lowercase.
    stage_np206 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP206', blank=True) # Field name made lowercase.
    flag_np206 = models.CharField(max_length=3, db_column='flag_NP206', blank=True) # Field name made lowercase.
    stage_np44 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP44', blank=True) # Field name made lowercase.
    flag_np44 = models.CharField(max_length=3, db_column='flag_NP44', blank=True) # Field name made lowercase.
    stage_np46 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP46', blank=True) # Field name made lowercase.
    flag_np46 = models.CharField(max_length=3, db_column='flag_NP46', blank=True) # Field name made lowercase.
    stage_np62 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP62', blank=True) # Field name made lowercase.
    flag_np62 = models.CharField(max_length=3, db_column='flag_NP62', blank=True) # Field name made lowercase.
    stage_np67 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP67', blank=True) # Field name made lowercase.
    flag_np67 = models.CharField(max_length=3, db_column='flag_NP67', blank=True) # Field name made lowercase.
    stage_np72 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NP72', blank=True) # Field name made lowercase.
    flag_np72 = models.CharField(max_length=3, db_column='flag_NP72', blank=True) # Field name made lowercase.
    stage_nr = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NR', blank=True) # Field name made lowercase.
    flag_nr = models.CharField(max_length=3, db_column='flag_NR', blank=True) # Field name made lowercase.
    stage_nts1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NTS1', blank=True) # Field name made lowercase.
    flag_nts1 = models.CharField(max_length=3, db_column='flag_NTS1', blank=True) # Field name made lowercase.
    stage_nts10 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NTS10', blank=True) # Field name made lowercase.
    flag_nts10 = models.CharField(max_length=3, db_column='flag_NTS10', blank=True) # Field name made lowercase.
    stage_nts14 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NTS14', blank=True) # Field name made lowercase.
    flag_nts14 = models.CharField(max_length=3, db_column='flag_NTS14', blank=True) # Field name made lowercase.
    stage_nts18 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NTS18', blank=True) # Field name made lowercase.
    flag_nts18 = models.CharField(max_length=3, db_column='flag_NTS18', blank=True) # Field name made lowercase.
    stage_nwwf = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_NWWF', blank=True) # Field name made lowercase.
    flag_nwwf = models.CharField(max_length=3, db_column='flag_NWWF', blank=True) # Field name made lowercase.
    stage_ol = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_OL', blank=True) # Field name made lowercase.
    flag_ol = models.CharField(max_length=3, db_column='flag_OL', blank=True) # Field name made lowercase.
    stage_ot = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_OT', blank=True) # Field name made lowercase.
    flag_ot = models.CharField(max_length=3, db_column='flag_OT', blank=True) # Field name made lowercase.
    stage_p33 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P33', blank=True) # Field name made lowercase.
    flag_p33 = models.CharField(max_length=3, db_column='flag_P33', blank=True) # Field name made lowercase.
    stage_p34 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P34', blank=True) # Field name made lowercase.
    flag_p34 = models.CharField(max_length=3, db_column='flag_P34', blank=True) # Field name made lowercase.
    stage_p35 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P35', blank=True) # Field name made lowercase.
    flag_p35 = models.CharField(max_length=3, db_column='flag_P35', blank=True) # Field name made lowercase.
    stage_p36 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P36', blank=True) # Field name made lowercase.
    flag_p36 = models.CharField(max_length=3, db_column='flag_P36', blank=True) # Field name made lowercase.
    stage_p37 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P37', blank=True) # Field name made lowercase.
    flag_p37 = models.CharField(max_length=3, db_column='flag_P37', blank=True) # Field name made lowercase.
    stage_p38 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_P38', blank=True) # Field name made lowercase.
    flag_p38 = models.CharField(max_length=3, db_column='flag_P38', blank=True) # Field name made lowercase.
    stage_r127 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_R127', blank=True) # Field name made lowercase.
    flag_r127 = models.CharField(max_length=3, db_column='flag_R127', blank=True) # Field name made lowercase.
    stage_r3110 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_R3110', blank=True) # Field name made lowercase.
    flag_r3110 = models.CharField(max_length=3, db_column='flag_R3110', blank=True) # Field name made lowercase.
    stage_rg1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_RG1', blank=True) # Field name made lowercase.
    flag_rg1 = models.CharField(max_length=3, db_column='flag_RG1', blank=True) # Field name made lowercase.
    stage_rg2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_RG2', blank=True) # Field name made lowercase.
    flag_rg2 = models.CharField(max_length=3, db_column='flag_RG2', blank=True) # Field name made lowercase.
    stage_s10a_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10A_T', blank=True) # Field name made lowercase.
    flag_s10a_t = models.CharField(max_length=3, db_column='flag_S10A_T', blank=True) # Field name made lowercase.
    stage_s10a_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10A_H', blank=True) # Field name made lowercase.
    flag_s10a_h = models.CharField(max_length=3, db_column='flag_S10A_H', blank=True) # Field name made lowercase.
    stage_s10c_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10C_T', blank=True) # Field name made lowercase.
    flag_s10c_t = models.CharField(max_length=3, db_column='flag_S10C_T', blank=True) # Field name made lowercase.
    stage_s10c_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10C_H', blank=True) # Field name made lowercase.
    flag_s10c_h = models.CharField(max_length=3, db_column='flag_S10C_H', blank=True) # Field name made lowercase.
    stage_s10d_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10D_T', blank=True) # Field name made lowercase.
    flag_s10d_t = models.CharField(max_length=3, db_column='flag_S10D_T', blank=True) # Field name made lowercase.
    stage_s10d_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S10D_H', blank=True) # Field name made lowercase.
    flag_s10d_h = models.CharField(max_length=3, db_column='flag_S10D_H', blank=True) # Field name made lowercase.
    stage_s11a_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11A_T', blank=True) # Field name made lowercase.
    flag_s11a_t = models.CharField(max_length=3, db_column='flag_S11A_T', blank=True) # Field name made lowercase.
    stage_s11a_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11A_H', blank=True) # Field name made lowercase.
    flag_s11a_h = models.CharField(max_length=3, db_column='flag_S11A_H', blank=True) # Field name made lowercase.
    stage_s11b_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11B_T', blank=True) # Field name made lowercase.
    flag_s11b_t = models.CharField(max_length=3, db_column='flag_S11B_T', blank=True) # Field name made lowercase.
    stage_s11b_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11B_H', blank=True) # Field name made lowercase.
    flag_s11b_h = models.CharField(max_length=3, db_column='flag_S11B_H', blank=True) # Field name made lowercase.
    stage_s11c_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11C_T', blank=True) # Field name made lowercase.
    flag_s11c_t = models.CharField(max_length=3, db_column='flag_S11C_T', blank=True) # Field name made lowercase.
    stage_s11c_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S11C_H', blank=True) # Field name made lowercase.
    flag_s11c_h = models.CharField(max_length=3, db_column='flag_S11C_H', blank=True) # Field name made lowercase.
    stage_s12a_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12A_T', blank=True) # Field name made lowercase.
    flag_s12a_t = models.CharField(max_length=3, db_column='flag_S12A_T', blank=True) # Field name made lowercase.
    stage_s12a_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12A_H', blank=True) # Field name made lowercase.
    flag_s12a_h = models.CharField(max_length=3, db_column='flag_S12A_H', blank=True) # Field name made lowercase.
    stage_s12b_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12B_T', blank=True) # Field name made lowercase.
    flag_s12b_t = models.CharField(max_length=3, db_column='flag_S12B_T', blank=True) # Field name made lowercase.
    stage_s12b_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12B_H', blank=True) # Field name made lowercase.
    flag_s12b_h = models.CharField(max_length=3, db_column='flag_S12B_H', blank=True) # Field name made lowercase.
    stage_s12c_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12C_T', blank=True) # Field name made lowercase.
    flag_s12c_t = models.CharField(max_length=3, db_column='flag_S12C_T', blank=True) # Field name made lowercase.
    stage_s12c_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12C_H', blank=True) # Field name made lowercase.
    flag_s12c_h = models.CharField(max_length=3, db_column='flag_S12C_H', blank=True) # Field name made lowercase.
    stage_s12d_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12D_T', blank=True) # Field name made lowercase.
    flag_s12d_t = models.CharField(max_length=3, db_column='flag_S12D_T', blank=True) # Field name made lowercase.
    stage_s12d_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S12D_H', blank=True) # Field name made lowercase.
    flag_s12d_h = models.CharField(max_length=3, db_column='flag_S12D_H', blank=True) # Field name made lowercase.
    stage_s140_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S140_H', blank=True) # Field name made lowercase.
    flag_s140_h = models.CharField(max_length=3, db_column='flag_S140_H', blank=True) # Field name made lowercase.
    stage_s140_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S140_T', blank=True) # Field name made lowercase.
    flag_s140_t = models.CharField(max_length=3, db_column='flag_S140_T', blank=True) # Field name made lowercase.
    stage_s141_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S141_H', blank=True) # Field name made lowercase.
    flag_s141_h = models.CharField(max_length=3, db_column='flag_S141_H', blank=True) # Field name made lowercase.
    stage_s141_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S141_T', blank=True) # Field name made lowercase.
    flag_s141_t = models.CharField(max_length=3, db_column='flag_S141_T', blank=True) # Field name made lowercase.
    stage_s142_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S142_H', blank=True) # Field name made lowercase.
    flag_s142_h = models.CharField(max_length=3, db_column='flag_S142_H', blank=True) # Field name made lowercase.
    stage_s142_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S142_T', blank=True) # Field name made lowercase.
    flag_s142_t = models.CharField(max_length=3, db_column='flag_S142_T', blank=True) # Field name made lowercase.
    stage_s143_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S143_T', blank=True) # Field name made lowercase.
    flag_s143_t = models.CharField(max_length=3, db_column='flag_S143_T', blank=True) # Field name made lowercase.
    stage_s144_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S144_H', blank=True) # Field name made lowercase.
    flag_s144_h = models.CharField(max_length=3, db_column='flag_S144_H', blank=True) # Field name made lowercase.
    stage_s144_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S144_T', blank=True) # Field name made lowercase.
    flag_s144_t = models.CharField(max_length=3, db_column='flag_S144_T', blank=True) # Field name made lowercase.
    stage_s145_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S145_H', blank=True) # Field name made lowercase.
    flag_s145_h = models.CharField(max_length=3, db_column='flag_S145_H', blank=True) # Field name made lowercase.
    stage_s145_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S145_T', blank=True) # Field name made lowercase.
    flag_s145_t = models.CharField(max_length=3, db_column='flag_S145_T', blank=True) # Field name made lowercase.
    stage_s146_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S146_H', blank=True) # Field name made lowercase.
    flag_s146_h = models.CharField(max_length=3, db_column='flag_S146_H', blank=True) # Field name made lowercase.
    stage_s146_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S146_T', blank=True) # Field name made lowercase.
    flag_s146_t = models.CharField(max_length=3, db_column='flag_S146_T', blank=True) # Field name made lowercase.
    stage_s150_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S150_T', blank=True) # Field name made lowercase.
    flag_s150_t = models.CharField(max_length=3, db_column='flag_S150_T', blank=True) # Field name made lowercase.
    stage_s151_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S151_H', blank=True) # Field name made lowercase.
    flag_s151_h = models.CharField(max_length=3, db_column='flag_S151_H', blank=True) # Field name made lowercase.
    stage_s151_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S151_T', blank=True) # Field name made lowercase.
    flag_s151_t = models.CharField(max_length=3, db_column='flag_S151_T', blank=True) # Field name made lowercase.
    stage_s175_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S175_H', blank=True) # Field name made lowercase.
    flag_s175_h = models.CharField(max_length=3, db_column='flag_S175_H', blank=True) # Field name made lowercase.
    stage_s175_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S175_T', blank=True) # Field name made lowercase.
    flag_s175_t = models.CharField(max_length=3, db_column='flag_S175_T', blank=True) # Field name made lowercase.
    stage_s18c_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S18C_T', blank=True) # Field name made lowercase.
    flag_s18c_t = models.CharField(max_length=3, db_column='flag_S18C_T', blank=True) # Field name made lowercase.
    stage_s190_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S190_H', blank=True) # Field name made lowercase.
    flag_s190_h = models.CharField(max_length=3, db_column='flag_S190_H', blank=True) # Field name made lowercase.
    stage_s190_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S190_T', blank=True) # Field name made lowercase.
    flag_s190_t = models.CharField(max_length=3, db_column='flag_S190_T', blank=True) # Field name made lowercase.
    stage_s31_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S31_H', blank=True) # Field name made lowercase.
    flag_s31_h = models.CharField(max_length=3, db_column='flag_S31_H', blank=True) # Field name made lowercase.
    stage_s332_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S332_T', blank=True) # Field name made lowercase.
    flag_s332_t = models.CharField(max_length=3, db_column='flag_S332_T', blank=True) # Field name made lowercase.
    stage_s332b_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S332B_T', blank=True) # Field name made lowercase.
    flag_s332b_t = models.CharField(max_length=3, db_column='flag_S332B_T', blank=True) # Field name made lowercase.
    stage_s332d_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S332D_T', blank=True) # Field name made lowercase.
    flag_s332d_t = models.CharField(max_length=3, db_column='flag_S332D_T', blank=True) # Field name made lowercase.
    stage_s333_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S333_H', blank=True) # Field name made lowercase.
    flag_s333_h = models.CharField(max_length=3, db_column='flag_S333_H', blank=True) # Field name made lowercase.
    stage_s333_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S333_T', blank=True) # Field name made lowercase.
    flag_s333_t = models.CharField(max_length=3, db_column='flag_S333_T', blank=True) # Field name made lowercase.
    stage_s334_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S334_H', blank=True) # Field name made lowercase.
    flag_s334_h = models.CharField(max_length=3, db_column='flag_S334_H', blank=True) # Field name made lowercase.
    stage_s334_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S334_T', blank=True) # Field name made lowercase.
    flag_s334_t = models.CharField(max_length=3, db_column='flag_S334_T', blank=True) # Field name made lowercase.
    stage_s335_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S335_H', blank=True) # Field name made lowercase.
    flag_s335_h = models.CharField(max_length=3, db_column='flag_S335_H', blank=True) # Field name made lowercase.
    stage_s335_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S335_T', blank=True) # Field name made lowercase.
    flag_s335_t = models.CharField(max_length=3, db_column='flag_S335_T', blank=True) # Field name made lowercase.
    stage_s336_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S336_H', blank=True) # Field name made lowercase.
    flag_s336_h = models.CharField(max_length=3, db_column='flag_S336_H', blank=True) # Field name made lowercase.
    stage_s336_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S336_T', blank=True) # Field name made lowercase.
    flag_s336_t = models.CharField(max_length=3, db_column='flag_S336_T', blank=True) # Field name made lowercase.
    stage_s337_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S337_T', blank=True) # Field name made lowercase.
    flag_s337_t = models.CharField(max_length=3, db_column='flag_S337_T', blank=True) # Field name made lowercase.
    stage_s339_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S339_H', blank=True) # Field name made lowercase.
    flag_s339_h = models.CharField(max_length=3, db_column='flag_S339_H', blank=True) # Field name made lowercase.
    stage_s339_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S339_T', blank=True) # Field name made lowercase.
    flag_s339_t = models.CharField(max_length=3, db_column='flag_S339_T', blank=True) # Field name made lowercase.
    stage_s34_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S34_H', blank=True) # Field name made lowercase.
    flag_s34_h = models.CharField(max_length=3, db_column='flag_S34_H', blank=True) # Field name made lowercase.
    stage_s340_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S340_H', blank=True) # Field name made lowercase.
    flag_s340_h = models.CharField(max_length=3, db_column='flag_S340_H', blank=True) # Field name made lowercase.
    stage_s340_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S340_T', blank=True) # Field name made lowercase.
    flag_s340_t = models.CharField(max_length=3, db_column='flag_S340_T', blank=True) # Field name made lowercase.
    stage_s343a_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S343A_H', blank=True) # Field name made lowercase.
    flag_s343a_h = models.CharField(max_length=3, db_column='flag_S343A_H', blank=True) # Field name made lowercase.
    stage_s343a_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S343A_T', blank=True) # Field name made lowercase.
    flag_s343a_t = models.CharField(max_length=3, db_column='flag_S343A_T', blank=True) # Field name made lowercase.
    stage_s343b_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S343B_H', blank=True) # Field name made lowercase.
    flag_s343b_h = models.CharField(max_length=3, db_column='flag_S343B_H', blank=True) # Field name made lowercase.
    stage_s343b_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S343B_T', blank=True) # Field name made lowercase.
    flag_s343b_t = models.CharField(max_length=3, db_column='flag_S343B_T', blank=True) # Field name made lowercase.
    stage_s344_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S344_H', blank=True) # Field name made lowercase.
    flag_s344_h = models.CharField(max_length=3, db_column='flag_S344_H', blank=True) # Field name made lowercase.
    stage_s344_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S344_T', blank=True) # Field name made lowercase.
    flag_s344_t = models.CharField(max_length=3, db_column='flag_S344_T', blank=True) # Field name made lowercase.
    stage_s380_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S380_H', blank=True) # Field name made lowercase.
    flag_s380_h = models.CharField(max_length=3, db_column='flag_S380_H', blank=True) # Field name made lowercase.
    stage_s39_h = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S39_H', blank=True) # Field name made lowercase.
    flag_s39_h = models.CharField(max_length=3, db_column='flag_S39_H', blank=True) # Field name made lowercase.
    stage_s7_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S7_T', blank=True) # Field name made lowercase.
    flag_s7_t = models.CharField(max_length=3, db_column='flag_S7_T', blank=True) # Field name made lowercase.
    stage_s8_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S8_T', blank=True) # Field name made lowercase.
    flag_s8_t = models.CharField(max_length=3, db_column='flag_S8_T', blank=True) # Field name made lowercase.
    stage_s9a_t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_S9A_T', blank=True) # Field name made lowercase.
    flag_s9a_t = models.CharField(max_length=3, db_column='flag_S9A_T', blank=True) # Field name made lowercase.
    stage_sh1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SH1', blank=True) # Field name made lowercase.
    flag_sh1 = models.CharField(max_length=3, db_column='flag_SH1', blank=True) # Field name made lowercase.
    stage_sh2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SH2', blank=True) # Field name made lowercase.
    flag_sh2 = models.CharField(max_length=3, db_column='flag_SH2', blank=True) # Field name made lowercase.
    stage_sh3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SH3', blank=True) # Field name made lowercase.
    flag_sh3 = models.CharField(max_length=3, db_column='flag_SH3', blank=True) # Field name made lowercase.
    stage_sh4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SH4', blank=True) # Field name made lowercase.
    flag_sh4 = models.CharField(max_length=3, db_column='flag_SH4', blank=True) # Field name made lowercase.
    stage_sh5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SH5', blank=True) # Field name made lowercase.
    flag_sh5 = models.CharField(max_length=3, db_column='flag_SH5', blank=True) # Field name made lowercase.
    stage_shark_river_below_gunboat_island = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Shark_River_Below_Gunboat_Island', blank=True) # Field name made lowercase.
    flag_shark_river_below_gunboat_island = models.CharField(max_length=3, db_column='flag_Shark_River_Below_Gunboat_Island', blank=True) # Field name made lowercase.
    stage_site_17 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_17', blank=True) # Field name made lowercase.
    flag_site_17 = models.CharField(max_length=3, db_column='flag_SITE_17', blank=True) # Field name made lowercase.
    stage_site_19 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_19', blank=True) # Field name made lowercase.
    flag_site_19 = models.CharField(max_length=3, db_column='flag_SITE_19', blank=True) # Field name made lowercase.
    stage_site_62 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_62', blank=True) # Field name made lowercase.
    flag_site_62 = models.CharField(max_length=3, db_column='flag_SITE_62', blank=True) # Field name made lowercase.
    stage_site_63 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_63', blank=True) # Field name made lowercase.
    flag_site_63 = models.CharField(max_length=3, db_column='flag_SITE_63', blank=True) # Field name made lowercase.
    stage_site_64 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_64', blank=True) # Field name made lowercase.
    flag_site_64 = models.CharField(max_length=3, db_column='flag_SITE_64', blank=True) # Field name made lowercase.
    stage_site_65 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_65', blank=True) # Field name made lowercase.
    flag_site_65 = models.CharField(max_length=3, db_column='flag_SITE_65', blank=True) # Field name made lowercase.
    stage_site_69e = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_69E', blank=True) # Field name made lowercase.
    flag_site_69e = models.CharField(max_length=3, db_column='flag_SITE_69E', blank=True) # Field name made lowercase.
    stage_site_69w = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_69W', blank=True) # Field name made lowercase.
    flag_site_69w = models.CharField(max_length=3, db_column='flag_SITE_69W', blank=True) # Field name made lowercase.
    stage_site_7 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_7', blank=True) # Field name made lowercase.
    flag_site_7 = models.CharField(max_length=3, db_column='flag_SITE_7', blank=True) # Field name made lowercase.
    stage_site_71 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_71', blank=True) # Field name made lowercase.
    flag_site_71 = models.CharField(max_length=3, db_column='flag_SITE_71', blank=True) # Field name made lowercase.
    stage_site_76 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_76', blank=True) # Field name made lowercase.
    flag_site_76 = models.CharField(max_length=3, db_column='flag_SITE_76', blank=True) # Field name made lowercase.
    stage_site_8c = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_8C', blank=True) # Field name made lowercase.
    flag_site_8c = models.CharField(max_length=3, db_column='flag_SITE_8C', blank=True) # Field name made lowercase.
    stage_site_8t = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_8T', blank=True) # Field name made lowercase.
    flag_site_8t = models.CharField(max_length=3, db_column='flag_SITE_8T', blank=True) # Field name made lowercase.
    stage_site_9 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_9', blank=True) # Field name made lowercase.
    flag_site_9 = models.CharField(max_length=3, db_column='flag_SITE_9', blank=True) # Field name made lowercase.
    stage_site_99 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SITE_99', blank=True) # Field name made lowercase.
    flag_site_99 = models.CharField(max_length=3, db_column='flag_SITE_99', blank=True) # Field name made lowercase.
    stage_south_ca1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SOUTH_CA1', blank=True) # Field name made lowercase.
    flag_south_ca1 = models.CharField(max_length=3, db_column='flag_SOUTH_CA1', blank=True) # Field name made lowercase.
    stage_sp = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SP', blank=True) # Field name made lowercase.
    flag_sp = models.CharField(max_length=3, db_column='flag_SP', blank=True) # Field name made lowercase.
    stage_sr1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SR1', blank=True) # Field name made lowercase.
    flag_sr1 = models.CharField(max_length=3, db_column='flag_SR1', blank=True) # Field name made lowercase.
    stage_srs1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SRS1', blank=True) # Field name made lowercase.
    flag_srs1 = models.CharField(max_length=3, db_column='flag_SRS1', blank=True) # Field name made lowercase.
    stage_stillwater_creek = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Stillwater_Creek', blank=True) # Field name made lowercase.
    flag_stillwater_creek = models.CharField(max_length=3, db_column='flag_Stillwater_Creek', blank=True) # Field name made lowercase.
    stage_taylor_river_at_mouth = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Taylor_River_at_mouth', blank=True) # Field name made lowercase.
    flag_taylor_river_at_mouth = models.CharField(max_length=3, db_column='flag_Taylor_River_at_mouth', blank=True) # Field name made lowercase.
    stage_taylor_slough_wetland_at_e146 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Taylor_Slough_wetland_at_E146', blank=True) # Field name made lowercase.
    flag_taylor_slough_wetland_at_e146 = models.CharField(max_length=3, db_column='flag_Taylor_Slough_wetland_at_E146', blank=True) # Field name made lowercase.
    stage_upstream_taylor_river = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Upstream_Taylor_River', blank=True) # Field name made lowercase.
    flag_upstream_taylor_river = models.CharField(max_length=3, db_column='flag_Upstream_Taylor_River', blank=True) # Field name made lowercase.
    stage_te = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TE', blank=True) # Field name made lowercase.
    flag_te = models.CharField(max_length=3, db_column='flag_TE', blank=True) # Field name made lowercase.
    stage_ti_8 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TI-8', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_ti_8 = models.CharField(max_length=3, db_column='flag_TI-8', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_ti_9 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TI-9', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_ti_9 = models.CharField(max_length=3, db_column='flag_TI-9', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_tmc = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TMC', blank=True) # Field name made lowercase.
    flag_tmc = models.CharField(max_length=3, db_column='flag_TMC', blank=True) # Field name made lowercase.
    stage_trout_creek_at_mouth = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Trout_Creek_at_mouth', blank=True) # Field name made lowercase.
    flag_trout_creek_at_mouth = models.CharField(max_length=3, db_column='flag_Trout_Creek_at_mouth', blank=True) # Field name made lowercase.
    stage_ts2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TS2', blank=True) # Field name made lowercase.
    flag_ts2 = models.CharField(max_length=3, db_column='flag_TS2', blank=True) # Field name made lowercase.
    stage_tsb = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TSB', blank=True) # Field name made lowercase.
    flag_tsb = models.CharField(max_length=3, db_column='flag_TSB', blank=True) # Field name made lowercase.
    stage_tsh = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_TSH', blank=True) # Field name made lowercase.
    flag_tsh = models.CharField(max_length=3, db_column='flag_TSH', blank=True) # Field name made lowercase.
    stage_turner_river_nr_chokoloskee_island = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_Turner_River_nr_Chokoloskee_Island', blank=True) # Field name made lowercase.
    flag_turner_river_nr_chokoloskee_island = models.CharField(max_length=3, db_column='flag_Turner_River_nr_Chokoloskee_Island', blank=True) # Field name made lowercase.
    stage_w11 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W11', blank=True) # Field name made lowercase.
    flag_w11 = models.CharField(max_length=3, db_column='flag_W11', blank=True) # Field name made lowercase.
    stage_w14 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W14', blank=True) # Field name made lowercase.
    flag_w14 = models.CharField(max_length=3, db_column='flag_W14', blank=True) # Field name made lowercase.
    stage_w15 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W15', blank=True) # Field name made lowercase.
    flag_w15 = models.CharField(max_length=3, db_column='flag_W15', blank=True) # Field name made lowercase.
    stage_w18 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W18', blank=True) # Field name made lowercase.
    flag_w18 = models.CharField(max_length=3, db_column='flag_W18', blank=True) # Field name made lowercase.
    stage_w2 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W2', blank=True) # Field name made lowercase.
    flag_w2 = models.CharField(max_length=3, db_column='flag_W2', blank=True) # Field name made lowercase.
    stage_w5 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_W5', blank=True) # Field name made lowercase.
    flag_w5 = models.CharField(max_length=3, db_column='flag_W5', blank=True) # Field name made lowercase.
    stage_wc2an1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WC2AN1', blank=True) # Field name made lowercase.
    flag_wc2an1 = models.CharField(max_length=3, db_column='flag_WC2AN1', blank=True) # Field name made lowercase.
    stage_wc2as1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WC2AS1', blank=True) # Field name made lowercase.
    flag_wc2as1 = models.CharField(max_length=3, db_column='flag_WC2AS1', blank=True) # Field name made lowercase.
    stage_wca1me = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA1ME', blank=True) # Field name made lowercase.
    flag_wca1me = models.CharField(max_length=3, db_column='flag_WCA1ME', blank=True) # Field name made lowercase.
    stage_wca2e1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2E1', blank=True) # Field name made lowercase.
    flag_wca2e1 = models.CharField(max_length=3, db_column='flag_WCA2E1', blank=True) # Field name made lowercase.
    stage_wca2e4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2E4', blank=True) # Field name made lowercase.
    flag_wca2e4 = models.CharField(max_length=3, db_column='flag_WCA2E4', blank=True) # Field name made lowercase.
    stage_wca2f1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2F1', blank=True) # Field name made lowercase.
    flag_wca2f1 = models.CharField(max_length=3, db_column='flag_WCA2F1', blank=True) # Field name made lowercase.
    stage_wca2f4 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2F4', blank=True) # Field name made lowercase.
    flag_wca2f4 = models.CharField(max_length=3, db_column='flag_WCA2F4', blank=True) # Field name made lowercase.
    stage_wca2rt = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2RT', blank=True) # Field name made lowercase.
    flag_wca2rt = models.CharField(max_length=3, db_column='flag_WCA2RT', blank=True) # Field name made lowercase.
    stage_wca2u1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2U1', blank=True) # Field name made lowercase.
    flag_wca2u1 = models.CharField(max_length=3, db_column='flag_WCA2U1', blank=True) # Field name made lowercase.
    stage_wca2u3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WCA2U3', blank=True) # Field name made lowercase.
    flag_wca2u3 = models.CharField(max_length=3, db_column='flag_WCA2U3', blank=True) # Field name made lowercase.
    stage_west_highway_creek = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_West_Highway_Creek', blank=True) # Field name made lowercase.
    flag_west_highway_creek = models.CharField(max_length=3, db_column='flag_West_Highway_Creek', blank=True) # Field name made lowercase.
    stage_ww = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_WW', blank=True) # Field name made lowercase.
    flag_ww = models.CharField(max_length=3, db_column='flag_WW', blank=True) # Field name made lowercase.
    stage_g_3575 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3575', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3575 = models.CharField(max_length=3, db_column='flag_G-3575', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3577 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3577', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3577 = models.CharField(max_length=3, db_column='flag_G-3577', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3578 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3578', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3578 = models.CharField(max_length=3, db_column='flag_G-3578', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3576 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3576', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3576 = models.CharField(max_length=3, db_column='flag_G-3576', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3574 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3574', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3574 = models.CharField(max_length=3, db_column='flag_G-3574', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_975 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-975', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_975 = models.CharField(max_length=3, db_column='flag_G-975', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3818 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3818', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3818 = models.CharField(max_length=3, db_column='flag_G-3818', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_596 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-596', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_596 = models.CharField(max_length=3, db_column='flag_G-596', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3626 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3626', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3626 = models.CharField(max_length=3, db_column='flag_G-3626', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3628 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3628', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3628 = models.CharField(max_length=3, db_column='flag_G-3628', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3437 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3437', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3437 = models.CharField(max_length=3, db_column='flag_G-3437', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_angel = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_ANGEL', blank=True) # Field name made lowercase.
    flag_angel = models.CharField(max_length=3, db_column='flag_ANGEL', blank=True) # Field name made lowercase.
    stage_rg3 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_RG3', blank=True) # Field name made lowercase.
    flag_rg3 = models.CharField(max_length=3, db_column='flag_RG3', blank=True) # Field name made lowercase.
    stage_g_3567 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3567', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3567 = models.CharField(max_length=3, db_column='flag_G-3567', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_1488 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-1488', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_1488 = models.CharField(max_length=3, db_column='flag_G-1488', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3761 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3761', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3761 = models.CharField(max_length=3, db_column='flag_G-3761', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_g_3676 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_G-3676', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    flag_g_3676 = models.CharField(max_length=3, db_column='flag_G-3676', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    stage_3ane_gw = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3ANE_GW', blank=True) # Field name made lowercase.
    flag_3ane_gw = models.CharField(max_length=3, db_column='flag_3ANE_GW', blank=True) # Field name made lowercase.
    stage_3anw_gw = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_3ANW_GW', blank=True) # Field name made lowercase.
    flag_3anw_gw = models.CharField(max_length=3, db_column='flag_3ANW_GW', blank=True) # Field name made lowercase.
    stage_ch1 = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_CH1', blank=True) # Field name made lowercase.
    flag_ch1 = models.CharField(max_length=3, db_column='flag_CH1', blank=True) # Field name made lowercase.
    stage_sparo = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='stage_SPARO', blank=True) # Field name made lowercase.
    flag_sparo = models.CharField(max_length=3, db_column='flag_SPARO', blank=True) # Field name made lowercase.
    
    def __unicode__(self):
        return u'%s with value %s' % (self.datetime)
    
    class Meta:
        db_table = u'stage'
        managed = False
        ordering = ['datetime']


