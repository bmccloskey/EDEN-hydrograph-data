EDEN-hydrograph-data
====================

Publish hydrograph pages and data for EDEN (Everglades Depth Estimation Network)

Project Set-up

Environment set-up
1. The requirements listed in requirements.txt must be installed in the Python environment before running this application. 

Certain files will need to be created before the application can be run. These files have not been included in version control for security reasons:
1. local_settings.py
	a. This should be in the same directory as 'settings.py'
2. secure.py
	a. This file contains information required to access the database and should be placed in the same directory as 'views.py'