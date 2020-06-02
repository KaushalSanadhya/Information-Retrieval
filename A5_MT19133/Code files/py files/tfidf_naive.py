# -*- coding: utf-8 -*-
"""IR_A5_TFIDF_Naive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ocRnrIO3j0CVCEflynOoXTCQ7mc6vkF5
"""

## Cell 0 ##

cat_list=["comp.graphics","rec.sport.hockey","sci.med","sci.space","talk.politics.misc"]
import pickle

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# UNCOMMENT these three pickle files for executing the code for (80:20) split. Give path to the pickled files.  #

#pickle_in = open("PATH OF classes_list(80:20).pickle FILE","rb")
#classes_list =pickle.load(pickle_in)

#pickle_in = open("PATH OF Global(80:20).pickle FILE","rb")
#GLOBAL =pickle.load(pickle_in)

#pickle_in = open("PATH OF xTest(80:20).pickle FILE","rb")
#xTest =pickle.load(pickle_in)



#pickle_in = open("PATH OF tf_idf(80:20).pickle FILE","rb")
#tf_idf =pickle.load(pickle_in)



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++






#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# UNCOMMENT these three pickle files for executing the code for 70:30 split. Give path to the pickled files. #

#pickle_in = open("PATH OF classes_list(70:30).pickle FILE","rb")
#classes_list =pickle.load(pickle_in)

#pickle_in = open("PATH OF Global(70:30).pickle FILE","rb")
#GLOBAL =pickle.load(pickle_in)

#pickle_in = open("PATH OF xTest(70:30).pickle FILE","rb")
#xTest =pickle.load(pickle_in)

#pickle_in = open("PATH OF tf_idf(70:30).pickle FILE","rb")
#tf_idf =pickle.load(pickle_in)



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# UNCOMMENT these three pickle files for executing the code for (50:50) split. Give path to the pickled files. #

#pickle_in = open("PATH OF classes_list(50:50).pickle FILE","rb")
#classes_list =pickle.load(pickle_in)

#pickle_in = open("PATH OF Global(50:50).pickle FILE","rb")
#GLOBAL =pickle.load(pickle_in)

#pickle_in = open("PATH OF xTest(50:50).pickle FILE","rb")
#xTest =pickle.load(pickle_in)

#pickle_in = open("PATH OF tf_idf(50:50).pickle FILE","rb")
#tf_idf =pickle.load(pickle_in)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Execution sequence of this python  code using pickled results

# Cell 1 --> Cell 2 --> Cell 3 -->Cell 4-->cell 10-->cell 11-->cell 12--->Cell 13--> Cell 14 --> Cell 15-->Cell 16
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

### Cell 1 ###
##importing  nltk##

import nltk
nltk.download('punkt')

#Cell 2 #
##installing num2words ##
pip install num2words

#Cell 3 #
#Importing all esentials#

from nltk.stem import PorterStemmer 
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize 
import numpy as np
import glob
from sklearn.utils import shuffle
import os
from num2words import num2words
from nltk.corpus import stopwords 
import pickle
import math
import operator
from sklearn.manifold import TSNE
import seaborn as sns
import matplotlib.pyplot as plt 
import random 
from sklearn.model_selection import train_test_split
import pandas as pd  

ps = PorterStemmer() 
tokenizer = RegexpTokenizer(r'\w+')

## CELL 4  ##
## Download stopwords ##

import nltk
nltk.download('stopwords')

## Cell 5 ##
##Splitting into Test & Train RANDOMLY using Test Train Split and shuffle ###


Data=pd.DataFrame(columns = ["file_name", "class"])
cat_list=["comp.graphics","rec.sport.hockey","sci.med","sci.space","talk.politics.misc"]


for group in cat_list:
  for filename in glob.glob("drive/My Drive/IR4/"+group+"/*"):
    
    length=len(filename)
    j=0
    for k in range(length-1,-1,-1):
      if filename[k]=='/':
        j=k
        break
  
    Data=Data.append({"file_name":filename[j+1:len(filename)],"class":group},ignore_index=True)
##Shuffling and split ##
Data = shuffle(Data)
x=Data["file_name"]
y=Data["class"]
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.2, random_state = 12)

## Cell 6 ##
#pickle_out = open("drive/My Drive/xTest(70:30).pickle","wb")
#pickle.dump(xTest, pickle_out)
#pickle_out.close()

##  Cell 7 ##
# # Train Data pre processing ##

stop_words = set(stopwords.words('english')) 
cat_list=["comp.graphics","rec.sport.hockey","sci.med","sci.space","talk.politics.misc"]
GLOBAL=[]
classes_list={}
for group in cat_list:
  global_doc=[]
  for filename in glob.glob("drive/My Drive/IR4/"+group+"/*"):
    
    length=len(filename)
    j=0
    for k in range(length-1,-1,-1):
      if filename[k]=='/':
        j=k
        break
    print(filename[j+1:len(filename)])
    if filename[j+1:len(filename)] in list(xTrain):
      if not os.path.isdir(filename):
        text = open(filename,"r+",errors='ignore') 
        var=(text.read())
        var=var.replace(',','')
        words_tokens=tokenizer.tokenize(var)
        words = [w for w in words_tokens if not w in stop_words] 
      
        Words=[]
        for w in words:
          if w.isdigit():
            Words.append(ps.stem(num2words(w)))
            GLOBAL.append(ps.stem(num2words(w)))
          else:
            Words.append(ps.stem(w))
            GLOBAL.append(ps.stem(w))
      global_doc.append(Words)
  classes_list.update({group:global_doc})


pickle_out = open("drive/My Drive/classes_list(80:20).pickle","wb")
pickle.dump(classes_list, pickle_out)
pickle_out.close()

## Cell 8 ##

## Fetch various essential variables which were pickled earliar ##


#cat_list=["comp.graphics","rec.sport.hockey","sci.med","sci.space","talk.politics.misc"]
#pickle_in = open("drive/My Drive/classes_list(70:30).pickle","rb")
#classes_list =pickle.load(pickle_in)

#pickle_in = open("drive/My Drive/Global(70:30).pickle","rb")
#GLOBAL =pickle.load(pickle_in)

#pickle_in = open("drive/My Drive/xTest(70:30).pickle","rb")
#xTest =pickle.load(pickle_in)

#Global_unique=np.unique(GLOBAL)

## Cell 9 ##
### Calculating TF-IDF score of each tuple (term,class). ###

tf_idf=[]

Global_unique=np.unique(GLOBAL)

for term in Global_unique:
  df=0
  for key in classes_list.keys():
    docs=classes_list.get(key)
    for doc in docs:
      if term in doc:
        df=df+1
        break
  #print(df,term)
  df=math.log((5/df),10)  

  for clas in cat_list:
    tf=0
    docs=classes_list.get(clas)
    for doc in docs:
      tf=tf+doc.count(term)
    
    tf=1+math.log((tf+1),10)
    print(tf*df,term)
    tf_idf.append(tuple([term,clas,tf*df]))

## Cell 10 ##
#### selecting the value of number of features (K) .I have selected 1/5 of total selected features###

#pickle_in = open("drive/My Drive/tf_idf(70:30).pickle","rb")
#tf_idf =pickle.load(pickle_in)
Global_unique=np.unique(GLOBAL)
tf_idf1=[]
tf_idf2=[]
tf_idf3=[]
tf_idf4=[]
tf_idf5=[]

for item in tf_idf:
  if item[1]==cat_list[0]:
    #print("Hi1")
    tf_idf1.append(item)
  if item[1]==cat_list[1]:
    tf_idf2.append(item)
    #print("Hi2")
  if item[1]==cat_list[2]:
    tf_idf3.append(item)
   # print("Hi3")
  if item[1]==cat_list[3]:
    tf_idf4.append(item)
   # print("Hi4")
  if item[1]==cat_list[4]:
    tf_idf5.append(item)
   # print("Hi5")

tf_idf1.sort(key=lambda elem : elem[2],reverse=True)
tf_idf2.sort(key=lambda elem : elem[2],reverse=True)
tf_idf3.sort(key=lambda elem : elem[2],reverse=True)
tf_idf4.sort(key=lambda elem : elem[2],reverse=True)
tf_idf5.sort(key=lambda elem : elem[2],reverse=True)


length=(len(tf_idf1))
length=length/2

TF_IDF=[]
TF_IDF.append(tf_idf1[0:int(length)])
TF_IDF.append(tf_idf2[0:int(length)])
TF_IDF.append(tf_idf3[0:int(length)])
TF_IDF.append(tf_idf4[0:int(length)])
TF_IDF.append(tf_idf5[0:int(length)])

##Cell 11 ##
## Calculating denominator of naive byes for each class ##

denominator=[] 
probab=[]
keys=list(classes_list.keys())
for i in range(0,len(TF_IDF)):
  List=TF_IDF[i]
  d=0
  docs=classes_list.get(keys[i])
  for term in List:
    ct=0
    for doc in docs:
      ct=ct+doc.count(term[0])
    #print(ct)
    probab.append(tuple([term[0],keys[i],ct]))
    d=d+ct
  #print("d",d)
  denominator.append(d)

## Cell 12 ##
## printing denominator for each class ##
print(denominator)

## Cell 13 ##
## Calcuating probability for each (class,term) pair ##

probab1={}
probab2={}
probab3={}
probab4={}
probab5={}

for item in probab:
  if item[1]==cat_list[0]:
    probab1.update({item[0]:item[2]})
  if item[1]==cat_list[1]:
    probab2.update({item[0]:item[2]})
  if item[1]==cat_list[2]:
    probab3.update({item[0]:item[2]})
  if item[1]==cat_list[3]:
    probab4.update({item[0]:item[2]})
  if item[1]==cat_list[4]:
    probab5.update({item[0]:item[2]})

## Cell 14 ##
## Pre-processing Test Docs ##

stop_words = set(stopwords.words('english')) 
cat_list=["comp.graphics","rec.sport.hockey","sci.med","sci.space","talk.politics.misc"]
m=0
docs_list=[]
for group in cat_list:
  for filename in glob.glob("drive/My Drive/IR4/"+group+"/*"):
    
    length=len(filename)
    j=0
    for k in range(length-1,-1,-1):
      if filename[k]=='/':
        j=k
        break
    #print(filename[j+1:len(filename)])
    if filename[j+1:len(filename)] in list(xTest):
      m=m+1
      print(m)
      if not os.path.isdir(filename):
        text = open(filename,"r+",errors='ignore') 
        var=(text.read())
        var=var.replace(',','')
        words_tokens=tokenizer.tokenize(var)
        words = [w for w in words_tokens if not w in stop_words] 
      
        Words=[]
        for w in words:
          if w.isdigit():
            Words.append(ps.stem(num2words(w)))
            
          else:
            Words.append(ps.stem(w))
            
      docs_list.append(tuple([Words,group]))

## Cell 15 ##
## Naive logic to find the class of each test doc accoring to Max probability ##
actual=[]
predicted=[]
B=len(Global_unique)
correct=0
for test in docs_list:
  max_arg=0
  p1=0
  p2=0
  p3=0
  p4=0
  p5=0
  for token in test[0]:
    if token in probab1.keys():
     # print(probab1.get(token))
      p1=p1+((probab1.get(token)+1)/(denominator[0]+B))
    if token in probab2.keys():
      p2=p2+((probab2.get(token)+1)/(denominator[1]+B))
    if token in probab3.keys():
      p3=p3+((probab3.get(token)+1)/(denominator[2]+B))
    if token in probab4.keys():
      p4=p4+((probab4.get(token)+1)/(denominator[3]+B))
    if token in probab5.keys():
      p5=p5+((probab5.get(token)+1)/(denominator[4]+B))

  T=list()
    
  T.append(p1)
  T.append(p2)
  T.append(p3)
  T.append(p4)
  T.append(p5)
  Index=T.index(max(T))
  actual.append(test[1])
  predicted.append(cat_list[Index])
  if cat_list[Index]==test[1]:
    correct=correct+1

## Cell 16 ##
## Calculating Accuracy and Confusion Matrix ##

accuracy=((correct*100)/len(docs_list))
print(accuracy)


from sklearn.metrics import confusion_matrix 

CM=confusion_matrix(actual, predicted)
print(CM)


#pickle_out = open("drive/My Drive/confusion_matrix_tfidf_Naive(70:30).pickle","wb")
#pickle.dump(CM, pickle_out)
#pickle_out.close()


#pickle_out = open("drive/My Drive/accuracy_tfidf_Naive(70:30).pickle","wb")
#pickle.dump(accuracy, pickle_out)
#pickle_out.close()