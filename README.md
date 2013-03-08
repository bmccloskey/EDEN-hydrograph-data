EDEN-hydrograph-data
====================

Publish hydrograph pages and data for EDEN (Everglades Depth Estimation Network)

Project Set-up

Environment set-up
1. The requirements listed in requirements.txt must be installed in the Python environment before running this application. 

Certain files will need to be created before the application can be run. These files have not been included in version control for security reasons:
\
1. local_settings.py
\
	a. Edit the 'local_settings_template.py' file with database connection information.
	b. Specify the location of static files in the server in the 'STATICFILES_DIRS' field.
	c. Request 'secret_key.py' from CIDA staff.
	d. The file should be renamed 'local_settings.py'. It and 'secret_key.py' should be saved in the same directory as 'settings.py' (eden_project).
\	
2. secure.py
\
	a. Edit the 'secure_template.py' file with database connection information.
	b. The file should be renamed 'secure.py' and saved in the same directory as 'hydrograph.py' (dj_eden_app).