#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import xml.parsers.expat
from objets import *

class ParserOSM:
  chemin = None
  pile = None
  enCours = None
  fichiers = None
  lignes = None
  tailleFichier = None
  
  def __init__(self, gui):
    self.chemin=[]
    self.pile={}
    self.enCours = None
    self.fichiers = []
    self.lignes = []
    self.tailleFichier = 0
    self.gui=gui
    if self.gui != None:
      self.cg = self.gui.cg
  
  def start_element(self, name, attrs):
    name=name.lower().strip()
    self.chemin.append(name)
    self.pile[str(self.chemin)]=[]
    for clef in attrs:
      self.pile[str(self.chemin)].append(str(clef.encode("utf-8"))+":"+str(attrs[clef].encode("utf-8")))
    
  nodelist={}
    
  def end_element(self, name):
    cg=self.cg
    name=name.lower().strip()
    OK=False
    
    idObj = None
    
    if name == "bounds":
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "tag":
      OK = True
      k, v = self.pile[str(self.chemin)]
      k=":".join(k.split(":")[1:])
      v=":".join(v.split(":")[1:])
      if k=="created_by":
        self.pile[str(self.chemin)] = None
      elif k.startswith("source"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("name"):
        self.pile[str(self.chemin)] = "nom",v
      elif k=="railway":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:LIN":
        self.pile[str(self.chemin)] = "LIN", v
      elif k=="KSJ2:RAC_label":
        self.pile[str(self.chemin)] = "RAC_label", v
      elif k=="KSJ2:INT_label":
        self.pile[str(self.chemin)] = "INT_label",v
      elif k=="KSJ2:STN":
        self.pile[str(self.chemin)] = "STN",v
      elif k=="KSJ2:PRN": #prefecture
        self.pile[str(self.chemin)] = "PRN",v
      elif k=="KSJ2:RAC":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:CON":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:CN2":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:RAS":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:lat":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:LOC":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:long":
        self.pile[str(self.chemin)] = None
      elif k.startswith("is_in"):
        self.pile[str(self.chemin)] = "is_in", v
      elif k.startswith("layer"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("place"):
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:segment":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:OPC":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:coordinate":
        self.pile[str(self.chemin)] = None
      elif k=="source_ref":
        self.pile[str(self.chemin)] = None
      elif k=="ref":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:INT":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:curve_id":
        self.pile[str(self.chemin)] = None
      elif k=="KSJ2:filename":
        self.pile[str(self.chemin)] = None
      elif k.startswith("note"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("maxspeed"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("operator"):
        self.pile[str(self.chemin)] = k,v
      elif k.startswith("leisure"):
        self.pile[str(self.chemin)] = k,v
      elif k.startswith("boundary"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("admin_level"):
        self.pile[str(self.chemin)] = None
      elif k.startswith("lanes"):
        self.pile[str(self.chemin)] = "lanes",v
      elif k.startswith("bridge"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "bridge"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("building"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "building"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("tunnel"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "tunnel"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("foot"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "foot"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("cutting"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "cutting"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("boat"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "boat"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("waterway"):
        self.pile[str(self.chemin)] = k,v
      elif k.startswith("oneway"):
        if v.lower().strip()=="yes":
          self.pile[str(self.chemin)] = "oneway"
        else:
          self.pile[str(self.chemin)] = None
      elif k.startswith("highway"):
        self.pile[str(self.chemin)] = "road",v
      elif k.startswith("route"):
        self.pile[str(self.chemin)] = "road"
      elif k.startswith("type"):
        self.pile[str(self.chemin)] = k,v
      elif k.startswith("shop"):
        self.pile[str(self.chemin)] = "shop",v
      elif k.startswith("barrier"):
        self.pile[str(self.chemin)] = "barrier",v
      elif k.startswith("amenity"):
        self.pile[str(self.chemin)] = "amenity",v
      elif k.startswith("natural"):
        self.pile[str(self.chemin)] = "amenity",v
      else:
        print "Tag inconnu :",k,v
        raw_input()
    elif name == "node":
      OK = True
      changeset, uid, timestamp, lon, visible, version, user, lat, id = self.pile[str(self.chemin)][0:9]
      parametres = self.pile[str(self.chemin)][9:]
      #if len(parametres)>0:
      #  print parametres
      self.nodelist[int(id.split(":")[1])]=int(id.split(":")[1])
      self.nodelist[int(changeset.split(":")[1])]=int(id.split(":")[1])
    elif name == "nd":
      OK = True
      self.pile[str(self.chemin)] = self.nodelist[int(self.pile[str(self.chemin)][0].split(":")[1])]
    elif name == "osm":
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "member":
      OK = True
      ref, role, type = self.pile[str(self.chemin)]
    elif name == "relation":
      OK = True
      changeset, uid, timestamp, visible, version, user, id = self.pile[str(self.chemin)][0:7]
      members = self.pile[str(self.chemin)][7:]
    elif name == "way":
      OK = True
      changeset, uid, timestamp, visible, version, user, id = self.pile[str(self.chemin)][0:7]
      chemins = self.pile[str(self.chemin)][7:]
      try:
        self.pile[str(self.chemin)] = self.nodelist[int(self.pile[str(self.chemin)][0].split(":")[1])]
      except KeyError:
        print ":(", int(self.pile[str(self.chemin)][0].split(":")[1])
    else:
      print
      print '  elif name == "'+name+'":'
      print '    pass'
      
    if idObj!=None:
      obj = self.cg.getObjet(idObj)
      if obj.typeG in self.cg.typeAffichage:
        self.cg.afficheObjet(render, obj, idObj)
    
    if not OK:
      print
      print
      print "fin",name
      for elem in self.pile[str(self.chemin)]:
        print "-",elem
      print "::",name
      raw_input("element inconnu")
      
    if len(self.chemin)>1 and self.pile[str(self.chemin)]!=None:
      self.pile[str(self.chemin[:-1])].append((name, self.pile[str(self.chemin)]))
    #print self.pile[str(self.chemin[:-1])], "<<", name
    self.pile[str(self.chemin)] = None
    del self.pile[str(self.chemin)]
    self.chemin.remove(name)
  
  def char_data(self,data):
    data=data.strip()
    if len(data)>0:
      self.pile[str(self.chemin)].append(data)
    
  def parse(self, BAM=False):
    if BAM:
      self.cg.typeAffichage=self.cg.elements["tout"]
    while self.parseTick() or self.cg.ping():
      pass
    
  def prepareParse(self):
    lst = os.listdir("./xml")
    
    fichTaille = {}
    tailles = []
    for fichier in lst:
      taille = os.path.getsize(os.path.join(".","xml",fichier))
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
      fichier = os.path.join(".","xml",fichier)
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

  def parseTick(self):
    if len(self.lignes)==0:
      if self.enCours!=None:
        shutil.move(self.enCours, os.path.join(".", "osm","fini",self.enCours.replace("\\","/").split("/")[-1]))
      if len(self.fichiers)==0:
        print "plus rien a parser"
        if self.enCours!=None:
          self.enCours=None
        return False
      self.parser = xml.parsers.expat.ParserCreate()
      self.parser.StartElementHandler = self.start_element
      self.parser.EndElementHandler = self.end_element
      self.parser.CharacterDataHandler = self.char_data
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
    if len(self.lignes)%100==0:
      txt = "Parsage de %s\n\rFait : %.2f%%" %(self.enCours.replace("\\","/").split("/")[-1], (1.0-len(self.lignes)*1.0/self.tailleFichier)*100.0)
      if self.gui != None:
        self.gui.afficheTexte(txt, orientation="bas", section="parse")
        print txt
      else:
        print txt
    
    self.parser.Parse(ligne)
    return True
