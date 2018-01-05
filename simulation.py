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
        
         # Demographic outputs
        self.pops = []
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
        
        self.marriageTally = 0
        self.numMarriages = []
        self.divorceTally = 0
        self.numDivorces = []
        
        # Social Care outputs
        
        self.totalCareDemand = []
        self.totalCareSupply = []
        self.totalUnmetDemand = []
        self.totalCareDemand_1 = []
        self.totalCareSupply_1 = []
        self.totalCareDemand_2 = []
        self.totalCareSupply_2 = []
        self.totalCareDemand_3 = []
        self.totalCareSupply_3 = []
        self.totalCareDemand_4 = []
        self.totalCareSupply_4 = []
        self.totalCareDemand_5 = []
        self.totalCareSupply_5 = []
        
        self.totalInformalSupply_1 = []
        self.totalFormalSupply_1 = []
        self.totalUnmetDemand_1 = []
        self.totalInformalSupply_2 = []
        self.totalFormalSupply_2 = []
        self.totalUnmetDemand_2 = []
        self.totalInformalSupply_3 = []
        self.totalFormalSupply_3 = []
        self.totalUnmetDemand_3 = []
        self.totalInformalSupply_4 = []
        self.totalFormalSupply_4 = []
        self.totalUnmetDemand_4 = []
        self.totalInformalSupply_5 = []
        self.totalFormalSupply_5 = []
        self.totalUnmetDemand_5 = []
        
        self.totalSupplyHousehold = []
        self.totalSupplyNoK_1 = []
        self.totalSupplyNoK_2 = []
        self.totalSupplyNoK_3 = []
        
        # Economic outputs
        
        self.totalEmployment = []
        self.totalEmployment_1 = []
        self.totalEmployment_2 = []
        self.totalEmployment_3 = []
        self.totalEmployment_4 = []
        self.totalEmployment_5 = []
        
        self.averageIncome_M = []
        self.averageIncome_F = []
        
        self.averageIncome_1 = []
        self.averageIncome_2 = []
        self.averageIncome_3 = []
        self.averageIncome_4 = []
        self.averageIncome_5 = []
        
        # Mobility outputs
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
        
        
        self.numTaxpayers = []
        self.totalUnmetNeed = []
        self.totalFamilyCare = []
        self.totalTaxBurden = []
        self.marriageProp = []
        
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

        random.seed(self.p['favouriteSeed'])

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

        # Graphic Output related code
        

        if self.p['singleRunGraphs']:
            self.doGraphs()

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
                                  )
            
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
        
        self.doDeaths()
        self.doBirths()
        self.careTransitions()
        self.careSupplies()
        self.allocateCare()
        self.jobMarket()
        self.doDivorces()
        self.doMarriages()
        self.movingAround()
        self.ageTransitions()
        
        # self.householdSize()
        
        self.pyramid.update(self.year, self.p['num5YearAgeClasses'],
                            self.p['numCareLevels'],
                            self.p['pixelsInPopPyramid'],
                            self.pop.livingPeople)
        self.doStats()
        if (self.p['interactiveGraphics']):
            self.updateCanvas()
        
    def doDeaths(self):
        
        preDeath = len(self.pop.livingPeople)
        
        """Consider the possibility of death for each person in the sim."""
        for person in self.pop.livingPeople:
            age = person.age
            
            ####     Death process with histroical data  after 1950   ##################
            if self.year > 1950:
                if age > 109:
                    age = 109
                if person.sex == 'male':
                    rawRate = self.death_male[age, self.year-1950]
                    baseRate = self.baseRate(self.p['mortalityBias'], rawRate)
                if person.sex == 'female':
                    rawRate = self.death_female[age, self.year-1950]
                    baseRate = self.baseRate(self.p['mortalityBias'], rawRate)
                dieProb = baseRate*math.pow(self.p['mortalityBias'], person.classRank)
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
                dieProb = self.p['baseDieProb'] + babyDieProb + ageDieProb
                ####################################################################
                
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
                
                
        
        self.pop.livingPeople[:] = [x for x in self.pop.livingPeople if x.dead == False]
        
        postDeath = len(self.pop.livingPeople)
        
        print('the number of people who died is: ' + str(preDeath - postDeath))
        
        # print(len(self.pop.livingPeople))
    
    def doBirths(self):
        preBirth = len(self.pop.livingPeople)
        marriedLadies = 0
        adultLadies = 0
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age > self.p['minPregnancyAge']
                                  and x.age < self.p['maxPregnancyAge']
                                  and x.partner != None ]
                        
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
                    rawRate = (self.fert_data[(self.year - woman.birthdate)
                                -16,self.year-1950])/marriedPercentage
                baseRate = self.baseRate(self.p['fertilityBias'], rawRate)
                birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
                
                if random.random() < birthProb:
                    # (self, mother, father, age, birthYear, sex, status, house,
                    # classRank, sec, edu, wage, income, finalIncome):

                    baby = Person(woman, woman.partner, 0, self.year, 'random', 
                                  'child', woman.house, woman.classRank, woman.sec, None, 0, 0, 0)
                    self.pop.allPeople.append(baby)
                    self.pop.livingPeople.append(baby)
                    woman.house.occupants.append(baby)
                    woman.children.append(baby)
                    woman.partner.children.append(baby)
                    if woman.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(woman.id) + " had a baby, #" + str(baby.id) + "." 
                        self.textUpdateList.append(messageString)
        postBirth = len(self.pop.livingPeople)
        
        print('the number of births is: ' + str(postBirth - preBirth))
        
    def careTransitions(self):
        for person in self.pop.livingPeople:
            person.visitedCarer = False
            person.hoursDemand = 0
            person.residualNeed = 0
            person.residualInformalSupply = 0
            person.residualFormalSupply = 0
            person.socialWork = 0
            person.workToCare = 0
            person.totalSupply = 0
            person.extraworkCare = 0
        children = [x for x in self.pop.livingPeople if x.age < 16]
        for child in children:
            care = self.p['zeroYearCare']/math.exp(self.p['childcareDecreaseRate']*child.age)
            if ( child.hoursDemand < care ):
                child.hoursDemand = care
            if child.age == 0:
                child.mother.socialWork = self.p['zeroYearCare']
                child.mother.income = 0
                child.mother.status = 'maternity'
                child.mother.babyCarer = True
                child.residualNeed = 0
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
            baseProb = self.baseRate(self.p['careBias'], careProb)
            careProb = baseProb*math.pow(self.p['careBias'], person.classRank)
            
            if random.random() < careProb:
                person.status = 'inactive'
                baseTransition = self.baseRate(self.p['careBias'], 1-self.p['careTransitionRate'])
                transitionRate = 1.0 - baseTransition*math.pow(self.p['careBias'], person.classRank)
                stepCare = 1
                bound = transitionRate
                while ( random.random() > bound and stepCare < self.p['numCareLevels'] - 1 ):
                    stepCare += 1
                    bound += (1-bound)*transitionRate
                person.careNeedLevel += stepCare
                
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = self.p['numCareLevels'] - 1
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                if ( person.hoursDemand < careNeed ):
                    person.hoursDemand = careNeed
                    person.residualNeed = careNeed
                    
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " now has "
                    messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                    self.textUpdateList.append(messageString)
    
    def careSupplies(self):
        for agent in self.pop.livingPeople:
            if agent.visitedCarer == True:
                continue
            household = agent.house.occupants
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

            employed = [x for x in householdCarers if x.status == 'employed']
            employed.sort(key=operator.attrgetter("marketWage"))

            householdIncome = self.householdIncome(household)
            householdPerCapitaIncome = householdIncome/len(household)
            
            # Compute the total income devoted to informal care supply
            incomeCoefficient = math.exp(self.p['incomeCareParam']*householdPerCapitaIncome)
            residualIncomeForCare = householdIncome*(1 - 1/incomeCoefficient)
            # Assign the total informal care supply to the employed members of the household (according to income)
            for worker in employed:
                worker.extraworkCare = self.p['employedHours']
                # worker.extraworkCare = self.p['employedHours']
                maxIndividualHours = residualIncomeForCare/worker.marketWage
                if maxIndividualHours > self.p['weeklyHours']:
                    individualSupply = self.p['weeklyHours']
                else:
                    individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                worker.residualInformalSupply = individualSupply
                residualIncomeForCare -= individualSupply*worker.marketWage
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
                residualSupply -= person.residualFormalSupply
                if residualSupply == 0:
                    break
                        
    def allocateCare(self):
        careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
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
            residualReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.totalSupply > 0]
    
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
        if pin.father != None:
            brothers = list(set(pin.father.children+pin.mother.children))
            for brother in brothers:
                if brother.dead == False and brother.house not in households and brother.house.town == pin.house.town:
                    independentBrothers.append(brother)
                    households.append(brother.house)
        kn.append(independentBrothers)
        # Uncles and aunts
        uncles = []
        if pin.father != None and pin.father.father != None:
            maternalUncles = list(set(pin.mother.father.children + pin.mother.mother.children))
            maternalUncles.remove(pin.mother)
            paternalUncles = list(set(pin.father.father.children + pin.father.mother.children))
            paternalUncles.remove(pin.father)
            unclesList = list(set(maternalUncles+paternalUncles))
            for uncle in unclesList:
                if uncle.dead == False and uncle.house not in households and uncle.house.town == pin.house.town:
                    uncles.append(uncle)
                    households.append(uncle.house)
        kn.append(uncles)
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
            if (carer == receiver.father or carer == receiver.mother or carer in receiver.children):
                if townCarer != townReceiver:
                    for member in householdCarers:
                        totsupply += member.residualFormalSupply
                else:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        if member.marketWage > self.p['priceSocialCare']:
                            totsupply += member.residualFormalSupply
                        else:   
                            totsupply += member.residualInformalSupply
            elif townCarer == townReceiver:
                for member in notWorking:
                    totsupply += member.residualInformalSupply
                for member in employed:
                    totsupply += member.extraworkCare
            
            supplies.append(totsupply)

        totalSupply = sum(supplies)
        # Then, randomly select a supplier according to the weighted supplies
        return(totalSupply)
    
    def getCare(self, receiver):
        townReceiver = receiver.house.town 
        informalCare = 0
        formalCare = 0
        networkList = []
        for i in range(len(receiver.socialNetwork)):
            for j in receiver.socialNetwork[i]:
                networkList.append(j)
        probCarers = self.probSuppliers(receiver)
        carer = np.random.choice(networkList, p = probCarers)
        townCarer = carer.house.town
        household = carer.house.occupants
        householdCarers = [x for x in household if x.hoursDemand == 0]
        notWorking = [x for x in householdCarers if x.residualInformalSupply > 0]
        retired = [x for x in notWorking if x.status == 'retired']
        retired.sort(key=operator.attrgetter("residualSupply"), reverse=True)
        students = [x for x in notWorking if x.status == 'student']
        students.sort(key=operator.attrgetter("residualSupply"), reverse=True)
        unemployed = [x for x in notWorking if x.status == 'unemployed']
        unemployed.sort(key=operator.attrgetter("marketWage"))
        employed = [x for x in householdCarers if x.status == 'employed' and (x.extraworkCare > 0 or x.residualInformalSupply > 0 or x.residualFormalSupply > 0)]
        employed.sort(key=operator.attrgetter("marketWage"))
        # Finally, extract a 'quantum' of care from one of the selected household's members.
        if (carer == receiver.father or carer == receiver.mother or carer in receiver.children):
            if townCarer == townReceiver:
                if len(retired) > 0:
                    retired[0].residualInformalSupply -= self.p['quantumCare']
                    retired[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                elif len(students) > 0:
                    students[0].residualInformalSupply -= self.p['quantumCare']
                    students[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                elif len(unemployed) > 0:
                    unemployed[0].residualInformalSupply -= self.p['quantumCare']
                    unemployed[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                else:
                    for member in employed:
                        if member.extraworkCare > 0:
                            member.socialWork += self.p['quantumCare']
                            member.extraworkCare -= self.p['quantumCare']
                            informalCare = self.p['quantumCare']
                            break
                        else:
                            if member.marketWage < self.p['priceSocialCare']: 
                                if member.residualInformalSupply > 0:
                                    member.residualInformalSupply -= self.p['quantumCare']
                                    member.socialWork += self.p['quantumCare']
                                    informalCare = self.p['quantumCare']
                                    break
                            else: 
                                if member.residualFormalSupply > 0:
                                    member.residualFormalSupply -= self.p['quantumCare']
                                    member.workToCare += self.p['quantumCare']
                                    formalCare = self.p['quantumCare']
                                    break
            else:
                for member in employed:
                     if member.residualFormalSupply > 0:
                         member.residualFormalSupply -= self.p['quantumCare']
                         member.workToCare += self.p['quantumCare']
                         formalCare = self.p['quantumCare']
                         break
                        
        elif townCarer == townReceiver: 
            if len(retired) > 0:
                retired[0].residualInformalSupply -= self.p['quantumCare']
                retired[0].socialWork += self.p['quantumCare']
                informalCare = self.p['quantumCare']
            elif len(students) > 0:
                students[0].residualInformalSupply -= self.p['quantumCare']
                students[0].socialWork += self.p['quantumCare']
                informalCare = self.p['quantumCare']
            elif len(unemployed) > 0:
                unemployed[0].residualInformalSupply -= self.p['quantumCare']
                unemployed[0].socialWork += self.p['quantumCare']
                informalCare = self.p['quantumCare']
            else:
                if employed[0].extraworkCare > 0:
                    employed[0].socialWork += self.p['quantumCare']
                    employed[0].extraworkCare -= self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                   # employed[0].residualInformalSupply -= self.p['quantumCare']
                   # employed[0].residualSupply -= self.p['quantumCare']
                   # employed[0].socialWork += self.p['quantumCare']
                   # informalCare = self.p['quantumCare']
                
        receiver.informalCare += informalCare
        receiver.formalCare += formalCare
        # receiver.totalSupply -= self.p['quantumCare']
        receiver.residualNeed -= self.p['quantumCare'] 
    
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
            if (carer == receiver.father or carer == receiver.mother or carer in receiver.children):
                if townCarer != townReceiver:
                    for member in householdCarers:
                        totsupply += member.residualFormalSupply
                else:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        if member.marketWage > self.p['priceSocialCare']:
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
                wages.append(member.marketWage)
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
            
        for person in self.pop.livingPeople:
            if person.status == 'maternity':
                minAge = min([x.age for x in person.children])
                if minAge > 0:
                    person.babyCarer == False
                    person.status = 'unemployed'
            
        activePop = [x for x in self.pop.livingPeople if x.status != 'inactive']
        
        for person in activePop:
            if person.age == self.p['minWorkingAge']:
                person.status = 'student'
                person.classRank = 0
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person)
                if random.random() > probStudy:
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now a student.")
            if ( person.age == 18 and person.status == 'student'):
                person.classRank = 1
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person)
                if random.random() > probStudy:
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
            if ( person.age == 20 and person.status == 'student'):
                person.classRank = 2
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person)
                if random.random() > probStudy:
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
            if ( person.age == 22 and person.status == 'student'):
                person.classRank = 3
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person)
                if random.random() > probStudy:
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
                person.income = self.p['pensionIncome'][person.classRank]*self.p['weeklyHours']
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " has now retired.")
                        
            if person.status == 'student' and person.mother.dead and person.father.dead:
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
    
    def transitionProb (self, person):
        if person.father.dead == False + person.mother.dead == False != 0:
            if person.father.dead == False:
                householdIncome = self.statusQuo(person.father)
            elif person.mother.dead == False:
                householdIncome = self.statusQuo(person.mother)
            forgoneSalary = self.p['incomeInitialLevels'][person.classRank]*self.p['weeklyHours']
            educationCosts = self.p['educationCosts'][person.classRank]
            relCost = (forgoneSalary+educationCosts)/householdIncome
            targetEL = max(person.father.classRank, person.mother.classRank)
            dE = abs(targetEL - (person.classRank + 1))
            incomeEffect = self.p['eduWageSensitivity']*math.pow(relCost, self.p['exponentIncome'])
            educationEffect = self.p['eduRankSensitivity']*math.pow(dE, self.p['exponentRank'])
            pStudy = 1/math.exp(incomeEffect+educationEffect)
        else:
            pStudy = 0.0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        return (pStudy)
    
    def enterWorkForce(self, person):
        person.status = 'unemployed'
        person.income = 0
        person.marketWage = self.marketWage(person)
        person.education = self.p['educationLevels'][person.classRank]
        self.finalIncome = self.p['incomeFinalLevels'][person.classRank]
        
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
            baseRate = self.baseRate(self.p['divorceBias'], rawSplit)
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
                elif i.sex == 'female':
                    eligibleWomen.append(i)
                    
        ######     Otional: select a subset of eligible men based on age    ##########################################
        potentialGrooms = []
        for m in eligibleMen:
            manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][m.age/10]
            if random.random() < manMarriageProb:
                potentialGrooms.append(m)
        ###########################################################################################################
        
        for man in eligibleMen: # for man in potentialGrooms:
            maxEncounters = self.datingActivity(man)
            potentialBrides = []
            for woman in eligibleWomen:
                if man.mother != None and woman.mother != None:
                    if man.mother != woman.mother and man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                else:
                    if man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                        
            if maxEncounters < len(potentialBrides):
                numberEncounters = maxEncounters
            else:
                numberEncounters = len(potentialBrides)
                
            for i in range(numberEncounters):
                woman = np.random.choice(potentialBrides)
                manTown = man.house.town
                womanTown = woman.house.town
                geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                statusDistance = float(abs(man.classRank-woman.classRank))/float((self.p['numberClasses']-1))
                geoEffect = self.p['betaGeo']*math.pow(geoDistance, self.p['expGeo'])
                socEffect = self.p['betaSoc']*math.pow(statusDistance, self.p['expSoc'])
                geosocProb = self.p['baseMarriageProb']/math.exp(geoEffect + socEffect)
                if random.random() < geosocProb:
                    ageProb = self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                    if random.random() < ageProb:
                        man.partner = woman
                        woman.partner = man
                        eligibleMen.remove(man)
                        eligibleWomen.remove(woman)
                        self.marriageTally += 1
                
                        if man.house == self.displayHouse or woman.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                            messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                            messageString += ") marry."
                            self.textUpdateList.append(messageString)
                            
                        break
         
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
                    
            
    def datingActivity(self, man):
        # Function to compute dating activity based on age, income and other factors.
        # .............................
        numberEncounters = self.p['baseEncounters']
        return numberEncounters
            
    def jobMarket(self):

        activePop = [x for x in self.pop.livingPeople if x.status == 'employed' or x.status == 'unemployed']
        
        for person in activePop:
            person.searchJob = True
            person.jobChange = False
            self.updateWork(person)
            
        employed = len([x for x in activePop if x.status == 'employed'])
        unemployed = len(activePop) - employed
        self.exitWork = 0
        self.enterWork = 0
        
        workingPool = [x for x in activePop if x.searchJob == True]
        
        while (len(workingPool) > 0):
            a = np.random.choice(workingPool)
            unemploymentProb = self.unemploymentRate(self.ageBand(a.age), a.classRank)
            a.searchJob = False
            r = random.random()
            if ( a.status == 'employed' and r < unemploymentProb*self.p['firedCoefficient'] ):
                a.status = 'unemployed'
                a.marketWage = self.marketWage(a)
                a.income = 0.0
                a.finalIncome = 0.0
                a.jobTenure = 0
                a.jobLocation = None
                self.exitWork += 1
            else: 
                statusQuo = self.statusQuo(a)
                relocationCost = self.computeRelocationsCost(a)
                relativeRC = relocationCost/statusQuo
                relocationPropensity = self.relocationPropensity(relativeRC)
                probTowns = self.townsProb(a.classRank, a.house.town, relocationPropensity)
                # A job opportunity, characterized by a certain wage and location, is generated for the agent
                jobTown1 = np.random.choice(self.map.towns, p = probTowns)
                dK = np.random.normal(0, self.p['wageVar'])
                k1 = self.p['incomeFinalLevels'][a.classRank]*math.exp(dK)
                wage1 = self.computeWage(a, k1)
                if ( a.partner == None ):
                    newHouseholdIncome = wage1*self.p['weeklyHours']
                    if a.status == 'employed':
                        resWage = (1+self.p['minIncreaseEmployed'])*statusQuo
                    elif a.status == 'unemployed':
                        resWage = (1+self.p['maxDecreaseUnemployed'])*statusQuo
                    relCost = 0
                    if ( jobTown1 != a.house.town ):
                        relCost = relocationCost
                    if newHouseholdIncome - relCost > resWage:
                        self.changeJob(a, None, False, jobTown1, wage1, None, k1, None)
                else:
                    b = a.partner
                    if a.status == 'unemployed' and b.status == 'unemployed':
                        resWage = (1+self.p['maxDecreaseUnemployed'])*statusQuo
                    else:
                        resWage = (1+self.p['minIncreaseEmployed'])*statusQuo
                        
                    if a.partner.searchJob == False:
                        newHouseholdIncome = (wage1+b.marketWage)*self.p['weeklyHours']
                        relCost = 0
                        if ( jobTown1 != a.house.town ):
                            relCost = relocationCost
                        if newHouseholdIncome - relCost > resWage:
                            self.changeJob(a, None, False, jobTown1, wage1, None, k1, None)
                    else:
                        # Conjoint decision
                        b.searchJob = False
                        relocationCost = self.computeRelocationsCost(b)
                        relativeRC = relocationCost/statusQuo
                        relocationPropensity = self.relocationPropensity(relativeRC)
                        probTowns = self.townsProb(b.classRank, b.house.town, relocationPropensity)
                        # A job opportunity, characterized by a certain wage and location, is generated for the agent's partner
                        jobTown2 = np.random.choice(self.map.towns, p = probTowns)
                        dK = np.random.normal(0, self.p['wageVar'])
                        k2 = self.p['incomeFinalLevels'][b.classRank]*math.exp(dK)
                        wage2 = self.computeWage(b, k2)

                        # There are 5 possible situations:
                        # Situation 1
                        if ( a.house.town != jobTown1 and a.house.town != jobTown2 and jobTown1 != jobTown2 ): 
                            # If the status quo changes, both partners will have to relocate
                            rc = relocationCost
                            # In this case, two changes to the status quo are possible: A accepts and B refuses or vice-versa
                            # Case 1: A accepts and B refuses
                            expectedHouseholdIncome = (wage1+b.marketWage)*self.p['weeklyHours']
                            netIncome1 = expectedHouseholdIncome - rc
                            # Case 2: B Accepts and A refuses
                            expectedHouseholdIncome = (wage2+a.marketWage)*self.p['weeklyHours']
                            netIncome2 = expectedHouseholdIncome - rc
                            
                            bestIncome = max(netIncome1, netIncome2)
                            if bestIncome > resWage:
                                if (netIncome1 > netIncome2):
                                    self.changeJob(a, b, False, jobTown1, wage1, wage2, k1, k2)
                                else:
                                    self.changeJob(b, a, False, jobTown2, wage2, wage1, k2, k1)
                        
                        # Situation 2
                        elif ( a.house.town != jobTown1 and b.house.town == jobTown2 ):
                            # In this case, two changes to the status quo are possible: A accepts and B refuses or vice-versa
                            # Case 1: A accepts and B refuses
                            rc = relocationCost
                            expectedHouseholdIncome = (wage1+b.marketWage)*self.p['weeklyHours']
                            netIncome1 = expectedHouseholdIncome - rc
                            # Case 2: B Accepts and A refuses
                            # No relocation needed: A does not need to resign, if employed
                            rc = 0
                            expectedHouseholdIncome = (wage2+a.marketWage)*self.p['weeklyHours']
                            netIncome2 = expectedHouseholdIncome - rc
                            
                            bestIncome = max(netIncome1, netIncome2)
                            
                            if bestIncome > resWage:
                                if ( netIncome1 > netIncome2):
                                    self.changeJob(a, b, False, jobTown1, wage1, wage2, k1, k2)
                                else:
                                    self.changeJob(b, a, False, jobTown2, wage2, wage1, k2, k1)
                        
                        # Situation 3
                        elif ( a.house.town != jobTown1 and jobTown1 == jobTown2 ):
                            # In this case, both partners can accept as the new destination is identical 
                            # We have 3 cases: both accept, A accepts and B refuses and B accepts and A refuses
                            # In all three cases, both need to relocate
                            rc = relocationCost
                            # Case 1: both accept
                            expectedHouseholdIncome = (wage1 + wage2)*self.p['weeklyHours']
                            netIncome1 = expectedHouseholdIncome - rc
                            # Case 2: A accepts and B refuses
                            expectedHouseholdIncome = (wage1 + b.marketWage)*self.p['weeklyHours']
                            netIncome2 = expectedHouseholdIncome - rc
                            #Case 3: A refuses and B accepts
                            expectedHouseholdIncome = (wage2 + a.marketWage)*self.p['weeklyHours']
                            netIncome3 = expectedHouseholdIncome - rc
                            bestIncome = max(netIncome1, netIncome2, netIncome3)
                            
                            if bestIncome > resWage:
                                if ( bestIncome == netIncome1 ):
                                    self.changeJob(a, b, True, jobTown1, wage1, wage2, k1, k2)
                                elif ( bestIncome == netIncome2 ):
                                    self.changeJob(a, b, False, jobTown1, wage1, wage2, k1, k2)
                                else:
                                    self.changeJob(b, a, False, jobTown2, wage2, wage1, k2, k1)
                                    
                        # Situation 4     
                        elif ( a.house.town == jobTown1 and jobTown1 != jobTown2 ):
                            # In this case, two changes to the status quo are possible: A accepts and B refuses or vice-versa
                            # Case 1: A accepts and B refuses: no relocation needed in this case
                            rc = 0
                            expectedHouseholdIncome = (wage1 + b.marketWage)*self.p['weeklyHours']
                            netIncome1 = expectedHouseholdIncome - rc
                            # Case 2: B accepts and a A refuses
                            rc = relocationCost
                            expectedHouseholdIncome = (wage2 + a.marketWage)*self.p['weeklyHours']
                            netIncome2 = expectedHouseholdIncome - rc
                            bestIncome = max(netIncome1, netIncome2)
                        
                            if bestIncome > resWage:
                                if ( netIncome1 > netIncome2):
                                    self.changeJob(a, b, False, jobTown1, wage1, wage2, k1, k2)
                                else:
                                    self.changeJob(b, a, False, jobTown2, wage2, wage1, k2, k1)
                        
                        # Situation 5
                        elif ( a.house.town == jobTown1 and jobTown1 == jobTown2 ):
                            # In this case, the offers are in the same town, so no relocation is needed
                            rc = 0
                            # Case 1: both accept
                            expectedHouseholdIncome = (wage1 + wage2)*self.p['weeklyHours']
                            netIncome1 = expectedHouseholdIncome - rc
                            # Case 2: A accepts and B refuses
                            expectedHouseholdIncome = (wage1 + b.marketWage)*self.p['weeklyHours']
                            netIncome2 = expectedHouseholdIncome - rc
                            #Case 3: A refuses and B accepts
                            expectedHouseholdIncome = (wage2 + a.marketWage)*self.p['weeklyHours']
                            netIncome3 = expectedHouseholdIncome - rc
                            
                            bestIncome = max(netIncome1, netIncome2, netIncome3)
                            if bestIncome > resWage:
                                if ( bestIncome == netIncome1 ):
                                    self.changeJob(a, b, True, jobTown1, wage1, wage2, k1, k2)
                                elif ( bestIncome == netIncome2 ):
                                    self.changeJob(a, b, False, jobTown1, wage1, wage2, k1, k2)
                                else:
                                    self.changeJob(b, a, False, jobTown2, wage2, wage1, k2, k1)
                                
            workingPool = [x for x in activePop if x.searchJob == True]
                    
        increaseTenure = [x for x in self.pop.livingPeople if x.status == 'employed' and x.jobChange == False]
        for agent in increaseTenure:
            agent.jobTenure += 1
            
    def updateWork(self, person):
        person.workingTime *= self.p['workDiscountingTime']
        workTime = 0
        if person.status == 'employed':
            workingHours = max(self.p['weeklyHours'] - person.socialWork, 0)
            workTime = workingHours/self.p['weeklyHours']
        person.workingTime += workTime
        k = self.p['incomeFinalLevels'][person.classRank]
        r = self.p['incomeGrowthRate'][person.classRank]
        c = np.log(self.p['incomeInitialLevels'][person.classRank]/k)
        exp = c*math.exp(-1*r*person.workingTime)
        person.marketWage = k*math.exp(exp)
          
    def movingAround(self):
    
        self.jobRelocation()
        self.joiningSpouses()
        self.sizeRelocation()
        self.relocatingPensioners()
        
        for i in self.pop.livingPeople:
            i.movedThisYear = False
            i.yearsInTown += 1
        
    def jobRelocation(self):
        employedPop = [x for x in self.pop.livingPeople if x.status == 'employed']
        for person in employedPop:
            peopleToMove = []
            if person.movedThisYear == True:
                continue
            if person.house.town != person.jobLocation:
                person.movedThisYear = True
                if (person.independentStatus == False):
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
                self.townChanges += 1
                
                self.findNewHouse(peopleToMove, person.jobLocation)
                
                
    
    def joiningSpouses(self):
        
        for person in self.pop.livingPeople:
            partnerJoined = False
            if person.movedThisYear == True:
                continue
            
            # ageClass = person.age / 10       
            # At least one of them needs to be employed to move 
            if ( person.partner != None and person.house != person.partner.house 
                and (person.income + person.partner.income) != 0 ):
                
                partnerJoined = True
                person.movedThisYear = True
                person.partner.movedThisYear = True
                
                # 1st case: both partners living with parents.
                # Find a new home near the highest earning partner
                if (person.independentStatus + person.partner.independentStatus == 0):
                    # person.independentStatus = True
                    # person.partner.independentStatus = True
                    if ( person.income > person.partner.income ):
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
                        b = person.partner
                    else:
                        # person.independentStatus = True
                        a = person.partner
                        b = person
                        
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
                    
                            self.findNewHouse(peopleToMove, destination)
                            continue
                    else:
                        if ( a.income > b.income ):
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
                        if ( person.income > person.partner.income ):
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
                        
            if partnerJoined == True:
                person.independentStatus == True
                person.partner.independentStatus == True
                        
    def sizeRelocation(self):
        for person in self.pop.livingPeople:
            if person.movedThisYear or person.independentStatus == False:
                continue
            actualOccupants = len(person.house.occupants)
            pReloc = self.relocationProb(actualOccupants, 0, person.house.initialOccupants)
            r = random.random()
            if ( r > pReloc ):
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

    def houseProb(self, town, classRank):
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
        probHouses = [i/denProb for i in socialDesirability]
        return (probHouses)
    
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
        unskilled = [x for x in self.pop.livingPeople if x.classRank == 1]
        self.unskilledPop.append(len(unskilled))
        skilled = [x for x in self.pop.livingPeople if x.classRank == 2]
        self.skilledPop.append(len(skilled))
        lowerclass = [x for x in self.pop.livingPeople if x.classRank == 3]
        self.lowerclassPop.append(len(lowerclass))
        middelclass = [x for x in self.pop.livingPeople if x.classRank == 4]
        self.middleclassPop.append(len(middelclass))
        upperclass = [x for x in self.pop.livingPeople if x.classRank == 5]
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
        
        workingPop = [x for x in self.pop.livingPeople if x.age > 24]
        for person in workingPop:
            if person.father != None:
                
                if person.classRank == 2 and person.father.classRank == 1:
                    tally_1to2 += 1
                if person.classRank == 3 and person.father.classRank == 1:
                    tally_1to3 += 1
                if person.classRank == 4 and person.father.classRank == 1:
                    tally_1to4 += 1
                if person.classRank == 5 and person.father.classRank == 1:
                    tally_1to5 += 1
                    
                if person.classRank == 1 and person.father.classRank == 2:
                    tally_2to1 += 1
                if person.classRank == 3 and person.father.classRank == 2:
                    tally_2to3 += 1
                if person.classRank == 4 and person.father.classRank == 2:
                    tally_2to4 += 1
                if person.classRank == 5 and person.father.classRank == 2:
                    tally_2to5 += 1
                    
                if person.classRank == 1 and person.father.classRank == 3:
                    tally_3to1 += 1
                if person.classRank == 2 and person.father.classRank == 3:
                    tally_3to2 += 1
                if person.classRank == 4 and person.father.classRank == 3:
                    tally_3to4 += 1
                if person.classRank == 5 and person.father.classRank == 3:
                    tally_3to5 += 1
                    
                if person.classRank == 1 and person.father.classRank == 4:
                    tally_4to1 += 1
                if person.classRank == 2 and person.father.classRank == 4:
                    tally_4to2 += 1
                if person.classRank == 3 and person.father.classRank == 4:
                    tally_4to3 += 1
                if person.classRank == 5 and person.father.classRank == 4:
                    tally_4to5 += 1
                    
                if person.classRank == 1 and person.father.classRank == 5:
                    tally_5to1 += 1
                if person.classRank == 2 and person.father.classRank == 5:
                    tally_5to2 += 1
                if person.classRank == 3 and person.father.classRank == 5:
                    tally_5to3 += 1
                if person.classRank == 4 and person.father.classRank == 5:
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
        self.map.occupiedHouses = list(set(self.map.occupiedHouses))

        ## Check for overlooked empty houses
        emptyHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        for h in emptyHouses:
            self.map.occupiedHouses.remove(h)
            if (self.p['interactiveGraphics']):
                self.canvas.itemconfig(h.icon, state='hidden')
        
        ## Avg household size (easily calculated by pop / occupied houses)
        households = len(self.map.occupiedHouses)
        self.avgHouseholdSize.append(currentPop / households )
        
        ## Marriages and divorces
        self.numMarriages.append(self.marriageTally)
        self.marriageTally = 0
        self.numDivorces.append(self.divorceTally)            
        self.divorceTally = 0
        
        ####### Social Care Outputs ################################################################
        
        
        ## Care demand calculations: first, what's the basic demand and theoretical supply?
        totalCareDemandHours = 0
        totalCareSupplyHours = 0
        taxPayers = 0
        for person in self.pop.livingPeople:
            totalCareDemandHours += person.hoursDemand
            totalCareSupplyHours += person.hoursSupply
            if person.status == 'employed':
                taxPayers += 1
        
        self.totalCareDemand.append(totalCareDemandHours)
        self.totalCareSupply.append(totalCareSupplyHours)   
        self.numTaxpayers.append(taxPayers)
            
        ## What actually happens to people: do they get the care they need?
        careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
        unmetNeeds = [x.residualNeed for x in careReceivers]
        totalUnmetNeeds = sum(unmetNeeds)
        self.totalUnmetNeed.append(totalUnmetNeeds)   
           
        if totalCareDemandHours == 0:
            networkCareRatio = 0.0
        else:
            networkCareRatio = (totalCareDemandHours - totalUnmetNeeds)/totalCareDemandHours

        ##familyCareRatio = ( totalCareDemandHours - unmetNeed ) / (1.0 * (totalCareDemandHours+0.01))
        self.totalFamilyCare.append(networkCareRatio)   

        taxBurden = ( totalUnmetNeeds * self.p['priceSocialCare'] * 52.18 ) / ( taxPayers * 1.0 )
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
    
    def baseRate(self, bias, cp):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.p['initialClassShares'][i]*math.pow(bias, i)
        baseRate = cp/a
        return (baseRate)
    
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
    
    def computeRelocationsCost(self, agent):
        rcA = math.pow(agent.yearsInTown, self.p['yearsintownSensitivityParam'])
        if ( agent.partner == None ):
            for child in agent.children:
                rcA += math.pow(child.yearsInTown, self.p['yearsintownSensitivityParam'])
        else:
            rcA += math.pow(agent.partner.yearsInTown, self.p['yearsintownSensitivityParam'])
            if agent.sex == 'male':
                previousChildren = np.setdiff1d(agent.children, agent.partner.children)
                for child in previousChildren:
                    rcA += math.pow(child.yearsInTown, self.p['yearsintownSensitivityParam'])
                for child in agent.partner.children:    
                    rcA += math.pow(child.yearsInTown, self.p['yearsintownSensitivityParam'])
            else:
                for child in agent.children:
                    rcA += math.pow(child.yearsInTown, self.p['yearsintownSensitivityParam'])
                previousChildren = np.setdiff1d(agent.partner.children, agent.children)
                for child in previousChildren:
                    rcA += math.pow(child.yearsInTown, self.p['yearsintownSensitivityParam'])
        rcA *= self.p['relocationCostParam']
        return (rcA)
        
    def relocationPropensity(self, rrc):   
        rp = 1/math.exp(self.p['propensityRelocationParam']*rrc)
        return(rp)
        
    def townsProb(self, classRank, town, relProp):
        townDensity = []
        classNumerosity = 0
        for t in self.map.towns:
            h = [x for x in t.houses if len(x.occupants) > 0 and x.occupants[0].classRank == classRank]
            classNumerosity = (float(len(h)) + float(len(t.houses)))/2
            if t != town:
                townDensity.append(classNumerosity*relProp)
            else:
                townDensity.append(classNumerosity)
        sumDensity = sum(townDensity)
        relTownDensity = [i/sumDensity for i in townDensity]
        return(relTownDensity)
        
    def computeWage(self, agent, k):
        # Gompertz Law
        c = np.log(self.p['incomeInitialLevels'][agent.classRank]/k)
        exp = c*math.exp(-1*self.p['incomeGrowthRate'][agent.classRank]*agent.workingTime)
        wage = k*math.exp(exp)
        return (wage)
    
    def unemploymentRate(self, i, j):
        classFactor = self.p['initialUnemployment'][j]
        ageFactor = math.pow(self.p['unemploymentAgeBandParam'], i)
        unemploymentRate = classFactor*ageFactor
        return (unemploymentRate)
    
    def statusQuo(self, agent):
        ehi = 0
        if (agent.status == 'employed'):
            ehi = agent.income
        else:
            ehi = agent.marketWage*self.p['weeklyHours']
        if ( agent.partner != None ):
            if agent.partner.status == 'employed':
                ehi += agent.partner.income
            elif agent.partner.status == 'unemployed':
                ehi += agent.partner.marketWage*self.p['weeklyHours']
        return (ehi)
        
    def changeJob(self, a, b, bothAccept, town, w1, w2, k1, k2):
        if a.status == 'unemployed':
            self.enterWork += 1
        if a.status == 'employed':
            a.jobChange == True
        a.status = 'employed'
        a.marketWage = w1
        a.income = w1*self.p['weeklyHours']
        a.finalIncome = k1
        a.jobLocation = town
        if (bothAccept == True):
            if b.status == 'unemployed':
                self.enterWork += 1
            if b.status == 'employed':
                b.jobChange == True
            b.status = 'employed'
            b.marketWage = w2
            b.income = w2*self.p['weeklyHours']
            b.finalIncome = k2
            b.jobLocation = town
            b.searchJob = False
        elif b != None and bothAccept == False:
            if b.status  == 'employed':
                if ( b.house.town != town ):
                    self.exitWork += 1
                    b.status = 'unemployed'
                    b.marketWage = self.marketWage(b)
                    b.income = 0
                    b.finalIncome = 0
                    b.jobLocation = None
                    b.searchJob = False
                    
    def leaveJob(self, person):
            self.exitWork += 1
            person.status = 'unemployed'
            person.marketWage = self.marketWage(person)
            person.income = 0
            person.finalIncome = 0
            person.jobLocation = None
        
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


    def doGraphs(self):
        """Plot the graphs needed at the end of one run."""

        p1, = pylab.plot(self.times,self.pops,color="red")
        p2, = pylab.plot(self.times,self.numTaxpayers,color="blue")
        pylab.legend([p1, p2], ['Total population', 'Taxpayers'],loc='lower right')
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Number of people')
        pylab.xlabel('Year')
        pylab.savefig('popGrowth.pdf')
        pylab.show()

        
        pylab.plot(self.times,self.avgHouseholdSize,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Average household size')
        pylab.xlabel('Year')
        pylab.savefig('avgHousehold.pdf')
        pylab.show()

##        pylab.plot(self.times,self.numMarriages)
##        pylab.ylabel('Number of marriages')
##        pylab.xlabel('Year')
##        pylab.savefig('numMarriages.pdf')
##
##        pylab.plot(self.times,self.numDivorces)
##        pylab.ylabel('Number of divorces')
##        pylab.xlabel('Year')
##        pylab.savefig('numDivorces.pdf')

        p1, = pylab.plot(self.times,self.totalCareDemand,color="red")
        p2, = pylab.plot(self.times,self.totalCareSupply,color="blue")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.legend([p1, p2], ['Care demand', 'Total theoretical supply'],loc='lower right')
        pylab.ylabel('Total hours per week')
        pylab.xlabel('Year')
        pylab.savefig('totalCareSituation.pdf')
        pylab.show()

        pylab.plot(self.times,self.totalFamilyCare,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of informal social care')
        pylab.xlabel('Year')
        pylab.savefig('informalCare.pdf')
        pylab.show()


        pylab.plot(self.times,self.totalTaxBurden,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Care costs in pounds per taxpayer per year')
        pylab.xlabel('Year')
        pylab.savefig('taxBurden.pdf')
        pylab.show()

        pylab.plot(self.times,self.marriageProp,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of married adult women')
        pylab.xlabel('Year')
        pylab.savefig('marriageProp.pdf')
        pylab.savefig('marriageProp.png')
        pylab.show()   
        
        
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