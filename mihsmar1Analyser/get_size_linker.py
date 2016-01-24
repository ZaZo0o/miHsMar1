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

######### get size Linker ########
    def get_score_ITR(self):
        size_file = file(sys.argv[3]+'/size_linker.tmp','w')
	header="Size_Linker\n"
        size_file.write(str(header))
        for match in self.match_list:
            size=match.variables[2].size
            size_file.write(str(size)+'\n')
        

def constructArray(xml_file):
    array(xml_file)

constructArray(sys.argv[1])
