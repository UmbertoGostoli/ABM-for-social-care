# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:46:24 2018

@author: ug4d
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
import pandas as pd

def init_params():
    """Set up the simulation parameters."""
    p = {}
    
    p['endYear'] = 2040
    p['statsCollectFrom'] = 1990
    p['numberPolicyParameters'] = 4
    p['numberScenarios'] = 9
    p['implementPoliciesFromYear'] = 2020
    p['discountingFactor'] = 0.03
    
    return p

p = init_params()

def createSensitivityGraphs(folder, numPolicies):
    
    p = init_params()
    
    outputs = []
    for r in range(numPolicies):
        repFolder = 'N:/Social Care Model III/Charts/SocPolicy_Sim/Policy_' + str(r)
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

folder  = 'N:/Social Care Model III/Charts/SensitivityCharts'
if not os.path.isdir(os.path.dirname(folder)):
    os.makedirs(folder)

createSensitivityGraphs(folder, p['numberScenarios'])