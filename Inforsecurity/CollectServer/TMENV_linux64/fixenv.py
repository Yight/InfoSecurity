#!/usr/bin/env python

import os,sys

if os.getcwd().find("ENV")==-1:
	print "please run in DMENV dir!"
	exit(-1)
env = open("bin/pip").readlines()[0]
env = env[2:].split("/bin")[0]
print env
for i in os.listdir("bin"):
	if i ==".svn" or i.startswith("python"):
		continue
	filename = os.path.join("bin",i)
	strorgi = open(filename,"r").read()
	new_env = os.getcwd()
	# print new_env
	strorgi = strorgi.replace(env,new_env)
	open(filename,"w").write(strorgi)
	print filename
