HEADER_MESSAGE = """
----------------------------------------- MESSAGE ---------------------------------------------
Thank you for retrieving data from the Exploring and Viewing EDEN (EVE)
application. The values entered for the query are reproduced below. Site names
are listed with the USGS code of the parameter measured at that location.

Note:
All times are reported in Eastern Time (EST: UTC-5:00, EDT: UTC-4:00) unless otherwise specified.

Flag Dictionary:

null: original measured value
M: missing value - not value provided by the originating agency, no estimated data available
G: gapfilled - EDEN estimated values to fill gaps in original data
H: hindcast - nominally estimated data from before the period of record for the gage began
E: estimated - timestamps for which measured points were provided by the agencies, but 
               data were identified as spurious and overwritten with EDEN estimated values
"""
EDEN_CONTACT = "Contact:   fake_email@usgs.gov"

END_OF_HEADER = "-----------------------------------------------------------------------------------------------"