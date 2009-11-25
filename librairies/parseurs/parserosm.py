#!/usr/bin/env python
# -*- coding: utf-8 -*-

from noeud import Noeud
from chemin import Chemin
from miseEnForme import MiseEnForme
import time, math
import MySQLdb as dbm

class Parser:
  minLon = None
  minLat = None
  maxLon = None
  maxLat = None
  
  threads = None
  
  def fabriqueTables(self):
    try:
      self.bdd.execute('CREATE TABLE sources (id INTEGER NOT NULL auto_increment, fichier VARCHAR(500), PRIMARY KEY  (`id`))')
      self.bdd.execute('CREATE TABLE noeuds (id INTEGER PRIMARY KEY, nom VARCHAR(500), longitude DOUBLE PRECISION, latitude DOUBLE PRECISION, couleur VARCHAR(500), epaisseur INTEGER, importance INTEGER, distance INTEGER)')
      self.bdd.execute('CREATE TABLE chemins (id INTEGER PRIMARY KEY, longitudeMin DOUBLE PRECISION, latitudeMin DOUBLE PRECISION, longitudeMax DOUBLE PRECISION, latitudeMax DOUBLE PRECISION, nom VARCHAR(500), couleur VARCHAR(500), epaisseur INTEGER, importance INTEGER, distance INTEGER)')
      self.bdd.execute('CREATE TABLE chemins_noeuds (id INTEGER NOT NULL auto_increment, id_chemin INTEGER, id_noeud INTEGER, PRIMARY KEY  (`id`))')
    except:
      #On a déjà les tables
      pass

  def fabriqueDB(self):
    self.basedonnee = dbm.connect('localhost','root','')
    self.basedonnee.cursor().execute('create database gps')
    self.basedonnee.select_db('gps')
    
  def __init__(self):
    self.miseEnForme = MiseEnForme()
    self.threadBdd = None
    try:
      self.basedonnee = dbm.connect('localhost','root','', 'gps')
    except:
      self.fabriqueDB()
    #self.basedonnee = sqlite.connect('./cartes/cartes.db')
    self.bdd = self.basedonnee.cursor()
    self.fabriqueTables()
    
  def importationOpenStreet(self, fichier, forceReload=False):
    self.bdd.execute("SELECT COUNT(*) FROM sources WHERE fichier = '%s'"%fichier)
    result=self.bdd.fetchall()[0][0]
    if result == 0 or forceReload: #Ce fichier n'a pas été chargé
      print "Chargement de",fichier
      self.mouline(fichier)
    else:
      print fichier,"déjà chargé"
      
  def mouline(self, fichier):
    nomFichier = fichier
    fichier = open(nomFichier, "r")
    self.bdd.execute("INSERT INTO sources (fichier) VALUES ('%s')"%nomFichier)
    currentNode = None
    currentWay = None
    
    couleurdefault = (-1,-1,-1)
    epaisseurdefault = -1
    importancedefault = -1
    
    cptLigne = 0
    for ligne in fichier:
      cptLigne+=1
    fichier.close()
    
    depart = time.time()
    
    cptPos = 0
    fichier = open(nomFichier, "r")
    for ligne in fichier:
      cptPos+=1
      if cptPos % 41 == 0:
        print nomFichier+" : "+str(cptLigne-cptPos)+" lignes (~%.2fs) restantes  \r" %((time.time()-depart)/float(cptPos)*(cptLigne-cptPos)),
      if ligne.strip().startswith("<node id="):
        elements = ligne.split(" ")
        lat= -1
        lon= -1
        id = -1
        for element in elements:
          if element.startswith("id"):
            id=int(element.split("=")[1].replace("\"","").replace("/","").replace(">",""))
          if element.startswith("lat"):
            lat=float(element.split("=")[1].replace("\"","").replace("/","").replace(">",""))
          if element.startswith("lon"):
            lon=float(element.split("=")[1].replace("\"","").replace("/","").replace(">",""))
            
        if self.possedeNoeud(id):
          #print "Node",id,"existe déjà, on oublie"
          pass
        else:
          self.bdd.execute("DELETE FROM noeuds WHERE id=%s"%id)
          self.bdd.execute("INSERT INTO noeuds (id, nom, longitude, latitude, couleur, epaisseur, importance, distance) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s, '%s')"%(
              id,
              "",
              str(lon),
              str(lat),
              str(couleurdefault),
              epaisseurdefault,
              importancedefault,
              str(-1)
            )
          )
          if self.minLon==None:
            self.minLon = lon
            self.minLat = lat
            self.maxLon = lon
            self.maxLat = lat
            
          self.minLon = min(lon, self.minLon)
          self.minLat = min(lat, self.minLat)
          self.maxLon = max(lon, self.maxLon)
          self.maxLat = max(lat, self.maxLat)
        
        currentNode = id
        currentWay = None
        
      elif ligne.strip().startswith("<way id="):
        elements = ligne.split(" ")
        id = -1
        for element in elements:
          if element.startswith("id"):
            id=int(element.split("=")[1].replace("\"","").replace("/","").replace(">",""))
        if self.possedeChemin(id):
          #print "Chemin",id,"existe déjà, on purge ses points"
          self.bdd.execute("DELETE FROM chemins_noeuds WHERE id_chemin=%s"%id)
        else:
          self.bdd.execute("DELETE FROM chemins WHERE id=%s"%id)
          self.bdd.execute("INSERT INTO chemins (id, nom, longitudeMin, latitudeMin, longitudeMax, latitudeMax, couleur, epaisseur, importance, distance) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, '%s')"%(
              id,
              "",
              -1000,
              -1000,
              -1000,
              -1000,
              str(couleurdefault),
              epaisseurdefault,
              importancedefault,
              -1
            )
          )
        currentWay = id
        currentNode = None
            
      elif ligne.strip().startswith("<nd"):
        elements = ligne.split(" ")
        id = -1
        for element in elements:
          if element.startswith("ref"):
            id=int(element.split("=")[1].replace("\"","").replace("/","").replace(">",""))
            self.bdd.execute("INSERT INTO chemins_noeuds (id_chemin, id_noeud) VALUES (%s, %s)"%(currentWay, id))
            chemin = self.getChemin(currentWay)
            noeud = self.getNoeud(id)
            chemin.ajoutePoint(id,{id:noeud})
            self.bdd.execute("UPDATE chemins set longitudeMin='%s', longitudeMax='%s', latitudeMin='%s', latitudeMax='%s' WHERE id=%s"%(str(chemin.lonMin), str(chemin.lonMax), str(chemin.latMin), str(chemin.latMax), currentWay))
            self.setChemin(chemin)
            
      elif ligne.strip().startswith("<tag k=\"name") or (ligne.strip().startswith("<tag k=\"") and ligne.strip().find("_name")>-1):
        nom = ligne.split("=")[2].replace("\"","").replace("/","").replace(">","").strip().replace("'"," ")
        if not nom.startswith("wpt"):
          if currentWay != None:
            nouveauNom = self.getChemin(currentWay).nom.strip()+" "+nom.strip()
            self.bdd.execute("UPDATE chemins set nom='%s' WHERE id=%s"%(nouveauNom, currentWay))
          if currentNode != None:
            nouveauNom = self.getNoeud(currentNode).nom.strip()+" "+nom.strip()
            req = "UPDATE noeuds set nom='%s' WHERE id=%s"%(nouveauNom, currentNode)
            self.bdd.execute(req)
          
      elif ligne.strip().startswith("<tag k=\""):
        objet = None
        if currentWay != None:
          objet = self.getChemin(currentWay)
        if currentNode != None:
          objet = self.getNoeud(currentNode)
        if objet != None:
          tag = ligne.split("=")[1].replace("\"","").replace("/","").replace(">","").replace(" v","").strip().lower()
          valeurs = ligne.split("=")[2].replace("\"","").replace("/","").replace(">","").strip().lower().split(";")
          for valeur in valeurs:
            (couleur, epaisseur, importance, distance) = self.miseEnForme.parseTag(tag, valeur)
  
            if objet.importance < importance:
              objet.importance = importance
              objet.couleur = couleur
              objet.epaisseur = epaisseur
            if objet.distance < distance:
              objet.distance = distance
            
        if currentWay != None:
          self.setChemin(objet)
        if currentNode != None:
          self.setNoeud(objet)
        
      elif ligne.strip().startswith("</osm"): pass
      elif ligne.strip().startswith("</way"): pass
      elif ligne.strip().startswith("</node"): pass
      elif ligne.strip().startswith("<osm"): pass
      elif ligne.strip().startswith("<bound"): pass
      elif ligne.strip().startswith("<?xml"): pass
      elif ligne.strip().startswith("<member"): pass
      elif ligne.strip().startswith("<relation"): pass
      elif ligne.strip().startswith("</member"): pass
      elif ligne.strip().startswith("</relation"): pass
      else:
        print "Balise inconnue : ", ligne.strip()
    print ""
    print "Chargement de",nomFichier,"terminé"
    fichier.close()
    self.basedonnee.commit()
    
  def possedeNoeud(self, id):
    self.bdd.execute("SELECT COUNT(*) FROM noeuds WHERE id=%s"%id)
    result=self.bdd.fetchall()[0][0]
    return result>0

  def possedeChemin(self, id):
    self.bdd.execute("SELECT COUNT(*) FROM chemins WHERE id=%s"%id)
    result=self.bdd.fetchall()[0][0]
    return result>0

  def getChemin(self, id):
    self.bdd.execute("SELECT id, nom, longitudeMin, longitudeMax, latitudeMin, latitudeMax, couleur, epaisseur, importance, distance FROM chemins WHERE id=%s"%id)
    chemins = self.bdd.fetchall()
    cheminOut = None
    for chemin in chemins:
      (id, nom, longitudeMin, longitudeMax, latitudeMin, latitudeMax, couleur, epaisseur, importance, distance) = chemin
      
      #print longitudeMin, longitudeMax, latitudeMin, latitudeMax, g,d,b,h
      
      id = int(id)
      try:
        nom = nom.encode("UTF-8")
      except:
        pass
      epaisseur = int(epaisseur)
      importance = int(importance)
      distance = float(distance)
      
      self.bdd.execute("SELECT nd.longitude, nd.latitude FROM chemins_noeuds cn, noeuds nd WHERE cn.id_chemin=%s AND cn.id_noeud=nd.id ORDER BY cn.id"%id)
      points = self.bdd.fetchall()
      
      pnts=[]
      for point in points:
        lon,lat = point
        
      cheminOut=Chemin()
      cheminOut.nom = ""
      cheminOut.id = id
      cheminOut.tags = []
      cheminOut.couleur = self.couleurStrToCouleur(couleur)
      cheminOut.epaisseur = epaisseur
      cheminOut.importance = importance
      cheminOut.points = pnts
      cheminOut.distance = distance
      cheminOut.latMax = latitudeMax
      cheminOut.latMin = latitudeMin
      cheminOut.lonMax = longitudeMax
      cheminOut.lonMin = longitudeMin
    return cheminOut
  
  def getNoeud(self, id):
    req = "SELECT id, nom, longitude, latitude, couleur, epaisseur, importance, distance FROM noeuds WHERE id=%s"%id
    self.bdd.execute(req)
    for noeud in self.bdd.fetchall():
      (id, nom, longitude, latitude, couleur, epaisseur, importance, distance) = noeud
      id = int(id)
      try:
        nom = nom.encode("UTF-8")
      except:
        pass
      longitude = float(longitude)
      latitude = float(latitude)
      epaisseur = int(epaisseur)
      importance = int(importance)
      distance = float(distance)

      noeud=Noeud()
      noeud.nom = nom
      noeud.id = id
      noeud.tags = []
      noeud.couleur = self.couleurStrToCouleur(couleur)
      noeud.epaisseur = epaisseur
      noeud.importance = importance
      noeud.position = (longitude, latitude, 0)
      noeud.distance = distance
    return noeud
  
  def setNoeud(self, noeud):
    self.bdd.execute("UPDATE noeuds SET nom='%s', longitude='%s', latitude='%s', couleur='%s', epaisseur=%s, importance=%s, distance='%s' WHERE id=%s"%(
        noeud.nom.replace("'"," "),
        str(noeud.position[0]),
        str(noeud.position[1]),
        str(noeud.couleur),
        noeud.epaisseur,
        noeud.importance,
        noeud.distance,
        noeud.id
      )
    )
    
  def setChemin(self, chemin):
    self.bdd.execute("UPDATE chemins SET nom='%s', couleur='%s', epaisseur=%s, importance=%s, distance='%s' WHERE id=%s"%(
        chemin.distance,
        str(chemin.couleur),
        chemin.epaisseur,
        chemin.importance,
        chemin.distance,
        chemin.id
      )
    )

  def couleurStrToCouleur(self, couleur):
    element = couleur[1:-1].split(", ")
    if len(element)==3:
      return (float(element[0]), float(element[1]), float(element[2]), 1)
    elif len(element)==4:
      return (float(element[0]), float(element[1]), float(element[2]), float(element[3]))
    else:
      print "Etrange couleur", couleur
    return (0,0,0,1)

if __name__=="__main__":
  parse = Parser()
  #parse.importationOpenStreet("../cartes/map-tsukuba.osm",True)
  #parse.importationOpenStreet("../cartes/map-tokyo.osm",True)
  parse.importationOpenStreet("../cartes/france.osm",True)