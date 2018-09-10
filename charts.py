# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 12:05:05 2018

@author: Umberto Gostoli
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
import pandas as pd



def init_params(output):
    """Set up the simulation parameters."""
    p = {}

    p['endYear'] = output['endYear'].values[0]
    p['statsCollectFrom'] = output['statCollectionYear'].values[0]
    p['numberPolicyParameters'] = output['numParameters'].values[0]
    p['numberScenarios'] = output['numScenarios'].values[0]
    p['numRepeats'] = output['numRepeats'].values[0]
    p['implementPoliciesFromYear'] = output['startPoliciesYear'].values[0]
    p['discountingFactor'] = output['discountingFactor'].values[0]
    p['numberClasses'] = output['numberClasses'].values[0]
    
    return p


def doGraphs(policyOnlySim):
    """Plot the graphs needed at the end of one run."""
    
    if noPolicySim == False:
        fileParam = rootFolder + '/Charts/SocPolicy_Sim/Policy_0/parameterValues.csv'
        output = pd.read_csv(fileParam, sep=',',header=0)
        p = init_params(output)
        numberFolders = p['numberScenarios']
        repFolder = rootFolder + '/Charts/SocPolicy_Sim/Policy_'
        sensitivityAnalysisFolder = rootFolder + '/Charts/SocPolicy_Sim/SensitivityCharts'
        if not os.path.exists(sensitivityAnalysisFolder):
            os.makedirs(sensitivityAnalysisFolder)
        createSensitivityGraphs(sensitivityAnalysisFolder, repFolder, numberFolders, p)
    else:
        fileParam = rootFolder + '/Charts/NoPolicy_Sim/Repeat_0/parameterValues.csv'
        output = pd.read_csv(fileParam, sep=',',header=0)
        p = init_params(output)
        numberFolders = p['numRepeats']
        repFolder = rootFolder + '/Charts/NoPolicy_Sim/Repeat_'
        multipleRunsFolder = rootFolder + '/Charts/NoPolicy_Sim/MultipleRunsCharts'
        if not os.path.exists(multipleRunsFolder):
            os.makedirs(multipleRunsFolder)
        createMultipleRunsGraphs(multipleRunsFolder, repFolder, numberFolders, p)
    
def createMultipleRunsGraphs(folder, singleRunsFolder, numFolders, p):
    
    outputs = []
    for r in range(numFolders):
        repFolder = singleRunsFolder + str(r)
        filename = repFolder + '/Outputs.csv'
        singleRunCharts(repFolder, filename, p)
        output = pd.read_csv(filename, sep=',',header=0)
        outputs.append(output)

    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['shareUnmetCareDemand'], label = 'Run ' + str(i+1))
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
    path = os.path.join(folder, 'ShareUnmetCareNeedChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 2: Average unmet care need
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of Unmet Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Average Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageUnmetCareNeedChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ### Add charts with not discounted aggregate and average QALY
    # Chart 3: Aggregate Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Aggregate QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Aggregate Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AggregateQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 4: Average Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['meanQALY'], label = 'Run ' + str(i+1))
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
    path = os.path.join(folder, 'AverageQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 5: Aggregate Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['discountedQALY'], label = 'Run ' + str(i+1))
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
    path = os.path.join(folder, 'DiscountedAggregateQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 6: Average Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['averageDiscountedQALY'], label = 'Run ' + str(i+1))
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
    path = os.path.join(folder, 'DiscountedAverageQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 7: per-capita Hospitalization Costs 
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Per-capita Yearly Cost')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Per-Capita Hospitalization Costs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaHospitalizationCostsChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
def createSensitivityGraphs(folder, singleRunsFolder, numFolders, p):
    outputs = []
    for r in range(numFolders):
        repFolder = singleRunsFolder + str(r)
        filename = repFolder + '/Outputs.csv'
        singleRunCharts(repFolder, filename, p)
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
        path = os.path.join(folder, 'shareUnmetCareDemand_L' + str(r) + '_Chart.pdf')
        pp = PdfPages(path)
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
        path = os.path.join(folder, 'averageUnmetCareDemand_L' + str(r) + '_Chart.pdf')
        pp = PdfPages(path)
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
        path = os.path.join(folder, 'aggregateQALY_L' + str(r) + '_Chart.pdf')
        pp = PdfPages(path)
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
        path = os.path.join(folder, 'averageQALY_L' + str(r) + '_Chart.pdf')
        pp = PdfPages(path)
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
        path = os.path.join(folder, 'perCapitaHealthCareCost_L' + str(r) + '_Chart.pdf')
        pp = PdfPages(path)
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
    path = os.path.join(folder, 'SharesUnmetCareSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
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
    path = os.path.join(folder, 'AveragesUnmetCareSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
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
        
        additionalSocialCare_1 = []
        additionalCost_1 = []
        additionalSocialCare_2 = []
        additionalCost_2 = []
        costPerAdditionalCare_P1 = []
        costPerAdditionalCare_P2 = []
        
        for i in range(len(outputs[0]['unmetSocialCareNeed'])):
            additionalSocialCare_1.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[r][0]['unmetSocialCareNeed'][i])
            additionalCost_1.append(outputsByParams[r][0]['totalCost'][i] - outputs[0]['totalCost'][i])
            additionalSocialCare_2.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[r][1]['unmetSocialCareNeed'][i])
            additionalCost_2.append(outputsByParams[r][1]['totalCost'][i] - outputs[0]['totalCost'][i])
            
        for i in range(len(additionalSocialCare_1)):    
            if additionalCost_1[i] != 0:
                costPerAdditionalCare_P1.append(additionalSocialCare_1[i]/additionalCost_1[i])
            else:
                costPerAdditionalCare_P1.append(0.0)
                
        for i in range(len(additionalSocialCare_2)):    
            if additionalCost_2[i] != 0:
                costPerAdditionalCare_P2.append(additionalSocialCare_2[i]/additionalCost_2[i])
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
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'CostPerHourOfCareSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
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
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalQALYSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
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
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'AverageQALYSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
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
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaHospitalizationCostsSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Total Cost charts
    P1_M = []
    P2_M = []
    P0_M = []
    P1_SD = []
    P2_SD = []
    P0_SD = []
    
    P1_M.append(np.sum(outputsByParams[0][0]['careCreditCost'][-policyYears:]))
    P1_M.append(np.sum(outputsByParams[1][0]['totalTaxRefund'][-policyYears:]))
    P1_M.append(np.sum(outputsByParams[2][0]['pensionBudget'][-policyYears:]))
    P1_M.append(np.sum(outputsByParams[3][0]['costDirectFunding'][-policyYears:]))
    
    P2_M.append(np.sum(outputsByParams[1][1]['careCreditCost'][-policyYears:]))
    P2_M.append(np.sum(outputsByParams[1][1]['totalTaxRefund'][-policyYears:]))
    P2_M.append(np.sum(outputsByParams[2][1]['pensionBudget'][-policyYears:]))
    P2_M.append(np.sum(outputsByParams[3][1]['costDirectFunding'][-policyYears:]))
    
    P0_M.append(np.sum(outputs[1]['careCreditCost'][-policyYears:]))
    P0_M.append(np.sum(outputs[1]['totalTaxRefund'][-policyYears:]))
    P0_M.append(np.sum(outputs[2]['pensionBudget'][-policyYears:]))
    P0_M.append(np.sum(outputs[3]['costDirectFunding'][-policyYears:]))
        
#    P1_SD.append(np.std(outputsByParams[r][0]['totalCost'][-policyYears:]))
#    P2_SD.append(np.std(outputsByParams[r][1]['totalCost'][-policyYears:]))
#    P0_SD.append(np.std(outputs[0]['totalCost'][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD, 
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD, 
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'Benchmark') # yerr = P0_SD, 
    plt.axhline(y = 0.0, color = 'black', linewidth = 0.5)
    ax.set_ylabel('Cost per Week')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Policies Net Cost')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'PoliciesNetCostsSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Discounted Cost charts
    P1_M = []
    P2_M = []
    P0_M = []
    P1_SD = []
    P2_SD = []
    P0_SD = []
    
    P1_M.append(discountedSum(outputsByParams[1][0]['careCreditCost'][-policyYears:]))
    P1_M.append(discountedSum(outputsByParams[1][0]['totalTaxRefund'][-policyYears:]))
    P1_M.append(discountedSum(outputsByParams[2][0]['pensionBudget'][-policyYears:]))
    P1_M.append(discountedSum(outputsByParams[3][0]['costDirectFunding'][-policyYears:]))
    
    P2_M.append(discountedSum(outputsByParams[1][1]['careCreditCost'][-policyYears:]))
    P2_M.append(discountedSum(outputsByParams[1][1]['totalTaxRefund'][-policyYears:]))
    P2_M.append(discountedSum(outputsByParams[2][1]['pensionBudget'][-policyYears:]))
    P2_M.append(discountedSum(outputsByParams[3][1]['costDirectFunding'][-policyYears:]))
    
    P0_M.append(discountedSum(outputs[1]['careCreditCost'][-policyYears:]))
    P0_M.append(discountedSum(outputs[1]['totalTaxRefund'][-policyYears:]))
    P0_M.append(discountedSum(outputs[2]['pensionBudget'][-policyYears:]))
    P0_M.append(discountedSum(outputs[3]['costDirectFunding'][-policyYears:]))
        
#    P1_SD.append(np.std(outputsByParams[r][0]['totalCost'][-policyYears:]))
#    P2_SD.append(np.std(outputsByParams[r][1]['totalCost'][-policyYears:]))
#    P0_SD.append(np.std(outputs[0]['totalCost'][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.25         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD, 
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD, 
    p0 = ax.bar(index + bar_width + bar_width, P0_M, bar_width,color='y', bottom = 0, label = 'Benchmark') # yerr = P0_SD, 
    plt.axhline(y = 0.0, color = 'black', linewidth = 0.5)
    ax.set_ylabel('Cost per Week')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Policies Discounted Net Cost')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'lower right')
    fig.tight_layout()
    path = os.path.join(folder, 'PoliciesDiscountedNetCostsSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Cost per additional hour of delivered social care
    P1_M = []
    P2_M = []
    P1_SD = []
    P2_SD = []
    
    additionalSocialCare_1 = []
    additionalCost_1 = []
    additionalSocialCare_2 = []
    additionalCost_2 = []
    additionalSocialCare_3 = []
    additionalCost_3 = []
    additionalSocialCare_4 = []
    additionalCost_4 = []
    
    for j in range(2):
        deltaCare_1 = []
        deltaCost_1 = []
        deltaCare_2 = []
        deltaCost_2 = []
        deltaCare_3 = []
        deltaCost_3 = []
        deltaCare_4 = []
        deltaCost_4 = []
        for i in range(len(outputs[0]['unmetSocialCareNeed'])):
            deltaCare_1.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[0][j]['unmetSocialCareNeed'][i])
            deltaCost_1.append(outputsByParams[0][j]['careCreditCost'][i] - outputs[0]['careCreditCost'][i])
            deltaCare_2.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[1][j]['unmetSocialCareNeed'][i])
            deltaCost_2.append(outputsByParams[1][j]['totalTaxRefund'][i] - outputs[0]['totalTaxRefund'][i])
            deltaCare_3.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[2][j]['unmetSocialCareNeed'][i])
            deltaCost_3.append(outputsByParams[2][j]['pensionBudget'][i] - outputs[0]['pensionBudget'][i])
            deltaCare_4.append(outputs[0]['unmetSocialCareNeed'][i]-outputsByParams[3][j]['unmetSocialCareNeed'][i])
            deltaCost_4.append(outputsByParams[3][j]['costDirectFunding'][i] - outputs[0]['costDirectFunding'][i])
        additionalSocialCare_1.append(deltaCare_1)
        additionalCost_1.append(deltaCost_1)
        additionalSocialCare_2.append(deltaCare_2)
        additionalCost_2.append(deltaCost_2)
        additionalSocialCare_3.append(deltaCare_3)
        additionalCost_3.append(deltaCost_3)
        additionalSocialCare_4.append(deltaCare_4)
        additionalCost_4.append(deltaCost_4)
    
    efficiency_1 = []
    efficiency_2 = []
    efficiency_3 = []
    efficiency_4 = []
    
    for j in range(2):
        e_1 = []
        e_2 = []
        e_3 = []
        e_4 = []
        for i in range(len(additionalSocialCare_1[j])):
            if additionalCost_1[j][i] != 0:
                e_1.append(additionalSocialCare_1[j][i]/additionalCost_1[j][i])
            else:
                e_1.append(0.0)
            if additionalCost_2[j][i] != 0:
                e_2.append(additionalSocialCare_2[j][i]/additionalCost_2[j][i])
            else:
                e_2.append(0.0)
            if additionalCost_3[j][i] != 0:
                e_3.append(additionalSocialCare_3[j][i]/additionalCost_3[j][i])
            else:
                e_3.append(0.0)
            if additionalCost_4[j][i] != 0:
                e_4.append(additionalSocialCare_4[j][i]/additionalCost_4[j][i])
            else:
                e_4.append(0.0)
        efficiency_1.append(e_1)
        efficiency_2.append(e_2)
        efficiency_3.append(e_3)
        efficiency_4.append(e_4)
        
    P1_M.append(np.mean(efficiency_1[0][-policyYears:]))
    P1_M.append(np.mean(efficiency_2[0][-policyYears:]))
    P1_M.append(np.mean(efficiency_3[0][-policyYears:]))
    P1_M.append(np.mean(efficiency_4[0][-policyYears:]))
    
    P2_M.append(np.mean(efficiency_1[1][-policyYears:]))
    P2_M.append(np.mean(efficiency_2[1][-policyYears:]))
    P2_M.append(np.mean(efficiency_3[1][-policyYears:]))
    P2_M.append(np.mean(efficiency_4[1][-policyYears:]))
    
    N = len(P1_M)
    fig, ax = plt.subplots()
    index = np.arange(N)    # the x locations for the groups
    bar_width = 0.35         # the width of the bars
    p1 = ax.bar(index, P1_M, bar_width, color='b', bottom = 0, label = 'Policy 1') # yerr = P1_SD, 
    p2 = ax.bar(index + bar_width, P2_M, bar_width,color='g', bottom = 0, label = 'Policy 2') # yerr = P2_SD, 
    plt.axhline(y = 0.0, color = 'black', linewidth = 0.5)
    ax.set_ylabel('Pounds')
    # ax.set_xlabel('Policy Levers')
    ax.set_title('Cost per Additional Hour of Care')
    # ax.set_xticks(index + bar_width/2)
    xLabels = []
    for r in range(p['numberPolicyParameters']):
        xLabels.append('Lever ' + str(r+1))
    xlab = tuple(xLabels)
    plt.xticks(index + bar_width/2, xlab)
    ax.xaxis.set_ticks_position('none')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    ax.legend(loc = 'upper right')
    fig.tight_layout()
    path = os.path.join(folder, 'CostPerAdditionalCareSensitivityGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

def discountedSum(timeSeries):
    discountedSum = 0
    ts = np.array(timeSeries)
    for i in range(len(ts)):
        discountedSum += ts[i]/pow((1.0 + p['discountingFactor']), float(i))
    return discountedSum

def singleRunCharts(folder, inputFile, p):
    # Individual runs charts
    output = pd.read_csv(inputFile, sep=',',header=0)

    # Chart 1: total social and child care demand and potential supply (from 1960 to 2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totalCareSupply'], linewidth=2, label = 'Potential Supply', color = 'green')
    ax.stackplot(output['year'], output['socialCareNeed'], output['childCareNeed'], labels = ['Social Care Need','Child Care Need'])
    # ax.plot(years, totalSocialCareDemand, linewidth=2, label = 'Social Care Need', color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    ax.set_title('Care Needs and Potential Supply')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'DemandSupplyStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 2: shares of care givers, total and by class shareCareGivers
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareCareGivers'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareCareGivers_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareCareGivers_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareCareGivers_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareCareGivers_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareCareGivers_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of population')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Care Givers')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareCareGiversChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 3: shares of care takers by level of care need
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['shareSocialCareTakers_N1'], output['shareSocialCareTakers_N2'], 
                  output['shareSocialCareTakers_N3'], output['shareSocialCareTakers_N4'],
                  labels = ['Need Level 1','Need Level 2', 'Need Level 3', 'Need level 4'])
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Share of Care Takers')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Care Takers by Care Need Level')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylim(0, 1)
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareByNeedLevelsStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 4: Share of Social Care Needs (1960-2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareSocialCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareSocialCare_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareSocialCare_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareSocialCare_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareSocialCare_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareSocialCare_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Share of Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareSocialCareNeedsChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 5: Per Capita total care demand and unmet care demand (1960-2020)    , 
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaCareReceived'], output['perCapitaUnmetCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Per Capita Received Care and Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaCareUnmetCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 6: Per Capita total social care demand and unmet social care demand (1960-2020) 
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaSocialCareReceived'], output['perCapitaUnmetSocialCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Per Capita Demand and Unmet Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaDemandUnmetSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 7: Per Capita total child care demand and unmet child care demand (1960-2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaChildCareReceived'], output['perCapitaUnmetChildCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Per Capita Demand and Unmet Child Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaDemandUnmetChildCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 8: total informal and formal care received and unmet care needs (from 1960 to 2020)
               
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalCareReceived'], output['formalCareReceived'], output['totalUnnmetCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 9: Shares informal care received (from 1960 to 2020)
    
    #sharesInformalCare_M.append(np.mean(shareInformalCareReceived[-20:]))
    #sharesInformalCare_SD.append(np.std(shareInformalCareReceived[-20:]))
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareReceived'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalCareReceived_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalCareReceived_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalCareReceived_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalCareReceived_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalCareReceived_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareInformalCareReceivedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 10: Shares informal social care received (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalSocialCare'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalSocialCare_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalSocialCare_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalSocialCare_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalSocialCare_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalSocialCare_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Social Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareInformalSocialCareReceivedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 11: Shares informal child care received (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalChildCare'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalChildCare_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalChildCare_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalChildCare_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalChildCare_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalChildCare_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Child Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareInformalChildCareReceivedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 12: total informal and formal social care received and unmet social care needs (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalSocialCareReceived'], output['formalSocialCareReceived'], output['unmetSocialCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Social Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 13: total informal and formal child care received and unmet child care needs (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalChildCareReceived'], output['formalChildCareReceived'], output['unmetChildCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Child Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    fig.tight_layout()
    path = os.path.join(folder, 'ChildCareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 14: Share of Unmet Care Need, total and by social class (from 1960 to 2020)
  
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareUnmetCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareUnmetCareDemand_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareUnmetCareDemand_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareUnmetCareDemand_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareUnmetCareDemand_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareUnmetCareDemand_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Share of Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetCareNeedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 15: Share of Unmet Social Care Need, total and by social class (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareUnmetSocialCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Share of Unmet Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetSocialCareNeedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 16: Share of Unmet Child Care Need, total and by social class (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareUnmetChildCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareUnmetChildCareDemand_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareUnmetChildCareDemand_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareUnmetChildCareDemand_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareUnmetChildCareDemand_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareUnmetChildCareDemand_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Unmet Child Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetChildCareNeedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 17: Per Capita Unmet Care Need, total and by social class (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['perCapitaUnmetCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Per Capita Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaUnmetNeedByClassChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 18: Average Unmet Care Need, total and by social class (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['averageUnmetCareDemand'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['averageUnmetCareDemand_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['averageUnmetCareDemand_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['averageUnmetCareDemand_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['averageUnmetCareDemand_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['averageUnmetCareDemand_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageUnmetCareNeedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 19 
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalCareReceived_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalCareReceived_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetCareNeed_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalCareReceived_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalCareReceived_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetCareNeed_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalCareReceived_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalCareReceived_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetCareNeed_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalCareReceived_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalCareReceived_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetCareNeed_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalCareReceived_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalCareReceived_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetCareNeed_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Care Need by Class')
    fig.tight_layout()
    path = os.path.join(folder, 'CareByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
     # Chart 20: informal care per recipient: population and by class
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['informalCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['informalCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['informalCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['informalCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['informalCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 50])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'InformalCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 21: formal care per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['formalCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['formalCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['formalCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['formalCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['formalCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['formalCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Formal Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'FormalCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    
    # Chart 22: unmet care need per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['unmetCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['unmetCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['unmetCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['unmetCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['unmetCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['unmetCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Unmet Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'UnmetCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 23: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalCarePerRecipient'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalCarePerRecipient'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['unmetCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 50])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 24: informal and formal care received and unmet care needs per recipient by social class (mean of last 20 years)
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalCarePerRecipient_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalCarePerRecipient_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetCarePerRecipient_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalCarePerRecipient_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalCarePerRecipient_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetCarePerRecipient_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalCarePerRecipient_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalCarePerRecipient_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetCarePerRecipient_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalCarePerRecipient_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalCarePerRecipient_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetCarePerRecipient_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalCarePerRecipient_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalCarePerRecipient_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetCarePerRecipient_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Care Need per Recipient')
    fig.tight_layout()
    path = os.path.join(folder, 'CarePerRecipientByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
   # Chart 25: informal and formal social care received and unmet social care needs by social class (mean of last 20 years)
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalSocialCareReceived_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalSocialCareReceived_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetSocialCareNeed_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalSocialCareReceived_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalSocialCareReceived_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetSocialCareNeed_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalSocialCareReceived_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalSocialCareReceived_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetSocialCareNeed_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalSocialCareReceived_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalSocialCareReceived_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetSocialCareNeed_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalSocialCareReceived_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalSocialCareReceived_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetSocialCareNeed_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Social Care Need by Class')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCareByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 26: informal and formal social care received and unmet social care needs per recipient by social class (mean of last 20 years)
   
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['informalSocialCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['informalSocialCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['informalSocialCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['informalSocialCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['informalSocialCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Social Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'informalSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 27: formal care per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['formalSocialCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['formalSocialCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['formalSocialCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['formalSocialCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Formal Social Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'formalSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

    # Chart 28: unmet care need per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Unmet Social Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'UnmetSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 29: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 30

    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalSocialCarePerRecipient_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalSocialCarePerRecipient_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetSocialCarePerRecipient_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalSocialCarePerRecipient_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalSocialCarePerRecipient_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetSocialCarePerRecipient_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalSocialCarePerRecipient_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalSocialCarePerRecipient_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetSocialCarePerRecipient_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalSocialCarePerRecipient_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalSocialCarePerRecipient_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetSocialCarePerRecipient_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalSocialCarePerRecipient_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalSocialCarePerRecipient_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetSocialCarePerRecipient_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Social Care Need per Recipient')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCarePerRecipientByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 31: informal and formal child care received and unmet child care needs by social class (mean of last 20 years)
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalChildCareReceived_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalChildCareReceived_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetChildCareNeed_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalChildCareReceived_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalChildCareReceived_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetChildCareNeed_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalChildCareReceived_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalChildCareReceived_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetChildCareNeed_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalChildCareReceived_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalChildCareReceived_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetChildCareNeed_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalChildCareReceived_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalChildCareReceived_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetChildCareNeed_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Child Care Need by Class')
    fig.tight_layout()
    path = os.path.join(folder, 'ChildCareByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 32: informal and formal child care received and unmet child care needs per recipient by Child class (mean of last 20 years)

    ### Add the three charts for the child care
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalChildCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['informalChildCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['informalChildCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['informalChildCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['informalChildCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['informalChildCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'informalChildCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 33: formal care per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['formalChildCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['formalChildCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['formalChildCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['formalChildCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['formalChildCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['formalChildCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Formal Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'formalChildCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

     # Chart 34: Average Supply by Class (from 1960 to 2020)
     
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['carePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['carePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['carePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['carePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['carePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['carePerRecipient_5'], label = 'Class V')
    maxValues = [max(output['carePerRecipient']), max(output['carePerRecipient_1']), max(output['carePerRecipient_2']), max(output['carePerRecipient_3']), max(output['carePerRecipient_4']), max(output['carePerRecipient_5'])]
    maxValue = max(maxValues)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylim([0, maxValue*2.0])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Hours of Care By Class')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim([0, 60])
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    

    # Chart 35: unmet care need per recipient: population and by class
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['unmetChildCarePerRecipient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['unmetChildCarePerRecipient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['unmetChildCarePerRecipient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['unmetChildCarePerRecipient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['unmetChildCarePerRecipient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['unmetChildCarePerRecipient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Unmet Child Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'UnmetChildCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 36: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalChildCarePerRecipient'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalChildCarePerRecipient'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['unmetChildCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Delivered and Unmet Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 30])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetChildCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 37
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalChildCarePerRecipient_1'][-20:])
    meanFormalCareReceived_1 = np.mean(output['formalChildCarePerRecipient_1'][-20:])
    meanUnmetNeed_1 = np.mean(output['unmetChildCarePerRecipient_1'][-20:])
    meanInformalCareReceived_2 = np.mean(output['informalChildCarePerRecipient_2'][-20:])
    meanFormalCareReceived_2 = np.mean(output['formalChildCarePerRecipient_2'][-20:])
    meanUnmetNeed_2 = np.mean(output['unmetChildCarePerRecipient_2'][-20:])
    meanInformalCareReceived_3 = np.mean(output['informalChildCarePerRecipient_3'][-20:])
    meanFormalCareReceived_3 = np.mean(output['formalChildCarePerRecipient_3'][-20:])
    meanUnmetNeed_3 = np.mean(output['unmetChildCarePerRecipient_3'][-20:])
    meanInformalCareReceived_4 = np.mean(output['informalChildCarePerRecipient_4'][-20:])
    meanFormalCareReceived_4 = np.mean(output['formalChildCarePerRecipient_4'][-20:])
    meanUnmetNeed_4 = np.mean(output['unmetChildCarePerRecipient_4'][-20:])
    meanInformalCareReceived_5 = np.mean(output['informalChildCarePerRecipient_5'][-20:])
    meanFormalCareReceived_5 = np.mean(output['formalChildCarePerRecipient_5'][-20:])
    meanUnmetNeed_5 = np.mean(output['unmetChildCarePerRecipient_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal, Formal and Unmet Child Care Need per Recipient')
    fig.tight_layout()
    path = os.path.join(folder, 'ChildCarePerRecipientByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 38: informal and formal care supplied per carer by social class (mean of last 20 years)
    
    n_groups = p['numberClasses']
    meanInformalCareSupplied_1 = np.mean(output['informalCarePerCarer_1'][-20:])
    meanFormalCareSupplied_1 = np.mean(output['formalCarePerCarer_1'][-20:])
    meanInformalCareSupplied_2 = np.mean(output['informalCarePerCarer_2'][-20:])
    meanFormalCareSupplied_2 = np.mean(output['formalCarePerCarer_2'][-20:])
    meanInformalCareSupplied_3 = np.mean(output['informalCarePerCarer_3'][-20:])
    meanFormalCareSupplied_3 = np.mean(output['formalCarePerCarer_3'][-20:])
    meanInformalCareSupplied_4 = np.mean(output['informalCarePerCarer_4'][-20:])
    meanFormalCareSupplied_4 = np.mean(output['formalCarePerCarer_4'][-20:])
    meanInformalCareSupplied_5 = np.mean(output['informalCarePerCarer_5'][-20:])
    meanFormalCareSupplied_5 = np.mean(output['formalCarePerCarer_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Informal and Formal Care per Carer')
    fig.tight_layout()
    path = os.path.join(folder, 'CarePerCarerByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 39: informal and formal care supplied by kinship network distance (mean of last 20 years) # Modified y lim
       
    n_groups = 4
    meanInformalCareHousehold = np.mean(output['sumNoK_informalSupplies[0]'][-20:])
    meanFormalCareHousehold = np.mean(output['sumNoK_formalSupplies[0]'][-20:])
    meanInformalCare_K1 = np.mean(output['sumNoK_informalSupplies[1]'][-20:])
    meanFormalCare_K1 = np.mean(output['sumNoK_formalSupplies[1]'][-20:])
    meanInformalCare_K2 = np.mean(output['sumNoK_informalSupplies[2]'][-20:])
    meanFormalCare_K2 = np.mean(output['sumNoK_formalSupplies[2]'][-20:])
    meanInformalCare_K3 = np.mean(output['sumNoK_informalSupplies[3]'][-20:])
    meanFormalCare_K3 = np.mean(output['sumNoK_formalSupplies[3]'][-20:])
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
    path = os.path.join(folder, 'InformalFormalCareByKinshipStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 40: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
   
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales'], linewidth = 3)
#        p2, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_1'], label = 'Class I')
#        p3, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_2'], label = 'Class II')
#        p4, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_3'], label = 'Class III')
#        p5, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_4'], label = 'Class IV')
#        p6, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care')
    ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Share of Informal Care supplied by Women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    # ax.set_ylim([0, 0.8])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareCareWomedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 41: informal care provided by gender per social class (mean of last 20 years)
    
    n_groups = p['numberClasses']
    informalCareMales_1 = np.mean(output['informalCareSuppliedByMales_1'][-20:])
    informalCareMales_2 = np.mean(output['informalCareSuppliedByMales_2'][-20:])
    informalCareMales_3 = np.mean(output['informalCareSuppliedByMales_3'][-20:])
    informalCareMales_4 = np.mean(output['informalCareSuppliedByMales_4'][-20:])
    informalCareMales_5 = np.mean(output['informalCareSuppliedByMales_5'][-20:])
    informalCareFemales_1 = np.mean(output['informalCareSuppliedByFemales_1'][-20:])
    informalCareFemales_2 = np.mean(output['informalCareSuppliedByFemales_2'][-20:])
    informalCareFemales_3 = np.mean(output['informalCareSuppliedByFemales_3'][-20:])
    informalCareFemales_4 = np.mean(output['informalCareSuppliedByFemales_4'][-20:])
    informalCareFemales_5 = np.mean(output['informalCareSuppliedByFemales_5'][-20:])
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
    ax.set_ylabel('Hours per week')
    ax.set_xlabel('Socio-Economic Classes')
    ax.set_title('Informal Care Supplied by Gender')
    ax.set_xticks(ind + bar_width/2)
    plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    fig.tight_layout()
    path = os.path.join(folder, 'InformalCareByGenderAndClassGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
     # Chart 42: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
   
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['ratioWage'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['ratioWage_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['ratioWage_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['ratioWage_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['ratioWage_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['ratioWage_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Wage Ratio')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Women and Men Wage Ratio')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenWageRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 43: income by gender per social class (mean of last 20 years)
           
    n_groups = p['numberClasses']
    WageMales_1 = np.mean(output['averageMalesWage_1'][-20:])
    WageMales_2 = np.mean(output['averageMalesWage_2'][-20:])
    WageMales_3 = np.mean(output['averageMalesWage_3'][-20:])
    WageMales_4 = np.mean(output['averageMalesWage_4'][-20:])
    WageMales_5 = np.mean(output['averageMalesWage_5'][-20:])
    WageFemales_1 = np.mean(output['averageFemalesWage_1'][-20:])
    WageFemales_2 = np.mean(output['averageFemalesWage_2'][-20:])
    WageFemales_3 = np.mean(output['averageFemalesWage_3'][-20:])
    WageFemales_4 = np.mean(output['averageFemalesWage_4'][-20:])
    WageFemales_5 = np.mean(output['averageFemalesWage_5'][-20:])
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
    path = os.path.join(folder, 'WageByGenderAndClassGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 44: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
   
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['ratioIncome'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['ratioIncome_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['ratioIncome_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['ratioIncome_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['ratioIncome_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['ratioIncome_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Income Ratio')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Women and Men Income Ratio')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenIncomeRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 45: income by gender per social class (mean of last 20 years)
    
    n_groups = p['numberClasses']
    incomeMales_1 = np.mean(output['averageMalesIncome_1'][-20:])
    incomeMales_2 = np.mean(output['averageMalesIncome_2'][-20:])
    incomeMales_3 = np.mean(output['averageMalesIncome_3'][-20:])
    incomeMales_4 = np.mean(output['averageMalesIncome_4'][-20:])
    incomeMales_5 = np.mean(output['averageMalesIncome_5'][-20:])
    incomeFemales_1 = np.mean(output['averageFemalesIncome_1'][-20:])
    incomeFemales_2 = np.mean(output['averageFemalesIncome_2'][-20:])
    incomeFemales_3 = np.mean(output['averageFemalesIncome_3'][-20:])
    incomeFemales_4 = np.mean(output['averageFemalesIncome_4'][-20:])
    incomeFemales_5 = np.mean(output['averageFemalesIncome_5'][-20:])
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
    path = os.path.join(folder, 'IncomeByGenderAndClassGroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ################################################################## 
    # Chart 46: Population by social class and number of taxpayers (1960-2020)
   
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['taxPayers'], linewidth = 3, label = 'Number of Taxpayers', color = 'yellow')
    ax.stackplot(output['year'], output['numUnskilled'], output['numSkilled'], output['numLowClass'],
                  output['numMidClass'], output['numUpClass'], 
                  labels = ['Unskilled Class (I)','Skilled Class (II)', 'Lower Class (III)', 'Middel Class (IV)', 'Upper Class (V)'])
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Hours of care')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Population and Number of Taxpayers')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PopulationTaxPayersStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 47: Average Household size (1960-2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['averageHouseholdSize_1'], label = 'Class I')
    p2, = ax.plot(output['year'], output['averageHouseholdSize_2'], label = 'Class II')
    p3, = ax.plot(output['year'], output['averageHouseholdSize_3'], label = 'Class III')
    p4, = ax.plot(output['year'], output['averageHouseholdSize_4'], label = 'Class IV')
    p5, = ax.plot(output['year'], output['averageHouseholdSize_5'], label = 'Class V')
    maxValue = max(output['averageHouseholdSize_1']+output['averageHouseholdSize_2']+output['averageHouseholdSize_3']+output['averageHouseholdSize_4']+output['averageHouseholdSize_5'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylim([0, maxValue*2.0])
    # ax.set_ylabel('Average Household Members')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Family Size')
    ax.set_ylim([0, 8])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageFamilySizeChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()         
             
##        pylab.plot(years,numMarriages)
##        pylab.ylabel('Number of marriages')
##        pylab.xlabel('Year')
##        pylab.savefig('numMarriages.pdf')
##
##        pylab.plot(years,numDivorces)
##        pylab.ylabel('Number of divorces')
##        pylab.xlabel('Year')
##        pylab.savefig('numDivorces.pdf')
    
    # Chart 48: Average Tax Burden (1960-2020)
   
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['taxBurden'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Care costs per taxpayer per year')
    # ax.set_xlabel('Year')
    ax.set_title('Average Tax Burden in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'TaxBurdenChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
  
    # total Tax Refund
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totalTaxRefund'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Tax Refund')
    # ax.set_xlabel('Year')
    ax.set_title('Total Tax Refund in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'totalTaxRefundChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
    
     # pension budget
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['pensionBudget'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Tax Refund')
    # ax.set_xlabel('Year')
    ax.set_title('Budget balance in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'pensionBudgetChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
    
    # Chart 49: Proportion of married adult women (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['marriageProp'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Proportion of married adult women')
    ax.set_title('Proportion of married adult women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'MarriageRateChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 49: Proportion of lone parents (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareLoneParents'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Proportion of married adult women')
    ax.set_title('Share of lone parents')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'LoneParentsShareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 50: Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['hospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    ax.set_title('Total Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'TotalHealthCareCostChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 51: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['perCapitaHospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    ax.set_title('Per Capita Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaHealthCareCostChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 52: Gini Coefficient of Unmet Social Care (from 1960 to 2020)
  
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Gini Coefficient')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Unmet Social Care Gini Coeffcient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0.5, 1.0)
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'UnmetSocialCareGiniCoefficientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 53: Gini Coefficient of Share of Unmet Social Care (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Gini Coefficient')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Unmet Social Care Gini Coeffcient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0.5, 1.0)
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetSocialCareGiniCoefficientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 54: Public supply
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['publicSupply'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Public Social Care Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PublicSocialCareSupplyChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
  
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['costDirectFunding'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Cost of Public Social Care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CostDirectFundingChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # care credit charts 
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['socialCareCredits'], linewidth = 3, label = 'Total Social Credit')
    p2, = ax.plot(output['year'], output['careCreditSupply'], linewidth = 3, label = 'Public Social Care Supply')
    p3, = ax.plot(output['year'], output['socialCreditSpent'], linewidth = 3, label = 'Social Credit Transferred')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    # ax.legend_.remove()
    ax.set_title('Credit Public Care Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CreditPublicSocialCareSupplyChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareCreditsSpent'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of total credit')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Share of Social Credit Transferred')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareSocialCreditTransferChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['careCreditCost'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Cost of Credit Public Social Care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CostCreditSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 55: Aggregate QALY
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totQALY'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('QALY Index')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Aggregate QALY Index')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AggregateQALYChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
     # Chart 56: Average QALY
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['meanQALY'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('QALY Index')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Average QALY Index')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageQALYChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
#        qualityAdjustedLifeYears_M.append(np.mean(discountedQALY[-20:]))
#        qualityAdjustedLifeYears_SD.append(np.std(discountedQALY[-20:]))
#        
#        perCapitaQualityAdjustedLifeYears_M.append(np.mean(averageDiscountedQALY[-20:]))
#        perCapitaQualityAdjustedLifeYears_SD.append(np.std(averageDiscountedQALY[-20:]))

    # Chart 57: Ratio of Unmet Care Need and Total Supply (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of total supply')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Ratio of Unmet Care Need and Total Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'RatioUnmetCareNeedTotalSupply.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
noPolicySim = True
rootFolder = 'C:/Users/Umberto Gostoli/SPHSU/Social Care Model II'
#rootFolder = 'N:/Social Care Model III'

doGraphs(policyOnlySim)