#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import random
import time
import sqlite
import sys
import hashlib

from objets import *
import objets
basedonnee = sqlite.connect('h.db')
bdd = basedonnee.cursor()
objets.basedonnee = basedonnee
objets.bdd = bdd

req = 'SELECT idpolyligne FROM polylignepoint WHERE idpoint IN (SELECT position FROM objet WHERE position!="None")'
bdd.execute(req)
reqStat=bdd.fetchall()
for elem in reqStat:
  print elem
if len(reqStat)==0:
  print ":( elevpt inutile"