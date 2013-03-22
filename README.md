EDEN-hydrograph-data
====================

Publish hydrograph pages and data for EDEN (Everglades Depth Estimation Network)

Project Set-up

Environment set-up  
1. The requirements listed in requirements.txt must be installed in the Python environment before running this application.   

Certain files will need to be created before the application can be run. These files have not been included in version control for security reasons:  

1. local_settings.py  

	a. Copy the file 'eden_project/local_settings_template.py' file to 'eden_project/local_settings.py and correct the database connection information in the copy.
	b. Specify the location of static files in the server in the 'STATICFILES_DIRS' field.  
	c. Request 'secret_key.py' from CIDA staff and save it in the eden_project directory.

2. secure.py  

	a. Copy the 'secure_template.py' file to "secure.py" and correct the database credentials in the copy.

Remember, don't check any security credentials (passwords, user names, private URLs) in to version control.

