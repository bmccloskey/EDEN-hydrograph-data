import datetime
import types
import pytz

HEADER_MESSAGE = """
----------------------------------------- MESSAGE ---------------------------------------------
Thank you for retrieving data from the Exploring and Viewing EDEN (EVE)
application.

Note:
All times are reported in Eastern Time unless otherwise specified.

Flag Dictionary:

null: original measured value
M: missing value - not value provided by the originating agency, no estimated data available
G: gapfilled - EDEN estimated values to fill gaps in original data
H: hindcast - nominally estimated data from before the period of record for the gage began
E: estimated - timestamps for which measured points were provided by the agencies, but 
               data was identified as spurious and overwritten with EDEN estimated values
"""
EDEN_CONTACT = "Contact:   fake_email@usgs.gov"

END_OF_HEADER = "---------------------------------------------------------------------------------------------"

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

def create_rdb_header(warning, contact, header_end, query_info, data_type):
    nwis_warning = warning
    nwis_contact = contact
    convert_time = timezone_conversion('US/Eastern')
    download_time = 'Retrieved: %s' % convert_time
    query_info_list = query_info.items()
    parameter_string = ''
    returned_data = 'Parameter Requested: %s' % data_type
    for element in query_info_list:
        key, value = element
        display_key = key.replace('_', ' ')
        if type(value) is types.ListType:
            tmp_list = []
            for item in value:
                parameter_value = item.encode('utf-8')
                tmp_list.append(parameter_value.replace('_', ' '))
            string_of_list = ', '.join(tmp_list)
            parameter = '%s: %s\n' % (display_key, string_of_list)
        else:
            parameter_value = value
            parameter = '%s: %s\n' % (display_key, parameter_value)
            
        parameter_string += parameter
    parameter_string += returned_data
    header_string = "%s\n%s\n%s\n%s\n%s\n" % (nwis_warning, nwis_contact, download_time, parameter_string, header_end)
    header_as_list = [header_string]
    
    return header_as_list