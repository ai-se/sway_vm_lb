#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


from __future__ import division

import glob

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import rename_files

ifs = glob.glob('../results/objCmpr/' + '*.txt')

for f in ifs:
    model_name = f.split('/')[-1][4:-4]
    records = list()
    with open(f, 'r') as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            if len(data) == 1:
                continue
            o0, o1 = float(data[1]), float(data[2])
            O0, O1 = float(data[4]), float(data[5])
            # records.append([math.ceil(o0 / 3600), math.ceil(O0 / 3600), o1, O1])
            records.append([o0, O0, o1, O1])

    df = pd.DataFrame(records, columns=['g0', 'a0', 'g1', 'a1'])

    o0range = max(max(df['g0']), max(df['a0'])) - min(min(df['g0']), min(df['a0']))
    o1range = max(max(df['g1']), max(df['a1'])) - min(min(df['g1']), min(df['a1']))

    df['delta0'] = (df['g0'] - df['a0']) / o0range  # /o0range
    df['delta1'] = (df['g1'] - df['a1']) / o1range

    errors = [i + j for i, j in zip(df['delta0'], df['delta1'])]
    errors = [i for i in errors if i != 0]

    plt.clf()
    plt.figure(figsize=(0.8, 0.8), dpi=200)
    matplotlib.rcParams.update({'font.size': 5.0})
    matplotlib.rc('axes', edgecolor='gray')

    frame1 = plt.gca()
    n_bins = 100
    n, bins, patches = plt.hist(errors, bins=n_bins, alpha=0.7)
    frame1.get_yaxis().set_visible(False)
    frame1.set_xlim([-0.9, 0.9])
    plt.xticks(np.array([-0.25, 0, 0.25]))
    vals = frame1.get_xticks()
    frame1.set_xticklabels(['' for x in vals])
    simple_model_name = model_name[0] + '.' + model_name.split('_')[1]
    # plt.title(simple_model_name)
    # showing the 80% data
    n_l = len(errors)
    r = -1
    for i in range(0, 100, 5):
        r = float(i) / 100
        if len([q for q in errors if -r < q < r]) > 0.75 * n_l:
            break

    for b, thispatch in zip(bins, patches):
        if -r < b < r:
            thispatch.set_facecolor('green')
        else:
            thispatch.set_facecolor('gray')

    plt.text(-0.85, plt.ylim()[1]*0.9, simple_model_name, fontdict={'weight': 'bold', 'size': 5.3})

    plt.tight_layout()
    # plt.show()
    plt.savefig('../results/objCmprImg2/' + model_name + '.eps')
rename_files('../results/objCmprImg2/', fileExtension='eps')

#
# plt.figure(figsize=(8, 8))
# ax = plt.gca()
#
# # plot scatters
# plt.xlim(-1, 1)
# plt.ylim(-1, 1)
# ax.scatter(x=df['delta0'], y=df['delta1'], s=0.2)
#
# # zoom in the center part
# axins = zoomed_inset_axes(ax, zoom=1.15, loc=1)
# axins.scatter(x=df['delta0'], y=df['delta1'], s=0.2)
# axins.set_xlim(-0.25, 0.25)
# axins.set_ylim(-0.25, 0.25)
# axins.axes.get_yaxis().set_visible(False)
#
# axins2 = zoomed_inset_axes(ax, zoom=2, loc=9)
# axins2.scatter(x=df['delta0'], y=df['delta1'], s=0.2)
# axins2.set_xlim(-0.1, 0.1)
# axins2.set_ylim(-0.1, 0.1)
# axins2.axes.get_xaxis().set_visible(False)
#
# mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
# mark_inset(axins, axins2, loc1=1, loc2=3, fc="none", ec="0.5")
#
# # print model name
# ax.text(-0.3, 1.1, model_name, fontsize=10)
#
# # print ratios between +-25%
# case_in_total = df.shape[0]
# center_count = df[(abs(df.delta0) < 0.25) & (abs(df.delta1) < 0.25)].shape[0]
# center_count2 = df[(abs(df.delta0) < 0.1) & (abs(df.delta1) < 0.1)].shape[0]
#
# # ax.text(0.3, -0.6, "Error in [+-0.25]^2 = %d/%d = %.2f%%" % (
# #     center_count, case_in_total, center_count / case_in_total * 100), fontsize=9, color='r')
# ax.text(0.75, -0.75, "100%", color='r')
# axins.text(0.15, -0.15, str(int(center_count / case_in_total * 100)) + '%', color='r')
# axins2.text(0.06, -0.08, str(int(center_count2 / case_in_total * 100)) + '%', color='r')

# pdb.set_trace()
# plt.show()
# plt.savefig('../results/objCmprImg/' + model_name + '.png')
