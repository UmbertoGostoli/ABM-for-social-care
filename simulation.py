# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 12:44:00 2017

@author: ug4d
"""

from society import Person
from society import Population
from space import House
from space import Town
from space import Map
import random
import math
import pylab
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
import Tkinter
import struct
import time
import sys
import pprint
import pickle
import numpy as np
import operator
# from PIL import ImageTk         
# from PIL import Image



class Sim:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, params):
        self.p = params

        ## Statistical tallies
        self.periodCount = 0
        
        self.times = []
        
        ###################### Demographic outputs ###################
        self.agent = None
        
        self.pops = []
        self.socialClassShares = []
        self.careNeedShares = []
        self.jobMarketMap = []
        self.births_1 = []
        self.births_2 = []
        self.births_3 = []
        self.births_4 = []
        self.births_5 = []
        self.deaths_1 = []
        self.deaths_2 = []
        self.deaths_3 = []
        self.deaths_4 = []
        self.deaths_5 = []
        self.unskilledPop = []
        self.skilledPop = []
        self.lowerclassPop = []
        self.middleclassPop = []
        self.upperclassPop = []
        
        self.socialMobility_1to2 = []
        self.socialMobility_1to3 = []
        self.socialMobility_1to4 = []
        self.socialMobility_1to5 = []
        self.socialMobility_2to1 = []
        self.socialMobility_2to3 = []
        self.socialMobility_2to4 = []
        self.socialMobility_2to5 = []
        self.socialMobility_3to1 = []
        self.socialMobility_3to2 = []
        self.socialMobility_3to4 = []
        self.socialMobility_3to5 = []
        self.socialMobility_4to1 = []
        self.socialMobility_4to2 = []
        self.socialMobility_4to3 = []
        self.socialMobility_4to5 = []
        self.socialMobility_5to1 = []
        self.socialMobility_5to2 = []
        self.socialMobility_5to3 = []
        self.socialMobility_5to4 = []
        
        self.numberHouseholds = []
        self.numberHouseholds_1 = []
        self.numberHouseholds_2 = []
        self.numberHouseholds_3 = []
        self.numberHouseholds_4 = []
        self.numberHouseholds_5 = []
        
        self.avgHouseholdSize = []
        self.avgHouseholdSize_1 = []
        self.avgHouseholdSize_2 = []
        self.avgHouseholdSize_3 = []
        self.avgHouseholdSize_4 = []
        self.avgHouseholdSize_5 = []
        
        self.marriageProp = []
        self.marriageTally = 0
        self.numMarriages = []
        self.divorceTally = 0
        self.numDivorces = []
        
        ############################# Social Care outputs ###################
        
        self.totalCareDemand = []
        self.totalChildCareDemand = []
        self.totalSocialCareDemand = []  # New!
        self.totalCareSupply = [] # New!
        self.totalInformalCareSupply = [] # New!
        self.totalFormalCareSupply = [] # New!
        self.totalCareReceived = [] # New!
        self.totalChildCareReceived = [] #New!
        self.totalSocialCareReceived = [] #New!
        self.totalInformalCareReceived = []
        self.totalFormalCareReceived = []
        self.totalInformalSocialCareReceived = []
        self.totalFormalSocialCareReceived = []
        self.totalInformalChildCareReceived = []
        self.totalFormalChildCareReceived = []
        self.totalUnmetDemand = []
        self.totalSocialCareUnmetDemand = [] # New!
        self.totalChildCareUnmetDemand = [] # New!
        self.totalCareSuppliedMale = [] # New!
        self.totalInformalCareSuppliedMale = [] # New!
        self.totalInformalCareSuppliedMale_1 = [] # New!
        self.totalInformalCareSuppliedMale_2 = [] # New!
        self.totalInformalCareSuppliedMale_3 = [] # New!
        self.totalInformalCareSuppliedMale_4 = [] # New!
        self.totalInformalCareSuppliedMale_5 = [] # New!
        self.totalFormalCareSuppliedMale = [] # New!
        self.totalCareSuppliedFemale = [] # New!
        self.totalInformalCareSuppliedFemale = [] # New!
        self.totalInformalCareSuppliedFemale_1 = [] # New!
        self.totalInformalCareSuppliedFemale_2 = [] # New!
        self.totalInformalCareSuppliedFemale_3 = [] # New!
        self.totalInformalCareSuppliedFemale_4 = [] # New!
        self.totalInformalCareSuppliedFemale_5 = [] # New!
        self.totalFormalCareSuppliedFemale = [] # New!
        
        self.totalCareDemand_1 = []
        self.totalCareSupply_1 = []
        self.totalUnmetDemand_1 = []
        self.totalCareDemand_2 = []
        self.totalCareSupply_2 = []
        self.totalUnmetDemand_2 = []
        self.totalCareDemand_3 = []
        self.totalCareSupply_3 = []
        self.totalUnmetDemand_3 = []
        self.totalCareDemand_4 = []
        self.totalCareSupply_4 = []
        self.totalUnmetDemand_4 = []
        self.totalCareDemand_5 = []
        self.totalCareSupply_5 = []
        self.totalUnmetDemand_5 = []
        
        self.totalInformalSupply = []
        self.totalFormalSupply = []
        self.totalInformalSupply_1 = []
        self.totalFormalSupply_1 = []
        self.totalInformalCarePerRecipient_1 = []
        self.totalFormalCarePerRecipient_1 = []
        self.totalUnmetNeedPerRecipient_1 = []
        self.totalInformalCarePerCarer_1 = []
        self.totalFormalCarePerCarer_1 = []
        self.totalInformalSupply_2 = []
        self.totalFormalSupply_2 = []
        self.totalInformalCarePerRecipient_2 = []
        self.totalFormalCarePerRecipient_2 = []
        self.totalUnmetNeedPerRecipient_2 = []
        self.totalInformalCarePerCarer_2 = []
        self.totalFormalCarePerCarer_2 = []
        self.totalInformalSupply_3 = []
        self.totalFormalSupply_3 = []
        self.totalInformalCarePerRecipient_3 = []
        self.totalFormalCarePerRecipient_3 = []
        self.totalUnmetNeedPerRecipient_3 = []
        self.totalInformalCarePerCarer_3 = []
        self.totalFormalCarePerCarer_3 = []
        self.totalInformalSupply_4 = []
        self.totalFormalSupply_4 = []
        self.totalInformalCarePerRecipient_4 = []
        self.totalFormalCarePerRecipient_4 = []
        self.totalUnmetNeedPerRecipient_4 = []
        self.totalInformalCarePerCarer_4 = []
        self.totalFormalCarePerCarer_4 = []
        self.totalInformalSupply_5 = []
        self.totalFormalSupply_5 = []
        self.totalInformalCarePerRecipient_5 = []
        self.totalFormalCarePerRecipient_5 = []
        self.totalUnmetNeedPerRecipient_5 = []
        self.totalInformalCarePerCarer_5 = []
        self.totalFormalCarePerCarer_5 = []
        
        self.totalSupplyHousehold = []
        self.totalSupplyNoK_1 = []
        self.totalSupplyNoK_2 = []
        self.totalSupplyNoK_3 = []
        self.totalInformalSupplyHousehold = []
        self.totalInformalSupplyNoK_1 = []
        self.totalInformalSupplyNoK_2 = []
        self.totalInformalSupplyNoK_3 = []
        self.totalFormalSupplyHousehold = []
        self.totalFormalSupplyNoK_1 = []
        self.totalFormalSupplyNoK_2 = []
        self.totalFormalSupplyNoK_3 = []
        ########################### Economic outputs ######################
        
        self.totalEmployment = []
        self.totalEmployment_1 = []
        self.totalEmployment_2 = []
        self.totalEmployment_3 = []
        self.totalEmployment_4 = []
        self.totalEmployment_5 = []
        
        self.totalJobChanges = []
        
        self.averageIncome_M = []
        self.averageIncome_F = []
        
        self.averageIncome_1 = []
        self.averageIncome_1_Males = []
        self.averageIncome_1_Females = []
        self.averageIncome_2 = []
        self.averageIncome_2_Males = []
        self.averageIncome_2_Females = []
        self.averageIncome_3 = []
        self.averageIncome_3_Males = []
        self.averageIncome_3_Females = []
        self.averageIncome_4 = []
        self.averageIncome_4_Males = []
        self.averageIncome_4_Females = []
        self.averageIncome_5 = []
        self.averageIncome_5_Males = []
        self.averageIncome_5_Females = []
        
        ########################## Mobility outputs ######################
        
        self.totalRelocations = 0
        self.numberRelocations = []
        self.jobRelocations = 0
        self.numJobRelocations = []
        self.marriageRelocations = 0
        self.numMarriageRelocations = []
        self.sizeRelocations = 0
        self.numSizeRelocations = []
        self.retiredRelocations = 0
        self.numRetiredRelocations = []
        self.townChanges = 0
        self.numberTownChanges = []
        
        ######################## Other outputs #############################
        
        self.numTaxpayers = []
        self.totalUnmetNeed = []
        self.totalFamilyCare = []
        self.totalTaxBurden = []
        
        
        self.enterWork = []
        self.exitWork = []
        self.changeWork = []

        # Counters and storage
        self.check = False
        self.exitWork = 0
        self.enterWork = 0
        self.year = self.p['startYear']
        self.pyramid = PopPyramid(self.p['num5YearAgeClasses'],
                                  self.p['numCareLevels'])
        self.textUpdateList = []

        if self.p['interactiveGraphics']:
            self.window = Tkinter.Tk()
            self.canvas = Tkinter.Canvas(self.window,
                                         width=self.p['screenWidth'],
                                         height=self.p['screenHeight'],
                                         background=self.p['bgColour'])

    def run(self):
        # Read parameters 
        self.parameters = np.genfromtxt('parameters.csv',
                                       skip_header = 1, delimiter=',')
        
        # Create a list of combinations
        combinations = []
        for i in range(len(self.parameters)):
            for j in range(len(self.parameters)):
                for z in range(len(self.parameters[i])):
                    for k in range(len(self.parameters[i])):
                        runParameters = []
                        runParameters.append(self.parameters[i][0])
                        runParameters.append(self.parameters[j][1])
                        runParameters.append(self.parameters[z][2])
                        runParameters.append(self.parameters[k][3])
                        combinations.append(runParameters)
                    
        for r in range(len(combinations)):
            
            folder  = 'N:/Social Care Model II/Charts/Run_' + str(r)
            
            random.seed(self.p['favouriteSeed'])
            
            self.p['unmetNeedExponent'] = combinations[r][0] # Default = 0.1
            self.p['incomeCareParam'] = combinations[r][1] # Default = 0.001
            self.p['excessNeedParam'] = combinations[r][2] # Default = 2.0
            self.p['alphaGeoExp'] = combinations[r][3] # Default = 0.3
    
            filename = folder + '/parameterValues.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))
            values = zip(np.array(combinations[r]))
            names = ('unmetNeedExponent, incomeCareParam, excessNeedParam, alphaGeoExp')
            np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="") 
            
            self.initializePop()
            
            if self.p['interactiveGraphics']:
                self.initializeCanvas()
            
            
            for self.year in range(self.p['startYear'], self.p['endYear']+1):
                
                print(" ")
                print(self.year)
                
                self.doOneYear()
                self.periodCount += 1
                if self.year == self.p['thePresent']:
                    random.seed()
            
    
            ###### Create csv with all the outputs   ############
            values = zip(self.pops, self.births_1, self.births_2, self.births_3, self.births_4, self.births_5, 
                         self.deaths_1, self.deaths_2, self.deaths_3, self.deaths_4, self.deaths_5,
                         self.unskilledPop, self.skilledPop, self.lowerclassPop, 
                         self.middleclassPop, self.upperclassPop, self.socialMobility_1to2, 
                         self.socialMobility_1to3, self.socialMobility_1to4, self.socialMobility_1to5, 
                         self.socialMobility_2to1, self.socialMobility_2to3, self.socialMobility_2to4, 
                         self.socialMobility_2to5, self.socialMobility_3to1, self.socialMobility_3to2, 
                         self.socialMobility_3to4, self.socialMobility_3to5, self.socialMobility_4to1, 
                         self.socialMobility_4to2, self.socialMobility_4to3, self.socialMobility_4to5, 
                         self.socialMobility_5to1, self.socialMobility_5to2, self.socialMobility_5to3, 
                         self.socialMobility_5to4, self.numberHouseholds, self.numberHouseholds_1, 
                         self.numberHouseholds_2, self.numberHouseholds_3, self.numberHouseholds_4, 
                         self.numberHouseholds_5, self.avgHouseholdSize, self.avgHouseholdSize_1, 
                         self.avgHouseholdSize_2, self.avgHouseholdSize_3, self.avgHouseholdSize_4, 
                         self.avgHouseholdSize_5, self.marriageProp, self.numMarriages, self.numDivorces, 
                         
                         self.totalCareDemand, self.totalChildCareDemand, self.totalCareSupply, self.totalUnmetDemand, 
                         self.totalInformalCareReceived, self.totalFormalCareReceived, 
                         
                         self.totalCareDemand_1, self.totalCareSupply_1, self.totalUnmetDemand_1, 
                         self.totalCareDemand_2, self.totalCareSupply_2, self.totalUnmetDemand_2, 
                         self.totalCareDemand_3, self.totalCareSupply_3, self.totalUnmetDemand_3, 
                         self.totalCareDemand_4, self.totalCareSupply_4, self.totalUnmetDemand_4, 
                         self.totalCareDemand_5, self.totalCareSupply_5, self.totalUnmetDemand_5, 
                         self.totalInformalSupply, self.totalFormalSupply, self.totalInformalSupply_1, 
                         self.totalFormalSupply_1, self.totalInformalSupply_2, self.totalFormalSupply_2, 
                         self.totalInformalSupply_3, self.totalFormalSupply_3, self.totalInformalSupply_4, 
                         self.totalFormalSupply_4, self.totalInformalSupply_5, self.totalFormalSupply_5, 
                         self.totalSupplyHousehold, self.totalSupplyNoK_1, self.totalSupplyNoK_2, 
                         self.totalSupplyNoK_3, self.totalEmployment, self.totalEmployment_1, self.totalEmployment_2, 
                         self.totalEmployment_3, self.totalEmployment_4, self.totalEmployment_5, self.totalJobChanges, 
                         self.averageIncome_M, self.averageIncome_F, self.averageIncome_1, self.averageIncome_2, 
                         self.averageIncome_3, self.averageIncome_4, self.averageIncome_5, self.numberRelocations, 
                         self.numJobRelocations, self.numMarriageRelocations, self.numSizeRelocations, 
                         self.numRetiredRelocations, self.numberTownChanges)
                         
            names = ('pops, births_1, births_2, births_3, births_4, births_5, '
                    'deaths_1, deaths_2, deaths_3, deaths_4, deaths_5,unskilledPop, '
                    'skilledPop, lowerclassPop, middleclassPop, upperclassPop, '
                    'socialMobility_1to2, socialMobility_1to3, socialMobility_1to4, socialMobility_1to5, '
                    'socialMobility_2to1, socialMobility_2to3, socialMobility_2to4, socialMobility_2to5, '
                    'socialMobility_3to1, socialMobility_3to2, socialMobility_3to4, socialMobility_3to5, '
                    'socialMobility_4to1, socialMobility_4to2, socialMobility_4to3, socialMobility_4to5, '
                    'socialMobility_5to1, socialMobility_5to2, socialMobility_5to3, socialMobility_5to4, '
                    'numberHouseholds, numberHouseholds_1, numberHouseholds_2, numberHouseholds_3, '
                    'numberHouseholds_4, numberHouseholds_5, avgHouseholdSize, avgHouseholdSize_1, '
                    'avgHouseholdSize_2, avgHouseholdSize_3, avgHouseholdSize_4, avgHouseholdSize_5, '
                    'marriageProp, numMarriages, numDivorces, totalCareDemand, totalChildCare, totalCareSupply, '
                    'totalUnmetDemand, totalInformalCareReceived, totalFormalCareReceived, ' 
                    'totalCareDemand_1, totalCareSupply_1, totalUnmetDemand_1, '
                    'totalCareDemand_2, totalCareSupply_2, totalUnmetDemand_2, totalCareDemand_3, '
                    'totalCareSupply_3, totalUnmetDemand_3, totalCareDemand_4, totalCareSupply_4, '
                    'totalUnmetDemand_4, totalCareDemand_5, totalCareSupply_5, totalUnmetDemand_5, '
                    'totalInformalSupply, totalFormalSupply, totalInformalSupply_1, totalFormalSupply_1, '
                    'totalInformalSupply_2, totalFormalSupply_2, totalInformalSupply_3, totalFormalSupply_3, '
                    'totalInformalSupply_4, totalFormalSupply_4, totalInformalSupply_5, totalFormalSupply_5, '
                    'totalSupplyHousehold, totalSupplyNoK_1, totalSupplyNoK_2, totalSupplyNoK_3, totalEmployment, '
                    'totalEmployment_1, totalEmployment_2, totalEmployment_3, totalEmployment_4, totalEmployment_5, '
                    'totalJobChanges, averageIncome_M, averageIncome_F, averageIncome_1, averageIncome_2, '
                    'averageIncome_3, averageIncome_4, averageIncome_5, numberRelocations, numJobRelocations, '
                    'numMarriageRelocations, numSizeRelocations, numRetiredRelocations, numberTownChanges')
            
            np.savetxt('Outputs.csv', values, delimiter=',', fmt='%f', header=names, comments="")
            
            # Graphic Output related code
            
    
            if self.p['singleRunGraphs']:
                self.doGraphs(folder)
    
        if self.p['interactiveGraphics']:
            print "Entering main loop to hold graphics up there."
            self.window.mainloop()

        return self.totalTaxBurden[-1]

    def initializePop(self):
        
        if self.p['loadFromFile'] == False:
            self.map = Map(self.p['mapGridXDimension'], 
                           self.p['mapGridYDimension'],
                           self.p['townGridDimension'],
                           self.p['cdfHouseClasses'],
                           self.p['ukMap'],
                           self.p['ukClassBias'],
                           self.p['mapDensityModifier'])
        else:
            self.map = pickle.load(open("initMap.txt", "rb"))
            
        if self.p['loadFromFile'] == False:
            self.pop = Population(self.p['initialPop'], self.p['startYear'],
                                  self.p['minStartAge'], self.p['maxStartAge'],
                                  self.p['numberClasses'],
                                  self.p['socialClasses'], 
                                  self.p['educationLevels'],
                                  self.p['initialClassShares'],
                                  self.p['initialUnemployment'],
                                  self.p['unemploymentAgeBandParam'],
                                  self.p['workingAge'],
                                  self.p['incomeInitialLevels'],
                                  self.p['incomeFinalLevels'],
                                  self.p['incomeGrowthRate'],
                                  self.p['workDiscountingTime'],
                                  self.p['wageVar'])
            
            men = [x for x in self.pop.allPeople if x.sex == 'male']
            remainingHouses = []
            remainingHouses.extend(self.map.allHouses)
            for man in men:
                man.house = random.choice(remainingHouses)
                if (man.status == 'employed'):
                    man.jobLocation = man.house.town
                else:
                    man.jobLocation = None
                # man.sec = man.house.size
                # Assumes house classes = SEC classes!
                self.map.occupiedHouses.append(man.house)
                remainingHouses.remove(man.house)
                woman = man.partner
                man.independentStatus = True
                woman.independentStatus = True
                woman.house = man.house
                if (woman.status == 'employed'):
                    woman.jobLocation = woman.house.town
                else:
                    woman.jobLocation = None
                woman.sec = man.sec
                man.house.occupants.append(man)
                man.house.occupants.append(woman)
                man.house.initialOccupants = 2
                
            
                
        else:
            self.pop = pickle.load(open("initPop.txt", "rb"))

        self.displayHouse = self.pop.allPeople[0].house
        self.nextDisplayHouse = None

        self.fert_data = np.genfromtxt('babyrate.txt.csv',
                                       skip_header=0, delimiter=',')
        self.death_female = np.genfromtxt('deathrate.fem.csv',
                                          skip_header=0, delimiter=',')
        self.death_male = np.genfromtxt('deathrate.male.csv',
                                        skip_header=0, delimiter=',')
        
        
        self.unemployment_series = np.genfromtxt('unemploymentrate.csv',
                                       skip_header=0, delimiter=',')
        
        
        visitedHouses = []
        maxSize = 0
        index = -1
        for person in self.pop.livingPeople:
            if person.house not in visitedHouses:
                visitedHouses.append(person.house)
                if len(person.house.occupants) > maxSize:
                    maxSize = len(person.house.occupants)
                    index = person.house.id
        
        
    def doOneYear(self):
        """Run one year of simulated time."""
        
        print('Population: ' + str(len(self.pop.livingPeople)))
        
        self.computeClassShares()
        
        print('Do Deaths')
        self.doDeaths()
        
        print('Do Births')
        self.doBirths()
        
        print('Divorces')
        self.doDivorces()
        
        print('Marriages')
        self.doMarriages()
        
        
        self.careNeeds()
        
        print('Care Supplies')
        self.careSupplies()
        
        print('Update Job Map')
        self.updateJobMap()
        
        
        self.updateUnemploymentRates()
        
        
        print('Social Care Map')
        self.socialCareMap()
        
        print('joiningSpouses')
        self.joiningSpouses()
        
        print('Allocate Care')
        self.allocateCare()
        
        print('Job Market')
        self.jobMarket()
        
        print('Moving Around')
        self.movingAround()
        
        
        self.doStats()
        
        print('Age Transition')
        self.ageTransitions()
        
        print('Care Transition')
        self.careTransitions()

        # self.householdSize()
        
        self.pyramid.update(self.year, self.p['num5YearAgeClasses'],
                            self.p['numCareLevels'],
                            self.p['pixelsInPopPyramid'],
                            self.pop.livingPeople)
        
        
        if (self.p['interactiveGraphics']):
            self.updateCanvas()
    
    
    def computeClassShares(self):
        
        self.socialClassShares[:] = []
        self.careNeedShares[:] = []
        numPop = float(len(self.pop.livingPeople))
        for c in range(self.p['numberClasses']):
            count = 0.0
            for x in self.pop.livingPeople:
                if x.classRank == c:
                    count += 1.0
            self.socialClassShares.append(count/numPop)
            
        for c in range(self.p['numberClasses']):
            classPop = [x for x in self.pop.livingPeople if x.classRank == c]
            numclassPop = float(len(classPop))
            needShares = []
            for b in range(self.p['numCareLevels']):
                count = 0.0
                for x in classPop:
                    if x.careNeedLevel == b:
                        count += 1.0
                needShares.append(count/numclassPop)
            self.careNeedShares.append(needShares)
    
    def deathProb(self, base, classRank, needLevel):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow(self.p['mortalityBias'], i)
        lowClassRate = base/a
        classRate = lowClassRate*math.pow(self.p['mortalityBias'], classRank)
        a = 0
        for i in range(self.p['numCareLevels']):
            a += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], i)
        lowerNeedRate = classRate/a
        deathProb = lowerNeedRate*math.pow(self.p['careNeedBias'], needLevel)
        return (deathProb)
    
    def doDeaths(self):
        
        preDeath = len(self.pop.livingPeople)
        
        deaths = [0, 0, 0, 0, 0]
        """Consider the possibility of death for each person in the sim."""
        for person in self.pop.livingPeople:
            age = person.age
            
            ####     Death process with histroical data  after 1950   ##################
            if self.year > 1950:
                if age > 109:
                    age = 109
                if person.sex == 'male':
                    rawRate = self.death_male[age, self.year-1950]
                if person.sex == 'female':
                    rawRate = self.death_female[age, self.year-1950]
                    
                dieProb = self.deathProb(rawRate, person.classRank, person.careNeedLevel)

            #############################################################################
            
                if random.random() < dieProb:
                    person.dead = True
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                    
                    # Check if the person leaves orphans
                    children = [x for x in person.children if x.status == 'child'and x.dead == False]
                    if len(children) > 0 and (person.partner == None or person.partner.dead == True):
                        # The children need to be adopted
                        # Find a suitable familiy
                        if children[0].house == self.displayHouse:
                                self.textUpdateList.append(str(self.year) + ": #" + str(children[0].id) + " and brothers will now be adopted.")
                        adoptiveMothers = [x for x in self.pop.livingPeople if x.status != 'child' and x.sex == 'female' and x.partner != None and x.dead == False]
                        adoptiveMother = random.choice(adoptiveMothers)
                        for child in children:
                            child.mother = adoptiveMother
                            adoptiveMother.children.append(child)
                            child.father = adoptiveMother.partner
                            adoptiveMother.partner.children.append(child)           
                            if adoptiveMother.house == self.displayHouse:
                                self.textUpdateList.append(str(self.year) + ": #" + str(children[0].id) +
                                               " and brothers have been newly adopted by " + str(adoptiveMother.id) + "." )
                                        
                        self.movePeopleIntoChosenHouse(adoptiveMother.house, person.house, children)
                        
            else: 
                
                #######   Death process with made-up rates  ######################
                babyDieProb = 0.0
                if age < 1:
                    babyDieProb = self.p['babyDieProb']
                if person.sex == 'male':
                    ageDieProb = ( ( math.exp( age /
                                               self.p['maleAgeScaling'] ) )
                                   * self.p['maleAgeDieProb'] )
                else:
                    ageDieProb = ( ( math.exp( age /
                                               self.p['femaleAgeScaling'] ) )
                                   * self.p['femaleAgeDieProb'] )
                rawRate = self.p['baseDieProb'] + babyDieProb + ageDieProb
                baseRate = self.baseRate(self.socialClassShares, self.p['mortalityBias'], rawRate)
                dieProb = baseRate*math.pow(self.p['mortalityBias'], person.classRank)
                
                
                ####################################################################
                
                if random.random() < dieProb:
                    person.dead = True
                    deaths[person.classRank] += 1
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                    
                    # Check if the person leaves orphans
                    children = [x for x in person.children if x.status == 'child'and x.dead == False]
                    if len(children) > 0 and (person.partner == None or person.partner.dead == True):
                        # The children need to be adopted
                        # Find a suitable familiy
                        if children[0].house == self.displayHouse:
                                self.textUpdateList.append(str(self.year) + ": #" + str(children[0].id) + " and brothers will now be adopted.")
                        adoptiveMothers = [x for x in self.pop.livingPeople if x.status != 'child' and x.sex == 'female' and x.partner != None and x.dead == False]
                        adoptiveMother = random.choice(adoptiveMothers)
                        for child in children:
                            child.mother = adoptiveMother
                            adoptiveMother.children.append(child)
                            child.father = adoptiveMother.partner
                            adoptiveMother.partner.children.append(child)           
                            if adoptiveMother.house == self.displayHouse:
                                self.textUpdateList.append(str(self.year) + ": #" + str(children[0].id) +
                                               " and brothers have been newly adopted by " + str(adoptiveMother.id) + "." )
                                        
                        self.movePeopleIntoChosenHouse(adoptiveMother.house, person.house, children)
                
                
        
        self.pop.livingPeople[:] = [x for x in self.pop.livingPeople if x.dead == False]
        
        postDeath = len(self.pop.livingPeople)
        
        self.deaths_1.append(deaths[0])
        self.deaths_2.append(deaths[1])
        self.deaths_3.append(deaths[2])
        self.deaths_4.append(deaths[3])
        self.deaths_5.append(deaths[4])
        
        print('the number of people who died is: ' + str(preDeath - postDeath))
        
        # print(len(self.pop.livingPeople))
    
    def doBirths(self):
        
        preBirth = len(self.pop.livingPeople)
        marriedLadies = 0
        adultLadies = 0
        births = [0, 0, 0, 0, 0]
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age > self.p['minPregnancyAge']
                                  and x.age < self.p['maxPregnancyAge']
                                  and x.partner != None and x.status != 'inactive']
                        
        for person in self.pop.livingPeople:
           
            if person.sex == 'female' and person.age >= self.p['minPregnancyAge']:
                adultLadies += 1
                if person.partner != None:
                    marriedLadies += 1
        marriedPercentage = float(marriedLadies)/float(adultLadies)
        
        for woman in womenOfReproductiveAge:
                if self.year < 1951:
                    rawRate = self.p['growingPopBirthProb']
                else:
                    rawRate = (self.fert_data[(self.year - woman.birthdate)-16,self.year-1950])/marriedPercentage
                baseRate = self.baseRate(self.socialClassShares, self.p['fertilityBias'], rawRate)
                birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
                
                if random.random() < birthProb:
                    # (self, mother, father, age, birthYear, sex, status, house,
                    # classRank, sec, edu, wage, income, finalIncome):
                    
                    baby = Person(woman, woman.partner, 0, self.year, 'random', 
                                  'child', woman.house, woman.classRank, woman.sec, None, 0, 0, 0, 0, 0, 0, 0)
                    births[woman.classRank] += 1
                    self.pop.allPeople.append(baby)
                    self.pop.livingPeople.append(baby)
                    woman.house.occupants.append(baby)
                    woman.children.append(baby)
                    woman.partner.children.append(baby)
                    if woman.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(woman.id) + " had a baby, #" + str(baby.id) + "." 
                        self.textUpdateList.append(messageString)
        postBirth = len(self.pop.livingPeople)
        
        self.births_1.append(births[0])
        self.births_2.append(births[1])
        self.births_3.append(births[2])
        self.births_4.append(births[3])
        self.births_5.append(births[4])
        
        print('the number of births is: ' + str(postBirth - preBirth))
    
    def careNeeds(self):
        
        for person in self.pop.livingPeople:
            person.visitedCarer = False
            person.hoursDemand = 0
            person.hoursInformalSupply = 0
            person.hoursFormalSupply = 0
            person.residualNeed = 0
            person.residualInformalSupply = 0
            person.residualFormalSupply = 0
            person.socialWork = 0
            person.workToCare = 0
            person.totalSupply = 0
            person.extraworkCare = 0
            person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            
            careNeed = self.p['careDemandInHours'][person.careNeedLevel]

            person.hoursDemand = careNeed
            person.residualNeed = person.hoursDemand
                
            if person.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(person.id) + " now has "
                messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                self.textUpdateList.append(messageString)
                       
        children = [x for x in self.pop.livingPeople if x.age < 16]
        
        for child in children:
            care = self.p['zeroYearCare']/math.exp(self.p['childcareDecreaseRate']*child.age)
            care = int((care+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            if ( child.hoursDemand < care ):
                child.hoursDemand = care
                child.residualNeed = child.hoursDemand
            if child.age == 0 and child.mother.status != 'inactive':
                child.mother.socialWork = self.p['zeroYearCare']
                child.mother.income = 0
                child.mother.status = 'maternity'
                child.mother.babyCarer = True
                child.residualNeed = 0
                child.informalCare = self.p['zeroYearCare']
    
    
    def careTransitions(self):
        
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        
        for person in peopleNotInCriticalCare:
            if person.sex == 'male':
                ageCareProb = ( ( math.exp( person.age /
                                            self.p['maleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            else:
                ageCareProb = ( ( math.exp( person.age /
                                           self.p['femaleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            careProb = (self.p['baseCareProb'] + ageCareProb)
            baseProb = self.baseRate(self.socialClassShares, self.p['careBias'], careProb)
            careProb = baseProb*math.pow(self.p['careBias'], person.classRank)
            
            if random.random() < careProb:
                person.status = 'inactive'
                baseTransition = self.baseRate(self.socialClassShares, self.p['careBias'], 1-self.p['careTransitionRate'])
                unmetNeedFactor = 1/math.exp(self.p['unmetNeedExponent']*person.residualNeed)
                transitionRate = (1.0 - baseTransition*math.pow(self.p['careBias'], person.classRank))*unmetNeedFactor
                stepCare = 1
                bound = transitionRate
                while random.random() > bound and stepCare < self.p['numCareLevels'] - 1:
                    stepCare += 1
                    bound += (1-bound)*transitionRate
                person.careNeedLevel += stepCare
                
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = self.p['numCareLevels'] - 1
                    
            if person.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(person.id) + " now has "
                messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                self.textUpdateList.append(messageString)
                       
                
    def careSupplies(self):
        
        for agent in self.pop.livingPeople:
            if agent.visitedCarer == True:
                continue
            if agent.justMarried == None:
                household = [x for x in agent.house.occupants if x.justMarried == None]
            else:
                household = [x for x in agent.house.occupants if x.justMarried == agent.partner.id]
                household.extend([x for x in agent.partner.house.occupants if x.justMarried == agent.id])
                
            for member in household:
                member.visitedCarer = True
                
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in household if x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            for member in notWorking:
                if member.status == 'student':
                    individualSupply = self.p['studentHours']
                elif member.status == 'retired':
                    individualSupply = self.p['retiredHours']
                elif member.status == 'unemployed':
                    individualSupply = self.p['unemployedHours']
                member.residualInformalSupply = int((individualSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                member.hoursInformalSupply = member.residualInformalSupply

            employed = [x for x in householdCarers if x.status == 'employed']
            employed.sort(key=operator.attrgetter("wage"))

            householdIncome = self.householdIncome(household)
            householdPerCapitaIncome = householdIncome/float(len(household))
            
            # Compute the total income devoted to informal care supply
            incomeCoefficient = math.exp(self.p['incomeCareParam']*householdPerCapitaIncome)
            residualIncomeForCare = householdIncome*(1 - 1/incomeCoefficient)
            # Assign the total informal care supply to the employed members of the household (according to income)
            for worker in employed:
                worker.extraworkCare = self.p['employedHours']
                worker.hoursInformalSupply = worker.extraworkCare
                # worker.extraworkCare = self.p['employedHours']
                maxIndividualHours = residualIncomeForCare/worker.wage
                if maxIndividualHours > self.p['weeklyHours']:
                    individualSupply = self.p['weeklyHours']
                else:
                    individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                worker.residualInformalSupply = individualSupply
                worker.hoursInformalSupply += worker.residualInformalSupply
                residualIncomeForCare -= individualSupply*worker.wage
                if residualIncomeForCare <= 0:
                    break

            # Compute the total income-based formal care supply   
            householdEmployedFormalSupply = householdIncome*(1 - 1/incomeCoefficient)/self.p['priceSocialCare']
            householdEmployedFormalSupply = int((householdEmployedFormalSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            # Assign the total income-based formal care supply to the employed members of the household (according to income) 
            residualSupply = householdEmployedFormalSupply
            for person in employed:
                individualSupply = min(self.p['weeklyHours'], residualSupply)
                person.residualFormalSupply = individualSupply
                person.hoursFormalSupply = person.residualFormalSupply
                residualSupply -= person.residualFormalSupply
                if residualSupply <= 0:
                    break
    
    def socialCareMap(self):
        
        for person in self.pop.livingPeople:
            person.visitedCarer = False
            
        for person in self.pop.livingPeople:
            
            if person.visitedCarer == True:
                continue
            
            if person.justMarried == None:
                household = [x for x in person.house.occupants if x.justMarried == None]
            else:
                household = [x for x in person.house.occupants if x.justMarried == person.partner.id]
                household.extend([x for x in person.partner.house.occupants if x.justMarried == person.id])
            
            for member in household:
                member.visitedCarer = True

            householdDemand = 0
            householdSupply = 0
            potentialIncome = 0
            for member in household:
                if member.status == 'employed' or member.status == 'retired':
                    potentialIncome += member.income
                elif member.status == 'unemployed':
                    potentialIncome += self.expectedIncome(member, member.house.town)
                    
                householdDemand += member.hoursDemand
                householdSupply += member.residualInformalSupply
                householdSupply += member.residualFormalSupply
                householdSupply += member.extraworkCare
            potentialIncome /= float(len(household))
            deltaHouseholdCare = householdSupply - householdDemand
            visitedPeople = []
            for town in self.map.towns:
                townNetworkDemand = 0
                townNetworkSupply = 0
                # Kinship distance == 1 (partents and children)
                kinshipDemand = 0
                kinshipSupply = 0
                kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*1.0)
                for member in household:
                    if member.father != None:
                        if member.father.dead == False and member.father not in visitedPeople and member.father not in household and member.father.house.town == town:
                            kinshipDemand += member.father.hoursDemand*kinshipWeight
                            kinshipSupply += member.father.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.father.extraworkCare*kinshipWeight
                            visitedPeople.append(member.father)
                        if member.mother.dead == False and member.mother not in visitedPeople and member.mother not in household and member.mother.house.town == town:
                            kinshipDemand += member.mother.hoursDemand*kinshipWeight
                            kinshipSupply += member.mother.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.mother.extraworkCare*kinshipWeight
                            visitedPeople.append(member.mother)
                    for child in member.children:
                        if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
                            kinshipDemand += child.hoursDemand*kinshipWeight
                            kinshipSupply += child.residualInformalSupply*kinshipWeight
                            kinshipSupply += child.extraworkCare*kinshipWeight
                            visitedPeople.append(child) 
                townNetworkDemand += kinshipDemand
                townNetworkSupply += kinshipSupply
                # Kinship distance == 2 (grandparents, grandchildren and brothers/sisters)   
                kinshipDemand = 0
                kinshipSupply = 0
                kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*2.0) 
                for member in household:
                    if member.father != None and member.father.father != None:
                        if member.father.father.dead == False and member.father.father not in visitedPeople and member.father.father not in household and member.father.father.house.town == town:
                            kinshipDemand += member.father.father.hoursDemand*kinshipWeight
                            kinshipSupply += member.father.father.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.father.father.extraworkCare*kinshipWeight
                            visitedPeople.append(member.father.father)
                        if member.father.mother.dead == False and member.father.mother not in visitedPeople and member.father.mother not in household and member.father.mother.house.town == town:
                            kinshipDemand += member.father.mother.hoursDemand*kinshipWeight
                            kinshipSupply += member.father.mother.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.father.mother.extraworkCare*kinshipWeight
                            visitedPeople.append(member.father.mother)
                        if member.mother.father.dead == False and member.mother.father not in visitedPeople and member.mother.father not in household and member.mother.father.house.town == town:
                            kinshipDemand += member.mother.father.hoursDemand*kinshipWeight
                            kinshipSupply += member.mother.father.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.mother.father.extraworkCare*kinshipWeight
                            visitedPeople.append(member.mother.father)
                        if member.mother.mother.dead == False and member.mother.mother not in visitedPeople and member.mother.mother not in household and member.mother.mother.house.town == town:
                            kinshipDemand += member.mother.mother.hoursDemand*kinshipWeight
                            kinshipSupply += member.mother.mother.residualInformalSupply*kinshipWeight
                            kinshipSupply += member.mother.mother.extraworkCare*kinshipWeight
                            visitedPeople.append(member.mother.mother)
                    for child in member.children:
                        for grandson in child.children:
                            if grandson.dead == False and grandson not in visitedPeople and grandson not in household and grandson.house.town == town:
                                kinshipDemand += grandson.hoursDemand*kinshipWeight
                                kinshipSupply += grandson.residualInformalSupply*kinshipWeight
                                kinshipSupply += grandson.extraworkCare*kinshipWeight
                                visitedPeople.append(grandson) 
                    if member.father != None:
                        brothers = list(set(member.father.children + member.mother.children))
                        brothers.remove(member)
                        for brother in brothers:
                            if brother.dead == False and brother not in visitedPeople and brother not in household and brother.house.town == town:
                                kinshipDemand += brother.hoursDemand*kinshipWeight
                                kinshipSupply += brother.residualInformalSupply*kinshipWeight
                                kinshipSupply += brother.extraworkCare*kinshipWeight
                                visitedPeople.append(brother) 
                townNetworkDemand += kinshipDemand
                townNetworkSupply += kinshipSupply
                # Kinship distance == 3 (uncles/aunts and grandchildren and nephews/nieces)   
                kinshipDemand = 0
                kinshipSupply = 0
                kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*3.0) 
                for member in household:
                    if member.father != None and member.father.father != None:
                        maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
                        maternalUncles.remove(member.mother)
                        paternalUncles = list(set(member.father.father.children + member.father.mother.children))
                        paternalUncles.remove(member.father)
                        unclesList = list(set(maternalUncles + paternalUncles))
                        unclesList = [x for x in unclesList if x.dead == False]
                        for uncle in unclesList:
                            if uncle.dead == False and uncle not in visitedPeople and uncle not in household and uncle.house.town == town:
                                kinshipDemand += uncle.hoursDemand*kinshipWeight
                                kinshipSupply += uncle.residualInformalSupply*kinshipWeight
                                kinshipSupply += uncle.extraworkCare*kinshipWeight
                                visitedPeople.append(uncle)
                    if member.father != None:
                        brothers = list(set(member.father.children + member.mother.children))
                        brothers = [x for x in brothers if x.dead == False]
                        brothers.remove(member)
                        for brother in brothers:
                            for child in brother.children:
                                if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
                                    kinshipDemand += child.hoursDemand*kinshipWeight
                                    kinshipSupply += child.residualInformalSupply*kinshipWeight
                                    kinshipSupply += child.extraworkCare*kinshipWeight
                                    visitedPeople.append(child) 
                townNetworkDemand += kinshipDemand
                townNetworkSupply += kinshipSupply
                deltaNetworkCare = townNetworkDemand - townNetworkSupply
                if deltaHouseholdCare < 0:
                    networkSocialCareParam = self.p['excessNeedParam']
                else:
                    networkSocialCareParam = self.p['excessNeedParam']*self.p['careSupplyBias']
                townSCI = (networkSocialCareParam*deltaHouseholdCare*deltaNetworkCare) # /math.exp(self.p['careIncomeParam']*potentialIncome)
                for member in household:
                    member.socialCareMap.append(townSCI)
                
                    
    def allocateCare(self):
        
        careReceivers = [x for x in self.pop.livingPeople if x.hoursDemand > 0 and x.age > 0]
        for receiver in careReceivers:
            receiver.informalCare = 0
            receiver.formalCare = 0
            receiver.socialNetwork[:] = self.kinshipNetwork(receiver)
            receiver.totalSupply = self.totalSupply(receiver)
        
        residualReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.totalSupply > 0]
        while len(residualReceivers) > 0:
            careList = [x.residualNeed for x in residualReceivers]
            probReceivers = [i/sum(careList) for i in careList]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            self.getCare(receiver)
            careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
            for receiver in careReceivers:
                receiver.totalSupply = self.totalSupply(receiver)
            residualReceivers = [x for x in careReceivers if x.totalSupply > 0]
    
    def kinshipNetwork(self, pin):
        kn = []
        households = []
        # Household members
        householdMembers = []
        for member in pin.house.occupants:
            if member.hoursDemand == 0 and member.house not in households:
                householdMembers.append(member)
                households.append(member.house)
        kn.append(householdMembers)
        # Parents
        parents = []
        if pin.father != None:
            if pin.father.dead == False and pin.father.house not in households:
                parents.append(pin.father)
                households.append(pin.father.house)
            if pin.mother.dead == False and pin.mother.house not in households:
                parents.append(pin.mother)
                households.append(pin.mother.house)
        kn.append(parents)
        # Grandparents
        grandparents = []
        if pin.father != None and pin.father.father != None:
            if pin.father.father.dead == False and pin.father.father.house not in households and pin.father.father.house.town == pin.house.town:
                grandparents.append(pin.father.father)
                households.append(pin.father.father.house)
            if pin.father.mother.dead == False and pin.father.mother.house not in households and pin.father.mother.house.town == pin.house.town:
                grandparents.append(pin.father.mother)
                households.append(pin.father.mother.house)
            if pin.mother.father.dead == False and pin.mother.father.house not in households and pin.mother.father.house.town == pin.house.town:
                grandparents.append(pin.mother.father)
                households.append(pin.mother.father.house)
            if pin.mother.mother.dead == False and pin.mother.mother.house not in households and pin.mother.mother.house.town == pin.house.town:
                grandparents.append(pin.mother.mother)
                households.append(pin.mother.mother.house)
        kn.append(grandparents)
        # Indipendent children
        independentChildren = []
        for child in pin.children:
            if child.dead == False and child.house not in households:
                independentChildren.append(child)
                households.append(child.house)
        kn.append(independentChildren)
        # Independent grandchildren
        independentGrandsons = []
        for child in pin.children:
            for grandson in child.children:
                if grandson.dead == False and grandson.house not in households and grandson.house.town == pin.house.town:
                    independentGrandsons.append(grandson)
                    households.append(grandson.house)
        kn.append(independentGrandsons)  
         # Indipendent brothers and sisters
        independentBrothers = []
        nephews = []
        if pin.father != None:
            brothers = list(set(pin.father.children+pin.mother.children))
            brothers = [x for x in brothers if x.dead == False]
            brothers.remove(pin)
            for brother in brothers:
                if brother.dead == False and brother.house not in households and brother.house.town == pin.house.town:
                    independentBrothers.append(brother)
                    households.append(brother.house)
                for child in brother.children:
                    if child.dead == False and child.house not in households and child.house.town == pin.house.town:
                        nephews.append(child)
                        households.append(child.house)
        kn.append(independentBrothers)
        # Uncles and aunts
        uncles = []
        if pin.father != None and pin.father.father != None:
            maternalUncles = list(set(pin.mother.father.children + pin.mother.mother.children))
            maternalUncles.remove(pin.mother)
            paternalUncles = list(set(pin.father.father.children + pin.father.mother.children))
            paternalUncles.remove(pin.father)
            unclesList = list(set(maternalUncles+paternalUncles))
            unclesList = [x for x in unclesList if x.dead == False]
            for uncle in unclesList:
                if uncle.dead == False and uncle.house not in households and uncle.house.town == pin.house.town:
                    uncles.append(uncle)
                    households.append(uncle.house)
        kn.append(uncles)
        # Nephews and Nieces
        kn.append(nephews)
        return (kn)
    
    def totalSupply(self, receiver):
        totalSupply = 0
        townReceiver = receiver.house.town 
        networkList = []
        supplies = []
        for i in range(len(receiver.socialNetwork)):
            for j in receiver.socialNetwork[i]:
                networkList.append(j)
        for carer in networkList:
            townCarer = carer.house.town
            household = carer.house.occupants
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in householdCarers if x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            employed = [x for x in householdCarers if x.status == 'employed']
            totsupply = 0
            if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
                if townCarer != townReceiver:
                    for member in employed:
                        totsupply += member.residualFormalSupply
                else:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        if member.wage > self.p['priceSocialCare']:
                            totsupply += member.residualFormalSupply
                        else:   
                            totsupply += member.residualInformalSupply
            else:
                if townCarer == townReceiver:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
            
            supplies.append(totsupply)

        totalSupply = sum(supplies)
        # Then, randomly select a supplier according to the weighted supplies
        return(totalSupply)
    
    def getCare(self, receiver):
        receiver.residualNeed -= self.p['quantumCare'] 
        townReceiver = receiver.house.town 
        informalCare = 0
        formalCare = 0
        networkList = []
        indexSupply = []
        for i in range(len(receiver.socialNetwork)):
            for j in receiver.socialNetwork[i]:
                networkList.append(j)
                indexSupply.append(int(self.p['socialNetworkDistances'][i]))
        probCarers = self.probSuppliers(receiver)
        carer = np.random.choice(networkList, p = probCarers)
        index = networkList.index(carer)
        townCarer = carer.house.town
        household = carer.house.occupants
        householdCarers = [x for x in household if x.hoursDemand == 0]
        notWorking = [x for x in householdCarers if x.residualInformalSupply > 0]
        retired = [x for x in notWorking if x.status == 'retired']
        retired.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        students = [x for x in notWorking if x.status == 'student']
        students.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        unemployed = [x for x in notWorking if x.status == 'unemployed']
        unemployed.sort(key=operator.attrgetter("wage"))
        employed = [x for x in householdCarers if x.status == 'employed' and (x.extraworkCare > 0 or x.residualInformalSupply > 0 or x.residualFormalSupply > 0)]
        employed.sort(key=operator.attrgetter("wage"))
        # Finally, extract a 'quantum' of care from one of the selected household's members.
        check = 0
        supplier = 'none'
        if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
            if townCarer == townReceiver:
                if len(retired) > 0:
                    retired[0].residualInformalSupply -= self.p['quantumCare']
                    retired[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                    supplier = 'retired (close relative, in town)'
                elif len(students) > 0:
                    students[0].residualInformalSupply -= self.p['quantumCare']
                    students[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                    supplier = 'student (close relative, in town)'
                elif len(unemployed) > 0:
                    for member in unemployed:
                        if member.residualInformalSupply > 0:
                            member.residualInformalSupply -= self.p['quantumCare']
                            member.socialWork += self.p['quantumCare']
                            informalCare = self.p['quantumCare']
                            supplier = 'unemployed (close relative, in town)'
                            break
                elif len(employed) > 0:
                    for member in employed:
                        if member.extraworkCare > 0:
                            member.socialWork += self.p['quantumCare']
                            member.extraworkCare -= self.p['quantumCare']
                            informalCare = self.p['quantumCare']
                            supplier = 'employed: extraworkCare (close relative, in town)'
                            break
                        else:
                            if member.wage < self.p['priceSocialCare']: 
                                if member.residualInformalSupply > 0:
                                    member.residualInformalSupply -= self.p['quantumCare']
                                    if member.residualFormalSupply > 0:
                                        member.residualFormalSupply -= self.p['quantumCare']
                                    member.socialWork += self.p['quantumCare']
                                    informalCare = self.p['quantumCare']
                                    supplier = 'employed: informal care (close relative, in town)'
                                    break
                            else: 
                                if member.residualFormalSupply > 0:
                                    member.residualFormalSupply -= self.p['quantumCare']
                                    if member.residualInformalSupply > 0:
                                        member.residualInformalSupply -= self.p['quantumCare']
                                    member.workToCare += self.p['quantumCare']
                                    formalCare = self.p['quantumCare']
                                    supplier = 'employed: formal care (close relative, in town)'
                                    break
            else:
                for member in employed:
                     if member.residualFormalSupply > 0:
                         member.residualFormalSupply -= self.p['quantumCare']
                         if member.residualInformalSupply > 0:
                             member.residualInformalSupply -= self.p['quantumCare']
                         member.workToCare += self.p['quantumCare']
                         formalCare = self.p['quantumCare']
                         supplier = 'employed: formal care (close relative, not in town)'
                         break
                         
        else:
            if townCarer == townReceiver: 
                if len(retired) > 0:
                    retired[0].residualInformalSupply -= self.p['quantumCare']
                    retired[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                    supplier = 'retired (not close relative, in town)'
                elif len(students) > 0:
                    students[0].residualInformalSupply -= self.p['quantumCare']
                    students[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                    supplier = 'student (not close relative, in town)'
                elif len(unemployed) > 0:
                    for member in unemployed:
                        if member.residualInformalSupply > 0:
                            member.residualInformalSupply -= self.p['quantumCare']
                            member.socialWork += self.p['quantumCare']
                            informalCare = self.p['quantumCare']
                            supplier = 'unemployed (not close relative, in town)'
                            break
                elif len(employed) > 0:
                    for member in employed:
                        if member.extraworkCare > 0:
                            member.socialWork += self.p['quantumCare']
                            member.extraworkCare -= self.p['quantumCare']
                            informalCare = self.p['quantumCare']
                            supplier = 'employed (not close relative, in town)'
                            break
                       # employed[0].residualInformalSupply -= self.p['quantumCare']
                       # employed[0].residualSupply -= self.p['quantumCare']
                       # employed[0].socialWork += self.p['quantumCare']
                       # informalCare = self.p['quantumCare']
        
        receiver.informalCare += informalCare
        receiver.formalCare += formalCare
        receiver.informalSupplyByKinship[indexSupply[index]] += informalCare
        receiver.formalSupplyByKinship[indexSupply[index]] += formalCare
        # receiver.totalSupply -= self.p['quantumCare']
        
    
    def probSuppliers(self, receiver):       
        townReceiver = receiver.house.town 
        networkList = []
        weights = []
        weightedSupplies = []
        for i in range(len(receiver.socialNetwork)):
            for j in receiver.socialNetwork[i]:
                networkList.append(j)
                weights.append(self.p['socialNetworkDistances'][i])
        for carer in networkList:
            index = networkList.index(carer)
            kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*weights[index])
            townCarer = carer.house.town
            household = carer.house.occupants
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in householdCarers if x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            employed = [x for x in householdCarers if x.status == 'employed']
            weightedHouseholdSupply = 0
            totsupply = 0
            if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
                if townCarer != townReceiver:
                    for member in employed:
                        totsupply += member.residualFormalSupply
                else:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        if member.wage > self.p['priceSocialCare']:
                            totsupply += member.residualFormalSupply
                        else:   
                            totsupply += member.residualInformalSupply
                        
            elif townCarer == townReceiver:
                for member in notWorking:
                    totsupply += member.residualInformalSupply
                for member in employed:
                    totsupply += member.extraworkCare
            
            weightedHouseholdSupply = totsupply*kinshipWeight
            weightedSupplies.append(weightedHouseholdSupply)
        
        # Then, randomly select a supplier according to the weighted supplies
        totWeightedSupplies = sum(weightedSupplies)
        probCarers = [i/totWeightedSupplies for i in weightedSupplies]
        return(probCarers)       
                
    def householdIncome(self, hm):
        income = 0
        for member in hm:
            income += member.income
        return(income)
        
    def householdMinWage(self, hm):
        wages = []
        for member in hm:
            if member.status == 'employed':
                wages.append(member.wage)
        minWage = min(wages)
        return(minWage)
         
    def ageTransitions(self):
       # peopleNotYetRetired = [x for x in self.pop.livingPeople if x.status != 'retired']
       
       # As the years go by, people change their status from 'child' to 'student', 
       # from 'student' to 'unemployed' (i.e. enter the workforce) and
       # from 'employed' (or 'unemployed') to retired
       # (additional states are: 'inactive', for people needing care; 
       # and 'maternity', for mothers of babies in their first year).
       
        for person in self.pop.livingPeople:
            person.age += 1
            # person.justMarried = None
            
        for person in self.pop.livingPeople:
            if person.status == 'maternity':
                minAge = min([x.age for x in person.children])
                if minAge > 0:
                    person.babyCarer == False
                    self.enterWorkForce(person)
            
        activePop = [x for x in self.pop.livingPeople if x.status != 'inactive']
        
        for person in activePop:
            if person.age == self.p['minWorkingAge']:
                person.status = 'student'
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 0)
                if random.random() > probStudy:
                    person.classRank = 0
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now a student.")
            if ( person.age == 18 and person.status == 'student'):
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 1)
                if random.random() > probStudy:
                    person.classRank = 1
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
            if ( person.age == 20 and person.status == 'student'):
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 2)
                if random.random() > probStudy:
                    person.classRank = 2
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
            if ( person.age == 22 and person.status == 'student'):
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 3)
                if random.random() > probStudy:
                    person.classRank = 3
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
            if ( person.age == 24 and person.status == 'student'):
                person.classRank = 4
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                        
            if person.age == self.p['ageOfRetirement']:
                person.status = 'retired'
                person.income = self.p['pensionWage'][person.classRank]*self.p['weeklyHours']
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " has now retired.")
                        
            if person.status == 'student' and person.mother.dead and person.father.dead:
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
    
    def transitionProb (self, person, stage):
        household = person.house.occupants
        if person.father.dead + person.mother.dead != 2:
            pStudy = 0
            potentialIncome = 0
            for member in household:
                if member.status == 'employed' or member.status == 'retired':
                    potentialIncome += member.income
                elif member.status == 'unemployed':
                    potentialIncome += self.expectedIncome(member, member.house.town)
            perCapitaIncome = potentialIncome/float(len(household))
            if perCapitaIncome > 0:
                forgoneSalary = self.p['incomeInitialLevels'][stage]*self.p['weeklyHours']
                educationCosts = self.p['educationCosts'][stage]
                relCost = (forgoneSalary+educationCosts)/perCapitaIncome
                incomeEffect = self.p['costantIncomeParam']/math.exp(self.p['eduWageSensitivity']*relCost)
                targetEL = max(person.father.classRank, person.mother.classRank)
                dE = targetEL - stage
                expEdu = math.exp(self.p['eduRankSensitivity']*dE)
                educationEffect = expEdu/(expEdu+self.p['costantEduParam'])
                pStudy = math.pow(incomeEffect, self.p['incEduExp'])*math.pow(educationEffect, 1-self.p['incEduExp'])
        else:
            pStudy = 0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        return (pStudy)
    
    def enterWorkForce(self, person):
        person.status = 'unemployed'
        person.wage = self.marketWage(person)
        person.income = 0
        person.finalIncome = 0
        person.jobTenure = 0
        person.jobLocation = None
        person.searchJob = True
    
    def marketWage(self, person):
         # Gompertz Law
        k = self.p['incomeFinalLevels'][person.classRank]
        r = self.p['incomeGrowthRate'][person.classRank]
        c = np.log(self.p['incomeInitialLevels'][person.classRank]/k)
        exp = c*math.exp(-1*r*person.workingTime)
        marketWage = k*math.exp(exp)
        return (marketWage)
    
    def doDivorces(self):

        menInRelationships = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner != None ]
        for man in menInRelationships:
            if self.year < self.p['thePresent']:
                rawSplit = self.p['basicDivorceRate'] * self.p['divorceModifierByDecade'][man.age/10]
            else:
                rawSplit = self.p['variableDivorce'] * self.p['divorceModifierByDecade'][man.age/10]      
            baseRate = self.baseRate(self.socialClassShares, self.p['divorceBias'], rawSplit)
            splitProb = baseRate*math.pow(self.p['divorceBias'], man.classRank)
            
            if random.random() < splitProb:
                man.movedThisYear = True
                wife = man.partner
                man.partner = None
                wife.partner = None
                self.divorceTally += 1
                
                # Find a new house: the choice should be based on social class
                # distance = random.choice(['near','far'])
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " splits with #" + str(wife.id) + "."
                    self.textUpdateList.append(messageString)
                    
                self.findNewHouse([man], man.house.town)
    
    def doMarriages(self):
 
        eligibleMen = []
        eligibleWomen = []

        for i in self.pop.livingPeople:
            if i.status != 'child' and i.partner == None:
                # Men need to be employed to marry
                if i.sex == 'male' and i.status == 'employed':
                    eligibleMen.append(i)
                    
        ######     Otional: select a subset of eligible men based on age    ##########################################
        potentialGrooms = []
        for m in eligibleMen:
            manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][m.age/10]
            if random.random() < manMarriageProb:
                potentialGrooms.append(m)
        ###########################################################################################################
        
        for man in potentialGrooms: # for man in eligibleMen: # 
            # maxEncounters = self.datingActivity(man)
            eligibleWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age > 15 and x.partner == None]
            
            potentialBrides = []
            for woman in eligibleWomen:
                if man.mother != None and woman.mother != None:
                    if man.mother != woman.mother and man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                else:
                    if man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                        
            # if maxEncounters < len(potentialBrides):
               #  numberEncounters = maxEncounters
            # else:
               #  numberEncounters = len(potentialBrides)
            if len(potentialBrides) > 0:
                manTown = man.house.town
                bridesWeights = []
                for woman in potentialBrides:
                    womanTown = woman.house.town
                    geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                    geoEffect = 1/math.exp(self.p['betaGeoExp']*geoDistance)
                    statusDistance = float(abs(man.classRank-woman.classRank))/float((self.p['numberClasses']-1))
                    socEffect = 1/math.exp(self.p['betaSocExp']*statusDistance)
                    ageEffect = self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                    # alphaAgeExp = 1 - (self.p['alphaGeoExp']+self.p['alphaSocExp'])
                    geoFactor = math.pow(geoEffect, self.p['alphaGeoExp'])
                    socExponent = 1 - self.p['alphaGeoExp']
                    # socFactor = math.pow(socEffect, self.p['alphaSocExp'])
                    socFactor = math.pow(socEffect, socExponent)
                    # ageFactor = math.pow(ageEffect, alphaAgeExp)
                    marriageProb = geoFactor*socFactor*ageEffect #ageFactor
                    bridesWeights.append(marriageProb)
                bridesProb = [i/sum(bridesWeights) for i in bridesWeights]
                woman = np.random.choice(potentialBrides, p = bridesProb)
                man.partner = woman
                woman.partner = man
                man.justMarried = woman.id
                woman.justMarried = man.id
                childrenWithMan = [x for x in man.children if x.dead == False and x.house == man.house]
                for child in childrenWithMan:
                    child.justMarried = woman.id
                childrenWithWoman = [x for x in woman.children if x.dead == False and x.house == woman.house]
                for child in childrenWithWoman:
                    child.justMarried = man.id
                self.marriageTally += 1
    
            if man.house == self.displayHouse or woman.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                messageString += ") marry."
                self.textUpdateList.append(messageString)
         
        # poolMen = float(len(eligibleMen))
        # menMarried = 0.0
        # while ( len(eligibleMen) > 0 and len(eligibleWomen) > 0 and menMarried/poolMen  < self.p['basicMaleMarriageProb'] ):
            
            # dageProb = 0.0
            # while (random.random() > dageProb):
                # probWed = 0.0
                # while (random.random() > probWed):
                    # man = np.random.choice(eligibleMen)
                    # probWed = self.p['maleMarriageProb'][self.getCat(man.age)]
                    
                    # eligibleWomen = []
                    
                # probWed = 0.0
                # while (random.random() > probWed):
                    # woman = np.random.choice(eligibleWomen) 
                    
                    # probWed = 1.0 # self.p['femaleMarriageProb'][self.getCat(woman.age)]
                    
                # dageProb = 1.0 # self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                
                # if man.mother != None and woman.mother != None:
                    # if man.mother == woman.mother:
                        # dageProb = 0.0
                        
                # if man.house == woman.house or man in woman.children or woman in man.children:
                    # dageProb = 0.0
                    
                # if man.income + woman.income == 0.0:
                    # dageProb = 0.0
                    
            # manTown = man.house.town
            # womanTown = woman.house.town
            # geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
            # statusDistance = float(abs(man.classRank-woman.classRank))/float((self.p['numClasses']-1))
            # geoEffect = self.p['betaGeo']*math.pow(geoDistance, self.p['expGeo'])
            # socEffect = self.p['betaSoc']*math.pow(statusDistance, self.p['expSoc'])
            
            # probMarriage = 0.0 # 1/math.exp(geoEffect + socEffect) # 
            
            # if (random.random() > probMarriage):
                # menMarried += 1
                # man.partner = woman
                # woman.partner = man
                
                # if man.partner in man.children:
                    # print('Married with daughter: ' + str(woman.id))
                # if woman.partner in woman.children:
                    # print('Married with son; ' + str(man.id))
                    
                # eligibleMen.remove(man)
                # eligibleWomen.remove(woman)
                # self.marriageTally += 1
                
                # if man.house == self.displayHouse or woman.house == self.displayHouse:
                    # messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                    # messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                    # messageString += ") marry."
                    # self.textUpdateList.append(messageString)
    
    
    def updateUnemploymentRates(self):
        
        unemployment = self.unemployment_series[(self.year-self.p['startYear'])]
        
        activePop = [x for x in self.pop.livingPeople if x.status == 'employed' or x.status == 'unemployed']
        
        numActivePop = float(len(activePop))
        classShares = []
        
        for c in range(self.p['numberClasses']):
            count = 0.0
            for x in activePop:
                if x.classRank == c:
                    count += 1.0
            classShares.append(count/numActivePop)
            
        for c in range(self.p['numberClasses']):
            
            classPop = [x for x in activePop if x.classRank == c]
            numclassPop = float(len(classPop))
            ageBandShares = []
            for b in range(self.p['numberAgeBands']):
                count = 0.0
                for x in classPop:
                    if self.ageBand(x.age) == b:
                        count += 1.0
                ageBandShares.append(count/numclassPop)
        
        for person in activePop:
            person.unemploymentRate = self.unemploymentRate(classShares, ageBandShares, self.p['unemploymentClassBias'], 
                                                         self.p['unemploymentAgeBias'], unemployment, 
                                                         self.ageBand(person.age), person.classRank)
            
            
    def updateJobMap(self):
        self.jobMarketMap[:] = []
        totalHouseholds = len(self.map.allHouses)
        for h in self.map.occupiedHouses:
                ranks = [x.classRank for x in h.occupants]
                h.rank = max(ranks)
        for c in range(self.p['numberClasses']):
            townJobProb = []
            n = len([x for x in self.map.occupiedHouses if x.rank == c])
            for t in self.map.towns:
                townHouses = len([x for x in t.houses])
                townRelativeDimension = float(townHouses)/float(totalHouseholds)
                j = len([x for x in t.houses if len(x.occupants) > 0 and x.rank == c])
                classRelativeDimension = float(j + self.p['minClassWeightParam'])/float(n + self.p['minClassWeightParam'])
                sizeFactor =  math.pow(townRelativeDimension, self.p['sizeWeightParam'])
                classFactor = math.pow(classRelativeDimension, 1-self.p['sizeWeightParam'])
                townJobProb.append(sizeFactor*classFactor)
            self.jobMarketMap.append(townJobProb)
       
    def jobMarket(self):
        
        activePop = [x for x in self.pop.livingPeople if x.status == 'employed' or x.status == 'unemployed']
        
        for person in activePop:
            person.searchJob = True
            person.jobChange = False
            person.jobOffer = False
            person.newTown = None
            self.updateWork(person)
        
        numActivePop = float(len(activePop))
        classShares = []
        
        for c in range(self.p['numberClasses']):
            count = 0.0
            for x in activePop:
                if x.classRank == c:
                    count += 1.0
            classShares.append(count/numActivePop)
        
        
        unemployment = self.unemployment_series[(self.year-self.p['startYear'])]
        
        totalUnemploymentRate = 0
        
        employedPeople = 0
        totPop = 0
        
        for c in range(self.p['numberClasses']):
            
            classPop = [x for x in activePop if x.classRank == c]
            numclassPop = float(len(classPop))
            ageBandShares = []
            for b in range(self.p['numberAgeBands']):
                count = 0.0
                for x in classPop:
                    if self.ageBand(x.age) == b:
                        count += 1.0
                ageBandShares.append(count/numclassPop)
            
            for a in range(self.p['numberAgeBands']):
               
                pop = []
                for x in activePop:
                    if x.classRank == c and self.ageBand(x.age) == a:
                        pop.append(x)
                
                sharePop = float(len(pop))/float(len(activePop))
                
                if len(pop) > 0:
                
                    unemploymentRate = self.unemploymentRate(classShares, ageBandShares, self.p['unemploymentClassBias'], 
                                                         self.p['unemploymentAgeBias'], unemployment, a, c)
                    
                    jobMobilityRate = (self.p['jobMobilitySlope']/unemploymentRate + self.p['jobMobilityIntercept'])*self.p['ageBiasParam'][a]
                    
                    if jobMobilityRate > 0.85:
                        jobMobilityRate = 0.85

                    employed = [x for x in pop if x.status == 'employed']

                    jobChanges = int(float(len(employed))*jobMobilityRate)
                    
                    changeWeights = []
                    if len(employed) > 0:
                        for person in employed:
                            householdStatusQuo = self.statusQuo(person)
                            relocationCost = self.computeRelocationsCost(person)
                            propensityToRelocate = self.relocationPropensity(relocationCost, person)
                            probTowns = self.townsProb(person.classRank, propensityToRelocate)
                            # Job opportunity location is sampled
                            if person.partner == None or person.partner not in activePop or person.partner.searchJob == True:
                                town = np.random.choice(self.map.towns, p = probTowns)
                            else:
                                town = person.partner.newTown
                            person.newTown = town
                            townIndex = self.map.towns.index(town)
                            relocationCareGain = relocationCost[townIndex]
                            townIndex = self.map.towns.index(person.house.town)
                            relocationCareLoss = relocationCost[townIndex]
                            relocationNetLoss = relocationCareLoss - relocationCareGain
                            # Job opportunity income is sampled
                            dK = abs(np.random.normal(0, self.p['wageVar']))
                            person.newK = self.p['incomeFinalLevels'][person.classRank]*math.exp(dK)
                            person.newWage = self.computeWage(person, person.newK)
                            newHouseholdIncome = person.newWage*self.p['weeklyHours']
                            
                            if person.partner != None and person.partner in activePop:
                                if town != person.partner.house.town or person.partner.status == 'unemployed':
                                    newHouseholdIncome += self.expectedIncome(person.partner, town) 
                                elif town == person.house.town and person.partner.status == 'employed':
                                    newHouseholdIncome += person.partner.income
                                    
                            deltaIncome = newHouseholdIncome - householdStatusQuo
                            deltaIncomeFactor = math.exp(self.p['deltaIncomeExp']*deltaIncome)
                            careLossFactor = 1/math.exp(self.p['relocationCareLossExp']*relocationNetLoss)
                            changeWeight = deltaIncomeFactor*careLossFactor
                            changeWeights.append(changeWeight)
                            person.searchJob = False
                        changeProbs = [i/sum(changeWeights) for i in changeWeights]
                        peopleToChange = np.random.choice(employed, jobChanges, replace = False, p = changeProbs)
                        for person in peopleToChange:
                            self.changeJob(person)
                            if person.partner != None and person.partner.status == 'employed' and person.newTown != person.partner.house.town:
                                self.leaveJob(person.partner)
                                    
        activePop = [x for x in self.pop.livingPeople if x.status == 'employed' or x.status == 'unemployed']
                                    
        for c in range(self.p['numberClasses']):
            
            classPop = [x for x in activePop if x.classRank == c]
            numclassPop = float(len(classPop))
            ageBandShares = []
            for b in range(self.p['numberAgeBands']):
                count = 0.0
                for x in classPop:
                    if self.ageBand(x.age) == b:
                        count += 1.0
                ageBandShares.append(count/numclassPop)
            
            for a in range(self.p['numberAgeBands']):
               
                pop = []
                for x in activePop:
                    if x.classRank == c and self.ageBand(x.age) == a:
                        pop.append(x)
                
                sharePop = float(len(pop))/float(len(activePop))
                
                if len(pop) > 0:
               
                    unemploymentRate = self.unemploymentRate(classShares, ageBandShares, self.p['unemploymentClassBias'], 
                                                         self.p['unemploymentAgeBias'], unemployment, a, c)

                    targetEmployed = int(float(len(pop))*(1.0-unemploymentRate) + 0.5)
                 
                    actualEmployed = len([x for x in pop if x.status == 'employed'])
                  
                    if targetEmployed > actualEmployed:
                       
                        peopleToHire = targetEmployed - actualEmployed 
                        
                        unemployed = [x for x in pop if x.status == 'unemployed']
                       
                        for person in unemployed:
                            relocationCost = self.computeRelocationsCost(person)
                            propensityToRelocate = self.relocationPropensity(relocationCost, person)
                            probTowns = self.townsProb(person.classRank, propensityToRelocate)
                            # Job opportunity location is sampled
                            town = np.random.choice(self.map.towns, p = probTowns)
                            if person.partner != None:
                                if person.partner.status == 'employed':
                                    town = person.partner.jobLocation
                                if person.partner in unemployed and person.partner.newTown != None:
                                    town = person.partner.newTown
                            person.newTown = town
                            # Job opportunity income is sampled
                            dK = np.random.normal(0, self.p['wageVar'])
                            person.newK = self.p['incomeFinalLevels'][person.classRank]*math.exp(dK)
                            person.newWage = self.computeWage(person, person.newK)
                        peopleToHire = np.random.choice(unemployed, peopleToHire, replace = False)
                        for person in peopleToHire:
                            self.changeJob(person)
  
                    else:
                        peopleToFire = actualEmployed - targetEmployed
                        while peopleToFire > 0:
                            peopleAtRisk = [x for x in pop if x.status == 'employed' and x.jobTenure > 0]
                            tenures = [1/math.exp(self.p['firingParam']*x.jobTenure) for x in peopleAtRisk]
                            sumTenures = sum(tenures)
                            probFired = [i/sumTenures for i in tenures]
                            person = np.random.choice(peopleAtRisk, p = probFired)
                            self.leaveJob(person)
                            peopleToFire -= 1
                            
                        actualEmployed = len([x for x in pop if x.status == 'employed'])
                        # print('Unemployment rate (target): ' + str(unemploymentRate))
                        actualUnemploymentRate = 1.0-float(actualEmployed)/float(len(pop))
                        # print('Unemployment rate (actual): ' + str(actualUnemploymentRate))
                        employedPeople += actualEmployed
                        totPop += len(pop)
                        totalUnemploymentRate += actualUnemploymentRate*sharePop
        
    def expectedIncome(self, person, town):
        marketWage = self.marketWage(person)
        income = marketWage*self.p['weeklyHours']
        townIndex = self.map.towns.index(town)
        townJobDensity = self.jobMarketMap[person.classRank][townIndex]
        townFactor = math.exp(self.p['incomeDiscountingExponent']*(townJobDensity + self.p['incomeDiscountingParam']))
        discountingFactor = 1 - person.unemploymentRate/townFactor
        expIncome = income*discountingFactor
        return (expIncome)
        
    def statusQuo(self, agent):
        ehi = 0
        if agent.status == 'employed':
            ehi = agent.income
        else:
            ehi = self.expectedIncome(agent, agent.house.town)
        if agent.partner != None:
            if agent.partner.status == 'employed':
                ehi += agent.partner.income
            elif agent.partner.status == 'unemployed':
                ehi += self.expectedIncome(agent.partner, agent.partner.house.town)
        return (ehi)    
    
    def unemploymentRate(self, classShares, ageBandShares, classBias, ageBias, u, ageBand, classRank):
        a = 0
        for i in range(self.p['numberClasses']):
            a += classShares[i]*math.pow(classBias, i)
        lowClassRate = u/a
        classRate = lowClassRate*math.pow(classBias, classRank)
        a = 0
        for i in range(self.p['numberAgeBands']):
            a += ageBandShares[i]*ageBias[i]
        lowerAgeBandRate = classRate/a
        unemploymentRate = lowerAgeBandRate*ageBias[ageBand]
        return (unemploymentRate)
    
    def computeRelocationsCostSpouses(self, agent):
        rcA = math.pow(float(agent.yearsInTown), self.p['yearsInTownSensitivityParam'])
        children = [x for x in agent.children if x.dead == False and x.house == agent.house]
        for child in children:
            rcA += math.pow(float(child.yearsInTown), self.p['yearsInTownSensitivityParam'])
        rcA *= self.p['relocationCostParam']
        
        socialAttractions = []
        index = 0
        for town in self.map.towns:
            if town == agent.house.town:
                socialAttraction = agent.socialCareMap[index]
            else:
                socialAttraction = agent.socialCareMap[index] - rcA
            attractionFactor = math.exp(self.p['propensityRelocationParam']*socialAttraction)
            relativeAttraction = attractionFactor/(attractionFactor + 1)    
            socialAttractions.append(relativeAttraction)
            index += 1
        return (socialAttractions)
    
    def computeRelocationsCost(self, agent):
        rcA = math.pow(float(agent.yearsInTown), self.p['yearsInTownSensitivityParam'])
        if agent.partner == None:
            children = [x for x in agent.children if x.dead == False and x.house == agent.house]
            for child in children:
                rcA += math.pow(float(child.yearsInTown), self.p['yearsInTownSensitivityParam'])
        else:
            rcA += math.pow(float(agent.partner.yearsInTown), self.p['yearsInTownSensitivityParam'])
            childrenAgent = [x for x in agent.children if x.dead == False and x.house == agent.house]
            childrenPartner = [x for x in agent.partner.children if x.dead == False and x.house == agent.partner.house]
            children = list(set(childrenAgent+childrenPartner))
            for child in children:
                rcA += math.pow(float(child.yearsInTown), self.p['yearsInTownSensitivityParam'])
        rcA *= self.p['relocationCostParam']

        townAttractions = []
        index = 0
        for town in self.map.towns:
            if town == agent.house.town:
                townAttraction = agent.socialCareMap[index]
            else:
                townAttraction = agent.socialCareMap[index] - rcA
            townAttractions.append(townAttraction)
            index += 1
        return (townAttractions)
        
    def relocationPropensity(self, relocationCost, agent):  
        potentialIncome = 0
        for member in agent.house.occupants:
            if member.status == 'employed' or member.status == 'retired':
                potentialIncome += member.income
            elif member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, member.house.town)
        perCapitaIncome = potentialIncome/float(len(agent.house.occupants))
        
        propensities = []
        index = 0
        for town in self.map.towns:
            relativeAttraction = relocationCost[index]/perCapitaIncome
            attractionFactor = math.exp(self.p['propensityRelocationParam']*relativeAttraction)
            rp = attractionFactor/(attractionFactor + 1.0)
            propensities.append(rp)
            index += 1
        return(propensities)
    
    def changeJob(self, a):
        if a.status == 'unemployed':
            self.enterWork += 1
        if a.status == 'employed':
            a.jobChange = True
        a.status = 'employed'
        a.wage = a.newWage
        a.income = a.wage*self.p['weeklyHours']
        a.finalIncome = a.newK
        a.jobLocation = a.newTown
        a.jobTenure = 0
        a.searchJob = False
        if a.independentStatus == False:
            self.findNewHouse([a], a.newTown)
            a.independentStatus = True
                    
    def leaveJob(self, person):
            self.exitWork += 1
            person.status = 'unemployed'
            person.wage = self.marketWage(person)
            person.income = 0
            person.finalIncome = 0
            person.jobTenure = 0
            person.jobLocation = None
            person.searchJob = True
    
    def computeWage(self, agent, k):
        # Gompertz Law
        c = np.log(self.p['incomeInitialLevels'][agent.classRank]/k)
        exp = c*math.exp(-1*self.p['incomeGrowthRate'][agent.classRank]*agent.workingTime)
        wage = k*math.exp(exp)
        return (wage)
        
    def baseRate(self, socialClassShares, bias, cp):
        a = 0
        for i in range(self.p['numberClasses']):
            a += socialClassShares[i]*math.pow(bias, i)
        baseRate = cp/a
        return (baseRate)
    
    def townsProb(self, classRank, relocPropensity):
        townDensity = []
        index = 0
        for t in self.map.towns:
            townSocialAttraction = relocPropensity[index]
            townDensity.append(self.jobMarketMap[classRank][index]*townSocialAttraction)
            index += 1
        sumDensity = sum(townDensity)
        relTownDensity = [i/sumDensity for i in townDensity]
        return(relTownDensity)            
            
    def updateWork(self, person):
        person.workingTime *= self.p['workDiscountingTime']
        workTime = 0
        if person.status == 'employed':
            person.jobTenure += 1
            workingHours = float(max(self.p['weeklyHours'] - person.socialWork, 0))
            workTime = workingHours/float(self.p['weeklyHours'])
        person.workingTime += workTime
        if person.status == 'employed':
            k = person.finalIncome
        else:
            k = self.p['incomeFinalLevels'][person.classRank]
        r = self.p['incomeGrowthRate'][person.classRank]
        c = np.log(self.p['incomeInitialLevels'][person.classRank]/k)
        exp = c*math.exp(-1*r*person.workingTime)
        person.wage = k*math.exp(exp)
        if person.status == 'employed':
            person.income = person.wage*self.p['weeklyHours']
        else:
            person.income = 0
            
      
    def movingAround(self):
    
        #print('Job Relocation')
        self.jobRelocation()
        
       # print('Join Spouses')
        # self.joiningSpouses()
        
        #print('Size Relocation')
        self.sizeRelocation()
        
        #print('Retired Relocation')
        self.relocatingPensioners()
        
        for i in self.pop.livingPeople:
            i.movedThisYear = False
            i.yearsInTown += 1.0
        
    def jobRelocation(self):
        employedPop = [x for x in self.pop.livingPeople if x.status == 'employed']
        for person in employedPop:
            peopleToMove = []
            if person.movedThisYear == True:
                continue
            if person.house.town != person.jobLocation:
                person.movedThisYear = True
                if person.independentStatus == False:
                    person.independentStatus = True
                peopleToMove.append(person)
                if person.partner != None:
                    person.partner.movedThisYear = True
                    if person.partner.independentStatus == False:
                        person.partner.independentStatus = True
                    peopleToMove.append(person.partner)
                    if person.house != person.partner.house:
                        peopleToMove += self.bringTheKids(person)
                        
                        for i in peopleToMove:        
                            repetitions = peopleToMove.count(i)
                            if repetitions > 1:
                                print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in jobRelocation (1)')
                        
                    else:
                        peopleToMove += self.childrenInHouse(person)
                        
                        for i in peopleToMove:        
                            repetitions = peopleToMove.count(i)
                            if repetitions > 1:
                                print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in jobRelocation (2)')
                        
                else:
                    
                    
                    
                    peopleToMove += self.kidsWithPerson(person)
                    
                    for i in peopleToMove:        
                        repetitions = peopleToMove.count(i)
                        if repetitions > 1:
                            print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in jobRelocation (3)')
                    
            if person.jobLocation == None:
                print('Job relocation town is None')
            if len(peopleToMove) > 0:
                
                for i in peopleToMove:        
                    repetitions = peopleToMove.count(i)
                    if repetitions > 1:
                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in jobRelocation')
                
                for member in peopleToMove:
                    if member not in member.house.occupants:
                        print('ERROR: ' + str(member.id) + ' not among his house occupants in job Relocation!')
                        print(member.dead)
                        
                self.totalRelocations += 1 
                self.jobRelocations += 1 
                
                
                self.findNewHouse(peopleToMove, person.jobLocation)
                
                
    
    def joiningSpouses(self):
        
        for person in self.pop.livingPeople:
            
            # ageClass = person.age / 10       
            if person.partner != None and person.house != person.partner.house:

                #person.movedThisYear = True
                #person.partner.movedThisYear = True
                
                relocationCost = self.computeRelocationsCostSpouses(person)
                personTownIndex = self.map.towns.index(person.house.town)
                personTownAttraction = relocationCost[personTownIndex]
                relocationCost = self.computeRelocationsCostSpouses(person.partner)
                partnerTownIndex = self.map.towns.index(person.partner.house.town)
                partnerTownAttraction = relocationCost[partnerTownIndex]
                
                # 1st case: both partners living with parents.
                # Find a new home near the highest earning partner
                if person.independentStatus + person.partner.independentStatus == 0:
                    print('Warning: they should not be married')
                    # person.independentStatus = True
                    # person.partner.independentStatus = True
                    if person.income*personTownAttraction > person.partner.income*partnerTownAttraction:
                        peopleToMove = [person, person.partner]
                        destination = person.house.town
                        if ( person.house.town != person.partner.house.town and person.partner.status == 'employed'):
                            self.leaveJob(person.partner)
                    else:
                        peopleToMove = [person.partner, person]
                        destination = person.partner.house.town
                        if ( person.house.town != person.partner.house.town and person.status == 'employed'):
                            self.leaveJob(person)
                    peopleToMove += self.bringTheKids(person)
                    
                    for i in peopleToMove:     
                        repetitions = peopleToMove.count(i)
                        if repetitions > 1:
                            print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (1)')
                            
                    self.totalRelocations += 1
                    self.marriageRelocations += 1
                    person.independentStatus = True
                    person.partner.independentStatus = True
                    self.findNewHouse(peopleToMove, destination)
                    continue
                
                # 2nd case: one living alone and the other living with parents
                # If in the same town: move in the house of independent partner
                # If in different towns: move in the house of independent partner
                #                        if higher income, otherwise find new house
                #                        near other partner.
                
                
                if ( person.independentStatus + person.partner.independentStatus == 1):
                    
                    if ( person.independentStatus == True and person.partner.independentStatus == False):
                        
                        # person.partner.independentStatus = True
                        a = person
                        aTownCare = personTownAttraction
                        b = person.partner
                        bTownCare = partnerTownAttraction
                    else:
                        # person.independentStatus = True
                        a = person.partner
                        aTownCare = partnerTownAttraction
                        b = person
                        bTownCare = personTownAttraction
                        
                    childrenWithPartner = self.kidsWithPartner(a)
                    childrenWithPerson = self.kidsWithPerson(a)
                    
                    if ( a.house.town == b.house.town ):
                        newOcc = 1 + len(childrenWithPartner)
                        oldOcc = len(a.house.occupants)
                        pReloc = self.relocationProb(newOcc, oldOcc, a.house.initialOccupants)
                        r = random.random()
                        if ( r > pReloc ):
                            targetHouse = a.house
                            peopleToMove = [b]
                            peopleToMove += self.kidsWithPartner(a)
                            if targetHouse == b.house:
                                print('Target house equal to departure house in 1')
                                
                            for i in peopleToMove:
                                if i in targetHouse.occupants:
                                    print('Error in Join Spouses 1')
                                    print(peopleToMove.index(i))
                                    
                            for i in peopleToMove:     
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 1')
                                
                            self.totalRelocations += 1
                            self.marriageRelocations += 1
                            b.independentStatus = True
                            self.movePeopleIntoChosenHouse(targetHouse, b.house, peopleToMove)
                            continue
                        
                        else:
                            destination = a.house.town
                            peopleToMove = [a, b]
                            peopleToMove += self.bringTheKids(a)
                            
                            for i in peopleToMove:     
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (2)')
                            self.totalRelocations += 1
                            self.marriageRelocations += 1
                            b.independentStatus = True
                            self.findNewHouse(peopleToMove, destination)
                            continue
                    else:
                        if a.income*aTownCare > b.income*bTownCare:
                            newOcc = 1 + len(childrenWithPartner)
                            oldOcc = len(a.house.occupants)
                            pReloc = self.relocationProb(newOcc, oldOcc, a.house.initialOccupants)
                            r = random.random()
                            if ( r > pReloc ):
                                targetHouse = a.house
                                peopleToMove = [b]
                                if b.status == 'employed':
                                    self.leaveJob(b)
                                peopleToMove += self.kidsWithPartner(a)
                                if targetHouse == b.house:
                                    print('Target house equal to departure house in 2')
                                    
                                for i in peopleToMove:
                                    if i in targetHouse.occupants:
                                        print('Error in Join Spouses 2')
                                        print(peopleToMove.index(i))
                                        
                                for i in peopleToMove:    
                                    repetitions = peopleToMove.count(i)
                                    if repetitions > 1:
                                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 2')    
                                        
                                self.totalRelocations += 1
                                self.marriageRelocations += 1   
                                b.independentStatus = True
                                self.movePeopleIntoChosenHouse(targetHouse, b.house, peopleToMove)
                                continue   
                            else:
                                destination = a.house.town
                                peopleToMove = [a, b]
                                if b.status == 'employed':
                                    self.leaveJob(b)
                                peopleToMove += self.bringTheKids(a)
                                
                                for i in peopleToMove:   
                                    repetitions = peopleToMove.count(i)
                                    if repetitions > 1:
                                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (3)')
                                
                                self.totalRelocations += 1
                                self.marriageRelocations += 1
                                b.independentStatus = True
                                self.findNewHouse(peopleToMove, destination)
                                continue
                        else:
                            destination = b.house.town
                            peopleToMove = [b, a]
                            if a.status == 'employed':
                                self.leaveJob(a)
                            peopleToMove += self.bringTheKids(a)
                            
                            for i in peopleToMove:  
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (4)')
                            
                            self.totalRelocations += 1
                            self.marriageRelocations += 1
                            b.independentStatus = True
                            self.findNewHouse(peopleToMove, destination)
                            continue
                        
                # 3rd case: both living alone
                
                if ( person.independentStatus + person.partner.independentStatus == 2):
                    
                    childrenWithPartner = self.kidsWithPartner(person)
                    childrenWithPerson = self.kidsWithPerson(person)
                    
                    newOcc1 = 1 + len(childrenWithPartner)
                    oldOcc1 = len(person.house.occupants)
                    totOcc1 = float(newOcc1 + oldOcc1)
                    ratio1 = totOcc1/float(person.house.initialOccupants)
                    newOcc2 = 1 + len(childrenWithPerson)
                    oldOcc2 = len(person.partner.house.occupants)
                    totOcc2 = float(newOcc2 + oldOcc2)
                    ratio2 = totOcc2/float(person.partner.house.initialOccupants)
                    # If in the same town: move into bigger house
                    if ( person.house.town == person.partner.house.town ):
                        if ( ratio1 < ratio2 ):
                            a = person
                            b = person.partner
                            newOcc = newOcc1
                        else:
                            b = person
                            a = person.partner
                            newOcc = newOcc2
                        oldOcc = len(a.house.occupants)
                        pReloc = self.relocationProb(newOcc, oldOcc, a.house.initialOccupants)
                        r = random.random()
                        if ( r > pReloc ):
                                targetHouse = a.house
                                peopleToMove = [b]
                                peopleToMove += self.kidsWithPartner(a)
                                
                                for i in peopleToMove:
                                    if i in targetHouse.occupants:
                                        print('Error in Join Spouses 3')
                                        print(peopleToMove.index(i))
                                        
                                for i in peopleToMove:   
                                    repetitions = peopleToMove.count(i)
                                    if repetitions > 1:
                                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 3')        
                                
                                self.totalRelocations += 1
                                self.marriageRelocations += 1
                                
                                self.movePeopleIntoChosenHouse(targetHouse, b.house, peopleToMove)
                                continue    
                        else:
                                peopleToMove = [a, b]
                                peopleToMove += self.bringTheKids(a)
                                
                                for i in peopleToMove:        
                                    repetitions = peopleToMove.count(i)
                                    if repetitions > 1:
                                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (5)')
                                
                                self.totalRelocations += 1
                                self.marriageRelocations += 1
                                
                                self.findNewHouse(peopleToMove, a.house.town)
                                continue
                    # If different town: move into house of higher income partner
                    else:
                        personIncome = person.income
                        if person.income == 0:
                            personIncome = self.expectedIncome(person, person.house.town)
                        partnerIncome = person.partner.income
                        if person.partner.income == 0:
                            partnerIncome = self.expectedIncome(person.partner, person.partner.house.town)
                        if personIncome*personTownAttraction > partnerIncome*partnerTownAttraction:
                            a = person
                            b = person.partner
                            newOcc = newOcc1
                        else:
                            a = person.partner
                            b = person
                            newOcc = newOcc2
                        oldOcc = len(a.house.occupants)
                        pReloc = self.relocationProb(newOcc, oldOcc, a.house.initialOccupants)
                        r = random.random()
                        if ( r > pReloc ):
                            targetHouse = a.house
                            peopleToMove = [b]
                            if b.status == 'employed':
                                self.leaveJob(b)
                            peopleToMove += self.kidsWithPartner(a)
                            if targetHouse == b.house:
                                print('Target house equal to departure house in 4')
                            
                            for i in peopleToMove:
                                if i in targetHouse.occupants:
                                    print('Error in Join Spouses 4')
                                    print(peopleToMove.index(i))
                                    
                            for i in peopleToMove:        
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 4')      
                             
                            self.totalRelocations += 1
                            self.marriageRelocations += 1
                            
                            self.movePeopleIntoChosenHouse(targetHouse, b.house, peopleToMove)
                            continue        
                        else:
                            peopleToMove = [a, b]
                            if b.status == 'employed':
                                self.leaveJob(b)
                            peopleToMove += self.bringTheKids(a)
                            
                            for i in peopleToMove:        
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (6)')
                        
                            self.totalRelocations += 1
                            self.marriageRelocations += 1
                    
                            self.findNewHouse(peopleToMove, a.house.town)
                            continue
                
                
        for person in self.pop.livingPeople:
            person.justMarried = None
            
    def sizeRelocation(self):
        for person in self.pop.livingPeople:
            if person.movedThisYear or person.independentStatus == False:
                continue
            actualOccupants = len(person.house.occupants)
            pReloc = self.relocationProb(actualOccupants, 0, person.house.initialOccupants)
            if random.random() < pReloc:
                person.movedThisYear = True
                peopleToMove = [person]
                
                if person.partner == None: 
                    
                    peopleToMove += self.kidsWithPerson(person)
                    
                    for i in peopleToMove:        
                        repetitions = peopleToMove.count(i)
                        if repetitions > 1:
                            print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in sizeRelocation (1)')
                                
                else:
                    person.partner.movedThisYear = True
                    peopleToMove.append(person.partner)
                    if person.house != person.partner.house:
                        peopleToMove += self.bringTheKids(person)
                        
                        for i in peopleToMove:        
                            repetitions = peopleToMove.count(i)
                            if repetitions > 1:
                                print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in sizeRelocation (2)')
                        
                    else:
                        peopleToMove += self.childrenInHouse(person)
                        
                        for i in peopleToMove:        
                            repetitions = peopleToMove.count(i)
                            if repetitions > 1:
                                print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in sizeRelocation (3)')
                            
                if person.house.town == None:
                    print('Size relocation town is None')  
                    
                for i in peopleToMove:        
                    repetitions = peopleToMove.count(i)
                    if repetitions > 1:
                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in sizeReloc')
                
                for member in peopleToMove:
                    if member not in member.house.occupants:
                        print('ERROR: ' + str(member.id) + ' not among his house occupants in size Relocation!')
                        print(member.dead)
                
                self.totalRelocations += 1
                self.sizeRelocations += 1
                
                self.findNewHouse(peopleToMove, person.house.town)
                
    def relocatingPensioners(self):
        for person in self.pop.livingPeople:
            if ( person.status == 'retired' and len(person.house.occupants) == 1 ):
                ## a retired person who lives alone
                for c in person.children:
                    if ( c.dead == False and c.independentStatus == True ):
                        distance = self.manhattanDistance(person.house.town, c.house.town)
                        distance += 1.0
                        if self.year < self.p['thePresent']:
                            mbRate = self.p['agingParentsMoveInWithKids'] / distance
                        else:
                            mbRate = self.p['variableMoveBack'] / distance
                        if random.random() < mbRate:
                            peopleToMove = [person]
                            if person.house == self.displayHouse:
                                messageString = str(self.year) + ": #" + str(person.id) + " is going to live with one of their children."
                                self.textUpdateList.append(messageString)
                                
                            for i in peopleToMove:
                                if i in c.house.occupants:
                                    print('Retired already in child house!')
                                    
                            for i in peopleToMove:        
                                repetitions = peopleToMove.count(i)
                                if repetitions > 1:
                                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in relocatingPensioners')
                            
                            self.totalRelocations += 1
                            self.retiredRelocations += 1
                            
                            self.movePeopleIntoChosenHouse(c.house, person.house, peopleToMove)
                            
                            
                                    
                            break
            
    def findNewHouse(self, personList, town):
        # Find a new house with a 'good' neighborhood, in the chosen town

        newHouse = None
        person = personList[0]
        departureHouse = person.house
        probHouses = self.houseProb(town, person.classRank)
        # print(sum(probHouses))
        newHouse = np.random.choice(town.houses, p = probHouses)
        
        if person.house.town != newHouse.town:
            self.townChanges += 1
        
        if len(newHouse.occupants) >  0:
            print('Moved in an occupied house!')
            
        if ( newHouse == person.house):
            print('Error: new house selected is departure house')    
            
        if newHouse == None:
            print "No houses left for person of SEC " + str(person.sec)
            sys.exit()
        # Actually make the chosen move
        for i in personList:
            if i in newHouse.occupants:
                print('New house not empty!')
                
        self.movePeopleIntoChosenHouse(newHouse, departureHouse, personList)
        
    def houseProb(self, town, classRank):
        numberHouses = len(town.houses)
        numberOccupiedHouses = len([x for x in town.houses if len(x.occupants) > 0])
        if numberHouses == numberOccupiedHouses:
            print('Attention: no more available houses in the town')
            print('Town ' + str(town.x) + ', ' + str(town.y) + ' has ' + str(numberHouses) + ' houses.')
        socialDesirability = []
        probHouses = []
        denProb = 0.0
        for h in town.houses:
            count = 0.0
            if len(h.occupants) > 0:
                socialDesirability.append(0.0)
                continue
            for x in town.houses:
                if len(x.occupants) == 0:
                    continue
                if x.occupants[0].classRank == classRank:
                    count += 1/math.pow(self.manhattanDistance(h, x), self.p['geoDistanceSensitivityParam'])
                else:
                    socialDistance = math.pow(abs(x.occupants[0].classRank-classRank), self.p['socDistanceSensitivityParam'])
                    count -= socialDistance/math.pow(self.manhattanDistance(h, x), self.p['geoDistanceSensitivityParam'])
                # Softmax function
            socialDesirability.append(math.exp(self.p['distanceSensitivityParam']*count))
        denProb = sum(socialDesirability)
        if sum(socialDesirability) == 0:
            print sum(socialDesirability)
        probHouses = [i/denProb for i in socialDesirability]
        return (probHouses)    
        
    def movePeopleIntoChosenHouse(self, newHouse, departureHouse, personList):
        
        if len(newHouse.occupants) ==  0:
            newHouse.initialOccupants = len(personList)
        
        if ( newHouse == departureHouse):
            print('Error: new house is departure house')
            
        for i in personList:
            oldHouse = i.house
            
            repetitions = personList.count(i)
            if repetitions > 1:
               print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times!')
             
            if i in newHouse.occupants:
               print('Person ' + str(i.id) + ' already in new house!')
               
            if oldHouse.town != newHouse.town:
                i.yearsInTown = 0
                
            oldHouse.occupants.remove(i)
            
            if len(oldHouse.occupants) ==  0:
                oldHouse.initialOccupants = 0
                self.map.occupiedHouses.remove(oldHouse)
                ##print "This house is now empty: ", oldHouse
                if (self.p['interactiveGraphics']):
                    self.canvas.itemconfig(oldHouse.icon, state='hidden')
            newHouse.occupants.append(i)
            i.house = newHouse
            i.movedThisYear = True
        
        if ( newHouse not in self.map.occupiedHouses):
            self.map.occupiedHouses.append(newHouse)
            
        if (self.p['interactiveGraphics']):
            self.canvas.itemconfig(newHouse.icon, state='normal')
            
        ## Check whether we've moved into the display house
        if newHouse == self.displayHouse:
            self.textUpdateList.append(str(self.year) + ": New people are moving into " + newHouse.name)
            messageString = ""
            for k in personList:
                messageString += "#" + str(k.id) + " "
            self.textUpdateList.append(messageString)
            
        if departureHouse == self.displayHouse:
            self.nextDisplayHouse = newHouse

    
    
    def householdSize(self):
        visitedHouses = []
        maxSize = 0
        numberOccupants = 0
        for person in self.pop.livingPeople:
            if person.house not in visitedHouses:
                visitedHouses.append(person.house)
                numberOccupants += len(person.house.occupants)
                if len(person.house.occupants) > maxSize:
                    maxSize = len(person.house.occupants)
        print('The most numerous household has a size of ' + str(maxSize))
        
    def doStats(self):
        
        # Year
        self.times.append(self.year)
        
        # Population stats
        currentPop = len(self.pop.livingPeople)
        self.pops.append(currentPop)
        unskilled = [x for x in self.pop.livingPeople if x.classRank == 0]
        self.unskilledPop.append(len(unskilled))
        skilled = [x for x in self.pop.livingPeople if x.classRank == 1]
        self.skilledPop.append(len(skilled))
        lowerclass = [x for x in self.pop.livingPeople if x.classRank == 2]
        self.lowerclassPop.append(len(lowerclass))
        middelclass = [x for x in self.pop.livingPeople if x.classRank == 3]
        self.middleclassPop.append(len(middelclass))
        upperclass = [x for x in self.pop.livingPeople if x.classRank == 4]
        self.upperclassPop.append(len(upperclass))
        
        tally_1to2 = 0
        tally_1to3 = 0
        tally_1to4 = 0
        tally_1to5 = 0
        tally_2to1 = 0
        tally_2to3 = 0
        tally_2to4 = 0
        tally_2to5 = 0
        tally_3to1 = 0
        tally_3to2 = 0
        tally_3to4 = 0
        tally_3to5 = 0
        tally_4to1 = 0
        tally_4to2 = 0
        tally_4to3 = 0
        tally_4to5 = 0
        tally_5to1 = 0
        tally_5to2 = 0
        tally_5to3 = 0
        tally_5to4 = 0
        
        workingPop = [x for x in self.pop.livingPeople if x.age == 24]
        for person in workingPop:
            if person.father != None:
                
                if person.classRank == 1 and person.father.classRank == 0:
                    tally_1to2 += 1
                if person.classRank == 2 and person.father.classRank == 0:
                    tally_1to3 += 1
                if person.classRank == 3 and person.father.classRank == 0:
                    tally_1to4 += 1
                if person.classRank == 4 and person.father.classRank == 0:
                    tally_1to5 += 1
                    
                if person.classRank == 0 and person.father.classRank == 1:
                    tally_2to1 += 1
                if person.classRank == 2 and person.father.classRank == 1:
                    tally_2to3 += 1
                if person.classRank == 3 and person.father.classRank == 1:
                    tally_2to4 += 1
                if person.classRank == 4 and person.father.classRank == 1:
                    tally_2to5 += 1
                    
                if person.classRank == 0 and person.father.classRank == 2:
                    tally_3to1 += 1
                if person.classRank == 1 and person.father.classRank == 2:
                    tally_3to2 += 1
                if person.classRank == 3 and person.father.classRank == 2:
                    tally_3to4 += 1 
                if person.classRank == 4 and person.father.classRank == 2:
                    tally_3to5 += 1
                    
                if person.classRank == 0 and person.father.classRank == 3:
                    tally_4to1 += 1
                if person.classRank == 1 and person.father.classRank == 3:
                    tally_4to2 += 1
                if person.classRank == 2 and person.father.classRank == 3:
                    tally_4to3 += 1
                if person.classRank == 4 and person.father.classRank == 3:
                    tally_4to5 += 1
                    
                if person.classRank == 0 and person.father.classRank == 4:
                    tally_5to1 += 1
                if person.classRank == 1 and person.father.classRank == 4:
                    tally_5to2 += 1
                if person.classRank == 2 and person.father.classRank == 4:
                    tally_5to3 += 1
                if person.classRank == 3 and person.father.classRank == 4:
                    tally_5to4 += 1
                    
        self.socialMobility_1to2.append(tally_1to2)
        self.socialMobility_1to3.append(tally_1to3)
        self.socialMobility_1to4.append(tally_1to4)
        self.socialMobility_1to5.append(tally_1to5)
        self.socialMobility_2to1.append(tally_2to1)
        self.socialMobility_2to3.append(tally_2to3)
        self.socialMobility_2to4.append(tally_2to4)
        self.socialMobility_2to5.append(tally_2to5)
        self.socialMobility_3to1.append(tally_3to1)
        self.socialMobility_3to2.append(tally_3to2)
        self.socialMobility_3to4.append(tally_3to4)
        self.socialMobility_3to5.append(tally_3to5)
        self.socialMobility_4to1.append(tally_4to1)
        self.socialMobility_4to2.append(tally_4to2)
        self.socialMobility_4to3.append(tally_4to3)
        self.socialMobility_4to5.append(tally_4to5)
        self.socialMobility_5to1.append(tally_5to1)
        self.socialMobility_5to2.append(tally_5to2)
        self.socialMobility_5to3.append(tally_5to3)
        self.socialMobility_5to4.append(tally_5to4)
        
        
        
        ## Check for double-included houses by converting to a set and back again
        pre_checkLength = len(self.map.occupiedHouses)
        self.map.occupiedHouses = list(set(self.map.occupiedHouses))
        post_checkLength = len(self.map.occupiedHouses)
        if pre_checkLength != post_checkLength:
            print('Warning: list of occupied houses contains double-counted houses')
        
        self.numberHouseholds.append(post_checkLength)
        
        h1 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 0]
        occupants_1 = 0.0
        for h in h1:
            occupants_1 += len(h.occupants)
        h2 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 1] 
        occupants_2 = 0.0
        for h in h2:
            occupants_2 += len(h.occupants)
        h3 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 2]
        occupants_3 = 0.0
        for h in h3:
            occupants_3 += len(h.occupants)
        h4 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 3]
        occupants_4 = 0.0
        for h in h4:
            occupants_4 += len(h.occupants)
        h5 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 4]
        occupants_5 = 0.0
        for h in h5:
            occupants_5 += len(h.occupants)
            
        self.numberHouseholds_1.append(len(h1))
        self.numberHouseholds_2.append(len(h2))
        self.numberHouseholds_3.append(len(h3))
        self.numberHouseholds_4.append(len(h4))
        self.numberHouseholds_5.append(len(h5))

        ## Check for overlooked empty houses
        emptyHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        for h in emptyHouses:
            self.map.occupiedHouses.remove(h)
            if (self.p['interactiveGraphics']):
                self.canvas.itemconfig(h.icon, state='hidden')
        
        ## Avg household size (easily calculated by pop / occupied houses)
        households = float(len(self.map.occupiedHouses))
        self.avgHouseholdSize.append(currentPop/households)

        self.avgHouseholdSize_1.append(occupants_1/float(len(h1)))
        self.avgHouseholdSize_2.append(occupants_2/float(len(h2)))
        self.avgHouseholdSize_3.append(occupants_3/float(len(h3)))
        self.avgHouseholdSize_4.append(occupants_4/float(len(h4)))
        self.avgHouseholdSize_5.append(occupants_5/float(len(h5)))
        
        ## Marriages and divorces
        self.numMarriages.append(self.marriageTally)
        
        # print('Marriages: ' + str(self.marriageTally))
        
        self.marriageTally = 0
        self.numDivorces.append(self.divorceTally)            
        self.divorceTally = 0
        
        
        ####### Social Care Outputs ################################################################
        
        
        ## Care demand calculations: first, what's the basic demand and theoretical supply?
        totalCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople])
        socialCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople if x.age > 15])
        childCareNeed = totalCareNeed - socialCareNeed
        informalCareSupply = sum([x.hoursInformalSupply for x in self.pop.livingPeople])
        formalCareSupply = sum([x.hoursFormalSupply for x in self.pop.livingPeople])
        totalCareSupply = informalCareSupply + formalCareSupply
        informalCareReceived = sum([x.informalCare for x in self.pop.livingPeople])
        formalCareReceived = sum([x.formalCare for x in self.pop.livingPeople])
        totalCareReceived = informalCareReceived + formalCareReceived
        informalSocialCareReceived = sum([x.informalCare for x in self.pop.livingPeople if x.age > 15])
        formalSocialCareReceived = sum([x.formalCare for x in self.pop.livingPeople if x.age > 15])
        socialCareReceived = informalSocialCareReceived + formalSocialCareReceived
        informalChildCareReceived = informalCareReceived - informalSocialCareReceived
        formalChildCareReceived = formalCareReceived - formalSocialCareReceived
        childCareReceived = informalChildCareReceived + formalChildCareReceived
        totalUnnmetCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
        totalUnmetSocialCareNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.age > 15])
        totalUnmetChildCareNeed = totalUnnmetCareNeed - totalUnmetSocialCareNeed
        totalInformalCareSupplied = sum([x.socialWork for x in self.pop.livingPeople])
        totalFormalCareSupplied = sum([x.workToCare for x in self.pop.livingPeople])
        totalCareSupplied = totalInformalCareSupplied + totalFormalCareSupplied
        
        totalInformalCareSuppliedMale = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male'])
        informalCareSuppliedMale_1 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 0])
        informalCareSuppliedMale_2 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 1])
        informalCareSuppliedMale_3 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 2])
        informalCareSuppliedMale_4 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 3])
        informalCareSuppliedMale_5 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 4])
        
        totalFormalCareSuppliedMale = sum([x.workToCare for x in self.pop.livingPeople if x.sex == 'male'])
        totalCareSuppliedMale = totalInformalCareSuppliedMale + totalFormalCareSuppliedMale
        totalInformalCareSuppliedFemale = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female'])
        informalCareSuppliedFemale_1 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 0])
        informalCareSuppliedFemale_2 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 1])
        informalCareSuppliedFemale_3 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 2])
        informalCareSuppliedFemale_4 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 3])
        informalCareSuppliedFemale_5 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 4])
        
        totalFormalCareSuppliedFemale = sum([x.workToCare for x in self.pop.livingPeople if x.sex == 'female'])
        totalCareSuppliedFemale = totalInformalCareSuppliedFemale + totalFormalCareSuppliedFemale
        
        self.totalCareDemand.append(totalCareNeed)
        self.totalSocialCareDemand.append(socialCareNeed)  # New!
        self.totalChildCareDemand.append(childCareNeed)
        self.totalCareSupply.append(totalCareSupply) # New!
        self.totalInformalCareSupply.append(informalCareSupply) # New!
        self.totalFormalCareSupply.append(formalCareSupply) # New!
        self.totalCareReceived.append(totalCareReceived) # New!
        self.totalSocialCareReceived.append(socialCareReceived) #New!
        self.totalChildCareReceived.append(childCareReceived) #New!
        self.totalInformalCareReceived.append(informalCareReceived)
        self.totalFormalCareReceived.append(formalCareReceived)
        self.totalInformalSocialCareReceived.append(informalSocialCareReceived)
        self.totalFormalSocialCareReceived.append(formalSocialCareReceived)
        self.totalInformalChildCareReceived.append(informalChildCareReceived)
        self.totalFormalChildCareReceived.append(formalChildCareReceived)
        self.totalUnmetDemand.append(totalUnnmetCareNeed)
        self.totalSocialCareUnmetDemand.append(totalUnmetSocialCareNeed) # New!
        self.totalChildCareUnmetDemand.append(totalUnmetChildCareNeed) # New!
        self.totalCareSuppliedMale.append(totalCareSuppliedMale) # New!
        self.totalInformalCareSuppliedMale.append(totalInformalCareSuppliedMale) # New!
        self.totalInformalCareSuppliedMale_1.append(informalCareSuppliedMale_1)
        self.totalInformalCareSuppliedMale_2.append(informalCareSuppliedMale_2)
        self.totalInformalCareSuppliedMale_3.append(informalCareSuppliedMale_3)
        self.totalInformalCareSuppliedMale_4.append(informalCareSuppliedMale_4)
        self.totalInformalCareSuppliedMale_5.append(informalCareSuppliedMale_5)
        self.totalFormalCareSuppliedMale.append(totalFormalCareSuppliedMale) # New!
        self.totalCareSuppliedFemale.append(totalCareSuppliedFemale) # New!
        self.totalInformalCareSuppliedFemale.append(totalInformalCareSuppliedFemale) # New!
        self.totalInformalCareSuppliedFemale_1.append(informalCareSuppliedFemale_1)
        self.totalInformalCareSuppliedFemale_2.append(informalCareSuppliedFemale_2)
        self.totalInformalCareSuppliedFemale_3.append(informalCareSuppliedFemale_3)
        self.totalInformalCareSuppliedFemale_4.append(informalCareSuppliedFemale_4)
        self.totalInformalCareSuppliedFemale_5.append(informalCareSuppliedFemale_5)
        self.totalFormalCareSuppliedFemale.append(totalCareSuppliedFemale) # New!
        
        class1 = [x for x in self.pop.livingPeople if x.classRank == 0]
        totalCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        for person in class1:
            if person.hoursDemand > 0:
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            else:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                numberOfCarers += 1
                
        self.totalCareDemand_1.append(totalCareDemandHours)
        self.totalCareSupply_1.append(totalInformalCareSupplyHours + totalFormalCareSupplyHours)   
        self.totalUnmetDemand_1.append(totalUnmetDemandHours) 
        self.totalInformalSupply_1.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_1.append(totalFormalCareSupplyHours)
        self.totalInformalCarePerRecipient_1.append(totalInformalCareSupplyHours/numberOfRecipients)
        self.totalFormalCarePerRecipient_1.append(totalFormalCareSupplyHours/numberOfRecipients)
        self.totalUnmetNeedPerRecipient_1.append(totalUnmetDemandHours/numberOfRecipients)
        self.totalInformalCarePerCarer_1.append(totalInformalCareSupplyHours/numberOfCarers)
        self.totalFormalCarePerCarer_1.append(totalFormalCareSupplyHours/numberOfCarers)
        
        class2 = [x for x in self.pop.livingPeople if x.classRank == 1]
        totalCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        for person in class2:
            if person.hoursDemand > 0:
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            else:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                numberOfCarers += 1
                
        self.totalCareDemand_2.append(totalCareDemandHours)
        self.totalCareSupply_2.append(totalInformalCareSupplyHours + totalFormalCareSupplyHours)   
        self.totalUnmetDemand_2.append(totalUnmetDemandHours) 
        self.totalInformalSupply_2.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_2.append(totalFormalCareSupplyHours)
        self.totalInformalCarePerRecipient_2.append(totalInformalCareSupplyHours/numberOfRecipients)
        self.totalFormalCarePerRecipient_2.append(totalFormalCareSupplyHours/numberOfRecipients)
        self.totalUnmetNeedPerRecipient_2.append(totalUnmetDemandHours/numberOfRecipients)
        self.totalInformalCarePerCarer_2.append(totalInformalCareSupplyHours/numberOfCarers)
        self.totalFormalCarePerCarer_2.append(totalFormalCareSupplyHours/numberOfCarers)
        
        class3 = [x for x in self.pop.livingPeople if x.classRank == 2]
        totalCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        for person in class3:
            if person.hoursDemand > 0:
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            else:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                numberOfCarers += 1
                
        self.totalCareDemand_3.append(totalCareDemandHours)
        self.totalCareSupply_3.append(totalInformalCareSupplyHours + totalFormalCareSupplyHours)   
        self.totalUnmetDemand_3.append(totalUnmetDemandHours) 
        self.totalInformalSupply_3.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_3.append(totalFormalCareSupplyHours)
        self.totalInformalCarePerRecipient_3.append(totalInformalCareSupplyHours/numberOfRecipients)
        self.totalFormalCarePerRecipient_3.append(totalFormalCareSupplyHours/numberOfRecipients)
        self.totalUnmetNeedPerRecipient_3.append(totalUnmetDemandHours/numberOfRecipients)
        self.totalInformalCarePerCarer_3.append(totalInformalCareSupplyHours/numberOfCarers)
        self.totalFormalCarePerCarer_3.append(totalFormalCareSupplyHours/numberOfCarers)
        
        class4 = [x for x in self.pop.livingPeople if x.classRank == 3]
        totalCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        for person in class4:
            if person.hoursDemand > 0:
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            else:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                numberOfCarers += 1
                
        self.totalCareDemand_4.append(totalCareDemandHours)
        self.totalCareSupply_4.append(totalInformalCareSupplyHours + totalFormalCareSupplyHours)   
        self.totalUnmetDemand_4.append(totalUnmetDemandHours) 
        self.totalInformalSupply_4.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_4.append(totalFormalCareSupplyHours)
        self.totalInformalCarePerRecipient_4.append(totalInformalCareSupplyHours/numberOfRecipients)
        self.totalFormalCarePerRecipient_4.append(totalFormalCareSupplyHours/numberOfRecipients)
        self.totalUnmetNeedPerRecipient_4.append(totalUnmetDemandHours/numberOfRecipients)
        self.totalInformalCarePerCarer_4.append(totalInformalCareSupplyHours/numberOfCarers)
        self.totalFormalCarePerCarer_4.append(totalFormalCareSupplyHours/numberOfCarers)
        
        class5 = [x for x in self.pop.livingPeople if x.classRank == 4]
        totalCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        for person in class5:
            if person.hoursDemand > 0:
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            else:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                numberOfCarers += 1
                
        self.totalCareDemand_5.append(totalCareDemandHours)
        self.totalCareSupply_5.append(totalInformalCareSupplyHours + totalFormalCareSupplyHours)   
        self.totalUnmetDemand_5.append(totalUnmetDemandHours) 
        self.totalInformalSupply_5.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_5.append(totalFormalCareSupplyHours)
        self.totalInformalCarePerRecipient_5.append(totalInformalCareSupplyHours/numberOfRecipients)
        self.totalFormalCarePerRecipient_5.append(totalFormalCareSupplyHours/numberOfRecipients)
        self.totalUnmetNeedPerRecipient_5.append(totalUnmetDemandHours/numberOfRecipients)
        self.totalInformalCarePerCarer_5.append(totalInformalCareSupplyHours/numberOfCarers)
        self.totalFormalCarePerCarer_5.append(totalFormalCareSupplyHours/numberOfCarers)
        
        taxPayers = len([x for x in self.pop.livingPeople if x.income > 0])
        self.numTaxpayers.append(taxPayers)
        
        sumNoK_informalSupplies = [0.0, 0.0, 0.0, 0.0]
        sumNoK_formalSupplies = [0.0, 0.0, 0.0, 0.0]
        receivers = [x for x in self.pop.livingPeople if x.hoursDemand > 0]
        for person in receivers:
            for i in range(4):
                sumNoK_informalSupplies[i] += person.informalSupplyByKinship[i]
                sumNoK_formalSupplies[i] += person.formalSupplyByKinship[i]
                
        self.totalInformalSupplyHousehold.append(sumNoK_informalSupplies[0])
        self.totalInformalSupplyNoK_1.append(sumNoK_informalSupplies[1])
        self.totalInformalSupplyNoK_2.append(sumNoK_informalSupplies[2])
        self.totalInformalSupplyNoK_3.append(sumNoK_informalSupplies[3])
        self.totalFormalSupplyHousehold.append(sumNoK_formalSupplies[0])
        self.totalFormalSupplyNoK_1.append(sumNoK_formalSupplies[1])
        self.totalFormalSupplyNoK_2.append(sumNoK_formalSupplies[2])
        self.totalFormalSupplyNoK_3.append(sumNoK_formalSupplies[3])
        self.totalSupplyHousehold.append(sumNoK_informalSupplies[0] + sumNoK_formalSupplies[0])
        self.totalSupplyNoK_1.append(sumNoK_informalSupplies[1] + sumNoK_formalSupplies[1])
        self.totalSupplyNoK_2.append(sumNoK_informalSupplies[2] + sumNoK_formalSupplies[2])
        self.totalSupplyNoK_3.append(sumNoK_informalSupplies[3] + sumNoK_formalSupplies[3])
        
        ####### Economic Outputs ################################################################
        
        activePop = [x for x in self.pop.livingPeople if x.status == 'employed' or x.status == 'unemployed']
        employed = [x for x in activePop if x.status == 'employed']
        unemployed = [x for x in activePop if x.status == 'unemployed']
        employmentRate = float(len(employed))/float(len(activePop))
        self.totalEmployment.append(employmentRate)
        # print('Employment rate: ' + str(employmentRate))
        
        employed_1 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 0]
        employed_1_Males = [x for x in employed_1 if x.sex == 'male']
        employed_1_Females = [x for x in employed_1 if x.sex == 'female']
        unemployed_1 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 0]
        employmentRate_1 = float(len(employed_1))/(float(len(employed_1)) + float(len(unemployed_1)))
        self.totalEmployment_1.append(employmentRate_1)
        # print('Employment rate of class 1: ' + str(employmentRate_1))
        
        employed_2 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 1]
        employed_2_Males = [x for x in employed_2 if x.sex == 'male']
        employed_2_Females = [x for x in employed_2 if x.sex == 'female']
        unemployed_2 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 1]
        employmentRate_2 = float(len(employed_2))/(float(len(employed_2)) + float(len(unemployed_2)))
        self.totalEmployment_2.append(employmentRate_2)
        # print('Employment rate of class 2: ' + str(employmentRate_2))
        
        employed_3 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 2]
        employed_3_Males = [x for x in employed_3 if x.sex == 'male']
        employed_3_Females = [x for x in employed_3 if x.sex == 'female']
        unemployed_3 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 2]
        employmentRate_3 = float(len(employed_3))/(float(len(employed_3)) + float(len(unemployed_3)))
        self.totalEmployment_3.append(employmentRate_3)
        # print('Employment rate of class 3: ' + str(employmentRate_3))
        
        employed_4 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 3]
        employed_4_Males = [x for x in employed_4 if x.sex == 'male']
        employed_4_Females = [x for x in employed_4 if x.sex == 'female']
        unemployed_4 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 3]
        employmentRate_4 = float(len(employed_4))/(float(len(employed_4)) + float(len(unemployed_4)))
        self.totalEmployment_4.append(employmentRate_4)
        # print('Employment rate of class 4: ' + str(employmentRate_4))
        
        employed_5 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 4]
        employed_5_Males = [x for x in employed_5 if x.sex == 'male']
        employed_5_Females = [x for x in employed_5 if x.sex == 'female']
        unemployed_5 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 4]
        employmentRate_5 = float(len(employed_5))/(float(len(employed_5)) + float(len(unemployed_5)))
        self.totalEmployment_5.append(employmentRate_5)
        # print('Employment rate of class 5: ' + str(employmentRate_5))
        
        jobChanges = [x for x in self.pop.livingPeople if x.status == 'employed' and x.jobChange == True]
        jobChangeRate = float(len(jobChanges))/float(len(employed))
        self.totalJobChanges.append(jobChangeRate)
        # print('Job Change Rate: ' + str(jobChangeRate))
        
        employedMales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'male']
        malesIncome = sum([x.income for x in employedMales])
        self.averageIncome_M.append(malesIncome/float(len(employedMales)))
        
        employedFemales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'female']
        femalesIncome = sum([x.income for x in employedFemales])
        self.averageIncome_F.append(femalesIncome/float(len(employedFemales)))
        
        income_1 = sum([x.income for x in employed_1])
        income_1_Males = sum([x.income for x in employed_1_Males])
        income_1_Females = sum([x.income for x in employed_1_Females])
        self.averageIncome_1.append(income_1/float(len(employed_1)))
        self.averageIncome_1_Males.append(income_1_Males/float(len(employed_1_Males)))
        self.averageIncome_1_Females.append(income_1_Females/float(len(employed_1_Females)))
        
        income_2 = sum([x.income for x in employed_2])
        income_2_Males = sum([x.income for x in employed_2_Males])
        income_2_Females = sum([x.income for x in employed_2_Females])
        self.averageIncome_2.append(income_2/float(len(employed_2)))
        self.averageIncome_2_Males.append(income_2_Males/float(len(employed_2_Males)))
        self.averageIncome_2_Females.append(income_2_Females/float(len(employed_2_Females)))
        
        income_3 = sum([x.income for x in employed_3])
        income_3_Males = sum([x.income for x in employed_3_Males])
        income_3_Females = sum([x.income for x in employed_3_Females])
        self.averageIncome_3.append(income_3/float(len(employed_3)))
        self.averageIncome_3_Males.append(income_3_Males/float(len(employed_3_Males)))
        self.averageIncome_3_Females.append(income_3_Females/float(len(employed_3_Females)))
        
        income_4 = sum([x.income for x in employed_4])
        income_4_Males = sum([x.income for x in employed_4_Males])
        income_4_Females = sum([x.income for x in employed_4_Females])
        self.averageIncome_4.append(income_4/float(len(employed_4)))
        self.averageIncome_4_Males.append(income_4_Males/float(len(employed_4_Males)))
        self.averageIncome_4_Females.append(income_4_Females/float(len(employed_4_Females)))
        
        income_5 = sum([x.income for x in employed_5])
        income_5_Males = sum([x.income for x in employed_5_Males])
        income_5_Females = sum([x.income for x in employed_5_Females])
        self.averageIncome_5.append(income_5/float(len(employed_5)))
        self.averageIncome_5_Males.append(income_5_Males/float(len(employed_5_Males)))
        self.averageIncome_5_Females.append(income_5_Females/float(len(employed_5_Females)))
        
        ####### Mobility Outputs ################################################################
        
        self.numberRelocations.append(self.totalRelocations)
        self.totalRelocations = 0
        
        self.numJobRelocations.append(self.jobRelocations)
        self.jobRelocations = 0
        
        self.numMarriageRelocations.append(self.marriageRelocations)
        self.marriageRelocations = 0
        
        self.numSizeRelocations.append(self.sizeRelocations)
        self.sizeRelocations = 0
        
        self.numRetiredRelocations.append(self.retiredRelocations)
        self.retiredRelocations = 0
        
        self.numberTownChanges.append(self.townChanges)
        self.townChanges = 0
        
        
        ## What actually happens to people: do they get the care they need?
       
          
        if totalCareDemandHours == 0:
            networkCareRatio = 0.0
        else:
            networkCareRatio = (totalCareDemandHours - totalUnmetDemandHours)/totalCareDemandHours

        ##familyCareRatio = ( totalCareDemandHours - unmetNeed ) / (1.0 * (totalCareDemandHours+0.01))
        self.totalFamilyCare.append(networkCareRatio)   

        taxBurden = ( totalUnmetDemandHours * self.p['pricePublicSocialCare'] * 52.18 ) / ( taxPayers * 1.0 )
        self.totalTaxBurden.append(taxBurden)
        
        ## Count the proportion of adult women who are married
        totalAdultWomen = 0
        totalMarriedAdultWomen = 0

        for person in self.pop.livingPeople:
            if person.sex == 'female' and person.age >= 18:
                totalAdultWomen += 1
                if person.partner != None:
                    totalMarriedAdultWomen += 1
        marriagePropNow = float(totalMarriedAdultWomen) / float(totalAdultWomen)
        self.marriageProp.append(marriagePropNow)

        ## Some extra debugging stuff just to check that all
        ## the lists are behaving themselves
        if self.p['verboseDebugging']:
            peopleCount = 0
            for i in self.pop.allPeople:
                if i.dead == False:
                    peopleCount += 1
            print "True pop counting non-dead people in allPeople list = ", peopleCount

            peopleCount = 0
            for h in self.map.occupiedHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of all occupied houses = ", peopleCount

            peopleCount = 0
            for h in self.map.allHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of ALL houses = ", peopleCount

            tally = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for h in self.map.occupiedHouses:
                tally[len(h.occupants)] += 1
            for i in range(len(tally)):
                if tally[i] > 0:
                    print i, tally[i]
        
    def relocationProb(self, newocc, oldocc, firstocc):
        alfa = self.p['baseRelocatingProb']/(1+self.p['baseRelocatingProb'])
        totOcc = float(newocc+oldocc)
        deltaOccupants = (totOcc-firstocc)/float(firstocc)
        prob = 1.0 - 1.0/math.exp(self.p['relocationParameter']*math.pow(deltaOccupants, self.p['expReloc']))
        if prob < 0.0:
            prob = 0.0
        return (prob)
    
    
    
    def ageBand(self, age):
        if age <= 19:
            band = 0
        elif age >= 20 and age <= 24:
            band = 1
        elif age >= 25 and age <= 34:
            band = 2
        elif age >= 35 and age <= 44:
            band = 3
        elif age >= 45 and age <= 54:
            band = 4
        else: 
            band = 5
        return (band)
    
    def tenureBand(self, tenure):
        if tenure == 1:
            band = 0
        if tenure >= 2 and tenure <= 3:
            band = 1
        if age >= 4 and age <= 7:
            band = 2
        if age >= 8 and age <= 16:
            band = 3
        else:
            band = 4
        return (band)
    
    def householdYearInTown(self, agent):
        yit = agent.yearsInTown
        if ( agent.partner == None ):
            for i in range(len(agent.children)):
                yit += agent.children[i].yearsInTown
        else:
            yit += agent.partner.yearsInTown
            children = list(set(agent.children + agent.partner.children))
            for i in range(len(children)):
                yit += children[i].yearsInTown
        return (yit)
        
    def childrenInHouse(self, person):
        childrenToMove = [x for x in person.children if x.house == person.house and x.dead == False]
        otherChildren = [x for x in person.partner.children if x.house == person.house and x.dead == False and x not in childrenToMove]
        childrenToMove += otherChildren
        return childrenToMove
    
    def bringTheKids(self, person):
        childrenToMove = [x for x in person.children if x.house == person.house and x.dead == False]
        childrenToMove += [x for x in person.partner.children if x.house == person.partner.house and x.dead == False]
        return childrenToMove
    
    def kidsWithPartner(self, person):
        childrenToMove = [x for x in person.partner.children if x.house == person.partner.house and x.dead == False]
        return childrenToMove
        
    def kidsWithPerson(self, person):
        childrenToMove = [x for x in person.children if x.house == person.house and x.dead == False]
        return childrenToMove
    
    def nearTown(self, ct):
        nearbyTowns = [ k for k in self.map.towns
                                if abs(k.x - ct.x) <= 1
                                and abs(k.y - ct.y) <= 1 ]
        return(random.choice(nearbyTowns))
    
    def farTown(self, ct):
        farTowns = [ k for k in self.map.towns
                                if abs(k.x - ct.x) > 1
                                or abs(k.y - ct.y) > 1 ]
        return(random.choice(farTowns))
        
    def manhattanDistance(self,t1,t2):
        """Calculates the distance between two towns"""
        xDist = abs(t1.x - t2.x)
        yDist = abs(t1.y - t2.y)
        return xDist + yDist 
        
    def getCat(self, age):
        cat = -1
        if age < 20 :
            cat = 0
        elif age >= 20 and age <= 24:
            cat = 1
        elif age >= 25 and age <= 29:
            cat = 2
        elif age >= 30 and age <= 34:
            cat = 3
        elif age >= 35 and age <= 39:
            cat = 4
        elif age >= 40 and age <= 44:
            cat = 5
        elif age >= 45 and age <= 49:
            cat = 6
        elif age >= 50 and age <= 54:
            cat = 7
        elif age >= 55 and age <= 59:
            cat = 8
        elif age >= 60 and age <= 64:
            cat = 9
        elif age >= 65 and age <= 69:
            cat = 10
        else: 
            cat = 11    
        return (cat)
    
    def deltaAge(self, dA):
        if dA <= -10 :
            cat = 0
        elif dA >= -9 and dA <= -3:
            cat = 1
        elif dA >= -2 and dA <= 0:
            cat = 2
        elif dA >= 1 and dA <= 4:
            cat = 3
        elif dA >= 5 and dA <= 9:
            cat = 4
        else:
            cat = 5
        return cat
     
    def initializeCanvas(self):
        """Put up a TKInter canvas window to animate the simulation."""
        self.canvas.pack()
        
         ## Draw some numbers for the population pyramid that won't be redrawn each time
        for a in range(0,self.p['num5YearAgeClasses']):
            self.canvas.create_text(170, 385 - (10 * a),
                                    text=str(5*a) + '-' + str(5*a+4),
                                    font='Helvetica 6',
                                    fill='white')

        ## Draw the overall map, including towns and houses (occupied houses only)
        for t in self.map.towns:
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            self.canvas.create_rectangle(xBasic, yBasic,
                                         xBasic+self.p['pixelsPerTown'],
                                         yBasic+self.p['pixelsPerTown'],
                                         outline='grey',
                                         state = 'hidden' )

        for h in self.map.allHouses:
            t = h.town
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            xOffset = xBasic + 2 + (h.x * 2)
            yOffset = yBasic + 2 + (h.y * 2)

            outlineColour = fillColour = self.p['houseSizeColour'][h.size]
            width = 1

            h.icon = self.canvas.create_rectangle(xOffset,yOffset,
                                                  xOffset + width, yOffset + width,
                                                  outline=outlineColour,
                                                  fill=fillColour,
                                                  state = 'normal' )

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.update()

        for h in self.map.allHouses:
            self.canvas.itemconfig(h.icon, state='hidden')

        for h in self.map.occupiedHouses:
            self.canvas.itemconfig(h.icon, state='normal')

        self.canvas.update()
        self.updateCanvas()
        
    def updateCanvas(self):
        """Update the appearance of the graphics canvas."""

        ## First we clean the canvas off; some items are redrawn every time and others are not
        self.canvas.delete('redraw')

        ## Now post the current year and the current population size
        self.canvas.create_text(self.p['dateX'],
                                self.p['dateY'],
                                text='Year: ' + str(self.year),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')
        self.canvas.create_text(self.p['popX'],
                                self.p['popY'],
                                text='Pop: ' + str(len(self.pop.livingPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        self.canvas.create_text(self.p['popX'],
                                self.p['popY'] + 30,
                                text='Ever: ' + str(len(self.pop.allPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        ## Also some other stats, but not on the first display
        if self.year > self.p['startYear']:
            self.canvas.create_text(350,20,
                                    text='Avg household: ' + str ( round ( self.avgHouseholdSize[-1] , 2 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,40,
                                    text='Marriages: ' + str(self.numMarriages[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,60,
                                    text='Divorces: ' + str(self.numDivorces[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,100,
                                    text='Total care demand: ' + str(round(self.totalCareDemand[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,120,
                                    text='Num taxpayers: ' + str(round(self.numTaxpayers[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,140,
                                    text='Family care ratio: ' + str(round(100.0 * self.totalFamilyCare[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,160,
                                    text='Tax burden: ' + str(round(self.totalTaxBurden[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,180,
                                    text='Marriage prop: ' + str(round(100.0 * self.marriageProp[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = self.p['fontColour'],
                                    tags = 'redraw')

        

        ## Draw the population pyramid split by care categories
        for a in range(0,self.p['num5YearAgeClasses']):
            malePixel = 153
            femalePixel = 187
            for c in range(0,self.p['numCareLevels']):
                mWidth = self.pyramid.maleData[a,c]
                fWidth = self.pyramid.femaleData[a,c]

                if mWidth > 0:
                    self.canvas.create_rectangle(malePixel, 380 - (10*a),
                                                 malePixel - mWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                malePixel -= mWidth
                
                if fWidth > 0:
                    self.canvas.create_rectangle(femalePixel, 380 - (10*a),
                                                 femalePixel + fWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                femalePixel += fWidth

        ## Draw in the display house and the people who live in it
        if len(self.displayHouse.occupants) < 1:
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
            

        outlineColour = self.p['houseSizeColour'][self.displayHouse.size]
        self.canvas.create_rectangle( 50, 450, 300, 650,
                                      outline = outlineColour,
                                      tags = 'redraw' )
        self.canvas.create_text ( 60, 660,
                                  text="Display house " + self.displayHouse.name,
                                  font='Helvetica 10',
                                  fill='white',
                                  anchor='nw',
                                  tags='redraw')
                                  

        ageBracketCounter = [ 0, 0, 0, 0, 0 ]

        for i in self.displayHouse.occupants:
            age = i.age
            ageBracket = age / 20
            if ageBracket > 4:
                ageBracket = 4
            careClass = i.careNeedLevel
            sex = i.sex
            idNumber = i.id
            self.drawPerson(age,ageBracket,ageBracketCounter[ageBracket],careClass,sex,idNumber)
            ageBracketCounter[ageBracket] += 1


        ## Draw in some text status updates on the right side of the map
        ## These need to scroll up the screen as time passes

        if len(self.textUpdateList) > self.p['maxTextUpdateList']:
            excess = len(self.textUpdateList) - self.p['maxTextUpdateList']
            self.textUpdateList = self.textUpdateList[excess:excess+self.p['maxTextUpdateList']]

        baseX = 1035
        baseY = 30
        for i in self.textUpdateList:
            self.canvas.create_text(baseX,baseY,
                                    text=i,
                                    anchor='nw',
                                    font='Helvetica 9',
                                    fill = 'white',
                                    width = 265,
                                    tags = 'redraw')
            baseY += 30

        ## Finish by updating the canvas and sleeping briefly in order to allow people to see it
        self.canvas.update()
        if self.p['delayTime'] > 0.0:
            time.sleep(self.p['delayTime'])


    def drawPerson(self, age, ageBracket, counter, careClass, sex, idNumber):
        baseX = 70 + ( counter * 30 )
        baseY = 620 - ( ageBracket * 30 )

        fillColour = self.p['careLevelColour'][careClass]

        self.canvas.create_oval(baseX,baseY,baseX+6,baseY+6,
                                fill=fillColour,
                                outline=fillColour,tags='redraw')
        if sex == 'male':
            self.canvas.create_rectangle(baseX-2,baseY+6,baseX+8,baseY+12,
                                fill=fillColour,outline=fillColour,tags='redraw')
        else:
            self.canvas.create_polygon(baseX+2,baseY+6,baseX-2,baseY+12,baseX+8,baseY+12,baseX+4,baseY+6,
                                fill=fillColour,outline=fillColour,tags='redraw')
        self.canvas.create_rectangle(baseX+1,baseY+13,baseX+5,baseY+20,
                                     fill=fillColour,outline=fillColour,tags='redraw')
            
        self.canvas.create_text(baseX+11,baseY,
                                text=str(age),
                                font='Helvetica 6',
                                fill='white',
                                anchor='nw',
                                tags='redraw')
        self.canvas.create_text(baseX+11,baseY+8,
                                text=str(idNumber),
                                font='Helvetica 6',
                                fill='grey',
                                anchor='nw',
                                tags='redraw')


    def doGraphs(self, folder):
        """Plot the graphs needed at the end of one run."""
        years = [int(i) for i in self.times]
        
        # Chart 1: total social and child care demand and potential supply (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.totalCareSupply, linewidth=3, label = 'Potential Supply')
        ax.stackplot(years, self.totalSocialCareDemand, self.totalChildCareDemand, labels = ['Social Care Need','Child Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        ax.set_title('Care Needs and Potential Supply')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/DemandSupplyStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 2: total informal and formal care received and unmet care needs (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalCareReceived, self.totalFormalCareReceived, 
                      self.totalUnmetDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Care and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/CareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 3: total informal and formal social care received and unmet social care needs (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalSocialCareReceived, self.totalFormalSocialCareReceived, 
                      self.totalSocialCareUnmetDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Social Care and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/SocialCareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 4: total informal and formal child care received and unmet child care needs (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalChildCareReceived, self.totalFormalChildCareReceived, 
                      self.totalChildCareUnmetDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Child Social Care and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/ChildCareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 5: informal and formal care received and unmet care needs per recipient by social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.totalInformalCarePerRecipient_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.totalFormalCarePerRecipient_1[-20:])
        meanUnmetNeed_1 = np.mean(self.totalUnmetNeedPerRecipient_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.totalInformalCarePerRecipient_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.totalFormalCarePerRecipient_2[-20:])
        meanUnmetNeed_2 = np.mean(self.totalUnmetNeedPerRecipient_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.totalInformalCarePerRecipient_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.totalFormalCarePerRecipient_3[-20:])
        meanUnmetNeed_3 = np.mean(self.totalUnmetNeedPerRecipient_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.totalInformalCarePerRecipient_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.totalFormalCarePerRecipient_4[-20:])
        meanUnmetNeed_4 = np.mean(self.totalUnmetNeedPerRecipient_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.totalInformalCarePerRecipient_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.totalFormalCarePerRecipient_5[-20:])
        meanUnmetNeed_5 = np.mean(self.totalUnmetNeedPerRecipient_5[-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours of care')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Care Need per Recipient')
        fig.tight_layout()
        filename = folder + '/CarePerRecipientByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 6: informal and formal care supplied per carer by social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        meanInformalCareSupplied_1 = np.mean(self.totalInformalCarePerCarer_1[-20:])
        meanFormalCareSupplied_1 = np.mean(self.totalFormalCarePerCarer_1[-20:])
        meanInformalCareSupplied_2 = np.mean(self.totalInformalCarePerCarer_2[-20:])
        meanFormalCareSupplied_2 = np.mean(self.totalFormalCarePerCarer_2[-20:])
        meanInformalCareSupplied_3 = np.mean(self.totalInformalCarePerCarer_3[-20:])
        meanFormalCareSupplied_3 = np.mean(self.totalFormalCarePerCarer_3[-20:])
        meanInformalCareSupplied_4 = np.mean(self.totalInformalCarePerCarer_4[-20:])
        meanFormalCareSupplied_4 = np.mean(self.totalFormalCarePerCarer_4[-20:])
        meanInformalCareSupplied_5 = np.mean(self.totalInformalCarePerCarer_5[-20:])
        meanFormalCareSupplied_5 = np.mean(self.totalFormalCarePerCarer_5[-20:])
        informalCare = (meanInformalCareSupplied_1, meanInformalCareSupplied_2, meanInformalCareSupplied_3,
                        meanInformalCareSupplied_4, meanInformalCareSupplied_5)
        formalCare = (meanFormalCareSupplied_1, meanFormalCareSupplied_2, meanFormalCareSupplied_3,
                      meanFormalCareSupplied_4, meanFormalCareSupplied_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal and Formal Care per Carer')
        fig.tight_layout()
        filename = folder + '/CarePerCarerByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 7: informal and formal care supplied by kinship network distance (mean of last 20 years)
        n_groups = 4
        meanInformalCareHousehold = np.mean(self.totalInformalSupplyHousehold[-20:])
        meanFormalCareHousehold = np.mean(self.totalFormalSupplyHousehold[-20:])
        meanInformalCare_K1 = np.mean(self.totalInformalSupplyNoK_1[-20:])
        meanFormalCare_K1 = np.mean(self.totalFormalSupplyNoK_1[-20:])
        meanInformalCare_K2 = np.mean(self.totalInformalSupplyNoK_2[-20:])
        meanFormalCare_K2 = np.mean(self.totalFormalSupplyNoK_2[-20:])
        meanInformalCare_K3 = np.mean(self.totalInformalSupplyNoK_3[-20:])
        meanFormalCare_K3 = np.mean(self.totalFormalSupplyNoK_3[-20:])
        informalCare = (meanInformalCareHousehold, meanInformalCare_K1, meanInformalCare_K2, meanInformalCare_K3)
        formalCare = (meanFormalCareHousehold, meanFormalCare_K1, meanFormalCare_K2, meanFormalCare_K3)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_xticks(ind)
        plt.xticks(ind, ('Household', 'I', 'II', 'III'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal and Formal Care per Kinship Level')
        fig.tight_layout()
        filename = folder + '/InformalFormalCareByKinshipStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 8: Care supplied by gender (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalCareSuppliedFemale, self.totalCareSuppliedMale, 
                      labels = ['Care by Women', 'Care by Men'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Care supplied by gender')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/CareSuppliedByGenderStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 9: informal care provided by gender per social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        informalCareMales_1 = np.mean(self.totalInformalCareSuppliedMale_1[-20:])
        informalCareMales_2 = np.mean(self.totalInformalCareSuppliedMale_2[-20:])
        informalCareMales_3 = np.mean(self.totalInformalCareSuppliedMale_3[-20:])
        informalCareMales_4 = np.mean(self.totalInformalCareSuppliedMale_4[-20:])
        informalCareMales_5 = np.mean(self.totalInformalCareSuppliedMale_5[-20:])
        informalCareFemales_1 = np.mean(self.totalInformalCareSuppliedFemale_1[-20:])
        informalCareFemales_2 = np.mean(self.totalInformalCareSuppliedFemale_2[-20:])
        informalCareFemales_3 = np.mean(self.totalInformalCareSuppliedFemale_3[-20:])
        informalCareFemales_4 = np.mean(self.totalInformalCareSuppliedFemale_4[-20:])
        informalCareFemales_5 = np.mean(self.totalInformalCareSuppliedFemale_5[-20:])
        means_males = (informalCareMales_1, informalCareMales_2, informalCareMales_3, informalCareMales_4, informalCareMales_5)
        means_females = (informalCareFemales_1, informalCareFemales_2, informalCareFemales_3, informalCareFemales_4, informalCareFemales_5)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        rects1 = ax.bar(index, means_females, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Female')
        rects2 = ax.bar(index + bar_width, means_males, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Male')
        ax.set_ylabel('Hours of Care')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Informal Care Supplied by Gender')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/InformalCareByGenderAndClassGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 10: income by gender per social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        incomeMales_1 = np.mean(self.averageIncome_1_Males[-20:])
        incomeMales_2 = np.mean(self.averageIncome_2_Males[-20:])
        incomeMales_3 = np.mean(self.averageIncome_3_Males[-20:])
        incomeMales_4 = np.mean(self.averageIncome_4_Males[-20:])
        incomeMales_5 = np.mean(self.averageIncome_5_Males[-20:])
        incomeFemales_1 = np.mean(self.averageIncome_1_Females[-20:])
        incomeFemales_2 = np.mean(self.averageIncome_2_Females[-20:])
        incomeFemales_3 = np.mean(self.averageIncome_3_Females[-20:])
        incomeFemales_4 = np.mean(self.averageIncome_4_Females[-20:])
        incomeFemales_5 = np.mean(self.averageIncome_5_Females[-20:])
        means_males = (incomeMales_1, incomeMales_2, incomeMales_3, incomeMales_4, incomeMales_5)
        means_females = (incomeFemales_1, incomeFemales_2, incomeFemales_3, incomeFemales_4, incomeFemales_5)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        rects3 = ax.bar(index, means_females, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Female')
        rects4 = ax.bar(index + bar_width, means_males, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Male')
        ax.set_ylabel('Income')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Female and Male Average Income')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        plt.tight_layout()
        filename = folder + '/IncomeByGenderAndClassGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        ################################################################## 
        # Chart 11: Population by social class and number of taxpayers (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.numTaxpayers, linewidth = 3, label = 'Number of Taxpayers', color = 'yellow')
        ax.stackplot(years, self.unskilledPop, self.skilledPop, self.lowerclassPop,
                      self.middleclassPop, self.upperclassPop, 
                      labels = ['Unskilled Class (I)','Skilled Class (II)', 'Lower Class (III)', 'Middel Class (IV)', 'Upper Class (V)'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Population and Number of Taxpayers')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/PopulationTaxPayersStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 12: Average Household size (1960-2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.avgHouseholdSize_1, label = 'Class I')
        p2, = ax.plot(years, self.avgHouseholdSize_2, label = 'Class II')
        p3, = ax.plot(years, self.avgHouseholdSize_3, label = 'Class III')
        p4, = ax.plot(years, self.avgHouseholdSize_4, label = 'Class IV')
        p5, = ax.plot(years, self.avgHouseholdSize_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Family Size')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/AverageFamilySizeChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()         
                 
##        pylab.plot(years,self.numMarriages)
##        pylab.ylabel('Number of marriages')
##        pylab.xlabel('Year')
##        pylab.savefig('numMarriages.pdf')
##
##        pylab.plot(years,self.numDivorces)
##        pylab.ylabel('Number of divorces')
##        pylab.xlabel('Year')
##        pylab.savefig('numDivorces.pdf')
        
        # Chart 13: Average Tax Burden (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.totalTaxBurden, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Care costs per taxpayer per year')
        ax.set_xlabel('Year')
        ax.set_title('Average Tax Burden in pounds')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/TaxBurdenChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()  
      
        # Chart 14: Proportion of married adult women (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.marriageProp, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Proportion of married adult women')
        ax.set_xlabel('Year')
        ax.set_title('Marriage Rate (females)')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        filename = folder + '/MarriageRateChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
class PopPyramid:
    """Builds a data object for storing population pyramid data in."""
    def __init__ (self, ageClasses, careLevels):
        self.maleData = pylab.zeros((ageClasses,careLevels),dtype=int)
        self.femaleData = pylab.zeros((ageClasses, careLevels),dtype=int)

    def update(self, year, ageClasses, careLevels, pixelFactor, people):
        ## zero the two arrays
        for a in range (ageClasses):
            for c in range (careLevels):
                self.maleData[a,c] = 0
                self.femaleData[a,c] = 0
        ## tally up who belongs in which category
        for i in people:
            ageClass = ( year - i.birthdate ) / 5
            if ageClass > ageClasses - 1:
                ageClass = ageClasses - 1
            careClass = i.careNeedLevel
            if i.sex == 'male':
                self.maleData[ageClass,careClass] += 1
            else:
                self.femaleData[ageClass,careClass] += 1

        ## normalize the totals into pixels
        total = len(people)        
        for a in range (ageClasses):
            for c in range (careLevels):
                self.maleData[a,c] = pixelFactor * self.maleData[a,c] / total
                self.femaleData[a,c] = pixelFactor * self.femaleData[a,c] / total