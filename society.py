# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:40:07 2017

@author: ug4d
"""
import random
import numpy as np
import math

class Population:
    """The population class stores a collection of persons."""
    def __init__ (self, initialPop, startYear, minStartAge, maxStartAge,
                  nc, soc, edu, ics, iu, up, wa, il, fl, gr, wdt, wv):
        self.allPeople = []
        self.livingPeople = []

        for i in range(initialPop/2):
            ageMale = random.randint(minStartAge, maxStartAge)
            ageFemale = ageMale + random.randint(-2,5)
            if ( ageFemale < 24 ):
                ageFemale = 24
            
            mab = self.ageBand(ageMale)
            fab = self.ageBand(ageFemale)
            maleBirthYear = startYear - ageMale
            femaleBirthYear = startYear - ageFemale
            classeRanks = range(nc)
            numClass = np.random.choice(classeRanks, p = ics)
            classRank = numClass
            um = self.unemploymentRate(mab, classRank, iu, up)
            uf = self.unemploymentRate(fab, classRank, iu, up)
            socialClass = soc[numClass]
            eduLevel = edu[numClass]
            
            workingTimeMale = 0
            for i in range(ageMale-wa[numClass]):
                workingTimeMale *= wdt
                workingTimeMale += 1
            workingTimeFemale = 0
            for i in range(ageFemale-wa[numClass]):
                workingTimeFemale *= wdt
                workingTimeFemale += 1
            dK = np.random.normal(0, wv)
            newK = fl[numClass]*math.exp(dK)    
            c = np.math.log(il[numClass]/newK)
            maleWage = newK*np.math.exp(c*np.math.exp(-1*gr[numClass]*workingTimeMale))
            femaleWage = newK*np.math.exp(c*np.math.exp(-1*gr[numClass]*workingTimeFemale))
            maleIncome = maleWage*40.0
            femaleIncome = femaleWage*40.0
            manStatus = 'employed'
            finalIncome = fl[numClass]
            if random.random() < um :
                manStatus = 'unemployed'
                maleIncome = 0
                finalIncome = 0
            yearsInTown = random.randint(0, 10)
            tenure = 1.0
            newMan = Person(None, None, ageMale, maleBirthYear, 'male', manStatus, 
                            None, classRank, socialClass, eduLevel, maleWage, 
                            maleIncome, finalIncome, workingTimeMale, yearsInTown, tenure, 0.02)
            status = 'employed'
            finalIncome = fl[numClass]
            if random.random() < uf and manStatus == 'employed':
                status = 'unemployed'
                femaleIncome = 0
                finalIncome = 0
            yearsInTown = random.randint(0, 10)
            newWoman = Person(None, None, ageFemale, femaleBirthYear, 'female', 
                              status, None, classRank, socialClass, eduLevel, 
                              femaleWage, femaleIncome, finalIncome, workingTimeFemale, yearsInTown, tenure, 0.02)
            
            newMan.independentStatus = True
            newWoman.independentStatus = True

            newMan.partner = newWoman
            newWoman.partner = newMan

            self.allPeople.append(newMan)
            self.livingPeople.append(newMan)
            self.allPeople.append(newWoman)
            self.livingPeople.append(newWoman)

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
    
    def unemploymentRate(self, i, j, iu, up):
        classFactor = iu[j]
        ageFactor = math.pow(up, i)
        unemploymentRate = classFactor*ageFactor
        return (unemploymentRate)
    
class Person:
    """The person class stores information about a person in the sim."""
    counter = 1

    def __init__(self, mother, father, age, birthYear, sex, status, house,
                 classRank, sec, edu, wage, income, finalIncome, workingTime, yit, tenure, ur):
        self.mother = mother
        self.father = father
        self.children = []
        self.age = age
        self.birthdate = birthYear
        self.visitedCarer = False
        self.careNeedLevel = 0
        self.hoursDemand = 0
        self.hoursInformalSupply = 0
        self.hoursFormalSupply = 0
        self.hoursSupply = 0
        self.extraworkCare = 0
        self.hoursFormalSupply = 0
        self.socialWork = 0
        self.workToCare = 0
        self.residualNeed = 0
        self.informalSupplyByKinship = []
        self.formalSupplyByKinship = []
        self.networkSupply = 0
        self.residualInformalSupply = 0
        self.residualFormalSupply = 0
        self.residualSupply = 0
        self.formalCare = 0
        self.informalCare = 0
        self.socialNetwork = []
        self.networkSupplies = []
        self.totalSupply = 0
        self.socialCareProvider = False
        self.babyCarer = False
        self.dead = False
        self.partner = None
        if sex == 'random':
            self.sex = random.choice(['male', 'female'])
        else:
            self.sex = sex
        self.house = house
        self.socialCareMap = []
        self.classRank = classRank
        self.sec = sec
        self.education = edu
        self.wage = wage
        self.income = income
        self.finalIncome = finalIncome
        self.jobOffers = []
        self.workingTime = workingTime
        self.status = status
        self.independentStatus = False
        self.jobLocation = None
        self.searchJob = False
        self.jobChange = False
        self.newTown = None
        self.newK = 0
        self.newWage = 0
        self.unemploymentDuration = 0
        self.jobTenure = tenure
        self.yearsInTown = yit
        self.justMarried = None
        self.unemploymentRate = ur
        # Introducing care needs of babies
        if age < 1:
            self.careRequired = 80
        self.careAvailable = 0
        self.movedThisYear = False
        self.id = Person.counter
        Person.counter += 1
        

        
        
        
        
        