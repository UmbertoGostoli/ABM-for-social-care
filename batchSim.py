# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:36:11 2018

@author: Umberto Gostoli
"""


from simulation import Sim
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import time
import random
import os
import sys
from sklearn.externals import joblib
import fnmatch


class Simulation:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, params):
        self.p = dict(params)
        # self.year = self.p['startYear']
        self.times = []
        # Output variables
        self.shareUnmetCareDemand = []
        self.averageUnmetCareDemand = []
        self.discountedQALY = []
        self.averageDiscountedQALY = []
        self.perCapitaHealthCareCost = []
        
    def run(self):
        
        # sys.setrecursionlimit(10000)
        # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        
        if self.p['policyOnlySim'] == False:
            
            for r in range(self.p['numRepeats']):
                
                folder  = 'N:/Social Care Model II/Charts/noPolicy_Sim/Repeat_' + str(r)
                if not os.path.isdir(os.path.dirname(folder)):
                    os.makedirs(folder)
               
                filename = folder + '/parameterValues.csv'
                if not os.path.isdir(os.path.dirname(filename)):
                    os.mkdir(os.path.dirname(filename))
                    
                self.times = []
                
                random.seed(self.p['favouriteSeed'])
                np.random.seed(self.p['favouriteSeed'])
                self.randomSeed = self.p['favouriteSeed']
                
                if self.p['numRepeats'] > 1:
                    rdTime = (int)(time.time())
                    self.randomSeed = rdTime
                    random.seed(rdTime)
                    np.random.seed(rdTime)
                    
                values = zip(np.array([self.randomSeed, self.p['incomeCareParam'], self.p['socialSupportLevel'], self.p['ageOfRetirement'], 
                            self.p['educationCosts'][0], self.p['educationCosts'][1], self.p['educationCosts'][2], self.p['educationCosts'][3]]))
                names = ('randomSeed, incomeCareParam, socialSupportLevel, ageOfRetirement, educationCosts_II, educationCosts_III, educationCosts_IV, educationCosts_V')
                np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="")
                
                s = Sim(self.p, self.randomSeed)
                s.initializePop()
                
                for self.year in range(self.p['startYear'], self.p['endYear']+1):
                    
                    print(" ")
                    print('No policy - Run ' + str(r) + ' - ' + str(self.year))
                    
                    s.doOneYear(self.year) 
                    
                    # self.p['implementPoliciesFromYear']-1
#                    if self.year == self.p['startYear']+5 and self.p['noPolicySim'] == False:
#                        
#                        oldList = list(s.pop.allPeople)
#                        print ('Old list: ' + str(len(oldList)))
#                        listsToSave = [s.pop.allPeople, s.pop.livingPeople, s.map.towns]#, s.map.allHouses, s.map.occupiedHouses, s.jobMarketMap]
#                        names = ['allPeople', 'livingPeople', 'towns']#, 'allHouses', 'occupiedHouses', 'jobMarketMap']
#                        
#                        # Save list of objects
#                        self.saveLists(listsToSave, names)
#                         
#                        # Retrieve list of objects
#                        loadedList = self.loadList(names)
#                        
#                        # Assign retrived 
#                        s.pop.allPeople = loadedList[0] # self.loadList('allPeople')
#                        s.pop.livingPeople = loadedList[1]
#                        s.map.towns = loadedList[2]
#                        s.map.allHouses = loadedList[3]
#                        s.map.occupiedHouses = loadedList[4]
#                        s.jobMarketMap = loadedList[5]
                        
                        # , s.pop.livingPeople, s.map.towns, s.map.allHouses, s.map.occupiedHouses, s.jobMarketMap 
                        
#                        for i in listsToSave:
#                            i = self.loadList(names[listsToSave.index(i)])
                        # savedLists = self.loadLists()
                        
                        # s.pop.allPeople, s.pop.livingPeople, s.map.towns, s.map.allHouses, s.map.occupiedHouses, s.jobMarketMap =  savedLists
                        
                        
                        
                        
#                        with open('pop.pkl', 'wb') as output:
#                            pickle.dump(s.pop, output, pickle.HIGHEST_PROTOCOL)
#                            
#                        with open('map.pkl', 'wb') as output:
#                            pickle.dump(s.map, output, pickle.HIGHEST_PROTOCOL)
#                            
#                        with open('job.pkl', 'wb') as output:
#                            pickle.dump(s.jobMarketMap, output, pickle.HIGHEST_PROTOCOL)
#                       
#                        with open('pop.pkl', 'rb') as input:
#                            s.pop = pickle.load(input)
#                        with open('map.pkl', 'rb') as input:
#                            s.map = pickle.load(input)
#                        with open('job.pkl', 'rb') as input:
#                            s.jobMarketMap = pickle.load(input)
                            
                    self.times.append(self.year)
                    
                s.outputFile(folder)
                
                if self.p['singleRunGraphs']:
                    s.doGraphs(folder)
                    
                s.interactiveGraphics()
                
                outputVariables = s.getOutputs()
                
                s.emptyLists()
                
                self.shareUnmetCareDemand.append(outputVariables[0])
                self.averageUnmetCareDemand.append(outputVariables[1])
                self.discountedQALY.append(outputVariables[2])
                self.averageDiscountedQALY.append(outputVariables[3])
                self.perCapitaHealthCareCost.append(outputVariables[4])
            
            folder  = 'N:/Social Care Model II/Charts/MultipleRunsCharts'
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            self.multipleRunsGraphs(folder)
            
            self.shareUnmetCareDemand = self.shareUnmetCareDemand[:1]
            self.averageUnmetCareDemand = self.averageUnmetCareDemand[:1]
            self.discountedQALY = self.discountedQALY[:1]
            self.averageDiscountedQALY = self.averageDiscountedQALY[:1]
            self.perCapitaHealthCareCost = self.perCapitaHealthCareCost[:1]
                
        if self.p['noPolicySim'] == False:   
            
            self.parameters = np.genfromtxt('parameters.csv', skip_header = 1, delimiter=',')
            self.parameters = map(list, zip(*self.parameters))
            policies = []
            defaultValues = [self.p['incomeCareParamPolicyCoeffcient'], self.p['socialSupportLevelPolicyChange'], self.p['ageOfRetirementPolicyChange'], self.p['educationCostsPolicyCoefficient']]
        
            for i in range(len(self.parameters)):
                for j in range(2):
                    runParameters = [x for x in defaultValues]
                    runParameters[i] = self.parameters[i][j]
                    policies.append(runParameters)
             
            random.seed(self.p['favouriteSeed'])
            np.random.seed(self.p['favouriteSeed'])
            self.randomSeed = self.p['favouriteSeed']
            
            for n in range(len(policies)):
                
                print('Policy Combination: ' + str(n))
                
                f = Sim(self.p, self.randomSeed)
                f.initializePop()
                
                
#                with open('simulation.pkl', 'rb') as input:
#                    f = pickle.load(input)
                
                policyParameters = [] 
                
                for i in range(self.p['numberPolicyParameters']):
                    policyParameters.append(policies[n][i])
                
                folder  = 'N:/Social Care Model II/Charts/Policy_' + str(n) #
                if not os.path.isdir(os.path.dirname(folder)):
                    os.makedirs(folder)
               
                filename = folder + '/parameterValues.csv'
                if not os.path.isdir(os.path.dirname(filename)):
                    os.mkdir(os.path.dirname(filename))
    
                values = zip(np.array([self.randomSeed, self.p['incomeCareParam']*policies[n][0], self.p['socialSupportLevel']+policies[n][1], 
                            self.p['ageOfRetirement']+policies[n][2], self.p['educationCosts'][0]*policies[n][3], 
                            self.p['educationCosts'][1]*policies[n][3], self.p['educationCosts'][2]*policies[n][3], 
                            self.p['educationCosts'][3]*policies[n][3]]))
                names = ('randomSeed, incomeCareParam, socialSupportLevel, ageOfRetirement, educationCosts_II, educationCosts_III, educationCosts_IV, educationCosts_V')
                np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="")
            
                for self.year in range(self.p['startYear'], self.p['endYear']+1):
                    
                    print(" ")
                    print('Policy ' + str(n) + ' - ' + str(self.year))
                    
                    if self.year == self.p['implementPoliciesFromYear']:
                        
                        f.updatePolicyParameters(policyParameters)
                    
                    f.doOneYear(self.year) 
                    
                    self.times.append(self.year)
                    
                f.outputFile(folder)
                
                if self.p['singleRunGraphs']:
                    f.doGraphs(folder)
                    
                f.interactiveGraphics()
                
                outputVariables = f.getOutputs()
                
                f.emptyLists()
                
                self.shareUnmetCareDemand.append(outputVariables[0])
                self.averageUnmetCareDemand.append(outputVariables[1])
                self.discountedQALY.append(outputVariables[2])
                self.averageDiscountedQALY.append(outputVariables[3])
                self.perCapitaHealthCareCost.append(outputVariables[4])
            
            folder  = 'N:/Social Care Model II/Charts/SensitivityCharts'
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            self.policyGraphs(folder)
     
    def saveLists(self, listOfLists, names):
        for singleList in listOfLists:
            p = self.subLists(singleList)
            for h in p:
                joblib.dump(h, names[listOfLists.index(singleList)] + '_' + str(p.index(h)) + '.pkl')
        
    def loadList(self, names):
        allLists = []
        for name in names:
            listOfObjects = []
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*' + name + '*.pkl'):
                    listOfObjects.extend(joblib.load(file))
            allLists.append(listOfObjects)
        return allLists
        
    def subLists(self, aList):
        itemsPerGroup = 100
        subLength = (int)(len(aList)/itemsPerGroup)
        remain = len(aList)-subLength*itemsPerGroup
        p = []
        for i in range (subLength):
            h = itemsPerGroup*i
            p.append(aList[h:(h+itemsPerGroup)])
        if remain > 0:
            h = itemsPerGroup*subLength
            p.append(aList[h:(h+remain)])
        return p
    
    
    def multipleRunsGraphs(self, folder):
        years = [int(i) for i in self.times]
        
        # Chart 1: Share of unmet care need
        fig, ax = plt.subplots()
        p = [None]*self.p['numRepeats']
        for i in range(self.p['numRepeats']):
            p[i], = ax.plot(years, self.shareUnmetCareDemand[i], label = 'Run ' + str(i))
#            p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
#            p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
#            p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
#            p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
#            p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/ShareUnmetCareNeedChart_MR.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 2: Average unmet care need
        fig, ax = plt.subplots()
        p = [None]*self.p['numRepeats']
        for i in range(self.p['numRepeats']):
            p[i], = ax.plot(years, self.averageUnmetCareDemand[i], label = 'Run ' + str(i))
#            p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
#            p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
#            p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
#            p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
#            p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of Care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AverageUnmetCareNeedChart_MR.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 3: Aggregate Quality-adjusted Life Years
        fig, ax = plt.subplots()
        p = [None]*self.p['numRepeats']
        for i in range(self.p['numRepeats']):
            p[i], = ax.plot(years, self.discountedQALY[i], label = 'Run ' + str(i))
#            p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
#            p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
#            p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
#            p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
#            p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Aggregate Quality-adjusted Life Years')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AggregateQALYChart_MR.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 4: Average Quality-adjusted Life Years
        fig, ax = plt.subplots()
        p = [None]*self.p['numRepeats']
        for i in range(self.p['numRepeats']):
            p[i], = ax.plot(years, self.averageDiscountedQALY[i], label = 'Run ' + str(i))
#            p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
#            p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
#            p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
#            p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
#            p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Quality-adjusted Life Years')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/AverageQALYChart_MR.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 5: per-capita Hospitalization Costs
        fig, ax = plt.subplots()
        p = [None]*self.p['numRepeats']
        for i in range(self.p['numRepeats']):
            p[i], = ax.plot(years, self.perCapitaHealthCareCost[i], label = 'Run ' + str(i))
#            p2, = ax.plot(years, self.shareUnmetCareDemand_1, label = 'Class I')
#            p3, = ax.plot(years, self.shareUnmetCareDemand_2, label = 'Class II')
#            p4, = ax.plot(years, self.shareUnmetCareDemand_3, label = 'Class III')
#            p5, = ax.plot(years, self.shareUnmetCareDemand_4, label = 'Class IV')
#            p6, = ax.plot(years, self.shareUnmetCareDemand_5, label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per-Capita Hospitalization Costs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/PerCapitaHospitalizationCostsChart_MR.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
         
    def policyGraphs(self, folder):
        
        # Chart 1: effect of incomeCareParamPolicyCoeffcient on share of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetCareDemand[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.shareUnmetCareDemand[1], label = 'Halved')
        p3, = ax.plot(years, self.shareUnmetCareDemand[2], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Unmet Care Demand')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Income-for-Care Share')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/shareUnmetCareDemand_L1_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 2: effect of socialSupportLevelPolicyChange on share of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetCareDemand[0], linewidth = 2, label = 'Benchmark (no support)')
        p2, = ax.plot(years, self.shareUnmetCareDemand[3], label = 'Level 5 supported')
        p3, = ax.plot(years, self.shareUnmetCareDemand[4], label = 'Level 4 and 5 supported')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Unmet Care Demand')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Public Support of Care Need Levels')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/shareUnmetCareDemand_L2_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 3: effect of age of retirement on share of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetCareDemand[0], linewidth = 2, label = 'Benchmark (65)')
        p2, = ax.plot(years, self.shareUnmetCareDemand[5], label = '60')
        p3, = ax.plot(years, self.shareUnmetCareDemand[6], label = '70')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Unmet Care Demand')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Age of Retirement')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/shareUnmetCareDemand_L3_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 4: effect of education costs on share of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.shareUnmetCareDemand[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.shareUnmetCareDemand[7], label = 'Halved')
        p3, = ax.plot(years, self.shareUnmetCareDemand[8], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of Unmet Care Demand')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Cost of Education')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/shareUnmetCareDemand_L4_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 5: effect of incomeCareParamPolicyCoeffcient on average of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageUnmetCareDemand[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageUnmetCareDemand[1], label = 'Halved')
        p3, = ax.plot(years, self.averageUnmetCareDemand[2], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of Care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Income-for-Care Share')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageUnmetCareDemand_L1_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 6: effect of socialSupportLevelPolicyChange on average of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageUnmetCareDemand[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageUnmetCareDemand[3], label = 'Level 5 supported')
        p3, = ax.plot(years, self.averageUnmetCareDemand[4], label = 'Level 4 and 5 supported')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of Care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Public Support of Care Need Levels')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageUnmetCareDemand_L2_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 7: effect of age of retirement on average of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageUnmetCareDemand[0], linewidth = 2, label = 'Benchmark (65)')
        p2, = ax.plot(years, self.averageUnmetCareDemand[5], label = '60')
        p3, = ax.plot(years, self.averageUnmetCareDemand[6], label = '70')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of Care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Age of Retirement')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageUnmetCareDemand_L3_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 8: effect of education costs on average of unmet care demand.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageUnmetCareDemand[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageUnmetCareDemand[5], label = 'Halved')
        p3, = ax.plot(years, self.averageUnmetCareDemand[6], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of Care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Cost of Education')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageUnmetCareDemand_L4_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 9: effect of incomeCareParamPolicyCoeffcient on total quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.discountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.discountedQALY[1], label = 'Halved')
        p3, = ax.plot(years, self.discountedQALY[2], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Income-for-Care Share')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/discountedQALY_L1_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 10: effect of socialSupportLevelPolicyChange on total quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.discountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.discountedQALY[3], label = 'Level 5 supported')
        p3, = ax.plot(years, self.discountedQALY[4], label = 'Level 4 and 5 supported')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Public Support of Care Need Levels')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/discountedQALY_L2_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 11: effect of age of retirement on total quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.discountedQALY[0], linewidth = 2, label = 'Benchmark (65)')
        p2, = ax.plot(years, self.discountedQALY[5], label = '60')
        p3, = ax.plot(years, self.discountedQALY[6], label = '70')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Age of Retirement')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/discountedQALY_L3_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 12: effect of education costs on total quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.discountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.discountedQALY[7], label = 'Halved')
        p3, = ax.plot(years, self.discountedQALY[8], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Cost of Education')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/discountedQALY_L4_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 13: effect of incomeCareParamPolicyCoeffcient on average quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageDiscountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageDiscountedQALY[1], label = 'Halved')
        p3, = ax.plot(years, self.averageDiscountedQALY[2], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Income-for-Care Share')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageDiscountedQALY_L1_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 14: effect of socialSupportLevelPolicyChange on average quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageDiscountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageDiscountedQALY[3], label = 'Level 5 supported')
        p3, = ax.plot(years, self.averageDiscountedQALY[4], label = 'Level 4 and 5 supported')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Public Support of Care Need Levels')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageDiscountedQALY_L2_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 15: effect of age of retirement on average quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageDiscountedQALY[0], linewidth = 2, label = 'Benchmark (65)')
        p2, = ax.plot(years, self.averageDiscountedQALY[5], label = '60')
        p3, = ax.plot(years, self.averageDiscountedQALY[6], label = '70')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Age of Retirement')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageDiscountedQALY_L3_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 16: effect of education costs on average quality-adjusted life years.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.averageDiscountedQALY[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.averageDiscountedQALY[7], label = 'Halved')
        p3, = ax.plot(years, self.averageDiscountedQALY[8], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Cost of Education')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/averageDiscountedQALY_L4_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 17: effect of incomeCareParamPolicyCoeffcient on per-capita Health Care Cost.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.perCapitaHealthCareCost[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.perCapitaHealthCareCost[1], label = 'Halved')
        p3, = ax.plot(years, self.perCapitaHealthCareCost[2], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost (£)')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Income-for-Care Share')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/perCapitaHealthCareCost_L1_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 18: effect of socialSupportLevelPolicyChange on per-capita Health Care Cost.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.perCapitaHealthCareCost[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.perCapitaHealthCareCost[3], label = 'Level 5 supported')
        p3, = ax.plot(years, self.perCapitaHealthCareCost[4], label = 'Level 4 and 5 supported')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost (£)')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Public Support of Care Need Levels')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/perCapitaHealthCareCost_L2_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 19: effect of age of retirement on per-capita Health Care Cost.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.perCapitaHealthCareCost[0], linewidth = 2, label = 'Benchmark (65)')
        p2, = ax.plot(years, self.perCapitaHealthCareCost[5], label = '60')
        p3, = ax.plot(years, self.perCapitaHealthCareCost[6], label = '70')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost (£)')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Age of Retirement')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/perCapitaHealthCareCost_L3_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 20: effect of education costs on per-capita Health Care Cost.
        fig, ax = plt.subplots()
        p1, = ax.plot(years, self.perCapitaHealthCareCost[0], linewidth = 2, label = 'Benchmark')
        p2, = ax.plot(years, self.perCapitaHealthCareCost[7], label = 'Halved')
        p3, = ax.plot(years, self.perCapitaHealthCareCost[8], label = 'Doubled')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Per-capita Yearly Cost (£)')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Cost of Education')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        filename = folder + '/perCapitaHealthCareCost_L4_Chart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 21: SharesUnmetCareSensitivityGroupedBarChart
        P1_M = []
        P2_M = []
        P0_M = []
        P1_M.append(np.mean(self.shareUnmetCareDemand[1][-20:]))
        P2_M.append(np.mean(self.shareUnmetCareDemand[2][-20:]))
        P1_M.append(np.mean(self.shareUnmetCareDemand[3][-20:]))
        P2_M.append(np.mean(self.shareUnmetCareDemand[4][-20:]))
        P1_M.append(np.mean(self.shareUnmetCareDemand[5][-20:]))
        P2_M.append(np.mean(self.shareUnmetCareDemand[6][-20:]))
        P1_M.append(np.mean(self.shareUnmetCareDemand[7][-20:]))
        P2_M.append(np.mean(self.shareUnmetCareDemand[8][-20:]))
        for i in range(4):
            P0_M.append(np.mean(self.shareUnmetCareDemand[0][-20:]))
            
        P1_SD = []
        P2_SD = []
        P0_SD = []
        P1_SD.append(np.std(self.shareUnmetCareDemand[1][-20:]))
        P2_SD.append(np.std(self.shareUnmetCareDemand[2][-20:]))
        P1_SD.append(np.std(self.shareUnmetCareDemand[3][-20:]))
        P2_SD.append(np.std(self.shareUnmetCareDemand[4][-20:]))
        P1_SD.append(np.std(self.shareUnmetCareDemand[5][-20:]))
        P2_SD.append(np.std(self.shareUnmetCareDemand[6][-20:]))
        P1_SD.append(np.std(self.shareUnmetCareDemand[7][-20:]))
        P2_SD.append(np.std(self.shareUnmetCareDemand[8][-20:]))
        for i in range(4):
            P0_SD.append(np.std(self.shareUnmetCareDemand[0][-20:]))
        
        N = len(P1_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                    label = 'P1')
        p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                    label = 'P2')
        p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                    label = 'No policy change')
        ax.set_ylabel('Share of Unmet Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Shares of Unmet Care Need')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('Lever 1', 'Lever 2', 'Lever 3', 'Lever 4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/SharesUnmetCareSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 22: AveragesUnmetCareSensitivityGroupedBarChart
        P1_M = []
        P2_M = []
        P0_M = []
        P1_M.append(np.mean(self.averageUnmetCareDemand[1][-20:]))
        P2_M.append(np.mean(self.averageUnmetCareDemand[2][-20:]))
        P1_M.append(np.mean(self.averageUnmetCareDemand[3][-20:]))
        P2_M.append(np.mean(self.averageUnmetCareDemand[4][-20:]))
        P1_M.append(np.mean(self.averageUnmetCareDemand[5][-20:]))
        P2_M.append(np.mean(self.averageUnmetCareDemand[6][-20:]))
        P1_M.append(np.mean(self.averageUnmetCareDemand[7][-20:]))
        P2_M.append(np.mean(self.averageUnmetCareDemand[8][-20:]))
        for i in range(4):
            P0_M.append(np.mean(self.averageUnmetCareDemand[0][-20:]))
            
        P1_SD = []
        P2_SD = []
        P0_SD = []
        P1_SD.append(np.std(self.averageUnmetCareDemand[1][-20:]))
        P2_SD.append(np.std(self.averageUnmetCareDemand[2][-20:]))
        P1_SD.append(np.std(self.averageUnmetCareDemand[3][-20:]))
        P2_SD.append(np.std(self.averageUnmetCareDemand[4][-20:]))
        P1_SD.append(np.std(self.averageUnmetCareDemand[5][-20:]))
        P2_SD.append(np.std(self.averageUnmetCareDemand[6][-20:]))
        P1_SD.append(np.std(self.averageUnmetCareDemand[7][-20:]))
        P2_SD.append(np.std(self.averageUnmetCareDemand[8][-20:]))
        for i in range(4):
            P0_SD.append(np.std(self.averageUnmetCareDemand[0][-20:]))
        
        N = len(P1_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                    label = 'P1')
        p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                    label = 'P2')
        p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                    label = 'No policy change')
        ax.set_ylabel('Average Unmet Care')
        ax.set_xlabel('Parameters')
        ax.set_title('Average Unmet Care Need')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('Lever 1', 'Lever 2', 'Lever 3', 'Lever 4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/AveragesUnmetCareSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 23: TotalQALYSensitivityGroupedBarChart
        P1_M = []
        P2_M = []
        P0_M = []
        P1_M.append(np.sum(self.discountedQALY[1][-20:]))
        P2_M.append(np.sum(self.discountedQALY[2][-20:]))
        P1_M.append(np.sum(self.discountedQALY[3][-20:]))
        P2_M.append(np.sum(self.discountedQALY[4][-20:]))
        P1_M.append(np.sum(self.discountedQALY[5][-20:]))
        P2_M.append(np.sum(self.discountedQALY[6][-20:]))
        P1_M.append(np.sum(self.discountedQALY[7][-20:]))
        P2_M.append(np.sum(self.discountedQALY[8][-20:]))
        for i in range(4):
            P0_M.append(np.sum(self.discountedQALY[0][-20:]))
            
#        P1_SD = []
#        P2_SD = []
#        P0_SD = []
#        P1_SD.append(np.std(self.discountedQALY[1][-20:]))
#        P2_SD.append(np.std(self.discountedQALY[2][-20:]))
#        P1_SD.append(np.std(self.discountedQALY[3][-20:]))
#        P2_SD.append(np.std(self.discountedQALY[4][-20:]))
#        P1_SD.append(np.std(self.discountedQALY[5][-20:]))
#        P2_SD.append(np.std(self.discountedQALY[6][-20:]))
#        P1_SD.append(np.std(self.discountedQALY[7][-20:]))
#        P2_SD.append(np.std(self.discountedQALY[8][-20:]))
#        for i in range(4):
#            P0_SD.append(np.std(self.discountedQALY[0][-20:]))
        
        N = len(P1_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'P1') # yerr = P1_SD,
        p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'P2') # yerr = P2_SD,
        p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'No policy change') # yerr = P0_SD,
        ax.set_ylabel('Aggregate QALY')
        ax.set_xlabel('Parameters')
        ax.set_title('Aggregate Quality-adjusted Life Years')
        ax.set_xticks(index + bar_width)
        plt.xticks(index + bar_width, ('Lever 1', 'Lever 2', 'Lever 3', 'Lever 4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/TotalQALYSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 24: AverageQALYSensitivityGroupedBarChart
        
        P1_M = []
        P2_M = []
        P0_M = []
        P1_M.append(np.sum(self.averageDiscountedQALY[1][-20:]))
        P2_M.append(np.sum(self.averageDiscountedQALY[2][-20:]))
        P1_M.append(np.sum(self.averageDiscountedQALY[3][-20:]))
        P2_M.append(np.sum(self.averageDiscountedQALY[4][-20:]))
        P1_M.append(np.sum(self.averageDiscountedQALY[5][-20:]))
        P2_M.append(np.sum(self.averageDiscountedQALY[6][-20:]))
        P1_M.append(np.sum(self.averageDiscountedQALY[7][-20:]))
        P2_M.append(np.sum(self.averageDiscountedQALY[8][-20:]))
        for i in range(4):
            P0_M.append(np.sum(self.averageDiscountedQALY[0][-20:]))
            
#        P1_SD = []
#        P2_SD = []
#        P0_SD = []
#        P1_SD.append(np.std(self.averageDiscountedQALY[1][-20:]))
#        P2_SD.append(np.std(self.averageDiscountedQALY[2][-20:]))
#        P1_SD.append(np.std(self.averageDiscountedQALY[3][-20:]))
#        P2_SD.append(np.std(self.averageDiscountedQALY[4][-20:]))
#        P1_SD.append(np.std(self.averageDiscountedQALY[5][-20:]))
#        P2_SD.append(np.std(self.averageDiscountedQALY[6][-20:]))
#        P1_SD.append(np.std(self.averageDiscountedQALY[7][-20:]))
#        P2_SD.append(np.std(self.averageDiscountedQALY[8][-20:]))
#        for i in range(4):
#            P0_SD.append(np.std(self.averageDiscountedQALY[0][-20:]))
        
        N = len(P1_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'P1') # yerr = P1_SD,
        p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'P2') # yerr = P2_SD,
        p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'No policy change') # yerr = P0_SD,
        ax.set_ylabel('Average QALY')
        ax.set_xlabel('Parameters')
        ax.set_title('Average Quality-adjusted Life Years')
        ax.set_xticks(index + bar_width)
        plt.xticks(index + bar_width, ('Lever 1', 'Lever 2', 'Lever 3', 'Lever 4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/AverageQALYSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
        # Chart 25: perCapitaHospitalizationCostsSensitivityGroupedBarChart

        P1_M = []
        P2_M = []
        P0_M = []
        P1_M.append(np.mean(self.perCapitaHealthCareCost[1][-20:]))
        P2_M.append(np.mean(self.perCapitaHealthCareCost[2][-20:]))
        P1_M.append(np.mean(self.perCapitaHealthCareCost[3][-20:]))
        P2_M.append(np.mean(self.perCapitaHealthCareCost[4][-20:]))
        P1_M.append(np.mean(self.perCapitaHealthCareCost[5][-20:]))
        P2_M.append(np.mean(self.perCapitaHealthCareCost[6][-20:]))
        P1_M.append(np.mean(self.perCapitaHealthCareCost[7][-20:]))
        P2_M.append(np.mean(self.perCapitaHealthCareCost[8][-20:]))
        for i in range(4):
            P0_M.append(np.mean(self.perCapitaHealthCareCost[0][-20:]))
            
        P1_SD = []
        P2_SD = []
        P0_SD = []
        P1_SD.append(np.std(self.perCapitaHealthCareCost[1][-20:]))
        P2_SD.append(np.std(self.perCapitaHealthCareCost[2][-20:]))
        P1_SD.append(np.std(self.perCapitaHealthCareCost[3][-20:]))
        P2_SD.append(np.std(self.perCapitaHealthCareCost[4][-20:]))
        P1_SD.append(np.std(self.perCapitaHealthCareCost[5][-20:]))
        P2_SD.append(np.std(self.perCapitaHealthCareCost[6][-20:]))
        P1_SD.append(np.std(self.perCapitaHealthCareCost[7][-20:]))
        P2_SD.append(np.std(self.perCapitaHealthCareCost[8][-20:]))
        for i in range(4):
            P0_SD.append(np.std(self.perCapitaHealthCareCost[0][-20:]))
        
        N = len(P1_M)
        fig, ax = plt.subplots()
        index = np.arange(N)    # the x locations for the groups
        bar_width = 0.35         # the width of the bars
        p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, yerr = P1_SD, 
                    label = 'P1')
        p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, yerr = P2_SD, 
                    label = 'P2')
        p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, yerr = P0_SD, 
                    label = 'No policy change')
        ax.set_ylabel('Per-capita Yearly Cost (£)')
        ax.set_xlabel('Parameters')
        ax.set_title('Per-capita Hospitalization Costs')
        ax.set_xticks(index + bar_width/2)
        plt.xticks(index + bar_width/2, ('Lever 1', 'Lever 2', 'Lever 3', 'Lever 4'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        filename = folder + '/perCapitaHospitalizationCostsSensitivityGroupedBarChart.pdf'
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pp = PdfPages(filename)
        pp.savefig(fig)
        pp.close()
        
#        # Sensitivity Chart 6: Shares of Social Care
#        lowSharesSocialCare_M = self.sharesSocialCare_M[0::2]
#        lowSharesSocialCare_SD = self.sharesSocialCare_SD[0::2]
#        highSharesSocialCare_M = self.sharesSocialCare_M[1::2]
#        highSharesSocialCare_SD = self.sharesSocialCare_SD[1::2]
#        
#        N = len(lowSharesSocialCare_M)
#        fig, ax = plt.subplots()
#        index = np.arange(N)    # the x locations for the groups
#        bar_width = 0.35         # the width of the bars
#        p1 = ax.bar(index, lowSharesSocialCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesSocialCare_SD, 
#                    label = 'Low')
#        p2 = ax.bar(index + bar_width, highSharesSocialCare_M, bar_width,color='g', bottom = 0, yerr = highSharesSocialCare_SD, 
#                    label = 'High')
#        ax.set_ylabel('Share of Social Care')
#        ax.set_xlabel('Parameters')
#        ax.set_title('Shares of Social Care Received')
#        ax.set_xticks(index + bar_width/2)
#        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1])
#        fig.tight_layout()
#        filename = folder + '/SharesSocialCareSensitivityGroupedBarChart.pdf'
#        if not os.path.isdir(os.path.dirname(filename)):
#            os.mkdir(os.path.dirname(filename))
#        pp = PdfPages(filename)
#        pp.savefig(fig)
#        pp.close()
#        
#        # Sensitivity Chart 7: Shares of Informal Care
#        lowSharesInformalCare_M = self.sharesInformalCare_M[0::2]
#        lowSharesInformalCare_SD = self.sharesInformalCare_SD[0::2]
#        highSharesInformalCare_M = self.sharesInformalCare_M[1::2]
#        highSharesInformalCare_SD = self.sharesInformalCare_SD[1::2]
#        
#        N = len(lowSharesSocialCare_M)
#        fig, ax = plt.subplots()
#        index = np.arange(N)    # the x locations for the groups
#        bar_width = 0.35         # the width of the bars
#        p1 = ax.bar(index, lowSharesInformalCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesInformalCare_SD, 
#                    label = 'Low')
#        p2 = ax.bar(index + bar_width, highSharesInformalCare_M, bar_width,color='g', bottom = 0, yerr = highSharesInformalCare_SD, 
#                    label = 'High')
#        ax.set_ylabel('Share of Informal Care')
#        ax.set_xlabel('Parameters')
#        ax.set_title('Shares of Informal Care Received')
#        ax.set_xticks(index + bar_width/2)
#        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1])
#        fig.tight_layout()
#        filename = folder + '/SharesInformalCareSensitivityGroupedBarChart.pdf'
#        if not os.path.isdir(os.path.dirname(filename)):
#            os.mkdir(os.path.dirname(filename))
#        pp = PdfPages(filename)
#        pp.savefig(fig)
#        pp.close()
            
                
            
            
            
            
            
            