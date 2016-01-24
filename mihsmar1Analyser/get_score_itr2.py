#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append(sys.argv[2] +"/mihsmar1Viewer/")
import pyparser
import os


class array:
    def __init__(self, xml_file):
        self.match_list = self.parser(xml_file)
        self.get_score_ITR()

    def parser(self, xml_file):
        self.match_liste = pyparser.contructList(xml_file)
        return self.match_liste

######## score ITR2 ###########
    def get_score_ITR(self):
        itr2_file = file(sys.argv[3]+'/score_itr2.tmp','w')
        nb_id_itr2 = file(sys.argv[3]+'/nb_id_itr2.tmp','w')
        itr2_file.write(str("Score_ITR2\n"))
        nb_id_itr2.write(str("Nb_id_ITR2\n"))
        consensus_ITR2 = ">consensus ITR2\nAACCGCAATTACTTTTGCACCAACCTAATA\n"
        fasta_header=">itr\n"
        for match in self.match_list:
            ITR2=match.variables[3].content+ match.variables[3].content+match.variables[4].content
            itr2=consensus_ITR2+fasta_header+ITR2+"\n"
            itr2_align_file=file(sys.argv[3]+'/itr2.et','w')
            itr2_align_file.write(itr2)
            itr2_align_file.close()
            os.system('./muscle_itr.sh itr2.et '+ sys.argv[3])

            align_itr2 = open(sys.argv[3] +'/align_itr2.et.fasta','r')
            ligne_itr2 = align_itr2.readlines()
            nb_identity = 0
            for i in ligne_itr2:
                text = i
                id = text.count("*")
                nb_identity = nb_identity+id
            align_itr2.close()
            nb_id_itr2.write(str(nb_identity)+"\n")
            get_score_itr2 = float((nb_identity/30.)*100)
            score_itr2 = round(get_score_itr2, 2)
            muscle_score_itr2 = str(score_itr2)+'\n'
            itr2_file.write(muscle_score_itr2)


def constructArray(xml_file):
    array(xml_file)

constructArray(sys.argv[1])
