#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pyparser
import os

xmlFile=sys.argv[1]
currentPath=sys.argv[2]
workingDir=sys.argv[3]


class array:
    def __init__(self, xml_file):
        self.match_list = self.parser(xml_file)
        self.get_score_ITR()

    def parser(self, xml_file):
        self.match_liste = pyparser.contructList(xml_file)
        return self.match_liste

######## score ITR1 ###########
    def get_score_ITR(self):
        itr1_file = file(workingDir+'/score_itr1.tmp','w')
        nb_id_itr1 = file(workingDir+'/nb_id_itr1.tmp','w')
        itr1_file.write(str("Score_ITR1\n"))
        nb_id_itr1.write(str("Nb_id_itr1\n"))
        consensus_ITR1 = ">consensus ITR1\nTATTAGGTTGGTGCAAAAGTAATTGCGGTT\n"
        fasta_header=">itr\n"
        for match in self.match_list:
            ITR1=match.variables[0].content+match.variables[1].content
            itr1=consensus_ITR1+fasta_header+ITR1+"\n"
            itr1_align_file=file(workingDir+'/itr1.et','w')
            itr1_align_file.write(itr1)
            itr1_align_file.close()
            os.system('./muscle_itr.sh itr1.et '+workingDir)
            align_itr1 = open(workingDir+'/align_itr1.et.fasta','r')
            ligne_itr1 = align_itr1.readlines()
            nb_identity = 0
            for i in ligne_itr1:
                text = i
                id = text.count("*")
                nb_identity = nb_identity+id
            align_itr1.close()
            nb_id_itr1.write(str(nb_identity)+"\n")
            get_score_itr1 = float((nb_identity/30.)*100)
            score_itr1 = round(get_score_itr1, 2)
            muscle_score_itr1 = str(score_itr1)+'\n'
            itr1_file.write(muscle_score_itr1)


def constructArray(xmlFile):
    array(xmlFile)

constructArray(xmlFile)
