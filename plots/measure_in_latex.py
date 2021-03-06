#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, Jianfeng Chen <jchen37@ncsu.edu>
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


from __future__ import division, print_function
from lxml import etree
import xml.etree.ElementTree as ET
import numpy
import sys
from scipy.stats import ttest_ind
import scipy
import pdb

modelref = ['Montage', 'Epigenomics', 'Inspiral', 'CyberShake', 'Sipht']


def median(lst):
    return numpy.median(numpy.array(lst))


def get_data_by_tag(tag):
    tree = ET.parse('../results/combined/reports.xml')
    subtree = filter(lambda t: t.tag == tag, tree.getroot().getchildren())[0]
    return subtree


def _change_sec_to_hour(s):
    if s == 'N/A':
        return s
    if int(s) < 1500:
        return s
    return '%.1fH' % (int(s) / 3600)


def get_runtime_csv():
    algorithms = ['RIOT', 'MOHEFT', 'EMSC-NSGAII', 'EMSC-SPEA2', 'EMSC-MOEA/D']

    # f1 = open('../results/combined/runtime.csv', 'w+')
    f1 = sys.stdout
    data = get_data_by_tag("runtimes")
    MK = get_data_by_tag("makespans")
    models = [i.get('name') for i in data.getchildren()]
    models = sorted(models, key=lambda n: (modelref.index(n.split('_')[0]), int(n.split('_')[1])))
    # header = ['model'] + algorithms
    # print(','.join(header), file=f1)

    for model in models:
        d = [i for i in data.getchildren() if i.get('name') == model][0]
        dd = [i for i in MK.getchildren() if i.get('name') == model][0]
        times = list()
        makespans = list()

        for alg in algorithms:
            time = [i for i in d.getchildren() if i.get('alg') == alg][0].get('algRunTime').split(' ')
            sub_makespans = [i for i in dd.getchildren() if i.get('alg') == alg][0].get('makespan').split(' ')

            if '' not in sub_makespans:
                sub_makespans = [float(i) for i in sub_makespans]
                makespans.extend(sub_makespans)

            if '' in time:
                times.append('N/A')
            else:
                time = [int(i) for i in time]
                times.append((max(time)))

        if times[0] == 0:
            times[0] = 1
        times.append(int(min(times[1:]) / times[0]))

        times = [str(i) for i in times]
        times = map(_change_sec_to_hour, times)

        makespans = sorted(makespans)[: int(len(makespans) * 0.6)]  # .6
        makespan = str(int(numpy.median(makespans)))
        makespan = _change_sec_to_hour(makespan)

        simple_model_name = model[0] + '.' + model.split('_')[1]
        print(' & '.join([simple_model_name] + [makespan] + times) + '\\\\', file=f1)
        if models.index(model) % 4 == 3 and models.index(model) != 19:
            print('\\hline', file=f1)


def get_hv_csv():
    f1 = open('../results/combined/hv.csv', 'w+')
    data = get_data_by_tag("hypervolumes")
    models = [i.get('name') for i in data.getchildren()]
    models = sorted(models, key=lambda n: (n.split('_')[0], int(n.split('_')[1])))

    header = ['model'] + algorithms
    print(','.join(header), file=f1)

    for model in models:
        d = [i for i in data.getchildren() if i.get('name') == model][0]
        times = list()
        for alg in algorithms:
            time = [i for i in d.getchildren() if i.get('alg') == alg][0].get('hypervolume').split(' ')
            if len(time) == 0 or (float(time[0]) < 0.2 and alg == 'MOHEFT'):
                times.append('N/A')
            else:
                time = [float(i) for i in time]
                times.append(str(median(time)))
        print(','.join([model] + times), file=f1)


def get_spread_csv():
    f1 = open('../results/combined/spread.csv', 'w+')
    data = get_data_by_tag("spreads")
    models = [i.get('name') for i in data.getchildren()]
    models = sorted(models, key=lambda n: (n.split('_')[0], int(n.split('_')[1])))

    header = ['model'] + algorithms
    print(','.join(header), file=f1)

    for model in models:
        d = [i for i in data.getchildren() if i.get('name') == model][0]
        times = list()
        for alg in algorithms:
            time = [i for i in d.getchildren() if i.get('alg') == alg][0].get('spread').split(' ')
            if len(time) == 0 or (float(time[0]) < 0.1 and alg == 'MOHEFT'):
                times.append('N/A')
            else:
                time = [float(i) for i in time]
                times.append(str(median(time)))
        print(','.join([model] + times), file=f1)


def get_igd_csv():
    f1 = open('../results/combined/igd.csv', 'w+')
    data = get_data_by_tag("igds")
    models = [i.get('name') for i in data.getchildren()]
    models = sorted(models, key=lambda n: (n.split('_')[0], int(n.split('_')[1])))

    header = ['model'] + algorithms
    print(','.join(header), file=f1)

    for model in models:
        d = [i for i in data.getchildren() if i.get('name') == model][0]
        times = list()
        for alg in algorithms:
            time = [i for i in d.getchildren() if i.get('alg') == alg][0].get('igd').split(' ')
            if len(time) == 0 or (float(time[0]) > 1 and alg == 'MOHEFT'):
                times.append('N/A')
            else:
                time = [float(i) for i in time]
                times.append(str(median(time)))
        print(','.join([model] + times), file=f1)


def wilconTest(x, y):
    # if len(x) < 5 or len(y) < 5 or len(x) != len(y):
    avg1 = sum(x) / len(x)
    avg2 = sum(y) / len(y)
    if avg1 > avg2:
        avg1, avg2 = avg2, avg1
    return avg2 / avg1 > 1.05

    # return scipy.stats.wilcoxon(x, y)[1] > 0.05


def results_in_latex():
    algorithms = ['RIOT', 'MOHEFT', 'EMSC-NSGAII', 'EMSC-SPEA2', 'EMSC-MOEA/D', 'RAND']
    hv_data = get_data_by_tag("hypervolumes")
    igd_data = get_data_by_tag("igds")
    spread_data = get_data_by_tag("spreads")

    models = [i.get('name') for i in hv_data.getchildren()]
    models = sorted(models, key=lambda n: (modelref.index(n.split('_')[0]), int(n.split('_')[1])))

    for model in models:
        unforn1 = False
        unforn3 = False
        unforn2 = False

        # hvs
        d = [i for i in hv_data.getchildren() if i.get('name') == model][0]
        hvr = list()
        for alg in algorithms:
            hvx = [i for i in d.getchildren() if i.get('alg') == alg][0].get('hypervolume').split(' ')
            hvx = [float(i) for i in hvx]
            hvr.append(median(hvx))
            if alg == 'RIOT':
                q75, q25 = numpy.percentile(hvx, [75, 25])
                iqrh = q75 - q25
                iqrh = max(iqrh, .01)
                iqrh = ('%d' % (iqrh * 100))

        if hvr[0] / (sum(hvr[2:5]) / 3) < 0.95:
            unforn1 = True

        if hvr[-1] < 0.1:
            hvr[-1] = 0.1
        hvr = [str(int(i * 100)) for i in hvr]

        # igds
        d = [i for i in igd_data.getchildren() if i.get('name') == model][0]
        ir = list()
        for alg in algorithms:
            ix = [i for i in d.getchildren() if i.get('alg') == alg][0].get('igd').split(' ')
            ix = [float(i) for i in ix]
            ir.append(median(ix))
            if alg == 'RIOT':
                q75, q25 = numpy.percentile(ix, [75, 25])
                iqri = q75 - q25
                iqri = max(iqri, .01)
                iqri = ('%d' % (iqri * 100))

        if ir[0] / (sum(ir[2:5]) / 3) > 1.15:
            unforn3 = True

        ir = [str(int(i * 100)) for i in ir]

        # spreads
        d = [i for i in spread_data.getchildren() if i.get('name') == model][0]
        spr = list()
        for alg in algorithms[:-1]:
            spx = [i for i in d.getchildren() if i.get('alg') == alg][0].get('spread').split(' ')
            spx = [float(i) for i in spx]
            spr.append(median(spx))

            if alg == 'RIOT':
                q75, q25 = numpy.percentile(spr, [75, 25])
                iqrs = q75 - q25
                iqrs = max(iqrs, .01)
                iqrs = ('%d' % (iqrs * 100))

        if spr[0] / (sum(spr[2:5]) / 3) > 1.15:
            unforn2 = True

        spr = [str(int(i * 100)) if i > 0 else '~{\it n.a.}' for i in spr]

        simple_model_name = model[0] + '.' + model.split('_')[1]
        printseq = [model.replace('_', ' '),
                    '\\s' + ('s' if unforn1 else '') + 'val{%s}{%s}' % (hvr[0], iqrh), hvr[1], hvr[2], hvr[3], hvr[4],
                    hvr[5],
                    '\\s' + ('s' if unforn3 else '') + 'val{%s}{%s}' % (ir[0], iqri), ir[1], ir[2], ir[3], ir[4], ir[5],
                    '\\s' + ('s' if unforn2 else '') + 'val{%s}{%s}' % (spr[0], iqrs), spr[1], spr[2], spr[3], spr[4]
                    ]

        print(' & '.join(printseq) + '\\\\')
        if models.index(model) % 4 == 3:
            print('\\hline')


if __name__ == '__main__':
    # get_runtime_csv()
    results_in_latex()
