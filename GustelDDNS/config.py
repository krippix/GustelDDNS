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



def getDomainsJSON():
    return "{}{}{}{}{}".format(Path(__file__).parent.parent, os.sep, "data", os.sep, "domains.json")

def checkDomainsJSON():
    logging.info("Checking for domains.json")
        
    if Path(getDomainsJSON()).exists():
        logging.info("domains.json found!")
    else:
        logging.warning("domains.json not found!")
        createDomainsJSON()
        
            
def createDomainsJSON():
    logging.info("Creating new domains.json")
        
    try:
        open(getDomainsJSON(), "x")
        logging.info("domains.json created!")
    except Exception as e:
        logging.error("Failed to create domains.json: "+str(e))
        exit()

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