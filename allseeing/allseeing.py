#!/usr/bin/env python

import sys, random, json, string

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import werkzeug.security

import ConfigParser
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

db = create_engine(config.get("database", "uri"))
#db.echo = True

metadata = MetaData(db)
users = Table('users', metadata, autoload=True)
follower = Table('follower', metadata, autoload=True)

session = sessionmaker(bind=db)()
conn = db.connect()

userlist = [a[1] for a in session.query(users).all()]

print userlist

for i in userlist:
	for j in userlist:
		if i != j:
			print i,j
			conn.execute(follower.insert().values(follower=i, following=j, confirmed=1))
			# todo: check status of this, and provide a way to add a certain user to everyone

session.commit()