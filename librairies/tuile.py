#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tuile:
  coord = None
  objets = None
  
  def __init__(self, coord):
    self.coord = coord
    self.objets = []
    
  def efface(self):
    for objet in self.objets:
      objet.detachNode()
      objet.removeNode()
      
  def memeTuile(self, tuile):
    (A1x, A1y), (A2x, A2y) = self.coord
    (B1x, B1y), (B2x, B2y) = tuile.coord
    if A1x!=B1x:
      return False
    if A1y!=B1y:
      return False
    if A2x!=B2x:
      return False
    if A2y!=B2y:
      return False
    return True
      
  def __repr__(self):
    return str(self.coord)+":"+str(len(self.objets))+"objs"