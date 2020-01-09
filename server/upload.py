#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import cgi
import hashlib
import time
import os
# import dbm.gnu as gdbm
ip="127.0.0.1"
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

with open(f"{hash}.png", mode='wb') as f:
    f.write(imagedata)

headers = {}
if create_newid:
    print({"X-Gyazo-Id":id})
    print(f"http://{ip}/{hash}.png")