#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(".", "librairies"))
sys.path.append(os.path.join(".", "data"))

from gps import GPS
from db import DB
from affichage import Affichage
from parserjp import ParserJP
from gui import Interface

def ping(task):
  aff.ping()
  if gui.parsageActif():
    parseur.parseTick()
  
  GPSCoord, GPSAltitude = gps.ping()
  affCoord = ""
  if GPSCoord==None:
    affCoord = "Pas de donnée GPS,"
  else:
    aff.GPSCoord = GPSCoord
    affCoord = "Position : %.5f; %.5f" %(GPSCoord[0], GPSCoord[1])
  affAltitude = ""
  if GPSAltitude==None:
    affAltitude = " altitude inconnue."
  else:
    aff.GPSAltitude = GPSAltitude
    affAltitude = " altitude : "+str(GPSAltitude)+"m"
    
  if GPSCoord!=None and gui.snapMode()=="gps":
    base.camera.setPos(GPSCoord[0], base.camera.getPos()[1], GPSCoord[1])
    base.camera.lookAt(GPSCoord[0], 0.0, GPSCoord[1])
  elif gui.snapMode()=="contenu":
    bnds = render.getTightBounds()
    centre = (bnds[0][0]+bnds[1][0])/2.0, (bnds[0][2]+bnds[1][2])/2.0
    base.camera.setPos(centre[0], base.camera.getPos()[1], centre[1])
    base.camera.lookAt(centre[0], 0.0, centre[1])
  gui.haut.coord.text=affCoord+affAltitude
  return task.cont
  
from pandac.PandaModules import *
#Change la résolution de la fenêtre
loadPrcFileData("",u"win-size 160 120")
#Kicke la synchro avec VSynch pour pouvoir dépasser les 60 FPS
loadPrcFileData("",u"sync-video #f")
loadPrcFileData("",u"audio-library-name NullAudioManager")
if len(sys.argv)>1:
  if sys.argv[1]=="parse" or sys.argv[1]=="parse+bam" or sys.argv[1]=="bam":
    loadPrcFileData("",u"window-type none")
import direct.directbase.DirectStart
from direct.task import Task
base.disableMouse()
if base.camLens != None:
  base.camLens.setNear(0.001)
if base.camera != None:
  base.camera.setPos(0.0, 5.0, 0.0)
  base.camera.lookAt(0.0, 0.0, 0.0)
if base.win != None:
  base.win.setClearColor(Vec4(0.8,0.8,0.8,1))
base.graphicsEngine.renderFrame()

  
db = DB()
gps = GPS()
aff = Affichage()
if base.win!=None:
  gui = Interface(aff)
else:
  gui = None
aff.gui = gui
parseur = ParserJP(gui)
parseur.cg = aff
parseur.prepareParse()

if len(sys.argv)>1:
  if sys.argv[1]=="parse+bam":
    parseur.parse(BAM=True)
    sys.exit()
  if sys.argv[1]=="parse":
    parseur.parse()
    sys.exit()
  if sys.argv[1]=="bam":
    aff.buildBam()
    while aff.ping(3.0):
      pass
    sys.exit()

taskMgr.add(ping, "ping")
run()
  
