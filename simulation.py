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
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import seaborn as sns
from time import gmtime, strftime
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
        self.socialClassShares = []
        self.careNeedShares = []
        self.jobMarketMap = []
        
        ## Statistical tallies
        self.periodCount = 0

        np.savetxt('dynamicParam.csv', (self.p['pensionWage']+self.p['incomeInitialLevels']+self.p['incomeFinalLevels']+self.p['educationCosts']+self.p['pricePublicSocialCare']+self.p['priceSocialCare']+self.p['incomeCareParamPolicyCoeffcient']+self.p['socialSupportLevelPolicyChange']+self.p['ageOfRetirementPolicyChange']+self.p['educationCostsPolicyCoefficient']), delimiter=',')
        np.savetxt('lengthDynamicParamLists.csv', (len(self.p['pensionWage']), len(self.p['incomeInitialLevels']), len(self.p['incomeFinalLevels']), len(self.p['educationCosts']), len(self.p['pricePublicSocialCare']), len(self.p['priceSocialCare']), len(self.p['incomeCareParamPolicyCoeffcient']), len(self.p['socialSupportLevelPolicyChange']), len(self.p['ageOfRetirementPolicyChange']), len(self.p['educationCostsPolicyCoefficient'])), delimiter=',')
        
        ###################### Demographic outputs ###################
        self.agent = None
        
        self.times = []
        self.pops = []
        self.householdsList = []
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
        
        self.socialMobility_1to1 = []
        self.socialMobility_1to2 = []
        self.socialMobility_1to3 = []
        self.socialMobility_1to4 = []
        self.socialMobility_1to5 = []
        self.socialMobility_2to1 = []
        self.socialMobility_2to2 = []
        self.socialMobility_2to3 = []
        self.socialMobility_2to4 = []
        self.socialMobility_2to5 = []
        self.socialMobility_3to1 = []
        self.socialMobility_3to2 = []
        self.socialMobility_3to3 = []
        self.socialMobility_3to4 = []
        self.socialMobility_3to5 = []
        self.socialMobility_4to1 = []
        self.socialMobility_4to2 = []
        self.socialMobility_4to3 = []
        self.socialMobility_4to4 = []
        self.socialMobility_4to5 = []
        self.socialMobility_5to1 = []
        self.socialMobility_5to2 = []
        self.socialMobility_5to3 = []
        self.socialMobility_5to4 = []
        self.socialMobility_5to5 = []
        
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
        self.shareCareGivers = []
        self.shareCareGivers_1 = []
        self.shareCareGivers_2 = []
        self.shareCareGivers_3 = []
        self.shareCareGivers_4 = []
        self.shareCareGivers_5 = []
        self.shareSocialCareTakers_N1 = []
        self.shareSocialCareTakers_N2 = []
        self.shareSocialCareTakers_N3 = []
        self.shareSocialCareTakers_N4 = []
        self.totalCareDemand = []
        self.perCapitaCareDemand = []
        self.perCapitaSocialCareDemand = []
        self.perCapitaChildCareDemand = []
        self.totalChildCareDemand = []
        self.totalSocialCareDemand = []
        self.shareSocialCareDemand = []
        
        self.totalCareSupply = []
        self.totalInformalCareSupply = []
        self.totalFormalCareSupply = []
        self.shareInformalCareSupply = []
        
        self.totalInformalCareReceived = []
        self.totalFormalCareReceived = []
        self.totalCareReceived = []
        self.averageCareReceived = []
        self.averageInformalCareReceived = []
        self.averageFormalCareReceived = []
        self.averageCareSupplied = []
        self.averageInformalCareSupplied = []
        self.averageFormalCareSupplied = []
        self.shareInformalCareReceived = []
        self.totalUnmetCareDemand = []
        self.shareUnmetCareDemand = []
        self.perCapitaUnmetCareDemand = []
        
        self.averageUnmetCareDemand = []
        
        self.totalInformalSocialCareReceived = []
        self.totalFormalSocialCareReceived = []
        self.totalSocialCareReceived = [] 
        self.averageSocialCareReceived = []
        self.averageInformalSocialCareReceived = []
        self.averageFormalSocialCareReceived = []
        self.averageSocialCareSupplied = []
        self.averageInformalSocialCareSupplied = []
        self.averageFormalSocialCareSupplied = []
        self.shareInformalSocialCareReceived = []
        self.totalSocialCareUnmetDemand = [] 
        self.shareUnmetSocialCareDemand = []
        self.perCapitaUnmetSocialCareDemand = []
        
        self.averageUnmetSocialCareDemand = []
        
        self.totalInformalChildCareReceived = []
        self.totalFormalChildCareReceived = []
        self.totalChildCareReceived = [] 
        self.averageChildCareReceived = []
        self.averageInformalChildCareReceived = []
        self.averageFormalChildCareReceived = []
        self.averageChildCareSupplied = []
        self.averageInformalChildCareSupplied = []
        self.averageFormalChildCareSupplied = []
        self.shareInformalChildCareReceived = []
        self.totalChildCareUnmetDemand = [] 
        self.shareUnmetChildCareDemand = []
        self.perCapitaUnmetChildCareDemand = []
        self.averageUnmetChildCareDemand = []
        
        self.perCapitaCareReceived = []
        self.perCapitaSocialCareReceived = []
        self.perCapitaChildCareReceived = []
        
        self.totalInformalCareSuppliedMale = [] 
        self.totalInformalCareSuppliedMale_1 = [] 
        self.totalInformalCareSuppliedMale_2 = [] 
        self.totalInformalCareSuppliedMale_3 = [] 
        self.totalInformalCareSuppliedMale_4 = []
        self.totalInformalCareSuppliedMale_5 = [] 
        self.totalInformalCareSuppliedFemale = [] 
        self.totalInformalCareSuppliedFemale_1 = [] 
        self.totalInformalCareSuppliedFemale_2 = [] 
        self.totalInformalCareSuppliedFemale_3 = [] 
        self.totalInformalCareSuppliedFemale_4 = [] 
        self.totalInformalCareSuppliedFemale_5 = [] 
        self.shareFemaleInformalCareSupplied = []
        self.shareFemaleInformalCareSupplied_1 = []
        self.shareFemaleInformalCareSupplied_2 = []
        self.shareFemaleInformalCareSupplied_3 = []
        self.shareFemaleInformalCareSupplied_4 = []
        self.shareFemaleInformalCareSupplied_5 = []
        
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
        self.shareSocialCare_1 = []
        self.totalInformalCarePerRecipient_1 = []
        self.totalFormalCarePerRecipient_1 = []
        self.totalUnmetNeedPerRecipient_1 = []
        self.totalInformalCarePerCarer_1 = []
        self.totalFormalCarePerCarer_1 = []
        self.shareInformalSupply_1 = []
        self.shareUnmetCareDemand_1 = []
        self.perCapitaUnmetCareDemand_1 = []
        
        self.totalInformalSupply_2 = []
        self.totalFormalSupply_2 = []
        self.shareSocialCare_2 = []
        self.totalInformalCarePerRecipient_2 = []
        self.totalFormalCarePerRecipient_2 = []
        self.totalUnmetNeedPerRecipient_2 = []
        self.totalInformalCarePerCarer_2 = []
        self.totalFormalCarePerCarer_2 = []
        self.shareInformalSupply_2 = []
        self.shareUnmetCareDemand_2 = []
        self.perCapitaUnmetCareDemand_2 = []
        
        self.totalInformalSupply_3 = []
        self.totalFormalSupply_3 = []
        self.shareSocialCare_3 = []
        self.totalInformalCarePerRecipient_3 = []
        self.totalFormalCarePerRecipient_3 = []
        self.totalUnmetNeedPerRecipient_3 = []
        self.totalInformalCarePerCarer_3 = []
        self.totalFormalCarePerCarer_3 = []
        self.shareInformalSupply_3 = []
        self.shareUnmetCareDemand_3 = []
        self.perCapitaUnmetCareDemand_3 = []
        
        self.totalInformalSupply_4 = []
        self.totalFormalSupply_4 = []
        self.shareSocialCare_4 = []
        self.totalInformalCarePerRecipient_4 = []
        self.totalFormalCarePerRecipient_4 = []
        self.totalUnmetNeedPerRecipient_4 = []
        self.totalInformalCarePerCarer_4 = []
        self.totalFormalCarePerCarer_4 = []
        self.shareInformalSupply_4 = []
        self.shareUnmetCareDemand_4 = []
        self.perCapitaUnmetCareDemand_4 = []
        
        self.totalInformalSupply_5 = []
        self.totalFormalSupply_5 = []
        self.shareSocialCare_5 = []
        self.totalInformalCarePerRecipient_5 = []
        self.totalFormalCarePerRecipient_5 = []
        self.totalUnmetNeedPerRecipient_5 = []
        self.totalInformalCarePerCarer_5 = []
        self.totalFormalCarePerCarer_5 = []
        self.shareInformalSupply_5 = []
        self.shareUnmetCareDemand_5 = []
        self.perCapitaUnmetCareDemand_5 = []
        
        self.averageCareSupply = []
        self.ratio_UnmetCareDemand_Supply = []
        
        self.totalCareSupply_1 = []
        self.averageCareSupply_1 = []
        self.ratio_UnmetCareDemand_Supply_1 = []
        self.totalSocialInformalCareSupply_1 = []
        self.totalSocialFormalCareSupply_1 = []
        self.totalUnmetSocialCareDemand_1 = []
        self.totalChildInformalCareSupply_1 = []
        self.totalChildFormalCareSupply_1 = []
        self.totalUnmetChildCareDemand_1 = []
        self.averageSocialInformalCareSupply_1 = []
        self.averageSocialFormalCareSupply_1 = []
        self.averageUnmetSocialCareDemand_1 = []
        self.averageChildInformalCareSupply_1 = []
        self.averageChildFormalCareSupply_1 = []
        self.averageUnmetChildCareDemand_1 = []
        
        self.totalCareSupply_2 = []
        self.averageCareSupply_2 = []
        self.ratio_UnmetCareDemand_Supply_2 = []
        self.totalSocialInformalCareSupply_2 = []
        self.totalSocialFormalCareSupply_2 = []
        self.totalUnmetSocialCareDemand_2 = []
        self.totalChildInformalCareSupply_2 = []
        self.totalChildFormalCareSupply_2 = []
        self.totalUnmetChildCareDemand_2 = []
        self.averageSocialInformalCareSupply_2 = []
        self.averageSocialFormalCareSupply_2 = []
        self.averageUnmetSocialCareDemand_2 = []
        self.averageChildInformalCareSupply_2 = []
        self.averageChildFormalCareSupply_2 = []
        self.averageUnmetChildCareDemand_2 = []
        
        self.totalCareSupply_3 = []
        self.averageCareSupply_3 = []
        self.ratio_UnmetCareDemand_Supply_3 = []
        self.totalSocialInformalCareSupply_3 = []
        self.totalSocialFormalCareSupply_3 = []
        self.totalUnmetSocialCareDemand_3 = []
        self.totalChildInformalCareSupply_3 = []
        self.totalChildFormalCareSupply_3 = []
        self.totalUnmetChildCareDemand_3 = []
        self.averageSocialInformalCareSupply_3 = []
        self.averageSocialFormalCareSupply_3 = []
        self.averageUnmetSocialCareDemand_3 = []
        self.averageChildInformalCareSupply_3 = []
        self.averageChildFormalCareSupply_3 = []
        self.averageUnmetChildCareDemand_3 = []
        
        self.totalCareSupply_4 = []
        self.averageCareSupply_4 = []
        self.ratio_UnmetCareDemand_Supply_4 = []
        self.totalSocialInformalCareSupply_4 = []
        self.totalSocialFormalCareSupply_4 = []
        self.totalUnmetSocialCareDemand_4 = []
        self.totalChildInformalCareSupply_4 = []
        self.totalChildFormalCareSupply_4 = []
        self.totalUnmetChildCareDemand_4 = []
        self.averageSocialInformalCareSupply_4 = []
        self.averageSocialFormalCareSupply_4 = []
        self.averageUnmetSocialCareDemand_4 = []
        self.averageChildInformalCareSupply_4 = []
        self.averageChildFormalCareSupply_4 = []
        self.averageUnmetChildCareDemand_4 = []
        
        self.totalCareSupply_5 = []
        self.averageCareSupply_5 = []
        self.ratio_UnmetCareDemand_Supply_5 = []
        self.totalSocialInformalCareSupply_5 = []
        self.totalSocialFormalCareSupply_5 = []
        self.totalUnmetSocialCareDemand_5 = []
        self.totalChildInformalCareSupply_5 = []
        self.totalChildFormalCareSupply_5 = []
        self.totalUnmetChildCareDemand_5 = []
        self.averageSocialInformalCareSupply_5 = []
        self.averageSocialFormalCareSupply_5 = []
        self.averageUnmetSocialCareDemand_5 = []
        self.averageChildInformalCareSupply_5 = []
        self.averageChildFormalCareSupply_5 = []
        self.averageUnmetChildCareDemand_5 = []
        
        self.shareInformalSocialSupply_1 = []
        self.shareUnmetSocialSupply_1 = []
        self.shareInformalChildSupply_1 = []
        self.shareUnmetChildSupply_1 = []
        
        self.shareInformalSocialSupply_2 = []
        self.shareUnmetSocialSupply_2 = []
        self.shareInformalChildSupply_2 = []
        self.shareUnmetChildSupply_2 = []
        
        self.shareInformalSocialSupply_3 = []
        self.shareUnmetSocialSupply_3 = []
        self.shareInformalChildSupply_3 = []
        self.shareUnmetChildSupply_3 = []
        
        self.shareInformalSocialSupply_4 = []
        self.shareUnmetSocialSupply_4 = []
        self.shareInformalChildSupply_4 = []
        self.shareUnmetChildSupply_4 = []
        
        self.shareInformalSocialSupply_5 = []
        self.shareUnmetSocialSupply_5 = []
        self.shareInformalChildSupply_5 = []
        self.shareUnmetChildSupply_5 = []
        
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
        
        self.unmetSocialCareNeedGiniCoefficient = []
        self.unmetSocialCareNeedGiniCoefficient_1 = []
        self.unmetSocialCareNeedGiniCoefficient_2 = []
        self.unmetSocialCareNeedGiniCoefficient_3 = []
        self.unmetSocialCareNeedGiniCoefficient_4 = []
        self.unmetSocialCareNeedGiniCoefficient_5 = []
        
        self.shareUnmetSocialCareNeedGiniCoefficient = []
        self.shareUnmetSocialCareNeedGiniCoefficient_1 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_2 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_3 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_4 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_5 = []
        
        self.unmetSocialCareNeedDistribution = []
        self.unmetSocialCareNeedDistribution_1 = []
        self.unmetSocialCareNeedDistribution_2 = []
        self.unmetSocialCareNeedDistribution_3 = []
        self.unmetSocialCareNeedDistribution_4 = []
        self.unmetSocialCareNeedDistribution_5 = []
        
        self.shareUnmetSocialCareNeedDistribution = []
        self.shareUnmetSocialCareNeedDistribution_1 = []
        self.shareUnmetSocialCareNeedDistribution_2 = []
        self.shareUnmetSocialCareNeedDistribution_3 = []
        self.shareUnmetSocialCareNeedDistribution_4 = []
        self.shareUnmetSocialCareNeedDistribution_5 = []
        
        ########################### Economic outputs ######################
        
        self.totalEmployment = []
        self.totalEmployment_1 = []
        self.totalEmployment_2 = []
        self.totalEmployment_3 = []
        self.totalEmployment_4 = []
        self.totalEmployment_5 = []
        
        self.totalJobChanges = []
        self.popHourlyWages = []
        
        self.averageWage_M = []
        self.averageWage_F = []
        self.ratioWomenMaleWage = []
        self.averageWage_1 = []
        self.averageWage_1_Males = []
        self.averageWage_1_Females = []
        self.ratioWomenMaleWage_1 = []
        self.averageWage_2 = []
        self.averageWage_2_Males = []
        self.averageWage_2_Females = []
        self.ratioWomenMaleWage_2 = []
        self.averageWage_3 = []
        self.averageWage_3_Males = []
        self.averageWage_3_Females = []
        self.ratioWomenMaleWage_3 = []
        self.averageWage_4 = []
        self.averageWage_4_Males = []
        self.averageWage_4_Females = []
        self.ratioWomenMaleWage_4 = []
        self.averageWage_5 = []
        self.averageWage_5_Males = []
        self.averageWage_5_Females = []
        self.ratioWomenMaleWage_5 = []
        
        self.averageIncome_M = []
        self.averageIncome_F = []
        self.ratioWomenMaleIncome = []
        self.averageIncome_1 = []
        self.averageIncome_1_Males = []
        self.averageIncome_1_Females = []
        self.ratioWomenMaleIncome_1 = []
        self.averageIncome_2 = []
        self.averageIncome_2_Males = []
        self.averageIncome_2_Females = []
        self.ratioWomenMaleIncome_2 = []
        self.averageIncome_3 = []
        self.averageIncome_3_Males = []
        self.averageIncome_3_Females = []
        self.ratioWomenMaleIncome_3 = []
        self.averageIncome_4 = []
        self.averageIncome_4_Males = []
        self.averageIncome_4_Females = []
        self.ratioWomenMaleIncome_4 = []
        self.averageIncome_5 = []
        self.averageIncome_5_Males = []
        self.averageIncome_5_Females = []
        self.ratioWomenMaleIncome_5 = []
        
        ########################## Mobility outputs ######################
        
        self.totalRelocations = 0
        self.numberRelocations = []
        self.jobRelocations_1 = 0
        self.jobRelocations_2 = 0
        self.jobRelocations_3 = 0
        self.jobRelocations_4 = 0
        self.jobRelocations_5 = 0
        self.numJobRelocations_1 = []
        self.numJobRelocations_2 = []
        self.numJobRelocations_3 = []
        self.numJobRelocations_4 = []
        self.numJobRelocations_5 = []
        self.marriageRelocations = 0
        self.numMarriageRelocations = []
        self.sizeRelocations = 0
        self.numSizeRelocations = []
        self.retiredRelocations = 0
        self.numRetiredRelocations = []
        self.townChanges = 0
        self.numberTownChanges = []
        
        ######################## Other outputs #############################
        self.aggregateQALY = []
        self.averageQALY = []
        self.discountedQALY = []
        self.averageDiscountedQALY = []
        self.publicSocialCareSupply = []
        self.numTaxpayers = []
        self.totalUnmetNeed = []
        self.totalFamilyCare = []
        self.totalTaxBurden = []
        self.healthCareCost = []
        self.perCapitaHealthCareCost = []
        
        self.enterWork = []
        self.exitWork = []
        self.changeWork = []
        
        ############   Sensitivity Outputs   #######
        
        self.sharesUnmetCare_M = []
        self.sharesUnmetCare_SD = []
        self.averagesUnmetCare_M = []
        self.averagesUnmetCare_SD = []
        self.qualityAdjustedLifeYears_M = []
        self.qualityAdjustedLifeYears_SD = []
        self.perCapitaQualityAdjustedLifeYears_M = []
        self.perCapitaQualityAdjustedLifeYears_SD = []
        self.perCapitaHospitalizationCost_M = []
        self.perCapitaHospitalizationCost_SD = []
        self.sharesSocialCare_M = []
        self.sharesSocialCare_SD = []
        self.sharesInformalCare_M = []
        self.sharesInformalCare_SD = []
        
        # Check variables
        # self.deathProb = []
        # self.careLevel = []
        self.perCapitaHouseholdIncome = []
        self.socialCareMapValues = []
        self.relativeEducationCost = []
        self.probKeepStudying = []
        self.stageStudent = []
        self.changeJobRate = []
        self.changeJobdIncome = []
        self.relocationCareLoss = []
        self.relocationCost = []
        self.townRelocationAttraction = []
        self.townRelativeAttraction = []
        self.townsJobProb = []
        self.townJobAttraction = []
        self.unemployedIncomeDiscountingFactor = []
        self.relativeTownAttraction = []
        self.houseScore = []
        self.deltaHouseOccupants = []
        
        # Counters and storage
        
        self.pensionWage = []
        self.incomeInitialLevels = []
        self.incomeFinalLevels = []
        self.pricePublicSocialCare = 0
        self.priceSocialCare = 0    
        self.check = False
        self.exitWork = 0
        self.enterWork = 0
        self.publicSupply = 0
        self.hospitalizationCost = 0
        self.year = self.p['startYear']
        self.pyramid = PopPyramid(self.p['num5YearAgeClasses'],
                                  self.p['numCareLevels'])
        self.textUpdateList = []
        
        self.inputsMortality = []
        self.outputMortality = []
        self.regressionModels_M = []
        
        self.inputsFertility = []
        self.outputFertility = []
        self.regressionModels_F = []
        
        self.unemploymentRateClasses = []
        self.meanUnemploymentRates = []

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
        
        self.parameters = map(list, zip(*self.parameters))
         # Create a list of combinations
        combinations = []
        defaultValues = [self.p['incomeCareParamPolicyCoeffcient'][0], self.p['socialSupportLevelPolicyChange'][0], self.p['ageOfRetirementPolicyChange'][0], self.p['educationCostsPolicyCoefficient'][0]]
        for i in range(len(self.parameters)):
            for j in range(2):
                runParameters = [x for x in defaultValues]
                runParameters[i] = self.parameters[i][j]
                combinations.append(runParameters)
                
        folder_S  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\\Charts II\SensitivityCharts'
        if not os.path.isdir(os.path.dirname(folder_S)):
            os.makedirs(folder_S)
            
        
        for r in range(len(combinations)): # 
            
            # Reset the parameters that have changed (add the policy parameters)
            g = np.genfromtxt('dynamicParam.csv', skip_header = 0, delimiter=',')
            n = np.genfromtxt('lengthDynamicParamLists.csv', skip_header = 0, delimiter=',')
    
            k = []
            i = 0
            for j in range(len(n)):
                h = i + int(n[j])
                k.append(g[i:h])
                i += int(n[j])
        
            self.p['pensionWage'] = k[0]
            self.p['incomeInitialLevels'] = k[1]
            self.p['incomeFinalLevels'] = k[2]
            self.p['educationCosts'] = k[3]
            self.p['pricePublicSocialCare'] = k[4][0]
            self.p['priceSocialCare'] = k[5][0]
            
            # Add these in the saved files
            self.p['incomeCareParamPolicyCoeffcient'] = k[6][0] # Default = 0.01
            self.p['socialSupportLevelPolicyChange'] = k[7][0] # Default = 0.0005
            self.p['ageOfRetirementPolicyChange'] = k[8][0] # Default = 2.0
            self.p['educationCostsPolicyCoefficient'] = k[9][0] # 
            
            #self.emptyTimeSeries()
            
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            print('Run: ' + str(r))

            
            folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\\Charts II\Run_' + str(r)
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            
            random.seed(self.p['favouriteSeed'])
            
            
            #self.p['propensityRelocationParam'] = 20.0 # combinations[r][5] Default = 20.0
    
            filename = folder + '/parameterValues.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))
            # values = zip(np.array(combinations[r]))
            #print(self.p['incomeCareParam']*combinations[r][0])
            values = zip(np.array([self.p['incomeCareParam']*combinations[r][0], self.p['socialSupportLevel']+combinations[r][1], self.p['ageOfRetirement']+combinations[r][2],
                         self.p['educationCosts'][0]*combinations[r][3], self.p['educationCosts'][1]*combinations[r][3], self.p['educationCosts'][2]*combinations[r][3], 
                         self.p['educationCosts'][3]*combinations[r][3]]))
            names = ('incomeCareParam, socialSupportLevel, ageOfRetirement, educationCosts_II, educationCosts_III, educationCosts_IV, educationCosts_V')
            np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="") 
            
            self.initializePop()
            
            if self.p['interactiveGraphics']:
                self.initializeCanvas()
            
            
            for self.year in range(self.p['startYear'], self.p['endYear']+1):
                
                print(" ")
                print(self.year)
                
                if self.year == self.p['implementPoliciesFromYear']:
                    
                    # 1 - dump all prices and agents on pickle
                    
                    # 2 - start parameter combinations' loop from here
                    
                        # 3 - load all prices and agents from pickle
                    
                        # 4 - load policies' parameters
                    
                    self.p['incomeCareParamPolicyCoeffcient'] = combinations[r][0] # Default = 0.01
                    print(self.p['incomeCareParamPolicyCoeffcient'])
                    self.p['socialSupportLevelPolicyChange'] = combinations[r][1] # Default = 0.0005
                    self.p['ageOfRetirementPolicyChange'] = combinations[r][2] # Default = 2.0
                    self.p['educationCostsPolicyCoefficient'] = combinations[r][3] # Default = 2.0
                
                self.doOneYear()
                self.periodCount += 1
                if self.year == self.p['thePresent']:
                    random.seed()
            
    
            ###### Create csv with all the outputs   ############
            values = zip(self.pops,self.unskilledPop,self.skilledPop,self.lowerclassPop,self.middleclassPop,
                         self.upperclassPop,self.numberHouseholds,self.numberHouseholds_1,self.numberHouseholds_2,
                         self.numberHouseholds_3,self.numberHouseholds_4,self.numberHouseholds_5,self.avgHouseholdSize,
                         self.avgHouseholdSize_1,self.avgHouseholdSize_2,self.avgHouseholdSize_3,self.avgHouseholdSize_4,
                         self.avgHouseholdSize_5,self.marriageProp,self.numMarriages,self.numDivorces,self.totalCareDemand,
                         self.perCapitaCareDemand,self.perCapitaSocialCareDemand,self.perCapitaChildCareDemand,
                         self.totalChildCareDemand,self.totalSocialCareDemand,self.shareSocialCareDemand,
                         self.totalCareSupply,self.totalInformalCareSupply,self.totalFormalCareSupply,self.shareInformalCareSupply,
                         self.totalInformalCareReceived,self.totalFormalCareReceived,self.totalCareReceived,self.averageCareReceived,
                         self.averageInformalCareReceived,self.averageFormalCareReceived,self.averageCareSupplied,
                         self.averageInformalCareSupplied,self.averageFormalCareSupplied,self.shareInformalCareReceived,
                         self.totalUnmetCareDemand,self.shareUnmetCareDemand,self.perCapitaUnmetCareDemand,self.averageUnmetCareDemand,
                         self.totalInformalSocialCareReceived,self.totalFormalSocialCareReceived,self.totalSocialCareReceived,
                         self.averageSocialCareReceived,self.averageInformalSocialCareReceived,self.averageFormalSocialCareReceived,
                         self.averageSocialCareSupplied,self.averageInformalSocialCareSupplied,self.averageFormalSocialCareSupplied,
                         self.shareInformalSocialCareReceived,self.totalSocialCareUnmetDemand ,self.shareUnmetSocialCareDemand,
                         self.perCapitaUnmetSocialCareDemand,self.averageUnmetSocialCareDemand,self.totalInformalChildCareReceived,
                         self.totalFormalChildCareReceived,self.totalChildCareReceived ,self.averageChildCareReceived,
                         self.averageInformalChildCareReceived,self.averageFormalChildCareReceived,self.averageChildCareSupplied,
                         self.averageInformalChildCareSupplied,self.averageFormalChildCareSupplied,self.shareInformalChildCareReceived,
                         self.totalChildCareUnmetDemand,self.shareUnmetChildCareDemand,self.perCapitaUnmetChildCareDemand,
                         self.averageUnmetChildCareDemand,self.totalInformalCareSuppliedMale,self.totalInformalCareSuppliedMale_1,
                         self.totalInformalCareSuppliedMale_2,self.totalInformalCareSuppliedMale_3,self.totalInformalCareSuppliedMale_4,
                         self.totalInformalCareSuppliedMale_5,self.totalInformalCareSuppliedFemale,self.totalInformalCareSuppliedFemale_1,
                         self.totalInformalCareSuppliedFemale_2,self.totalInformalCareSuppliedFemale_3,self.totalInformalCareSuppliedFemale_4,
                         self.totalInformalCareSuppliedFemale_5,self.shareFemaleInformalCareSupplied,self.shareFemaleInformalCareSupplied_1,
                         self.shareFemaleInformalCareSupplied_2,self.shareFemaleInformalCareSupplied_3,self.shareFemaleInformalCareSupplied_4,
                         self.shareFemaleInformalCareSupplied_5,self.totalCareDemand_1,self.totalCareSupply_1,self.totalUnmetDemand_1,
                         self.totalCareDemand_2,self.totalCareSupply_2,self.totalUnmetDemand_2,self.totalCareDemand_3,self.totalCareSupply_3,
                         self.totalUnmetDemand_3,self.totalCareDemand_4,self.totalCareSupply_4,self.totalUnmetDemand_4,self.totalCareDemand_5,
                         self.totalCareSupply_5,self.totalUnmetDemand_5,self.shareSocialCare_1,self.totalInformalSupply_1,self.totalFormalSupply_1,
                         self.totalInformalCarePerRecipient_1,self.totalFormalCarePerRecipient_1,self.totalUnmetNeedPerRecipient_1,
                         self.totalInformalCarePerCarer_1,self.totalFormalCarePerCarer_1,self.shareInformalSupply_1,self.shareUnmetCareDemand_1,
                         self.perCapitaUnmetCareDemand_1,self.shareSocialCare_2,self.totalInformalSupply_2,self.totalFormalSupply_2,
                         self.totalInformalCarePerRecipient_2,self.totalFormalCarePerRecipient_2,self.totalUnmetNeedPerRecipient_2,
                         self.totalInformalCarePerCarer_2,self.totalFormalCarePerCarer_2,self.shareInformalSupply_2,self.shareUnmetCareDemand_2,
                         self.perCapitaUnmetCareDemand_2,self.shareSocialCare_3,self.totalInformalSupply_3,self.totalFormalSupply_3,
                         self.totalInformalCarePerRecipient_3,self.totalFormalCarePerRecipient_3,
                         self.totalUnmetNeedPerRecipient_3,self.totalInformalCarePerCarer_3,self.totalFormalCarePerCarer_3,self.shareSocialCare_4,
                         self.shareInformalSupply_3,self.shareUnmetCareDemand_3,self.perCapitaUnmetCareDemand_3,self.totalInformalSupply_4,
                         self.totalFormalSupply_4,self.totalInformalCarePerRecipient_4,self.totalFormalCarePerRecipient_4,
                         self.totalUnmetNeedPerRecipient_4,self.totalInformalCarePerCarer_4,self.totalFormalCarePerCarer_4,
                         self.shareInformalSupply_4,self.shareUnmetCareDemand_4,self.perCapitaUnmetCareDemand_4,self.shareSocialCare_5,
                         self.totalInformalSupply_5,self.totalFormalSupply_5,self.totalInformalCarePerRecipient_5,self.totalFormalCarePerRecipient_5,
                         self.totalUnmetNeedPerRecipient_5,self.totalInformalCarePerCarer_5,self.totalFormalCarePerCarer_5,
                         self.shareInformalSupply_5,self.shareUnmetCareDemand_5,self.perCapitaUnmetCareDemand_5,self.totalSupplyHousehold,
                         self.totalSupplyNoK_1,self.totalSupplyNoK_2,self.totalSupplyNoK_3,self.totalInformalSupplyHousehold,
                         self.totalInformalSupplyNoK_1,self.totalInformalSupplyNoK_2,self.totalInformalSupplyNoK_3,self.totalFormalSupplyHousehold,
                         self.totalFormalSupplyNoK_1,self.totalFormalSupplyNoK_2,self.totalFormalSupplyNoK_3,self.totalEmployment,
                         self.totalEmployment_1,self.totalEmployment_2,self.totalEmployment_3,self.totalEmployment_4,self.totalEmployment_5,
                         self.totalJobChanges,self.averageIncome_M,self.averageIncome_F,self.averageIncome_1,self.averageIncome_1_Males,
                         self.averageIncome_1_Females,self.averageIncome_2,self.averageIncome_2_Males,self.averageIncome_2_Females,
                         self.averageIncome_3,self.averageIncome_3_Males,self.averageIncome_3_Females,self.averageIncome_4,
                         self.averageIncome_4_Males,self.averageIncome_4_Females,self.averageIncome_5,self.averageIncome_5_Males,
                         self.averageIncome_5_Females,self.numberRelocations,self.numJobRelocations_1,self.numJobRelocations_2,
                         self.numJobRelocations_3,self.numJobRelocations_4,self.numJobRelocations_5,self.numMarriageRelocations,
                         self.numSizeRelocations,self.numRetiredRelocations,self.numberTownChanges)
                         
            names = ('pops,unskilledPop,skilledPop,lowerclassPop,middleclassPop, '
                     'upperclassPop,numberHouseholds,numberHouseholds_1,numberHouseholds_2, '
                     'numberHouseholds_3,numberHouseholds_4,numberHouseholds_5,avgHouseholdSize, '
                     'avgHouseholdSize_1,avgHouseholdSize_2,avgHouseholdSize_3,avgHouseholdSize_4, '
                     'avgHouseholdSize_5,marriageProp,numMarriages,numDivorces,totalCareDemand, '
                     'perCapitaCareDemand,perCapitaSocialCareDemand,perCapitaChildCareDemand, '
                     'totalChildCareDemand,totalSocialCareDemand,shareSocialCareDemand, '
                     'totalCareSupply,totalInformalCareSupply,totalFormalCareSupply,shareInformalCareSupply, '
                     'totalInformalCareReceived,totalFormalCareReceived,totalCareReceived,averageCareReceived, '
                     'averageInformalCareReceived,averageFormalCareReceived,averageCareSupplied, '
                     'averageInformalCareSupplied,averageFormalCareSupplied,shareInformalCareReceived, '
                     'totalUnmetCareDemand,shareUnmetCareDemand,perCapitaUnmetCareDemand,averageUnmetCareDemand, '
                     'totalInformalSocialCareReceived,totalFormalSocialCareReceived,totalSocialCareReceived, '
                     'averageSocialCareReceived,averageInformalSocialCareReceived,averageFormalSocialCareReceived, '
                     'averageSocialCareSupplied,averageInformalSocialCareSupplied,averageFormalSocialCareSupplied, '
                     'shareInformalSocialCareReceived,totalSocialCareUnmetDemand ,shareUnmetSocialCareDemand, '
                     'perCapitaUnmetSocialCareDemand,averageUnmetSocialCareDemand,totalInformalChildCareReceived, '
                     'totalFormalChildCareReceived,totalChildCareReceived ,averageChildCareReceived, '
                     'averageInformalChildCareReceived,averageFormalChildCareReceived,averageChildCareSupplied, '
                     'averageInformalChildCareSupplied,averageFormalChildCareSupplied,shareInformalChildCareReceived, '
                     'totalChildCareUnmetDemand,shareUnmetChildCareDemand,perCapitaUnmetChildCareDemand, '
                     'averageUnmetChildCareDemand,totalInformalCareSuppliedMale,totalInformalCareSuppliedMale_1, '
                     'totalInformalCareSuppliedMale_2,totalInformalCareSuppliedMale_3,totalInformalCareSuppliedMale_4, '
                     'totalInformalCareSuppliedMale_5,totalInformalCareSuppliedFemale,totalInformalCareSuppliedFemale_1, '
                     'totalInformalCareSuppliedFemale_2,totalInformalCareSuppliedFemale_3,totalInformalCareSuppliedFemale_4, '
                     'totalInformalCareSuppliedFemale_5,shareFemaleInformalCareSupplied,shareFemaleInformalCareSupplied_1, '
                     'shareFemaleInformalCareSupplied_2,shareFemaleInformalCareSupplied_3,shareFemaleInformalCareSupplied_4, '
                     'shareFemaleInformalCareSupplied_5,totalCareDemand_1,totalCareSupply_1,totalUnmetDemand_1, '
                     'totalCareDemand_2,totalCareSupply_2,totalUnmetDemand_2,totalCareDemand_3,totalCareSupply_3, '
                     'totalUnmetDemand_3,totalCareDemand_4,totalCareSupply_4,totalUnmetDemand_4,totalCareDemand_5, '
                     'totalCareSupply_5,totalUnmetDemand_5,shareSocialCare_1,totalInformalSupply_1,totalFormalSupply_1, '
                     'totalInformalCarePerRecipient_1,totalFormalCarePerRecipient_1,totalUnmetNeedPerRecipient_1, '
                     'totalInformalCarePerCarer_1,totalFormalCarePerCarer_1,shareInformalSupply_1,shareUnmetCareDemand_1, '
                     'perCapitaUnmetCareDemand_1,shareSocialCare_2,totalInformalSupply_2,totalFormalSupply_2,totalInformalCarePerRecipient_2, '
                     'totalFormalCarePerRecipient_2,totalUnmetNeedPerRecipient_2,totalInformalCarePerCarer_2, '
                     'totalFormalCarePerCarer_2,shareInformalSupply_2,shareUnmetCareDemand_2,perCapitaUnmetCareDemand_2, '
                     'shareSocialCare_3,totalInformalSupply_3,totalFormalSupply_3,totalInformalCarePerRecipient_3,totalFormalCarePerRecipient_3, '
                     'totalUnmetNeedPerRecipient_3,totalInformalCarePerCarer_3,totalFormalCarePerCarer_3, '
                     'shareInformalSupply_3,shareUnmetCareDemand_3,perCapitaUnmetCareDemand_3,shareSocialCare_4,totalInformalSupply_4, '
                     'totalFormalSupply_4,totalInformalCarePerRecipient_4,totalFormalCarePerRecipient_4, '
                     'totalUnmetNeedPerRecipient_4,totalInformalCarePerCarer_4,totalFormalCarePerCarer_4, '
                     'shareInformalSupply_4,shareUnmetCareDemand_4,perCapitaUnmetCareDemand_4,shareSocialCare_5,totalInformalSupply_5, '
                     'totalFormalSupply_5,totalInformalCarePerRecipient_5,totalFormalCarePerRecipient_5, '
                     'totalUnmetNeedPerRecipient_5,totalInformalCarePerCarer_5,totalFormalCarePerCarer_5, '
                     'shareInformalSupply_5,shareUnmetCareDemand_5,perCapitaUnmetCareDemand_5,totalSupplyHousehold, '
                     'totalSupplyNoK_1,totalSupplyNoK_2,totalSupplyNoK_3,totalInformalSupplyHousehold, '
                     'totalInformalSupplyNoK_1,totalInformalSupplyNoK_2,totalInformalSupplyNoK_3,totalFormalSupplyHousehold, '
                     'totalFormalSupplyNoK_1,totalFormalSupplyNoK_2,totalFormalSupplyNoK_3,totalEmployment, '
                     'totalEmployment_1,totalEmployment_2,totalEmployment_3,totalEmployment_4,totalEmployment_5, '
                     'totalJobChanges,averageIncome_M,averageIncome_F,averageIncome_1,averageIncome_1_Males, '
                     'averageIncome_1_Females,averageIncome_2,averageIncome_2_Males,averageIncome_2_Females, '
                     'averageIncome_3,averageIncome_3_Males,averageIncome_3_Females,averageIncome_4, '
                     'averageIncome_4_Males,averageIncome_4_Females,averageIncome_5,averageIncome_5_Males, '
                     'averageIncome_5_Females,numberRelocations,numJobRelocations_1,numJobRelocations_2, '
                     'numJobRelocations_3,numJobRelocations_4,numJobRelocations_5,numMarriageRelocations, '
                     'numSizeRelocations,numRetiredRelocations,numberTownChanges')
            
            filename = folder + '/Outputs.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))
            np.savetxt(filename, values, delimiter=',', fmt='%f', header=names, comments="")
            
                
            values = zip(self.perCapitaHouseholdIncome, self.socialCareMapValues, 
                         self.relativeEducationCost, self.probKeepStudying, self.stageStudent, self.changeJobRate, 
                         self.changeJobdIncome, self.relocationCareLoss, self.relocationCost, self.townRelocationAttraction, 
                         self.townRelativeAttraction, self.townsJobProb, self.townJobAttraction, 
                         self.unemployedIncomeDiscountingFactor, self.relativeTownAttraction, self.houseScore, 
                         self.deltaHouseOccupants)
            
            names = ('perCapitaHouseholdIncome, socialCareMapValues, '
                     'relativeEducationCost, probKeepStudying, stageStudent, changeJobRate, '
                     'changeJobdIncome, relocationCareLoss, relocationCost, townRelocationAttraction, '
                     'townRelativeAttraction, townsJobProb, townJobAttraction, '
                     'unemployedIncomeDiscountingFactor, relativeTownAttraction, houseScore, '
                     'deltaHouseOccupants')
            
            filename = folder + '/Check_Value.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))
            np.savetxt(filename, values, delimiter=',', fmt='%f', header=names, comments="")
            
            
            
            # Graphic Output related code
        
            if self.p['singleRunGraphs']:
                self.doGraphs(folder)
                
        self.sensitivityGraphs(folder_S)
    
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
            
            self.socialClassShares = [0.0, 0.0, 0.0, 0.0, 0.0]
            
            while (self.socialClassShares[0] < 0.15 or self.socialClassShares[0] > 0.25 ) or (self.socialClassShares[1] < 0.2 or self.socialClassShares[1] > 0.3 ) or (self.socialClassShares[2] < 0.25 or self.socialClassShares[2] > 0.35 ) or self.socialClassShares[0] > self.socialClassShares[1] or self.socialClassShares[1] > self.socialClassShares[2] or (self.socialClassShares[3] < 0.15 or self.socialClassShares[3] > 0.25 ) or self.socialClassShares[3] > self.socialClassShares[1] or (self.socialClassShares[4] < 0.04 or self.socialClassShares[4] > 0.06 ):
                
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
                
                self.computeClassShares()
            
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
        
        
        # Initialize mortality rates' dataset
        for k in range(2):
            self.inputsMortality.append([])
            self.outputMortality.append([])
            self.regressionModels_M.append([])
        for k in range(2):    
            for i in range(self.p['numberClasses']):
                self.inputsMortality[k].append([])
                self.outputMortality[k].append([])
                self.regressionModels_M[k].append([])
        for k in range(2):
            for i in range(5):
                for j in range(self.p['numCareLevels']):
                    self.inputsMortality[k][i].append([])
                    self.outputMortality[k][i].append([])
                    self.regressionModels_M[k][i].append(RandomForestRegressor(n_estimators=500, random_state=0)) # LinearRegression())
        
        for i in range(self.p['numberClasses']):
                self.inputsFertility.append([])
                self.outputFertility.append([])
                self.regressionModels_F.append(RandomForestRegressor(n_estimators=500, random_state=0)) # LinearRegression())           
        
        for i in range(self.p['numberClasses']):
            self.unemploymentRateClasses.append([])
            self.meanUnemploymentRates.append([])
            for j in range(6):
                self.unemploymentRateClasses[i].append([])
                self.meanUnemploymentRates[i].append([])
        
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
        executionTimes = []
        # print('Population: ' + str(len(self.pop.livingPeople)))
        # 1
        start = time.time()
        self.computeClassShares()
        end = time.time()
        executionTimes.append(end-start)
        
        # 2
        start = time.time()
        self.updateJobMap()
        end = time.time()
        executionTimes.append(end-start)
        
        # 3
        start = time.time()
        self.updateUnemploymentRates()
        end = time.time()
        executionTimes.append(end-start)
        
        # 4
        start = time.time()
        self.doRegressions()
        end = time.time()
        executionTimes.append(end-start)
        
        # 5
        start = time.time()
        self.doDeaths()
        end = time.time()
        executionTimes.append(end-start)
        
        # 6
        start = time.time()
        self.doBirths()
        end = time.time()
        executionTimes.append(end-start)
        
        # 7
        start = time.time()
        self.doDivorces()
        end = time.time()
        executionTimes.append(end-start)
        
        # 8
        start = time.time()
        self.doMarriages()
        end = time.time()
        executionTimes.append(end-start)
        
         # 12
        start = time.time()
        self.netHouseholdCare()
        end = time.time()
        executionTimes.append(end-start)
        
        # 9
        start = time.time()
        self.joiningSpouses()
        end = time.time()
        executionTimes.append(end-start)
        
        # 13
        start = time.time()
        self.socialCareMap()
        end = time.time()
        executionTimes.append(end-start)
        
         # 10
        start = time.time()
        self.careNeeds()
        end = time.time()
        executionTimes.append(end-start)
        
        # 11
        start = time.time()
        self.careSupplies()
        end = time.time()
        executionTimes.append(end-start)
        
        # 14
        start = time.time()
        self.allocateCare()
        end = time.time()
        executionTimes.append(end-start)
        
        # 15
        start = time.time()
        self.computeNetIncome()
        end = time.time()
        executionTimes.append(end-start)
        
        # 16
        start = time.time()
        self.healthServiceCost()
        end = time.time()
        executionTimes.append(end-start)
        
        # 17
        start = time.time()
        self.ageTransitions()
        end = time.time()
        executionTimes.append(end-start)
        
        # 18
        start = time.time()
        self.socialTransition()
        end = time.time()
        executionTimes.append(end-start)
        
        # 19
        start = time.time()
        self.jobMarket()
        end = time.time()
        executionTimes.append(end-start)
        
        # 20
        start = time.time()
        self.movingAround()
        end = time.time()
        executionTimes.append(end-start)
        
        # 21
        start = time.time()
        self.doStats()
        end = time.time()
        executionTimes.append(end-start)
        
        # 22
        start = time.time()
        self.careTransitions()
        end = time.time()
        executionTimes.append(end-start)
        
        # 23
        start = time.time()
        self.wagesGrowth()
        end = time.time()
        executionTimes.append(end-start)
        
        totTime = sum(executionTimes)
        shareExecutionTimes = [x/totTime for x in executionTimes]
        print(shareExecutionTimes)

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
    
    def deathProb(self, base, classRank, needLevel, shareUnmetNeed, classPop):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow(self.p['mortalityBias'], i)
        lowClassRate = base/a
        classRate = lowClassRate*math.pow(self.p['mortalityBias'], classRank)
        a = 0
        for i in range(self.p['numCareLevels']):
            a += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
        higherNeedRate = classRate/a
        classRate = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - needLevel) # deathProb
        
        # Add the effect of unmet care need on mortality rate for each care need level
        a = 0
        for x in classPop:
            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
        higherUnmetNeed = (classRate*len(classPop))/a
        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
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
                    
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                dieProb = self.deathProb(rawRate, person.classRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                if  self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['startRegressionCollectionFrom']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['startRegressionCollectionFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    self.inputsMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(regressors)
                    dependentVariable = dieProb # [dieProb]
                    self.outputMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(dependentVariable)
                    
                elif self.year >= self.p['implementPoliciesFromYear']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['startRegressionCollectionFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    dieProb = self.regressionModels_M[person.sexIndex][person.classRank][person.careNeedLevel].predict([regressors])
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
                    ageDieProb = (math.exp(age/self.p['maleAgeScaling']))*self.p['maleAgeDieProb'] 
                else:
                    ageDieProb = (math.exp(age/self.p['femaleAgeScaling']))* self.p['femaleAgeDieProb']
                rawRate = self.p['baseDieProb'] + babyDieProb + ageDieProb
                
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                dieProb = self.deathProb(rawRate, person.classRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                if self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['startRegressionCollectionFrom']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['startRegressionCollectionFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    self.inputsMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(regressors)
                    dependentVariable = dieProb # [dieProb]
                    self.outputMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(dependentVariable)
                    
                elif self.year >= self.p['implementPoliciesFromYear']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['startRegressionCollectionFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    dieProb = self.regressionModels_M[person.sexIndex][person.classRank][person.careNeedLevel].predict([regressors])
                # Check variable
#                if person.age == 40 and person.classRank == 0:
#                    self.deathProb.append(dieProb) 
#                    self.careLevel.append(person.careNeedLevel)
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
        
        maxAge = max([x.age for x in self.pop.livingPeople])
        
        print('Maximum age:' + str(maxAge))
        
        postDeath = len(self.pop.livingPeople)
        
        self.deaths_1.append(deaths[0])
        self.deaths_2.append(deaths[1])
        self.deaths_3.append(deaths[2])
        self.deaths_4.append(deaths[3])
        self.deaths_5.append(deaths[4])
        
        print('the number of people who died is: ' + str(preDeath - postDeath))
        
        # print(len(self.pop.livingPeople))
    def doRegressions(self):
        if self.year == self.p['implementPoliciesFromYear']:
            for k in range(2):
                for i in range(self.p['numberClasses']):
                    for j in range(self.p['numCareLevels']):
#                        print('cat: ' + str(k) + ' ' + str(i) + ' ' + str(j))
#                        print(len(self.inputsMortality[k][i][j]))
#                        print(len(self.outputMortality[k][i][j]))
                        # self.regressionModels_M[k][i][j] = LinearRegression()
                        if len(self.inputsMortality[k][i][j]) > 0:
                            self.regressionModels_M[k][i][j].fit(self.inputsMortality[k][i][j], self.outputMortality[k][i][j])
                        
                            # mr_predict = self.regressionModels_M[k][i][j].predict(self.inputsMortality[k][i][j])
                            # self.plotRegressions(self.outputMortality[k][i][j], mr_predict)
                            # print(self.regressionModels_M[k][i][j].score(self.inputsMortality[k][i][j], self.outputMortality[k][i][j]))
                        
            for i in range(self.p['numberClasses']):
                # self.regressionModels_F[i]  = LinearRegression()
                self.regressionModels_F[i].fit(self.inputsFertility[i], self.outputFertility[i])
    
    def plotRegressions(self, mr, prediction):
        plt.scatter(mr, prediction)
        plt.show()
    
    def doBirths(self):
        
        preBirth = len(self.pop.livingPeople)
        marriedLadies = 0
        adultLadies = 0
        births = [0, 0, 0, 0, 0]
        marriedPercentage = []
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age >= self.p['minPregnancyAge']
                                  and x.age <= self.p['maxPregnancyAge']
                                  and x.partner != None and x.status != 'inactive']
        
        adultLadies_1 = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.classRank == 0]   
        marriedLadies_1 = len([x for x in adultLadies_1 if x.partner != None])     
        marriedPercentage.append(marriedLadies_1/float(len(adultLadies_1)))
        adultLadies_2 = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.classRank == 1]    
        marriedLadies_2 = len([x for x in adultLadies_2 if x.partner != None])     
        marriedPercentage.append(marriedLadies_2/float(len(adultLadies_2)))
        adultLadies_3 = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.classRank == 2]   
        marriedLadies_3 = len([x for x in adultLadies_3 if x.partner != None])     
        marriedPercentage.append(marriedLadies_3/float(len(adultLadies_3)))
        adultLadies_4 = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.classRank == 3]  
        marriedLadies_4 = len([x for x in adultLadies_4 if x.partner != None])     
        marriedPercentage.append(marriedLadies_4/float(len(adultLadies_4)))
        adultLadies_5 = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.classRank == 4]   
        marriedLadies_5 = len([x for x in adultLadies_5 if x.partner != None])     
        marriedPercentage.append(marriedLadies_5/float(len(adultLadies_5)))
        
        # print(marriedPercentage)
        
#        for person in self.pop.livingPeople:
#           
#            if person.sex == 'female' and person.age >= self.p['minPregnancyAge']:
#                adultLadies += 1
#                if person.partner != None:
#                    marriedLadies += 1
#        marriedPercentage = float(marriedLadies)/float(adultLadies)
        
        for woman in womenOfReproductiveAge:
            
            
            if self.year < 1951:
                rawRate = self.p['growingPopBirthProb']
            else:
                rawRate = self.fert_data[(self.year - woman.birthdate)-16, self.year-1950]
                
            birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, woman.classRank)
            
            if self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['startRegressionCollectionFrom']:
                age = woman.age-16
                year = self.year-self.p['startRegressionCollectionFrom']
                regressors = [age, math.log(age), year, math.log(year+1)]
                self.inputsFertility[woman.classRank].append(regressors)
                dependentVariable = birthProb # [birthProb]
                self.outputFertility[woman.classRank].append(dependentVariable)
                
            elif self.year >= self.p['implementPoliciesFromYear']:
                age = woman.age-16
                year = self.year-self.p['startRegressionCollectionFrom']
                regressors = [age, math.log(age), year, math.log(year+1)]
                birthProb = self.regressionModels_F[woman.classRank].predict([regressors])
            #baseRate = self.baseRate(self.socialClassShares, self.p['fertilityBias'], rawRate)
            #fertilityCorrector = (self.socialClassShares[woman.classRank] - self.p['initialClassShares'][woman.classRank])/self.p['initialClassShares'][woman.classRank]
            #baseRate *= 1/math.exp(self.p['fertilityCorrector']*fertilityCorrector)
            #birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
            
            if random.random() < birthProb/marriedPercentage[woman.classRank]:
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
        
        # print('the number of births is: ' + str(postBirth - preBirth))
    
    def computeBirthProb(self, fertilityBias, rawRate, womanRank):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow(fertilityBias, i)
        baseRate = rawRate/a
        birthProb = baseRate*math.pow(self.p['fertilityBias'], womanRank)
        return(birthProb)
#        classRates = []
#        for i in range(self.p['numberClasses']):
#            birthProb = baseRate*math.pow(self.p['fertilityBias'], i)
#            fertilityCorrector = (classShares[i] - self.p['initialClassShares'][i])/self.p['initialClassShares'][i]
#            classRate = birthProb*(1/math.exp(self.p['fertilityCorrector']*fertilityCorrector))
#            classRates.append(classRate)
#        a = 0
#        for i in range(self.p['numberClasses']):
#            a += classShares[i]*classRates[i]
#        correction = rawRate/a
#        correctedClassRates = [x*correction for x in classRates]
#        return(correctedClassRates[womanRank])
            
    def careNeeds(self):
        self.publicSupply = 0
        for person in self.pop.livingPeople:
            person.visitedCarer = False
            person.hoursDemand = 0
            person.residualNeed = 0
            person.informalCare = 0
            person.formalCare = 0
            person.hoursSocialCareDemand = 0
            person.residualSocialCareNeed = 0
            person.residualIncomeCare = 0
            person.hoursChildCareDemand = 0
            person.residualChildCareNeed = 0
            person.hoursInformalSupply = 0
            person.residualInformalSupply = 0
            person.residualFormalSupply = 0
            person.hoursFormalSupply = 0
            person.socialWork = 0
            person.workToCare = 0
            person.totalSupply = 0
            person.extraworkCare = 0
            person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            
            careNeed = self.p['careDemandInHours'][person.careNeedLevel]

            person.hoursDemand = careNeed
            person.residualNeed = person.hoursDemand
            
            if person.careNeedLevel >= (self.p['socialSupportLevel'] + self.p['socialSupportLevelPolicyChange']):
                self.publicSupply += person.hoursDemand
                person.residualNeed = person.hoursDemand
                
#            person.hoursSocialCareDemand = careNeed
#            person.residualSocialCareNeed = person.hoursDemand
                
            if person.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(person.id) + " now has "
                messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                self.textUpdateList.append(messageString)
        
        # Childcare need
        
        children = [x for x in self.pop.livingPeople if x.age < self.p['ageTeenagers']]
#        
        for child in children:
            if child.age == 0:
                child.status == 'child'
                childCare = self.p['zeroYearCare']
                if child.hoursDemand < childCare:
                    child.hoursDemand = childCare
                    child.residualNeed = child.hoursDemand
#            householdDisposableIncome = self.computeDisposableIncome(child.father) + self.computeDisposableIncome(child.mother)
#            childCare = self.p['zeroYearCare']
#            if child.age >= self.p['schoolAge']:
#                childCare -= self.p['schoolHours']
#            elif child.age >= self.p['minAgeStartChildCareSupport']:
#                if child.father.status == 'employed' and child.mother.status == 'employed':
#                    childCare -= self.p['workingParentsFreeChildcareHours']
#                else:
#                    childCare -= self.p['freeChildcareHours']
#            elif child.age >= self.p['minAgeStartChildCareSupportByIncome'] and householdDisposableIncome < p['maxHouseholdIncomeChildCareSupport']:
#                childCare -= self.p['freeChildcareHours']
##            care = self.p['zeroYearCare']/math.exp(self.p['childcareDecreaseRate']*child.age)
##            care = int((care+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#            if child.hoursDemand < childCare:
#                child.hoursDemand = childCare
#                child.residualNeed = child.hoursDemand
#                
#            if child.hoursSocialCareDemand < childCare:
#                child.hoursChildCareDemand = childCare - child.hoursSocialCareDemand
#                child.residualChildCareNeed = child.hoursChildCareDemand
#                
            if child.age == 0 and child.mother.status != 'inactive':
                child.mother.socialWork = self.p['zeroYearCare']
                child.mother.income = 0
                child.mother.disposableIncome = child.mother.income
                child.mother.status = 'maternity'
                child.mother.babyCarer = True
                child.residualNeed = 0
                child.informalCare = self.p['zeroYearCare']
#                
#        for person in self.pop.livingPeople:
#            person.hoursDemand = person.hoursSocialCareDemand + person.hoursChildCareDemand
    
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
                if person.careNeedLevel > 0:
                    unmetNeedFactor = 1/math.exp(self.p['unmetNeedExponent']*person.cumulativeUnmetNeed)
                else:
                    unmetNeedFactor = 1.0
                transitionRate = (1.0 - baseTransition*math.pow(self.p['careBias'], person.classRank))*unmetNeedFactor
                stepCare = 1
                bound = transitionRate
                while random.random() > bound and stepCare < self.p['numCareLevels'] - 1:
                    stepCare += 1
                    bound += (1-bound)*transitionRate
                person.careNeedLevel += stepCare
                
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = self.p['numCareLevels'] - 1
                
                if person.age < self.p['ageOfRetirement'] and person.ageStartWorking != -1:
                    shareWorkingLife = (person.age - person.ageStartWorking)/(self.p['ageOfRetirement'] - person.ageStartWorking)
                    person.income = self.p['pensionWage'][person.classRank]*self.p['weeklyHours']
                    if person.careNeedLevel < self.p['hillHealthLevelThreshold']:
                        person.income *= shareWorkingLife
                    else:
                        person.income *= (shareWorkingLife + self.p['seriouslyHillSupportRate']*(1-shareWorkingLife))
                    
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
            notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            for member in notWorking:
                if member.status == 'teenager':
                    individualSupply = self.p['teenAgersHours']
                elif member.status == 'student':
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
            
            # Check time series
            self.perCapitaHouseholdIncome.append(householdPerCapitaIncome)
            
            # Compute the total income devoted to informal care supply
            incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
            incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
            residualIncomeForCare = householdIncome*(1 - incomeCoefficient)
            
            for worker in employed:
                worker.extraworkCare = self.p['employedHours']
                worker.hoursInformalSupply = worker.extraworkCare
            
#           Code for tax breaks policy
#
#            higherBandIncome = 0
#            middleBandIncome = 0
#            lowerBandIncome = 0
#            earningMembers = [x for x in household if x.income > 0]
#            for member in earningMembers:
#                if member.income > self.p['taxBands'][1]:
#                    higherBandIncome += member.income - self.p['taxBands'][1]
#                if member.income > self.p['taxBands'][0] and member.income <= self.p['taxBands'][1]:
#                    middleBandIncome += member.income - self.p['taxBands'][0]
#                else:
#                    lowerBandIncome += member.income
#            
#            incomeByTaxBands = []
#            netSocialCarePrices = []
#            incomeByTaxBands.append(higherBandIncome, middleBandIncome, lowerBandIncome)
#            for i in range(self.p['taxBandsNumber']-1, -1, -1):
#                netSocialCarePrices.append(self.p['priceSocialCare']*(1-self.p['taxBreakRate']*self.p['bandsTaxationRates'][i]))
#                    
#            residualIncomeForCare = householdIncome
#            for worker in employed:
#                for i in range(self.p['taxBandsNumber']):
#                    if netSocialCarePrices[i] <= worker.wage:
#                        optimalIncomeForCare = self.computeIncomeForCare(residualIncomeForCare, len(household), netSocialCarePrices[i])
#                        incomeForCare = min(optimalIncomeForCare, incomeByTaxBands[i])
#                        totHours = incomeForCare/netSocialCarePrices[i]
#                        formalSupplyHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                        for member in household:
#                            member.residualFormalSupply += formalSupplyHours
#                            member.hoursFormalSupply += formalSupplyHours
#                        residualIncomeForCare -= incomeForCare
#                        if residualIncomeForCare <= 0:
#                            break
#                     else:
#                        optimalIncomeForCare = self.computeIncomeForCare(residualIncomeForCare, len(household), worker.wage)
#                        maxIndividualHours = optimalIncomeForCare/worker.wage
#                        if maxIndividualHours > self.p['weeklyHours']:
#                            individualSupply = self.p['weeklyHours']
#                        else:
#                            individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                        worker.residualInformalSupply = individualSupply
#                        worker.hoursInformalSupply += worker.residualInformalSupply
#                        residualIncomeForCare -= individualSupply*worker.wage
#                        if residualIncomeForCare <= 0:
#                            break
                
            
            for worker in employed:
                if worker.wage < self.p['priceSocialCare']:
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

            totHours = residualIncomeForCare/self.p['priceSocialCare']
            formalSupplyHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            
            earningMembers = [x for x in household if x.income > 0]
        
            if len(earningMembers) == 0 and formalSupplyHours > 0:
                print('Error: no income to pay social care from (careSupplies)')
                
            for member in household:
                member.residualFormalSupply = formalSupplyHours
                member.hoursFormalSupply = formalSupplyHours 

            
                ######################    Old code   ###########################
                
                # worker.extraworkCare = self.p['employedHours']
                

            # Compute the total income-based formal social care supply   
            
#            workToCareHours = residualIncomeForCare/self.p['priceSocialCare']
#            workToCareHours = int((workToCareHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            
            # householdEmployedFormalSupply = int((householdEmployedFormalSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            # Assign the total income-based formal care supply to the employed members of the household (according to income) 
#            residualSupply = residualIncomeForCare
#            earners = [x for x in household if x.status == 'retired' or x.status == 'employed']
#            for person in earners:
#                workToCareHours = min(self.p['weeklyHours'], residualSupply/self.p['priceSocialCare'])
#                individualSupply = int((workToCareHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                person.residualFormalSupply = individualSupply
#                person.hoursFormalSupply = person.residualFormalSupply
#                residualIncomeForCare -= individualSupply*self.p['priceSocialCare']
#                if residualIncomeForCare <= 0:
#                    break
   
    def computeIncomeForCare(self, householdIncome, householdSize, formalSocialCarePrice):
        householdPerCapitaIncome = householdIncome/householdSize
        incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
        incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome/formalSocialCarePrice) # Min-Max: 0 - 1500
        residualIncomeForCare = householdIncome*(1 - incomeCoefficient)
        return (residualIncomeForCare)
        
    def netHouseholdCare(self):
        self.householdsList = []
        for person in self.pop.livingPeople:
            # person.netHouseholdCare = 0
            person.visitedCarer = False
            
        for person in self.pop.livingPeople:
            if person.visitedCarer == True:
                continue
            household = []
            notInHousehold = []
            if person.justMarried == None: 
                if person.independentStatus == False and (person.status == 'employed' or person.status == 'unemployed'):
                    household = [person]
                    household.extend([x for x in person.children if x.dead == False and x.house == person.house])
                else:
                    notInHousehold = [x for x in person.house.occupants if x.independentStatus == False and (x.status == 'employed' or x.status == 'unemployed')]
                    for agent in notInHousehold:
                        notInHousehold.extend([x for x in agent.children if x.dead == False and x.house == agent.house])
                    householdTemp = [x for x in person.house.occupants if x.justMarried == None]
                    household = [x for x in householdTemp if x not in notInHousehold]
            else:
                household = [person, person.partner]
                childrenWithPerson = [x for x in person.children if x.dead == False and x.house == person.house]
                household.extend(childrenWithPerson)
                childrenWithPartner = [x for x in person.partner.children if x.dead == False and x.house == person.partner.house]
                household.extend(childrenWithPartner)
                
            if len(household) > 0:
                self.householdsList.append(household)
            
                householdDemand = 0
                householdSupply = 0
    
                for member in household:
                    if member.age > 0:
                        householdDemand += self.p['careDemandInHours'][member.careNeedLevel]
                    else:
                        householdDemand += self.p['zeroYearCare']
    
                householdCarers = [x for x in household if x.hoursDemand == 0]
                # notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
                for member in householdCarers:
                    if member.status == 'teenager':
                        householdSupply += self.p['teenAgersHours']
                    elif member.status == 'student':
                        householdSupply += self.p['studentHours']
                    elif member.status == 'retired':
                        householdSupply += self.p['retiredHours']
                    elif member.status == 'unemployed':
                        householdSupply += self.p['unemployedHours']
                    elif member.status == 'employed':
                        householdSupply += self.p['employedHours']
                    
                    
                    
                deltaHouseholdCare = householdSupply - householdDemand
                
                for member in household:
                    member.visitedCarer = True
                    member.householdName = household[0]
                    member.netHouseholdCare = deltaHouseholdCare
                    
    def socialCareMap(self):
        for household in self.householdsList:
            for member in household:
                member.socialCareMap = []
                
#            householdDemand = 0
#            householdSupply = 0
#
#            for member in household:
#                if member.age > 0:
#                    householdDemand += self.p['careDemandInHours'][member.careNeedLevel]
#                else:
#                    householdDemand += self.p['zeroYearCare']
#
#            householdCarers = [x for x in household if x.hoursDemand == 0]
#            notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
#            for member in notWorking:
#                if member.status == 'teenager':
#                    individualSupply = self.p['teenAgersHours']
#                elif member.status == 'student':
#                    individualSupply = self.p['studentHours']
#                elif member.status == 'retired':
#                    individualSupply = self.p['retiredHours']
#                elif member.status == 'unemployed':
#                    individualSupply = self.p['unemployedHours']
#                householdSupply += int((individualSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#    
#            employed = [x for x in householdCarers if x.status == 'employed']
#            employed.sort(key=operator.attrgetter("wage"))
#            potentialIncome = 0
#            for member in household:
#                if member.income > 0:
#                    potentialIncome += member.income
#                elif member.status == 'unemployed':
#                    potentialIncome += self.expectedIncome(member, member.house.town)
#            
#            householdPerCapitaIncome = potentialIncome/float(len(household))
#            
#            # Compute the total income devoted to informal care supply
#            incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
#            incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
#            residualIncomeForCare = potentialIncome*(1 - incomeCoefficient)
#            
#            for worker in employed:
#                householdSupply += self.p['employedHours']
#                
#            for worker in employed:
#                if worker.wage < self.p['priceSocialCare']:
#                    maxIndividualHours = residualIncomeForCare/worker.wage
#                    if maxIndividualHours > self.p['weeklyHours']:
#                        individualSupply = self.p['weeklyHours']
#                    else:
#                        individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                    householdSupply += individualSupply
#                    residualIncomeForCare -= individualSupply*worker.wage
#                    if residualIncomeForCare <= 0:
#                        break
#    
#            totHours = residualIncomeForCare/self.p['priceSocialCare']
#            householdSupply += int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#            
#            potentialIncome /= float(len(household))
            
            deltaHouseholdCare = household[0].netHouseholdCare #householdSupply - householdDemand
            
            # deltaHouseholdCare = household[0].netHouseholdCare
            kinshipWeight_1 = 1/math.exp(self.p['networkDistanceParam']*1.0)
            kinshipWeight_2 = 1/math.exp(self.p['networkDistanceParam']*2.0)
            kinshipWeight_3 = 1/math.exp(self.p['networkDistanceParam']*3.0)
            visitedPeople = []
            for town in self.map.towns:
                deltaNetworkCare = 0
                for member in household:
                    if member.father != None:
                        nok = member.father
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                        nok = member.mother
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                            visitedPeople.extend(h for h in self.householdsList if nok in h)    
                    for nok in member.children:
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                    if member.father != None and member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                        nok = member.father.mother
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                    if member.mother != None and member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                    for child in member.children:
                            for nok in child.children:
                                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                    if member.father != None:
                            brothers = list(set(member.father.children + member.mother.children))
                            brothers.remove(member)
                            for nok in brothers:
                                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                            paternalUncles = []
                            maternalUncles = []
                            if member.father.father != None:
                                paternalUncles = list(set(member.father.father.children + member.father.mother.children))
                                paternalUncles.remove(member.father)
                            if member.mother.father != None:    
                                maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
                                maternalUncles.remove(member.mother)
                            unclesList = list(set(maternalUncles + paternalUncles))
                            for nok in unclesList:
                                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_3
                                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                            for brother in brothers:
                                for nok in brother.children:
                                    if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town:
                                        deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_3
                                        visitedPeople.extend(h for h in self.householdsList if nok in h)
                    
        
#        for person in self.pop.livingPeople:
#            person.visitedCarer = False
#            
#        for person in self.pop.livingPeople:
#            
#            if person.visitedCarer == True:
#                continue
#            
#            household = []
#            notInHousehold = []
#            if person.justMarried == None:
#                if person.independentStatus == False and (person.status == 'employed' or person.status == 'unemployed'):
#                    household = [person]
#                    household.extend([x for x in person.children if x.dead == False and x.house == person.house])
#                else:
#                    notInHousehold = [x for x in person.house.occupants if x.independentStatus == False and (x.status == 'employed' or x.status == 'unemployed')]
#                    for agent in notInHousehold:
#                        notInHousehold.extend([x for x in agent.children if x.dead == False and x.house == agent.house])
#                    householdTemp = [x for x in person.house.occupants if x.justMarried == None]
#                    household = [x for x in householdTemp if x not in notInHousehold]
##            else:
##                household = [x for x in person.house.occupants if x.justMarried == person.partner.id]
##                household.extend([x for x in person.partner.house.occupants if x.justMarried == person.id])
#            if len(household) > 0:
#                for member in household:
#                    member.visitedCarer = True
#    
#                householdDemand = 0
#                householdSupply = 0
#
#                for member in household:
#                    if member.age > 0:
#                        householdDemand += self.p['careDemandInHours'][member.careNeedLevel]
#                    else:
#                        householdDemand += self.p['zeroYearCare']
#
#                householdCarers = [x for x in household if x.hoursDemand == 0]
#                notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
#                for member in notWorking:
#                    if member.status == 'teenager':
#                        individualSupply = self.p['teenAgersHours']
#                    elif member.status == 'student':
#                        individualSupply = self.p['studentHours']
#                    elif member.status == 'retired':
#                        individualSupply = self.p['retiredHours']
#                    elif member.status == 'unemployed':
#                        individualSupply = self.p['unemployedHours']
#                    householdSupply += int((individualSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#        
#                employed = [x for x in householdCarers if x.status == 'employed']
#                employed.sort(key=operator.attrgetter("wage"))
#                potentialIncome = 0
#                for member in household:
#                    if member.income > 0:
#                        potentialIncome += member.income
#                    elif member.status == 'unemployed':
#                        potentialIncome += self.expectedIncome(member, member.house.town)
#                
#                householdPerCapitaIncome = potentialIncome/float(len(household))
#                
#                # Compute the total income devoted to informal care supply
#                incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
#                incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
#                residualIncomeForCare = potentialIncome*(1 - incomeCoefficient)
#                
#                for worker in employed:
#                    householdSupply += self.p['employedHours']
#                    
#                for worker in employed:
#                    if worker.wage < self.p['priceSocialCare']:
#                        maxIndividualHours = residualIncomeForCare/worker.wage
#                        if maxIndividualHours > self.p['weeklyHours']:
#                            individualSupply = self.p['weeklyHours']
#                        else:
#                            individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                        householdSupply += individualSupply
#                        residualIncomeForCare -= individualSupply*worker.wage
#                        if residualIncomeForCare <= 0:
#                            break
#        
#                totHours = residualIncomeForCare/self.p['priceSocialCare']
#                householdSupply += int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                
#                potentialIncome /= float(len(household))
#                deltaHouseholdCare = householdSupply - householdDemand
#                visitedPeople = []
#                for town in self.map.towns:
#                    townNetworkDemand = 0
#                    townNetworkSupply = 0
#                    # Kinship distance == 1 (partents and children)
#                    kinshipDemand = 0
#                    kinshipSupply = 0
#                    kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*1.0)
#                    for member in household:
#                        if member.father != None:
#                            if member.father.dead == False and member.father not in visitedPeople and member.father not in household and member.father.house.town == town:
#                                nok_Household = self.householdMembers(member.father)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                            if member.mother.dead == False and member.mother not in visitedPeople and member.mother not in household and member.mother.house.town == town:
#                                nok_Household = self.householdMembers(member.mother)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                        for child in member.children:
#                            if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
#                                nok_Household = self.householdMembers(child)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                    townNetworkDemand += kinshipDemand
#                    townNetworkSupply += kinshipSupply
#                    # Kinship distance == 2 (grandparents, grandchildren and brothers/sisters)   
#                    kinshipDemand = 0
#                    kinshipSupply = 0
#                    kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*2.0) 
#                    for member in household:
#                        if member.father != None and member.father.father != None:
#                            if member.father.father.dead == False and member.father.father not in visitedPeople and member.father.father not in household and member.father.father.house.town == town:
#                                nok_Household = self.householdMembers(member.father.father)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                            if member.father.mother.dead == False and member.father.mother not in visitedPeople and member.father.mother not in household and member.father.mother.house.town == town:
#                                nok_Household = self.householdMembers(member.father.mother)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                        if member.father != None and member.mother.father != None:
#                            if member.mother.father.dead == False and member.mother.father not in visitedPeople and member.mother.father not in household and member.mother.father.house.town == town:
#                                nok_Household = self.householdMembers(member.mother.father)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                            if member.mother.mother.dead == False and member.mother.mother not in visitedPeople and member.mother.mother not in household and member.mother.mother.house.town == town:
#                                nok_Household = self.householdMembers(member.mother.mother)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                        for child in member.children:
#                            for grandson in child.children:
#                                if grandson.dead == False and grandson not in visitedPeople and grandson not in household and grandson.house.town == town:
#                                    nok_Household = self.householdMembers(grandson)
#                                    if len(nok_Household) > 0:
#                                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                        for agent in nok_Household:
#                                            visitedPeople.append(agent)
#                        if member.father != None:
#                            brothers = list(set(member.father.children + member.mother.children))
#                            brothers.remove(member)
#                            for brother in brothers:
#                                if brother.dead == False and brother not in visitedPeople and brother not in household and brother.house.town == town:
#                                    nok_Household = self.householdMembers(brother)
#                                    if len(nok_Household) > 0:
#                                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                                        for agent in nok_Household:
#                                            visitedPeople.append(agent)
#                    townNetworkDemand += kinshipDemand
#                    townNetworkSupply += kinshipSupply
#                    # Kinship distance == 3 (uncles/aunts and grandchildren and nephews/nieces)   
#                    kinshipDemand = 0
#                    kinshipSupply = 0
#                    kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*3.0) 
#                    for member in household:
#                        paternalUncles = []
#                        maternalUncles = []
#                        if member.father != None and member.father.father != None:
#                            paternalUncles = list(set(member.father.father.children + member.father.mother.children))
#                            paternalUncles.remove(member.father)
#                        if member.father != None and member.mother.father != None:    
#                            maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
#                            maternalUncles.remove(member.mother)
#                        unclesList = list(set(maternalUncles + paternalUncles))
#                        unclesList = [x for x in unclesList if x.dead == False]
#                        for uncle in unclesList:
#                            if uncle.dead == False and uncle not in visitedPeople and uncle not in household and uncle.house.town == town:
#                                nok_Household = self.householdMembers(uncle)
#                                if len(nok_Household) > 0:
#                                    kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                    kinshipSupply += self.householdCareSupply(nok_Household, 3)*kinshipWeight 
#                                    for agent in nok_Household:
#                                        visitedPeople.append(agent)
#                        if member.father != None:
#                            brothers = list(set(member.father.children + member.mother.children))
#                            brothers = [x for x in brothers if x.dead == False]
#                            brothers.remove(member)
#                            for brother in brothers:
#                                for child in brother.children:
#                                    if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
#                                        nok_Household = self.householdMembers(child)
#                                        if len(nok_Household) > 0:
#                                            kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                            kinshipSupply += self.householdCareSupply(nok_Household, 3)*kinshipWeight 
#                                            for agent in nok_Household:
#                                                visitedPeople.append(agent) 
#                    townNetworkDemand += kinshipDemand
#                    townNetworkSupply += kinshipSupply
#                    deltaNetworkCare = townNetworkDemand - townNetworkSupply
                    
                    
                if deltaHouseholdCare < 0:
                    networkSocialCareParam = self.p['excessNeedParam']
                else:
                    networkSocialCareParam = self.p['excessNeedParam']*self.p['careSupplyBias']
                
                # Check variable
                if deltaHouseholdCare*deltaNetworkCare != 0:
                    self.socialCareMapValues.append(deltaHouseholdCare*deltaNetworkCare)
                    
                # Min-Max: -6000 - 3000
                townSCI = (networkSocialCareParam*deltaHouseholdCare*deltaNetworkCare) # /math.exp(self.p['careIncomeParam']*potentialIncome)
                for member in household:
                    member.socialCareMap.append(townSCI)
                
    def householdMembers(self, person):
        household = []
        notInHousehold = []
        if person.justMarried == None:
            if person.independentStatus == False and (person.status == 'employed' or person.status == 'unemployed'):
                household = [person]
                household.extend([x for x in person.children if x.dead == False and x.house == person.house])
            else:
                notInHousehold = [x for x in person.house.occupants if x.independentStatus == False and (x.status == 'employed' or x.status == 'unemployed')]
                for agent in notInHousehold:
                    notInHousehold.extend([x for x in agent.children if x.dead == False and x.house == agent.house])
                householdTemp = [x for x in person.house.occupants if x.justMarried == None]
                household = [x for x in householdTemp if x not in notInHousehold]
        return(household)
    
    def householdCareDemand(self, household):
        householdDemand = 0
        for member in household:
            if member.age > 0:
                householdDemand += self.p['careDemandInHours'][member.careNeedLevel]
            else:
                householdDemand += self.p['zeroYearCare']
        return(householdDemand)
    
    def householdCareSupply(self, household, kinshipDistance):
        householdSupply = 0
        householdCarers = [x for x in household if x.hoursDemand == 0]
        notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
        for member in notWorking:
            if member.status == 'teenager':
                individualSupply = self.p['teenAgersHours']
            elif member.status == 'student':
                individualSupply = self.p['studentHours']
            elif member.status == 'retired':
                individualSupply = self.p['retiredHours']
            elif member.status == 'unemployed':
                individualSupply = self.p['unemployedHours']
            householdSupply += int((individualSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']

        employed = [x for x in householdCarers if x.status == 'employed']
        employed.sort(key=operator.attrgetter("wage"))
        potentialIncome = 0
        for member in household:
            if member.income > 0:
                potentialIncome += member.income
            elif member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, member.house.town)
        
        householdPerCapitaIncome = potentialIncome/float(len(household))
        
        # Compute the total income devoted to informal care supply
        incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
        incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
        residualIncomeForCare = potentialIncome*(1 - incomeCoefficient)
        
        for worker in employed:
            householdSupply += self.p['employedHours']
            
        for worker in employed:
            if worker.wage < self.p['priceSocialCare']:
                maxIndividualHours = residualIncomeForCare/worker.wage
                if maxIndividualHours > self.p['weeklyHours']:
                    individualSupply = self.p['weeklyHours']
                else:
                    individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                householdSupply += individualSupply
                residualIncomeForCare -= individualSupply*worker.wage
                if residualIncomeForCare <= 0:
                    break
        
        if kinshipDistance < 2:
            totHours = residualIncomeForCare/self.p['priceSocialCare']
            householdSupply += int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        
        return(householdSupply)
    
    def spousesCareLocation(self, person):
        
        householdDemand = 0
        householdSupply = 0
        
        household = [person, person.partner]
        childrenWithPerson = [x for x in person.children if x.dead == False and x.house == person.house]
        household.extend(childrenWithPerson)
        childrenWithPartner = [x for x in person.partner.children if x.dead == False and x.house == person.partner.house]
        household.extend(childrenWithPartner)
        
#        for member in household:
#            if member.age > 0:
#                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
#                householdDemand += careNeed
#            else:
#                householdDemand += self.p['zeroYearCare']
#
#        householdCarers = [x for x in household if x.hoursDemand == 0]
#        notWorking = [x for x in household if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
#        for member in notWorking:
#            if member.status == 'teenager':
#                individualSupply = self.p['teenAgersHours']
#            elif member.status == 'student':
#                individualSupply = self.p['studentHours']
#            elif member.status == 'retired':
#                individualSupply = self.p['retiredHours']
#            elif member.status == 'unemployed':
#                individualSupply = self.p['unemployedHours']
#            householdSupply += int((individualSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#
#        employed = [x for x in householdCarers if x.status == 'employed']
#        employed.sort(key=operator.attrgetter("wage"))
#        potentialIncome = 0
#        for member in household:
#            if member.income > 0:
#                potentialIncome += member.income
#            elif member.status == 'unemployed':
#                potentialIncome += self.expectedIncome(member, member.house.town)
#        
#        householdPerCapitaIncome = potentialIncome/float(len(household))
#        
#        # Compute the total income devoted to informal care supply
#        incomeCareParameter = self.p['incomeCareParam']*self.p['incomeCareParamPolicyCoeffcient']
#        incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
#        residualIncomeForCare = potentialIncome*(1 - incomeCoefficient)
#        
#        for worker in employed:
#            householdSupply += self.p['employedHours']
#            
#        for worker in employed:
#            if worker.wage < self.p['priceSocialCare']:
#                maxIndividualHours = residualIncomeForCare/worker.wage
#                if maxIndividualHours > self.p['weeklyHours']:
#                    individualSupply = self.p['weeklyHours']
#                else:
#                    individualSupply = int((maxIndividualHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                householdSupply += individualSupply
#                residualIncomeForCare -= individualSupply*worker.wage
#                if residualIncomeForCare <= 0:
#                    break
#
#        totHours = residualIncomeForCare/self.p['priceSocialCare']
#        householdSupply += int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#        
#        potentialIncome /= float(len(household))
        
        deltaHouseholdCare = household[0].netHouseholdCare #householdSupply - householdDemand
        
        kinshipWeight_1 = 1/math.exp(self.p['networkDistanceParam']*1.0)
        kinshipWeight_2 = 1/math.exp(self.p['networkDistanceParam']*2.0)
        kinshipWeight_3 = 1/math.exp(self.p['networkDistanceParam']*3.0)
        visitedPeople = []
        deltaNetworkCare = 0
        town = person .house.town
        for member in household:
            if member.father != None:
                nok = member.father
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                nok = member.mother
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                    visitedPeople.extend(h for h in self.householdsList if nok in h)    
            for nok in member.children:
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_1
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
            if member.father != None and member.father.father != None:
                nok = member.father.father
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                nok = member.father.mother
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
            if member.mother != None and member.mother.father != None:
                nok = member.mother.father
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
                nok = member.mother.mother
                if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                    deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                    visitedPeople.extend(h for h in self.householdsList if nok in h)
            for child in member.children:
                    for nok in child.children:
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
            if member.father != None:
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for nok in brothers:
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_2
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                    paternalUncles = []
                    maternalUncles = []
                    if member.father.father != None:
                        paternalUncles = list(set(member.father.father.children + member.father.mother.children))
                        paternalUncles.remove(member.father)
                    if member.mother.father != None:    
                        maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
                        maternalUncles.remove(member.mother)
                    unclesList = list(set(maternalUncles + paternalUncles))
                    for nok in unclesList:
                        if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                            deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_3
                            visitedPeople.extend(h for h in self.householdsList if nok in h)
                    for brother in brothers:
                        for nok in brother.children:
                            if nok.dead == False and nok not in visitedPeople and nok not in household and nok.house.town == town and nok != member.partner:
                                deltaNetworkCare += -1*nok.netHouseholdCare*kinshipWeight_3
                                visitedPeople.extend(h for h in self.householdsList if nok in h)
        
        
#        visitedPeople = []
#        town = person.house.town
#        townNetworkDemand = 0
#        townNetworkSupply = 0
#        # Kinship distance == 1 (partents and children)
#        kinshipDemand = 0
#        kinshipSupply = 0
#        kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*1.0)
#        for member in household:
#            if member.father != None:
#                if member.father.dead == False and member.father not in visitedPeople and member.father not in household and member.father.house.town == town:
#                    nok_Household = self.householdMembers(member.father)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#                if member.mother.dead == False and member.mother not in visitedPeople and member.mother not in household and member.mother.house.town == town:
#                    nok_Household = self.householdMembers(member.mother)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#            for child in member.children:
#                if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
#                    nok_Household = self.householdMembers(child)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 1)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#        townNetworkDemand += kinshipDemand
#        townNetworkSupply += kinshipSupply
#        # Kinship distance == 2 (grandparents, grandchildren and brothers/sisters)   
#        kinshipDemand = 0
#        kinshipSupply = 0
#        kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*2.0) 
#        for member in household:
#            if member.father != None and member.father.father != None:
#                if member.father.father.dead == False and member.father.father not in visitedPeople and member.father.father not in household and member.father.father.house.town == town:
#                    nok_Household = self.householdMembers(member.father.father)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#                if member.father.mother.dead == False and member.father.mother not in visitedPeople and member.father.mother not in household and member.father.mother.house.town == town:
#                    nok_Household = self.householdMembers(member.father.mother)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#            if member.father != None and member.mother.father != None:
#                if member.mother.father.dead == False and member.mother.father not in visitedPeople and member.mother.father not in household and member.mother.father.house.town == town:
#                    nok_Household = self.householdMembers(member.mother.father)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#                if member.mother.mother.dead == False and member.mother.mother not in visitedPeople and member.mother.mother not in household and member.mother.mother.house.town == town:
#                    nok_Household = self.householdMembers(member.mother.mother)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#            for child in member.children:
#                for grandson in child.children:
#                    if grandson.dead == False and grandson not in visitedPeople and grandson not in household and grandson.house.town == town:
#                        nok_Household = self.householdMembers(grandson)
#                        if len(nok_Household) > 0:
#                            kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                            kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                            for agent in nok_Household:
#                                visitedPeople.append(agent) 
#            if member.father != None:
#                brothers = list(set(member.father.children + member.mother.children))
#                brothers.remove(member)
#                for brother in brothers:
#                    if brother.dead == False and brother not in visitedPeople and brother not in household and brother.house.town == town:
#                        nok_Household = self.householdMembers(brother)
#                        if len(nok_Household) > 0:
#                            kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                            kinshipSupply += self.householdCareSupply(nok_Household, 2)*kinshipWeight 
#                            for agent in nok_Household:
#                                visitedPeople.append(agent)
#        townNetworkDemand += kinshipDemand
#        townNetworkSupply += kinshipSupply
#        # Kinship distance == 3 (uncles/aunts and grandchildren and nephews/nieces)   
#        kinshipDemand = 0
#        kinshipSupply = 0
#        kinshipWeight = 1/math.exp(self.p['networkDistanceParam']*3.0) 
#        for member in household:
#            paternalUncles = []
#            maternalUncles = []
#            if member.father != None and member.father.father != None:
#                paternalUncles = list(set(member.father.father.children + member.father.mother.children))
#                paternalUncles.remove(member.father)
#            if member.father != None and member.mother.father != None:    
#                maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
#                maternalUncles.remove(member.mother)
#            unclesList = list(set(maternalUncles + paternalUncles))
#            unclesList = [x for x in unclesList if x.dead == False]
#            for uncle in unclesList:
#                if uncle.dead == False and uncle not in visitedPeople and uncle not in household and uncle.house.town == town:
#                    nok_Household = self.householdMembers(uncle)
#                    if len(nok_Household) > 0:
#                        kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                        kinshipSupply += self.householdCareSupply(nok_Household, 3)*kinshipWeight 
#                        for agent in nok_Household:
#                            visitedPeople.append(agent)
#            if member.father != None:
#                brothers = list(set(member.father.children + member.mother.children))
#                brothers = [x for x in brothers if x.dead == False]
#                brothers.remove(member)
#                for brother in brothers:
#                    for child in brother.children:
#                        if child.dead == False and child not in visitedPeople and child not in household and child.house.town == town:
#                            nok_Household = self.householdMembers(child)
#                            if len(nok_Household) > 0:
#                                kinshipDemand += self.householdCareDemand(nok_Household)*kinshipWeight 
#                                kinshipSupply += self.householdCareSupply(nok_Household, 3)*kinshipWeight 
#                                for agent in nok_Household:
#                                    visitedPeople.append(agent) 
#        townNetworkDemand += kinshipDemand
#        townNetworkSupply += kinshipSupply
#        deltaNetworkCare = townNetworkDemand - townNetworkSupply
        
        if deltaHouseholdCare < 0:
            networkSocialCareParam = self.p['excessNeedParam']
        else:
            networkSocialCareParam = self.p['excessNeedParam']*self.p['careSupplyBias']
        townSCI = (networkSocialCareParam*deltaHouseholdCare*deltaNetworkCare)
        return(townSCI)

    def spousesSocialCareMap(self, person):
        household = [x for x in person.house.occupants]
        householdDemand = 0
        householdSupply = 0
        potentialIncome = 0
        for member in household:
            if member.income > 0:
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
                if member.father != None and member.mother.father != None:
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
                paternalUncles = []
                maternalUncles = []
                if member.father != None and member.father.father != None:
                    paternalUncles = list(set(member.father.father.children + member.father.mother.children))
                    paternalUncles.remove(member.father)
                if member.father != None and member.mother.father != None:
                    maternalUncles = list(set(member.mother.father.children + member.mother.mother.children))
                    maternalUncles.remove(member.mother)
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
        
#    def allocateInformalSocialCare(self):
#        careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
#        for receiver in careReceivers:
#            receiver.informalCare = 0
#            receiver.formalCare = 0
#            receiver.socialNetwork[:] = self.kinshipNetwork(receiver)
#            
#        socialCareReceivers = [x for x in self.pop.livingPeople if x.hoursSocialCareDemand > 0]
#        for receiver in socialCareReceivers:    
#            # The total supply of informal care for the agent's kinship network is computed.
#            # It includes all the informal care supply except the time-off-work infromal care supply (which is parte of the income-funded social care supply).
#            receiver.totalInformalSocialSupply = self.totalInformalSocialSupply(receiver)
         
    def allocateCare(self):
        
        # The care need is satisfied by the household's informal care supply, starting from the social care need if present.
        # First, select all the agents with care need in the population.
        careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
        for receiver in careReceivers:
            receiver.socialNetwork[:] = self.kinshipNetwork(receiver)
            
            # The total supply of informal care for the agent's kinship network is computed.
            # It includes all the informal care supply except the time-off-work infromal care supply (which is parte of the income-funded social care supply).
            receiver.totalSupply = self.totalSupply(receiver)
            #receiver.totalInformalSupply = self.totalInformalSupply(receiver)
            
        residualReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.totalSupply > 0]
        while len(residualReceivers) > 0:
            totalResidualNeed_init = sum([x.residualNeed for x in residualReceivers])
            careList = []
            for x in residualReceivers:
                if x.age < 16:
                    needWeight = x.residualNeed
                else:
                    needWeight = x.residualNeed*self.p['socialCareWeightBias']
                careList.append(needWeight)
            probReceivers = [i/sum(careList) for i in careList]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            self.getCare(receiver)
            careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
            for receiver in careReceivers:
                receiver.totalSupply = self.totalSupply(receiver)
            residualReceivers = [x for x in careReceivers if x.totalSupply > 0]
            totalResidualNeed_end = sum([x.residualNeed for x in residualReceivers])
            if totalResidualNeed_init == totalResidualNeed_end:
                print('Error: final and initial need is equal')
                
        for receiver in careReceivers:
            receiver.cumulativeUnmetNeed *= self.p['unmetCareNeedDiscountParam']
            receiver.cumulativeUnmetNeed += receiver.residualNeed
            receiver.totalDiscountedShareUnmetNeed *= self.p['shareUnmetNeedDiscountParam']
            receiver.totalDiscountedTime *= self.p['shareUnmetNeedDiscountParam']
            receiver.totalDiscountedShareUnmetNeed += receiver.residualNeed/receiver.hoursDemand
            receiver.totalDiscountedTime += 1
            receiver.averageShareUnmetNeed = receiver.totalDiscountedShareUnmetNeed/receiver.totalDiscountedTime
                
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
        if pin.father != None and pin.mother.father != None:
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
        maternalUncles = []
        paternalUncles = []
        if pin.father != None and pin.father.father != None:
            paternalUncles = list(set(pin.father.father.children + pin.father.mother.children))
            paternalUncles.remove(pin.father)
        if pin.father != None and pin.mother.father != None:   
            maternalUncles = list(set(pin.mother.father.children + pin.mother.mother.children))
            maternalUncles.remove(pin.mother)
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
            household = [x for x in carer.house.occupants]
            formalSupplyHours = household[0].residualFormalSupply
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            employed = [x for x in householdCarers if x.status == 'employed']
            # employed.sort(key=operator.attrgetter("wage"))
            totsupply = 0
            if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
                totsupply += formalSupplyHours
                if townCarer == townReceiver:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        totsupply += member.residualInformalSupply
            else:
                if townCarer == townReceiver:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
            
            supplies.append(totsupply)

        totalSupply = sum(supplies)
        return(totalSupply)
    
#    def totalInformalSocialSupply(self, receiver):
#        totalSupply = 0
#        townReceiver = receiver.house.town 
#        networkList = []
#        supplies = []
#        for i in range(len(receiver.socialNetwork)):
#            for j in receiver.socialNetwork[i]:
#                networkList.append(j)
#        for carer in networkList:
#            townCarer = carer.house.town
#            household = [x for x in carer.house.occupants]
#            householdCarers = [x for x in household if x.hoursDemand == 0]
#            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
#            employed = [x for x in householdCarers if x.status == 'employed']
#            earners = [x for x in notWorking if x.status == 'retired']
#            earners.extend(employed)
#            incomeForCare = 0
#            if len(earners) > 0:
#                incomeForCare = earners[0].residualIncomeCare
#            totsupply = 0
#            if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
#                if townCarer != townReceiver:
#                    formalCare = incomeForCare/self.p['priceSocialCare']
#                    totsupply += int((formalCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#                else:
#                    for member in notWorking:
#                        totsupply += member.residualInformalSupply
#                    for member in employed:
#                        totsupply += member.extraworkCare
#                        if member.wage > self.p['priceSocialCare'] or member.status == 'retired':
#                            # For member is more convenient (or is possible) to pay for formal care
#                            totsupply += member.residualFormalSupply
#                        else:   
#                            # For member is more convenient to take time off work.
#                            totsupply += member.residualInformalSupply
#            else:
#                if townCarer == townReceiver:
#                    for member in notWorking:
#                        totsupply += member.residualInformalSupply
#                    for member in employed:
#                        totsupply += member.extraworkCare
#            
#            supplies.append(totsupply)
#
#        totalSupply = sum(supplies)
#        return(totalSupply)
    
    
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
        
#        print('')
#        for h in household:
#            print('ID: ' + str(h.id))
#            print('Status: ' + str(h.status))
#            print('Income: ' + str(h.income))
#            print('Residual Income Care: ' + str(h.hoursFormalSupply))
#            
#        houseIncome = self.householdIncome(household)
#        
#            
#        print('Household income: ' + str(houseIncome))

        residualFormalSupplyHours = household[0].residualFormalSupply
        householdCarers = [x for x in household if x.hoursDemand == 0]
        notWorking = [x for x in householdCarers if x.residualInformalSupply > 0]
        
        householdsGroups = []
        groupsAvailability = []
        
        teenagers = [x for x in notWorking if x.status == 'teenager']
        teenagers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        householdsGroups.append(teenagers)
        totTeenagersSupply = sum([x.residualInformalSupply for x in teenagers])
        groupsAvailability.append(totTeenagersSupply)

        retired = [x for x in notWorking if x.status == 'retired']
        retiredIncome = sum([x.income for x in retired])
#        print(len(retired))
#        print('Retired income: ' + str(retiredIncome))
        
        retired.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        householdsGroups.append(retired)
        totRetiredSupply = sum([x.residualInformalSupply for x in retired])
        groupsAvailability.append(totRetiredSupply)
        
        students = [x for x in notWorking if x.status == 'student']
        students.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        householdsGroups.append(students)
        totStudentsSupply = sum([x.residualInformalSupply for x in students])
        groupsAvailability.append(totStudentsSupply)
        
        unemployed = [x for x in notWorking if x.status == 'unemployed']
        unemployed.sort(key=operator.attrgetter("wage"))
        householdsGroups.append(unemployed)
        totUnemployedSupply = sum([x.residualInformalSupply for x in unemployed])
        groupsAvailability.append(totUnemployedSupply)
        
        employed_1 = [x for x in householdCarers if x.status == 'employed' and x.extraworkCare > 0]
        employed_1.sort(key=operator.attrgetter("extraworkCare"), reverse=True)
        householdsGroups.append(employed_1)
        extraWorkSupply = sum([x.extraworkCare for x in employed_1])
        groupsAvailability.append(extraWorkSupply)
        
        employed_2 = [x for x in householdCarers if x.status == 'employed' and x.residualInformalSupply > 0]
        employed_2.sort(key=operator.attrgetter("wage"))
        householdsGroups.append('Out-of-Income Supply')
        totOutOfIncomeSupply = sum([x.residualInformalSupply for x in employed_2])
        totOutOfIncomeSupply += residualFormalSupplyHours
        groupsAvailability.append(totOutOfIncomeSupply)
        
        employed = list(set().union(employed_1, employed_2))
        employedIncome = sum([x.income for x in employed])
#        print(len(employed))
#        print('Employed income:' + str(employedIncome))
        
        groupsProbabilities = [x/sum(groupsAvailability) for x in groupsAvailability]
        
        earningMembers = [x for x in household if x.income > 0]
        
        if len(earningMembers) == 0 and totOutOfIncomeSupply > 0:
            print('Error: no income to pay social care from (Get Care)')
            
        # Finally, extract a 'quantum' of care from one of the selected household's members.
        check = 0
        supplier = 'none'
        if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
            if townCarer == townReceiver:
                carers = np.random.choice(householdsGroups, p = groupsProbabilities) 
                if carers == 'Out-of-Income Supply':
                    if len(employed_2) > 0:
                        employed_2[0].residualInformalSupply -= self.p['quantumCare']
                        employed_2[0].socialWork += self.p['quantumCare']
                        informalCare = self.p['quantumCare']
                        supplier = 'employed: informal care (close relative, in town)'
                    else:
                        residualFormalSupplyHours -= self.p['quantumCare']
                        if residualFormalSupplyHours <= 0:
                            residualFormalSupplyHours = 0
                        for agent in household:
                            agent.residualFormalSupply = residualFormalSupplyHours
                        earningMembers[0].workToCare += self.p['quantumCare']
                        formalCare = self.p['quantumCare']
                        supplier = 'employed: formal care (close relative, in town)'
                else:
                    if carers[0].status == 'employed':
                        carers[0].extraworkCare -= self.p['quantumCare']
                    else:
                        carers[0].residualInformalSupply -= self.p['quantumCare']
                    carers[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
                    
                # Sequential supply    
                
#                if len(teenagers) > 0:
#                    teenagers[0].residualInformalSupply -= self.p['quantumCare']
#                    teenagers[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                elif len(retired) > 0:
#                    retired[0].residualInformalSupply -= self.p['quantumCare']
#                    retired[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                    supplier = 'retired (close relative, in town)'
#                elif len(students) > 0:
#                    students[0].residualInformalSupply -= self.p['quantumCare']
#                    students[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                    supplier = 'student (close relative, in town)'
#                elif len(unemployed) > 0:
#                    for member in unemployed:
#                        if member.residualInformalSupply > 0:
#                            member.residualInformalSupply -= self.p['quantumCare']
#                            member.socialWork += self.p['quantumCare']
#                            informalCare = self.p['quantumCare']
#                            supplier = 'unemployed (close relative, in town)'
#                            break
#                elif len(employed) > 0:
#                    for member in employed:
#                        if member.extraworkCare > 0:
#                            member.socialWork += self.p['quantumCare']
#                            member.extraworkCare -= self.p['quantumCare']
#                            informalCare = self.p['quantumCare']
#                            supplier = 'employed: extraworkCare (close relative, in town)'
#                            break
#                        else:
#                            if member.wage < self.p['priceSocialCare']: 
#                                if member.residualInformalSupply > 0:
#                                    # member.residualInformalSupply -= self.p['quantumCare']
#                                    residualIncomeForCare -= self.p['quantumCare']*member.wage
#                                    if residualIncomeForCare <= 0:
#                                        residualIncomeForCare = 0
#                                    for agent in household:
#                                        agent.residualFormalSupply = residualIncomeForCare
#                                    self.workerInformalCareSupply(employed, residualIncomeForCare)
#                                    member.socialWork += self.p['quantumCare']
#                                    informalCare = self.p['quantumCare']
#                                    supplier = 'employed: informal care (close relative, in town)'
#                                    break
#                            else: 
#                                if formalSupplyHours >= 0:
#                                    # formalSupplyHours -= self.p['quantumCare']
#                                    residualIncomeForCare -= self.p['quantumCare']*self.p['priceSocialCare']
#                                    if residualIncomeForCare <= 0:
#                                        residualIncomeForCare = 0
#                                    for agent in household:
#                                        agent.residualFormalSupply = residualIncomeForCare
#                                    self.workerInformalCareSupply(employed, residualIncomeForCare)
#                                    member.workToCare += self.p['quantumCare']
#                                    formalCare = self.p['quantumCare']
#                                    supplier = 'employed: formal care (close relative, in town)'
#                                    break
            else:
                if residualFormalSupplyHours > 0:
                    residualFormalSupplyHours -= self.p['quantumCare']
                    if residualFormalSupplyHours <= 0:
                        residualFormalSupplyHours = 0
                    for agent in household:
                        agent.residualFormalSupply = residualFormalSupplyHours
                    earningMembers[0].workToCare += self.p['quantumCare']
                    formalCare = self.p['quantumCare']
                    supplier = 'employed: formal care (close relative, not in town)'
        else:
            if townCarer == townReceiver: 
                groupsAvailability[-1] = 0.0
                groupsProbabilities = [x/sum(groupsAvailability) for x in groupsAvailability]
                carers = np.random.choice(householdsGroups, p = groupsProbabilities)
                if carers[0].status == 'employed':
                    carers[0].extraworkCare -= self.p['quantumCare']
                else:
                    carers[0].residualInformalSupply -= self.p['quantumCare']
                carers[0].socialWork += self.p['quantumCare']
                informalCare = self.p['quantumCare']
                
                # Sequential supply
                
#                if len(teenagers) > 0:
#                    teenagers[0].residualInformalSupply -= self.p['quantumCare']
#                    teenagers[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                elif len(retired) > 0:
#                    retired[0].residualInformalSupply -= self.p['quantumCare']
#                    retired[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                    supplier = 'retired (not close relative, in town)'
#                elif len(students) > 0:
#                    students[0].residualInformalSupply -= self.p['quantumCare']
#                    students[0].socialWork += self.p['quantumCare']
#                    informalCare = self.p['quantumCare']
#                    supplier = 'student (not close relative, in town)'
#                elif len(unemployed) > 0:
#                    for member in unemployed:
#                        if member.residualInformalSupply > 0:
#                            member.residualInformalSupply -= self.p['quantumCare']
#                            member.socialWork += self.p['quantumCare']
#                            informalCare = self.p['quantumCare']
#                            supplier = 'unemployed (not close relative, in town)'
#                            break
#                elif len(employed) > 0:
#                    for member in employed:
#                        if member.extraworkCare > 0:
#                            member.socialWork += self.p['quantumCare']
#                            member.extraworkCare -= self.p['quantumCare']
#                            informalCare = self.p['quantumCare']
#                            supplier = 'employed (not close relative, in town)'
#                            break
                       # employed[0].residualInformalSupply -= self.p['quantumCare']
                       # employed[0].residualSupply -= self.p['quantumCare']
                       # employed[0].socialWork += self.p['quantumCare']
                       # informalCare = self.p['quantumCare']
        
        receiver.informalCare += informalCare
        receiver.formalCare += formalCare
        receiver.informalSupplyByKinship[indexSupply[index]] += informalCare
        receiver.formalSupplyByKinship[indexSupply[index]] += formalCare
        if informalCare == 0 and formalCare == 0:
            print('Error: no care is transferred')
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
            formalSupplyHours = household[0].residualFormalSupply
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student' or x.status == 'unemployed']
            employed = [x for x in householdCarers if x.status == 'employed']
            weightedHouseholdSupply = 0
            totsupply = 0
            if (receiver.father != None and receiver.father in carer.house.occupants) or (receiver.mother != None and receiver.mother in carer.house.occupants) or carer in receiver.children:
                if townCarer != townReceiver:
                    totsupply += formalSupplyHours
                else:
                    for member in notWorking:
                        totsupply += member.residualInformalSupply
                    for member in employed:
                        totsupply += member.extraworkCare
                        if member.wage < self.p['priceSocialCare']:
                            totsupply += member.residualInformalSupply
                    totsupply += formalSupplyHours
            else:
                if townCarer == townReceiver:
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
            # if self.year >= self.p['implementPoliciesFromYear']:
            person.qaly = self.p['qalyIndexes'][person.careNeedLevel] #/math.pow(1+self.p['qalyDiscountRate'], person.yearAfterPolicy)
                # person.yearAfterPolicy += 1
            if person.status == 'child' and person.age >= self.p['ageTeenagers']:
                person.status = 'teenager'
            # person.justMarried = None
            
        for person in self.pop.livingPeople:
            if person.status == 'student':
                person.yearOfSchoolLeft -= 1
            if person.status == 'maternity':
                minAge = min([x.age for x in person.children])
                if minAge > 0:
                    person.babyCarer == False
                    if person.yearOfSchoolLeft == 0:
                        self.enterWorkForce(person)
                    else:
                        person.status = 'student'
            
        activePop = [x for x in self.pop.livingPeople if x.status != 'inactive']
        
        for person in activePop:
            if person.age == (self.p['ageOfRetirement'] + self.p['ageOfRetirementPolicyChange']) and person.status != 'inactive':
                person.status = 'retired'
                person.income = self.p['pensionWage'][person.classRank]*self.p['weeklyHours']
                person.disposableIncome = person.income
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " has now retired.")
    
    
    def computeNetIncome(self):
        employedPop = [x for x in self.pop.livingPeople if x.status == 'employed']
        for person in employedPop:
            careWorkingHours = person.socialWork - self.p['employedHours']
            if careWorkingHours < 0:
                careWorkingHours = 0
            workingHours = float(max(self.p['weeklyHours'] - careWorkingHours, 0))
            workTime = workingHours/float(self.p['weeklyHours'])
            person.netIncome = workTime*person.income
        self.updateNetIncomeStat()
                
    def healthServiceCost(self):
        self.hospitalizationCost = 0
        peopleWithUnmetNeed = [x for x in self.pop.livingPeople if x.cumulativeUnmetNeed != 0 and x.careNeedLevel > 0]
        for person in peopleWithUnmetNeed:
            needLevelFactor = math.pow(self.p['needLevelParam'], person.careNeedLevel)
            unmetSocialCareFactor = math.pow(self.p['unmetSocialCareParam'], person.averageShareUnmetNeed)
            averageHospitalization = self.p['hospitalizationParam']*needLevelFactor*unmetSocialCareFactor
            self.hospitalizationCost += averageHospitalization*self.p['costHospitalizationPerDay']
#            alfa = math.exp(self.p['unmetCareHealthParam']*person.cumulativeUnmetNeed)
#            hospitalizationProb = (alfa - 1)/alfa
#            if random.random() < hospitalizationProb:
#                 # Hospitalization Lenght (depends on kinship network)
#                 # Function for number of days in hospital
#                 self.hospitalizationCost += self.p['costPerHospitalization']
    
    def socialTransition(self):
        
        activePop = [x for x in self.pop.livingPeople if x.status != 'inactive']
        
        for person in activePop:
            if person.age == self.p['minWorkingAge']:
                person.status = 'student'
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 0)
                if random.random() > probStudy:
                    # person.classRank = 0
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 1
                    person.yearOfSchoolLeft = 2
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now a student.")
            if person.age >= 18 and person.status == 'student' and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 1:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 1)
                if random.random() > probStudy:
                    # person.classRank = 1
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 2
                    person.yearOfSchoolLeft = 2
            if person.age >= 20 and person.status == 'student' and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 2:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 2)
                if random.random() > probStudy:
                    # person.classRank = 2
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 3
                    person.yearOfSchoolLeft = 2
            if person.age >= 22 and person.status == 'student' and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 3:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 3)
                if random.random() > probStudy:
                    # person.classRank = 3
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 4
                    person.yearOfSchoolLeft = 2
            if person.age >= 24 and person.status == 'student' and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 4:
                # person.classRank = 4
                person.yearOfSchoolLeft = 0
                person.classRank = person.temporaryClassRank
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
         
            if person.status == 'student' and person.mother.dead and person.father.dead:
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")

    def transitionProb (self, person, stage):
        household = [x for x in person.house.occupants]
        if person.father.dead + person.mother.dead != 2:
            pStudy = 0
            disposableIncome = 0
            perCapitaDisposableIncome = self.computeDisposableIncome(household)/float(len(household))
            
            # print('Per Capita Disposable Income: ' + str(perCapitaDisposableIncome))
            
            if perCapitaDisposableIncome > 0.0:
                forgoneSalary = self.p['incomeInitialLevels'][stage]*self.p['weeklyHours']
                educationCosts = self.p['educationCosts'][stage]*self.p['educationCostsPolicyCoefficient']
                relCost = (forgoneSalary+educationCosts)/perCapitaDisposableIncome
                
                # Check variable
                self.relativeEducationCost.append(relCost) # 0.2 - 5
                
                incomeEffect = self.p['costantIncomeParam']/(math.exp(self.p['eduWageSensitivity']*relCost) + (self.p['costantIncomeParam']-1)) # Min-Max: 0 - 10
                targetEL = max(person.father.classRank, person.mother.classRank)
                dE = targetEL - stage
                expEdu = math.exp(self.p['eduRankSensitivity']*dE)
                educationEffect = expEdu/(expEdu+self.p['costantEduParam'])
                careEffect = 1/math.exp(self.p['careEducationParam']*person.socialWork)
                pStudy = incomeEffect*educationEffect*careEffect
                # pStudy = math.pow(incomeEffect, self.p['incEduExp'])*math.pow(educationEffect, 1-self.p['incEduExp'])
                if pStudy < 0:
                    pStudy = 0
                # Check
                self.probKeepStudying.append(pStudy)
                self.stageStudent.append(stage)
                
            else:
                # print('perCapitaDisposableIncome: ' + str(perCapitaDisposableIncome))
                pStudy = 0
        else:
            pStudy = 0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        #pStudy = 0.8
        return (pStudy)
    
    def wagesGrowth(self):
        for i in range(self.p['numberClasses']):
            self.p['pensionWage'][i] *= self.p['wageGrowthRate']
            self.p['incomeInitialLevels'][i] *= self.p['wageGrowthRate']
            self.p['incomeFinalLevels'][i] *= self.p['wageGrowthRate']
        for i in range(4):
            self.p['educationCosts'][i] *= self.p['wageGrowthRate']
        self.p['pricePublicSocialCare'] *= self.p['wageGrowthRate']
        self.p['priceSocialCare'] *= self.p['wageGrowthRate']    
            
            
    def enterWorkForce(self, person):
        person.status = 'unemployed'
        person.wage = self.marketWage(person)
        person.income = 0
        person.disposableIncome = 0
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
            if i.partner == None:
                # Men need to be employed to marry
                if i.sex == 'male' and i.status == 'employed':
                    eligibleMen.append(i)
                    
        ######     Otional: select a subset of eligible men based on age    ##########################################
        potentialGrooms = []
        for m in eligibleMen:
            incomeFactor = (math.exp(self.p['incomeMarriageParam']*m.income)-1)/math.exp(self.p['incomeMarriageParam']*m.income)
            manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][m.age/10]*incomeFactor # add income: *
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
                    studentFactor = 1.0
                    if woman.status == 'student':
                        studentFactor = self.p['studentFactorParam']
                    womanTown = woman.house.town
                    geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                    geoFactor = 1/math.exp(self.p['betaGeoExp']*geoDistance)
                    statusDistance = float(abs(man.classRank-woman.classRank))/float((self.p['numberClasses']-1))
                    if man.classRank < woman.classRank:
                        betaExponent = self.p['betaSocExp']
                    else:
                        betaExponent = self.p['betaSocExp']*self.p['rankGenderBias']
                    socFactor = 1/math.exp(betaExponent*statusDistance)
                    ageFactor = self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                    marriageProb = geoFactor*socFactor*ageFactor*studentFactor
                    bridesWeights.append(marriageProb)
                if sum(bridesWeights) > 0:
                    bridesProb = [i/sum(bridesWeights) for i in bridesWeights]
                    woman = np.random.choice(potentialBrides, p = bridesProb)
                else:
                    woman = np.random.choice(potentialBrides)
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
                if numclassPop > 0:
                    ageBandShares.append(count/numclassPop)
                else:
                    ageBandShares.append(0)
        
        
        if self.year == self.p['implementPoliciesFromYear']:
            for i in range(self.p['numberClasses']):
                for j in range(6):
                    self.meanUnemploymentRates[i][j] = np.mean(self.unemploymentRateClasses[i][j])
        
        for person in activePop:
            
            if self.year < self.p['implementPoliciesFromYear']:
                person.unemploymentRate = self.unemploymentRate(classShares, ageBandShares, self.p['unemploymentClassBias'], 
                                                             self.p['unemploymentAgeBias'], unemployment, 
                                                             self.ageBand(person.age), person.classRank)
                
                if  self.year >= self.p['startRegressionCollectionFrom']:
                    self.unemploymentRateClasses[person.classRank][self.ageBand(person.age)].append(person.unemploymentRate)
                    
            else:
                person.unemploymentRate = self.meanUnemploymentRates[person.classRank][self.ageBand(person.age)]
                
            
            
            
            
    def updateJobMap(self):
        
        # This function computes the class-specific 'weight' of towns in the job market, 
        # that is, an index that represents the relative importance of a town in the job market 
        # for a particular socio-economic class.
        # The weight is a weighted average of the towns' relative size and the class-specific towns' relative size
        # (i.e. the share of individuals of a particular class living in that town).
        # The assumptions are that:
        # - the bigger a town the greater his weight in the job market;
        # - the greater the share of people of a certain class living in a town the greater the availability of jobs specific to that class, in that town.
        # This weight is used to determine:
        # - the probability that an individual's new job opportunity will come from a particular town;
        # - the discounting factor of the expected income of unemployed people (which depends on how likely is that they will find a job in a particular town).
        
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
                if numclassPop > 0:
                    ageBandShares.append(count/numclassPop)
                else:
                    ageBandShares.append(0)
            
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
                    
                    self.changeJobRate.append(jobMobilityRate)
                    
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
                            
                            # Check variables
                            self.changeJobdIncome.append(deltaIncome)
                            self.relocationCareLoss.append(relocationNetLoss)
                            
                            deltaIncomeFactor = math.exp(self.p['deltaIncomeExp']*deltaIncome)/(math.exp(self.p['deltaIncomeExp']*deltaIncome)+1) # Min-Max: -70 - 73
                            careLossFactor = 1/math.exp(self.p['relocationCareLossExp']*relocationNetLoss) # Min-Max: 0 - 17
                            # The probability to change job depends both on the wage increase and the cost of relocating 
                            changeWeight = math.pow(deltaIncomeFactor, self.p['incomeSocialCostRelativeWeight'])*math.pow(careLossFactor, 1-self.p['incomeSocialCostRelativeWeight'])
                            changeWeights.append(changeWeight)
                            person.searchJob = False
                        changeProbs = [i/sum(changeWeights) for i in changeWeights]
                        if len([x for x in changeProbs if x != 0]) >= jobChanges:
                            peopleToChange = np.random.choice(employed, jobChanges, replace = False, p = changeProbs)
                        else:
                            jobChanges = len([x for x in changeProbs if x != 0])
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
                if numclassPop > 0:
                    ageBandShares.append(count/numclassPop)
                else:
                    ageBandShares.append(0)
            
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
                        # Unemployed people who engage more in social work will be penalized in finding a job (less job search).
                        # The parameter which 'weights' this penalization is: p['unemployedCareBurdernParam']
                        unemployedWeights = [1/math.exp(self.p['unemployedCareBurdernParam']*x.socialWork) for x in unemployed]
                        unemployedProbs = [x/sum(unemployedWeights) for x in unemployedWeights]
                        peopleToHire = np.random.choice(unemployed, peopleToHire, replace = False, p = unemployedProbs)
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
        
        # Check variable
        self.townJobAttraction.append(townJobDensity) # MIn-Max: 0.006 - 0.07
        
        townFactor = math.exp(self.p['incomeDiscountingExponent']*townJobDensity) # + self.p['incomeDiscountingParam']))
        discountingFactor = person.unemploymentRate/townFactor
        
        if np.isnan(person.unemploymentRate):
            print('Error: unemploymentRate is NAN!')
            
        # Check variable
        self.unemployedIncomeDiscountingFactor.append(discountingFactor) # Min-Max: 0.99 - 0.999
        
        expIncome = income*math.exp(-1*discountingFactor*self.p['discountingMultiplier'])#discountingFactor
        if np.isnan(expIncome):
            print('Error: expIncome is NAN!')
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
        if a > 0:
            lowerAgeBandRate = classRate/a 
        else:
            lowerAgeBandRate = 0
        unemploymentRate = lowerAgeBandRate*ageBias[ageBand]
        return (unemploymentRate)
    
    def computeTownSocialAttraction(self, agent):
        potentialIncome = 0
        household = [agent]
        household.extend([x for x in agent.children if x.dead == False and x.house == agent.house])
        numHousehold = len(household)
        count = 0
        for member in household:
            if member.income > 0:
                potentialIncome += member.income
                count += 1
            elif member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, member.house.town)
                count += 1
        household = [agent.partner]        
        household.extend([x for x in agent.partner.children if x.dead == False and x.house == agent.partner.house])
        numHousehold += len(household)
        for member in household:
            if member.status == 'retired':
                potentialIncome += member.income
                count += 1
            if member.status == 'employed' or member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, agent.house.town)
                count += 1
        perCapitaIncome = potentialIncome/float(numHousehold)
        
        rcA = math.pow(float(agent.partner.yearsInTown), self.p['yearsInTownSensitivityParam'])
        children = [x for x in agent.partner.children if x.dead == False and x.house == agent.partner.house]
        for child in children:
            rcA += math.pow(float(child.yearsInTown), self.p['yearsInTownSensitivityParam'])
        rcA *= self.p['relocationCostParam']
        
#        if perCapitaIncome == 0:
#            print('Error: per capita income equal to zero')
#        print('Total Income:' + str(potentialIncome))
#        print('Number earners: ' + str(count))
#        print('Per Capita Income:' + str(perCapitaIncome))
#        print('Household components:' + str(numHousehold))
#        print(agent.sex)
#        print(agent.status)
#        print(agent.income)
#        print(self.expectedIncome(agent, agent.house.town))
#        print(agent.partner.sex)
#        print(agent.partner.status)
#        print(agent.partner.income)
#        print(self.expectedIncome(agent.partner, agent.house.town))
#        print('')
        
        
        socialAttraction = (self.spousesCareLocation(agent) - rcA)/perCapitaIncome
        
        attractionFactor = math.exp(self.p['propensityRelocationParam']*socialAttraction)
        relativeAttraction = attractionFactor/(attractionFactor + 1)
        return (relativeAttraction)
    
    def computeRelocationsCost(self, agent):
        
        potentialIncome = 0
        for member in agent.house.occupants:
            if member.income > 0:
                potentialIncome += member.income
            elif member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, member.house.town)
        perCapitaIncome = potentialIncome/float(len(agent.house.occupants))
        
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
        
        # Check variable
        self.relocationCost.append(rcA)  # Min-Max: 0 - 8
        
        rcA *= self.p['relocationCostParam']

        townAttractions = []
        index = 0
        for town in self.map.towns:
            if town == agent.house.town:
                townAttraction = agent.socialCareMap[index]/perCapitaIncome # Min-Max: -60 - +30 (*networkSocialCareParam)
            else:
                townAttraction = (agent.socialCareMap[index] - rcA)/perCapitaIncome
                
            # Check variable
            self.townRelocationAttraction.append(townAttraction) 
            
            townAttractions.append(townAttraction)
            index += 1
        return (townAttractions)
        
    def relocationPropensity(self, relocationCost, agent):  
        
        potentialIncome = 0
        for member in agent.house.occupants:
            if member.income > 0:
                potentialIncome += member.income
            elif member.status == 'unemployed':
                potentialIncome += self.expectedIncome(member, member.house.town)
        perCapitaIncome = potentialIncome/float(len(agent.house.occupants))
        
        propensities = []
        index = 0
        for town in self.map.towns:
            relativeAttraction = relocationCost[index] # /perCapitaIncome
            
            if relativeAttraction > 5:
                print('Relative Attraction: ' + str(relativeAttraction))
                print('Per Capita Income: ' + str(perCapitaIncome))
                relativeAttraction = 5
            #if relativeAttraction > 0.5:
              #  print('Relative Attraction is:')
              #  print(relativeAttraction)
            # Check variable
            
            self.relativeTownAttraction.append(relativeAttraction) # Min-Max: -0.07 - 0.05
            
            attractionFactor = math.exp(self.p['propensityRelocationParam']*relativeAttraction)
            rp = attractionFactor/(attractionFactor + self.p['denRelocationWeight'])
            
            # Check variable
            self.townRelativeAttraction.append(rp) # 0.87 - 0.9
            
            propensities.append(rp)
            index += 1
        return(propensities)
    
    def changeJob(self, a):
        if a.status == 'unemployed':
            self.enterWork += 1
        if a.status == 'employed':
            a.jobChange = True
        a.status = 'employed'
        if a.ageStartWorking == -1:
            a.ageStartWorking = a.age
        a.wage = a.newWage
        a.hourlyWage = a.wage
        a.income = a.wage*self.p['weeklyHours']
        a.disposableIncome = a.income
        a.finalIncome = a.newK
        a.jobLocation = a.newTown
        a.jobTenure = 0
        a.searchJob = False
        if a.independentStatus == False:
            if a.jobLocation != a.house.town:
                self.findNewHouse([a], a.newTown)
                a.independentStatus = True
                    
    def leaveJob(self, person):
            self.exitWork += 1
            person.status = 'unemployed'
            person.wage = self.marketWage(person)
            person.hourlyWage = 0
            person.income = 0
            person.disposableIncome = 0
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
        
        # This function determines (and returns) the probabilities associated to the locatin of new job opportunities.
        # They are proportional to the product of two factors:
        # - an objective factor represented by the town's job 'weight' for that particular class (see 'jobMarketMap' function);
        # - a subjective factor represented by the town's care attractiveness for that particular agent
        
        townDensity = []
        index = 0
        for t in self.map.towns:
            townSocialAttraction = relocPropensity[index]
            townDensity.append(self.jobMarketMap[classRank][index]*townSocialAttraction)
            
            # Check
            self.townsJobProb.append(self.jobMarketMap[classRank][index]*townSocialAttraction)
            
            index += 1
        sumDensity = sum(townDensity)
        relTownDensity = [i/sumDensity for i in townDensity]
        return(relTownDensity)            
            
    def updateWork(self, person):
        person.workingTime *= self.p['workDiscountingTime']
        workTime = 0
        if person.status == 'employed':
            person.jobTenure += 1
            careWorkingHours = person.socialWork - self.p['employedHours']
            if careWorkingHours < 0:
                careWorkingHours = 0
            workingHours = float(max(self.p['weeklyHours'] - careWorkingHours, 0))
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
            person.hourlyWage = person.wage
        else:
            person.income = 0
            person.hourlyWage = 0
            
     
    def computeDisposableIncome(self, household):
        disposableIncome = 0
        for person in household:
            if person.income > 0:
                if person.status == 'retired' or person.status == 'inactive':
                    disposableIncome += person.income - person.workToCare*self.p['priceSocialCare']
                else:
                    careWorkingHours = person.socialWork - self.p['employedHours']
                    if careWorkingHours < 0:
                        careWorkingHours = 0
                    workingHours = float(max(self.p['weeklyHours'] - careWorkingHours, 0))
                    workTime = workingHours/float(self.p['weeklyHours'])
                    disposableIncome += workTime*person.income - person.workToCare*self.p['priceSocialCare']
#        elif person.status == 'unemployed':
#            disposableIncome = self.expectedIncome(person, person.house.town)*workTime
        if disposableIncome < 0:
            disposableIncome = 0
        return(disposableIncome)
    
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
                classRank = max([x.classRank for x in peopleToMove])
                if classRank == 0:
                    self.jobRelocations_1 += 1 
                if classRank == 1:
                    self.jobRelocations_2 += 1 
                if classRank == 2:
                    self.jobRelocations_3 += 1 
                if classRank == 3:
                    self.jobRelocations_4 += 1 
                if classRank == 4:
                    self.jobRelocations_5 += 1 
                
                self.findNewHouse(peopleToMove, person.jobLocation)
                
                
    
    def joiningSpouses(self):
        
        for person in self.pop.livingPeople:
            
            # ageClass = person.age / 10       
            if person.partner != None and person.house != person.partner.house:

                #person.movedThisYear = True
                #person.partner.movedThisYear = True
                if person.house.town != person.partner.house.town:
                    personTownAttraction = self.computeTownSocialAttraction(person)
                    partnerTownAttraction = self.computeTownSocialAttraction(person.partner)
                else:
                    personTownAttraction = 1.0
                    partnerTownAttraction = 1.0
                
                # 1st case: both partners living with parents.
                # Find a new home near the highest earning partner
                check = 0
                if person.independentStatus + person.partner.independentStatus == 0:
                    check = 1
                    person.independentStatus = True
                    person.partner.independentStatus = True
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
                    # self.spousesSocialCareMap(person)
                    continue
                
                # 2nd case: one living alone and the other living with parents
                # If in the same town: move in the house of independent partner
                # If in different towns: move in the house of independent partner
                #                        if higher income, otherwise find new house
                #                        near other partner.
                
                
                elif person.independentStatus + person.partner.independentStatus == 1:
                    if check == 1:
                        print('Error: couple already joined')
                    else:
                        check = 1
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
                    
                    if a.house.town == b.house.town:
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
                            # self.spousesSocialCareMap(a)
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
                            # self.spousesSocialCareMap(a)
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
                                # self.spousesSocialCareMap(a)
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
                                # self.spousesSocialCareMap(a)
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
                            # self.spousesSocialCareMap(a)
                            continue
                        
                # 3rd case: both living alone
                
                elif person.independentStatus + person.partner.independentStatus == 2:
                    if check == 1:
                        print('Error: couple already joined')
                    else:
                        check = 1
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
                                # self.spousesSocialCareMap(a)
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
                                # self.spousesSocialCareMap(a)
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
                            # self.spousesSocialCareMap(a)
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
                            # self.spousesSocialCareMap(a)
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
                    count += self.p['classAffinityWeight']/math.pow(self.manhattanDistance(h, x), self.p['geoDistanceSensitivityParam'])
                else:
                    socialDistance = math.pow(abs(x.occupants[0].classRank-classRank), self.p['socDistanceSensitivityParam'])
                    count -= socialDistance/math.pow(self.manhattanDistance(h, x), self.p['geoDistanceSensitivityParam'])
                # Softmax function
                
            # Check variable
            self.houseScore.append(count) # Min-Max: -10 - 1
            
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
    
    def updateNetIncomeStat(self):
        employed_1 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 0]
        employed_1_Males = [x for x in employed_1 if x.sex == 'male']
        employed_1_Females = [x for x in employed_1 if x.sex == 'female']
        
        employed_2 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 1]
        employed_2_Males = [x for x in employed_2 if x.sex == 'male']
        employed_2_Females = [x for x in employed_2 if x.sex == 'female']
        
        employed_3 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 2]
        employed_3_Males = [x for x in employed_3 if x.sex == 'male']
        employed_3_Females = [x for x in employed_3 if x.sex == 'female']
        
        employed_4 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 3]
        employed_4_Males = [x for x in employed_4 if x.sex == 'male']
        employed_4_Females = [x for x in employed_4 if x.sex == 'female']
        
        employed_5 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 4]
        employed_5_Males = [x for x in employed_5 if x.sex == 'male']
        employed_5_Females = [x for x in employed_5 if x.sex == 'female']
        
        averageMalesIncome = 0
        averageFemalesIncome = 0
        employedMales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'male']
        
        if len(employedMales) > 0:
            averageMalesIncome = sum([x.netIncome for x in employedMales])/float(len(employedMales))
        else:
            averageMalesIncome = 0
        self.averageIncome_M.append(averageMalesIncome)
        
        employedFemales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'female']
        if len(employedFemales) > 0:
            averageFemalesIncome = sum([x.netIncome for x in employedFemales])/float(len(employedFemales))
        else:
            averageFemalesIncome = 0
        self.averageIncome_F.append(averageFemalesIncome)
        
        if averageMalesIncome > 0:
            self.ratioWomenMaleIncome.append(averageFemalesIncome/averageMalesIncome)
        else:
            self.ratioWomenMaleIncome.append(0)
        
        income_1 = sum([x.netIncome for x in employed_1])
        income_1_Males = sum([x.netIncome for x in employed_1_Males])
        income_1_Females = sum([x.netIncome for x in employed_1_Females])
        if len(employed_1) > 0:
            averageIncome = income_1/float(len(employed_1))
        else:
            averageIncome = 0
        self.averageIncome_1.append(averageIncome)
        
        averageIncome_M = 0
        averageIncome_F = 0
        if len(employed_1_Males) > 0:
            averageIncome_M = income_1_Males/float(len(employed_1_Males))
        else:
            averageIncome_M = 0
        self.averageIncome_1_Males.append(averageIncome_M)
        if len(employed_1_Females) > 0:
            averageIncome_F = income_1_Females/float(len(employed_1_Females))
        else:
            averageIncome_F = 0
        self.averageIncome_1_Females.append(averageIncome_F)
        
        if averageIncome_M > 0:
            self.ratioWomenMaleIncome_1.append(averageIncome_F/averageIncome_M)
        else:
            self.ratioWomenMaleIncome_1.append(0)
        
        income_2 = sum([x.netIncome for x in employed_2])
        income_2_Males = sum([x.netIncome for x in employed_2_Males])
        income_2_Females = sum([x.netIncome for x in employed_2_Females])
        if len(employed_2) > 0:
            averageIncome = income_2/float(len(employed_2))
        else:
            averageIncome = 0
        self.averageIncome_2.append(averageIncome)
        
        averageIncome_M = 0
        averageIncome_F = 0
        if len(employed_2_Males) > 0:
            averageIncome_M = income_2_Males/float(len(employed_2_Males))
        else:
            averageIncome_M = 0
        self.averageIncome_2_Males.append(averageIncome_M)
        if len(employed_2_Females) > 0:
            averageIncome_F = income_2_Females/float(len(employed_2_Females))
        else:
            averageIncome_F = 0
        self.averageIncome_2_Females.append(averageIncome_F)
        
        if averageIncome_M > 0:
            self.ratioWomenMaleIncome_2.append(averageIncome_F/averageIncome_M)
        else:
            self.ratioWomenMaleIncome_2.append(0)
        
        income_3 = sum([x.netIncome for x in employed_3])
        income_3_Males = sum([x.netIncome for x in employed_3_Males])
        income_3_Females = sum([x.netIncome for x in employed_3_Females])
        if len(employed_3) > 0:
            averageIncome = income_3/float(len(employed_3))
        else:
            averageIncome = 0
        self.averageIncome_3.append(averageIncome)
        
        averageIncome_M = 0
        averageIncome_F = 0
        if len(employed_3_Males) > 0:
            averageIncome_M = income_3_Males/float(len(employed_3_Males))
        else:
            averageIncome_M = 0
        self.averageIncome_3_Males.append(averageIncome_M)
        if len(employed_3_Females) > 0:
            averageIncome_F = income_3_Females/float(len(employed_3_Females))
        else:
            averageIncome_F = 0
        self.averageIncome_3_Females.append(averageIncome_F)
        
        if averageIncome_M > 0:
            self.ratioWomenMaleIncome_3.append(averageIncome_F/averageIncome_M)
        else:
            self.ratioWomenMaleIncome_3.append(0)
        
        income_4 = sum([x.netIncome for x in employed_4])
        income_4_Males = sum([x.netIncome for x in employed_4_Males])
        income_4_Females = sum([x.netIncome for x in employed_4_Females])
        if len(employed_4) > 0:
            averageIncome = income_4/float(len(employed_4))
        else:
            averageIncome = 0
        self.averageIncome_4.append(averageIncome)
        
        averageIncome_M = 0
        averageIncome_F = 0
        if len(employed_4_Males) > 0:
            averageIncome_M = income_4_Males/float(len(employed_4_Males))
        else:
            averageIncome_M = 0
        self.averageIncome_4_Males.append(averageIncome_M)
        if len(employed_4_Females) > 0:
            averageIncome_F = income_4_Females/float(len(employed_4_Females))
        else:
            averageIncome_F = 0
        self.averageIncome_4_Females.append(averageIncome_F)
        
        if averageIncome_M > 0:
            self.ratioWomenMaleIncome_4.append(averageIncome_F/averageIncome_M)
        else:
            self.ratioWomenMaleIncome_4.append(0)
        
        income_5 = sum([x.netIncome for x in employed_5])
        income_5_Males = sum([x.netIncome for x in employed_5_Males])
        income_5_Females = sum([x.netIncome for x in employed_5_Females])
        if len(employed_5) > 0:
            averageIncome = income_5/float(len(employed_5))
        else:
            averageIncome = 0
        self.averageIncome_5.append(averageIncome)
        
        averageIncome_M = 0
        averageIncome_F = 0
        if len(employed_5_Males) > 0:
            averageIncome_M = income_5_Males/float(len(employed_5_Males))
        else:
            averageIncome_M = 0
        self.averageIncome_5_Males.append(averageIncome_M)
        if len(employed_5_Females) > 0:
            averageIncome_F = income_5_Females/float(len(employed_5_Females))
        else:
            averageIncome_F = 0
        self.averageIncome_5_Females.append(averageIncome_F)
        
        if averageIncome_M > 0:
            self.ratioWomenMaleIncome_5.append(averageIncome_F/averageIncome_M)
        else:
            self.ratioWomenMaleIncome_5.append(0)
    
    def doStats(self):
        
        # Year
        self.times.append(self.year)
        # Population stats
        adultPop = [x for x in self.pop.livingPeople if x.age > self.p['minWorkingAge'] and x.status != 'student']
        currentPop = float(len(self.pop.livingPeople))
        
        totQALY = sum([x.qaly for x in self.pop.livingPeople])
        self.aggregateQALY.append(totQALY)
        meanQALY = totQALY/currentPop
        self.averageQALY.append(meanQALY)
        if self.year < self.p['implementPoliciesFromYear']:
            self.discountedQALY.append(0)
        else:
            self.discountedQALY.append(totQALY/math.pow(1+self.p['qalyDiscountRate'], self.year-self.p['implementPoliciesFromYear']))
            
        if self.year < self.p['implementPoliciesFromYear']:
            self.averageDiscountedQALY.append(0)
        else:
            self.averageDiscountedQALY.append((meanQALY/math.pow(1+self.p['qalyDiscountRate'], self.year-self.p['implementPoliciesFromYear']))/currentPop)
        
        self.pops.append(currentPop)
        unskilled = [x for x in adultPop if x.classRank == 0]
        print(float(len(unskilled))/len(adultPop))
        self.unskilledPop.append(len(unskilled))
        skilled = [x for x in adultPop if x.classRank == 1]
        print(float(len(skilled))/len(adultPop))
        self.skilledPop.append(len(skilled))
        lowerclass = [x for x in adultPop if x.classRank == 2]
        print(float(len(lowerclass))/len(adultPop))
        self.lowerclassPop.append(len(lowerclass))
        middelclass = [x for x in adultPop if x.classRank == 3]
        print(float(len(middelclass))/len(adultPop))
        self.middleclassPop.append(len(middelclass))
        upperclass = [x for x in adultPop if x.classRank == 4]
        print(float(len(upperclass))/len(adultPop))
        self.upperclassPop.append(len(upperclass))
        
        tally_1to1 = 0
        tally_1to2 = 0
        tally_1to3 = 0
        tally_1to4 = 0
        tally_1to5 = 0
        tally_2to1 = 0
        tally_2to2 = 0
        tally_2to3 = 0
        tally_2to4 = 0
        tally_2to5 = 0
        tally_3to1 = 0
        tally_3to2 = 0
        tally_3to3 = 0
        tally_3to4 = 0
        tally_3to5 = 0
        tally_4to1 = 0
        tally_4to2 = 0
        tally_4to3 = 0
        tally_4to4 = 0
        tally_4to5 = 0
        tally_5to1 = 0
        tally_5to2 = 0
        tally_5to3 = 0
        tally_5to4 = 0
        tally_5to5 = 0
        
        workingPop = [x for x in self.pop.livingPeople if x.age == 24]
        classRank_1 = [x for x in self.pop.livingPeople if x.age == 24 and x.classRank == 0]
        classRank_2 = [x for x in self.pop.livingPeople if x.age == 24 and x.classRank == 1]
        classRank_3 = [x for x in self.pop.livingPeople if x.age == 24 and x.classRank == 2]
        classRank_4 = [x for x in self.pop.livingPeople if x.age == 24 and x.classRank == 3]
        classRank_5 = [x for x in self.pop.livingPeople if x.age == 24 and x.classRank == 4]
        
        for person in workingPop:
            if person.father != None:
                
                if person.classRank == 0 and person.father.classRank == 0:
                    tally_1to1 += 1
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
                if person.classRank == 1 and person.father.classRank == 1:
                    tally_2to2 += 1
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
                if person.classRank == 2 and person.father.classRank == 2:
                    tally_3to3 += 1
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
                if person.classRank == 3 and person.father.classRank == 3:
                    tally_4to4 += 1
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
                if person.classRank == 4 and person.father.classRank == 4:
                    tally_5to5 += 1
        
        if len(classRank_1) > 0:
            self.socialMobility_1to1.append(tally_1to1/len(classRank_1))
            self.socialMobility_1to2.append(tally_1to2/len(classRank_1))
            self.socialMobility_1to3.append(tally_1to3/len(classRank_1))
            self.socialMobility_1to4.append(tally_1to4/len(classRank_1))
            self.socialMobility_1to5.append(tally_1to5/len(classRank_1))
        else:
            self.socialMobility_1to1.append(0)
            self.socialMobility_1to2.append(0)
            self.socialMobility_1to3.append(0)
            self.socialMobility_1to4.append(0)
            self.socialMobility_1to5.append(0)
            
        if len(classRank_2) > 0:
            self.socialMobility_2to1.append(tally_2to1/len(classRank_2))
            self.socialMobility_2to2.append(tally_2to2/len(classRank_2))
            self.socialMobility_2to3.append(tally_2to3/len(classRank_2))
            self.socialMobility_2to4.append(tally_2to4/len(classRank_2))
            self.socialMobility_2to5.append(tally_2to5/len(classRank_2))
        else:
            self.socialMobility_2to1.append(0)
            self.socialMobility_2to2.append(0)
            self.socialMobility_2to3.append(0)
            self.socialMobility_2to4.append(0)
            self.socialMobility_2to5.append(0)
            
        if len(classRank_3) > 0:
            self.socialMobility_3to1.append(tally_3to1/len(classRank_3))
            self.socialMobility_3to2.append(tally_3to2/len(classRank_3))
            self.socialMobility_3to3.append(tally_3to3/len(classRank_3))
            self.socialMobility_3to4.append(tally_3to4/len(classRank_3))
            self.socialMobility_3to5.append(tally_3to5/len(classRank_3))
        else:
            self.socialMobility_3to1.append(0)
            self.socialMobility_3to2.append(0)
            self.socialMobility_3to3.append(0)
            self.socialMobility_3to4.append(0)
            self.socialMobility_3to5.append(0)
        
        if len(classRank_4) > 0:
            self.socialMobility_4to1.append(tally_4to1/len(classRank_4))
            self.socialMobility_4to2.append(tally_4to2/len(classRank_4))
            self.socialMobility_4to3.append(tally_4to3/len(classRank_4))
            self.socialMobility_4to4.append(tally_4to4/len(classRank_4))
            self.socialMobility_4to5.append(tally_4to5/len(classRank_4))
        else:
            self.socialMobility_4to1.append(0)
            self.socialMobility_4to2.append(0)
            self.socialMobility_4to3.append(0)
            self.socialMobility_4to4.append(0)
            self.socialMobility_4to5.append(0)
            
        if len(classRank_5) > 0:
            self.socialMobility_5to1.append(tally_5to1/len(classRank_5))
            self.socialMobility_5to2.append(tally_5to2/len(classRank_5))
            self.socialMobility_5to3.append(tally_5to3/len(classRank_5))
            self.socialMobility_5to4.append(tally_5to4/len(classRank_5))
            self.socialMobility_5to5.append(tally_5to5/len(classRank_5))
        else:
            self.socialMobility_5to1.append(0)
            self.socialMobility_5to2.append(0)
            self.socialMobility_5to3.append(0)
            self.socialMobility_5to4.append(0)
            self.socialMobility_5to5.append(0)
        
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
        
        if len(h1) > 0:
            self.avgHouseholdSize_1.append(occupants_1/float(len(h1)))
            #print(occupants_1/float(len(h1)))
        else:
            self.avgHouseholdSize_1.append(0)
        if len(h2) > 0:
            self.avgHouseholdSize_2.append(occupants_2/float(len(h2)))
            #print(occupants_2/float(len(h2)))
        else:
            self.avgHouseholdSize_2.append(0)
        if len(h3) > 0:
            self.avgHouseholdSize_3.append(occupants_3/float(len(h3)))
            #print(occupants_3/float(len(h3)))
        else:
            self.avgHouseholdSize_3.append(0)
        if len(h4) > 0:
            self.avgHouseholdSize_4.append(occupants_4/float(len(h4)))
            #print(occupants_4/float(len(h4)))
        else:
            self.avgHouseholdSize_4.append(0)
        if len(h5) > 0:
            self.avgHouseholdSize_5.append(occupants_5/float(len(h5)))
            #print(occupants_5/float(len(h5)))
        else:
            self.avgHouseholdSize_5.append(0)
       
        ## Marriages and divorces
        self.numMarriages.append(self.marriageTally)
        
        # print('Marriages: ' + str(self.marriageTally))
        
        self.marriageTally = 0
        self.numDivorces.append(self.divorceTally)            
        self.divorceTally = 0
        
        
        ####### Social Care Outputs ################################################################
        
        self.publicSocialCareSupply.append(self.publicSupply)
        
        ## Care demand calculations: first, what's the basic demand and theoretical supply?
        totalCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople])
        socialCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople if x.status == 'inactive'])
        
        childCareNeed = totalCareNeed - socialCareNeed
        self.totalCareDemand.append(totalCareNeed)
        self.totalSocialCareDemand.append(socialCareNeed)  
        self.totalChildCareDemand.append(childCareNeed)
        
        self.perCapitaCareDemand.append(totalCareNeed/currentPop)
        self.perCapitaSocialCareDemand.append(socialCareNeed/currentPop)
        self.perCapitaChildCareDemand.append(childCareNeed/currentPop)
        
        if totalCareNeed > 0:
            self.shareSocialCareDemand.append(socialCareNeed/totalCareNeed)
        else:
            self.shareSocialCareDemand.append(0)
        
        informalCareSupply = sum([x.hoursInformalSupply for x in self.pop.livingPeople])
        visitedHousehold = []
        formalCareSupply = 0
        for x in self.pop.livingPeople:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply
        totalCareSupply = informalCareSupply + formalCareSupply
        self.totalInformalCareSupply.append(informalCareSupply) 
        self.totalFormalCareSupply.append(formalCareSupply) 
        self.totalCareSupply.append(totalCareSupply) 
        if totalCareSupply > 0:
            self.shareInformalCareSupply.append(informalCareSupply/totalCareSupply)
        else:
            self.shareInformalCareSupply.append(0)
        numberOfRecipients = len([x for x in self.pop.livingPeople if x.status == 'inactive' or (x.status == 'child' and x.age == 0)])    
        if numberOfRecipients > 0:
            self.averageCareSupply.append(totalCareSupply/numberOfRecipients)
        else:
            self.averageCareSupply.append(0)   
        
        informalCareReceived = sum([x.informalCare for x in self.pop.livingPeople])
        formalCareReceived = sum([x.formalCare for x in self.pop.livingPeople])
        totalCareReceived = informalCareReceived + formalCareReceived
        totalUnnmetCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
        if totalCareSupply > 0:
            self.ratio_UnmetCareDemand_Supply.append(totalUnnmetCareNeed/totalCareSupply) 
        else:
            self.ratio_UnmetCareDemand_Supply.append(0)
            
        totalCareReceivers = len([x for x in self.pop.livingPeople if x.hoursDemand > 0])
        totalCareSuppliers = len([x for x in self.pop.livingPeople if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        self.shareCareGivers.append(float(totalCareSuppliers)/currentPop)
        totalCareEmployed = len([x for x in self.pop.livingPeople if x.hoursDemand == 0 and x.status == 'employed'])
        self.totalInformalCareReceived.append(informalCareReceived)
        self.totalFormalCareReceived.append(formalCareReceived)
        self.totalCareReceived.append(totalCareReceived) # New!
        self.perCapitaCareReceived.append(totalCareReceived/currentPop)
        if totalCareReceivers > 0:
            self.averageCareReceived.append(totalCareReceived/totalCareReceivers)
            self.averageInformalCareReceived.append(informalCareReceived/totalCareReceivers)
            self.averageFormalCareReceived.append(formalCareReceived/totalCareReceivers)
            self.averageUnmetCareDemand.append(totalUnnmetCareNeed/totalCareReceivers)
        else:
            self.averageCareReceived.append(0)
            self.averageInformalCareReceived.append(0)
            self.averageFormalCareReceived.append(0)
            self.averageUnmetCareDemand.append(0)
        if totalCareSuppliers > 0:
            self.averageCareSupplied.append(totalCareReceived/totalCareSuppliers)
            self.averageInformalCareSupplied.append(informalCareReceived/totalCareSuppliers)
        else:
            self.averageCareSupplied.append(0)
            self.averageInformalCareSupplied.append(0)
        if totalCareEmployed > 0:
            self.averageFormalCareSupplied.append(formalCareReceived/totalCareEmployed)
        else:
            self.averageFormalCareSupplied.append(0)
        if totalCareReceived > 0:
            self.shareInformalCareReceived.append(informalCareReceived/totalCareReceived)
        else:
            self.shareInformalCareReceived.append(0)
        self.totalUnmetCareDemand.append(totalUnnmetCareNeed)
        if totalCareNeed > 0:
            self.shareUnmetCareDemand.append(totalUnnmetCareNeed/totalCareNeed)
        else:
            self.shareUnmetCareDemand.append(0)
        self.perCapitaUnmetCareDemand.append(totalUnnmetCareNeed/currentPop)
        
        
        informalSocialCareReceived = sum([x.informalCare for x in self.pop.livingPeople if x.status == 'inactive'])
        formalSocialCareReceived = sum([x.formalCare for x in self.pop.livingPeople if x.status == 'inactive'])
        socialCareReceived = informalSocialCareReceived + formalSocialCareReceived
        totalUnmetSocialCareNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.status == 'inactive'])
        socialCareReceivers = [x for x in self.pop.livingPeople if x.hoursDemand > 0 and x.status == 'inactive']
        totalSocialCareReceivers = float(len(socialCareReceivers))
        totalSocialCareReceivers_N1 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 1]))
        totalSocialCareReceivers_N2 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 2]))
        totalSocialCareReceivers_N3 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 3]))
        totalSocialCareReceivers_N4 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 4]))
        if totalSocialCareReceivers > 0:
            self.shareSocialCareTakers_N1.append(totalSocialCareReceivers_N1/totalSocialCareReceivers)
            self.shareSocialCareTakers_N2.append(totalSocialCareReceivers_N2/totalSocialCareReceivers)
            self.shareSocialCareTakers_N3.append(totalSocialCareReceivers_N3/totalSocialCareReceivers)
            self.shareSocialCareTakers_N4.append(totalSocialCareReceivers_N4/totalSocialCareReceivers)
        else:
            self.shareSocialCareTakers_N1.append(0)
            self.shareSocialCareTakers_N2.append(0)
            self.shareSocialCareTakers_N3.append(0)
            self.shareSocialCareTakers_N4.append(0)
        self.totalInformalSocialCareReceived.append(informalSocialCareReceived)
        self.totalFormalSocialCareReceived.append(formalSocialCareReceived)
        self.totalSocialCareReceived.append(socialCareReceived) #New!
        self.perCapitaSocialCareReceived.append(socialCareReceived/currentPop)
        if totalSocialCareReceivers > 0:
            self.averageSocialCareReceived.append(socialCareReceived/totalSocialCareReceivers)
            self.averageInformalSocialCareReceived.append(informalSocialCareReceived/totalSocialCareReceivers)
            self.averageFormalSocialCareReceived.append(formalSocialCareReceived/totalSocialCareReceivers)
            self.averageUnmetSocialCareDemand.append(totalUnmetSocialCareNeed/totalSocialCareReceivers)
        else:
            self.averageSocialCareReceived.append(0)
            self.averageInformalSocialCareReceived.append(0)
            self.averageFormalSocialCareReceived.append(0)
            self.averageUnmetSocialCareDemand.append(0)
        if totalCareSuppliers > 0:
            self.averageSocialCareSupplied.append(socialCareReceived/totalCareSuppliers)
            self.averageInformalSocialCareSupplied.append(informalSocialCareReceived/totalCareSuppliers)
        else:
            self.averageSocialCareSupplied.append(0)
            self.averageInformalSocialCareSupplied.append(0)
        if totalCareEmployed > 0:
            self.averageFormalSocialCareSupplied.append(formalSocialCareReceived/totalCareEmployed)
        else:
            self.averageFormalSocialCareSupplied.append(0)
        if socialCareReceived > 0:
            self.shareInformalSocialCareReceived.append(informalSocialCareReceived/socialCareReceived)
        else:
            self.shareInformalSocialCareReceived.append(0)
        self.totalSocialCareUnmetDemand.append(totalUnmetSocialCareNeed) # New!
        self.perCapitaUnmetSocialCareDemand.append(totalUnmetSocialCareNeed/currentPop)
        if socialCareNeed > 0:
            self.shareUnmetSocialCareDemand.append(totalUnmetSocialCareNeed/socialCareNeed)
        else:
            self.shareUnmetSocialCareDemand.append(0)
        
        informalChildCareReceived = sum([x.informalCare for x in self.pop.livingPeople if x.status == 'child'])
        formalChildCareReceived = sum([x.formalCare for x in self.pop.livingPeople if x.status == 'child'])
        childCareReceived = informalChildCareReceived + formalChildCareReceived
        totalUnmetChildCareNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.status == 'child'])
        totalChildCareReceivers = len([x for x in self.pop.livingPeople if x.hoursDemand > 0 and x.status == 'child'])
        self.totalInformalChildCareReceived.append(informalChildCareReceived)
        self.totalFormalChildCareReceived.append(formalChildCareReceived)
        self.totalChildCareReceived.append(childCareReceived) #New!
        self.perCapitaChildCareReceived.append(socialCareReceived/currentPop)
        if totalChildCareReceivers > 0:
            self.averageChildCareReceived.append(childCareReceived/totalChildCareReceivers)
            self.averageInformalChildCareReceived.append(informalChildCareReceived/totalChildCareReceivers)
            self.averageFormalChildCareReceived.append(formalChildCareReceived/totalChildCareReceivers)
            self.averageUnmetChildCareDemand.append(totalUnmetChildCareNeed/totalChildCareReceivers)
        else:
            self.averageChildCareReceived.append(0)
            self.averageInformalChildCareReceived.append(0)
            self.averageFormalChildCareReceived.append(0)
            self.averageUnmetChildCareDemand.append(0)
        if totalCareSuppliers > 0:
            self.averageChildCareSupplied.append(childCareReceived/totalCareSuppliers)
            self.averageInformalChildCareSupplied.append(informalChildCareReceived/totalCareSuppliers)
        else:
            self.averageChildCareSupplied.append(0)
            self.averageInformalChildCareSupplied.append(0)
        if totalCareEmployed > 0:
            self.averageFormalChildCareSupplied.append(formalChildCareReceived/totalCareEmployed)
        else:
            self.averageFormalChildCareSupplied.append(0)
        if childCareReceived > 0:
            self.shareInformalChildCareReceived.append(informalChildCareReceived/childCareReceived)
        else:
            self.shareInformalChildCareReceived.append(0)
        self.totalChildCareUnmetDemand.append(totalUnmetChildCareNeed) # New!
        self.perCapitaUnmetChildCareDemand.append(totalUnmetChildCareNeed/currentPop)
        if childCareNeed > 0:
            self.shareUnmetChildCareDemand.append(totalUnmetChildCareNeed/childCareNeed)
        else:
            self.shareUnmetChildCareDemand.append(0)
        
        totalInformalCareSupplied = sum([x.socialWork for x in self.pop.livingPeople])
        totalFormalCareSupplied = sum([x.workToCare for x in self.pop.livingPeople])
        totalCareSupplied = totalInformalCareSupplied + totalFormalCareSupplied
    
        totalInformalCareSuppliedMale = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male'])
        informalCareSuppliedMale_1 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 0])
        informalCareSuppliedMale_2 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 1])
        informalCareSuppliedMale_3 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 2])
        informalCareSuppliedMale_4 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 3])
        informalCareSuppliedMale_5 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'male' and x.classRank == 4])
        self.totalInformalCareSuppliedMale.append(totalInformalCareSuppliedMale) 
        self.totalInformalCareSuppliedMale_1.append(informalCareSuppliedMale_1)
        self.totalInformalCareSuppliedMale_2.append(informalCareSuppliedMale_2)
        self.totalInformalCareSuppliedMale_3.append(informalCareSuppliedMale_3)
        self.totalInformalCareSuppliedMale_4.append(informalCareSuppliedMale_4)
        self.totalInformalCareSuppliedMale_5.append(informalCareSuppliedMale_5)
        
        totalInformalCareSuppliedFemale = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female'])
        informalCareSuppliedFemale_1 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 0])
        informalCareSuppliedFemale_2 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 1])
        informalCareSuppliedFemale_3 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 2])
        informalCareSuppliedFemale_4 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 3])
        informalCareSuppliedFemale_5 = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female' and x.classRank == 4])
        self.totalInformalCareSuppliedFemale.append(totalInformalCareSuppliedFemale)  
        self.totalInformalCareSuppliedFemale_1.append(informalCareSuppliedFemale_1)
        self.totalInformalCareSuppliedFemale_2.append(informalCareSuppliedFemale_2)
        self.totalInformalCareSuppliedFemale_3.append(informalCareSuppliedFemale_3)
        self.totalInformalCareSuppliedFemale_4.append(informalCareSuppliedFemale_4)
        self.totalInformalCareSuppliedFemale_5.append(informalCareSuppliedFemale_5)
        totalInformalCare = totalInformalCareSuppliedMale + totalInformalCareSuppliedFemale
        totalInformalCare_1 = informalCareSuppliedMale_1 + informalCareSuppliedFemale_1
        totalInformalCare_2 = informalCareSuppliedMale_2 + informalCareSuppliedFemale_2
        totalInformalCare_3 = informalCareSuppliedMale_3 + informalCareSuppliedFemale_3
        totalInformalCare_4 = informalCareSuppliedMale_4 + informalCareSuppliedFemale_4
        totalInformalCare_5 = informalCareSuppliedMale_5 + informalCareSuppliedFemale_5
        if totalInformalCare > 0:
            self.shareFemaleInformalCareSupplied.append(totalInformalCareSuppliedFemale/totalInformalCare)
        else:
            self.shareFemaleInformalCareSupplied.append(0)
        if totalInformalCare_1 > 0:
            self.shareFemaleInformalCareSupplied_1.append(informalCareSuppliedFemale_1/totalInformalCare_1)
        else:
            self.shareFemaleInformalCareSupplied_1.append(0)
        if totalInformalCare_2 > 0:
            self.shareFemaleInformalCareSupplied_2.append(informalCareSuppliedFemale_2/totalInformalCare_2)
        else:
            self.shareFemaleInformalCareSupplied_2.append(0)
        if totalInformalCare_3 > 0:
            self.shareFemaleInformalCareSupplied_3.append(informalCareSuppliedFemale_3/totalInformalCare_3)
        else:
            self.shareFemaleInformalCareSupplied_3.append(0)
        if totalInformalCare_4 > 0:
            self.shareFemaleInformalCareSupplied_4.append(informalCareSuppliedFemale_4/totalInformalCare_4)
        else:
            self.shareFemaleInformalCareSupplied_4.append(0)
        if totalInformalCare_5 > 0:
            self.shareFemaleInformalCareSupplied_5.append(informalCareSuppliedFemale_5/totalInformalCare_5)
        else:
            self.shareFemaleInformalCareSupplied_5.append(0)
        
        class1 = [x for x in self.pop.livingPeople if x.classRank == 0]
        totalSupply = 0
        totalCareDemandHours = 0
        totalSocialCareDemandHours = 0
        totalChildCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalSocialCare = 0
        totalChildCare = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        totalSocialInformalCare = 0
        totalSocialFormalCare = 0
        totalUnmetSocialCare = 0
        totalChildInformalCare = 0
        totalChildFormalCare = 0
        totalUnmetChildCare = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        socialCareReceivers = 0
        childCareReceivers = 0
        for person in class1:
            if person.hoursDemand > 0:
                if person.status == 'child':
                    totalChildInformalCare += person.informalCare
                    totalChildFormalCare += person.formalCare
                    totalUnmetChildCare += person.residualNeed
                    totalChildCareDemandHours += person.hoursDemand
                    childCareReceivers += 1
                else:
                    totalSocialInformalCare += person.informalCare
                    totalSocialFormalCare += person.formalCare
                    totalUnmetSocialCare += person.residualNeed
                    totalSocialCareDemandHours += person.hoursDemand
                    socialCareReceivers += 1
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            elif person.hoursDemand == 0 and person.age >= self.p['ageTeenagers']:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                totalSupply += person.hoursInformalSupply
                numberOfCarers += 1
        visitedHousehold = []
        formalCareSupply = 0
        for person in class1:
            if person.house in visitedHousehold:
                continue
            visitedHousehold.append(person.house)
            totalSupply += person.hoursFormalSupply
        # Save stats
        if len(class1) > 0:
            self.shareCareGivers_1.append(float(numberOfCarers)/float(len(class1)))
        else:
            self.shareCareGivers_1.append(0)
            
        # totalSupply = totalInformalCareSupplyHours + totalFormalCareSupplyHours
        
        
        totalChildCare = totalChildInformalCare + totalChildFormalCare
        totalSocialCare = totalSocialInformalCare + totalSocialFormalCare
        totalInformalCare = totalChildInformalCare + totalSocialInformalCare
        totalCare = totalSocialCare + totalChildCare

        
        if totalCareDemandHours > 0:
            self.shareSocialCare_1.append(totalSocialCareDemandHours/totalCareDemandHours)
        else:
            self.shareSocialCare_1.append(0)
        
        self.totalCareSupply_1.append(totalSupply)
        if numberOfRecipients > 0:
            self.averageCareSupply_1.append(totalSupply/numberOfRecipients)
        else:
            self.averageCareSupply_1.append(0)
            
        if totalSupply > 0:
            self.ratio_UnmetCareDemand_Supply_1.append(totalUnmetDemandHours/totalSupply)
        else:
            self.ratio_UnmetCareDemand_Supply_1.append(0)
        
        self.totalCareDemand_1.append(totalCareDemandHours)
        self.totalCareSupply_1.append(totalSupply) 
        self.totalUnmetDemand_1.append(totalUnmetDemandHours) 
        self.totalInformalSupply_1.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_1.append(totalFormalCareSupplyHours)
        self.totalSocialInformalCareSupply_1.append(totalSocialInformalCare)
        self.totalSocialFormalCareSupply_1.append(totalSocialFormalCare)
        self.totalUnmetSocialCareDemand_1.append(totalUnmetSocialCare)
        self.totalChildInformalCareSupply_1.append(totalChildInformalCare)
        self.totalChildFormalCareSupply_1.append(totalChildFormalCare)
        self.totalUnmetChildCareDemand_1.append(totalUnmetChildCare)
        
        if totalCare > 0:
            self.shareInformalSupply_1.append(totalInformalCare/totalCare)
        else:
            self.shareInformalSupply_1.append(0)
            
        if totalCareDemandHours > 0:
            self.shareUnmetCareDemand_1.append(totalUnmetDemandHours/totalCareDemandHours)
        else:
            self.shareUnmetCareDemand_1.append(0)
            
        self.perCapitaUnmetCareDemand_1.append(totalUnmetDemandHours/float(len(class1)))
        
        if totalSocialCare > 0:
            self.shareInformalSocialSupply_1.append(totalSocialInformalCare/totalSocialCare)
        else:
            self.shareInformalSocialSupply_1.append(0)
            
        if totalSocialCareDemandHours > 0:
            self.shareUnmetSocialSupply_1.append(totalUnmetSocialCare/totalSocialCareDemandHours)
        else:
            self.shareUnmetSocialSupply_1.append(0)
            
        if totalChildCare > 0:
            self.shareInformalChildSupply_1.append(totalChildInformalCare/totalChildCare)
        else:
            self.shareInformalChildSupply_1.append(0)
            
        if totalChildCareDemandHours > 0:
            self.shareUnmetChildSupply_1.append(totalUnmetChildCare/totalChildCareDemandHours)
        else:
            self.shareUnmetChildSupply_1.append(0)
        
        
        if numberOfRecipients > 0:
            self.totalInformalCarePerRecipient_1.append(totalInformalCareSupplyHours/numberOfRecipients)
            self.totalFormalCarePerRecipient_1.append(totalFormalCareSupplyHours/numberOfRecipients)
            self.totalUnmetNeedPerRecipient_1.append(totalUnmetDemandHours/numberOfRecipients)
        else:
            self.totalInformalCarePerRecipient_1.append(0)
            self.totalFormalCarePerRecipient_1.append(0)
            self.totalUnmetNeedPerRecipient_1.append(0)
        if numberOfCarers > 0:
            self.totalInformalCarePerCarer_1.append(totalInformalCareSupplyHours/numberOfCarers)
            self.totalFormalCarePerCarer_1.append(totalFormalCareSupplyHours/numberOfCarers)
        else:
            self.totalInformalCarePerCarer_1.append(0)
            self.totalFormalCarePerCarer_1.append(0)
            
        if socialCareReceivers > 0:
            self.averageSocialInformalCareSupply_1.append(totalSocialInformalCare/socialCareReceivers)
            self.averageSocialFormalCareSupply_1.append(totalSocialFormalCare/socialCareReceivers)
            self.averageUnmetSocialCareDemand_1.append(totalUnmetSocialCare/socialCareReceivers)
        else:
            self.averageSocialInformalCareSupply_1.append(0)
            self.averageSocialFormalCareSupply_1.append(0)
            self.averageUnmetSocialCareDemand_1.append(0)
            
        if childCareReceivers > 0:
            self.averageChildInformalCareSupply_1.append(totalChildInformalCare/childCareReceivers)
            self.averageChildFormalCareSupply_1.append(totalChildFormalCare/childCareReceivers)
            self.averageUnmetChildCareDemand_1.append(totalUnmetChildCare/childCareReceivers)
        else:
            self.averageChildInformalCareSupply_1.append(0)
            self.averageChildFormalCareSupply_1.append(0)
            self.averageUnmetChildCareDemand_1.append(0)
        
        class2 = [x for x in self.pop.livingPeople if x.classRank == 1]
        totalSupply = 0
        totalCareDemandHours = 0
        totalSocialCareDemandHours = 0
        totalChildCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalSocialCare = 0
        totalChildCare = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        totalSocialInformalCare = 0
        totalSocialFormalCare = 0
        totalUnmetSocialCare = 0
        totalChildInformalCare = 0
        totalChildFormalCare = 0
        totalUnmetChildCare = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        socialCareReceivers = 0
        childCareReceivers = 0
        for person in class2:
            if person.hoursDemand > 0:
                if person.status == 'child':
                    totalChildInformalCare += person.informalCare
                    totalChildFormalCare += person.formalCare
                    totalUnmetChildCare += person.residualNeed
                    totalChildCareDemandHours += person.hoursDemand
                    childCareReceivers += 1
                else:
                    totalSocialInformalCare += person.informalCare
                    totalSocialFormalCare += person.formalCare
                    totalUnmetSocialCare += person.residualNeed
                    totalSocialCareDemandHours += person.hoursDemand
                    socialCareReceivers += 1
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            elif person.hoursDemand == 0 and person.age >= self.p['ageTeenagers']:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                totalSupply += person.hoursInformalSupply
                numberOfCarers += 1
        visitedHousehold = []
        formalCareSupply = 0
        for person in class2:
            if person.house in visitedHousehold:
                continue
            visitedHousehold.append(person.house)
            totalSupply += person.hoursFormalSupply
        # Save stats
        if len(class2) > 0:
            self.shareCareGivers_2.append(float(numberOfCarers)/float(len(class2)))
        else:
            self.shareCareGivers_2.append(0)
            
        # totalSupply = totalInformalCareSupplyHours + totalFormalCareSupplyHours
        
        
        totalChildCare = totalChildInformalCare + totalChildFormalCare
        totalSocialCare = totalSocialInformalCare + totalSocialFormalCare
        totalInformalCare = totalChildInformalCare + totalSocialInformalCare
        totalCare = totalSocialCare + totalChildCare
        
        if totalCareDemandHours > 0:
            self.shareSocialCare_2.append(totalSocialCareDemandHours/totalCareDemandHours)
        else:
            self.shareSocialCare_2.append(0)
        
        self.totalCareSupply_2.append(totalSupply)
        if numberOfRecipients > 0:
            self.averageCareSupply_2.append(totalSupply/numberOfRecipients)
        else:
            self.averageCareSupply_2.append(0)
            
        if totalSupply > 0:
            self.ratio_UnmetCareDemand_Supply_2.append(totalUnmetDemandHours/totalSupply)
        else:
            self.ratio_UnmetCareDemand_Supply_2.append(0)
            
        self.totalCareDemand_2.append(totalCareDemandHours)
        self.totalCareSupply_2.append(totalSupply) 
        self.totalUnmetDemand_2.append(totalUnmetDemandHours) 
        self.totalInformalSupply_2.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_2.append(totalFormalCareSupplyHours)
        self.totalSocialInformalCareSupply_2.append(totalSocialInformalCare)
        self.totalSocialFormalCareSupply_2.append(totalSocialFormalCare)
        self.totalUnmetSocialCareDemand_2.append(totalUnmetSocialCare)
        self.totalChildInformalCareSupply_2.append(totalChildInformalCare)
        self.totalChildFormalCareSupply_2.append(totalChildFormalCare)
        self.totalUnmetChildCareDemand_2.append(totalUnmetChildCare)
        
        if totalCare > 0:
            self.shareInformalSupply_2.append(totalInformalCare/totalCare)
        else:
            self.shareInformalSupply_2.append(0)
            
        if totalCareDemandHours > 0:
            self.shareUnmetCareDemand_2.append(totalUnmetDemandHours/totalCareDemandHours)
        else:
            self.shareUnmetCareDemand_2.append(0)
            
        self.perCapitaUnmetCareDemand_2.append(totalUnmetDemandHours/float(len(class2)))
        
        if totalSocialCare > 0:
            self.shareInformalSocialSupply_2.append(totalSocialInformalCare/totalSocialCare)
        else:
            self.shareInformalSocialSupply_2.append(0)
            
        if totalSocialCareDemandHours > 0:
            self.shareUnmetSocialSupply_2.append(totalUnmetSocialCare/totalSocialCareDemandHours)
        else:
            self.shareUnmetSocialSupply_2.append(0)
            
        if totalChildCare > 0:
            self.shareInformalChildSupply_2.append(totalChildInformalCare/totalChildCare)
        else:
            self.shareInformalChildSupply_2.append(0)
            
        if totalChildCareDemandHours > 0:
            self.shareUnmetChildSupply_2.append(totalUnmetChildCare/totalChildCareDemandHours)
        else:
            self.shareUnmetChildSupply_2.append(0)
        
        
        if numberOfRecipients > 0:
            self.totalInformalCarePerRecipient_2.append(totalInformalCareSupplyHours/numberOfRecipients)
            self.totalFormalCarePerRecipient_2.append(totalFormalCareSupplyHours/numberOfRecipients)
            self.totalUnmetNeedPerRecipient_2.append(totalUnmetDemandHours/numberOfRecipients)
        else:
            self.totalInformalCarePerRecipient_2.append(0)
            self.totalFormalCarePerRecipient_2.append(0)
            self.totalUnmetNeedPerRecipient_2.append(0)
        if numberOfCarers > 0:
            self.totalInformalCarePerCarer_2.append(totalInformalCareSupplyHours/numberOfCarers)
            self.totalFormalCarePerCarer_2.append(totalFormalCareSupplyHours/numberOfCarers)
        else:
            self.totalInformalCarePerCarer_2.append(0)
            self.totalFormalCarePerCarer_2.append(0)
            
        if socialCareReceivers > 0:
            self.averageSocialInformalCareSupply_2.append(totalSocialInformalCare/socialCareReceivers)
            self.averageSocialFormalCareSupply_2.append(totalSocialFormalCare/socialCareReceivers)
            self.averageUnmetSocialCareDemand_2.append(totalUnmetSocialCare/socialCareReceivers)
        else:
            self.averageSocialInformalCareSupply_2.append(0)
            self.averageSocialFormalCareSupply_2.append(0)
            self.averageUnmetSocialCareDemand_2.append(0)
            
        if childCareReceivers > 0:
            self.averageChildInformalCareSupply_2.append(totalChildInformalCare/childCareReceivers)
            self.averageChildFormalCareSupply_2.append(totalChildFormalCare/childCareReceivers)
            self.averageUnmetChildCareDemand_2.append(totalUnmetChildCare/childCareReceivers)
        else:
            self.averageChildInformalCareSupply_2.append(0)
            self.averageChildFormalCareSupply_2.append(0)
            self.averageUnmetChildCareDemand_2.append(0)
        
        class3 = [x for x in self.pop.livingPeople if x.classRank == 2]
        totalSupply = 0
        totalCareDemandHours = 0
        totalSocialCareDemandHours = 0
        totalChildCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalSocialCare = 0
        totalChildCare = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        totalSocialInformalCare = 0
        totalSocialFormalCare = 0
        totalUnmetSocialCare = 0
        totalChildInformalCare = 0
        totalChildFormalCare = 0
        totalUnmetChildCare = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        socialCareReceivers = 0
        childCareReceivers = 0
        for person in class3:
            if person.hoursDemand > 0:
                if person.status == 'child':
                    totalChildInformalCare += person.informalCare
                    totalChildFormalCare += person.formalCare
                    totalUnmetChildCare += person.residualNeed
                    totalChildCareDemandHours += person.hoursDemand
                    childCareReceivers += 1
                else:
                    totalSocialInformalCare += person.informalCare
                    totalSocialFormalCare += person.formalCare
                    totalUnmetSocialCare += person.residualNeed
                    totalSocialCareDemandHours += person.hoursDemand
                    socialCareReceivers += 1
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            elif person.hoursDemand == 0 and person.age >= self.p['ageTeenagers']:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                totalSupply += person.hoursInformalSupply
                numberOfCarers += 1
        visitedHousehold = []
        formalCareSupply = 0
        for person in class3:
            if person.house in visitedHousehold:
                continue
            visitedHousehold.append(person.house)
            totalSupply += person.hoursFormalSupply
        # Save stats
        if len(class3) > 0:
            self.shareCareGivers_3.append(float(numberOfCarers)/float(len(class3)))
        else:
            self.shareCareGivers_3.append(0)
            
        # totalSupply = totalInformalCareSupplyHours + totalFormalCareSupplyHours
        
        
        totalChildCare = totalChildInformalCare + totalChildFormalCare
        totalSocialCare = totalSocialInformalCare + totalSocialFormalCare
        totalInformalCare = totalChildInformalCare + totalSocialInformalCare
        totalCare = totalSocialCare + totalChildCare
        
        if totalCareDemandHours > 0:
            self.shareSocialCare_3.append(totalSocialCareDemandHours/totalCareDemandHours)
        else:
            self.shareSocialCare_3.append(0)
            
        self.totalCareSupply_3.append(totalSupply)
        if numberOfRecipients > 0:
            self.averageCareSupply_3.append(totalSupply/numberOfRecipients)
        else:
            self.averageCareSupply_3.append(0)
            
        if totalSupply > 0:
            self.ratio_UnmetCareDemand_Supply_3.append(totalUnmetDemandHours/totalSupply)
        else:
            self.ratio_UnmetCareDemand_Supply_3.append(0)
            
        self.totalCareDemand_3.append(totalCareDemandHours)
        self.totalCareSupply_3.append(totalSupply) 
        self.totalUnmetDemand_3.append(totalUnmetDemandHours) 
        self.totalInformalSupply_3.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_3.append(totalFormalCareSupplyHours)
        self.totalSocialInformalCareSupply_3.append(totalSocialInformalCare)
        self.totalSocialFormalCareSupply_3.append(totalSocialFormalCare)
        self.totalUnmetSocialCareDemand_3.append(totalUnmetSocialCare)
        self.totalChildInformalCareSupply_3.append(totalChildInformalCare)
        self.totalChildFormalCareSupply_3.append(totalChildFormalCare)
        self.totalUnmetChildCareDemand_3.append(totalUnmetChildCare)
        
        if totalCare > 0:
            self.shareInformalSupply_3.append(totalInformalCare/totalCare)
        else:
            self.shareInformalSupply_3.append(0)
            
        if totalCareDemandHours > 0:
            self.shareUnmetCareDemand_3.append(totalUnmetDemandHours/totalCareDemandHours)
        else:
            self.shareUnmetCareDemand_3.append(0)
            
        self.perCapitaUnmetCareDemand_3.append(totalUnmetDemandHours/float(len(class3)))
        
        if totalSocialCare > 0:
            self.shareInformalSocialSupply_3.append(totalSocialInformalCare/totalSocialCare)
        else:
            self.shareInformalSocialSupply_3.append(0)
            
        if totalSocialCareDemandHours > 0:
            self.shareUnmetSocialSupply_3.append(totalUnmetSocialCare/totalSocialCareDemandHours)
        else:
            self.shareUnmetSocialSupply_3.append(0)
            
        if totalChildCare > 0:
            self.shareInformalChildSupply_3.append(totalChildInformalCare/totalChildCare)
        else:
            self.shareInformalChildSupply_3.append(0)
            
        if totalChildCareDemandHours > 0:
            self.shareUnmetChildSupply_3.append(totalUnmetChildCare/totalChildCareDemandHours)
        else:
            self.shareUnmetChildSupply_3.append(0)
        
        
        if numberOfRecipients > 0:
            self.totalInformalCarePerRecipient_3.append(totalInformalCareSupplyHours/numberOfRecipients)
            self.totalFormalCarePerRecipient_3.append(totalFormalCareSupplyHours/numberOfRecipients)
            self.totalUnmetNeedPerRecipient_3.append(totalUnmetDemandHours/numberOfRecipients)
        else:
            self.totalInformalCarePerRecipient_3.append(0)
            self.totalFormalCarePerRecipient_3.append(0)
            self.totalUnmetNeedPerRecipient_3.append(0)
        if numberOfCarers > 0:
            self.totalInformalCarePerCarer_3.append(totalInformalCareSupplyHours/numberOfCarers)
            self.totalFormalCarePerCarer_3.append(totalFormalCareSupplyHours/numberOfCarers)
        else:
            self.totalInformalCarePerCarer_3.append(0)
            self.totalFormalCarePerCarer_3.append(0)
            
        if socialCareReceivers > 0:
            self.averageSocialInformalCareSupply_3.append(totalSocialInformalCare/socialCareReceivers)
            self.averageSocialFormalCareSupply_3.append(totalSocialFormalCare/socialCareReceivers)
            self.averageUnmetSocialCareDemand_3.append(totalUnmetSocialCare/socialCareReceivers)
        else:
            self.averageSocialInformalCareSupply_3.append(0)
            self.averageSocialFormalCareSupply_3.append(0)
            self.averageUnmetSocialCareDemand_3.append(0)
            
        if childCareReceivers > 0:
            self.averageChildInformalCareSupply_3.append(totalChildInformalCare/childCareReceivers)
            self.averageChildFormalCareSupply_3.append(totalChildFormalCare/childCareReceivers)
            self.averageUnmetChildCareDemand_3.append(totalUnmetChildCare/childCareReceivers)
        else:
            self.averageChildInformalCareSupply_3.append(0)
            self.averageChildFormalCareSupply_3.append(0)
            self.averageUnmetChildCareDemand_3.append(0)
        
        class4 = [x for x in self.pop.livingPeople if x.classRank == 3]
        totalSupply = 0
        totalCareDemandHours = 0
        totalSocialCareDemandHours = 0
        totalChildCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalSocialCare = 0
        totalChildCare = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        totalSocialInformalCare = 0
        totalSocialFormalCare = 0
        totalUnmetSocialCare = 0
        totalChildInformalCare = 0
        totalChildFormalCare = 0
        totalUnmetChildCare = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        socialCareReceivers = 0
        childCareReceivers = 0
        for person in class4:
            if person.hoursDemand > 0:
                if person.status == 'child':
                    totalChildInformalCare += person.informalCare
                    totalChildFormalCare += person.formalCare
                    totalUnmetChildCare += person.residualNeed
                    totalChildCareDemandHours += person.hoursDemand
                    childCareReceivers += 1
                else:
                    totalSocialInformalCare += person.informalCare
                    totalSocialFormalCare += person.formalCare
                    totalUnmetSocialCare += person.residualNeed
                    totalSocialCareDemandHours += person.hoursDemand
                    socialCareReceivers += 1
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            elif person.hoursDemand == 0 and person.age >= self.p['ageTeenagers']:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                totalSupply += person.hoursInformalSupply
                numberOfCarers += 1
        visitedHousehold = []
        formalCareSupply = 0
        for person in class4:
            if person.house in visitedHousehold:
                continue
            visitedHousehold.append(person.house)
            totalSupply += person.hoursFormalSupply
        # Save stats
        if len(class4) > 0:
            self.shareCareGivers_4.append(float(numberOfCarers)/float(len(class4)))
        else:
            self.shareCareGivers_4.append(0)
            
        # totalSupply = totalInformalCareSupplyHours + totalFormalCareSupplyHours
        
        
        totalChildCare = totalChildInformalCare + totalChildFormalCare
        totalSocialCare = totalSocialInformalCare + totalSocialFormalCare
        totalInformalCare = totalChildInformalCare + totalSocialInformalCare
        totalCare = totalSocialCare + totalChildCare
        
        if totalCareDemandHours > 0:
            self.shareSocialCare_4.append(totalSocialCareDemandHours/totalCareDemandHours)
        else:
            self.shareSocialCare_4.append(0)
            
        self.totalCareSupply_4.append(totalSupply)
        if numberOfRecipients > 0:
            self.averageCareSupply_4.append(totalSupply/numberOfRecipients)
        else:
            self.averageCareSupply_4.append(0)
            
        if totalSupply > 0:
            self.ratio_UnmetCareDemand_Supply_4.append(totalUnmetDemandHours/totalSupply)
        else:
            self.ratio_UnmetCareDemand_Supply_4.append(0)
            
        self.totalCareDemand_4.append(totalCareDemandHours)
        self.totalCareSupply_4.append(totalSupply) 
        self.totalUnmetDemand_4.append(totalUnmetDemandHours) 
        self.totalInformalSupply_4.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_4.append(totalFormalCareSupplyHours)
        self.totalSocialInformalCareSupply_4.append(totalSocialInformalCare)
        self.totalSocialFormalCareSupply_4.append(totalSocialFormalCare)
        self.totalUnmetSocialCareDemand_4.append(totalUnmetSocialCare)
        self.totalChildInformalCareSupply_4.append(totalChildInformalCare)
        self.totalChildFormalCareSupply_4.append(totalChildFormalCare)
        self.totalUnmetChildCareDemand_4.append(totalUnmetChildCare)
        
        if totalCare > 0:
            self.shareInformalSupply_4.append(totalInformalCare/totalCare)
        else:
            self.shareInformalSupply_4.append(0)
            
        if totalCareDemandHours > 0:
            self.shareUnmetCareDemand_4.append(totalUnmetDemandHours/totalCareDemandHours)
        else:
            self.shareUnmetCareDemand_4.append(0)
            
        self.perCapitaUnmetCareDemand_4.append(totalUnmetDemandHours/float(len(class4)))
        
        if totalSocialCare > 0:
            self.shareInformalSocialSupply_4.append(totalSocialInformalCare/totalSocialCare)
        else:
            self.shareInformalSocialSupply_4.append(0)
            
        if totalSocialCareDemandHours > 0:
            self.shareUnmetSocialSupply_4.append(totalUnmetSocialCare/totalSocialCareDemandHours)
        else:
            self.shareUnmetSocialSupply_4.append(0)
            
        if totalChildCare > 0:
            self.shareInformalChildSupply_4.append(totalChildInformalCare/totalChildCare)
        else:
            self.shareInformalChildSupply_4.append(0)
            
        if totalChildCareDemandHours > 0:
            self.shareUnmetChildSupply_4.append(totalUnmetChildCare/totalChildCareDemandHours)
        else:
            self.shareUnmetChildSupply_4.append(0)
        
        
        if numberOfRecipients > 0:
            self.totalInformalCarePerRecipient_4.append(totalInformalCareSupplyHours/numberOfRecipients)
            self.totalFormalCarePerRecipient_4.append(totalFormalCareSupplyHours/numberOfRecipients)
            self.totalUnmetNeedPerRecipient_4.append(totalUnmetDemandHours/numberOfRecipients)
        else:
            self.totalInformalCarePerRecipient_4.append(0)
            self.totalFormalCarePerRecipient_4.append(0)
            self.totalUnmetNeedPerRecipient_4.append(0)
        if numberOfCarers > 0:
            self.totalInformalCarePerCarer_4.append(totalInformalCareSupplyHours/numberOfCarers)
            self.totalFormalCarePerCarer_4.append(totalFormalCareSupplyHours/numberOfCarers)
        else:
            self.totalInformalCarePerCarer_4.append(0)
            self.totalFormalCarePerCarer_4.append(0)
            
        if socialCareReceivers > 0:
            self.averageSocialInformalCareSupply_4.append(totalSocialInformalCare/socialCareReceivers)
            self.averageSocialFormalCareSupply_4.append(totalSocialFormalCare/socialCareReceivers)
            self.averageUnmetSocialCareDemand_4.append(totalUnmetSocialCare/socialCareReceivers)
        else:
            self.averageSocialInformalCareSupply_4.append(0)
            self.averageSocialFormalCareSupply_4.append(0)
            self.averageUnmetSocialCareDemand_4.append(0)
            
        if childCareReceivers > 0:
            self.averageChildInformalCareSupply_4.append(totalChildInformalCare/childCareReceivers)
            self.averageChildFormalCareSupply_4.append(totalChildFormalCare/childCareReceivers)
            self.averageUnmetChildCareDemand_4.append(totalUnmetChildCare/childCareReceivers)
        else:
            self.averageChildInformalCareSupply_4.append(0)
            self.averageChildFormalCareSupply_4.append(0)
            self.averageUnmetChildCareDemand_4.append(0)
        
        class5 = [x for x in self.pop.livingPeople if x.classRank == 4]
        totalSupply = 0
        totalCareDemandHours = 0
        totalSocialCareDemandHours = 0
        totalChildCareDemandHours = 0
        totalUnmetDemandHours = 0
        totalSocialCare = 0
        totalChildCare = 0
        totalInformalCareSupplyHours = 0
        totalFormalCareSupplyHours = 0
        totalSocialInformalCare = 0
        totalSocialFormalCare = 0
        totalUnmetSocialCare = 0
        totalChildInformalCare = 0
        totalChildFormalCare = 0
        totalUnmetChildCare = 0
        numberOfRecipients = 0
        numberOfCarers = 0
        socialCareReceivers = 0
        childCareReceivers = 0
        for person in class5:
            if person.hoursDemand > 0:
                if person.status == 'child':
                    totalChildInformalCare += person.informalCare
                    totalChildFormalCare += person.formalCare
                    totalUnmetChildCare += person.residualNeed
                    totalChildCareDemandHours += person.hoursDemand
                    childCareReceivers += 1
                else:
                    totalSocialInformalCare += person.informalCare
                    totalSocialFormalCare += person.formalCare
                    totalUnmetSocialCare += person.residualNeed
                    totalSocialCareDemandHours += person.hoursDemand
                    socialCareReceivers += 1
                totalCareDemandHours += person.hoursDemand
                totalUnmetDemandHours += person.residualNeed
                numberOfRecipients += 1
            elif person.hoursDemand == 0 and person.age >= self.p['ageTeenagers']:
                totalInformalCareSupplyHours += person.socialWork
                totalFormalCareSupplyHours += person.workToCare
                totalSupply += person.hoursInformalSupply
                numberOfCarers += 1
        visitedHousehold = []
        formalCareSupply = 0
        for person in class5:
            if person.house in visitedHousehold:
                continue
            visitedHousehold.append(person.house)
            totalSupply += person.hoursFormalSupply
        # Save stats
        if len(class5) > 0:
            self.shareCareGivers_5.append(float(numberOfCarers)/float(len(class5)))
        else:
            self.shareCareGivers_5.append(0)
            
        #totalSupply = totalInformalCareSupplyHours + totalFormalCareSupplyHours
        
        
        totalChildCare = totalChildInformalCare + totalChildFormalCare
        totalSocialCare = totalSocialInformalCare + totalSocialFormalCare
        totalInformalCare = totalChildInformalCare + totalSocialInformalCare
        totalCare = totalSocialCare + totalChildCare
        
        if totalCareDemandHours > 0:
            self.shareSocialCare_5.append(totalSocialCareDemandHours/totalCareDemandHours)
        else:
            self.shareSocialCare_5.append(0)
            
        self.totalCareSupply_5.append(totalSupply)
        if numberOfRecipients > 0:
            self.averageCareSupply_5.append(totalSupply/numberOfRecipients)
        else:
            self.averageCareSupply_5.append(0)
            
        if totalSupply > 0:
            self.ratio_UnmetCareDemand_Supply_5.append(totalUnmetDemandHours/totalSupply)
        else:
            self.ratio_UnmetCareDemand_Supply_5.append(0)
            
        self.totalCareDemand_5.append(totalCareDemandHours)
        self.totalCareSupply_5.append(totalSupply) 
        self.totalUnmetDemand_5.append(totalUnmetDemandHours) 
        self.totalInformalSupply_5.append(totalInformalCareSupplyHours)
        self.totalFormalSupply_5.append(totalFormalCareSupplyHours)
        self.totalSocialInformalCareSupply_5.append(totalSocialInformalCare)
        self.totalSocialFormalCareSupply_5.append(totalSocialFormalCare)
        self.totalUnmetSocialCareDemand_5.append(totalUnmetSocialCare)
        self.totalChildInformalCareSupply_5.append(totalChildInformalCare)
        self.totalChildFormalCareSupply_5.append(totalChildFormalCare)
        self.totalUnmetChildCareDemand_5.append(totalUnmetChildCare)
        
        if totalCare > 0:
            self.shareInformalSupply_5.append(totalInformalCare/totalCare)
        else:
            self.shareInformalSupply_5.append(0)
            
        if totalCareDemandHours > 0:
            self.shareUnmetCareDemand_5.append(totalUnmetDemandHours/totalCareDemandHours)
        else:
            self.shareUnmetCareDemand_5.append(0)
            
        self.perCapitaUnmetCareDemand_5.append(totalUnmetDemandHours/float(len(class5)))
        
        if totalSocialCare > 0:
            self.shareInformalSocialSupply_5.append(totalSocialInformalCare/totalSocialCare)
        else:
            self.shareInformalSocialSupply_5.append(0)
            
        if totalSocialCareDemandHours > 0:
            self.shareUnmetSocialSupply_5.append(totalUnmetSocialCare/totalSocialCareDemandHours)
        else:
            self.shareUnmetSocialSupply_5.append(0)
            
        if totalChildCare > 0:
            self.shareInformalChildSupply_5.append(totalChildInformalCare/totalChildCare)
        else:
            self.shareInformalChildSupply_5.append(0)
            
        if totalChildCareDemandHours > 0:
            self.shareUnmetChildSupply_5.append(totalUnmetChildCare/totalChildCareDemandHours)
        else:
            self.shareUnmetChildSupply_5.append(0)
        
        
        if numberOfRecipients > 0:
            self.totalInformalCarePerRecipient_5.append(totalInformalCareSupplyHours/numberOfRecipients)
            self.totalFormalCarePerRecipient_5.append(totalFormalCareSupplyHours/numberOfRecipients)
            self.totalUnmetNeedPerRecipient_5.append(totalUnmetDemandHours/numberOfRecipients)
        else:
            self.totalInformalCarePerRecipient_5.append(0)
            self.totalFormalCarePerRecipient_5.append(0)
            self.totalUnmetNeedPerRecipient_5.append(0)
        if numberOfCarers > 0:
            self.totalInformalCarePerCarer_5.append(totalInformalCareSupplyHours/numberOfCarers)
            self.totalFormalCarePerCarer_5.append(totalFormalCareSupplyHours/numberOfCarers)
        else:
            self.totalInformalCarePerCarer_5.append(0)
            self.totalFormalCarePerCarer_5.append(0)
            
        if socialCareReceivers > 0:
            self.averageSocialInformalCareSupply_5.append(totalSocialInformalCare/socialCareReceivers)
            self.averageSocialFormalCareSupply_5.append(totalSocialFormalCare/socialCareReceivers)
            self.averageUnmetSocialCareDemand_5.append(totalUnmetSocialCare/socialCareReceivers)
        else:
            self.averageSocialInformalCareSupply_5.append(0)
            self.averageSocialFormalCareSupply_5.append(0)
            self.averageUnmetSocialCareDemand_5.append(0)
            
        if childCareReceivers > 0:
            self.averageChildInformalCareSupply_5.append(totalChildInformalCare/childCareReceivers)
            self.averageChildFormalCareSupply_5.append(totalChildFormalCare/childCareReceivers)
            self.averageUnmetChildCareDemand_5.append(totalUnmetChildCare/childCareReceivers)
        else:
            self.averageChildInformalCareSupply_5.append(0)
            self.averageChildFormalCareSupply_5.append(0)
            self.averageUnmetChildCareDemand_5.append(0)
        
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
        
        self.healthCareCost.append(self.hospitalizationCost)
        self.perCapitaHealthCareCost.append(self.hospitalizationCost/len(self.pop.livingPeople))
        
        self.unmetSocialCareNeedDistribution = [x.residualNeed for x in self.pop.livingPeople if x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution))
        self.unmetSocialCareNeedDistribution_1 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 0 and x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient_1.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution_1))
        self.unmetSocialCareNeedDistribution_2 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 1 and x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient_2.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution_2))
        self.unmetSocialCareNeedDistribution_3 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 2 and x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient_3.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution_3))
        self.unmetSocialCareNeedDistribution_4 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 3 and x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient_4.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution_4))
        self.unmetSocialCareNeedDistribution_5 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 4 and x.careNeedLevel > 0]
        self.unmetSocialCareNeedGiniCoefficient_5.append(self.computeGiniCoefficient(self.unmetSocialCareNeedDistribution_5))
        
        self.shareUnmetSocialCareNeedDistribution = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution))
        self.shareUnmetSocialCareNeedDistribution_1 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 0 and x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient_1.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution_1))
        self.shareUnmetSocialCareNeedDistribution_2 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 1 and x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient_2.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution_2))
        self.shareUnmetSocialCareNeedDistribution_3 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 2 and x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient_3.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution_3))
        self.shareUnmetSocialCareNeedDistribution_4 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 3 and x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient_4.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution_4))
        self.shareUnmetSocialCareNeedDistribution_5 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 4 and x.careNeedLevel > 0]
        self.shareUnmetSocialCareNeedGiniCoefficient_5.append(self.computeGiniCoefficient(self.shareUnmetSocialCareNeedDistribution_5))
        
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
        if len(employed_1) + len(unemployed_1) > 0: 
            employmentRate_1 = float(len(employed_1))/(float(len(employed_1)) + float(len(unemployed_1)))
        else:
            employmentRate_1 = 0
        self.totalEmployment_1.append(employmentRate_1)
        # print('Employment rate of class 1: ' + str(employmentRate_1))
        
        employed_2 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 1]
        employed_2_Males = [x for x in employed_2 if x.sex == 'male']
        employed_2_Females = [x for x in employed_2 if x.sex == 'female']
        unemployed_2 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 1]
        if len(employed_2) + len(unemployed_2) > 0: 
            employmentRate_2 = float(len(employed_2))/(float(len(employed_2)) + float(len(unemployed_2)))
        else:
            employmentRate_2 = 0
        self.totalEmployment_2.append(employmentRate_2)
        # print('Employment rate of class 2: ' + str(employmentRate_2))
        
        employed_3 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 2]
        employed_3_Males = [x for x in employed_3 if x.sex == 'male']
        employed_3_Females = [x for x in employed_3 if x.sex == 'female']
        unemployed_3 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 2]
        if len(employed_3) + len(unemployed_3) > 0: 
            employmentRate_3 = float(len(employed_3))/(float(len(employed_3)) + float(len(unemployed_3)))
        else:
            employmentRate_3 = 0
        self.totalEmployment_3.append(employmentRate_3)
        # print('Employment rate of class 3: ' + str(employmentRate_3))
        
        employed_4 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 3]
        employed_4_Males = [x for x in employed_4 if x.sex == 'male']
        employed_4_Females = [x for x in employed_4 if x.sex == 'female']
        unemployed_4 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 3]
        if len(employed_4) + len(unemployed_4) > 0:
            employmentRate_4 = float(len(employed_4))/(float(len(employed_4)) + float(len(unemployed_4)))
        else:
            employmentRate_4 = 0
        self.totalEmployment_4.append(employmentRate_4)
        # print('Employment rate of class 4: ' + str(employmentRate_4))
        
        employed_5 = [x for x in self.pop.livingPeople if x.status == 'employed' and x.classRank == 4]
        employed_5_Males = [x for x in employed_5 if x.sex == 'male']
        employed_5_Females = [x for x in employed_5 if x.sex == 'female']
        unemployed_5 = [x for x in self.pop.livingPeople if x.status == 'unemployed' and x.classRank == 4]
        if len(employed_5) + len(unemployed_5) > 0: 
            employmentRate_5 = float(len(employed_5))/(float(len(employed_5)) + float(len(unemployed_5)))
        else:
            employmentRate_5 = 0
        self.totalEmployment_5.append(employmentRate_5)
        # print('Employment rate of class 5: ' + str(employmentRate_5))
        
        jobChanges = [x for x in self.pop.livingPeople if x.status == 'employed' and x.jobChange == True]
        jobChangeRate = float(len(jobChanges))/float(len(employed))
        self.totalJobChanges.append(jobChangeRate)
        # print('Job Change Rate: ' + str(jobChangeRate))
        
        self.popHourlyWages = [x.hourlyWage for x in self.pop.livingPeople if x.status == 'employed']
        
        averageMalesWage = 0
        averageFemalesWage = 0
        employedMales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'male']
        
        if len(employedMales) > 0:
            averageMalesWage = sum([x.hourlyWage for x in employedMales])/float(len(employedMales))
        else:
            averageMalesWage = 0
        self.averageWage_M.append(averageMalesWage)
        
        employedFemales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'female']
        if len(employedFemales) > 0:
            averageFemalesWage = sum([x.hourlyWage for x in employedFemales])/float(len(employedFemales))
        else:
            averageFemalesWage = 0
        self.averageWage_F.append(averageFemalesWage)
        
        if averageMalesWage > 0:
            self.ratioWomenMaleWage.append(averageFemalesWage/averageMalesWage)
        else:
            self.ratioWomenMaleWage.append(0)
        
        Wage_1 = sum([x.hourlyWage for x in employed_1])
        Wage_1_Males = sum([x.hourlyWage for x in employed_1_Males])
        Wage_1_Females = sum([x.hourlyWage for x in employed_1_Females])
        if len(employed_1) > 0:
            averageWage = Wage_1/float(len(employed_1))
        else:
            averageWage = 0
        self.averageWage_1.append(averageWage)
        
        averageWage_M = 0
        averageWage_F = 0
        if len(employed_1_Males) > 0:
            averageWage_M = Wage_1_Males/float(len(employed_1_Males))
        else:
            averageWage_M = 0
        self.averageWage_1_Males.append(averageWage_M)
        
        if len(employed_1_Females) > 0:
            averageWage_F = Wage_1_Females/float(len(employed_1_Females))
        else:
            averageWage_F = 0
        self.averageWage_1_Females.append(averageWage_F)
        
        if averageWage_M > 0:
            self.ratioWomenMaleWage_1.append(averageWage_F/averageWage_M)
        else:
            self.ratioWomenMaleWage_1.append(0)
        
        Wage_2 = sum([x.hourlyWage for x in employed_2])
        Wage_2_Males = sum([x.hourlyWage for x in employed_2_Males])
        Wage_2_Females = sum([x.hourlyWage for x in employed_2_Females])
        if len(employed_2) > 0:
            averageWage = Wage_2/float(len(employed_2))
        else:
            averageWage = 0
        self.averageWage_2.append(averageWage)
        
        averageWage_M = 0
        averageWage_F = 0
        if len(employed_2_Males) > 0:
            averageWage_M = Wage_2_Males/float(len(employed_2_Males))
        else:
            averageWage_M = 0
        self.averageWage_2_Males.append(averageWage_M)
        if len(employed_2_Females) > 0:
            averageWage_F = Wage_2_Females/float(len(employed_2_Females))
        else:
            averageWage_F = 0
        self.averageWage_2_Females.append(averageWage_F)
        
        if averageWage_M > 0:
            self.ratioWomenMaleWage_2.append(averageWage_F/averageWage_M)
        else:
            self.ratioWomenMaleWage_2.append(0)
        
        Wage_3 = sum([x.hourlyWage for x in employed_3])
        Wage_3_Males = sum([x.hourlyWage for x in employed_3_Males])
        Wage_3_Females = sum([x.hourlyWage for x in employed_3_Females])
        if len(employed_3) > 0:
            averageWage = Wage_3/float(len(employed_3))
        else:
            averageWage = 0
        self.averageWage_3.append(averageWage)
        
        averageWage_M = 0
        averageWage_F = 0
        if len(employed_3_Males) > 0:
            averageWage_M = Wage_3_Males/float(len(employed_3_Males))
        else:
            averageWage_M = 0
        self.averageWage_3_Males.append(averageWage_M)
        if len(employed_3_Females) > 0:
            averageWage_F = Wage_3_Females/float(len(employed_3_Females))
        else:
            averageWage_F = 0
        self.averageWage_3_Females.append(averageWage_F)
        
        if averageWage_M > 0:
            self.ratioWomenMaleWage_3.append(averageWage_F/averageWage_M)
        else:
            self.ratioWomenMaleWage_3.append(0)
        
        Wage_4 = sum([x.hourlyWage for x in employed_4])
        Wage_4_Males = sum([x.hourlyWage for x in employed_4_Males])
        Wage_4_Females = sum([x.hourlyWage for x in employed_4_Females])
        if len(employed_4) > 0:
            averageWage = Wage_4/float(len(employed_4))
        else:
            averageWage = 0
        self.averageWage_4.append(averageWage)
        
        averageWage_M = 0
        averageWage_F = 0
        if len(employed_4_Males) > 0:
            averageWage_M = Wage_4_Males/float(len(employed_4_Males))
        else:
            averageWage_M = 0
        self.averageWage_4_Males.append(averageWage_M)
        if len(employed_4_Females) > 0:
            averageWage_F = Wage_4_Females/float(len(employed_4_Females))
        else:
            averageWage_F = 0
        self.averageWage_4_Females.append(averageWage_F)
        
        if averageWage_M > 0:
            self.ratioWomenMaleWage_4.append(averageWage_F/averageWage_M)
        else:
            self.ratioWomenMaleWage_4.append(0)
        
        Wage_5 = sum([x.hourlyWage for x in employed_5])
        Wage_5_Males = sum([x.hourlyWage for x in employed_5_Males])
        Wage_5_Females = sum([x.hourlyWage for x in employed_5_Females])
        if len(employed_5) > 0:
            averageWage = Wage_5/float(len(employed_5))
        else:
            averageWage = 0
        self.averageWage_5.append(averageWage)
        
        averageWage_M = 0
        averageWage_F = 0
        if len(employed_5_Males) > 0:
            averageWage_M = Wage_5_Males/float(len(employed_5_Males))
        else:
            averageWage_M = 0
        self.averageWage_5_Males.append(averageWage_M)
        if len(employed_5_Females) > 0:
            averageWage_F = Wage_5_Females/float(len(employed_5_Females))
        else:
            averageWage_F = 0
        self.averageWage_5_Females.append(averageWage_F)
        
        if averageWage_M > 0:
            self.ratioWomenMaleWage_5.append(averageWage_F/averageWage_M)
        else:
            self.ratioWomenMaleWage_5.append(0)
            
        ####### Mobility Outputs ################################################################
        
        self.numberRelocations.append(self.totalRelocations)
        self.totalRelocations = 0
        
        self.numJobRelocations_1.append(self.jobRelocations_1)
        self.jobRelocations_1 = 0
        self.numJobRelocations_2.append(self.jobRelocations_2)
        self.jobRelocations_2 = 0
        self.numJobRelocations_3.append(self.jobRelocations_3)
        self.jobRelocations_3 = 0
        self.numJobRelocations_4.append(self.jobRelocations_4)
        self.jobRelocations_4 = 0
        self.numJobRelocations_5.append(self.jobRelocations_5)
        self.jobRelocations_5 = 0
        
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
    
    def computeGiniCoefficient(self, unmetCareNeeds):
        sorted_list = sorted(unmetCareNeeds)
        height, area = 0, 0
        for value in sorted_list:
            height += float(value)
            area += height - float(value)/2.
        fair_area = height*len(unmetCareNeeds)/float(2)
        if fair_area > 0:
            return (fair_area-area)/fair_area
        else:
            return 0
    
    def relocationProb(self, newocc, oldocc, firstocc):
        alfa = self.p['baseRelocatingProb']/(1+self.p['baseRelocatingProb'])
        totOcc = float(newocc+oldocc)
        deltaOccupants = (totOcc-firstocc)/float(firstocc)
        
        # Check variable
        self.deltaHouseOccupants.append(deltaOccupants) # Min-Max: -0.5 - 2
        
        prob = 1.0 - 1.0/math.exp(self.p['relocationParameter']*deltaOccupants)
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
        ax.plot(years, self.totalCareSupply, linewidth=2, label = 'Potential Supply', color = 'green')
        ax.stackplot(years, self.totalSocialCareDemand, self.totalChildCareDemand, labels = ['Social Care Need','Child Care Needs'])
        # ax.plot(years, self.totalSocialCareDemand, linewidth=2, label = 'Social Care Need', color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        ax.set_title('Care Needs and Potential Supply')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/DemandSupplyStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 2: shares of care givers, total and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareCareGivers, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareCareGivers_1, label = 'Class I')
        p3, = ax.plot(years, self.shareCareGivers_2, label = 'Class II')
        p4, = ax.plot(years, self.shareCareGivers_3, label = 'Class III')
        p5, = ax.plot(years, self.shareCareGivers_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareCareGivers_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Population')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Care Givers')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareCareGiversChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 3: shares of care takers by level of care need
        fig, ax = plt.subplots()
        ax.stackplot(years, self.shareSocialCareTakers_N1, self.shareSocialCareTakers_N2, 
                      self.shareSocialCareTakers_N3, self.shareSocialCareTakers_N4,
                      labels = ['Need Level 1','Need Level 2', 'Need Level 3', 'Need level 4'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care Takers')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Care Takers by Care Need Level')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.ylim(0, 1)
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareByNeedLevelsStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 4: Share of Social Care Needs (1960-2020)
        
        self.sharesSocialCare_M.append(np.mean(self.shareSocialCareDemand[-20:]))
        self.sharesSocialCare_SD.append(np.std(self.shareSocialCareDemand[-20:]))
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareSocialCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareSocialCare_1, label = 'Class I')
        p3, = ax.plot(years, self.shareSocialCare_2, label = 'Class II')
        p4, = ax.plot(years, self.shareSocialCare_3, label = 'Class III')
        p5, = ax.plot(years, self.shareSocialCare_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareSocialCare_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care Need')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Social Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareSocialCareNeedsChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 5: Per Capita total care demand and unmet care demand (1960-2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.perCapitaCareReceived, self.perCapitaUnmetCareDemand, labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Care and Unmet Care')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaCareUnmetCareChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 6: Per Capita total social care demand and unmet social care demand (1960-2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.perCapitaSocialCareReceived, self.perCapitaUnmetSocialCareDemand, labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Demand and Unmet Social Care')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaDemandUnmetSocialCareChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 7: Per Capita total child care demand and unmet child care demand (1960-2020)
        
        fig, ax = plt.subplots()
        ax.stackplot(years, self.perCapitaChildCareReceived, self.perCapitaUnmetChildCareDemand, labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Demand and Unmet Child Care')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaDemandUnmetChildCareChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 8: total informal and formal care received and unmet care needs (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalCareReceived, self.totalFormalCareReceived, 
                      self.totalUnmetCareDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Care and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/CareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 9: Shares informal care received (from 1960 to 2020)
        
        self.sharesInformalCare_M.append(np.mean(self.shareInformalCareReceived[-20:]))
        self.sharesInformalCare_SD.append(np.std(self.shareInformalCareReceived[-20:]))
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareInformalCareReceived, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareInformalSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.shareInformalSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.shareInformalSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.shareInformalSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareInformalSupply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareInformalCareReceivedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        
        # Chart 10: Shares informal social care received (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareInformalSocialCareReceived, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareInformalSocialSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.shareInformalSocialSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.shareInformalSocialSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.shareInformalSocialSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareInformalSocialSupply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Social Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareInformalSocialCareReceivedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 11: Shares informal child care received (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareInformalChildCareReceived, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareInformalChildSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.shareInformalChildSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.shareInformalChildSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.shareInformalChildSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareInformalChildSupply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Child Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareInformalChildCareReceivedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 12: total informal and formal social care received and unmet social care needs (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalSocialCareReceived, self.totalFormalSocialCareReceived, 
                      self.totalSocialCareUnmetDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Social Care and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/SocialCareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 13: total informal and formal child care received and unmet child care needs (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        ax.stackplot(years, self.totalInformalChildCareReceived, self.totalFormalChildCareReceived, 
                      self.totalChildCareUnmetDemand, labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Child Social Care and Unmet Child Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        fig.tight_layout()
        filename = folder + '/ChildCareReceivedStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 14: Share of Unmet Care Need, total and by social class (from 1960 to 2020)
        
        
        
        
        self.sharesUnmetCare_M.append(np.mean(self.shareUnmetCareDemand[-20:]))
        self.sharesUnmetCare_SD.append(np.std(self.shareUnmetCareDemand[-20:]))
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
        p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
        p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
        p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareUnmetCareNeedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 15: Share of Unmet Social Care Need, total and by social class (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetSocialCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareUnmetSocialSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.shareUnmetSocialSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.shareUnmetSocialSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.shareUnmetSocialSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareUnmetSocialSupply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Unmet Social Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareUnmetSocialCareNeedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 16: Share of Unmet Child Care Need, total and by social class (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetChildCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareUnmetChildSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.shareUnmetChildSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.shareUnmetChildSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.shareUnmetChildSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareUnmetChildSupply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Unmet Child Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareUnmetChildCareNeedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 17: Per Capita Unmet Care Need, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.perCapitaUnmetCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.perCapitaUnmetCareDemand_1, label = 'Class I')
        p3, = ax.plot(years, self.perCapitaUnmetCareDemand_2, label = 'Class II')
        p4, = ax.plot(years, self.perCapitaUnmetCareDemand_3, label = 'Class III')
        p5, = ax.plot(years, self.perCapitaUnmetCareDemand_4, label = 'Class IV')
        p6, = ax.plot(years, self.perCapitaUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaUnmetNeedChartByClass.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 18: Average Unmet Care Need, total and by social class (from 1960 to 2020)
        
        self.averagesUnmetCare_M.append(np.mean(self.averageUnmetCareDemand[-20:]))
        self.averagesUnmetCare_SD.append(np.std(self.averageUnmetCareDemand[-20:]))
        
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageUnmetCareDemand, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.totalUnmetNeedPerRecipient_1, label = 'Class I')
        p3, = ax.plot(years, self.totalUnmetNeedPerRecipient_2, label = 'Class II')
        p4, = ax.plot(years, self.totalUnmetNeedPerRecipient_3, label = 'Class III')
        p5, = ax.plot(years, self.totalUnmetNeedPerRecipient_4, label = 'Class IV')
        p6, = ax.plot(years, self.totalUnmetNeedPerRecipient_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AverageUnmetCareNeedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 19: informal and formal care received and unmet care needs by social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.totalInformalSupply_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.totalFormalSupply_1[-20:])
        meanUnmetNeed_1 = np.mean(self.totalUnmetDemand_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.totalInformalSupply_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.totalFormalSupply_2[-20:])
        meanUnmetNeed_2 = np.mean(self.totalUnmetDemand_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.totalInformalSupply_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.totalFormalSupply_3[-20:])
        meanUnmetNeed_3 = np.mean(self.totalUnmetDemand_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.totalInformalSupply_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.totalFormalSupply_4[-20:])
        meanUnmetNeed_4 = np.mean(self.totalUnmetDemand_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.totalInformalSupply_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.totalFormalSupply_5[-20:])
        meanUnmetNeed_5 = np.mean(self.totalUnmetDemand_5[-20:])
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
        ax.set_title('Informal, Formal and Unmet Care Need by Class')
        fig.tight_layout()
        filename = folder + '/CareByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 20: informal and formal care received and unmet care needs per recipient by social class (mean of last 20 years)
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
        
       # Chart 21: informal and formal social care received and unmet social care needs by social class (mean of last 20 years)
      
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.totalSocialInformalCareSupply_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.totalSocialFormalCareSupply_1[-20:])
        meanUnmetNeed_1 = np.mean(self.totalUnmetSocialCareDemand_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.totalSocialInformalCareSupply_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.totalSocialFormalCareSupply_2[-20:])
        meanUnmetNeed_2 = np.mean(self.totalUnmetSocialCareDemand_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.totalSocialInformalCareSupply_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.totalSocialFormalCareSupply_3[-20:])
        meanUnmetNeed_3 = np.mean(self.totalUnmetSocialCareDemand_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.totalSocialInformalCareSupply_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.totalSocialFormalCareSupply_4[-20:])
        meanUnmetNeed_4 = np.mean(self.totalUnmetSocialCareDemand_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.totalSocialInformalCareSupply_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.totalSocialFormalCareSupply_5[-20:])
        meanUnmetNeed_5 = np.mean(self.totalUnmetSocialCareDemand_5[-20:])
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
        ax.set_title('Informal, Formal and Unmet Social Care Need by Class')
        fig.tight_layout()
        filename = folder + '/SocialCareByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 22: informal and formal social care received and unmet social care needs per recipient by social class (mean of last 20 years)
        
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.averageSocialInformalCareSupply_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.averageSocialFormalCareSupply_1[-20:])
        meanUnmetNeed_1 = np.mean(self.averageUnmetSocialCareDemand_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.averageSocialInformalCareSupply_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.averageSocialFormalCareSupply_2[-20:])
        meanUnmetNeed_2 = np.mean(self.averageUnmetSocialCareDemand_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.averageSocialInformalCareSupply_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.averageSocialFormalCareSupply_3[-20:])
        meanUnmetNeed_3 = np.mean(self.averageUnmetSocialCareDemand_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.averageSocialInformalCareSupply_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.averageSocialFormalCareSupply_4[-20:])
        meanUnmetNeed_4 = np.mean(self.averageUnmetSocialCareDemand_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.averageSocialInformalCareSupply_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.averageSocialFormalCareSupply_5[-20:])
        meanUnmetNeed_5 = np.mean(self.averageUnmetSocialCareDemand_5[-20:])
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
        ax.set_title('Informal, Formal and Unmet Social Care Need per Recipient')
        fig.tight_layout()
        filename = folder + '/SocialCarePerRecipientByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 23: informal and formal child care received and unmet child care needs by social class (mean of last 20 years)
      
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.totalChildInformalCareSupply_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.totalChildFormalCareSupply_1[-20:])
        meanUnmetNeed_1 = np.mean(self.totalUnmetChildCareDemand_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.totalChildInformalCareSupply_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.totalChildFormalCareSupply_2[-20:])
        meanUnmetNeed_2 = np.mean(self.totalUnmetChildCareDemand_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.totalChildInformalCareSupply_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.totalChildFormalCareSupply_3[-20:])
        meanUnmetNeed_3 = np.mean(self.totalUnmetChildCareDemand_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.totalChildInformalCareSupply_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.totalChildFormalCareSupply_4[-20:])
        meanUnmetNeed_4 = np.mean(self.totalUnmetChildCareDemand_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.totalChildInformalCareSupply_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.totalChildFormalCareSupply_5[-20:])
        meanUnmetNeed_5 = np.mean(self.totalUnmetChildCareDemand_5[-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours of care')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Child Care Need by Class')
        fig.tight_layout()
        filename = folder + '/ChildCareByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 24: informal and formal child care received and unmet child care needs per recipient by Child class (mean of last 20 years)
        
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(self.averageChildInformalCareSupply_1[-20:])
        meanFormalCareReceived_1 = np.mean(self.averageChildFormalCareSupply_1[-20:])
        meanUnmetNeed_1 = np.mean(self.averageUnmetChildCareDemand_1[-20:])
        meanInformalCareReceived_2 = np.mean(self.averageChildInformalCareSupply_2[-20:])
        meanFormalCareReceived_2 = np.mean(self.averageChildFormalCareSupply_2[-20:])
        meanUnmetNeed_2 = np.mean(self.averageUnmetChildCareDemand_2[-20:])
        meanInformalCareReceived_3 = np.mean(self.averageChildInformalCareSupply_3[-20:])
        meanFormalCareReceived_3 = np.mean(self.averageChildFormalCareSupply_3[-20:])
        meanUnmetNeed_3 = np.mean(self.averageUnmetChildCareDemand_3[-20:])
        meanInformalCareReceived_4 = np.mean(self.averageChildInformalCareSupply_4[-20:])
        meanFormalCareReceived_4 = np.mean(self.averageChildFormalCareSupply_4[-20:])
        meanUnmetNeed_4 = np.mean(self.averageUnmetChildCareDemand_4[-20:])
        meanInformalCareReceived_5 = np.mean(self.averageChildInformalCareSupply_5[-20:])
        meanFormalCareReceived_5 = np.mean(self.averageChildFormalCareSupply_5[-20:])
        meanUnmetNeed_5 = np.mean(self.averageUnmetChildCareDemand_5[-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_ylabel('Hours of care')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Child Care Need per Recipient')
        fig.tight_layout()
        filename = folder + '/ChildCarePerRecipientByClassStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 25: informal and formal care supplied per carer by social class (mean of last 20 years)
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
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_ylabel('Hours of care')
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
        
        # Chart 26: informal and formal care supplied by kinship network distance (mean of last 20 years) # Modified y lim
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
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_xticks(ind)
        plt.xticks(ind, ('Household', 'I', 'II', 'III'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper right')
        ax.set_title('Informal and Formal Care per Kinship Level')
        fig.tight_layout()
        filename = folder + '/InformalFormalCareByKinshipStackedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 27: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareFemaleInformalCareSupplied, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareFemaleInformalCareSupplied_1, label = 'Class I')
        p3, = ax.plot(years, self.shareFemaleInformalCareSupplied_2, label = 'Class II')
        p4, = ax.plot(years, self.shareFemaleInformalCareSupplied_3, label = 'Class III')
        p5, = ax.plot(years, self.shareFemaleInformalCareSupplied_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareFemaleInformalCareSupplied_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Care supplied by Women')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareCareWomedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 28: informal care provided by gender per social class (mean of last 20 years)
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
        
         # Chart 29: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.ratioWomenMaleWage, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.ratioWomenMaleWage_1, label = 'Class I')
        p3, = ax.plot(years, self.ratioWomenMaleWage_2, label = 'Class II')
        p4, = ax.plot(years, self.ratioWomenMaleWage_3, label = 'Class III')
        p5, = ax.plot(years, self.ratioWomenMaleWage_4, label = 'Class IV')
        p6, = ax.plot(years, self.ratioWomenMaleWage_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Wage Ratio')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Women and Men Wage Ratio')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/WomenMenWageRatioChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 30: income by gender per social class (mean of last 20 years)
        n_groups = self.p['numberClasses']
        WageMales_1 = np.mean(self.averageWage_1_Males[-20:])
        WageMales_2 = np.mean(self.averageWage_2_Males[-20:])
        WageMales_3 = np.mean(self.averageWage_3_Males[-20:])
        WageMales_4 = np.mean(self.averageWage_4_Males[-20:])
        WageMales_5 = np.mean(self.averageWage_5_Males[-20:])
        WageFemales_1 = np.mean(self.averageWage_1_Females[-20:])
        WageFemales_2 = np.mean(self.averageWage_2_Females[-20:])
        WageFemales_3 = np.mean(self.averageWage_3_Females[-20:])
        WageFemales_4 = np.mean(self.averageWage_4_Females[-20:])
        WageFemales_5 = np.mean(self.averageWage_5_Females[-20:])
        means_males = (WageMales_1, WageMales_2, WageMales_3, WageMales_4, WageMales_5)
        means_females = (WageFemales_1, WageFemales_2, WageFemales_3, WageFemales_4, WageFemales_5)
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
        ax.set_ylabel('Average Wage')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Female and Male Average Wage')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        plt.tight_layout()
        filename = folder + '/WageByGenderAndClassGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 31: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.ratioWomenMaleIncome, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.ratioWomenMaleIncome_1, label = 'Class I')
        p3, = ax.plot(years, self.ratioWomenMaleIncome_2, label = 'Class II')
        p4, = ax.plot(years, self.ratioWomenMaleIncome_3, label = 'Class III')
        p5, = ax.plot(years, self.ratioWomenMaleIncome_4, label = 'Class IV')
        p6, = ax.plot(years, self.ratioWomenMaleIncome_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Income Ratio')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Women and Men Income Ratio')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/WomenMenIncomeRatioChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 32: income by gender per social class (mean of last 20 years)
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
        # Chart 33: Population by social class and number of taxpayers (1960-2020)
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
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PopulationTaxPayersStackedChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 34: Average Household size (1960-2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.avgHouseholdSize_1, label = 'Class I')
        p2, = ax.plot(years, self.avgHouseholdSize_2, label = 'Class II')
        p3, = ax.plot(years, self.avgHouseholdSize_3, label = 'Class III')
        p4, = ax.plot(years, self.avgHouseholdSize_4, label = 'Class IV')
        p5, = ax.plot(years, self.avgHouseholdSize_5, label = 'Class V')
        maxValue = max(self.avgHouseholdSize_1+self.avgHouseholdSize_2+self.avgHouseholdSize_3+self.avgHouseholdSize_4+self.avgHouseholdSize_5)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylim([0, maxValue*2.0])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Family Size')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
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
        
        # Chart 35: Average Tax Burden (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.totalTaxBurden, linewidth = 2, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Care costs per taxpayer per year')
        ax.set_xlabel('Year')
        ax.set_title('Average Tax Burden in pounds')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/TaxBurdenChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()  
      
        # Chart 36: Proportion of married adult women (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.marriageProp, linewidth = 2, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Proportion of married adult women')
        ax.set_title('Marriage Rate (females)')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/MarriageRateChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 37: Health Care Cost (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(years, self.healthCareCost, linewidth = 2, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Cost in Pounds')
        ax.set_xlabel('Year')
        ax.set_title('Total Health Care Cost')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/TotalHealthCareCostChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 38: Per Capita Health Care Cost (1960-2020)
        

        self.perCapitaHospitalizationCost_M.append(np.mean(self.perCapitaHealthCareCost[-20:]))
        self.perCapitaHospitalizationCost_SD.append(np.std(self.perCapitaHealthCareCost[-20:]))
        
        
        fig, ax = plt.subplots()
        ax.plot(years, self.perCapitaHealthCareCost, linewidth = 2, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Cost in Pounds')
        ax.set_xlabel('Year')
        ax.set_title('Per Capita Health Care Cost')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaHealthCareCostChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 39 Gini Coefficient of Unmet Social Care (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient_1, label = 'Class I')
        p3, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient_2, label = 'Class II')
        p4, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient_3, label = 'Class III')
        p5, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient_4, label = 'Class IV')
        p6, = ax.plot(years, self.unmetSocialCareNeedGiniCoefficient_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Gini Coefficient')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Unmet Social Care Gini Coeffcient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/UnmetSocialCareGiniCoefficientChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 40: Gini Coefficient of Share of Unmet Social Care (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient_1, label = 'Class I')
        p3, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient_2, label = 'Class II')
        p4, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient_3, label = 'Class III')
        p5, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient_4, label = 'Class IV')
        p6, = ax.plot(years, self.shareUnmetSocialCareNeedGiniCoefficient_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Gini Coefficient')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Unmet Social Care Gini Coeffcient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareUnmetSocialCareGiniCoefficientChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 41: Unmet Social Care Density (2030)
        data1 = self.unmetSocialCareNeedDistribution
        data2 = self.unmetSocialCareNeedDistribution_1
        data3 = self.unmetSocialCareNeedDistribution_2
        data4 = self.unmetSocialCareNeedDistribution_3
        data5 = self.unmetSocialCareNeedDistribution_4
        data6 = self.unmetSocialCareNeedDistribution_5
        data = [data1, data2, data3, data4, data5, data6]
        fig, ax = plt.subplots()
        ax.boxplot(data, labels = ('Pop', 'I', 'II', 'III', 'IV', 'V'))
        ax.set_ylabel("Unmet Social Care")
        ax.set_xlabel("Populations")
        ax.set_title('Unmet Social Care Distribution')
        fig.tight_layout()
        filename = folder + '/UnmetSocialCareDistributionChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 42: Unmet Social Care Density by SES (2030)
        data1 = self.shareUnmetSocialCareNeedDistribution
        data2 = self.shareUnmetSocialCareNeedDistribution_1
        data3 = self.shareUnmetSocialCareNeedDistribution_2
        data4 = self.shareUnmetSocialCareNeedDistribution_3
        data5 = self.shareUnmetSocialCareNeedDistribution_4
        data6 = self.shareUnmetSocialCareNeedDistribution_5
        data = [data1, data2, data3, data4, data5, data6]
        fig, ax = plt.subplots()
        ax.boxplot(data, labels = ('Pop', 'I', 'II', 'III', 'IV', 'V'))
        ax.set_ylabel("Share of Unmet Social Care")
        ax.set_xlabel("Populations")
        ax.set_title('Share of Unmet Social Care Distribution')
        fig.tight_layout()
        filename = folder + '/UnmetSocialCareDistributionChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 43: income distribution
        data = self.popHourlyWages
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylabel("Density")
        ax.set_xlabel("Hourly Wage")
        ax.set_title('Hourly Wage Distribution')
        fig.tight_layout()
        sns.kdeplot(data, shade=True)
        fig.tight_layout()
        filename = folder + '/HourlyWageDistributionChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 44: Public supply
        fig, ax = plt.subplots()
        ax.plot(years, self.publicSocialCareSupply, linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Public Social Care Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PublicSocialCareSupplyChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 45: Aggregate QALY
        fig, ax = plt.subplots()
        ax.plot(years, self.aggregateQALY, linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('QALY Index')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Aggregate QALY Index')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AggregateQALYChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
         # Chart 46: Average QALY
        fig, ax = plt.subplots()
        ax.plot(years, self.averageQALY, linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('QALY Index')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Average QALY Index')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AverageQALYChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        self.qualityAdjustedLifeYears_M.append(np.mean(self.discountedQALY[-20:]))
        self.qualityAdjustedLifeYears_SD.append(np.std(self.discountedQALY[-20:]))
        
        self.perCapitaQualityAdjustedLifeYears_M.append(np.mean(self.averageDiscountedQALY[-20:]))
        self.perCapitaQualityAdjustedLifeYears_SD.append(np.std(self.averageDiscountedQALY[-20:]))
        
        
        # Chart 47: Average Supply by Class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageCareSupply, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.averageCareSupply_1, label = 'Class I')
        p3, = ax.plot(years, self.averageCareSupply_2, label = 'Class II')
        p4, = ax.plot(years, self.averageCareSupply_3, label = 'Class III')
        p5, = ax.plot(years, self.averageCareSupply_4, label = 'Class IV')
        p6, = ax.plot(years, self.averageCareSupply_5, label = 'Class V')
        maxValue = max(self.averageCareSupply+self.averageCareSupply_1+self.averageCareSupply_2+self.averageCareSupply_3+self.averageCareSupply_4+self.averageCareSupply_5)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylim([0, maxValue*2.0])
        ax.set_ylabel('Hours of Supply')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Hours of Potential Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AverageCareSupplyChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 48: Ratio of Unmet Care Need and Total Supply (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.ratio_UnmetCareDemand_Supply, linewidth = 3, label = 'Population')
        p2, = ax.plot(years, self.ratio_UnmetCareDemand_Supply_1, label = 'Class I')
        p3, = ax.plot(years, self.ratio_UnmetCareDemand_Supply_2, label = 'Class II')
        p4, = ax.plot(years, self.ratio_UnmetCareDemand_Supply_3, label = 'Class III')
        p5, = ax.plot(years, self.ratio_UnmetCareDemand_Supply_4, label = 'Class IV')
        p6, = ax.plot(years, self.ratio_UnmetCareDemand_Supply_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Total Supply')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Ratio of Unmet Care Need and Total Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/RatioUnmetCareNeedTotalSupply.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        ####  Empty Time Series
        self.times = []
        self.pops = []
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
        self.socialMobility_1to1 = []
        self.socialMobility_1to2 = []
        self.socialMobility_1to3 = []
        self.socialMobility_1to4 = []
        self.socialMobility_1to5 = []
        self.socialMobility_2to1 = []
        self.socialMobility_2to2 = []
        self.socialMobility_2to3 = []
        self.socialMobility_2to4 = []
        self.socialMobility_2to5 = []
        self.socialMobility_3to1 = []
        self.socialMobility_3to2 = []
        self.socialMobility_3to3 = []
        self.socialMobility_3to4 = []
        self.socialMobility_3to5 = []
        self.socialMobility_4to1 = []
        self.socialMobility_4to2 = []
        self.socialMobility_4to3 = []
        self.socialMobility_4to4 = []
        self.socialMobility_4to5 = []
        self.socialMobility_5to1 = []
        self.socialMobility_5to2 = []
        self.socialMobility_5to3 = []
        self.socialMobility_5to4 = []
        self.socialMobility_5to5 = []
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
        self.shareCareGivers = []
        self.shareCareGivers_1 = []
        self.shareCareGivers_2 = []
        self.shareCareGivers_3 = []
        self.shareCareGivers_4 = []
        self.shareCareGivers_5 = []
        self.shareSocialCareTakers_N1 = []
        self.shareSocialCareTakers_N2 = []
        self.shareSocialCareTakers_N3 = []
        self.shareSocialCareTakers_N4 = []
        self.totalCareDemand = []
        self.perCapitaCareDemand = []
        self.perCapitaSocialCareDemand = []
        self.perCapitaChildCareDemand = []
        self.totalChildCareDemand = []
        self.totalSocialCareDemand = []
        self.shareSocialCareDemand = []
        self.totalCareSupply = []
        self.totalInformalCareSupply = []
        self.totalFormalCareSupply = []
        self.shareInformalCareSupply = []
        self.totalInformalCareReceived = []
        self.totalFormalCareReceived = []
        self.totalCareReceived = []
        self.averageCareReceived = []
        self.averageInformalCareReceived = []
        self.averageFormalCareReceived = []
        self.averageCareSupplied = []
        self.averageInformalCareSupplied = []
        self.averageFormalCareSupplied = []
        self.shareInformalCareReceived = []
        self.totalUnmetCareDemand = []
        self.shareUnmetCareDemand = []
        self.perCapitaUnmetCareDemand = []
        self.averageUnmetCareDemand = []
        self.totalInformalSocialCareReceived = []
        self.totalFormalSocialCareReceived = []
        self.totalSocialCareReceived = [] 
        self.averageSocialCareReceived = []
        self.averageInformalSocialCareReceived = []
        self.averageFormalSocialCareReceived = []
        self.averageSocialCareSupplied = []
        self.averageInformalSocialCareSupplied = []
        self.averageFormalSocialCareSupplied = []
        self.shareInformalSocialCareReceived = []
        self.totalSocialCareUnmetDemand = [] 
        self.shareUnmetSocialCareDemand = []
        self.perCapitaUnmetSocialCareDemand = []
        self.averageUnmetSocialCareDemand = []
        self.totalInformalChildCareReceived = []
        self.totalFormalChildCareReceived = []
        self.totalChildCareReceived = [] 
        self.averageChildCareReceived = []
        self.averageInformalChildCareReceived = []
        self.averageFormalChildCareReceived = []
        self.averageChildCareSupplied = []
        self.averageInformalChildCareSupplied = []
        self.averageFormalChildCareSupplied = []
        self.shareInformalChildCareReceived = []
        self.totalChildCareUnmetDemand = [] 
        self.shareUnmetChildCareDemand = []
        self.perCapitaUnmetChildCareDemand = []
        self.averageUnmetChildCareDemand = []
        self.totalInformalCareSuppliedMale = [] 
        self.totalInformalCareSuppliedMale_1 = [] 
        self.totalInformalCareSuppliedMale_2 = [] 
        self.totalInformalCareSuppliedMale_3 = [] 
        self.totalInformalCareSuppliedMale_4 = []
        self.totalInformalCareSuppliedMale_5 = [] 
        self.totalInformalCareSuppliedFemale = [] 
        self.totalInformalCareSuppliedFemale_1 = [] 
        self.totalInformalCareSuppliedFemale_2 = [] 
        self.totalInformalCareSuppliedFemale_3 = [] 
        self.totalInformalCareSuppliedFemale_4 = [] 
        self.totalInformalCareSuppliedFemale_5 = [] 
        self.shareFemaleInformalCareSupplied = []
        self.shareFemaleInformalCareSupplied_1 = []
        self.shareFemaleInformalCareSupplied_2 = []
        self.shareFemaleInformalCareSupplied_3 = []
        self.shareFemaleInformalCareSupplied_4 = []
        self.shareFemaleInformalCareSupplied_5 = []
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
        self.shareSocialCare_1 = []
        self.totalInformalCarePerRecipient_1 = []
        self.totalFormalCarePerRecipient_1 = []
        self.totalUnmetNeedPerRecipient_1 = []
        self.totalInformalCarePerCarer_1 = []
        self.totalFormalCarePerCarer_1 = []
        self.shareInformalSupply_1 = []
        self.shareUnmetCareDemand_1 = []
        self.perCapitaUnmetCareDemand_1 = []
        self.totalInformalSupply_2 = []
        self.totalFormalSupply_2 = []
        self.shareSocialCare_2 = []
        self.totalInformalCarePerRecipient_2 = []
        self.totalFormalCarePerRecipient_2 = []
        self.totalUnmetNeedPerRecipient_2 = []
        self.totalInformalCarePerCarer_2 = []
        self.totalFormalCarePerCarer_2 = []
        self.shareInformalSupply_2 = []
        self.shareUnmetCareDemand_2 = []
        self.perCapitaUnmetCareDemand_2 = []
        self.totalInformalSupply_3 = []
        self.totalFormalSupply_3 = []
        self.shareSocialCare_3 = []
        self.totalInformalCarePerRecipient_3 = []
        self.totalFormalCarePerRecipient_3 = []
        self.totalUnmetNeedPerRecipient_3 = []
        self.totalInformalCarePerCarer_3 = []
        self.totalFormalCarePerCarer_3 = []
        self.shareInformalSupply_3 = []
        self.shareUnmetCareDemand_3 = []
        self.perCapitaUnmetCareDemand_3 = []
        self.totalInformalSupply_4 = []
        self.totalFormalSupply_4 = []
        self.shareSocialCare_4 = []
        self.totalInformalCarePerRecipient_4 = []
        self.totalFormalCarePerRecipient_4 = []
        self.totalUnmetNeedPerRecipient_4 = []
        self.totalInformalCarePerCarer_4 = []
        self.totalFormalCarePerCarer_4 = []
        self.shareInformalSupply_4 = []
        self.shareUnmetCareDemand_4 = []
        self.perCapitaUnmetCareDemand_4 = []
        self.totalInformalSupply_5 = []
        self.totalFormalSupply_5 = []
        self.shareSocialCare_5 = []
        self.totalInformalCarePerRecipient_5 = []
        self.totalFormalCarePerRecipient_5 = []
        self.totalUnmetNeedPerRecipient_5 = []
        self.totalInformalCarePerCarer_5 = []
        self.totalFormalCarePerCarer_5 = []
        self.shareInformalSupply_5 = []
        self.shareUnmetCareDemand_5 = []
        self.perCapitaUnmetCareDemand_5 = []
        
        self.averageCareSupply = []
        self.ratio_UnmetCareDemand_Supply = []
        
        self.perCapitaCareReceived = []
        self.perCapitaSocialCareReceived = []
        self.perCapitaChildCareReceived = []
        
        self.totalCareSupply_1 = []
        self.averageCareSupply_1 = []
        self.ratio_UnmetCareDemand_Supply_1 = []
        self.totalSocialInformalCareSupply_1 = []
        self.totalSocialFormalCareSupply_1 = []
        self.totalUnmetSocialCareDemand_1 = []
        self.totalChildInformalCareSupply_1 = []
        self.totalChildFormalCareSupply_1 = []
        self.totalUnmetChildCareDemand_1 = []
        self.averageSocialInformalCareSupply_1 = []
        self.averageSocialFormalCareSupply_1 = []
        self.averageUnmetSocialCareDemand_1 = []
        self.averageChildInformalCareSupply_1 = []
        self.averageChildFormalCareSupply_1 = []
        self.averageUnmetChildCareDemand_1 = []
        
        self.totalCareSupply_2 = []
        self.averageCareSupply_2 = []
        self.ratio_UnmetCareDemand_Supply_2 = []
        self.totalSocialInformalCareSupply_2 = []
        self.totalSocialFormalCareSupply_2 = []
        self.totalUnmetSocialCareDemand_2 = []
        self.totalChildInformalCareSupply_2 = []
        self.totalChildFormalCareSupply_2 = []
        self.totalUnmetChildCareDemand_2 = []
        self.averageSocialInformalCareSupply_2 = []
        self.averageSocialFormalCareSupply_2 = []
        self.averageUnmetSocialCareDemand_2 = []
        self.averageChildInformalCareSupply_2 = []
        self.averageChildFormalCareSupply_2 = []
        self.averageUnmetChildCareDemand_2 = []
        
        self.totalCareSupply_3 = []
        self.averageCareSupply_3 = []
        self.ratio_UnmetCareDemand_Supply_3 = []
        self.totalSocialInformalCareSupply_3 = []
        self.totalSocialFormalCareSupply_3 = []
        self.totalUnmetSocialCareDemand_3 = []
        self.totalChildInformalCareSupply_3 = []
        self.totalChildFormalCareSupply_3 = []
        self.totalUnmetChildCareDemand_3 = []
        self.averageSocialInformalCareSupply_3 = []
        self.averageSocialFormalCareSupply_3 = []
        self.averageUnmetSocialCareDemand_3 = []
        self.averageChildInformalCareSupply_3 = []
        self.averageChildFormalCareSupply_3 = []
        self.averageUnmetChildCareDemand_3 = []
        
        self.totalCareSupply_4 = []
        self.averageCareSupply_4 = []
        self.ratio_UnmetCareDemand_Supply_4 = []
        self.totalSocialInformalCareSupply_4 = []
        self.totalSocialFormalCareSupply_4 = []
        self.totalUnmetSocialCareDemand_4 = []
        self.totalChildInformalCareSupply_4 = []
        self.totalChildFormalCareSupply_4 = []
        self.totalUnmetChildCareDemand_4 = []
        self.averageSocialInformalCareSupply_4 = []
        self.averageSocialFormalCareSupply_4 = []
        self.averageUnmetSocialCareDemand_4 = []
        self.averageChildInformalCareSupply_4 = []
        self.averageChildFormalCareSupply_4 = []
        self.averageUnmetChildCareDemand_4 = []
        
        self.totalCareSupply_5 = []
        self.averageCareSupply_5 = []
        self.ratio_UnmetCareDemand_Supply_5 = []
        self.totalSocialInformalCareSupply_5 = []
        self.totalSocialFormalCareSupply_5 = []
        self.totalUnmetSocialCareDemand_5 = []
        self.totalChildInformalCareSupply_5 = []
        self.totalChildFormalCareSupply_5 = []
        self.totalUnmetChildCareDemand_5 = []
        self.averageSocialInformalCareSupply_5 = []
        self.averageSocialFormalCareSupply_5 = []
        self.averageUnmetSocialCareDemand_5 = []
        self.averageChildInformalCareSupply_5 = []
        self.averageChildFormalCareSupply_5 = []
        self.averageUnmetChildCareDemand_5 = []
        
        self.shareInformalSocialSupply_1 = []
        self.shareUnmetSocialSupply_1 = []
        self.shareInformalChildSupply_1 = []
        self.shareUnmetChildSupply_1 = []
        
        self.shareInformalSocialSupply_2 = []
        self.shareUnmetSocialSupply_2 = []
        self.shareInformalChildSupply_2 = []
        self.shareUnmetChildSupply_2 = []
        
        self.shareInformalSocialSupply_3 = []
        self.shareUnmetSocialSupply_3 = []
        self.shareInformalChildSupply_3 = []
        self.shareUnmetChildSupply_3 = []
        
        self.shareInformalSocialSupply_4 = []
        self.shareUnmetSocialSupply_4 = []
        self.shareInformalChildSupply_4 = []
        self.shareUnmetChildSupply_4 = []
        
        self.shareInformalSocialSupply_5 = []
        self.shareUnmetSocialSupply_5 = []
        self.shareInformalChildSupply_5 = []
        self.shareUnmetChildSupply_5 = []
        
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
        self.totalEmployment = []
        self.totalEmployment_1 = []
        self.totalEmployment_2 = []
        self.totalEmployment_3 = []
        self.totalEmployment_4 = []
        self.totalEmployment_5 = []
        self.totalJobChanges = []
        self.popHourlyWages = []
        
        self.averageIncome_M = []
        self.averageIncome_F = []
        self.ratioWomenMaleIncome = []
        self.averageIncome_1 = []
        self.averageIncome_1_Males = []
        self.averageIncome_1_Females = []
        self.ratioWomenMaleIncome_1 = []
        self.averageIncome_2 = []
        self.averageIncome_2_Males = []
        self.averageIncome_2_Females = []
        self.ratioWomenMaleIncome_2 = []
        self.averageIncome_3 = []
        self.averageIncome_3_Males = []
        self.averageIncome_3_Females = []
        self.ratioWomenMaleIncome_3 = []
        self.averageIncome_4 = []
        self.averageIncome_4_Males = []
        self.averageIncome_4_Females = []
        self.ratioWomenMaleIncome_4 = []
        self.averageIncome_5 = []
        self.averageIncome_5_Males = []
        self.averageIncome_5_Females = []
        self.ratioWomenMaleIncome_5 = []
        
        self.averageWage_M = []
        self.averageWage_F = []
        self.ratioWomenMaleWage = []
        self.averageWage_1 = []
        self.averageWage_1_Males = []
        self.averageWage_1_Females = []
        self.ratioWomenMaleWage_1 = []
        self.averageWage_2 = []
        self.averageWage_2_Males = []
        self.averageWage_2_Females = []
        self.ratioWomenMaleWage_2 = []
        self.averageWage_3 = []
        self.averageWage_3_Males = []
        self.averageWage_3_Females = []
        self.ratioWomenMaleWage_3 = []
        self.averageWage_4 = []
        self.averageWage_4_Males = []
        self.averageWage_4_Females = []
        self.ratioWomenMaleWage_4 = []
        self.averageWage_5 = []
        self.averageWage_5_Males = []
        self.averageWage_5_Females = []
        self.ratioWomenMaleWage_5 = []
        
        self.totalRelocations = 0
        self.numberRelocations = []
        self.jobRelocations_1 = 0
        self.jobRelocations_2 = 0
        self.jobRelocations_3 = 0
        self.jobRelocations_4 = 0
        self.jobRelocations_5 = 0
        self.numJobRelocations_1 = []
        self.numJobRelocations_2 = []
        self.numJobRelocations_3 = []
        self.numJobRelocations_4 = []
        self.numJobRelocations_5 = []
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
        # Check variables
        # self.deathProb = []
        # self.careLevel = []
        self.perCapitaHouseholdIncome = []
        self.socialCareMapValues = []
        self.relativeEducationCost = []
        self.probKeepStudying = []
        self.stageStudent = []
        self.changeJobRate = []
        self.changeJobdIncome = []
        self.relocationCareLoss = []
        self.relocationCost = []
        self.townRelocationAttraction = []
        self.townRelativeAttraction = []
        self.townsJobProb = []
        self.townJobAttraction = []
        self.unemployedIncomeDiscountingFactor = []
        self.relativeTownAttraction = []
        self.houseScore = []
        self.deltaHouseOccupants = []
        
        self.unmetSocialCareNeedGiniCoefficient = []
        self.unmetSocialCareNeedGiniCoefficient_1 = []
        self.unmetSocialCareNeedGiniCoefficient_2 = []
        self.unmetSocialCareNeedGiniCoefficient_3 = []
        self.unmetSocialCareNeedGiniCoefficient_4 = []
        self.unmetSocialCareNeedGiniCoefficient_5 = []
        
        self.shareUnmetSocialCareNeedGiniCoefficient = []
        self.shareUnmetSocialCareNeedGiniCoefficient_1 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_2 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_3 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_4 = []
        self.shareUnmetSocialCareNeedGiniCoefficient_5 = []
        
        self.unmetSocialCareNeedDistribution = []
        self.unmetSocialCareNeedDistribution_1 = []
        self.unmetSocialCareNeedDistribution_2 = []
        self.unmetSocialCareNeedDistribution_3 = []
        self.unmetSocialCareNeedDistribution_4 = []
        self.unmetSocialCareNeedDistribution_5 = []
        
        self.shareUnmetSocialCareNeedDistribution = []
        self.shareUnmetSocialCareNeedDistribution_1 = []
        self.shareUnmetSocialCareNeedDistribution_2 = []
        self.shareUnmetSocialCareNeedDistribution_3 = []
        self.shareUnmetSocialCareNeedDistribution_4 = []
        self.shareUnmetSocialCareNeedDistribution_5 = []
        
        self.healthCareCost = []
        self.perCapitaHealthCareCost = []
        self.publicSocialCareSupply = []
        self.aggregateQALY = []
        self.averageQALY = []
        self.discountedQALY = []
        self.averageDiscountedQALY = []
        
        self.inputsMortality = []
        self.outputMortality = []
        self.regressionModels_M = []
        
        self.inputsFertility = []
        self.outputFertility = []
        self.regressionModels_F = []
        
        self.unemploymentRateClasses = []
        self.meanUnemploymentRates = []

        
    def sensitivityGraphs(self, folder):
        
        # Sensitivity Chart 1: Shares of Unmet Care Needs
        lowSharesUnmetCare_M = self.sharesUnmetCare_M[0::2]
        lowSharesUnmetCare_SD = self.sharesUnmetCare_SD[0::2]
        highSharesUnmetCare_M = self.sharesUnmetCare_M[1::2]
        highSharesUnmetCare_SD = self.sharesUnmetCare_SD[1::2]
        
        N = len(lowSharesUnmetCare_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowSharesUnmetCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesUnmetCare_SD, 
                    label = 'Low')
        p2 = ax.bar(index + bar_width, highSharesUnmetCare_M, bar_width,color='g', bottom = 0, yerr = highSharesUnmetCare_SD, 
                    label = 'High')
        ax.set_ylabel('Share of Unmet Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Shares of Unmet Care Need')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/SharesUnmetCareSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 2: Averages of Unmet Care Needs
        lowAveragesUnmetCare_M = self.averagesUnmetCare_M[0::2]
        lowAveragesUnmetCare_SD = self.averagesUnmetCare_SD[0::2]
        highAveragesUnmetCare_M = self.averagesUnmetCare_M[1::2]
        highAveragesUnmetCare_SD = self.averagesUnmetCare_SD[1::2]
        
        N = len(lowAveragesUnmetCare_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowAveragesUnmetCare_M, bar_width, color='b', bottom = 0, yerr = lowAveragesUnmetCare_SD, 
                    label = 'Low')
        p2 = ax.bar(index + bar_width, highAveragesUnmetCare_M, bar_width,color='g', bottom = 0, yerr = highAveragesUnmetCare_SD, 
                    label = 'High')
        ax.set_ylabel('Hours of Unmet Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Unmet Care per Receiver')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/AveragesUnmetCareSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 3: Quality-Adjusted-Life-Years
       
        lowQALY_M = self.qualityAdjustedLifeYears_M[0::2]
        lowQALY_SD = self.qualityAdjustedLifeYears_SD[0::2]
        highQALY_M = self.qualityAdjustedLifeYears_M[1::2]
        highQALY_SD = self.qualityAdjustedLifeYears_SD[1::2]
        
        N = len(lowQALY_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowQALY_M, bar_width, color='b', bottom = 0, yerr = lowQALY_SD, label = 'Low')
        p2 = ax.bar(index + bar_width, highQALY_M, bar_width,color='g', bottom = 0, yerr = highQALY_SD, label = 'High')
        ax.set_ylabel('Quality-Adjusted Life Years')
        ax.set_xlabel('Parameters')
        ax.set_title('Total Quality-Adjusted Life Years')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/TotalQualityAdjustedLifeYearsSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 4: Per Capita Quality-Adjusted-Life-Years
        
        lowAverageQALY_M = self.perCapitaQualityAdjustedLifeYears_M[0::2]
        lowAverageQALY_SD = self.perCapitaQualityAdjustedLifeYears_SD[0::2]
        highAverageQALY_M = self.perCapitaQualityAdjustedLifeYears_M[1::2]
        highAverageQALY_SD = self.perCapitaQualityAdjustedLifeYears_SD[1::2]
        
        N = len(lowAverageQALY_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowAverageQALY_M, bar_width, color='b', bottom = 0, yerr = lowAverageQALY_SD, label = 'Low')
        p2 = ax.bar(index + bar_width, highAverageQALY_M, bar_width,color='g', bottom = 0, yerr = highAverageQALY_SD, label = 'High')
        ax.set_ylabel('Quality-Adjusted Life Years')
        ax.set_xlabel('Parameters')
        ax.set_title('Per Capita Quality-Adjusted Life Years')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/perCapitaQualityAdjustedLifeYearsSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 5: Per Capita Hospitalization Costs

        lowAverageHC_M = self.perCapitaHospitalizationCost_M[0::2]
        lowAverageHC_SD = self.perCapitaHospitalizationCost_SD[0::2]
        highAverageHC_M = self.perCapitaHospitalizationCost_M[1::2]
        highAverageUC_SD = self.perCapitaHospitalizationCost_SD[1::2]
        
        N = len(lowAverageHC_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowAverageHC_M, bar_width, color='b', bottom = 0, yerr = lowAverageHC_SD, label = 'Low')
        p2 = ax.bar(index + bar_width, highAverageHC_M, bar_width,color='g', bottom = 0, yerr = highAverageUC_SD, label = 'High')
        ax.set_ylabel('Per Capita Costs')
        ax.set_xlabel('Parameters')
        ax.set_title('Per Capita Hospitalization Costs')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/perCapitaHospitalizationCostsSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 6: Shares of Social Care
        lowSharesSocialCare_M = self.sharesSocialCare_M[0::2]
        lowSharesSocialCare_SD = self.sharesSocialCare_SD[0::2]
        highSharesSocialCare_M = self.sharesSocialCare_M[1::2]
        highSharesSocialCare_SD = self.sharesSocialCare_SD[1::2]
        
        N = len(lowSharesSocialCare_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowSharesSocialCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesSocialCare_SD, 
                    label = 'Low')
        p2 = ax.bar(index + bar_width, highSharesSocialCare_M, bar_width,color='g', bottom = 0, yerr = highSharesSocialCare_SD, 
                    label = 'High')
        ax.set_ylabel('Share of Social Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Shares of Social Care Received')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/SharesSocialCareSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Sensitivity Chart 7: Shares of Informal Care
        lowSharesInformalCare_M = self.sharesInformalCare_M[0::2]
        lowSharesInformalCare_SD = self.sharesInformalCare_SD[0::2]
        highSharesInformalCare_M = self.sharesInformalCare_M[1::2]
        highSharesInformalCare_SD = self.sharesInformalCare_SD[1::2]
        
        N = len(lowSharesSocialCare_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, lowSharesInformalCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesInformalCare_SD, 
                    label = 'Low')
        p2 = ax.bar(index + bar_width, highSharesInformalCare_M, bar_width,color='g', bottom = 0, yerr = highSharesInformalCare_SD, 
                    label = 'High')
        ax.set_ylabel('Share of Informal Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Shares of Informal Care Received')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/SharesInformalCareSensitivityGroupedBarChart.pdf'
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