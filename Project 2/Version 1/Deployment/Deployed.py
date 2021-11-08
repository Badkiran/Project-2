# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 16:40:57 2021

@author: Kiran B
"""

import streamlit as st
import spacy_streamlit as sts
 
from PIL import Image

from bs4 import BeautifulSoup #converts the contents of a page into a proper format
import requests #used to get the content from a web page
import spacy

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('EMAIL TEMPLATE GENERATION')

st.write("Using Webscraping and NLP Techniques to Generate an E-mail Template")

image = Image.open('WebScraping_EmailTemplate.png')
st.image(image, caption='Email Template Generation by Web-Scraping')

def Webscrape_divID(URL, div_id):
    '''This function scrapes the website from the URL given to it.\
    It collects the entire website data and stores the data in the html format\
        Also it extracts the data segment based on the div_id'''
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
  
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    results = soup.find(id=div_id)
    
    st.write(results.get_text())
    
    # model = ["en_core_web_trf"]
    # visualizers = ["parser"]
    # sts.visualize(model, results.get_text(), visualizers)
    
    return results.get_text()


def Webscrape_Classname(URL, classname):
    
    '''This function scrapes the website from the URL given to it.\
    It collects the entire website data and stores the data in the html format \
    Also it extracts the data segment based on the classname'''
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
  
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
   
    results = soup.find("div", class_= classname)
    
    st.write(results.get_text())
    
    return results.get_text()


def Word_Frequency(spacy_text):
    '''Visualize the Noun and Verb frequencies in the extracted text'''
    
    #Filtering for nouns and verbs only
    nouns_verbs = [token.text for token in spacy_text if token.pos_ in ('NOUN', 'VERB')]
    
    cv = CountVectorizer()
    X = cv.fit_transform(nouns_verbs)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in cv.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    wf_df = pd.DataFrame(words_freq)
    wf_df.columns = ['word', 'count']
    
    # sns.set(rc={'figure.figsize':(12,8)})
    sns.barplot(x = 'count', y = 'word', data = wf_df, palette="GnBu_r")
    st.pyplot()
    
    st.write("**Word Count(Noun & Verb) of the Extracted Text:\n**")
    st.write(wf_df)
    

def POS_Tag(data):
    '''Tag Parts of Speech to the Extracted data and visualize'''
    
    sts.visualize_parser(data)
    sts.visualize_ner(data, labels=nlp.get_pipe("ner").labels)
    

 # Use case 1
def Replace_Content1(token):
    '''Find and replace selected tokens for Usecase 1'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and (token.text == 'John' or token.text == 'John Dooley'):
        return '[Your Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jennifer':
        return "[Your Manager's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return '[Date]'
    return token.text

def FindnReplace1(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content1, nlp_doc)
    return ' '.join(tokens)

# Use Case 2
def Replace_Content2(token):
    '''Find and replace selected tokens for Usecase 2'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and (token.text == 'Joe' or token.text == 'Joe Brown'):
        return '[Your Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Steve':
        return "[Your Manager's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return '[Sickness Date]'
    if token.ent_iob != 0 and token.ent_type_ == 'ORG':
        return '[Hospital/Clinic Name]'
    if token.text == 'Joejoe.brown765@email.com555':
        return '[Your Name]\n [Your Email ID]'
    if token.text == '555':
        return '\n [Your Contact'
    if token.text == '5555':
        return 'Number]'
    return token.text

def FindnReplace2(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content2, nlp_doc)
    return ' '.join(tokens)

# Use Case 3
def Replace_Content3(token):
    '''Find and replace selected tokens for Usecase 3'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Smith':
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonny\n':
        return "[Your Name]\n [Your Designation]"
    if token.text == "Formal":
        return 'Formal Birthday Wishes'
    if token.text == "Mr.":
        return ''
    return token.text

def FindnReplace3(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content3, nlp_doc)
    return ' '.join(tokens)

# Use Case 4
def Replace_Content4(token):
    '''Find and replace selected tokens for Usecase 4'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Paul JonesPhoneEmail':
        return "Regards,\n [Your Name]\n [Your Contact No.]\n [Your Email ID]\n"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return "[Years of Experience]"
    if token.text == "Address":
        return ""
    if token.text == "store":
        return "\b"
    if token.text == "retail":
        return "\b"
    
    return token.text

def FindnReplace4(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content4, nlp_doc)
    return ' '.join(tokens)

# Use Case 5
def Replace_Content5(token):
    '''Find and replace selected tokens for Usecase 5'''
    
    if token.text == ",":
        return ""
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Amy':
        return "[Your Colleague's Name],\n"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonathan':
        return "\n [Your Name]\n [Your Contact number]"
    if token.text == "Sincerely":
        return "\n Sincerely,"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return "[Timeline] and [Reason for Appreciation]"
    return token.text

def FindnReplace5(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content5, nlp_doc)
    return ' '.join(tokens)

# Use Case 6
def Replace_Content6(token):
    '''Find and replace selected tokens for Usecase 6'''
    
    if token.text == ",":
        return ""
    if token.text == "Hello":
        return "Dear [Sender's Name],\n"
    if token.text == "COLLEAGUE":
        return "[Your Colleague's Name]"
    if token.text == "Regards":
        return "\n Regards,"
    if token.text == "NAME":
        return "\n [Your Name]"
    if token.text == "do":
        return "don't"
    if token.text == "n’t":
        return "\b"
    return token.text

def FindnReplace6(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content6, nlp_doc)
    return ' '.join(tokens)

# Use Case 7
def Replace_Content7(token):
    '''Find and replace selected tokens for Usecase 7'''
    
    if token.text == ",":
        return ""
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Sam':
        return "[Your Partner's Name],\n"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonathan':
        return "\n[Your Name]\n[Your Contact Number]"
    if token.text == "Please":
        return "\nPlease"
    if token.text == "Thank":
        return "\nThank"
    if token.text == "again!Sincerely":
        return "\b\b, again!\nSincerely,"
    return token.text

def FindnReplace7(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content7, nlp_doc)
    return ' '.join(tokens)

# Collect User Input    
st.write("**Select your desrired category for the Email Template:**")
option = st.selectbox("Drop down options",\
                      ('Vacation Leave Email Template', 'Sick Leave Email Template',\
                       'Birthday Wishes Email Template', 'Cover Letter Email Template',\
                           'Employee work appreciation Email Template', 'Out of Office Email Template',\
                               'Business Deal Closure Email Template'))
st.write('\n**You have selected**:', option)
st.text("Scraping Web......Done!\n")
st.write('\n\n**Exracted text to be analyzed:**')

nlp = spacy.load('en_core_web_trf')

if option == 'Vacation Leave Email Template':
    URL = "https://www.thebalancecareers.com/formal-leave-of-absence-letter-request-example-2060597"
    
    div_id = "mntl-sc-block-callout-body_1-0-3"
    extract = Webscrape_divID(URL, div_id)
        
    # Parse the text with spaCy
    spacy_text1 = nlp(extract)
    
    Word_Frequency(spacy_text1)
    
    POS_Tag(spacy_text1)
    sts.visualize_tokens(spacy_text1, attrs=["text", "pos_", "dep_", "ent_type_"])
     
    # Generate Template
    template1 = FindnReplace1(spacy_text1)
    st.write("**Your Template for Vacation Leave Email**\n")
    st.text(template1)
    
    
elif option == 'Sick Leave Email Template':
    URL = "https://www.thebalancecareers.com/sample-sickness-absence-excuse-letter-2060603"
    
    div_id = "mntl-sc-block-callout-body_1-0-3"
    extract = Webscrape_divID(URL, div_id)
    
    # Parse the text with spaCy
    spacy_text2 = nlp(extract)
    
    Word_Frequency(spacy_text2)
    
    POS_Tag(spacy_text2)
    sts.visualize_tokens(spacy_text2, attrs=["text", "pos_", "dep_", "ent_type_"])
        
    # Generate Template
    template2 = FindnReplace2(spacy_text2)
    st.write("**Your Template for Sick Leave Email**\n")
    st.text(template2)
    
    
elif option == 'Birthday Wishes Email Template':
    URL = "https://www.targettraining.eu/happy-birthday-emails/"
    
    classname = "avia-promocontent"
    extract1 = Webscrape_Classname(URL, classname)
        
    # Parse the text with spaCy
    spacy_text3 = nlp(extract1)
    
    Word_Frequency(spacy_text3)
    
    POS_Tag(spacy_text3)
    sts.visualize_tokens(spacy_text3, attrs=["text", "pos_", "dep_", "ent_type_"])
    
    # Generate Template
    template3 = FindnReplace3(spacy_text3)
         
    st.write("**Your Template for Birthday Wishes Email**\n")
    st.text(template3)
    
    
elif option == 'Cover Letter Email Template':
    URL = "https://www.thebalancecareers.com/email-cover-letter-samples-2060246"
    
    div_id = "mntl-sc-block-callout-body_1-0-1"
    extract = Webscrape_divID(URL, div_id)
    
    phr1 = "Store Manager Position"
    temp1 = extract.replace(str(phr1),"[Role you are applying for]")
    
    phr2 = "Your Name"
    temp2 = temp1.replace(str(phr2), "[Your Name]")
    
    phr3 = "Store Manager position"
    temp3 = temp2.replace(str(phr3),"[Role you are applying for]")
    
    phr4 = "Payroll management, scheduling, reports, and inventory control expertise"
    temp4 = temp3.replace(str(phr4),"")
    
    phr5 = "Extensive work with visual standards and merchandising high-ticket items"
    temp5 = temp4.replace(str(phr5),"")
    
    phr6 = "retail management"
    temp6 = temp5.replace(str(phr6),"[Your previous role]")
    
    phr7 = "XYZ Company:"
    temp7 = temp6.replace(str(phr7),"[Company name you are applying for]:\n[Your Skill Set]...for example")
    
    # Parse the text with spaCy
    spacy_text4 = nlp(temp7)
    
    Word_Frequency(spacy_text4)
    
    POS_Tag(spacy_text4)
    sts.visualize_tokens(spacy_text4, attrs=["text", "pos_", "dep_", "ent_type_"])
    
    # Generate Template
    template4 = FindnReplace4(spacy_text4)
         
    st.write("**Your Template for Cover Letter Email**\n")
    st.text(template4)


elif option == 'Employee work appreciation Email Template':
    URL = "https://talkroute.com/7-sample-thank-you-notes-for-business/"
    
    div_id = "x-content-band-5"
    extract = Webscrape_divID(URL, div_id)
    
    phr1 = "You showed"
    temp1 = extract.replace(str(phr1),"\nYou showed")
    
    phr2 = "I am"
    temp2 = temp1.replace(str(phr2),"\nI am")
    
    # Parse the text with spaCy
    spacy_text5 = nlp(temp2)
    
    Word_Frequency(spacy_text5)
    
    POS_Tag(spacy_text5)
    sts.visualize_tokens(spacy_text5, attrs=["text", "pos_", "dep_", "ent_type_"])
    
    # Generate Template    
    template5 = FindnReplace5(spacy_text5)
    
    st.write("**Your Template for Employee Work Appreciation Email**\n")
    st.text(template5)
    

elif option == 'Out of Office Email Template':
    URL = "https://www.ionos.com/digitalguide/e-mail/technical-matters/perfect-out-of-office-message-examples-and-templates/"
    
    div_id = "c118391"
    extract = Webscrape_divID(URL, div_id)
    
    phrase = "Formal out of office reply with referral for customers"
    temp = extract.replace(str(phrase),"")
    
    phr1 = "Feel free"
    temp1 = temp.replace(str(phr1),"\nFeel free")
    
    phr2 = "You can"
    temp2 = temp1.replace(str(phr2),"\nYou can")
    
    phr3 = "Thank you"
    temp3 = temp2.replace(str(phr3),"\nThank you")
    
    # Parse the text with spaCy
    spacy_text6 = nlp(temp3)
    
    Word_Frequency(spacy_text6)
    
    POS_Tag(spacy_text6)
    sts.visualize_tokens(spacy_text6, attrs=["text", "pos_", "dep_", "ent_type_"])
    
    # Generate Template
    temp1 = FindnReplace6(spacy_text6)
    
    phr = "MM / DD / YY"
    temp2 = temp1.replace(str(phr), "[Your Date of Return]")
    
    phr1 = "( colleague@example.com )"
    temp3 = temp2.replace(str(phr1), "[Your Colleague's Email ID]")
    
    phr2 = "( XXX - XXXX )"
    template6 = temp3.replace(str(phr2), "[Your Colleague's Contact No.]")
         
    st.write("**Your Template for Out of Office Email**\n")
    st.text(template6)
    

elif option == 'Business Deal Closure Email Template':
    URL = "https://talkroute.com/7-sample-thank-you-notes-for-business/"
    
    div_id = "x-content-band-6"
    extract = Webscrape_divID(URL, div_id)
    
    # Parse the text with spaCy
    spacy_text7 = nlp(extract)
    
    Word_Frequency(spacy_text7)
    
    POS_Tag(spacy_text7)
    sts.visualize_tokens(spacy_text7, attrs=["text", "pos_", "dep_", "ent_type_"])
    
    # Generate Template
    template7 = FindnReplace7(spacy_text7)
         
    st.write("**Your Template for Business Deal Closure Email**\n")
    st.text(template7)


