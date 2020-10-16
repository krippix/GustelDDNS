'''
Created on 04.08.2020

@author: Dennis
'''

import sys
import logging
import requests
import time

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
/
    The "answer" return value is True for "yes" or False for "no".
    
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
            

def retrievePublicIPv4():
    
    errorCount = 0
    
    while True:
        try:
            response = requests.get('https://ifconfig.io/ip')
        except Exception as e:
            logging.error("Failed to retrieve Public IP-address: "+str(e))
            exit()
            
            
        ipv4Address = str(response.text)
        
        #Removing return from result
        if str(response) == "<Response [200]>":
            logging.info("Current Public IP: "+ipv4Address[0:-1])
            return ipv4Address[0:-1]
        
        elif errorCount < 1:
            errorCount += 1
            logging.error("Failed to retrieve IPv4 address "+str(errorCount)+" time!")
            logging.info("Waiting 15 Seconds until retry...")
            time.sleep(15)

        elif errorCount < 8:
            errorCount += 1
            logging.error("Failed to retrieve IPv4 address "+str(errorCount)+" times!")
            logging.info("Waiting 15 Seconds until retry...")
            time.sleep(15)
            
        elif errorCount < 10:
            logging.error("Failed to retrieve IPv4 address "+str(errorCount)+" times!")
            logging.info("Waiting 5 Minutes until retry...")
            time.sleep(300)
            
        else:
            logging.error("Failed to retrieve IPv4 address "+str(errorCount)+" times!")
            logging.error("Exiting Program...")
            
            #TODO Send E-Mail about Failure
            exit()
            

def removeSubDomains(domain):
    #Removes all Subdomains
    
    domainList = domain.split(".")
    try:
        domain_new = domainList[-2] +"."+ domainList[-1]
    except Exception as e:
        logging.error(str(e))
        print("Invalid Domain. Program terminated.")
        exit()

    return domain_new