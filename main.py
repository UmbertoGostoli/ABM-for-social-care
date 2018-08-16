 
#from simulation import Sim
from batchSim import Simulation
import os
import cProfile
import pylab
import math
import matplotlib.pyplot as plt
import pickle
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
    
    p['favouriteSeed'] = 123
    p['loadFromFile'] = False
    p['verboseDebugging'] = False
    p['singleRunGraphs'] = True
     
    p['multiprocessing'] = False
    p['numberProcessors'] = 2
    p['noPolicySim'] = False
    p['numRepeats'] = 1
    
    p['numberPolicyParameters'] = 4
    
    # The basics: starting population and year, etc.
    p['policyOnlySim'] = False
    
    
    
    p['initialPop'] = 600
    p['startYear'] = 1860
    p['endYear'] = 2040
    p['thePresent'] = 2012
    p['statsCollectFrom'] = 1990
    p['regressionCollectFrom'] = 1960 
    p['implementPoliciesFromYear'] = 2020   
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
    p['incomeCareParam'] = 0.0005 #[0.00025 - 0.001]
    p['incomeCareParamPolicyCoeffcient'] = 1.0
    
    
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
    p['socialSupportLevel'] = 5 # 5: No public supply 
    p['socialSupportLevelPolicyChange'] = 0
    
    p['retiredHours'] = 60.0
    p['studentHours'] = 16.0
    p['teenAgersHours'] = 8.0
    p['unemployedHours'] = 30.0
    p['socialNetworkDistances'] = [0.0, 1.0, 2.0, 1.0, 2.0, 2.0, 3.0, 3.0]
    p['networkDistanceParam'] = 1.0
    p['employedHours'] = 16.0
    p['socialCareWeightBias'] = 1.0
    p['unmetCareNeedDiscountParam'] = 0.5
    p['shareUnmetNeedDiscountParam'] = 0.5
    # p['pastShareUnmetNeedWeight'] = 0.5
    
    p['excessNeedParam'] = 0.01 #1.0 #[0.005 - 0.02]
    
    p['careSupplyBias'] = 0.5
    p['careIncomeParam'] = 0.001
    
    # Hospitalization Costs
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
    p['ageOfRetirement'] = 65
    p['hillHealthLevelThreshold'] = 3
    p['seriouslyHillSupportRate'] = 0.5
    p['ageOfRetirementPolicyChange'] = 0
    
    ###   Prices   ####
    p['pricePublicSocialCare'] = 20.0 # [2.55] # 20
    p['priceSocialCare'] = 17.0 # [2.29] # 18
    p['taxBrackets'] = [663, 228, 0] # [28.16, 110.23] # [221, 865]
    p['taxBandsNumber'] = 3
    p['bandsTaxationRates'] = [0.4, 0.2, 0.0] # [0.0, 0.2, 0.4]
    # Tax Break Policy
    p['taxBreakRate'] = 0.0
    p['tbrPolicyChange'] = 0.0 # 1.0
    
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0] # [0.64, 0.89, 1.27, 1.66, 2.29] #  
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0] #[0.64, 0.89, 1.15, 1.40, 1.78] #  
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0] #[1.27, 1.91, 2.80, 4.21, 6.37] #  
    p['educationCosts'] = [0.0, 100.0, 150.0, 200.0] #[0.0, 12.74, 19.12, 25.49] # 
    
    # Priced growth  #####
    p['wageGrowthRate'] = 1.0 # 1.01338 # 

    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    
    ########   Key parameter 4  ##############
    
    p['educationCostsPolicyCoefficient'] = 1.0
    
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
    p['betaGeoExp'] = 2.0 #[1.0 - 4.0]
    
    p['betaSocExp'] = 2.0
    p['rankGenderBias'] = 0.5
    p['basicMaleMarriageProb'] =  0.85
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
    p['relocationCareLossExp'] = 40.0 # 0.05
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
    p['retiredRelocationParam'] = 0.01
    
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
    p['propensityRelocationParam'] = 5.0 #0.002 # [10 - 40]
    p['denRelocationWeight'] = 0.5
    
    
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
  
def multipleRunsGraphs(folder, repeats):
    
    outputs = []
    for r in range(repeats):
        repFolder = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\NoPolicy_Sim\Repeat_' + str(r)
        filename = repFolder + '/Outputs.csv'
        output = pd.read_csv(filename, sep=',',header=0)
        outputs.append(output)
        
    p = init_params()
    
#    times = []
#    shareUnmetCareDemand = []
#    averageUnmetCareDemand = []
#    totalQALY = []
#    averageQALY = []
#    discountedQALY = []
#    averageDiscountedQALY = []
#    perCapitaHealthCareCost = []
    
#    for output in outputs:
#        shareUnmetCareDemand.append(output[0])
#        averageUnmetCareDemand.append(output[1])
#        totalQALY.append(output[2])
#        averageQALY.append(output[3])
#        discountedQALY.append(output[4])
#        averageDiscountedQALY.append(output[5])
#        perCapitaHealthCareCost.append(output[6])
#        times.append(output[7])
        
    # years = [int(i) for i in times[0]]
        
     # Chart 1: Share of unmet care need
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['shareUnmetCareDemand'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['shareUnmetCareDemand'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Share of Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    filename = folder + '/ShareUnmetCareNeedChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Chart 2: Average unmet care need
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of Unmet Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Average Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    filename = folder + '/AverageUnmetCareNeedChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    ### Add charts with not discounted aggregate and average QALY
    # Chart 3: Aggregate Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Aggregate QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Aggregate Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    filename = folder + '/AggregateQALYChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Chart 4: Average Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['meanQALY'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['meanQALY'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Average QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Average Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    filename = folder + '/AverageQALYChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Chart 5: Aggregate Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['discountedQALY'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['discountedQALY'])

    ax.set_xlim(left = p['implementPoliciesFromYear'])
    ax.set_ylabel('Discounted QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Discounted Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['implementPoliciesFromYear'], p['endYear'])
    plt.xticks(range(p['implementPoliciesFromYear'], p['endYear']+1, 5))
    fig.tight_layout()
    filename = folder + '/DiscountedAggregateQALYChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Chart 6: Average Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['averageDiscountedQALY'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['averageDiscountedQALY'])

    ax.set_xlim(left = p['implementPoliciesFromYear'])
    ax.set_ylabel('Discounted Average QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Discounted Average Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['implementPoliciesFromYear'], p['endYear'])
    plt.xticks(range(p['implementPoliciesFromYear'], p['endYear']+1, 5))
    fig.tight_layout()
    filename = folder + '/DiscountedAverageQALYChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Chart 7: per-capita Hospitalization Costs 
    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'], label = 'Run ' + str(i))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Per-capita Yearly Cost')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Per-Capita Hospitalization Costs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    filename = folder + '/PerCapitaHospitalizationCostsChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    

def policyGraphs(folder, numPolicies):
    
    p = init_params()
    
    outputs = []
    for r in range(numPolicies):
        repFolder = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\SocPolicy_Sim\Policy_' + str(r)
        filename = repFolder + '/Outputs.csv'
        output = pd.read_csv(filename, sep=',',header=0)
        outputs.append(output)
    
    outputsByParams = []
    n = 1
    for i in range(p['numberPolicyParameters']):
        outputsByParams.append([])
        outputsByParams[i].append(outputs[n])
        outputsByParams[i].append(outputs[n+1])
        n += 2
        
    for r in range(p['numberPolicyParameters']):
        
        fig, ax = plt.subplots()
        p1, = ax.plot(outputs[0]['year'], outputs[0]['shareUnmetCareDemand'], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(outputsByParams[r][0]['year'], outputsByParams[r][0]['shareUnmetCareDemand'], label = 'Policy A')
        p3, = ax.plot(outputsByParams[r][1]['year'], outputsByParams[r][1]['shareUnmetCareDemand'], label = 'Policy B')
        ax.set_xlim(left = p['statsCollectFrom'])
        ax.set_ylabel('Share of Unmet Care Demand')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Policy Lever ' + str(r))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(p['statsCollectFrom'], p['endYear'])
        plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/shareUnmetCareDemand_L' + str(r) + '_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
    
        fig, ax = plt.subplots()
        p1, = ax.plot(outputs[0]['year'], outputs[0]['unmetCarePerRecipient'], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(outputsByParams[r][0]['year'], outputsByParams[r][0]['unmetCarePerRecipient'], label = 'Policy A')
        p3, = ax.plot(outputsByParams[r][1]['year'], outputsByParams[r][1]['unmetCarePerRecipient'], label = 'Policy B')
        ax.set_xlim(left = p['statsCollectFrom'])
        ax.set_ylabel('Hours of Unmet Care Need')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Policy Lever ' + str(r))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(p['statsCollectFrom'], p['endYear'])
        plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageUnmetCareDemand_L' + str(r) + '_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
    
        fig, ax = plt.subplots()
        p1, = ax.plot(outputs[0]['year'], outputs[0]['totQALY'], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(outputsByParams[r][0]['year'], outputsByParams[r][0]['totQALY'], label = 'Policy A')
        p3, = ax.plot(outputsByParams[r][1]['year'], outputsByParams[r][1]['totQALY'], label = 'Policy B')
        ax.set_xlim(left = p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Policy Lever ' + str(r))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(p['statsCollectFrom'], p['endYear'])
        plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/aggregateQALY_L' + str(r) + '_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
    
        fig, ax = plt.subplots()
        p1, = ax.plot(outputs[0]['year'], outputs[0]['meanQALY'], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(outputsByParams[r][0]['year'], outputsByParams[r][0]['meanQALY'], label = 'Policy A')
        p3, = ax.plot(outputsByParams[r][1]['year'], outputsByParams[r][1]['meanQALY'], label = 'Policy B')
        ax.set_xlim(left = p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Policy Lever ' + str(r))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(p['statsCollectFrom'], p['endYear'])
        plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageQALY_L' + str(r) + '_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
    
        fig, ax = plt.subplots()
        p1, = ax.plot(outputs[0]['year'], outputs[0]['perCapitaHospitalizationCost'], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(outputsByParams[r][0]['year'], outputsByParams[r][0]['perCapitaHospitalizationCost'], label = 'Policy A')
        p3, = ax.plot(outputsByParams[r][1]['year'], outputsByParams[r][1]['perCapitaHospitalizationCost'], label = 'Policy B')
        ax.set_xlim(left = p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Policy Lever ' + str(r))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(p['statsCollectFrom'], p['endYear'])
        plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/perCapitaHealthCareCost_L' + str(r) + '_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
    
    # Grouped Bar Charts
    
    policyYears = (p['endYear']-p['implementPoliciesFromYear']) + 1
    
    P1_M = []
    P2_M = []
    P0_M = []
    P1_SD = []
    P2_SD = []
    P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        P1_M.append(np.mean(outputsByParams[r][0]['shareUnmetCareDemand'][-policyYears:]))
        P2_M.append(np.mean(outputsByParams[r][1]['shareUnmetCareDemand'][-policyYears:]))
        P0_M.append(np.mean(outputs[0]['shareUnmetCareDemand'][-policyYears:]))
            
        P1_SD.append(np.std(outputsByParams[r][0]['shareUnmetCareDemand'][-policyYears:]))
        P2_SD.append(np.std(outputsByParams[r][1]['shareUnmetCareDemand'][-policyYears:]))
        P0_SD.append(np.std(outputs[0]['shareUnmetCareDemand'][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                label = 'Policy 1')
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                label = 'Policy 2')
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                label = 'Benchmark')
    ax.set_ylabel('Share of Unmet Care Need')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Shares of Unmet Care Need')
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/SharesUnmetCareSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    P1_M = []
    P2_M = []
    P0_M = []
    P1_SD = []
    P2_SD = []
    P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        P1_M.append(np.mean(outputsByParams[r][0]['unmetCarePerRecipient'][-policyYears:]))
        P2_M.append(np.mean(outputsByParams[r][1]['unmetCarePerRecipient'][-policyYears:]))
        P0_M.append(np.mean(outputs[0]['unmetCarePerRecipient'][-policyYears:]))
            
        P1_SD.append(np.std(outputsByParams[r][0]['unmetCarePerRecipient'][-policyYears:]))
        P2_SD.append(np.std(outputsByParams[r][1]['unmetCarePerRecipient'][-policyYears:]))
        P0_SD.append(np.std(outputs[0]['unmetCarePerRecipient'][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                label = 'Policy 1')
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                label = 'Policy 2')
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                label = 'Benchmark')
    ax.set_ylabel('Hours of Unmet Care Need')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Average Unmet Care Need')
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/AveragesUnmetCareSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    # Add chart of cost per hour of additional care
    # unmetSocialCareNeed
    
    P1_M = []
    P2_M = []
    P0_M = []
#        P1_SD = []
#        P2_SD = []
#        P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        
        costPerAdditionalCare_P1 = []
        costPerAdditionalCare_P2 = []
        
        for i in range(len(outputs[0]['unmetSocialCareNeed'])):
            if outputsByParams[r][0]['totalTaxRefund'][i] != 0:
                costPerAdditionalCare_P1.append((outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[r][0]['unmetSocialCareNeed'][i])/outputsByParams[r][0]['totalTaxRefund'][i])
            else:
                costPerAdditionalCare_P1.append(0.0)
            if outputsByParams[r][1]['totalTaxRefund'][i] != 0:
                costPerAdditionalCare_P2.append((outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[r][1]['unmetSocialCareNeed'][i])/outputsByParams[r][1]['totalTaxRefund'][i])
            else:
                costPerAdditionalCare_P2.append(0.0)
        
        P1_M.append(np.mean(costPerAdditionalCare_P1[-policyYears:]))
        P2_M.append(np.mean(costPerAdditionalCare_P2[-policyYears:]))
        
#        P1_SD.append(np.std(outputsByParams[r][0]['discountedQALY'][-policyYears:]))
#        P2_SD.append(np.std(outputsByParams[r][1]['discountedQALY'][-policyYears:]))
#        P0_SD.append(np.std(outputs[0]['discountedQALY'][-policyYears:]))
        
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.35         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD,
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD,
    # p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'Benchmark') # yerr = P0_SD,
    ax.set_ylabel('Cost per Hour')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Cost per Hour of Additional Care')
    # ax.set_xticks(index + bar_width + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/CostPerHourOfCareSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    ###########################################################################################################################
    
    P1_M = []
    P2_M = []
    P0_M = []
#        P1_SD = []
#        P2_SD = []
#        P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        P1_M.append(np.mean(outputsByParams[r][0]['discountedQALY'][-policyYears:]))
        P2_M.append(np.mean(outputsByParams[r][1]['discountedQALY'][-policyYears:]))
        P0_M.append(np.mean(outputs[0]['discountedQALY'][-policyYears:]))
        
#        P1_SD.append(np.std(outputsByParams[r][0]['discountedQALY'][-policyYears:]))
#        P2_SD.append(np.std(outputsByParams[r][1]['discountedQALY'][-policyYears:]))
#        P0_SD.append(np.std(outputs[0]['discountedQALY'][-policyYears:]))
        
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD,
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD,
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'Benchmark') # yerr = P0_SD,
    ax.set_ylabel('Aggregate QALY')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Aggregate Quality-adjusted Life Years')
    # ax.set_xticks(index + bar_width + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/TotalQALYSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    P1_M = []
    P2_M = []
    P0_M = []
#        P1_SD = []
#        P2_SD = []
#        P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        P1_M.append(np.mean(outputsByParams[r][0]['averageDiscountedQALY'][-policyYears:]))
        P2_M.append(np.mean(outputsByParams[r][1]['averageDiscountedQALY'][-policyYears:]))
        P0_M.append(np.mean(outputs[0]['averageDiscountedQALY'][-policyYears:]))
        
#        P1_SD.append(np.std(outputsByParams[r][0]['averageDiscountedQALY'][-policyYears:]))
#        P2_SD.append(np.std(outputsByParams[r][1]['averageDiscountedQALY'][-policyYears:]))
#        P0_SD.append(np.std(outputs[0]['averageDiscountedQALY'][-policyYears:]))
        
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD,
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD,
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'Benchmark') # yerr = P0_SD,
    ax.set_ylabel('Average QALY')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Average Quality-adjusted Life Years')
    # ax.set_xticks(index + bar_width)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/AverageQALYSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()

    P1_M = []
    P2_M = []
    P0_M = []
    P1_SD = []
    P2_SD = []
    P0_SD = []
    
    for r in range(p['numberPolicyParameters']):
        P1_M.append(np.mean(outputsByParams[r][0]['perCapitaHospitalizationCost'][-policyYears:]))
        P2_M.append(np.mean(outputsByParams[r][1]['perCapitaHospitalizationCost'][-policyYears:]))
        P0_M.append(np.mean(outputs[0]['perCapitaHospitalizationCost'][-policyYears:]))
            
        P1_SD.append(np.std(outputsByParams[r][0]['perCapitaHospitalizationCost'][-policyYears:]))
        P2_SD.append(np.std(outputsByParams[r][1]['perCapitaHospitalizationCost'][-policyYears:]))
        P0_SD.append(np.std(outputs[0]['perCapitaHospitalizationCost'][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                label = 'Policy 1')
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                label = 'Policy 2')
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                label = 'Benchmark')
    ax.set_ylabel('Per-capita Yearly Cost')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Per-capita Hospitalization Costs')
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    filename = folder + '/perCapitaHospitalizationCostsSensitivityGroupedBarChart.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()

def simulation(params):
    
    p = init_params()
    bs = Simulation(p)
    # output = bs.run(params)
    bs.run(params)
    #return output

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
            # result = pool.map(simulation, runNumber)
            pool.imap(simulation, runNumber)
            pool.close()
            pool.join()
            
            folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\MultipleRunsCharts'
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            multipleRunsGraphs(folder, p['numRepeats'])
            
        else:
            parameters = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
            parameters = map(list, zip(*parameters))
            policies = []
            defaultValues = [p['incomeCareParamPolicyCoeffcient'], p['socialSupportLevelPolicyChange'],
                             p['ageOfRetirementPolicyChange'], p['educationCostsPolicyCoefficient']]
            # Policies' combinations
            policies.append(defaultValues)
            for i in range(len(parameters)):
                for j in range(2):
                    runParameters = [x for x in defaultValues]
                    runParameters[i] = parameters[i][j]
                    policies.append(runParameters)       
            for p in policies:
                p.append(policies.index(p))
            
            numPolicies = range(len(policies))
            # result = pool.map(simulation, policies)
            pool.imap(simulation, policies)
            pool.close()
            pool.join()
    
            folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\SensitivityCharts'
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            policyGraphs(folder, numPolicies)
            
    else:
        p = init_params()
        random.seed(p['favouriteSeed'])
        np.random.seed(p['favouriteSeed'])
        
        if p['noPolicySim'] == True:  
            for i in range(p['numRepeats']):
                b = Simulation(p)
                b.run(i)
            
            folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\MultipleRunsCharts'
            
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            multipleRunsGraphs(folder, p['numRepeats'])
            
        else:
            parameters = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
            parameters = map(list, zip(*parameters))
            policies = []
            defaultValues = [p['incomeCareParamPolicyCoeffcient'], p['socialSupportLevelPolicyChange'],
                             p['ageOfRetirementPolicyChange'], p['educationCostsPolicyCoefficient']]
            # Policies' combinations
            policies.append(defaultValues)
            for i in range(len(parameters)):
                for j in range(2):
                    runParameters = [x for x in defaultValues]
                    runParameters[i] = parameters[i][j]
                    policies.append(runParameters)       
            for n in policies:
                n.append(policies.index(n))
            
            numPolicies = len(policies)
            
            for n in range(numPolicies):
                b = Simulation(p)
                b.run(policies[n])
                
            folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model\Charts\SensitivityCharts'
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            policyGraphs(folder, numPolicies)
    
    
    














