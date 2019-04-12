# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 15:45:43 2019

@author: ug4d
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
from collections import OrderedDict
import pandas as pd


def doGraphs(graphsParams, metaParams):
    
    folder = graphsParams[0]
    numRepeats = graphsParams[2]
    numScenarios = graphsParams[3]
    numPolicies = graphsParams[4]
    
    simFolder = 'Simulations_Folder/' + folder
    
   
    
    multipleRepeatsDF = []
    for repeatID in range(numRepeats):
        repFolder = simFolder + '/Rep_' + str(repeatID)
        multipleScenariosDF = []
        for scenarioID in range(numScenarios):
            scenarioFolder = repFolder + '/Scenario_' + str(scenarioID)
            multiplePoliciesDF = []
            for policyID in range(numPolicies):
                policyFolder = scenarioFolder + '/Policy_' + str(policyID)
                outputsDF = pd.read_csv(policyFolder + '/Outputs.csv', sep=',', header=0)
                singlePolicyGraphs(outputsDF, policyFolder, metaParams)
                multiplePoliciesDF.append(outputsDF)
            if numPolicies > 1:
                multiplePoliciesGraphs(multiplePoliciesDF, scenarioFolder, metaParams, numPolicies)
            multipleScenariosDF.append(multiplePoliciesDF)
        if numScenarios > 1:
            multipleScenariosGraphs(multipleScenariosDF, repFolder, metaParams, numPolicies, numScenarios)
        multipleRepeatsDF.append(multipleScenariosDF)
    if numRepeats > 1:
        multipleRepeatsGraphs(multipleRepeatsDF, simFolder, metaParams, numPolicies, numScenarios, numRepeats)
    
    
def singlePolicyGraphs(output, policyFolder, p):
    
    folder = policyFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    policyYears = int((p['endYear']-p['implementPoliciesFromYear']) + 1)
    
    # Fig. 1: Met social care needs by kind and unmet social care need (hours per week)
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
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Figure 2: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0, 25)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 3: informal and formal social care received and unmet social care need by care need level
    n_groups = p['numCareLevels']-1
    meanInformalCareReceived_1 = np.mean(output['meanInformalSocialCareReceived_N1'][-policyYears:])
    meanFormalCareReceived_1 = np.mean(output['meanFormalSocialCareReceived_N1'][-policyYears:])
    meanUnmetNeed_1 = np.mean(output['meanUnmetSocialCareNeed_N1'][-policyYears:])
    meanInformalCareReceived_2 = np.mean(output['meanInformalSocialCareReceived_N2'][-policyYears:])
    meanFormalCareReceived_2 = np.mean(output['meanFormalSocialCareReceived_N2'][-policyYears:])
    meanUnmetNeed_2 = np.mean(output['meanUnmetSocialCareNeed_N2'][-policyYears:])
    meanInformalCareReceived_3 = np.mean(output['meanInformalSocialCareReceived_N3'][-policyYears:])
    meanFormalCareReceived_3 = np.mean(output['meanFormalSocialCareReceived_N3'][-policyYears:])
    meanUnmetNeed_3 = np.mean(output['meanUnmetSocialCareNeed_N3'][-policyYears:])
    meanInformalCareReceived_4 = np.mean(output['meanInformalSocialCareReceived_N4'][-policyYears:])
    meanFormalCareReceived_4 = np.mean(output['meanFormalSocialCareReceived_N4'][-policyYears:])
    meanUnmetNeed_4 = np.mean(output['meanUnmetSocialCareNeed_N4'][-policyYears:])
    informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                    meanInformalCareReceived_4)
    formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                  meanFormalCareReceived_4)
    sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
    unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4)
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
    p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
    p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('NL 1', 'NL 2', 'NL 3', 'NL 4'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal, Formal and Unmet Social Care by Care Need Level')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCarePerRecipientByNeedLevelStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 4: Hours of informal and formal social care and unmet social care need per recipient by SES
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalSocialCarePerRecipient_1'][-policyYears:])
    meanFormalCareReceived_1 = np.mean(output['formalSocialCarePerRecipient_1'][-policyYears:])
    meanUnmetNeed_1 = np.mean(output['unmetSocialCarePerRecipient_1'][-policyYears:])
    meanInformalCareReceived_2 = np.mean(output['informalSocialCarePerRecipient_2'][-policyYears:])
    meanFormalCareReceived_2 = np.mean(output['formalSocialCarePerRecipient_2'][-policyYears:])
    meanUnmetNeed_2 = np.mean(output['unmetSocialCarePerRecipient_2'][-policyYears:])
    meanInformalCareReceived_3 = np.mean(output['informalSocialCarePerRecipient_3'][-policyYears:])
    meanFormalCareReceived_3 = np.mean(output['formalSocialCarePerRecipient_3'][-policyYears:])
    meanUnmetNeed_3 = np.mean(output['unmetSocialCarePerRecipient_3'][-policyYears:])
    meanInformalCareReceived_4 = np.mean(output['informalSocialCarePerRecipient_4'][-policyYears:])
    meanFormalCareReceived_4 = np.mean(output['formalSocialCarePerRecipient_4'][-policyYears:])
    meanUnmetNeed_4 = np.mean(output['unmetSocialCarePerRecipient_4'][-policyYears:])
    meanInformalCareReceived_5 = np.mean(output['informalSocialCarePerRecipient_5'][-policyYears:])
    meanFormalCareReceived_5 = np.mean(output['formalSocialCarePerRecipient_5'][-policyYears:])
    meanUnmetNeed_5 = np.mean(output['unmetSocialCarePerRecipient_5'][-policyYears:])
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
    
    # Fig. 5: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care')
    ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    # ax.legend_.remove()
    ax.set_title('Share of Informal Care supplied by Women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    # ax.set_ylim([0, 0.8])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareCareWomedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 6: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
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
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenIncomeRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 7: informal and formal care supplied by kinship network distance (mean of last 20 years) # Modified y lim
    n_groups = 4
    meanInformalCareHousehold = np.mean(output['sumNoK_informalSupplies[0]'][-policyYears:])
    meanFormalCareHousehold = np.mean(output['sumNoK_formalSupplies[0]'][-policyYears:])
    meanInformalCare_K1 = np.mean(output['sumNoK_informalSupplies[1]'][-policyYears:])
    meanFormalCare_K1 = np.mean(output['sumNoK_formalSupplies[1]'][-policyYears:])
    meanInformalCare_K2 = np.mean(output['sumNoK_informalSupplies[2]'][-policyYears:])
    meanFormalCare_K2 = np.mean(output['sumNoK_formalSupplies[2]'][-policyYears:])
    meanInformalCare_K3 = np.mean(output['sumNoK_informalSupplies[3]'][-policyYears:])
    meanFormalCare_K3 = np.mean(output['sumNoK_formalSupplies[3]'][-policyYears:])
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
    
    # Fig. 8: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['perCapitaHospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    ax.set_title('Per Capita Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaHealthCareCostChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['sharePublicSocialCare'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of Total Care')
    # ax.set_xlabel('Year')
    ax.set_title('Public share of social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'sharePublicSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['costPublicSocialCare'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    # ax.set_xlabel('Year')
    ax.set_title('Cost of public social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'costPublicSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    

def multiplePoliciesGraphs(output, scenarioFolder, p, numPolicies):
    
    folder = scenarioFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    
    policyYears = (p['endYear']-p['implementPoliciesFromYear']) + 1
    
    # Add graphs across policies (within the same run/scenario)
    
    #############################  Population   #######################################
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        graph.append(ax.plot(output[i]['year'], output[i]['currentPop'], label = 'Policy ' + str(i)))
    ax.set_title('Populations')
    ax.set_ylabel('Number of people')
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
    ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
    fig.tight_layout()
    path = os.path.join(folder, 'popGrowth_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

    ########################### Share of Umnet Care Needs    #################################
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(outputs[i]['unmetSocialCareNeed'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hours of Unmet Care')
    ax.set_title('Total Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalUnmetCareNeedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 10: bar chart of direct policy costs (net of tax revenue changes)
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        totalCost = np.sum(outputs[i]['costPublicSocialCare'][-policyYears:]) + np.sum(outputs[i]['totalTaxRefund'][-policyYears:])
        shareUnmetCareDemand.append(totalCost)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.set_title('Total Policy Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalPolicyCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 11: bar chart of ICER
    fig, ax = plt.subplots()
    objects = ('Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    benchmarkRevenue = np.sum(outputs[0]['taxRevenue'][-policyYears:])
    benchmarkCost = np.sum(outputs[0]['costPublicSocialCare'][-policyYears:]) + np.sum(outputs[0]['totalTaxRefund'][-policyYears:])
    benchmarkBudget = benchmarkRevenue - benchmarkCost
    benchmarkUnmetCareNeed = np.sum(outputs[0]['unmetSocialCareNeed'][-policyYears:])
    for i in range(1, numPolicies):
        policyRevenue = np.sum(outputs[i]['taxRevenue'][-policyYears:])
        policyCost = np.sum(outputs[i]['costPublicSocialCare'][-policyYears:]) + np.sum(outputs[i]['totalTaxRefund'][-policyYears:])
        policyBudget = policyRevenue - policyCost
        policyUnmetCareNeed = np.sum(outputs[i]['unmetSocialCareNeed'][-policyYears:])
        icer = (benchmarkBudget-policyBudget)/(benchmarkUnmetCareNeed-policyUnmetCareNeed)
        shareUnmetCareDemand.append(icer)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per hour')
    ax.set_title('ICER')
    fig.tight_layout()
    path = os.path.join(folder, 'ICERB.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 12: bar chart of hospitalization costs
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(outputs[i]['hospitalizationCost'][-policyYears:])/52.0)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.set_title('Total Hospitalization Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalHospitalizationCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
   
   
def multipleScenariosGraphs(output, repFolder, p, numPolicies, numScenarios):
    
    folder = repFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    scenarios = []
    for i in range(numScenarios):
        scenarios.append('Scenario ' + str(i+1))
        
    # Add graphs across scenarios (for the same policies)
    for j in range(numPolicies):
        
        # Plots of values in the period 1990-2040, for each scenario (single run)
        fig, ax = plt.subplots() # Argument: figsize=(5, 3)
        graph = []
        for i in range(numScenarios):
            graph.append(ax.plot(output[i][j]['year'], output[i][j]['currentPop'], label = 'Scenario ' + str(i+1)))
        # p2, = ax.plot(output[1][0]['year'], output[1]['currentPop'], color="blue", label = 'Policy 1')
        ax.set_title('Populations - P' + str(j))
        ax.set_ylabel('Number of people')
        handels, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower right')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
        ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
        fig.tight_layout()
        path = os.path.join(folder, 'popGrowth_axScen_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Bar Charts of mean values in the period 2025-2035, for each sceanario (single run)
        meansOutput = []
        sdOutput = []
        for i in range(numScenarios):
            policyWindow = []
            for yearOutput in range(2025, 2036, 1):
                policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
            meansOutput.append(np.mean(policyWindow))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(scenarios))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios)
        ax.set_title('Unmet Social Care (mean 2025-2035) - P' + str(j))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
    
    

def multipleRepeatsGraphs(output, simFolder, p, numRepeats, numPolicies, numScenarios):
    
    folder = simFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    

    # Add graphs across runs (for the same scenario/policy combinations)
    # For each policy scenario, take the average of year 2010-2020 for each run, and do a bar chart with error bars for each outcome of interest
    
    # Policy comparison: make charts by outcomes with bars representing the different policies.
    
    
    # Graphs to compare policies across scenarios
    policies = ['Benchmark', 'Policy 1', 'Policy 2']
    
    for i in range(numScenarios):
        
        scenarioFolder = folder + '/Scenario ' + str(i+1)
        if not os.path.exists(scenarioFolder):
            os.makedirs(scenarioFolder)
        
        # Unmet Social Care: mean and sd across the n repeats for the 5 policies.
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Unmet Social Care (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Hospitalization Costs
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'hospitalizationCost'].values[0]/52.0)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per week')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Hospitalization Costs (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'hospitalizationCosts_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Framework for cost graphs
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    psc = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    tr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    policyWindow.append(psc+tr)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per week')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Direct Policy Cost (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'directPolicyCost_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Framework for ICER graphs
        newPolicies = policies[1:]
        meansOutput = []
        sdOutput = []
        for j in range(1, numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    ptr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'taxRevenue'].values[0]
                    pdc = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    pr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    policyBudget = ptr-(pdc+pr)
                    btr = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'taxRevenue'].values[0]
                    bdc = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    br = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    benchmarkBudget = btr-(bdc+br)
                    deltaBudget = benchmarkBudget-policyBudget
                    hourUnmetCarePolicy = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0]
                    hourUnmetCareBenchmark = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0]
                    deltaCare = hourUnmetCareBenchmark-hourUnmetCarePolicy
                    policyWindow.append(deltaBudget/deltaCare)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(newPolicies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per hour')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(newPolicies)
        ax.set_title('Direct Cost ICER (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
        
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'directICER_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
    # Graphs to compare scenarios across policies
    scenarios = []
    for i in range(numScenarios):
        scenarios.append('Scenario ' + str(i+1))
        
    for j in range(numPolicies):
        
        scenarioFolder = folder + '/Policy ' + str(j)
        if not os.path.exists(scenarioFolder):
            os.makedirs(scenarioFolder)
            
        # Share of Unmet Social Care: mean and sd across the n repeats for the 5 policies.
        meansOutput = []
        sdOutput = []
        for i in range(numScenarios):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(scenarios))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios)
        ax.set_title('Unmet Social Care (mean 2025-2035) - P' + str(j))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
    
    
    
    
    
    
    # Add graphs across runs (for the same scenario/policy combinations)
    # For each policy scenario, take the average of year 2010-2020 for each run, and do a bar chart with error bars for each outcome of interest
    
    # Policy comparison: make charts by outcomes with bars representing the different policies.
    
    for j in range(numPolicies):
        for i in range(numScenarios):
            fig, ax = plt.subplots() # Argument: figsize=(5, 3)
            graph = []
            for z in range(numRepeats):
                graph.append(ax.plot(output[z][i][j]['year'], output[z][i][j]['currentPop'], label = 'Run ' + str(z+1)))
            ax.set_title('Populations - ' + 'Scenario ' + str(i+1) + '/Policy ' + str(j))
            ax.set_ylabel('Number of people')
            handels, labels = ax.get_legend_handles_labels()
            ax.legend(loc = 'lower right')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
            ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
            fig.tight_layout()
            path = os.path.join(folder, 'popGrowth_axRep_S' + str(i+1) + '_P' + str(j) + '.pdf')
            pp = PdfPages(path)
            pp.savefig(fig)
            pp.close()
            
    for j in range(numPolicies):
        for i in range(numScenarios):
            fig, ax = plt.subplots() # Argument: figsize=(5, 3)
            graph = []
            for z in range(numRepeats):
                graph.append(ax.plot(output[z][i][j]['year'], output[z][i][j]['unmetSocialCareNeed'], label = 'Run ' + str(z+1)))
            ax.set_title('Unmet Care Needs - ' + 'Scenario ' + str(i+1) + '/Policy ' + str(j))
            ax.set_ylabel('Unmet Care Needs (h/w)')
            handels, labels = ax.get_legend_handles_labels()
            ax.legend(loc = 'lower right')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
            ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
            fig.tight_layout()
            path = os.path.join(folder, 'unmetCareNeeds_axRep_S' + str(i+1) + '_P' + str(j) + '.pdf')
            pp = PdfPages(path)
            pp.savefig(fig)
            pp.close()



mP = pd.read_csv('defaultParameters.csv', sep=',', header=0)
numberRows = mP.shape[0]
keys = list(mP.columns.values)
values = []
for column in mP:
    colValues = []
    for i in range(numberRows):
        if pd.isnull(mP.loc[i, column]):
            break
        colValues.append(mP[column][i])
    values.append(colValues)
metaParams = OrderedDict(zip(keys, values))
for key, value in metaParams.iteritems():
    if len(value) < 2:
        metaParams[key] = value[0]
        
graphsParams = pd.read_csv('graphsParams.csv', sep=',', header=0)
dummy = list(graphsParams['doGraphs'])
for i in range(len(dummy)):
    if dummy[i] == 1:
        doGraphs(graphsParams.loc[i], metaParams)

        

