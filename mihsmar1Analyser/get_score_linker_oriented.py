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
        self.get_score_Linker()

    def parser(self, xml_file):
        self.match_liste = pyparser.contructList(xml_file)
        return self.match_liste

######## score ITR1 ###########
    def get_score_Linker(self):
        linker_file = file(workingDir+'/score_linker.tmp','w')
        nb_id_linker = file(workingDir+'/nb_id_linker.tmp','w')
        linker_file.write(str("Score_Linker\tOrientation\n"))
        nb_id_linker.write(str("Nb_id_Linker\n"))
        consensus_linker = ">consensus Linker\nTTTGCCATTGAAAGTAATGGCAAA\n>linker\n"
        linker_align_file=file(workingDir+'/linker.et','w')


        for match in self.match_list:
            linker_seq=match.variables[2].content
            complement_linker_seq=''
            for i in linker_seq:
                if i == 'a':
                    complement_linker_seq='t'+complement_linker_seq
                if i == 't':
                    complement_linker_seq='a'+complement_linker_seq
                if i == 'g':
                    complement_linker_seq='c'+complement_linker_seq
                if i == 'c':
                    complement_linker_seq='g'+complement_linker_seq


            linker_align_file=open(workingDir+'/linker.et','w')
            linker_align_file.write(consensus_linker+linker_seq)
            linker_align_file.close()
            id_linker=self.muscle()

            linker_align_file=open(workingDir+'/linker.et','w')
            linker_align_file.write(consensus_linker+complement_linker_seq)
            linker_align_file.close()
            id_reverse_linker=self.muscle()

            if id_linker>id_reverse_linker:
                nb_id_linker.write(str(id_linker)+"\n")
                get_score_linker = float((id_linker/30.)*100)
                score_linker = round(get_score_linker, 2)
                muscle_score_linker = str(score_linker)+'\t+'+'\n'
                linker_file.write(muscle_score_linker)
            elif id_linker<id_reverse_linker:
                nb_id_linker.write(str(id_reverse_linker)+"\n")
                get_score_linker = float((id_reverse_linker/30.)*100)
                score_linker = round(get_score_linker, 2)
                muscle_score_linker = str(score_linker)+'\t-'+'\n'
                linker_file.write(muscle_score_linker)
            elif id_linker==id_reverse_linker:
                nb_id_linker.write(str(id_linker)+"\n")
                get_score_linker = float((id_linker/30.)*100)
                score_linker = round(get_score_linker, 2)
                muscle_score_linker = str(score_linker)+'\t?'+'\n'
                linker_file.write(muscle_score_linker)


    def muscle(self):
#            os.system('./muscle_itr.sh linker.et '+workingDir)
#            linker_fasta=consensus_linker+fasta_header+linker_seq+"\n"
#            linker_align_file=file(workingDir+'/linker.et','w')
#            linker_align_file.write(linker_fasta)
#            linker_align_file.close()
            os.system('./muscle_itr.sh linker.et '+workingDir)
            align_linker = open(workingDir+'/align_linker.et.fasta','r')
            ligne_linker = align_linker.readlines()
            nb_identity = 0
            for i in ligne_linker:
                text = i
                id = text.count("*")
                nb_identity = nb_identity+id
            align_linker.close()
#            nb_id_linker.write(str(nb_identity)+"\t\n")
#            get_score_linker = float((nb_identity/30.)*100)
#            score_linker_+ = round(get_score_linker, 2)
#            muscle_score_linker = str(score_linker)+'\t'+'\n'
#            linker_file.write(muscle_score_linker)
            return nb_identity





def constructArray(xml_file):
    array(xml_file)

constructArray(xmlFile)
