#!/usr/bin/env python

import sys, random, json, string

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import werkzeug.security

import ConfigParser
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

f = open("/usr/share/dict/words", "r")
words = [a[:-1] for a in f.readlines()]


db = create_engine(config.get("database", "uri"))
#db.echo = True

metadata = MetaData(db)
users = Table('users', metadata, autoload=True)
apikey = Table('api_key', metadata, autoload=True)

session = sessionmaker(bind=db)()
conn = db.connect()

userlist = []

for i in range(20):
	user = {'username': random.choice(words) + random.choice(words),
			'email': random.choice(words) + "@example.com",
			'password': random.choice(words) + ("%4i" % random.randint(0,9999)),
			'apikey': "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])}
	userlist.append(user)
	conn.execute(users.insert().values(username=user['username'], email=user['email'], 
									   password=werkzeug.security.generate_password_hash(user['password'])))
	conn.execute(apikey.insert().values(key=user['apikey'], user=user['username'], name='test'))

f = open("users.json",'w')
f.write(json.dumps(userlist))
f.close()

session.commit()