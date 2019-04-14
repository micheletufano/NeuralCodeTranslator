#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:40:56 2018

@author: cawatson
"""

import sys
import numpy

buggy_file = open(sys.argv[1], 'r')
fixed_file = open(sys.argv[2], 'r')
prediction_file = open(sys.argv[3], 'r')

perfect_predictions = 0
bad_predictions = 0
all_bad_predictions = 0
all_potential_predictions = 0
potential_predictions = []

for line in buggy_file:
    
    buggy_line = line.strip()
    fixed_line = fixed_file.readline().strip()
    prediction_lines = prediction_file.readline().split(" <SEP> ")
    for i in range(len(prediction_lines)):
        prediction_lines[i] = prediction_lines[i].strip()
    
    perfect_pred = False
    count_potential = 0
    count_same = 0
    
    for i in range(len(prediction_lines)):
        if(prediction_lines[i] == fixed_line):
            perfect_pred = True
        elif(prediction_lines[i] != buggy_line):
            count_potential += 1
        elif(prediction_lines[i] == buggy_line):
            count_same += 1
            all_bad_predictions += 1
        else:
            sys.exit("BAD CLASSIFICATION")
            
            
    if(perfect_pred == True):
        perfect_predictions += 1
    if(count_same == len(prediction_lines)):
        bad_predictions += 1
    potential_predictions.append(count_potential)
    
potential_predictions_avg = numpy.average(numpy.asarray(potential_predictions))
all_potential_predictions = numpy.sum(numpy.asarray(potential_predictions))    

sys.exit((str(perfect_predictions) + " " + str(all_potential_predictions) + " " + str(all_bad_predictions) + " " + str(potential_predictions_avg) + " " + str(bad_predictions)))
        
