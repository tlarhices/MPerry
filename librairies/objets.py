#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite
import hashlib

import general

class Point:
  id = None
  x = None
  y = None
  z = None
  def __init__(self, id, x,y,z):
    self.id = id
    self.x = x
    self.y = y
    self.z = z
    
  def __repr__(self):
    return "("+str(self.x)+";"+str(self.y)+";"+str(self.z)+")"

  def depuisBDD(self, id=None):
    if id!=None:
      self.id = id
    req = "SELECT x, y, z FROM point WHERE id="+str(self.id)
    general.bdd.execute(req)
    reqCharge=general.bdd.fetchall()
    self.x = float(reqCharge[0][0])
    self.y = float(reqCharge[0][1])
    self.z = float(reqCharge[0][2])
  def majBDD(self):
    req = "UPDATE point SET x="+str(self.x)+", y="+str(self.y)+", z="+str(self.z)+" WHERE id="+str(self.id)
    general.bdd.execute(req)
    general.basedonnee.commit()
  def versBDD(self):
    req = "SELECT id FROM point WHERE x="+str(self.x)+" AND z="+str(self.z)+ " ORDER BY id ASC"
    general.bdd.execute(req)
    reqExiste=general.bdd.fetchall()
    if len(reqExiste)>0:
      self.id = int(reqExiste[0][0])
      return self.id
    else:
      general.bdd.execute("SELECT MAX(id) FROM point")
      reqID=general.bdd.fetchall()
      if len(reqID)<=0:
        id=0
      else:
        if reqID[0][0]==None:
          id=0
        else:
          id=int(reqID[0][0])+1
      req = 'INSERT INTO point(id, x, y, z) VALUES('+str(id)+','+str(self.x)+','+str(self.y)+','+str(self.z)+')'
      general.bdd.execute(req)
      general.basedonnee.commit()
      self.id=id
      return id

    
class Polyligne:
  id = None
  points = None
  interpolation = None
  def __init__(self, id, interpolation):
    self.id = id
    self.interpolation = interpolation
    self.points = []
  def ajoutePoint(self, point):
    self.points.append(point)
  def fusionne(self, polyligne):
    if not str(polyligne).startswith("Polyligne"):
      polyligne = Polyligne(polyligne, None)
      polyligne.depuisBDD()
    for point in polyligne.points:
      if point not in self.points:
        self.ajoutePoint(point)
  def __repr__(self):
    out = "Polyligne("+str(self.interpolation)+";"
    if len(self.points)>0:
      for point in self.points[:-1]:
        out+=str(point)+";"
      out+=str(self.points[-1])
    else:
      out+="Vide"
    out += ")"
    return out
    
  def depuisBDD(self, id=None):
    if id!=None:
      self.id = id
      
    req = 'SELECT interpolation FROM polyligne WHERE id='+str(self.id)
    general.bdd.execute(req)
    reqInterp=general.bdd.fetchall()
    self.interpolation=reqInterp[0][0]
    
    req = 'SELECT idpoint FROM polylignepoint WHERE idpolyligne='+str(self.id)
    general.bdd.execute(req)
    reqPoints=general.bdd.fetchall()
    for point in reqPoints:
      self.ajoutePoint(int(point[0]))
  def majBDD(self):
    req = "DELETE FROM polyligne WHERE id="+str(self.id)
    general.bdd.execute(req)
    req = "DELETE FROM polylignepoint WHERE idpolyligne="+str(self.id)
    general.bdd.execute(req)
    self.versBDD(self.id)
  def versBDD(self, id=None):
    pts = self.points[:]
    pts.sort()
    hashV = str(hashlib.sha512(str(pts)).hexdigest())
    req = "SELECT idpolyligne FROM polylignehash WHERE hash='"+hashV+ "' ORDER BY idpolyligne ASC"
    general.bdd.execute(req)
    reqExiste=general.bdd.fetchall()
    if len(reqExiste)>0 and id==None:
      self.id = int(reqExiste[0][0])
      return self.id
    else:
      if id==None:
        general.bdd.execute("SELECT MAX(id) FROM polyligne")
        reqID=general.bdd.fetchall()
        if len(reqID)<=0:
          id=0
        else:
          if reqID[0][0]==None:
            id=0
          else:
            id=int(reqID[0][0])+1
      req = 'INSERT INTO polyligne (id, interpolation) VALUES( '+str(id)+', "'+self.interpolation+'")'
      general.bdd.execute(req)
      req = 'INSERT INTO polylignehash (idpolyligne, hash) VALUES( '+str(id)+', "'+hashV+'")'
      general.bdd.execute(req)
      for point in self.points:
        req = 'INSERT INTO polylignepoint (idpolyligne, idpoint) VALUES( '+str(id)+', '+str(point)+')'
        general.bdd.execute(req)
      general.basedonnee.commit()
      self.id = id
      return self.id
      
class Polygone:
  id = None
  polylignes = None
  plein = None
  clos = None
  interieur = None
  orientation = None
  
  def __init__(self, id, plein, clos):
    self.id = id
    self.plein = plein
    self.clos = clos
    self.polylignes = []
    self.interieur = True
    self.orientation = "+"
    
  def ajoutePolyligne(self, polyligne):
    self.polylignes.append(polyligne)
  def fusionne(self, polygone):
    if not str(polygone).startswith("Polygone"):
      polygone = Polygone(polygone, None, None)
      polygone.depuisBDD()
    for polyligne in polygone.polylignes:
      if polyligne not in self.polylignes:
        self.ajoutePolyligne(polyligne)
  def __repr__(self):
    out = "Polygone("
    if not self.plein:
      out += "-"
    else:
      out += "+"
    out += "P"
    if not self.clos:
      out += "-"
    else:
      out += "+"
    out += "C"
    if not self.interieur:
      out += "-"
    else:
      out += "+"
    out += "I"
    out+="["+self.orientation+"]"
    out += ";"
    if len(self.polylignes)>0:
      for polyligne in self.polylignes[:-1]:
        out+=str(polyligne)+";"
      out+=str(self.polylignes[-1])
    else:
      out+="Vide"
    out += ")"
    return out
    
  def depuisBDD(self, id=None):
    if id!=None:
      self.id = id
      
    req = 'SELECT plein, clos, interieur, orientation FROM polygone WHERE id='+str(self.id)
    general.bdd.execute(req)
    reqInterp=general.bdd.fetchall()
    self.plein=reqInterp[0][0]=="1"
    self.clos=reqInterp[0][1]=="1"
    self.interieur=reqInterp[0][2]=="1"
    self.orientation=reqInterp[0][3]
    
    req = 'SELECT idpolyligne FROM polygonepolyligne WHERE idpolygone='+str(self.id)
    general.bdd.execute(req)
    reqPolylignes=general.bdd.fetchall()
    for polyligne in reqPolylignes:
      self.ajoutePolyligne(int(polyligne[0]))
  def majBDD(self):
    req = "DELETE FROM polygone WHERE id="+str(self.id)
    general.bdd.execute(req)
    req = "DELETE FROM polygonepolyligne WHERE idpolygone="+str(self.id)
    general.bdd.execute(req)
    self.versBDD(self.id)
  def versBDD(self, id=None):
    pls = self.polylignes[:]
    pls.sort()
    hashV = str(hashlib.sha512(str(pls)).hexdigest())
    req = "SELECT idpolygone FROM polygonehash WHERE hash='"+hashV+ "' ORDER BY idpolygone ASC"
    general.bdd.execute(req)
    reqExiste=general.bdd.fetchall()
    if len(reqExiste)>0 and id==None:
      self.id = int(reqExiste[0][0])
      return self.id
    else:
      if id==None:
        general.bdd.execute("SELECT MAX(id) FROM polygone")
        reqID=general.bdd.fetchall()
        if len(reqID)<=0:
          id=0
        else:
          if reqID[0][0]==None:
            id=0
          else:
            id=int(reqID[0][0])+1
      if self.plein:
        plein="1"
      else:
        plein="0"
      if self.clos:
        clos="1"
      else:
        clos="0"
      if self.interieur:
        interieur="1"
      else:
        interieur="0"
        
      req = 'INSERT INTO polygone (id, plein, clos, interieur, orientation) VALUES( '+str(id)+', "'+plein+'", "'+clos+'", "'+interieur+'", "'+self.orientation+'")'
      general.bdd.execute(req)
      req = 'INSERT INTO polygonehash (idpolygone, hash) VALUES( '+str(id)+', "'+hashV+'")'
      general.bdd.execute(req)
      for polyligne in self.polylignes:
        req = 'INSERT INTO polygonepolyligne (idpolygone, idpolyligne) VALUES( '+str(id)+', '+str(polyligne)+')'
        general.bdd.execute(req)
      general.basedonnee.commit()
      self.id = id
      return self.id
      
class Objet:
  dateDeb = None
  dateFin = None
  position = None #pos   #zone et position ne peuvent cohabiter
  zone = None #area | loc    #zone et position ne peuvent cohabiter
  typeG = None #admarea | admbdry | admpt (position, pas zone) | blda | bldl | cntr | commbdry | commpt (position, pas zone) | cstline | railcl | rdcompt | rdedg | wa | wl
  type = None
  nom = None #Optionel
  codeAdministratif = None #Optionel
  
  def __init__(self, dateDeb, dateFin, position, zone, typeG, type, nom, codeAdministratif):
    self.dateDeb = dateDeb
    self.dateFin = dateFin
    self.position = position
    self.zone = zone
    self.typeG = typeG
    self.type = type
    self.nom = nom
    self.codeAdministratif = codeAdministratif
    
  def __repr__(self):
    return "objet("+str(self.typeG)+";"+str(self.position)+";"+str(self.zone)+")"
    
  def depuisBDD(self, id):
    req = "SELECT dateDeb, dateFin, position, zone, typeG, type, nom, codeAdministratif FROM objet WHERE id="+str(id)
    general.bdd.execute(req)
    reqCharge=general.bdd.fetchall()
    self.dateDeb = (int(reqCharge[0][0].split(",")[0]), int(reqCharge[0][0].split(",")[1]), int(reqCharge[0][0].split(",")[2]))
    self.dateFin = (int(reqCharge[0][1].split(",")[0]), int(reqCharge[0][1].split(",")[1]), int(reqCharge[0][1].split(",")[2]))
    if reqCharge[0][2]=="None":
      self.position = None
    else:
      self.position = reqCharge[0][2]
    if reqCharge[0][3]=="None":
      self.zone = None
    else:
      self.zone = reqCharge[0][3]
    self.typeG = reqCharge[0][4]
    self.type = reqCharge[0][5]
    if reqCharge[0][6]=="None":
      self.nom=None
    else:
      self.nom = reqCharge[0][6]
    if reqCharge[0][7]=="None":
      self.codeAdministratif = None
    else:
      self.codeAdministratif = reqCharge[0][7]
    return id
  def majBDD(self):
    print "TODO objet:majBDD"
  def versBDD(self):
    type = str(self.type.encode("utf-8"))
    if self.nom!=None:
      nom =  str(self.nom.encode("utf-8"))
    else:
      nom = "None"
    req = "SELECT id FROM objet WHERE position='"+str(self.position)+"' AND zone='"+str(self.zone)+"' AND typeG='"+str(self.typeG)+"' AND type='"+str(type)+"' AND nom='"+str(nom)+"' AND codeAdministratif = '"+str(self.codeAdministratif)+"'"

    general.bdd.execute(req)
    reqExiste=general.bdd.fetchall()
    if len(reqExiste)>0:
      self.id = int(reqExiste[0][0])
      return self.id
    else:
      general.bdd.execute("SELECT MAX(id) FROM objet")
      reqID=general.bdd.fetchall()
      if len(reqID)<=0:
        id="0"
      else:
        if reqID[0][0]==None:
          id="0"
        else:
          id=str(int(reqID[0][0])+1)

      req = "INSERT INTO objet(id, dateDeb, dateFin, position, zone, typeG, type, nom, codeAdministratif) VALUES ("+id+", '"+str(self.dateDeb)[1:-1]+"', '"+str(self.dateFin)[1:-1]+"', '"+str(self.position)+"', '"+str(self.zone)+"', '"+str(self.typeG)+"', '"+str(type)+"', '"+str(nom)+"', '"+str(self.codeAdministratif)+"')"
      general.bdd.execute(req)
      general.basedonnee.commit()
      return int(id)
    
  def affiche(self):
    out = u"-------------------------\r\n"
    out += self.typeG+" "+self.type.encode("utf-8").decode("utf-8")
    if self.nom != None:
      out += " - "+self.nom
    if self.codeAdministratif != None:
      out += " "+self.codeAdministratif
    out +="\r\n"
    out += str(self.dateDeb)+" "+str(self.dateFin)
    if self.position!=None:
      out += " P:",str(self.position)
    if self.zone!=None:
      out += " Z:"+str(self.zone)
    out += "\r\n"
    out += "-------------------------\r\n"
    print out