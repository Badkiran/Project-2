# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:07:54 2021

@author: Kiran B
"""

from bs4 import BeautifulSoup #converts the contents of a page into a proper format
import requests #used to get the content from a web page
import spacy

import warnings
warnings.filterwarnings("ignore")

#Defining Functions for Webscraping and Text Visualization

def Webscrape(URL, div_id):
    '''This function scrapes the website from the URL given to it.\
    It collects the entire website data and stores the data in the html format '''
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
  
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    results = soup.find(id=div_id)

    print(results.get_text())
    
    return results.get_text()


def Macro_Visualize(data):
    '''Visualize the entire extracted data using Parse Trees'''
    
    spacy.displacy.serve(data, style="dep")
    

def Micro_Visualize(data):
    '''Visualize the extracted data sentence by sentence using Parse Trees'''
    
    sentence_spans = list(data.sents)
    spacy.displacy.serve(sentence_spans, style="dep")


def POS_Tag(data):
    '''Tag Parts of Speech to the Extracted data and visualize'''
    
    spacy.displacy.serve(data, style='ent')
    
    
#Obtaining the email category input from the user

def Collect_input():
    print("    1. Sick Leave Email Template\n\
    2. Vacation Leave Email Template\n\
    3. Birthday Wishes Email Template\n\
    4. Marketing Reply Email Template\n\
    5. Out of Town Email Template\n\
    6. Interview Application Email Template\n\n")

    val = input("Enter your desrired category(1-6) for the Email Template:\n>>> ")
    return val


val = int(Collect_input())
    
while val <= 0 or val >= 7:
    print("That is not a valid input. Numbers between 1 and 6 only please!\n\n")
    val = int(Collect_input())
        
if val == 1:
    print("\nYou have chosen to generate a Sick Leave Email Template:\n\n")
    URL = "https://www.thebalancecareers.com/formal-leave-of-absence-letter-request-example-2060597"
    
    div_id = "mntl-sc-block-callout-body_1-0-3"
    extract = Webscrape(URL, div_id)
            
    nlp = spacy.load('en_core_web_lg')
        
    # Parse the text with spaCy
    spacy_text = nlp(extract)

    # Print out all the named entities that were detected
    print("\n\n*Tagged POS entities of the Extracted Text*")
    for entity in spacy_text.ents:
        print(f"{entity.text} ({entity.label_})")
        
    # Parse Trees
    # Macro_Visualize(spacy_text)
        
    # Parts of Speech Tagging
    # POS_Tag(spacy_text)
    
    






