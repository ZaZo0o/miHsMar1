#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from xml.sax import ContentHandler
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
import string



# Data model 


class Match:
    def __init__(self, model, id, begin, end, errors, distance, variables):
        self.model = model
        self.id = id
        self.begin = begin
        self.end = end
        self.errors = errors
        self.distance = distance
        self.variables = variables

class Variables:
    def __init__(self, begin, end, size, errors, distance, content, text):
        self.begin = begin
        self.end = end
        self.size = size
        self.errors = errors
        self.distance = distance
        self.content = content
        self.text = text



# Parser XML

class MyContentHandler(ContentHandler):

    def __init__(self):
        self.buf = ''
        self.Match_list= []
        self.currentMatch = None
        self.currentVariable = None
        self.inVar = 0

    def characters(self, content):
        self.buf += content

    def startElement(self, name, attrs):
         if name == 'match':
            self.currentMatch = Match('', '', '', '', '', '', [])
         elif name == 'variable':
            self.currentVariable = Variables('', '', '', '', '', '', '')
            self.inVar = 1

    def endElement(self, name):
        if name == 'match':
            self.Match_list.append(self.currentMatch)
            self.currentMatch = None
        elif name == 'model':
            self.currentMatch.model = self.buf.strip()
            self.buf = ''
        elif name == 'id':
            self.currentMatch.id = self.buf.strip()
            self.buf = ''
        elif name == 'begin':
            if self.inVar == 0:
                self.currentMatch.begin = self.buf.strip()
                self.buf = ''
            elif self.inVar == 1:
                self.currentVariable.begin = self.buf.strip()
                self.buf = ''
        elif name == 'end':
            if self.inVar == 0:
                self.currentMatch.end = self.buf.strip()
                self.buf = ''
            elif self.inVar == 1:
                self.currentVariable.end = self.buf.strip()
                self.buf = ''
        elif name == 'errors':
            if self.inVar == 0:
                self.currentMatch.errors = self.buf.strip()
                self.buf = ''
            elif self.inVar == 1:
                self.currentVariable.errors = self.buf.strip()
                self.buf = ''
        elif name == 'distance':
            if self.inVar == 0:
                self.currentMatch.distance = self.buf.strip()
                self.buf = ''
            elif self.inVar == 1:
                self.currentVariable.distance = self.buf.strip()
                self.buf = ''
        elif name == 'variable':
            self.inVar = 0
            self.currentMatch.variables.append(self.currentVariable)
            self.currentPract = None
            self.buf = ''
        elif name == 'end':
            self.currentVariable.end = self.buf.strip()
            self.buf = ''
        elif name == 'size':
            self.currentVariable.size = self.buf.strip()
            self.buf = ''
        elif name == 'errors':
            self.currentVariable.errors = self.buf.strip()
            self.buf = ''
        elif name == 'distance':
            self.currentVariable.distance = self.buf.strip()
            self.buf = ''
        elif name == 'content':
            self.currentVariable.content = self.buf.strip()
            self.buf = ''
        elif name == 'text':
            self.currentVariable.text = self.buf.strip()
            self.buf = ''



class Parser:
    def __init__(self, filename):
        f = open(filename, 'r')
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        self.dh = MyContentHandler()
        # Tell the parser to use our handler
        parser.setContentHandler(self.dh)
        # Parse the input
        parser.parse(f)

    def Match_list(self):
        return self.dh.Match_list

def contructList(xml_file):
    #xml_file = sys.argv[1]
    p = Parser(xml_file)
    return p.Match_list()

#contructList(sys.argv[1])
