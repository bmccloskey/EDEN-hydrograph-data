import re
import MySQLdb as mdb
import sys

from secure import DB_USER, DB_PASSWORD, DB_SCHEMA, DB_HOST

db_host = DB_HOST
db_user = DB_USER
db_password = DB_PASSWORD
db_schema = DB_SCHEMA

try:
	con = None

	con = mdb.connect(db_host, db_user, db_password, db_schema);

	cur = con.cursor()

	cur.execute("select * from stage limit 1")
	
	onion = ''

	view = "create view stage_view as \n"

	pat = re.compile('stage_(.+)')

	for i in cur.description:
		name = i[0]
		m = pat.match(name)
		if m :
			stn = m.group(1)
			view += onion
			view += "(select '%s' as station, datetime as datetime, 'stage_%s' as stage, 'flag_%s' as flag from stage)\n" % (stn, stn, stn)
			onion = " union\n"
	print view
except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close()
