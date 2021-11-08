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
st.set_page_config(layout = 'wide')
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
    st.text("Scraping Web......Done!\n")
    st.write('**Exracted text to be analyzed:**')   
    st.write(results.get_text())
    
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
    st.text("Scraping Web......Done!\n")
    st.write('**Exracted text to be analyzed:**')   
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
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'John Dooley':
        return '[Your Name]\n'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'John':
        return '\n[Your Name]'
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

def Replace_Content1a(token):
    '''Find and replace selected tokens for Usecase 1a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'William J. Jones':
        return '[Your Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'William Jones':
        return '[Your Signature on the Hard copy]'
    if token.ent_iob != 0 and token.ent_type_ == 'ORG':
        return '[Your Company Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Perez':
        return "[Your Manager's Name]"
    if token.ent_iob !=0 and token.ent_type_ == 'DATE' and token.text == 'between now and September 1, 2013':
        return "before [Your task completion timeline]"
    if token.ent_iob !=0 and token.ent_type_ == 'DATE' and token.text == 'September 1, 2013 through September 21, 2013':
        return "[From Date] through [To Date]"
    if token.ent_iob != 0 and token.ent_type_ == 'GPE':
        return '[Place/Country name]'
    if token.text == "Mr.":
        return '\b'
    if token.text == "cruise":
        return '\b'
    if token.text == "wife":
        return "[self/companion/friend]"
    
    return token.text

def FindnReplace1a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content1a, nlp_doc)
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
        return '\n[Your Name]\n[Your Email ID]'
    if token.text == '555':
        return '\n[Your Contact'
    if token.text == '5555':
        return 'Number]'
    return token.text

def FindnReplace2(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content2, nlp_doc)
    return ' '.join(tokens)

def Replace_Content2a(token):
    '''Find and replace selected tokens for Usecase 2a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jane':
        return '\n[Your Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jane Doe':
        return '[Your Name]'
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and (token.text == 'Patricia' or token.text == 'Tom'):
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE' and token.text == 'Friday':
        return "on [Meeting day]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return '[Sickness Date]'
    return token.text

def FindnReplace2a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content2a, nlp_doc)
    return ' '.join(tokens)


# Use Case 3
def Replace_Content3(token):
    '''Find and replace selected tokens for Usecase 3'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Smith':
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonny\n':
        return "\n [Your Name]\n [Your Designation]"
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

def Replace_Content3a(token):
    '''Find and replace selected tokens for Usecase 3a'''
    
    if token.text == "company!Have":
        return 'company!\n Have'
    return token.text

def FindnReplace3a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content3a, nlp_doc)
    return ' '.join(tokens)


# Use Case 4
def Replace_Content4(token):
    '''Find and replace selected tokens for Usecase 4'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Paul JonesPhoneEmail':
        return "\n\n Regards,\n [Your Name]\n [Your Contact No.]\n [Your Email ID]\n"
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

def Replace_Content4a(token):
    '''Find and replace selected tokens for Usecase 4a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and (token.text == 'Mary Garcia12' or token.text == 'Mary Garcia'):
        return "[Your Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Lee':
        return "[Hiring Manager's Name]"
    if token.text == "Lee":
        return "\n [Hiring Manager's Name]\n"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Franklin Lee':
        return "To: [Hiring Manager's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE' and token.text == 'five years':
        return "[Your experience in years]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return "[Mailing Date]\n"
    if token.ent_iob != 0 and token.ent_type_ == 'ORG' and token.text == 'CBI Industries39':
        return "[Company Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'ORG':
        return "[Your leaving Company name]"
    if token.ent_iob != 0 and token.ent_type_ == 'GPE' and token.text == 'AvenueTownville':
        return "[Building No., Street Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'GPE' and token.text == 'New Hampshire':
        return "\n [Area Name, Town Name, Pincode]\n"
    if token.ent_iob != 0 and token.ent_type_ == 'GPE':
        return "[Campus Name]"
    if token.text == 'Rogers':
        return "\n"
    if token.text == "Mr.":
        return ""
    if token.text == "03060":
        return "\n"
    if token.text == "Sincerely":
        return "\n\n Sincerely"
    if token.text == "Signature":
        return "\n [Signature]"
    return token.text

def FindnReplace4a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content4a, nlp_doc)
    return ' '.join(tokens)


# Use Case 5
def Replace_Content5(token):
    '''Find and replace selected tokens for Usecase 5'''
    
    if token.text == ",":
        return ""
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Amy':
        return "[Your Colleague's Name],\n"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonathan':
        return "\n\n [Your Name]\n [Your Contact number]"
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

def Replace_Content5a(token):
    '''Find and replace selected tokens for Usecase 5a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'John':
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Samantha':
        return "\n [Your Name]\n [Your Designation]"
    if token.text == "Best":
        return "Best Regards"
    if token.text == 'project':
        return "[Work of Appreciation]"
    if token.text == "Dear":
        return "\nDear"
    return token.text

def FindnReplace5a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content5a, nlp_doc)
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
        return "\n\n [Your Name]"
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

def Replace_Content6a(token):
    '''Find and replace selected tokens for Usecase 6a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jane Doe':
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'John Smith':
        return "\n [Your Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE':
        return "[Your Return Date]"
    if token.text == "Thank":
        return "Dear [Sender's Name],\n\n\t Thank"
    if token.text == "She":
        return "He/She"
    return token.text

def FindnReplace6a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content6a, nlp_doc)
    return ' '.join(tokens)


# Use Case 7
def Replace_Content7(token):
    '''Find and replace selected tokens for Usecase 7'''
    
    if token.text == ",":
        return ""
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Sam':
        return "[Your Partner's Name],\n\n"
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'Jonathan':
        return "\n\n[Your Name]\n[Your Contact Number]"
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

def Replace_Content7a(token):
    '''Find and replace selected tokens for Usecase 7a'''
    
    if token.ent_iob != 0 and token.ent_type_ == 'PERSON' and token.text == 'James':
        return "[Your Colleague's Name]"
    if token.ent_iob != 0 and token.ent_type_ == 'DATE' and token.text == 'a whole year':
        return "[Number of years]"
    if token.text == "at":
        return ""
    return token.text

def FindnReplace7a(nlp_doc):
    with nlp_doc.retokenize() as retokenizer:
        for ent in nlp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(Replace_Content7a, nlp_doc)
    return ' '.join(tokens)


# Collect User Input    
st.write("**Select your desrired category for the Email Template:**")
option = st.selectbox("Drop down options",\
                      ('Vacation Leave Email Template', 'Sick Leave Email Template',\
                       'Birthday Wishes Email Template', 'Cover Letter Email Template',\
                           'Employee work appreciation Email Template', 'Out of Office Email Template',\
                               'Thank you note for Business Email Template'))
st.write('\n**You have selected**:', option)

nlp = spacy.load('en_core_web_trf')

if option == 'Vacation Leave Email Template':
        
    URL1 = "https://www.thebalancecareers.com/formal-leave-of-absence-letter-request-example-2060597"
    div_id1 = "mntl-sc-block-callout-body_1-0-3"
    URL2 = "https://www.greatsampleresume.com/letters/personal-letters/vacation-leave"
    classname2 = "letter-table"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
        
        phr = "As we discussed"
        temp = extract1.replace(str(phr), "\n\tAs we discussed")
        phr1 = "Dear"
        temp2 = temp.replace(str(phr1), "\nDear") 
        
        # Parse the text with spaCy
        spacy_text1 = nlp(temp2)
    
        Word_Frequency(spacy_text1)
        
        POS_Tag(spacy_text1)
        sts.visualize_tokens(spacy_text1, attrs=["text", "pos_", "dep_", "ent_type_"])
    
        # Generate Template
        temp2 = FindnReplace1(spacy_text1)
        
        phr2 = "I plan"
        temp3 = temp2.replace(str(phr2), "\nI plan")
        phr3 = "I would also"
        temp4 = temp3.replace(str(phr3), "\nI would also")
        phr4 = "Thank you"
        temp5 = temp4.replace(str(phr4), "\nThank you")
        phr5 = "Best"
        template1 = temp5.replace(str(phr5), "\n\nBest")
        st.subheader("**Your Template for Vacation Leave Email**\n")
        st.text(template1)
    
    
    def Process_URL2():
        extract2 = Webscrape_Classname(URL2, classname2)
        
        phr1 = "Yours sincerely,"
        temp1 = extract2.replace(str(phr1), "\nYours sincerely,\n")
        phr2 = "(555)-555-5555"
        temp2 = temp1.replace(str(phr2), "[Your Contact Number]")
        phr3 = "my leave"
        temp3 = temp2.replace(str(phr3), "\b\b\b my leave")
        phr4 = "I think you"
        temp4 = temp3.replace(str(phr4), "\nI think you")
        phr5 = "I am planning"
        temp5 = temp4.replace(str(phr5), "\n\tI am planning")
        phr6 = "If there are"
        temp6 = temp5.replace(str(phr6), "\nIf there are")
        phr7 = "I am writing"
        temp7 = temp6.replace(str(phr7), "\n\tI am writing")
        
        # Parse the text with spaCy
        spacy_text1a = nlp(temp7)
    
        Word_Frequency(spacy_text1a)
        
        POS_Tag(spacy_text1a)
        sts.visualize_tokens(spacy_text1a, attrs=["text", "pos_", "dep_", "ent_type_"])
           
        # Generate Template
        temp = FindnReplace1a(spacy_text1a)
        
        phr4 = "Assistant Manager"
        template1a = temp.replace(str(phr4), "[Your Designation]")
        
        st.subheader("**Your Template for Vacation Leave Email**\n")
        st.text(template1a)
            
    
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('absence, discussed, approved, assistance',\
                                                'vacation, formally, endeavored, trip'))
        
    if(keyword == 'absence, discussed, approved, assistance'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'vacation, formally, endeavored, trip'):
        st.write('You selected:', keyword)
        Process_URL2()
    
    
elif option == 'Sick Leave Email Template':
    
    URL1 = "https://www.thebalancecareers.com/sample-sickness-absence-excuse-letter-2060603"
    div_id1 = "mntl-sc-block-callout-body_1-0-3"
    URL2 = "https://www.thebalancecareers.com/sample-sickness-absence-excuse-letter-2060603"
    div_id2 = "mntl-sc-block-callout-body_1-0-4"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
        
        phr = "Dear"
        temp = extract1.replace(str(phr), "\n\nDear") 
        phr1 = "I am writing"
        temp1 = temp.replace(str(phr1), "\n\t I am writing")
        phr2 = "Please"
        temp2 = temp1.replace(str(phr2), "\nPlease")
        phr3 = "Regards"
        temp2 = temp2.replace(str(phr3), "\n\nRegards")
        
        # Parse the text with spaCy
        spacy_text2 = nlp(temp2)
    
        Word_Frequency(spacy_text2)
    
        POS_Tag(spacy_text2)
        sts.visualize_tokens(spacy_text2, attrs=["text", "pos_", "dep_", "ent_type_"])
        
       # Generate Template
        temp = FindnReplace2(spacy_text2)
    
        phrase = "an acute attack of food poisoning"
        template2 = temp.replace(str(phrase),"[Reason for Sickness]")
        st.subheader("**Your Template for Sick Leave Email**\n")
        st.text(template2)
        
    def Process_URL2():
        extract2 = Webscrape_divID(URL2, div_id2)
        
        phr = "Dear"
        temp = extract2.replace(str(phr), "\n\nDear")
        phr1 = "Supervisor Name"
        temp1 = temp.replace(str(phr1), "[Your Manager's Name]")
        phr2 = "I've asked"
        temp2 = temp1.replace(str(phr2), "\nI've asked")
        phr3 = "I've come"
        temp3 = temp2.replace(str(phr3), "\n\tI've come")
        phr4 = "I will try"
        temp4 = temp3.replace(str(phr4), "\nI will try")
        phr5 = "Thank you"
        temp5 = temp4.replace(str(phr5), "\n\nThank you")
        
        # Parse the text with spaCy
        spacy_text2a = nlp(temp5)
    
        Word_Frequency(spacy_text2a)
    
        POS_Tag(spacy_text2a)
        sts.visualize_tokens(spacy_text2a, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template
        template2a = FindnReplace2a(spacy_text2a)
        st.subheader("**Your Template for Sick Leave Email**\n")
        st.text(template2a)
    
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('document, absence, illness, treatment',\
                                                'flu, rest, recover, prepare'))
        
    if(keyword == 'document, absence, illness, treatment'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'flu, rest, recover, prepare'):
        st.write('You selected:', keyword)
        Process_URL2()
    
    
elif option == 'Birthday Wishes Email Template':
    
    URL1 = "https://www.targettraining.eu/happy-birthday-emails/"
    classname1 = "avia-promocontent"
    URL2 = "https://www.happybirthdaywisher.com/employee/"
    div_id2 = "mensagem-1072"
    
    def Process_URL1():
        extract1 = Webscrape_Classname(URL1, classname1)
        
        phr1 = "I am"
        temp1 = extract1.replace(str(phr1),"\n\tI am")
        
        # Parse the text with spaCy
        spacy_text3 = nlp(temp1)
    
        Word_Frequency(spacy_text3)
    
        POS_Tag(spacy_text3)
        sts.visualize_tokens(spacy_text3, attrs=["text", "pos_", "dep_", "ent_type_"])
    
        # Generate Template
        template3 = FindnReplace3(spacy_text3)
         
        st.subheader("**Your Template for Birthday Wishes Email**\n")
        st.text(template3)
        
        
    def Process_URL2():
        extract2 = Webscrape_divID(URL2, div_id2)
    
        phr1 = "birthday!"
        temp1 = extract2.replace(str(phr1), "birthday!\n\nSincerely,\n[Your Name]\n[Your Designation]")
        
        phr2 = "Happy"
        temp2 = temp1.replace(str(phr2), "Dear [Your Colleague's Name],\n\tHappy")
        
        phr3 = "Your positivity"
        temp3 = temp2.replace(str(phr3), "\nYour positivity")
        
        
        # Parse the text with spaCy
        spacy_text3a = nlp(temp3)
    
        Word_Frequency(spacy_text3a)
    
        POS_Tag(spacy_text3a)
        sts.visualize_tokens(spacy_text3a, attrs=["text", "pos_", "dep_", "ent_type_"])
    
        # Generate Template
        template3a = FindnReplace3a(spacy_text3a)
         
        st.subheader("**Your Template for Birthday Wishes Email**\n")
        st.text(template3a)
        
    
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('writing, wish, enjoy, returns',\
                                                'wonderful, positivity, expertise, regarded'))
        
    if(keyword == 'writing, wish, enjoy, returns'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'wonderful, positivity, expertise, regarded'):
        st.write('You selected:', keyword)
        Process_URL2()
        
   
    
elif option == 'Cover Letter Email Template':
    
    URL1 = "https://www.thebalancecareers.com/email-cover-letter-samples-2060246"
    div_id1 = "mntl-sc-block-callout-body_1-0-1"
    URL2 = "https://www.thebalancecareers.com/how-to-address-a-cover-letter-2060281"
    div_id2 = "mntl-sc-block-callout-body_1-0-5"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
    
        phr1 = "Store Manager Position"
        temp1 = extract1.replace(str(phr1),"[Role you are applying for]")
        
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
        
        phr8 = "I read"
        temp8 = temp7.replace(str(phr8), "\n\tI read")
        
        phr9 = "Dear"
        temp9 = temp8.replace(str(phr9), "\n\nDear")
        
        phr10 = "I can offer"
        temp10 = temp9.replace(str(phr10), "\nI can offer")
        
        phr11 = "Over"
        temp11 = temp10.replace(str(phr11), "\nOver")
        
        phr12 = "Ability"
        temp12 = temp11.replace(str(phr12), "\nAbility")
        
        phr13 = "In addition"
        temp13 = temp12.replace(str(phr13), "\n\nIn addition")
        
        phr14 = "My broad"
        temp14 = temp13.replace(str(phr14), "\nMy broad")
        
        phr15 = "I look"
        temp15 = temp14.replace(str(phr15), "\nI look")
        
        # Parse the text with spaCy
        spacy_text4 = nlp(temp15)
        
        Word_Frequency(spacy_text4)
        
        POS_Tag(spacy_text4)
        sts.visualize_tokens(spacy_text4, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template
        template4 = FindnReplace4(spacy_text4)
             
        st.subheader("**Your Template for Cover Letter Email**\n")
        st.text(template4)
        
    def Process_URL2():
        extract2 = Webscrape_divID(URL2, div_id2)
        
        phr = "Dear"
        temp = extract2.replace(str(phr), "\nDear")
        
        phr1 = "03060555-555-5555mary.garcia@email.com"
        temp1 = temp.replace(str(phr1), "[Your Contact Number and Email ID]\n")
        
        phr2 = "operations assistant/associate"
        temp2 = temp1.replace(str(phr2), "[Role in which you have experience]")
        
        phr3 = "operations assistant"
        temp3 = temp2.replace(str(phr3), "[Role you are applying for]")
        
        phr4 = "orders, resolved customer issues, ordered supplies, and prepared reports"
        temp4 = temp3.replace(str(phr4), "[Your responsibilities at your leaving company]")
        
        phr5 = "bookkeeping, data entry, and sales support"
        temp5 = temp4.replace(str(phr5), "[Your prior job nature]")
        
        phr6 = "Strong communication skills, in person, in writing, and on the phone"
        temp6 = temp5.replace(str(phr6), "\n[Your Skillset]")
        
        phr7 = "Excellent attention to detail and organization skills"
        temp7 = temp6.replace(str(phr7), "-")
        
        phr8 = "Top-notch customer service"
        temp8 = temp7.replace(str(phr8), "-")
        
        phr9 = "Experience in the industry and passion for the product"
        temp9 = temp8.replace(str(phr9), "-")
        
        phr10 = "Adept at all the usual professional software, including Microsoft Office Suite"
        temp10 = temp9.replace(str(phr10), "-")
        
        phr11 = "I’ve included"
        temp11 = temp10.replace(str(phr11), "\n\nI’ve included")
        
        phr12 = "Basically"
        temp12 = temp11.replace(str(phr12), "\nBasically")
        
        phr13 = "I was excited"
        temp13 = temp12.replace(str(phr13), "\n\tI was excited")
        
        phr14 = "CBI Industries39 Main"
        temp14 = temp13.replace(str(phr14), "")
        
        phr15 = "In my most"
        temp15 = temp14.replace(str(phr15), "\nIn my most")
        
        phr16 = "My other"
        temp16 = temp15.replace(str(phr16), "\nMy other")
        
        phr17 = "(hard copy letter)"
        temp17 = temp16.replace(str(phr17), "\n")
        
        
        # Parse the text with spaCy
        spacy_text4a = nlp(temp17)
    
        Word_Frequency(spacy_text4a)
        
        POS_Tag(spacy_text4a)
        sts.visualize_tokens(spacy_text4a, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template
        template4a = FindnReplace4a(spacy_text4a)
             
        st.subheader("**Your Template for Cover Letter Email**\n")
        st.text(template4a)
        
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('qualifications, seeking, gracious, superior',\
                                                'excited, smoothly, recent, previous'))
        
    if(keyword == 'qualifications, seeking, gracious, superior'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'excited, smoothly, recent, previous'):
        st.write('You selected:', keyword)
        Process_URL2()
        


elif option == 'Employee work appreciation Email Template':
    
    URL1 = "https://talkroute.com/7-sample-thank-you-notes-for-business/"
    div_id1 = "x-content-band-5"
    URL2 = "https://www.thebalancecareers.com/appreciation-email-samples-2059555"
    div_id2 = "mntl-sc-block-callout-body_1-0-4"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
    
        phr1 = "You showed"
        temp1 = extract1.replace(str(phr1),"\nYou showed")
        
        phr2 = "I am"
        temp2 = temp1.replace(str(phr2),"\nI am")
        
        phr3 = "Thank you"
        temp3 = temp2.replace(str(phr3),"\n\tThank you")
        
        # Parse the text with spaCy
        spacy_text5 = nlp(temp3)
        
        Word_Frequency(spacy_text5)
        
        POS_Tag(spacy_text5)
        sts.visualize_tokens(spacy_text5, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template    
        template5 = FindnReplace5(spacy_text5)
        
        st.subheader("**Your Template for Employee Work Appreciation Email**\n")
        st.text(template5)
    
    
    def Process_URL2():
        extract2 = Webscrape_divID(URL2, div_id2)
    
        phr1 = "Subject Line: Thank You Very Much!"
        temp1 = extract2.replace(str(phr1), "Subject Line: Thank You Very Much!\n")
        
        phr2 = "I wanted"
        temp2 = temp1.replace(str(phr2), "\n\tI wanted")
        
        phr3 = "I know how"
        temp3 = temp2.replace(str(phr3), "\nI know how")
        
        phr4 = "You are a"
        temp4 = temp3.replace(str(phr4), "\nYou are a")
        
        phr5 = "Best"
        temp5 = temp4.replace(str(phr5), "\n\nBest")
        
        # Parse the text with spaCy
        spacy_text5a = nlp(temp5)
        
        Word_Frequency(spacy_text5a)
        
        POS_Tag(spacy_text5a)
        sts.visualize_tokens(spacy_text5a, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template    
        template5a = FindnReplace5a(spacy_text5a)
        
        st.subheader("**Your Template for Employee Work Appreciation Email**\n")
        st.text(template5a)
        
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('tremendous, busy, depend, exceptional',\
                                                'appreciated, effort, satisfied, contributions'))
        
    if(keyword == 'tremendous, busy, depend, exceptional'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'appreciated, effort, satisfied, contributions'):
        st.write('You selected:', keyword)
        Process_URL2()
    

elif option == 'Out of Office Email Template':
   
    URL1 = "https://www.ionos.com/digitalguide/e-mail/technical-matters/perfect-out-of-office-message-examples-and-templates/"
    div_id1 = "c118391"
    URL2 = "https://www.tenfold-security.com/en/outlook-out-of-office-different-user/"
    classname2 = "fusion-reading-box-container reading-box-container-2"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
    
        phrase = "Formal out of office reply with referral for customers"
        temp = extract1.replace(str(phrase),"")
        
        phr1 = "Feel free"
        temp1 = temp.replace(str(phr1),"\nFeel free")
        
        phr2 = "You can"
        temp2 = temp1.replace(str(phr2),"\nYou can")
        
        phr3 = "Thank you"
        temp3 = temp2.replace(str(phr3),"\nThank you")
        
        phr4 = "Thank you for your message"
        temp4 = temp3.replace(str(phr4), "\tThank you for your message")
        
        # Parse the text with spaCy
        spacy_text6 = nlp(temp4)
        
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
             
        st.subheader("**Your Template for Out of Office Email**\n")
        st.text(template6)
        
    def Process_URL2():
        extract2 = Webscrape_Classname(URL2, classname2)
    
        phr1 = "(555-555-1234)"
        temp1 = extract2.replace(str(phr1), "[Your Colleague's Phone Number]")
        
        phr2 = "(jane.doe@example.com)"
        temp2 = temp1.replace(str(phr2), "[Your Colleague's Email ID]")
        
        phr3 = "In urgent"
        temp3 = temp2.replace(str(phr3), "\nIn urgent")
        
        phr4 = "Your message"
        temp4 = temp3.replace(str(phr4), "\nYour message")
        
        # Parse the text with spaCy
        spacy_text6a = nlp(temp4)
        
        Word_Frequency(spacy_text6a)
        
        POS_Tag(spacy_text6a)
        sts.visualize_tokens(spacy_text6a, attrs=["text", "pos_", "dep_", "ent_type_"])
    
        # Generate Template
        template6a = FindnReplace6a(spacy_text6a)
    
        st.subheader("**Your Template for Out of Office Email**\n")
        st.text(template6a)
        
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('access, represent, assist, understanding',\
                                                'respond, urgent, matters, forwarded'))
        
    if(keyword == 'access, represent, assist, understanding'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'respond, urgent, matters, forwarded'):
        st.write('You selected:', keyword)
        Process_URL2()
        
    

elif option == 'Thank you note for Business Email Template':
    
    URL1 = "https://talkroute.com/7-sample-thank-you-notes-for-business/"
    div_id1 = "x-content-band-6"
    URL2 = "https://talkroute.com/7-sample-thank-you-notes-for-business/"
    div_id2 = "x-content-band-2"
    
    def Process_URL1():
        extract1 = Webscrape_divID(URL1, div_id1)
        
        phr1 = "I’m very"
        temp1 = extract1.replace(str(phr1), "\tI’m very")
    
        # Parse the text with spaCy
        spacy_text7 = nlp(temp1)
        
        Word_Frequency(spacy_text7)
        
        POS_Tag(spacy_text7)
        sts.visualize_tokens(spacy_text7, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template
        template7 = FindnReplace7(spacy_text7)
             
        st.subheader("**Your Template for Business Deal Closure Email**\n")
        st.text(template7)
        
    def Process_URL2():
        extract2 = Webscrape_divID(URL2, div_id2)
    
        phr1 = "great day!Sincerely"
        temp1 = extract2.replace(str(phr1), "great day!\nSincerely")
        phr2 = "Your friends"
        temp2 = temp1.replace(str(phr2), "\n\n[Your Name]")
        phr3 = "I’m delighted"
        temp3 = temp2.replace(str(phr3), "\n\n\tI’m delighted")
        phr4 = "We would"
        temp4 = temp3.replace(str(phr4), "\nWe would")
        phr5 = "You could"
        temp5 = temp4.replace(str(phr5), "\nYou could")
        phr6 = "(your business)"
        temp6 = temp5.replace(str(phr6), "\n[Your Company Name]")
        
        # Parse the text with spaCy
        spacy_text7a = nlp(temp6)
        
        Word_Frequency(spacy_text7a)
        
        POS_Tag(spacy_text7a)
        sts.visualize_tokens(spacy_text7a, attrs=["text", "pos_", "dep_", "ent_type_"])
        
        # Generate Template
        template7a = FindnReplace7a(spacy_text7a)
             
        st.subheader("**Your Template for Business Deal Closure Email**\n")
        st.text(template7a)
        
    st.write('**Please select the keyword set from the below options to generate the Template**')
    keyword = st.radio("Keyword-set Selection",('partnership, family, fruitful, business',\
                                                'delighted, customer, loyal, patronage'))
        
    if(keyword == 'partnership, family, fruitful, business'):
        st.write('You selected:', keyword)
        Process_URL1()
    
    elif(keyword == 'delighted, customer, loyal, patronage'):
        st.write('You selected:', keyword)
        Process_URL2()


