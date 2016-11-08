#!/usr/bin/python
import random

content = {" ": set()}
ports = {"127.0.0.1": random.randint(1024,65535)}
dir = "192.168.0.1"

if "mozart.mp3" in content:
  content["mozart.mp3"].add([dir])
else:
  holder = set([dir])
  print holder
  content["mozart.mp3"] = holder

if "beethoven.mp3" in content:
  content["beethoven.mp3"].add(dir)
else:
  holder = set([dir])
  print holder
  content["beethoven.mp3"] = holder

dir = "192.168.0.3"

if "mozart.mp3" in content:
  content["mozart.mp3"].add(dir)
else:
  holder = set([dir])
  print holder
  content["mozart.mp3"] = holder

dir = "192.168.0.1"

if "mozart.mp3" in content:
  content["mozart.mp3"].add(dir)
else:
  holder = set(dir)
  print holder
  content["mozart.mp3"] = holder

if "mozart.mp3" not in content:
  print "Chido"

for key, val in content.items():
  print key
  for addr in val:
    print addr