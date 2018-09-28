 
#from simulation import Sim
from simulation import Sim
import cProfile
import pylab
import math
import matplotlib.pyplot as plt
import random
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import time
import os
import pandas as pd



def init_params():
    """Set up the simulation parameters."""
    p = {}
    
    # p['rootFolder'] = 'C:/Users/Umberto Gostoli/SPHSU/Social Care Model II'
    p['rootFolder'] = 'N:/Social Care Model Paper I'
    
    p['noPolicySim'] = False
    p['numRepeats'] = 1
    
    p['multiprocessing'] = True
    p['numberProcessors'] = 9
    
    p['startYear'] = 1860
    p['endYear'] = 2040
    p['thePresent'] = 2012
    p['statsCollectFrom'] = 1990
    p['regressionCollectFrom'] = 1960 
    p['implementPoliciesFromYear'] = 2020
    
    p['favouriteSeed'] = 123
    p['loadFromFile'] = False
    p['verboseDebugging'] = False
    p['singleRunGraphs'] = False
    p['saveChecks'] = True
    p['getCheckVariablesAtYear'] = 2015
    # To change through command-line arguments

    p['numberPolicyParameters'] = 2
    p['valuesPerParam'] = 1
    p['numberScenarios'] = 3
    
    ############  Policy Parameters    #######################
    p['incomeCareParam'] = 0.0005 #[0.00025 - 0.001]
    p['taxBreakRate'] = 0.0
    p['ageOfRetirement'] = 65
    p['socialSupportLevel'] = 5
    # p['educationCosts']
    #############################################################
    p['socialCareCreditShare'] = 0.0
    p['maxWtWChildAge'] = 5
     # The basics: starting population and year, etc.
    
    p['discountingFactor'] = 0.03
    
    
    p['initialPop'] = 600   
    
    p['minStartAge'] = 24
    p['maxStartAge'] = 45
    p['numberClasses'] = 5
    p['socialClasses'] = ['unskilled', 'skilled', 'lower', 'middle', 'upper']
    p['initialClassShares'] = [0.2, 0.25, 0.3, 0.2, 0.05]
    p['initialUnemployment'] = [0.25, 0.2, 0.15, 0.1, 0.1]
    p['unemploymentAgeBandParam'] = 0.3
    
    # doDeath function parameters
    p['mortalityBias'] = 0.85 # After 1950
    p['careNeedBias'] = 0.9
    p['unmetCareNeedBias'] = 0.5
    p['baseDieProb'] = 0.0001
    p['babyDieProb'] = 0.005
    p['maleAgeScaling'] = 14.0
    p['maleAgeDieProb'] = 0.00021
    p['femaleAgeScaling'] = 15.5
    p['femaleAgeDieProb'] = 0.00019
    
    p['orphansRelocationParam'] = 0.5
    
    # doBirths function parameters
    p['minPregnancyAge'] = 17
    p['maxPregnancyAge'] = 42
    p['growingPopBirthProb'] = 0.215
    p['fertilityCorrector'] = 1.0
    p['fertilityBias'] = 0.9
    
    # careTransitions function parameters
    p['zeroYearCare'] = 80.0
    p['childcareDecreaseRate'] = 0.25
    p['personCareProb'] = 0.0008
    p['maleAgeCareScaling'] = 18.0 # p['maleAgeCareProb'] = 0.0008
    p['femaleAgeCareScaling'] = 19.0 # p['femaleAgeCareProb'] = 0.0008
    p['baseCareProb'] = 0.0002
    p['careBias'] = 0.9
    p['careTransitionRate'] = 0.7

    p['unmetNeedExponent'] = 1.0 # 0.005 #[0.005 - 0.02]
    
    p['numCareLevels'] = 5
    p['careLevelNames'] = ['none','low','moderate','substantial','critical']
    p['careDemandInHours'] = [ 0.0, 8.0, 16.0, 32.0, 80.0 ]
    p['quantumCare'] = 4.0
    
    # careSupplies getCare and probSuppliers function parameters
    
    ########   Key parameter 1  ##############
    
    
    p['weeklyHours'] = 40.0
    
    
    p['priceChildCare'] = 0.76 # 6 
    p['schoolAge'] = 5
    p['maxFormalChildcareHours'] = 48
    p['schoolHours'] = 30
    p['freeChildcareHours'] = 15
    p['workingParentsFreeChildcareHours'] = 30
    p['minAgeStartChildCareSupport'] = 3
    p['minAgeStartChildCareSupportByIncome'] =  2
    p['maxHouseholdIncomeChildCareSupport'] = 40 # 320
    
    ########   Key parameter 2  ##############
     # 5: No public supply 
    
    p['retiredHours'] = 60.0
    p['studentHours'] = 16.0
    p['teenAgersHours'] = 8.0
    p['unemployedHours'] = 30.0
    p['socialNetworkDistances'] = [0.0, 1.0, 2.0, 1.0, 2.0, 2.0, 3.0, 3.0]
    p['networkDistanceParam'] = 2.0
    p['employedHours'] = 16.0
    p['socialCareWeightBias'] = 1.0
    p['unmetCareNeedDiscountParam'] = 0.5
    p['shareUnmetNeedDiscountParam'] = 0.5
    # p['pastShareUnmetNeedWeight'] = 0.5
    
    p['networkSizeParam'] = 5.0 # 0.01 #[0.005 - 0.02]
    
    p['careSupplyBias'] = 0.5
    p['careIncomeParam'] = 0.001
    
    # Hospitalization Costs
    p['qalyBeta'] = 0.18
    p['qalyAlpha'] = 1.5
    p['qalyDiscountRate'] = 0.035
    p['qalyIndexes'] = [1.0, 0.8, 0.6, 0.4, 0.2]
    p['unmetCareHealthParam'] = 0.1
    p['hospitalizationParam'] = 0.5
    p['needLevelParam'] = 2.0
    p['unmetSocialCareParam'] = 2.0
    p['costHospitalizationPerDay'] = 400
    
    # ageTransitions, enterWorkForce and marketWage functions parameters
    p['ageTeenagers'] = 12
    p['minWorkingAge'] = 16
    
    ########   Key parameter 3  ##############
    
    p['careBankingSchemeOn'] = False
    p['socialCareBankingAge'] = 65
    
    p['absoluteCreditQuantity'] = False
    p['quantityYearlyIncrease'] = 0.0
    p['socialCareCreditQuantity'] = 0
    p['kinshipNetworkCarePropension'] = 0.5
    p['volunteersCarePropensionCoefficient'] = 0.01
    p['pensionContributionRate'] = 0.05
    
    p['hillHealthLevelThreshold'] = 3
    p['seriouslyHillSupportRate'] = 0.5
    
    ###   Prices   ####
    p['pricePublicSocialCare'] = 20.0 # [2.55] # 20
    p['priceSocialCare'] = 17.0 # [2.29] # 18
    p['taxBrackets'] = [663, 228, 0] # [28.16, 110.23] # [221, 865]
    p['taxBandsNumber'] = 3
    p['bandsTaxationRates'] = [0.4, 0.2, 0.0] # [0.0, 0.2, 0.4]
    # Tax Break Policy

    
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0] # [0.64, 0.89, 1.27, 1.66, 2.29] #  
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0] #[0.64, 0.89, 1.15, 1.40, 1.78] #  
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0] #[1.27, 1.91, 2.80, 4.21, 6.37] #  
    p['educationCosts'] = [0.0, 100.0, 150.0, 200.0] #[0.0, 12.74, 19.12, 25.49] # 
    
    # Priced growth  #####
    p['wageGrowthRate'] = 1.0 # 1.01338 # 

    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    
    # SES inter-generational mobility parameters
    p['eduWageSensitivity'] = 0.2 # 0.5
    p['eduRankSensitivity'] = 3.0 # 5.0
    p['costantIncomeParam'] = 80.0 # 20.0
    p['costantEduParam'] = 10.0 #  10.0
    p['careEducationParam'] = 0.005        # 0.04
    
    # p['incEduExp'] = 0.25
    p['educationLevels'] = ['GCSE', 'A-Level', 'HND', 'Degree', 'Higher Degree']
    p['workingAge'] = [16, 18, 20, 22, 24]
    
    # doDivorce function parameters
    p['basicDivorceRate'] = 0.06
    p['variableDivorce'] = 0.06
    p['divorceModifierByDecade'] = [ 0.0, 1.0, 0.9, 0.5, 0.4, 0.2, 0.1, 0.03, 0.01, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['divorceBias'] = 1.0
    
    # doMarriages function parameters
    p['deltageProb'] =  [0.0, 0.1, 0.25, 0.4, 0.2, 0.05]
    p['incomeMarriageParam'] = 0.025
    p['studentFactorParam'] = 0.5
    ########   Key parameter 4  ##############
    p['betaGeoExp'] = 3.0 #[1.0 - 4.0]
    
    p['betaSocExp'] = 2.0
    p['rankGenderBias'] = 0.5
    p['basicMaleMarriageProb'] =  0.9
    p['maleMarriageModifierByDecade'] = [ 0.0, 0.16, 0.5, 1.0, 0.8, 0.7, 0.66, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.0, 0.0, 0.0, 0.0 ]
    
    # jobMarket, updateWork and unemploymentRate functions parameters
    p['unemploymentClassBias'] = 0.75
    p['unemploymentAgeBias'] = [1.0, 0.55, 0.35, 0.25, 0.2, 0.2]
    p['numberAgeBands'] = 6
    p['jobMobilitySlope'] = 0.004
    p['jobMobilityIntercept'] = 0.05
    p['ageBiasParam'] = [7.0, 3.0, 1.0, 0.5, 0.35, 0.15]
    p['deltaIncomeExp'] = 0.05
    p['unemployedCareBurdernParam'] = 0.025
    # Potential key parameter
    p['relocationCareLossExp'] = 1.0 # 40.0 # 
    p['incomeSocialCostRelativeWeight'] = 0.5
    
    p['firingParam'] = 0.2
    p['wageVar'] = 0.06
    p['workDiscountingTime'] = 0.8
    p['sizeWeightParam'] = 0.7
    p['minClassWeightParam'] = 1.0
    p['incomeDiscountingExponent'] = 4.0
    p['discountingMultiplier'] = 2.0
    #p['incomeDiscountingParam'] = 2.0
    
    # relocationPensioners function parameters
    p['agingParentsMoveInWithKids'] = 0.1
    p['variableMoveBack'] = 0.1
    p['retiredRelocationParam'] = 0.004 # 0.01
    
    # houseMap function parameters
    p['geoDistanceSensitivityParam'] = 2.0
    p['socDistanceSensitivityParam'] = 2.0
    p['classAffinityWeight'] = 4.0
    p['distanceSensitivityParam'] = 0.5
    
    # relocationProb function parameters
    p['baseRelocatingProb'] = 0.05
    p['relocationParameter'] = 1.0 
    p['apprenticesRelocationProb'] = 0.5
    #p['expReloc'] = 1.0
    
    # computeRelocationCost and relocation Propensity functions parameters
    p['yearsInTownSensitivityParam'] = 0.5
    
     ########   Key parameter 5  ##############
    p['relocationCostParam'] = 2.0 # [1 -4]
    
    ########   Key parameter 6  ##############
    p['propensityRelocationParam'] = 1.0 # 5.0 
    p['denRelocationWeight'] = 0.5
    
    
     ## Description of the map, towns, and houses
    p['mapGridXDimension'] = 8
    p['mapGridYDimension'] = 12    
    p['townGridDimension'] = 70
    p['cdfHouseClasses'] = [ 0.6, 0.9, 5.0 ]
    p['ukMap'] = [[ 0.0, 0.1, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.1, 0.1, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0 ],
                  [ 0.0, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.0, 0.2, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.4, 0.0, 0.2, 0.2, 0.4, 0.0, 0.0, 0.0 ],
                  [ 0.6, 0.0, 0.0, 0.3, 0.8, 0.2, 0.0, 0.0 ],
                  [ 0.0, 0.0, 0.0, 0.6, 0.8, 0.4, 0.0, 0.0 ],
                  [ 0.0, 0.0, 0.2, 1.0, 0.8, 0.6, 0.1, 0.0 ],
                  [ 0.0, 0.0, 0.1, 0.2, 1.0, 0.6, 0.3, 0.4 ],
                  [ 0.0, 0.0, 0.5, 0.7, 0.5, 1.0, 1.0, 0.0 ],
                  [ 0.0, 0.0, 0.2, 0.4, 0.6, 1.0, 1.0, 0.0 ],
                  [ 0.0, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0 ]]
    p['ukClassBias'] = [[ 0.0, -0.05, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, -0.05, -0.05, 0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0 ],
                        [ 0.0, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, -0.05, 0.0, -0.05, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, -0.05, 0.0, 0.2, 0.15, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.15, 0.0 ],
                        [ 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0 ] ]
    p['mapDensityModifier'] = 0.6
    # p['numHouseClasses'] = 3
    # p['houseClasses'] = ['small','medium','large']
    
    ## Graphical interface details
    p['interactiveGraphics'] = False #True
    p['delayTime'] = 0.0
    p['screenWidth'] = 1300
    p['screenHeight'] = 700
    p['bgColour'] = 'black'
    p['mainFont'] = 'Helvetica 18'
    p['fontColour'] = 'white'
    p['dateX'] = 70
    p['dateY'] = 20
    p['popX'] = 70
    p['popY'] = 50
    p['pixelsInPopPyramid'] = 2000
    p['num5YearAgeClasses'] = 28
    p['careLevelColour'] = ['blue','green','yellow','orange','red']
    p['houseSizeColour'] = ['brown','purple','yellow']
    p['pixelsPerTown'] = 56
    p['maxTextUpdateList'] = 22
    
    # p['eduEduSensitivity'] = 0.5
    # p['mortalityBias'] = [1.0, 0.92, 0.84, 0.76, 0.68]
    # p['fertilityBias'] = [1.0, 0.92, 0.84, 0.76, 0.68]
    # p['divorceBias'] = [2.0, 1.5, 1.0, 0.75, 0.5]

    ## Transitions to care statistics
    
    ## Availability of care statistics
    
    #p['childHours'] = 5.0
    # p['employedHours'] = 12.0
    #p['homeAdultHours'] = 30.0
    #p['workingAdultHours'] = 25.0
    #p['maxEmployedHours'] = 60.0
    
    #p['lowCareHandicap'] = 0.5
    #p['hourlyCostOfCare'] = 20.0
    
    ## Fertility statistics
    
   # p['steadyPopBirthProb'] = 0.13
   # p['transitionYear'] = 1965
    
    ## Class and employment statistics
    # p['numClasses'] = 5
    # p['occupationClasses'] = ['lower','intermediate','higher']
    # p['cdfOccupationClasses'] = [ 0.6, 0.9, 1.0 ]

    ## Age transition statistics
    # p['ageOfAdulthood'] = 17
    
    ## Marriage function parameters
    
    # p['basicFemaleMarriageProb'] = 0.25
    # p['femaleMarriageModifierByDecade'] = [ 0.0, 0.5, 1.0, 1.0, 1.0, 0.6, 0.5, 0.4, 0.1, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    # p['femaleMarriageProb'] =  [0.01, 0.15, 0.3, 0.2, 0.1, 0.1, 0.06, 0.05, 0.02, 0.01, 0.01, 0.005]
    # p['maleMarriageProb'] =  [0.005, 0.08, 0.25, 0.25, 0.15, 0.1, 0.07, 0.05, 0.03, 0.02, 0.01, 0.005]
    
    ## Leaving home and moving around statistics
    # p['probApartWillMoveTogether'] = 0.3
    # p['coupleMovesToExistingHousehold'] = 0.3
    # p['basicProbAdultMoveOut'] = 0.22
    # p['probAdultMoveOutModifierByDecade'] = [ 0.0, 0.2, 1.0, 0.6, 0.3, 0.15, 0.03, 0.03, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    # p['basicProbSingleMove'] = 0.05
    # p['probSingleMoveModifierByDecade'] = [ 0.0, 1.0, 1.0, 0.8, 0.4, 0.06, 0.04, 0.02, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    # p['basicProbFamilyMove'] = 0.03
    # p['probFamilyMoveModifierByDecade'] = [ 0.0, 0.5, 0.8, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ]

    
    return p

def simulation(params):
    p = init_params()
    bs = Sim(p)
    bs.run(params)


if __name__ == "__main__":
    
    # multiprocessing.set_start_method('forkserver')
    p = init_params()
    
    if p['multiprocessing'] == True:

        random.seed(p['favouriteSeed'])
        np.random.seed(p['favouriteSeed'])
        
        processors = p['numberProcessors']
        if processors > multiprocessing.cpu_count():
            processors = multiprocessing.cpu_count()
        
        pool = multiprocessing.Pool(processors)
        
        if p['noPolicySim'] == True:  
            runNumber = range(p['numRepeats'])
            pool.map(simulation, runNumber)
            pool.close()
            pool.join()
           
        else:
#            params = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
#            parameters = np.array(zip(*[iter(params)]*1))
#            policies = []
#            defaultValues = [p['taxBreakRate'], p['socialSupportLevel']]
#            # Policies' combinations
#            policies.append(defaultValues)
#            for i in range(len(parameters)):
#                for j in range(p['valuesPerParam']):
#                    runParameters = [x for x in defaultValues]
#                    runParameters[i] = parameters[i][j]
#                    policies.append(runParameters)     
#            for p in policies:
#                p.append(policies.index(p))
            
            parameters = np.genfromtxt('structuralParameters.csv', skip_header = 1, delimiter=',')
            parameters = map(list, zip(*parameters))
            scenarios = []
            for i in range(len(parameters[0])):
                combinations = []
                for j in range(len(parameters)):
                    combinations.append(parameters[j][i])
                scenarios.append(combinations)
                
            params = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
            parameters = np.array(zip(*[iter(params)]*1))
            policies = []
            defaultValues = [p['taxBreakRate'], p['socialSupportLevel']]
            policies.append(defaultValues)
            for i in range(len(parameters)):
                for j in range(1):
                    runParameters = [x for x in defaultValues]
                    runParameters[i] = parameters[i][j]
                    policies.append(runParameters)
            combinations = []
            for z in scenarios:
                for p in policies: 
                    combinations.append(z+p)
                    
            for p in combinations:
                p.append(combinations.index(p))
            
            numPolicies = range(len(policies))
            pool.map(simulation, policies)
            pool.close()
            pool.join()
            
    else:
        p = init_params()
        random.seed(p['favouriteSeed'])
        np.random.seed(p['favouriteSeed'])
        
        if p['noPolicySim'] == True:  
            for i in range(p['numRepeats']):
                b = Sim(p)
                b.run(i)

        else:
#            params = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
#            parameters = np.array(zip(*[iter(params)]*1))
#            policies = []
#            defaultValues = [p['taxBreakRate'], p['socialSupportLevel']]
#            # Policies' combinations
#            policies.append(defaultValues)
#            for i in range(len(parameters)):
#                for j in range(p['valuesPerParam']):
#                    runParameters = [x for x in defaultValues]
#                    runParameters[i] = parameters[i][j]
#                    policies.append(runParameters)     
#            for n in policies:
#                n.append(policies.index(n))
            
            parameters = np.genfromtxt('structuralParameters.csv', skip_header = 1, delimiter=',')
            parameters = map(list, zip(*parameters))
            scenarios = []
            for i in range(len(parameters[0])):
                combinations = []
                for j in range(len(parameters)):
                    combinations.append(parameters[j][i])
                scenarios.append(combinations)
                
            params = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
            parameters = np.array(zip(*[iter(params)]*1))
            policies = []
            defaultValues = [p['taxBreakRate'], p['socialSupportLevel']]
            policies.append(defaultValues)
            for i in range(len(parameters)):
                for j in range(1):
                    runParameters = [x for x in defaultValues]
                    runParameters[i] = parameters[i][j]
                    policies.append(runParameters)
            combinations = []
            for z in scenarios:
                for p in policies: 
                    combinations.append(z+p)
                    
            for d in combinations:
                d.append(combinations.index(d))
            
            numPolicies = len(policies)
            
            for n in range(numPolicies):
                b = Sim(p)
                b.run(policies[n])
                
            
    
    
    














