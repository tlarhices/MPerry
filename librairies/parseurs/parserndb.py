#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import xml.parsers.expat
from objets import *

class ParserNDB:
  chemin = None
  pile = None
  enCours = None
  fichiers = None
  lignes = None
  tailleFichier = None
  
  def __init__(self, gui):
    self.enCours = None
    self.fichiers = []
    self.lignes = []
    self.tailleFichier = 0
    self.gui=gui
    if self.gui != None:
      self.cg = self.gui.cg
  
  def parse(self, BAM=False):
    if BAM:
      self.cg.typeAffichage=self.cg.elements["tout"]
    while self.parseTick() or self.cg.ping():
      pass
    
  def parseTick(self):
    if len(self.lignes)==0:
      if self.enCours!=None:
        shutil.move(self.enCours, os.path.join(".", "ndb","fini",self.enCours.replace("\\","/").split("/")[-1]))
      if len(self.fichiers)==0:
        print "plus rien a parser"
        if self.enCours!=None:
          self.enCours=None
        return False
      f = open(self.fichiers[0])
      self.enCours = self.fichiers[0]
      txt ="Parsage de %s..." %(self.enCours.replace("\\","/").split("/")[-1])
      if self.gui != None:
        self.gui.afficheTexte(txt, orientation="bas", section="parse")
      else:
        print txt
      self.fichiers=self.fichiers[1:]
      self.lignes = f.readlines()
      self.tailleFichier = len(self.lignes)
      f.close()
    ligne = self.lignes[0]
    self.lignes = self.lignes[1:]
    if len(self.lignes)%10==0:
      txt = "Parsage de %s\n\rFait : %.2f%%" %(self.enCours.replace("\\","/").split("/")[-1], (1.0-len(self.lignes)*1.0/self.tailleFichier)*100.0)
      if self.gui != None:
        self.gui.afficheTexte(txt, orientation="bas", section="parse")
        print txt
      else:
        print txt

    if not ligne.strip().startswith(";"):
      if not ligne.strip().lower().startswith("meshsize"):
        ll = len(ligne)+2
        while ll!=len(ligne):
          ll=len(ligne)
          ligne = ligne.replace("  ", " ")
        ligne = ligne.decode("sjis")
        elements = ligne.split(" ")
        romaji, long, lat, taille, katakana, i1, i2, i3, i4, i5 = elements
        idp = Point(None, long, 0.0, lat).versBDD()
        a=str(katakana.encode("utf-8"))
        b=str(romaji.encode("utf-8"))
        a = b+" "+a
        a = a.decode("utf-8")
        obj = Objet(dateDeb="-1", dateFin="-1", position=str(idp), zone=None, typeG="ndb", type="ndb", nom=a, codeAdministratif=None)
        idObj = obj.versBDD()
        self.cg.afficheObjet(render, obj, idObj)
    return True
