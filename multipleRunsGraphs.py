# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:34:41 2018

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
    
    p['endYear'] = 1940 # 2040
    p['statsCollectFrom'] = 1900 # 1990
    p['implementPoliciesFromYear'] = 1920
    p['numRepeats'] = 4
    
    return p

p = init_params()

def createRunsGraphs(folder, repeats):
    
    outputs = []
    for r in range(repeats):
        repFolder = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model II\Charts\NoPolicy_Sim\Repeat_' + str(r)
        filename = repFolder + '\Outputs.csv'
        output = pd.read_csv(filename, sep=',',header=0)
        outputs.append(output)

    fig, ax = plt.subplots()
    chart = [None]*repeats
    for i in range(repeats):
        if repeats > 1:
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
    filename = folder + '/PerCapitaHospitalizationCostsChart_MR.pdf'
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    
    
folder  = 'C:\Users\Umberto Gostoli\SPHSU\Social Care Model II\Charts\MultipleRunsCharts'
            
if not os.path.isdir(os.path.dirname(folder)):
    os.makedirs(folder)
    
createRunsGraphs(folder, p['numRepeats'])