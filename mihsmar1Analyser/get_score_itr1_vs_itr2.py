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

############# ITR1 vs ITR2 ##############
    def get_score_ITR(self):
        itr_file = file(workingDir+'/score_inter_itrs.tmp','w')
        itr_file.write(str("Score ITR1 vs ITR2\n"))
        consensus_ITR1 = ">consensus ITR1\nTATTAGGTTGGTGCAAAAGTAATTGCGGTT\n"
        consensus_ITR2 = ">consensus ITR2\nAACCGCAATTACTTTTGCACCAACCTAATA\n"
        fasta_header=">itr\n"
        for match in self.match_list:

            seq_ITR1=str(match.variables[0].content+match.variables[1].content)
            seq_ITR2=str(match.variables[3].content+match.variables[4].content)
            header_complement=">reverse_itr2\n"
            complement_ITR2=''
            reverse_ITR2=''
            for i in seq_ITR2:
                if i == 'a':
                    complement_ITR2='t'+complement_ITR2
                if i == 't':
                    complement_ITR2='a'+complement_ITR2
                if i == 'g':
                    complement_ITR2='c'+complement_ITR2
                if i == 'c':
                    complement_ITR2='g'+complement_ITR2
            reverse_ITR2=fasta_header+seq_ITR1+'\n'+header_complement+complement_ITR2
            itr2_wc=file(workingDir+'/wc_itr2.et','w')
            itr2_wc.write(reverse_ITR2)
            itr2_wc.close()
            os.system('./muscle_itr.sh wc_itr2.et ' + workingDir)
            align_wc_itr2 = open(workingDir+'/align_wc_itr2.et.fasta','r')
            ligne_wc_itr2 = align_wc_itr2.readlines()
            nb_identity = 0
            for i in ligne_wc_itr2:
                text = i
                id = text.count("*")
                nb_identity = nb_identity+id
            align_wc_itr2.close()
            score_wc_itr2 = float((nb_identity/30.)*100)
            muscle_score_wc_itr2 = str(round(score_wc_itr2,2))+'\n'
            itr_file.write(muscle_score_wc_itr2)


def constructArray(xml_file):
    array(xml_file)

constructArray(xmlFile)
