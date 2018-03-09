
from simulation import Sim
import os
import cProfile
import pylab
import math
import matplotlib.pyplot as plt


def init_params():
    """Set up the simulation parameters."""
    p = {}
    
    p['favouriteSeed'] = 123
    p['loadFromFile'] = False
    p['verboseDebugging'] = False
    p['singleRunGraphs'] = True
    p['numRepeats'] = 1
    
    # The basics: starting population and year, etc.
    p['initialPop'] = 500
    p['startYear'] = 1860
    p['endYear'] = 2030
    p['thePresent'] = 2012
    p['statsCollectFrom'] = 1960
    p['minStartAge'] = 24
    p['maxStartAge'] = 45
    p['numberClasses'] = 5
    p['socialClasses'] = ['unskilled', 'skilled', 'lower', 'middle', 'upper']
    p['initialClassShares'] = [0.2, 0.25, 0.35, 0.15, 0.05]
    p['initialUnemployment'] = [0.25, 0.2, 0.15, 0.1, 0.1]
    p['unemploymentAgeBandParam'] = 0.3
    
    # doDeath function parameters
    p['mortalityBias'] = 0.85 # After 1950
    p['careNeedBias'] = 0.8
    p['baseDieProb'] = 0.0001
    p['babyDieProb'] = 0.005
    p['maleAgeScaling'] = 14.0
    p['maleAgeDieProb'] = 0.00021
    p['femaleAgeScaling'] = 15.5
    p['femaleAgeDieProb'] = 0.00019
    
    # doBirths function parameters
    p['minPregnancyAge'] = 17
    p['maxPregnancyAge'] = 42
    p['growingPopBirthProb'] = 0.215
    p['fertilityCorrector'] = 1.0
    p['fertilityBias'] = 0.9
    
    # careTransitions function parameters
    p['zeroYearCare'] = 80.0
    p['childcareDecreaseRate'] = 0.18
    p['personCareProb'] = 0.0008
    p['maleAgeCareScaling'] = 18.0 # p['maleAgeCareProb'] = 0.0008
    p['femaleAgeCareScaling'] = 19.0 # p['femaleAgeCareProb'] = 0.0008
    p['baseCareProb'] = 0.0002
    p['careBias'] = 0.9
    p['careTransitionRate'] = 0.7
    
    ########   Key parameter 1  ##############
    p['unmetNeedExponent'] = 0.01 #[0.005 - 0.02]
    
    p['numCareLevels'] = 5
    p['careLevelNames'] = ['none','low','moderate','substantial','critical']
    p['careDemandInHours'] = [ 0.0, 8.0, 16.0, 32.0, 80.0 ]
    p['quantumCare'] = 4.0
    
    # careSupplies getCare and probSuppliers function parameters
    ########   Key parameter 2  ##############
    p['incomeCareParam'] = 0.001 #[0.0005 - 0.002]
    
    p['weeklyHours'] = 40.0
    p['pricePublicSocialCare'] = 20.0
    p['priceSocialCare'] = 17.0
    p['retiredHours'] = 60.0
    p['studentHours'] = 12.0
    p['unemployedHours'] = 24.0
    p['socialNetworkDistances'] = [0.0, 1.0, 2.0, 1.0, 2.0, 2.0, 3.0, 3.0]
    p['networkDistanceParam'] = 1.0
    p['employedHours'] = 12.0
    p['socialCareWeightBias'] = 1.0
    
    ########   Key parameter 3  ##############
    p['excessNeedParam'] = 0.01 #1.0 #[0.25 - 1.0]
    
    p['careSupplyBias'] = 0.5
    p['careIncomeParam'] = 0.001
    
    # ageTransitions, enterWorkForce and marketWage functions parameters
    p['minWorkingAge'] = 16
    p['ageOfRetirement'] = 65
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0]
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0]
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0]
    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    p['educationCosts'] = [0.0, 0.0, 0.0, 0.0]
    p['eduWageSensitivity'] = 0.5
    p['eduRankSensitivity'] = 1.0
    p['costantIncomeParam'] = 1.0
    p['costantEduParam'] = 1.0
    p['incEduExp'] = 0.25
    p['educationLevels'] = ['GCSE', 'A-Level', 'HND', 'Degree', 'Higher Degree']
    p['workingAge'] = [16, 18, 20, 22, 24]
    
    # doDivorce function parameters
    p['basicDivorceRate'] = 0.06
    p['variableDivorce'] = 0.06
    p['divorceModifierByDecade'] = [ 0.0, 1.0, 0.9, 0.5, 0.4, 0.2, 0.1, 0.03, 0.01, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0, 0.0 ]
    p['divorceBias'] = 0.9
    
    # doMarriages function parameters
    p['deltageProb'] =  [0.0, 0.1, 0.25, 0.4, 0.2, 0.05]
    
    ########   Key parameter 4  ##############
    p['betaGeoExp'] = 2.0 #[1.0 - 4.0]
    
    p['betaSocExp'] = 4.0
    p['rankGenderBias'] = 0.5
    p['basicMaleMarriageProb'] =  0.7
    p['maleMarriageModifierByDecade'] = [ 0.0, 0.16, 0.5, 1.0, 0.8, 0.7, 0.66, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.0, 0.0, 0.0 ]
    
    # jobMarket, updateWork and unemploymentRate functions parameters
    p['unemploymentClassBias'] = 0.75
    p['unemploymentAgeBias'] = [1.0, 0.55, 0.35, 0.25, 0.2, 0.2]
    p['numberAgeBands'] = 6
    p['jobMobilitySlope'] = 0.004
    p['jobMobilityIntercept'] = 0.05
    p['ageBiasParam'] = [7.0, 3.0, 1.0, 0.5, 0.35, 0.15]
    p['deltaIncomeExp'] = 0.1
    p['relocationCareLossExp'] = 0.01
    p['firingParam'] = 0.2
    p['wageVar'] = 0.04
    p['workDiscountingTime'] = 0.8
    p['sizeWeightParam'] = 0.7
    p['minClassWeightParam'] = 1.0
    p['incomeDiscountingExponent'] = 4.0
    #p['incomeDiscountingParam'] = 2.0
    
    # relocationPensioners function parameters
    p['agingParentsMoveInWithKids'] = 0.1
    p['variableMoveBack'] = 0.1
    
    # houseMap function parameters
    p['geoDistanceSensitivityParam'] = 2.0
    p['socDistanceSensitivityParam'] = 2.0
    p['classAffinityWeight'] = 4.0
    p['distanceSensitivityParam'] = 1.0
    
    # relocationProb function parameters
    p['baseRelocatingProb'] = 0.05
    p['relocationParameter'] = 2.0 
    #p['expReloc'] = 1.0
    
    # computeRelocationCost and relocation Propensity functions parameters
    p['yearsInTownSensitivityParam'] = 0.5
    
     ########   Key parameter 5  ##############
    p['relocationCostParam'] = 2.0
    
    ########   Key parameter 6  ##############
    p['propensityRelocationParam'] = 5.0 #0.002 # [0.001 - 0.004]
    p['denRelocationWeight'] = 0.1
    
    
     ## Description of the map, towns, and houses
    p['mapGridXDimension'] = 8
    p['mapGridYDimension'] = 12    
    p['townGridDimension'] = 35
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

p = init_params()
s = Sim(p)
tax = s.run()