#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pandac.PandaModules import *

import treegui
from treegui.components import Form,Widget,ScrollPane
from treegui.widgets import *
from treegui.core import Gui
import rtheme

class Gauche(ScrollPane):
  style = "default"
  
  def clic(self, bouton, etat):
    self.gui.select(bouton.lower(), etat)
  
  def inverse(self):
    for bouton in self.boutons:
      bouton.onClick()
  
  def __init__(self, gui):
    self.gui=gui
    ScrollPane.__init__(self)
    self.add(Label("Couches :", y = 0))
    self.boutons = []
    i=1
    liste=self.gui.cg.elements.keys()
    liste.remove("tout")
    liste.sort()
    for elem in liste:
      check = self.add(Check(elem.capitalize(), y = 17*i))
      check.callback = self.clic
      self.boutons.append(check)
      i+=1
    self.inverse = self.add(Button("Inverser", self.inverse, y=17 * i + 5, width="55px"))
    
    self.x = "left" 
    self.y = "center" 
    self.width = "20%"
    self.height = "60%"
        
class Droite(Form):
  style = "default"

  def __init__(self, gui):
    self.gui=gui
    Form.__init__(self)
    
    self.plus = self.add(Icon("rtheme/twotone/zoom-in.png", x="left", y=0))
    self.plus.onClick = self.gui.zoomPlus
    self.moins = self.add(Icon("rtheme/twotone/zoom-out.png", x="right", y=0))
    self.moins.onClick = self.gui.zoomMoins
    self.haut = self.add(Icon("rtheme/twotone/arrow-up.png", x="center", y=20))
    self.haut.onClick = self.gui.deplaceHaut
    self.gauche = self.add(Icon("rtheme/twotone/arrow-left.png", x="left", y=37))
    self.gauche.onClick = self.gui.deplaceGauche
    self.droite = self.add(Icon("rtheme/twotone/arrow-right.png", x="right", y=37))
    self.droite.onClick = self.gui.deplaceDroite
    self.bas = self.add(Icon("rtheme/twotone/arrow-down.png", x="center", y=54))
    self.bas.onClick = self.gui.deplaceBas
    
    zero = 60
    self.snapGPS = self.add(PictureRadio("rtheme/twotone/target-over.png", "rtheme/twotone/target.png", y = zero + 17, x=0))
    self.snapContenu = self.add(PictureRadio("rtheme/twotone/news-over.png", "rtheme/twotone/news.png", y = zero + 17, x=17))
    self.snapLibre = self.add(PictureRadio("rtheme/twotone/move-over.png", "rtheme/twotone/move.png", y = zero + 17, x=34))
    self.snapGPS.onClick()
    
    self.x = "right" 
    self.y = "20%" 
    self.width = "54px"
    self.height = "95px"

class Bas(Form):
  style = "default"
  
  def __init__(self):
    Form.__init__(self)
    
    self.label = self.add(Label("...", y = 0))
    #label.font = font
    
    self.x = "center" 
    self.y = "bottom" 
    self.width = "80%"
    self.height = "10%"

class Haut(Form):
  style = "default"
  
  def clic(self):
    print "Recherche de "+self.recherche.text
  
  def __init__(self):
    Form.__init__(self)
    
    self.coord = self.add(Label("Position : 0.0, 0.0", x="center", y ="top", width="100%"))
    self.recherche = self.add(Entry("Rechercher...", x="left", y="bottom", width="90%"))
    self.recherche.onEnter = self.clic
    self.bouton = self.add(Icon("rtheme/twotone/search.png", x="right", y="bottom"))
    self.bouton.onClick = self.clic
    #label.font = font
    
    self.x = "center" 
    self.y = "top" 
    self.width = "80%"
    self.height = "10%"
        
class Interface:
  def __init__(self, cg):
    self.cg=cg

    base.accept("q", sys.exit)
    base.accept("escape", sys.exit)
    base.accept("+", self.zoomPlus)
    base.accept("-", self.zoomMoins)
    base.accept("arrow_left", self.deplaceGauche)
    base.accept("arrow_right", self.deplaceDroite)
    base.accept("arrow_up", self.deplaceHaut)
    base.accept("arrow_down", self.deplaceBas)
    #base.accept("mouse1", clicGauche)
    #base.accept("mouse2", clicCentre)
    #base.accept("mouse3", clicDroit)

    self.gui = Gui(theme = rtheme.RTheme())
    self.bas = Bas()
    self.gui.add(self.bas)
    self.haut = Haut()
    self.gui.add(self.haut)
    self.droite = Droite(self)
    self.gui.add(self.droite)
    self.gauche = Gauche(self)
    self.gui.add(self.gauche)
    self.quit = self.gui.add(Icon("rtheme/twotone/x.png", x="right", y="top"))
    self.quit.onClick = sys.exit
    
  def zoomPlus(self):
    p = base.camera.getPos()
    base.camera.setPos(p[0], p[1]*0.75, p[2])
  
  def zoomMoins(self):
    p = base.camera.getPos()
    base.camera.setPos(p[0], p[1]*1.333, p[2])
    
  deltaCamX = 0.001
  deltaCamY = 0.001
    
  def deplaceHaut(self):
    self.droite.snapLibre.onClick()
    p = base.camera.getPos()
    base.camera.setPos(p[0], p[1], p[2]+self.deltaCamY)
  
  def deplaceBas(self):
    self.droite.snapLibre.onClick()
    p = base.camera.getPos()
    base.camera.setPos(p[0], p[1], p[2]-self.deltaCamY)

  def deplaceGauche(self):
    self.droite.snapLibre.onClick()
    p = base.camera.getPos()
    base.camera.setPos(p[0]-self.deltaCamX, p[1], p[2])

  def deplaceDroite(self):
    self.droite.snapLibre.onClick()
    p = base.camera.getPos()
    base.camera.setPos(p[0]+self.deltaCamX, p[1], p[2])
    
  def select(self, type, affiche=True):
    type=type.lower()
    liste = self.cg.elements[type][:]
    
    if not affiche:
      for element in self.cg.elements[type]:
        self.cg.effaceCategorie(element)
    else:
      self.cg.charge(liste, tuile=None)#self.cg.tuile((self.cg.GPSCoord[0], 0.0, self.cg.GPSCoord[1])))
      
  def afficheTexte(self, texte, orientation="centre", section=None, forceRefresh=False):
    """Affiche le texte sur l'écran, si texte==None, alors efface le dernier texte affiché"""
    print texte
    try:
      if texte!=None:
        self.bas.label.text=texte
    except NameError:
      return
    
    if forceRefresh:
      base.graphicsEngine.renderFrame()
      
  def snapMode(self):
    if self.droite.snapLibre.value:
      return "libre"
    if self.droite.snapGPS.value:
      return "gps"
    if self.droite.snapContenu.value:
      return "contenu"
    return "snap err"