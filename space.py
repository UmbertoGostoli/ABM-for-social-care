# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:01:53 2017

@author: ug4d
"""
import random

class Map:
    """Contains a collection of towns to make up the whole country being simulated."""
    def __init__ (self, gridXDimension, gridYDimension, townGridDimension, 
                  cdfHouseClasses, ukMap, ukClassBias, densityModifier ):
        self.towns = []
        self.allHouses = []
        self.occupiedHouses = []

        for y in range(gridYDimension):
            for x in range(gridXDimension):
                newTown = Town(townGridDimension, x, y,
                               cdfHouseClasses, ukMap[y][x],
                               ukClassBias[y][x], densityModifier )
                self.towns.append(newTown)

        for t in self.towns:
            for h in t.houses:
                self.allHouses.append(h)
                
class Town:
    """Contains a collection of houses."""
    def __init__ (self, townGridDimension, tx, ty,
                  cdfHouseClasses, density, classBias, densityModifier ):
        self.x = tx
        self.y = ty
        self.houses = []
        self.name = str(tx) + "-" + str(ty)
        if density > 0.0:
            adjustedDensity = density * densityModifier
            for hy in range(townGridDimension):
                for hx in range(townGridDimension):
                    if random.random() < adjustedDensity:
                        newHouse = House(self,cdfHouseClasses,
                                         classBias,hx,hy)
                        self.houses.append(newHouse)
                        
class House:
    counter = 1
    """The house class stores information about a distinct house in the sim."""
    def __init__ (self, town, cdfHouseClasses, classBias, hx, hy):
        r = random.random()
        i = 0
        c = cdfHouseClasses[i] - classBias
        while r > c:
            i += 1
            c = cdfHouseClasses[i] - classBias
        self.size = i
        self.initialOccupants = 0
        self.occupants = []
        self.town = town
        self.x = hx
        self.y = hy
        self.rank = None
        self.icon = None
        self.id = House.counter
        House.counter += 1
        self.name = self.town.name + "-" + str(hx) + "-" + str(hy)
        