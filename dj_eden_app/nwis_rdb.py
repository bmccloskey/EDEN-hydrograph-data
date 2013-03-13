import datetime
import types

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

def create_rdf_header(warning, contact, header_end, query_info):
    nwis_warning = warning
    nwis_contact = contact
    download_date = datetime.datetime.utcnow()
    download_time = 'Retrieved: %s UTC' % download_date
    query_info_list = query_info.items()
    parameter_string = ''
    for element in query_info_list:
        key, value = element
        if type(value) is types.ListType:
            tmp_list = []
            for item in value:
                parameter_value = item.encode('utf-8')
                tmp_list.append(parameter_value.replace('_', ' '))
            string_of_list = ', '.join(tmp_list)
            parameter = '%s: %s\n' % (key, string_of_list)
        else:
            parameter_value = value
            parameter = '%s: %s\n' % (key, parameter_value)
            
        parameter_string += parameter
    header_string = "%s\n%s\n%s\n%s\n%s\n" % (nwis_warning, nwis_contact, download_time, parameter_string, header_end)
    header_as_list = [header_string]
    
    return header_as_list