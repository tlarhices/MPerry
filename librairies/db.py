#!/usr/bin/env python
# -*- coding: utf-8 -*-
import general
import sqlite

class DB:
  basedonnee = None
  bdd = None
  def __init__(self):
    self.basedonnee = sqlite.connect('g.db')
    self.bdd = self.basedonnee.cursor()
    try:
      self.bdd.execute('CREATE TABLE point (id INTEGER, x FLOAT, y FLOAT, z FLOAT)')
      self.basedonnee.commit()
      print "Création de la table point"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polyligne (id INTEGER, interpolation VARCHAR(100))')
      self.basedonnee.commit()
      print "Création de la table polyligne"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polylignehash (idpolyligne INTEGER, hash VARCHAR(256))')
      self.basedonnee.commit()
      print "Création de la table polylignehash"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polylignepoint (idpolyligne INTEGER, idpoint INTEGER)')
      self.basedonnee.commit()
      print "Création de la table polylignepoint"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polygone (id INTEGER, plein INTEGER, clos INTEGER, interieur INTEGER, orientation VARCHAR2(10))')
      self.basedonnee.commit()
      print "Création de la table polygone"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polygonehash (idpolygone INTEGER, hash VARCHAR(256))')
      self.basedonnee.commit()
      print "Création de la table polygonehash"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE polygonepolyligne (idpolygone INTEGER, idpolyligne INTEGER)')
      self.basedonnee.commit()
      print "Création de la table polygonepoint"
    except sqlite.DatabaseError:
      pass
    try:
      self.bdd.execute('CREATE TABLE objet (id INTEGER, dateDeb VARCHAR2(100), dateFin VARCHAR2(100), position VARCHAR2(100), zone VARCHAR2(100), typeG VARCHAR2(512), type VARCHAR2(512), nom VARCHAR2(512), codeAdministratif VARCHAR2(512))')
      self.basedonnee.commit()
      print "Création de la table objet"
    except sqlite.DatabaseError:
      pass  
      
    general.basedonnee = self.basedonnee
    general.bdd = self.bdd
