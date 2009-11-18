#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandac.PandaModules import *
from tuile import Tuile
import general
import time, os, hashlib
from objets import *

class Affichage:
  enMemoire = None
  elements = None
  
  typeAffichage = None
  NoLoad = False
  tuiles = None
  GPSAltitude = None
  GPSCoord = None
  resX = 0.065
  resY = 0.065
  
  racine=None
  
  objetsAAfficher = None
  objetsAFabriquer = None
  objetsACharger = None
  
  def __init__(self):
    self.racine = NodePath("")
    self.racine.reparentTo(render)
    
    self.elements = {"trains":["railcl"], "eau":["wa", "wl", "cstline"], "routes":["rdcompt", "rdedg"], "communaute":["commbdry", "commpt"], "administration":["admarea", "admpt", "admbdry"], "batiments":["blda", "bldl"], "terrain":["cntr", "elevpt"], "tout":["railcl", "wa", "wl", "cstline", "rdcompt", "rdedg", "commbdry", "commpt", "admarea", "admpt", "admbdry", "blda", "bldl", "cntr", "elevpt"]}

    self.enMemoire={}
    self.typeAffichage = []
    self.tuiles = []
    
    self.objetsAAfficher = []
    self.objetsAFabriquer = []
    self.objetsACharger = []
    
  def debutLigne(self, couleur, depart):
    ls = LineSegs()
    ls.setColor(*couleur)
    ls.setThickness(1.0)
    ls.moveTo(*depart)
    return ls
    
  def nouveauPoint(self, ls, arrivee):
    ls.drawTo(*arrivee)

  def finLigne(self, ls, racine)  :
    racine.attachNewNode(ls.create())
    
  def dessineLigne(self, couleur, depart, arrivee, racine):
    """Dessine une ligne de depart vers arrivée et ne fait pas de doublons"""
    ls = LineSegs()
    ls.setColor(*couleur)
    ls.setThickness(1.0)
    racine.attachNewNode(ls.create())
    ls.moveTo(*depart)
    ls.drawTo(*arrivee)
    racine.attachNewNode(ls.create())
        
  def getCoord(self, point):
    return point.z, point.y, point.x

  def getPoint(self, idPoint):
    pt = Point(idPoint, None, None, None)
    pt.depuisBDD()
    return pt
    
  def getPolyligne(self, idPolyligne):
    pl = Polyligne(idPolyligne, None)
    pl.depuisBDD()
    return pl

  def getPolygone(self, idPolygone):
    pg = Polygone(idPolygone, None, None)
    pg.depuisBDD()
    return pg

  def getObjet(self, idObjet):
    ob = Objet(None, None, None, None, None, None, None, None)
    ob.depuisBDD(idObjet)
    return ob

  def affichePoint(self, point, racine, couleur):
    pt = NodePath("point")
    self.dessineLigne(couleur, self.getCoord(point), self.getCoord(point), pt)
    pt.reparentTo(racine)

  def affichePolyligne(self, polyligne, racine, couleur, boucle=False):
    ligne = NodePath("ligne")
    
    if len(polyligne.points)==0:
      return
    prev=self.getCoord(self.getPoint(polyligne.points[0]))
    #base.camera.setPos(prev[0], 5.0, prev[2])
    #base.camera.lookAt(prev[0], prev[1], prev[2])
    ls = self.debutLigne(couleur, prev)
    for point in polyligne.points[1:]:
      pt = self.getCoord(self.getPoint(point))
      self.nouveauPoint(ls, pt)
      prev = pt
    if boucle:
      self.nouveauPoint(ls, self.getCoord(self.getPoint(polyligne.points[0])))
    self.finLigne(ls, ligne)
    ligne.setAttrib(ColorAttrib.makeVertex()) 
    ligne.flattenStrong()
    ligne.reparentTo(racine)
      
  def affichePolygone(self, polygone, racine, couleur):
    if len(polygone.polylignes)==0:
      return
    
    poly = NodePath("ligne")
    
    if not polygone.plein:
      for polyligne in polygone.polylignes:
        self.affichePolyligne(self.getPolyligne(polyligne), poly, couleur, polygone.clos)
    else:
      print ":("
    poly.setAttrib(ColorAttrib.makeVertex()) 
    poly.flattenStrong()
    poly.reparentTo(racine)

  def afficheObjet(self, racine, objet=None, id=None):
    fichier = os.path.join(".", "bam", str(hashlib.sha512(str(objet)).hexdigest())+".bam")
    if objet.typeG not in self.enMemoire.keys():
      self.enMemoire[objet.typeG]=[]
    for fichierM, truc in self.enMemoire[objet.typeG]:
      if fichierM==fichier:
        return
    if os.path.exists(fichier):
      if self.NoLoad:
        return
      else:
        self.objetsACharger.append((racine, objet, id))
        #rac=loader.loadModel(fichier)#, callback=chargeModel, extraArgs=[racine])
    else:
      self.objetsAFabriquer.append((racine, objet, id))
      
  def ping(self):
    
    deb = time.time()
    
    while time.time()-deb<0.1:
      self.gui.setObjetEnAttente(False)
      if len(self.objetsAAfficher)>0:
        self.gui.setObjetEnAttente(True)
        racine, id, typeG = self.objetsAAfficher[0]
        self.objetsAAfficher = self.objetsAAfficher[1:]
        if typeG in self.typeAffichage:
          obj = self.getObjet(id)
          self.afficheObjet(racine, obj, id)
      if len(self.objetsACharger)>0:
        self.gui.setObjetEnAttente(True)
        racine, objet, id = self.objetsACharger[0]
        self.objetsACharger = self.objetsACharger[1:]
        if objet.typeG in self.typeAffichage:
          self.chargeObjet(racine, objet, id)
      if len(self.objetsAFabriquer)>0:
        self.gui.setObjetEnAttente(True)
        racine, objet, id = self.objetsAFabriquer[0]
        self.objetsAFabriquer = self.objetsAFabriquer[1:]
        if objet.typeG in self.typeAffichage:
          self.fabriqueObjet(racine, objet, id)
      
  def chargeObjet(self, racine, objet, id):
    fichier = os.path.join(".", "bam", str(hashlib.sha512(str(objet)).hexdigest())+".bam")
    rac=loader.loadModel(fichier)
    rac.reparentTo(racine)
    rac.setPythonTag("inst", objet)
    rac.setPythonTag("id", str(id))
    self.enMemoire[objet.typeG].append((fichier, rac))
    return rac
      
  def fabriqueObjet(self, racine, objet, id):
    fichier = os.path.join(".", "bam", str(hashlib.sha512(str(objet)).hexdigest())+".bam")
    if objet.typeG=="admarea":
      couleur = (1.0, 1.0, 1.0, 1.0)
    elif objet.typeG=="admpt":
      couleur = (1.0, 1.0, 1.0, 1.0)
    elif objet.typeG=="admbdry":
      couleur = (1.0, 1.0, 1.0, 1.0)
    elif objet.typeG=="blda":
      couleur = (0.9, 0.0, 0.9, 1.0)
    elif objet.typeG=="bldl":
      couleur = (0.9, 0.0, 0.9, 1.0)
    elif objet.typeG=="cntr":
      couleur = (0.1, 0.8, 1.0, 1.0)
    elif objet.typeG=="commbdry":
      couleur = (1.0, 1.0, 1.0, 1.0)
    elif objet.typeG=="commpt":
      couleur = (1.0, 1.0, 1.0, 1.0)
    elif objet.typeG=="cstline":
      couleur = (0.0, 0.0, 0.8, 1.0)
    elif objet.typeG=="railcl":
      couleur = (0.0, 0.0, 0.0, 1.0)
    elif objet.typeG=="rdcompt":
      couleur = (1.0, 0.0, 0.0, 1.0)
    elif objet.typeG=="rdedg":
      couleur = (1.0, 0.0, 0.0, 1.0)
    elif objet.typeG=="wa":
      couleur = (0.0, 0.0, 1.0, 1.0)
    elif objet.typeG=="wl":
      couleur = (0.0, 0.0, 1.0, 1.0)
    elif objet.typeG=="elevpt":
      return
      couleur = (1.0, 0.8, 1.0, 1.0)
    else:
      couleur = (0.0, 1.0, 0.0, 1.0)
      print "Type inconnu :",objet.typeG


    rac = NodePath("objet"+str(id))
    if objet.position != "None" and objet.position != None:
      self.affichePoint(self.getPoint(objet.position), rac, couleur)
    if objet.zone != "None" and objet.zone != None:
      self.affichePolygone(self.getPolygone(objet.zone), rac, couleur)
    rac.setAttrib(ColorAttrib.makeVertex()) 
    rac.flattenStrong()
    rac.writeBamFile(fichier)
    rac.reparentTo(racine)
    rac.setPythonTag("inst", objet)
    rac.setPythonTag("id", str(id))
    self.enMemoire[objet.typeG].append((fichier, rac))
    return rac
    
  def effaceCategorie(self, categorie):
    if self.typeAffichage.count(categorie)>0:
      self.typeAffichage.remove(categorie)
    if not categorie in self.enMemoire.keys():
      return
      
    for fichier, racine in self.enMemoire[categorie]:
      racine.detachNode()
      racine.removeNode()
    self.enMemoire[categorie] = []
    
  def tuile(self, coord):
    vx = pow(10, len(str(self.resX))-2)
    vy = pow(10, len(str(self.resY))-2)
    X = float(int(coord[0]*vx))/vx
    Y = float(int(coord[2]*vy))/vy
    return Tuile(((X,Y),(X+self.resX*2, Y+self.resY*2)))
    
  def voisinsTuile(self, tuile):
    (Xb, Yb), BD = tuile.coord
    tuiles = []
    x = Xb-self.resX*2
    while x<=Xb+self.resX*3:
      y = Yb-self.resY*2
      while y<=Yb+self.resY*3:
        tuiles.append(Tuile(((x,y),(x+self.resX*2, y+self.resY*2))))
        y+=self.resY*2
      x+=self.resX*2
    if len(tuiles)!=9:
      raw_input("Erreur trouvage des tuiles voisines %i au lieu de 9 produites"%len(tuiles))
      print tuiles
      raw_input("Erreur trouvage des tuiles voisines %i au lieu de 9 produites"%len(tuiles))
    return tuiles
    
  def sansFenetre(self):
    self.racine = NodePath("")
    self.NoLoad = True
    
  def buildBam(self):
    self.sansFenetre()
    self.charge(self.elements["tout"])

  def charge(self, test, tuile=None):
    if tuile!=None:
      return self.chargeTuiles(test, tuile)
      
    req = "SELECT id, typeG FROM objet WHERE ("
    for type in test:
      if not type in self.typeAffichage:
        self.typeAffichage.append(type)
      req+= "typeG='"+type+"' OR "
    
    req+="1=0)"
    print req
    general.bdd.execute(req)
    reqObjets=general.bdd.fetchall()
    self.chargeObjets(reqObjets, self.racine)

  def dessineCarre(self, couleur, ptA, ptB, racine):
    xA, yA = ptA
    xB, yB = ptB
    rac = NodePath("")
    self.dessineLigne(couleur, (xA, 0.0, yA), (xB, 0.0, yA), rac)
    self.dessineLigne(couleur, (xB, 0.0, yA), (xB, 0.0, yB), rac)
    self.dessineLigne(couleur, (xB, 0.0, yB), (xA, 0.0, yB), rac)
    self.dessineLigne(couleur, (xA, 0.0, yB), (xA, 0.0, yA), rac)
    rac.reparentTo(racine)
    return rac
    

  def chargeTuiles(self, tableau, tuile):
    inutiles = self.tuiles[:]
    self.dessineCarre((0.0, 0.0, 1.0, 1.0), tuile.coord[0], tuile.coord[1], self.racine)
    for voisin in self.voisinsTuile(tuile):
      fabriqueTuile = True
      for test in self.tuiles[:]:
        if test.memeTuile(voisin):
          fabriqueTuile=False
          if self.tuiles.count(test)>0:
            inutiles.remove(test)
      if fabriqueTuile:
        self.dessineCarre((1.0, 0.0, 0.0, 1.0), voisin.coord[0], voisin.coord[1], self.racine)
        self.chargeTuile(tableau, voisin, self.racine)
    for tuile in inutiles:
      if tuile in self.tuiles:
        self.tuiles.remove(tuile)
    
  def chargeTuile(self, test, tuile, racine):
    fichier = os.path.join(".", "bam", str(hashlib.sha512(str(tuile)).hexdigest())+".bam")
    if os.path.exists(fichier):
      racineTuile=loader.loadModel(fichier)#, callback=chargeModel, extraArgs=[racine])
    else:
      req = "SELECT id, typeG FROM objet WHERE ("
      for type in test:
        if not type in self.typeAffichage:
          self.typeAffichage.append(type)
        req+= "typeG='"+type+"' OR "

      reqIdPoint = "SELECT DISTINCT id FROM point WHERE (x<"+str(tuile.coord[1][0])+" AND x>"+str(tuile.coord[0][0])+" AND z<"+str(tuile.coord[1][1])+" AND z>"+str(tuile.coord[0][1])+")"
      reqIdPolyligne = "SELECT DISTINCT idpolyligne FROM polylignepoint WHERE idpoint IN ("+reqIdPoint+")"
      reqIdPolygone = "SELECT DISTINCT idpolygone FROM polygonepolyligne WHERE idpolyligne IN ("+reqIdPolyligne+")"
        
      req+="1=0) AND (position=='None' OR position in ("+reqIdPolyligne+")) AND (zone=='None' OR zone in ("+reqIdPolygone+"))"
      
      general.bdd.execute(req)
      reqObjets=general.bdd.fetchall()
      racineTuile = NodePath("Tuile"+str(tuile.coord))
      tuile.objets = self.chargeObjets(reqObjets, racineTuile)
      racineTuile.writeBamFile(fichier)
    racineTuile.reparentTo(racine)
    
    self.tuiles.append(tuile)

  def chargeObjets(self, reqObjets, racine):
    majTime = -1000
    cpt=0.0
    objets = []
    print "Chargement de %i objets" %len(reqObjets)
    for objet in reqObjets:
      cpt+=1.0
      if time.time() - majTime > 1.5:
        txt = "Progression : %.2f%%" %(cpt/len(reqObjets)*100.0)
        self.gui.afficheTexte(txt, orientation="haut", section="charge", forceRefresh=True)
        majTime = time.time()
      self.objetsAAfficher.append((racine, objet[0], objet[1]))
      #objets.append(self.afficheObjet(racine, self.getObjet(objet[0]), objet[0]))
    return objets
