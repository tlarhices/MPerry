#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import xml.parsers.expat
from objets import *

from parserjp import ParserJP
from parserndb import ParserNDB
from parserosm import ParserOSM

class Parser:
  parser = None
  gui = None
  fichiers = None
  lignes = None
  enCours = None
  doitChanger = None
  
  def __init__(self, gui):
    self.gui = gui
    if self.gui != None:
      self.cg = self.gui.cg
    self.fichiers = []
    self.lignes = []
    self.doitChanger = True
    
  def parse(self, BAM=False):
    if BAM:
      self.cg.typeAffichage=self.cg.elements["tout"]
    while self.parseTick() or self.cg.ping():
      pass
    
  def prepareParse(self):
    lst1 = os.listdir("./xml")
    lst2 = os.listdir("./ndb")
    lst3 = os.listdir("./osm")
    lst = []
    for elem in lst1:
      lst.append(os.path.join(".","xml",elem))
    for elem in lst2:
      lst.append(os.path.join(".","ndb",elem))
    for elem in lst3:
      lst.append(os.path.join(".","osm",elem))
      
    fichTaille = {}
    tailles = []
    for fichier in lst:
      taille = os.path.getsize(fichier)
      if not taille in fichTaille.keys():
        fichTaille[taille]=[]
      fichTaille[taille].append(fichier)
      tailles.append(taille)
    d = {}
    for x in tailles:
        d[x] = None
    tailles = d.keys()
    tailles.sort()
    
    lst=[]
    for taille in tailles:
      for fichier in fichTaille[taille]:
        lst.append(fichier)
    
    for fichier in lst:
      if fichier.lower().strip().endswith(".xml"):
        tt=fichier.split("-")
        if len(tt)>2:
          tt = tt[3]
        else:
          tt = fichier.split(".")[0]
    #    if tt in ['AdmArea', 'AdmBdry', 'AdmPt', 'BldA', 'BldL', 'CommBdry', 'CommPt', 'Cstline', 'ElevPt', 'RailCL', 'RdCompt', 'RdEdg', 'WA', 'WL']:
        if tt in ['AdmArea', 'AdmBdry', 'AdmPt', 'BldA', 'BldL', 'CommBdry', 'CommPt', 'Cstline', 'ElevPt', 'RailCL', 'RdCompt', 'RdEdg', 'WA', 'WL']: #'RdEdg', 
    #    if tt in ['AdmArea25000', 'AdmArea', 'AdmBdry', 'AdmBdry25000', 'AdmPt25000', 'AdmPt', 'BldA', 'BldA25000', 'BldA', 'BldA25000', 'BldL', 'Cntr25000', 'CommBdry', 'CommPt', 'Cstline25000', 'Cstline', 'ElevPt', 'ElevPt25000', 'RailCL', 'RailCL25000', 'RdCompt', 'RdEdg25000', 'RdEdg', 'WA', 'WL', 'WL25000']:
          self.fichiers.append(fichier)
      elif fichier.lower().strip().endswith(".ndb"):
        self.fichiers.append(fichier)
      elif fichier.lower().strip().endswith(".osm"):
        self.fichiers.append(fichier)

  def parseTick(self):
    if self.doitChanger:
      if len(self.fichiers)==0:
        print "plus rien a parser"
        if self.enCours!=None:
          self.enCours=None
          self.parser = None
        return False
      f = open(self.fichiers[0])
      self.enCours = self.fichiers[0]
      txt ="Parsage de %s, %i fichiers restants..." %(self.enCours.replace("\\","/").split("/")[-1], len(self.fichiers)+1)
      if self.gui != None:
        self.gui.afficheTexte(txt, orientation="bas", section="parse")
        print txt
      else:
        print txt
      self.fichiers=self.fichiers[1:]
      self.lignes = f.readlines()
      f.close()
      if self.enCours.endswith(".ndb"):
        self.parser = ParserNDB(self.gui)
        self.parser.cg = self.cg
        self.parser.fichiers = [self.enCours]
      elif self.enCours.endswith(".osm"):
        self.parser = ParserOSM(self.gui)
        self.parser.cg = self.cg
        self.parser.fichiers = [self.enCours]
      else:
        OK=False
        i=0
        while not OK:
          if i>=len(self.lignes):
            OK=True
            raw_input("Parseur :: Format de fichier inconnu")
            return
          ligne = self.lignes[i]
          i+=1
          if ligne.lower().strip().startswith("<gi"):
            # JP
            self.parser = ParserJP(self.gui)
            self.parser.cg = self.cg
            self.parser.fichiers = [self.enCours]
            OK=True
    self.doitChanger = not self.parser.parseTick()
    return True
