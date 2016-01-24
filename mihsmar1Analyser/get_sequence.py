#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pyparser
import os


class array:
    def __init__(self, xml_file):
        self.match_list = self.parser(xml_file)
        self.get_score_ITR()

    def parser(self, xml_file):
        self.match_liste = pyparser.contructList(xml_file)
        return self.match_liste

######### get sequence ########
    def get_score_ITR(self):
        seq_file = file(sys.argv[3]+'/sequences.tmp','w')
        seq_file.write(str( "Sequences"+"\n"))
        for match in self.match_list:
            text_buffer=''
            for var in match.variables:
                text = var.content + '  '
                text_buffer = text_buffer+ text
            seq_file.write(str(text_buffer)+'\n')
        

def constructArray(xml_file):
    array(xml_file)

constructArray(sys.argv[1])
