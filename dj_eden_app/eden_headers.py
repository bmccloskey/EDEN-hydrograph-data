HEADER_MESSAGE = """
----------------------------------------- MESSAGE ---------------------------------------------
Thank you for retrieving data from the Exploring and Viewing EDEN (EVE)
application. The values entered for the query are reproduced below. The reported
values are depths in feet, relative to the NAVD-88 datum.

All times are reported in Eastern Time (EST: UTC-5:00, EDT: UTC-4:00) unless otherwise specified.

Please note: 
Water-level data is periodically updated by the originating agencies. 
Real-time data is updated and replaced by provisional data approximately 45 days after the end of a quarter; 
provisional is updated and replaced by final data approximately 9 months 
after the end of a water year (Sept. 30)."

Flag Dictionary:

O: observed value
M: missing value - no value provided by the originating agency, no estimated data available
E: estimated - EDEN estimated value
D: dry measurement - observed (or estimated) value is below reliable measurement range
"""
EDEN_CONTACT = "Contact:   fake_email@usgs.gov"

END_OF_HEADER = "-----------------------------------------------------------------------------------------------"
