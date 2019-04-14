#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 17:39:42 2018

@author: mtufano
"""

import numpy as np
import sys

def get_word(pred):
    vword = vocab[pred];
    return vword.split('\t', 1)[0]



path = sys.argv[1]

output_file_together = open((path + '/predictions.beam.mul.txt'), 'w')
output_file_separate = open((path + '/predictions.beam.vis.txt'), 'w')

#Load vocabulary
vocab = None
with open((path + '/vocab.fixed.txt')) as file:
    vocab = file.readlines()
vocab = [_.strip() for _ in vocab]
vocab += ["UNK", "SEQUENCE_START", "SEQUENCE_END"]


#Load files (TODO replace these lines and simply load the entire .npz file)
data = np.load((path + '/beams.npz'))
pred = data['predicted_ids']
parents = data['beam_parent_ids']

num_pred = len(pred)

print('Predictions:', num_pred)


for idx in range(num_pred):
    predicted_ids = pred[idx] #gives the predicted ids for the idx-th input sentence
    parents_ids = parents[idx] # give the array of parent ids
    seq_length = predicted_ids.shape[0]
    beam_size = predicted_ids.shape[1]


    output = [["" for x in range(seq_length)] for y in range(beam_size)]
    last_parent = parents_ids[seq_length-1]
    aliases = parents_ids[seq_length-1]


    for level in range(seq_length-1,-1,-1):
        word_ids = [pred for pred in predicted_ids[level]]
        
        #Fill the output sentences
        for i in range(beam_size):

            #Get the alias index for the i-th output sentence.
            out_id = aliases[i];

            #Get the word            
            output[i][level] = get_word(word_ids[last_parent[out_id]])

        
        #Update aliases and parents
        for al_id in range(len(aliases)):
            aliases[al_id] = last_parent[aliases[al_id]]        
        last_parent = parents_ids[level]

    #Prints the arrays as strings
    final_string = ""
    for i in range(beam_size):
        output_string = ' '.join(output[i])
        if(i < (beam_size-1)):
            output_file_separate.write(output_string.replace("SEQUENCE_END", "").strip() + "\n")
            final_string = final_string + output_string.replace("SEQUENCE_END", "").strip() + " <SEP> "
        else:
            output_file_separate.write(output_string.replace("SEQUENCE_END", "").strip() + "\n\n")
            final_string = final_string + output_string.replace("SEQUENCE_END", "").strip()
    output_file_together.write(final_string + "\n")

output_file_separate.close()
output_file_together.close()
