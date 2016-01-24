#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pyparser
import os

class array:
    def __init__(self, xml_file):
        self.match_list = self.parser(xml_file)
        self.get_coord()

    def parser(self, xml_file):
        self.match_liste = pyparser.contructList(xml_file)
        return self.match_liste

    def get_coord(self):
        coord_Linker_file = file(sys.argv[3]+'/coord_Linker.tmp','w')
        coord_Linker_file.write(str("Begin_Linker\tEnd_Linker\n"))
        for match in self.match_list:
            coord=match.variables[2].begin + '\t' + match.variables[2].end + '\n'
            coord_Linker_file.write(coord)
        

def constructArray(xml_file):
    array(xml_file)

constructArray(sys.argv[1])
