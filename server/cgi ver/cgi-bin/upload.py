#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import hashlib
import time
import os
# import dbm.gnu as gdbm
print("Content-Type: text/html")
print()
ip="192.168.0.10"
form = cgi.FieldStorage()
id = form["id"].value
imagedata = form["imagedata"].value
hash = hashlib.md5(imagedata).hexdigest()
create_newid = False
if not id or id == "":
    id = hashlib.md5(os.environ['REMOTE_ADDR'] + str(time.time())).hexdigest()
    create_newid = True

# dbm = gdbm.open('db/id',"c")
# dbm[hash] = id
# dbm.close

with open("uploads/"+hash+".png", mode='wb') as f:
    f.write(imagedata)

headers = {}
if create_newid:
    print({"X-Gyazo-Id":id})
print("http://"+ip+"/uploads/"+hash+".png")