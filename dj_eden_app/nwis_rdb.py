import datetime
import types
import pytz
from decimal import Decimal

def timezone_conversion(tz):
    '''
    Returns the time in the specified timezone ('tz')
    in YYYY-MM-DD HH:MM:SS TZ format
    '''
    dt_format = '%Y-%m-%d %H:%M:%S %Z'
    utc_dt = datetime.datetime.utcnow()
    utc = pytz.utc
    op_tz = pytz.timezone(tz)
    utc_time = utc.localize(utc_dt)
    time_in_tz = utc_time.astimezone(op_tz)
    display_time = time_in_tz.strftime(dt_format)
    
    return str(display_time)

def convert_string_tuple(data_string, delimiter):
    '''
    Converts a limited string a tuple for further processing.
    '''
    string_list = data_string.split(delimiter)
    string_tuple = tuple(string_list)
    
    return string_tuple
    

def convert_dms_string_to_decimal(geo_tuple):    
    '''
    Takes a tuple of form ('deg', 'min', 'sec') and
    returns the lat or lon as a decimal number.
    '''
    deg, g_min, sec = (geo_tuple)
    deg_num = Decimal(deg)
    min_num = Decimal(g_min)
    sec_num = Decimal(sec)
    
    dec_60 = Decimal(60)
    sec_conv = sec_num/dec_60
    min_conv = (min_num + sec_conv)/dec_60
    abs_conv = abs(deg_num) + min_conv
    if deg_num < 0:
        conv_complete = abs_conv*(-1)
    else:
        conv_complete = abs_conv
    display_number = round(conv_complete, 2)
    
    return display_number
    

def create_rdb_header(message, contact, header_end, query_info, param_qs):
    '''
    Generates the header for data downloads.
    '''
    nwis_message = message
    nwis_contact = contact
    convert_time = timezone_conversion('US/Eastern')
    download_time = 'Retrieved: %s' % convert_time
    query_info_list = query_info.items()
    site_string = ''

    site_parameter_str = 'Sites and USGS parameters:\n'
    
    for qs_object in param_qs:
        site_name = qs_object.station_name_web
        p_code = qs_object.param
        site_name_display = site_name.encode('utf-8').replace('_', ' ')
        p_code_display = p_code.encode('utf-8')
        site_p_string = 'Station Name: %s, USGS Parameter Code: %s\n' % (site_name_display, p_code_display)
        site_parameter_str += site_p_string
        
    usgs_p_codes = '\nUSGS parameter codes can be searched at: http://nwis.waterdata.usgs.gov/usa/nwis/pmcodes.'
    
    site_parameter_str += usgs_p_codes
        
    for element in query_info_list:
        key, value = element
        display_key = key.replace('_', ' ')

        if type(value) is not types.ListType:
            parameter_value = value
            parameter = '%s: %s\n' % (display_key, parameter_value)
        else:
            continue
            
        site_string += parameter
    header_string = "%s\n%s\n%s\n%s\n%s\n%s\n" % (nwis_message, nwis_contact, download_time, site_string, site_parameter_str, header_end)
    header_as_list = [header_string]
    
    return header_as_list