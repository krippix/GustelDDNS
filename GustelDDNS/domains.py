#System imports
import logging

#Part of Project
import simpleTools
import providers.cloudFlare

#External Imports



def createNewDomain(domains_dict):
    #Creates new Domain (locally!)
    logging.debug("GustelDDNS.domains.createNewDomain()")
    #TODO: Allow Domain Creation on CF Server
    
    #Possible allow choosing Provider(?)
    
    #Ask for Record Type and Domainname
    domain = input("Enter Domain: ")
    recordType = input("Enter record Type: ")
    
    #Include in DDNS-Updates?
    if simpleTools.query_yes_no("Include Domain in DDNS-Updates?"):
        enable_DDNS = True
    else:
        enable_DDNS = False
            
    #Check if domain and RecordType already exists
    try: 
        if domain in domains_dict and recordType in domains_dict[domain]:

            #Check if you want to override existing entry
            if not simpleTools.query_yes_no("{}{}{}{}{}".format("Record type: ",recordType, " already Exists for '",domain,"', do you want to override it?")):
                print("Domain creation cancelled.")
                exit()
    except Exception as e:
        logging.error(str(e))
    
    
    #Creates new Domain, returns edited domains_dict
    domains_dict = providers.cloudFlare.createNewDomain(domains_dict, domain, recordType)
    
    
    

def updateDDNSdomains(domains_dict):
    logging.debug("GustelDDNS.domains.updateDDNSdomains()")
    #Get every Record with DDNS = true
    
    
    #Get current Public IP
    currentPubIPv4 = simpleTools.retrievePublicIPv4() 
    
    #Get Domains
    for x in domains_dict:
        
        logging.info("-----------------\nChecking Domain '"+x+"'")
        
        
        
        #Get Records in Domain
        for y in domains_dict[x]:
            
            #If Record Type A exist and is set for DDNS
            if y == "A" and domains_dict[x][y]["DDNS"]:
                
                
                domain = str(x)
                xAuthKey = domains_dict[x][y]["xAuthKey"]
                email = domains_dict[x][y]["email"]
                zoneID = domains_dict[x][y]["zoneID"]
                recordID = domains_dict[x][y]["recordID"]         
                
                logging.info("Attempting to update '"+domain+"'")
                providers.cloudFlare.updateIPadress(xAuthKey, email, zoneID, recordID, domain, currentPubIPv4)
            else:
                logging.info("skipping '"+x+"', as no valid record was found.")
    
    
    logging.info("-----------------")
    logging.info("Domain Updates finished. Exiting...")
    exit()

        




    
       