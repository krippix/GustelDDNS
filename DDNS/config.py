'''
Created on 23.07.2020

@author: Dennis
'''
from pathlib import Path
import os
import logging
import configparser

#Path of inifile
inifile = str(Path(__file__).parent.parent)+os.sep+'config.ini'




def readinifile(section,option):
    parse = configparser.ConfigParser()
    
    try:
        parse.read(inifile)
    except Exception as e:
        logging.warning(str(e))
    
    
    try:
        return parse.get(section, option)
    except Exception as e:
        logging.warning(str(e))
    
    
    
    
    
#readinifile("domains", "datalocation")