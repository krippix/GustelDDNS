'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import json
import logging
import sys

#Part of Project
import config
import simpleTools

#External Imports
import requests
from importlib._bootstrap_external import ExtensionFileLoader

#domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'


class domains:
    #newDomain: Create or Load, domainNo in case newDomain is true
    
    
    def __init__(self):
        logging.debug("domain __init__")
        
        #Variables
        self.domain = ""
        self.recordType = ""
        self.xAuthKey = ""
        self.email = ""
        self.zoneID = ""
        self.recordID = ""
        
        #Pulls location of domains.json from config.py
        self.domainsJSON = config.getDomainsJSON()
        #Example of Dict: 'example.com': {'A': {'xAuthKey': '123xxx123xxx','email': 'user@example.com', 'zoneID': '123123123'}}
        
        #Loading domains.json into domains_dict
        try:
            self.domains_dict = self.loadDomains()
        except Exception as e:
            logging.error(str(e))
            self.domains_dict = {}
        
        if sys.argv[1] == "-new":
            self.createNewDomain()
            
        if sys.argv[1] == "-update":
            self.getDDNSdomains()
        
        
        
        
        
        
            
        
        #Finishes by writing everything to domains.json
        self.writeDomains(self.domains_dict)
        logging.info("done!")  
        
        logging.debug("class domains: done!")
    
    
    def loadDomains(self):
        logging.info("Loading Domains...")
        
        with open(self.domainsJSON) as json_file:
            data = json.load(json_file)
            return data
    
    
    def writeDomains(self, data):
        logging.debug("writeDomainsJSON")
        logging.info("Writing Domains...")
        #Writes Dict to domains.json
        
        with open(self.domainsJSON, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
            
    def createNewDomain(self):    
        
        self.domain = input("Enter Domain: ")
        self.recordType = input("Enter record Type: ")
                
        #Check if domain and RecordType already exists
        try: 
            if self.domain in self.domains_dict and self.recordType in self.domains_dict[self.domain]:
    
                #Check if you want to override existing entry
                if not simpleTools.query_yes_no("{}{}{}{}{}".format("Record type: ",self.recordType, " already Exists for '",self.domain,"', do you want to override it?")):
                    print("Domain creation cancelled.")
                    exit()
        except Exception as e:
            logging.error(str(e))
        
        #Continue with domain creation
        self.xAuthKey = input("Enter xAuthKey: ")
        self.email = input("Enter E-Mail: ")        
        
        
        #Retrieve ZoneID for domain
        self.zoneID = self.requestZoneID(self.domain, self.xAuthKey, self.email)
        
        #Retrieve RecordID for (sub)domain
        self.recordID = self.requestRecordID(self.domain, self.xAuthKey, self.email, self.zoneID)
        
        #Include in DDNS-Updates?
        if simpleTools.query_yes_no("Include Domain in DDNS-Updates?"):
            self.enable_DDNS = True
        else:
            self.enable_DDNS = False
        
        
        #Write everything into domains_dict
        self.domains_dict[self.domain]= {self.recordType: {'xAuthKey': self.xAuthKey, 'email': self.email, 'zoneID': self.zoneID, 'recordID': self.recordID, 'DDNS': self.enable_DDNS}}      
    
    
    def getDDNSdomains(self):
        
        #Get every Record with DDNS = true
        data = self.loadDomains()
        
        
        #Get current Public IP
        currentPubIPv4 = simpleTools.retrievePublicIPv4() 
        
        #Get Domains
        for x in data:
            
            logging.info("-----------------\nChecking Domain '"+x+"'")
            
            
            
            #Get Records in Domain
            for y in data[x]:
                
                #If Record Type A exist and is set for DDNS
                if y == "A" and data[x][y]["DDNS"]:
                    
                    
                    domain = str(x)
                    xAuthKey = data[x][y]["xAuthKey"]
                    email = data[x][y]["email"]
                    zoneID = data[x][y]["zoneID"]
                    recordID = data[x][y]["recordID"]         
                    
                    logging.info("Attempting to update '"+domain+"'")
                    self.updateIPadress(xAuthKey, email, zoneID, recordID, domain, currentPubIPv4)
                else:
                    logging.info("skipping '"+x+"', as no valid record was found.")
        
        
        logging.info("Domain Updates finished. Exiting...")
        exit()
    
        
    def updateIPadress(self, xAuthKey, email, zoneID, recordID, domain, currentPubIPv4):
        #Updates IP of record
        
        
        #Retrieve current IP of record
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': xAuthKey,
            'Content-Type': 'application/json',
        }
        
        
        logging.info(domain+" - Retrieving current Record-IP...")
        try:
            response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records/'+recordID, headers=headers)
            logging.debug(str(response))  
            data = response.json()
        except Exception as e:
            logging.error(domain+" - Failed to retrieve Record-IP: "+e)
        
        
        if str(response) == "<Response [200]>":
            #Check Retrieved IP-Address
            try:
                recordIPv4 = str(data['result']['content'])
                logging.info(domain+" - Current Record IP: "+recordIPv4)
            
            except Exception as e:
                logging.error(domain+"- Failed to retrieve current Record IPv4 address: "+str(e))
                return
  
        else:
            logging.error(domain+" - Failed to retrieve Record-IP: "+str(response))
            return
        
        

        #Check if record IP matches current Public IP-Address
        if currentPubIPv4 == recordIPv4:
            logging.info(domain+" - IP address stays "+currentPubIPv4)
            return
        
        #Attempt to update DNS-Record
        else:
            try:
                logging.info(domain+" - Updating Record IP...")
                payload = {'type':'A','name': domain,'content': currentPubIPv4}
                
                response = requests.put('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records/'+recordID, headers=headers, data = json.dumps(payload))
                print(response.text)
                logging.info(str(response))
                
            except Exception as e:
                logging.error(domain+"- Failed to Update DNS-Record: "+str(e))
                return
            
            if str(response) == "<Response [200]>":
                logging.info("Success!")
            else:
                logging.error(domain+" - Updating failed: "+str(response))
        
        
    
    def requestZoneID(self, domain, xAuthKey, email):
        #Get ZoneID from main domain
        
        #Remove Subdomains
        domain = simpleTools.removeSubDomains(domain)     
              
        
        
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': xAuthKey,
            'Content-Type': 'application/json',
        }
            
        response = requests.get('https://api.cloudflare.com/client/v4/zones?name='+domain, headers=headers)
        logging.debug(str(response.json))  
        data = response.json()
    
        
        #Sucess!
        if str(response) == "<Response [200]>":
            logging.info("Succesfully retrieved ZoneID!")
            
            return str(data["result"][0]["id"])
        
        else:
            logging.error("Failed to retrieve ZoneID: "+str(data["result"][0]["id"]))
            exit()
                
                    
    def requestRecordID(self, domain, xAuthKey, email, zoneID):            
        #Get record ID for domain / subdomain
        
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': xAuthKey,
            'Content-Type': 'application/json',
        }
            
        response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records?name='+domain, headers=headers)
        logging.debug(str(response.json))  
        data = response.json()
    
        
        #Sucess!
        if str(response) == "<Response [200]>":
            logging.info("Succesfully retrieved ZoneID!")
            
            return str(data["result"][0]["id"])
        
        else:
            print("Requesting RecordID failed!")        
                
            
            
            
            
            
        
        
            
        
