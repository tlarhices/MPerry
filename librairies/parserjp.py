#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import xml.parsers.expat
from objets import *

class ParserJP:
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
      self.pile[str(self.chemin)].append(str(clef)+":"+str(attrs[clef]))
    
  def end_element(self, name):
    cg=self.cg
    name=name.lower().strip()
    OK=False
    
    idObj = None
    
    if name == "gi": #Racine de la structure
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "exchangemetadata": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:datasetcitation": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:title": #Infos
      OK=True
    elif name == "jps:date": #Date
      OK=True
      if len(self.pile[str(self.chemin)])==1:
        annee, mois, jour = self.pile[str(self.chemin)][0].split("-")
        annee = int(annee)
        mois = int(mois)
        jour = int(jour)
        self.pile[str(self.chemin)] = [(annee, mois, jour),]
      elif len(self.pile[str(self.chemin)])==2:
        pass
      else:
        print "Erreur de date, 1 ou 2 éléments attendu, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
    elif name == "jps:date8601": #Date stricte
      OK=True
      if len(self.pile[str(self.chemin)])==1:
        annee, mois, jour = self.pile[str(self.chemin)][0].split("-")
        annee = int(annee)
        mois = int(mois)
        jour = int(jour)
        self.pile[str(self.chemin)] = [(annee, mois, jour),]
      else:
        print "Erreur de date, 1 ou 2 éléments attendu, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
    elif name == "jps:datetype": #???
      OK=True
    elif name == "devdate": #La date à laquelle l'enregistrement a été créé (Development Date)
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "jps:metadatacitation": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:encodingrule": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:encodingrulecitation": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:toolname": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:toolversion": #Inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "dataset": #Racine des informations
      OK = True
      if len(self.pile[str(self.chemin)]) != 0: #S'il reste des trucs en mémoire à ce point là, c'est qu'on a mal fait le ménage
        print "ERREUR : dataset, erreur de nettoyage de tableau"
        for element in self.pile[str(self.chemin)]:
          print element
          raw_input()
      self.pile[str(self.chemin)] = None
    elif name == "fid": #Identifiant de l'élément (Feature ID)
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "lfspanfr": #Date de début de validité (Life Span From)
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:position":
        print "Erreur dans lfspanfr, 1 élément attendu de type jps:position, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1][0]
    elif name == "lfspanto": #Date de fin de validité (Life Span To)
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:position":
        print "Erreur dans lfspanto, 1 élément attendu de type jps:position, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1][0]
    elif name == "orggilvl": #ID de l'objet d'origine - inutile (Original Geographic Information Level)
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "orgmdid": #ID des métadonnées d'origine - inutile (Original Metadata ID)
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "jps:position": #Coordonnées
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or (self.pile[str(self.chemin)][0][0]!="jps:date8601" and self.pile[str(self.chemin)][0][0]!="jps:coordinate"):
        print "Erreur dans jps:position, 1 élément attendu de type jps:date8601 ou jps:coordinate, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1]
    elif name == "loc": #Un ensemble de segments (Location)
      OK = True
      if len(self.pile[str(self.chemin)])<4 or \
        self.pile[str(self.chemin)][2][0]!="jps:orientation":
        print "Erreur dans loc, 4+ éléments attendus de type id/uuid/jps:orientation/jps:segment*, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        out = Polygone(None, False, True)
        for element in self.pile[str(self.chemin)][3:]:
          if element[0]!="jps:segment":
            print "Erreur dans loc, 6+ éléments attendus de type id/uuid/jps:crs/jps:orientation/jps:primitive/jps:segment*, %i reçut" %len(self.pile[str(self.chemin)])
            for element in self.pile[str(self.chemin)]:
              print "-",element
              raw_input()
          else:
            out.ajoutePolyligne(element[1])
        self.pile[str(self.chemin)] = out.versBDD()
    elif name == "jps:crs": #Code interne, inutile
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "jps:orientation": #Ordre des points
      OK = True
      self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0]
    elif name == "jps:primitive": #ID de l'objet graphique
      OK = True
      self.pile[str(self.chemin)] = None
    elif name == "jps:segment": #Une ligne brisée
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:gm_linestring":
        print "Erreur dans jps:segment, 1 élément attendu de type jps:gm_linestring, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1]
    elif name == "jps:gm_linestring": #Une ligne brisée
      OK = True
      if len(self.pile[str(self.chemin)])!=2 or self.pile[str(self.chemin)][0][0]!="jps:interpolation" or self.pile[str(self.chemin)][1][0]!="jps:controlpoint":
        print "Erreur dans jps:gm_linestring, 2 éléments attendu de type jps:interpolation/jps:controlpoint, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        polyligne = Polyligne(None, "linear")
        polyligne.id = self.pile[str(self.chemin)][1][1]
        polyligne.depuisBDD()
        polyligne.interpolation = self.pile[str(self.chemin)][0][1]
        polyligne.versBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][1][1]
    elif name == "jps:interpolation": #Type d'interpolation
      OK = True
      self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0]
    elif name == "jps:controlpoint": #Liste de points produisant une forme
      OK = True
      polyligne = Polyligne(None, "linear")
      for i in range(0, len(self.pile[str(self.chemin)])):
        elem = self.pile[str(self.chemin)][i]
        if elem[0]!="jps:column":
          print "Erreur dans jps:controlpoint, N éléments attendu de type jps:column, %i reçut" %len(self.pile[str(self.chemin)])
          for element in self.pile[str(self.chemin)]:
            print "-",element
            raw_input()
        polyligne.ajoutePoint(self.pile[str(self.chemin)][i][1])
      self.pile[str(self.chemin)] = polyligne.versBDD()
    elif name == "jps:column": #???
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:direct":
        print "Erreur dans jps:column, 1 élément attendu de type jps:direct, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1]
    elif name == "jps:direct": #???
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:coordinate":
        print "Erreur dans jps:direct, 1 élément attendu de type jps:coordinate, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1]
    elif name == "jps:coordinate": #Coordonnées d'un point
      OK = True
      coord = self.pile[str(self.chemin)][0].split(" ")
      self.pile[str(self.chemin)] = Point(None, float(coord[0]), 0.0, float(coord[1])).versBDD()
    elif name == "type": #Type d'objet (route, rivière, ...)
      OK=True
      if len(self.pile[str(self.chemin)])==0:
        self.pile[str(self.chemin)] = ""
      else:
        self.pile[str(self.chemin)] = " ".join(self.pile[str(self.chemin)])
    elif name == "name": #Nom de l'objet (Nom du fleuve, ...)
      OK=True
      if len(self.pile[str(self.chemin)])==0:
        self.pile[str(self.chemin)] = ""
      else:
        self.pile[str(self.chemin)] = " ".join(self.pile[str(self.chemin)])

    elif name == "pos": #Coordonnées
      OK=True
      if len(self.pile[str(self.chemin)])!=3 or \
        self.pile[str(self.chemin)][2][0]!="jps:position":
        print "Erreur dans pos, 3 éléments attendus de type id/uuid/jps:position, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][2][1]
    elif name == "admcode": #Code administratif (Administrative Area Code)
      OK = True
    elif name == "area": #Une Zone
      OK = True
      if len(self.pile[str(self.chemin)])<4 or \
        self.pile[str(self.chemin)][2][0]!="jps:orientation":
        print "Erreur dans area, 4 éléments attendus de type id/uuid/jps:orientation/jps:patch, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        out = self.pile[str(self.chemin)][3][1]
        pl = Polygone(self.pile[str(self.chemin)][3][1], None, None)
        pl.depuisBDD()
        for element in self.pile[str(self.chemin)][4:0]:
          if element[0]!="jps:patch":
            print "Erreur dans area, 4 éléments attendus de type id/uuid/jps:orientation/jps:patch, %i reçut" %len(self.pile[str(self.chemin)])
            for element in self.pile[str(self.chemin)]:
              print "-",element
              raw_input()
          else:
            pl.fusionne(element[1])
        pl.orientation = self.pile[str(self.chemin)][2][1]
        pl.majBDD()
        self.pile[str(self.chemin)] = pl.versBDD()
    elif name == "jps:patch": #Un polygone
      OK = True
      if len(self.pile[str(self.chemin)])!=1 or self.pile[str(self.chemin)][0][0]!="jps:gm_polygon":
        print "Erreur dans jps:patch, 1 élément attendus de type jps:gm_polygon, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][0][1]
    elif name == "jps:gm_polygon": #Un polygone bis
      OK = True
      if len(self.pile[str(self.chemin)])!=2 or \
        self.pile[str(self.chemin)][0][0]!="jps:interpolation" or \
        self.pile[str(self.chemin)][1][0]!="jps:boundary" :
        print "Erreur dans jps:gm_polygon, 11 éléments attendus de type jps:interpolation/jps:boundary, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        pl = Polygone(self.pile[str(self.chemin)][1][1], None, None)
        pl.depuisBDD()
        for IDpolyligne in pl.polylignes:
          polyligne = Polyligne(IDpolyligne, None)
          polyligne.depuisBDD()
          polyligne.interpolation=self.pile[str(self.chemin)][0][1]
          polyligne.majBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][1][1]
    elif name == "jps:boundary": #Une frontière
      OK = True
      if len(self.pile[str(self.chemin)])<2:
        print "Erreur dans jps:boundary, au moins 2 éléments attendus de type id/[jps:exterior*/jps:interior*], %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        out=self.pile[str(self.chemin)][1][1]
        pl = Polygone(self.pile[str(self.chemin)][1][1], None, None)
        pl.depuisBDD()
        for element in self.pile[str(self.chemin)][2:]: 
          if element[0]!="jps:exterior" and element[0]!="jps:interior":
            print "typeError", "jps:exterior|jps:interior VS", element[0]
            print "Erreur dans jps:boundary, au moins 2 éléments attendus de type id/[jps:exterior*/jps:interior*], %i reçut" %len(self.pile[str(self.chemin)])
            for element in self.pile[str(self.chemin)]:
              print "-",element
              raw_input()
          else:
            pl.fusionne(element[1])
        pl.majBDD()
        self.pile[str(self.chemin)] = out
    elif name == "jps:element": #Code interne - inutile
      OK=True
      self.pile[str(self.chemin)] = None
    elif name == "jps:exterior": #La surface correspond à tout sauf la zone décrite
      OK=True
      if len(self.pile[str(self.chemin)])!=3 or \
        self.pile[str(self.chemin)][1][0]!="jps:orientation" or \
        self.pile[str(self.chemin)][2][0]!="jps:generator":
        print "Erreur dans jps:exterior, 3 éléments attendus de type id/jps:orientation/jps:segment, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        pl = Polygone(self.pile[str(self.chemin)][2][1], None, None)
        pl.depuisBDD()
        pl.interieur = False
        pl.plein = True
        pl.majBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][2][1]
    elif name == "jps:interior": #La surface correspond uniquement à la zone décrite
      OK=True
      if len(self.pile[str(self.chemin)])!=3 or \
        self.pile[str(self.chemin)][1][0]!="jps:orientation" or \
        self.pile[str(self.chemin)][2][0]!="jps:generator":
        print "Erreur dans jps:interior, 3 éléments attendus de type id/jps:orientation/jps:segment, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        pl = Polygone(self.pile[str(self.chemin)][2][1], None, None)
        pl.depuisBDD()
        pl.interieur = True
        pl.plein = True
        pl.majBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][2][1]
    elif name == "jps:generator": #Un groupement de courbes
      OK = True
      if len(self.pile[str(self.chemin)])!=2 or \
        self.pile[str(self.chemin)][1][0]!="jps:gm_orientablecurve":
        print "Erreur dans jps:generator, 2 éléments attendus de type id/jps:gm_orientablecurve, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][1][1]
    elif name == "jps:gm_orientablecurve": #Une courbe
      OK=True
      if len(self.pile[str(self.chemin)])!=3 or \
        self.pile[str(self.chemin)][1][0]!="jps:orientation" or \
        self.pile[str(self.chemin)][2][0]!="jps:segment":
        print "Erreur dans jps:gm_orientablecurve, 3 éléments attendus de type id/jps:orientation/jps:segment, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        out = Polygone(None, False, False)
        out.ajoutePolyligne(self.pile[str(self.chemin)][2][1])
        out.orientation = self.pile[str(self.chemin)][1][1]
        self.pile[str(self.chemin)] = out.versBDD()
    elif name == "alti": #Un point avec altitude
      OK = True
      if len(self.pile[str(self.chemin)])!=1 :
        print "Erreur dans alti, 1 élément attendus de type float, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      self.pile[str(self.chemin)][0] = float(self.pile[str(self.chemin)][0])
      
      
    elif name == "admarea": #Zone administrative (Administrative Area)
      OK = True
      if len(self.pile[str(self.chemin)])!=8 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="area" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name" or \
        self.pile[str(self.chemin)][7][0]!="admcode":
        print "Erreur dans admarea, 8 éléments attendus de type id/uuid/lfspanfr/lfspanto/area/type/name/admcode, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=self.pile[str(self.chemin)][7][1][0]).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "admbdry": #Frontières administratives (Administrative Boundary)
      OK=True
      if len(self.pile[str(self.chemin)])!=6 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type":
        print "Erreur dans admbdry, 6 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=None, codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "admpt": #(Representative point of Administrative Area)
      OK=True
      if len(self.pile[str(self.chemin)])!=8 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="pos" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name" or \
        self.pile[str(self.chemin)][7][0]!="admcode":
        print "Erreur dans admpt, 8 éléments attendus de type id/uuid/lfspanfr/lfspanto/pos/type/name/admcode, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=self.pile[str(self.chemin)][4][1], zone=None, typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=self.pile[str(self.chemin)][7][1][0]).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "blda": #(Boulding Area)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="area" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans blda, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/area/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "bldl": #(Boulding Outine)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans bldl, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "cntr": # Courbes de niveau (Countour) ???
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="alti":
        print "Erreur dans cntr, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/alti, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        pl = Polygone(self.pile[str(self.chemin)][4][1], None, None)
        pl.depuisBDD()

        for IDpolyligne in pl.polylignes:
          polyligne = Polyligne(IDpolyligne, None)
          polyligne.depuisBDD()
          for point in polyligne.points:
            pt = Point(point, None, None, None)
            pt.depuisBDD()
            if pt.y != self.pile[str(self.chemin)][6][1][0]:
              pt.y = self.pile[str(self.chemin)][6][1][0]
              pt.majBDD()
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=None, codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][2:6]
        self.pile[str(self.chemin)] = None
        
    elif name == "commbdry": #(Community Boundary)
      OK = True
      if len(self.pile[str(self.chemin)])!=6 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type":
        print "Erreur dans commbdry, 6 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=None, codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "commpt": #(Representative Point of Community Area)
      OK=True
      if len(self.pile[str(self.chemin)])!=8 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="pos" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name" or \
        self.pile[str(self.chemin)][7][0]!="admcode":
        print "Erreur dans commpt, 8 éléments attendus de type id/uuid/lfspanfr/lfspanto/pos/type/name/admcode, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=self.pile[str(self.chemin)][4][1], zone=None, typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=self.pile[str(self.chemin)][7][1][0]).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "cstline": #Une côte (Coastline)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans cstline, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "elevpt": #Un point en 3D (Elevation Point)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="pos" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="alti":
        print "Erreur dans elevpt, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/pos/type/alti, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        pt = Point(self.pile[str(self.chemin)][4][1], None, None, None)
        pt.depuisBDD()
        if pt.y != self.pile[str(self.chemin)][6][1][0]:
          pt.y = self.pile[str(self.chemin)][6][1][0]
          pt.majBDD()
        
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=self.pile[str(self.chemin)][4][1], zone=None, typeG=name, type=self.pile[str(self.chemin)][5][1], nom=None, codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = self.pile[str(self.chemin)][2:6]
        self.pile[str(self.chemin)] = None
        
    elif name == "railcl": #Voie ferrée (Railroad Track Centerline)
      OK = True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans railcl, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "rdcompt": #Route (Road Component)
      OK=True
      if len(self.pile[str(self.chemin)])!=6 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type":
        print "Erreur dans rdcompt, 6 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=None, codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "rdedg": #Route (Road Edge)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans rdedg, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "wa": #(Water Area)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="area" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans wa, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/area/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        self.pile[str(self.chemin)][0] = self.pile[str(self.chemin)][0].split(":")[1]
        self.pile[str(self.chemin)][1] = self.pile[str(self.chemin)][1].split(":")[1]
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
    elif name == "wl": #(Water Line)
      OK=True
      if len(self.pile[str(self.chemin)])!=7 or \
        self.pile[str(self.chemin)][2][0]!="lfspanfr" or \
        self.pile[str(self.chemin)][3][0]!="lfspanto" or \
        self.pile[str(self.chemin)][4][0]!="loc" or \
        self.pile[str(self.chemin)][5][0]!="type" or \
        self.pile[str(self.chemin)][6][0]!="name":
        print "Erreur dans wl, 7 éléments attendus de type id/uuid/lfspanfr/lfspanto/loc/type/name, %i reçut" %len(self.pile[str(self.chemin)])
        for element in self.pile[str(self.chemin)]:
          print "-",element
          raw_input()
      else:
        idObj = Objet(dateDeb=self.pile[str(self.chemin)][2][1], dateFin=self.pile[str(self.chemin)][3][1], position=None, zone=self.pile[str(self.chemin)][4][1], typeG=name, type=self.pile[str(self.chemin)][5][1], nom=self.pile[str(self.chemin)][6][1], codeAdministratif=None).versBDD()
        self.pile[str(self.chemin)] = None
        
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
        if tt in ['AdmBdry', 'AdmPt', 'CommBdry', 'CommPt', 'Cstline', 'RailCL', 'RdCompt', 'WL', 'WA']: #'RdEdg', 
    #    if tt in ['AdmArea25000', 'AdmArea', 'AdmBdry', 'AdmBdry25000', 'AdmPt25000', 'AdmPt', 'BldA', 'BldA25000', 'BldA', 'BldA25000', 'BldL', 'Cntr25000', 'CommBdry', 'CommPt', 'Cstline25000', 'Cstline', 'ElevPt', 'ElevPt25000', 'RailCL', 'RailCL25000', 'RdCompt', 'RdEdg25000', 'RdEdg', 'WA', 'WL', 'WL25000']:
          self.fichiers.append(fichier)

  def parseTick(self):
    if len(self.lignes)==0:
      if self.enCours!=None:
        print "mv",self.enCours, os.path.join(".", "xml","fini",self.enCours.replace("\\","/").split("/")[-1])
        shutil.move(self.enCours, os.path.join(".", "xml","fini",self.enCours.replace("\\","/").split("/")[-1]))
      if len(self.fichiers)==0:
        print "plus rien a parser"
        if self.enCours!=None:
          afficheTexte(None, section="charge", forceRefresh=True)
          self.enCours=None
        return False
      self.parser = xml.parsers.expat.ParserCreate()
      self.parser.StartElementHandler = self.start_element
      self.parser.EndElementHandler = self.end_element
      self.parser.CharacterDataHandler = self.char_data
      f = open(self.fichiers[0])
      self.enCours = self.fichiers[0]
      txt ="Parsage de %s, %i fichiers restants..." %(self.enCours.replace("\\","/").split("/")[-1], len(self.fichiers)+1)
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
      txt = "Parsage de %s\n\rFait : %.2f%%, %i fichiers restants" %(self.enCours.replace("\\","/").split("/")[-1], (1.0-len(self.lignes)*1.0/self.tailleFichier)*100.0, len(self.fichiers)+1)
      if self.gui != None:
        self.gui.afficheTexte(txt, orientation="bas", section="parse")
      else:
        print txt
    try:
      if ligne.index("encoding")>0:
        ligne=""
    except ValueError:
      pass
    
    self.parser.Parse(ligne.decode("shift_jis").encode("utf-8"))
    return True
