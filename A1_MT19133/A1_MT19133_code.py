# -*- coding: utf-8 -*-
"""InvertedIndex.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u1-w59_DjnUEJ1tQoEZnCxcIuNVuM_p-
"""

import glob
from nltk.tokenize import RegexpTokenizer
import os
Dict = {} 
tokenizer = RegexpTokenizer(r'\w+')
for filename in glob.glob("*"):
  if not os.path.isdir(filename):
    text = open(filename,"r+",errors='ignore') 
    var=(text.read())
    words=tokenizer.tokenize(var)
  
    for word in words:
      if word.lower() in Dict:
        val=Dict.get(word.lower())
        if filename not in val:
          val.append(filename)
          val.sort()
          Dict.update({word.lower():val})
      else:
        List=[filename]
        Dict.update({word.lower():List})

temp={}
for key in sorted(Dict.keys()):
    temp.update({key :Dict[key]})
Dict=temp

print((Dict))

query=input("Enter query")
words=query.split()

listy=[]
temp=0
comp=0

for i in range(0,len(words)):
  if words[i].lower() == 'or':
    T=[]
    for j in range(temp,i):
      if words[j].lower() != 'and' :        
        T.append(words[j].lower())
    for m in range(0,len(T)):
      if T[m]=='not':
        T[m+1]=T[m+1].upper()    
    listy.append(T)
    temp=i+1
T=[]
for k in range(temp,len(words)):
  if words[k].lower() != 'and' :
    T.append(words[k].lower())
for m in range(0,len(T)):
      if T[m]=='not':
        T[m+1]=T[m+1].upper()  
listy.append(T)

listz=[]

for t_list in listy:
  T=[]
  for item in t_list:
    if item != 'not':
      T.append(item)
  listz.append(T)

print(listz)


########################################################
#Code to take intersection or union of the posting lists 
########################################################
import operator

postings=[]

for item in listz:
  d={}
  for val in item:
    d.update({val:len(Dict.get(val.lower()))})
  sorted_d = sorted(d.items(), key=operator.itemgetter(1))

  if len(sorted_d)!=1 :
    result=[]
    if sorted_d[0][0].isupper()==True and sorted_d[1][0].isupper()==True :
      i=0
      flag=0
      kai=[]
      for item in sorted_d:
        Data=item[0]
        #print(Data)
        if Data.islower()== True:
          flag=1
          break
        else:
          i=i+1

      if flag==1 :

        pos=i    
        kai.append(sorted_d[pos])

        p=0
        for item in sorted_d:
          if item !=sorted_d[pos]:
            kai.append(item)
            p=p+1
        
        sorted_d=kai
    L1=Dict.get(sorted_d[0][0].lower())
    L2=Dict.get(sorted_d[1][0].lower())

    if sorted_d[0][0].islower() ==True and  sorted_d[1][0].islower() ==True :
      result,c=X_AND_Y(L1,L2) 
      comp=comp+c
    if sorted_d[0][0].islower() ==True and  sorted_d[1][0].isupper() ==True :
      result,c=X_AND_NOT_Y(L1,L2) 
      comp=comp+c 
    if sorted_d[0][0].isupper() ==True and  sorted_d[1][0].islower() ==True :
      result,c=X_AND_NOT_Y(L2,L1)
      comp=comp+c
    if sorted_d[0][0].isupper() ==True and  sorted_d[1][0].isupper() ==True :
      result,c=Not_X_AND_NOT_Y(L1,L2)
      comp=comp+c
    for i in range(2,len(sorted_d)):
      if sorted_d[i][0].isupper ==True:
        result,c=X_AND_Not_Y(result,Dict.get(sorted_d[i][0].lower()))
        comp=comp+c
      if sorted_d[i][0].islower ==True:
        result,c=X_AND_Y(result,Dict.get(sorted_d[i][0].lower()))
        comp=comp+c
    postings.append(result) 
    

  else:
    if sorted_d[0][0].islower() == True:
      postings.append(Dict.get(sorted_d[0][0].lower()))
      
    else:    
      corpus=[]
      second_list=[]
      for filename in glob.glob("*"):

        if not os.path.isdir(filename):
          corpus.append(filename)
      
      L2=Dict.get(sorted_d[0][0].lower())
      for filename in corpus:
        if filename not in L2:
          second_list.append(filename)
          comp=comp+1
      postings.append(second_list)


if len(postings) > 1:

  L1=postings[0]
  L2=postings[1]
  final,c=X_OR_Y(L1,L2)
  comp=comp+c
  for i in range(2,len(postings)):
    final,c=X_OR_Y(final,postings[i])
    comp=comp+c

  

  print(("Number of documents returned: ",len(final)))
  print(("List of documents returned: ",final)) 
  print("TOtal number of comparisions",comp)  
else:
  length=0
  for items in postings:
    for item in items:
      length=length+1
  print("Number of documents returned: ",length) 
  print("List of documents returned: ",(postings))
  print("TOtal number of comparisions",comp)

#And Query

def X_AND_Y(L1,L2):
  try:
    result=[]
    #print(L1)
    #print(L2)
    p1=0
    p2=0
    comp=0
    while p1 <= len(L1)-1 and p2 <= len(L2)-1:
      if L1[p1] == L2[p2]:
        result.append(L1[p1])
        p1=p1+1
        p2=p2+1
        comp=comp+1
      else:
        if L1[p1] < L2[p2] :
          p1= p1+1
          comp=comp+1
        else:
          p2=p2 +1
          comp=comp+1


    
    return(result,comp)
  except:
    print("Sorry!! some error occured!!")

##Calling And Function
x = input("Enter value of X: ") 
y = input("Enter value of Y: ")
L1=Dict.get(x.lower())
L2=Dict.get(y.lower())
result=And(L1,L2)  
print(result)

#OR Query


def X_OR_Y(L1,L2):
  try:
    result=[]
    p1=0
    p2=0
    #print(len(L1))
    #print(len(L2))
    comp=0

    while p1 <= len(L1)-1 or p2 <= len(L2)-1:
      if p1>len(L1)-1 :
        while p2<=len(L2)-1 :
          result.append(L2[p2])
          p2=p2+1
        break
      
      if p2>len(L2)-1 :
        while p1<=len(L1)-1 :
          result.append(L1[p1])
          p1=p1+1
        break
      
      
      if L1[p1] == L2[p2]:
        result.append(L1[p1])
        p1=p1+1
        p2=p2+1
        comp=comp+1
      else:
        if L1[p1] < L2[p2] :
          result.append(L1[p1])
          p1= p1+1
          comp=comp+1
          

        else:
          result.append(L2[p2])
          p2=p2 +1
          comp=comp+1
          


    return(result,comp)
  except:
    print("Sorry!! some error occured.")

x = input("Enter value of X: ") 
y = input("Enter value of Y: ")
L1=Dict.get(x.lower())
L2=Dict.get(y.lower())
print(X_OR_Y(L1,L2))

#x AND NOT y
def X_AND_NOT_Y(L1,L2):
  try:
    result=[]
  
    p1=0
    p2=0
    #print(L1)
    #print(L2)
    comp=0
    while p1 <= len(L1)-1 and p2 <= len(L2)-1 :
      if L1[p1]== L2[p2]:
        p1=p1+1
        p2=p2+1
        comp=comp+1
      else:
        if L1[p1]<L2[p2]:
          result.append(L1[p1])
          p1=p1+1
          comp=comp+1
        else:
          p2=p2+1
          comp=comp+1

    if p1<= len(L1)-1 and p2 > len(L2)-1 and L1[p1]>L2[p2-1]:
      result.append(L1[p1])
      comp=comp+1
    return(result,comp)
  except:
    print("some error occured! ")

x = input("Enter value of X: ") 
y = input("Enter value of Y: ")
L1=Dict.get(x.lower())
L2=Dict.get(y.lower())
print(X_AND_NOT_Y(L1,L2))

def Not_X_AND_NOT_Y(L1,L2):
  try:
    result=[]
    p1=0
    p2=0
    #print(len(L1))
    #print(len(L2))
    comp=0

    while p1 <= len(L1)-1 or p2 <= len(L2)-1:
      if p1>len(L1)-1 :
        while p2<=len(L2)-1 :
          result.append(L2[p2])
          p2=p2+1
        break
      
      if p2>len(L2)-1 :
        while p1<=len(L1)-1 :
          result.append(L1[p1])
          p1=p1+1
        break
      
      
      if L1[p1] == L2[p2]:
        result.append(L1[p1])
        p1=p1+1
        p2=p2+1
        comp=comp+1
      else:
        if L1[p1] < L2[p2] :
          result.append(L1[p1])
          p1= p1+1
          comp=comp+1

        else:
          result.append(L2[p2])
          p2=p2 +1
          comp=comp+1


    corpus=[]

    second_list=[]

    for filename in glob.glob("*"):
      if not os.path.isdir(filename):
        corpus.append(filename)

    for filename in corpus:
      if filename not in result:
        second_list.append(filename)
        comp=comp+1
    return(second_list,comp)
  except:
    print("Sorry!! some error occured.")

#x OR NOT y
try:
  x = input("Enter value of X: ") 
  y = input("Enter value of Y: ")

  result=[]
  L1=Dict.get(x.lower())
  L2=Dict.get(y.lower())

  p1=0
  p2=0
  corpus=[]

  second_list=[]

  for filename in glob.glob("*"):
    if not os.path.isdir(filename):
      corpus.append(filename)

  for filename in corpus:
    if filename not in L2:
      second_list.append(filename)

  L2=second_list

  while p1 <= len(L1)-1 or p2 <= len(L2)-1:
    
    if p1>len(L1)-1 :
      while p2<=len(L2)-1 :
        result.append(L2[p2])
        p2=p2+1
      break
    
    if p2>len(L2)-1 :
      while p1<=len(L1)-1 :
        result.append(L1[p1])
        p1=p1+1
      break
    
    
    if L1[p1] == L2[p2]:
      result.append(L1[p1])
      p1=p1+1
      p2=p2+1
    else:
      if L1[p1] < L2[p2] :
        result.append(L1[p1])
        p1= p1+1
        

      else:
        result.append(L2[p2])
        p2=p2 +1
        
  print((result))
except:
  print("Some error occured!!!")

###Phrase queries using positional indexing


from nltk.tokenize import RegexpTokenizer 
import operator
query = input("Enter phrase query: ")

outerfunc(query)

def outerfunc(query):


  tokenizer = RegexpTokenizer(r'\w+')
  words=tokenizer.tokenize(query)
  query_terms=[]
  for word in words:
    query_terms.append(word.lower())

  dict1={}
  for qt in query_terms:
    temp=Dict.get(qt)
    dict1.update({qt:len(temp)})

  #sorted query terms by document frequency
  sorted_d = sorted(dict1.items(), key=operator.itemgetter(1))
  print('Dictionary in ascending order by value : ',sorted_d)
  if len(sorted_d) == 1:
    print(Dict.get(sorted_d[0][0]))
    return 
  result=[]
  ###Def for intersection
  def intersection(L1,L2):
    try:
      p1=0
      p2=0

      while p1 <= len(L1)-1 and p2 <= len(L2)-1:
        if L1[p1] == L2[p2]:
          result.append(L1[p1])
          p1=p1+1
          p2=p2+1
        else:
          if L1[p1] < L2[p2] :
            p1= p1+1
          else:
            p2=p2 +1

      return result
    except:
      print("some error occured1")

  try:
    L1=Dict.get(sorted_d[0][0])
    L2=Dict.get(sorted_d[1][0])

    result=intersection(L1,L2)
    
    for i in range(2,len(sorted_d)):
      result=intersection(result,sorted_d[i])

    ##result contains list of docs which contain all query terms in them but not necessarily in form of phrase
    print(result)

    list1 = [[]]*len(query_terms)
    i=0

    farzi=[]
    for item in sorted_d:
      farzi.append(item[0])
  except:
    print("some error occured2")
  #print(farzi)
  
  try:

    for qt in query_terms :
      temp=[]
      for doc in result:
        text = open(doc,"r+",errors='ignore') 
        var=(text.read())
        words=tokenizer.tokenize(var.lower())
        index=0
        I=[]
        for word in words:
          index=index+1
          if word== qt:
            I.append(index)
        temp.append(I)
      list1[i].append(temp)
      i=i+1

  except:
    print("some error occured3!!")
  print(list1[0])

  #try:

  listx=[[]]*len(query_terms)
  answer=[]
  for j in range(0,len(result)):
    for i in range(0,len(query_terms)):
      listx[i]=list1[0][i][j]
    ret=khatarnak(listx,query_terms)
    if ret ==1:
      answer.append(result[j])  
  #except:
   # print("Some error occured4!")



  print("Final result list",answer)

def khatarnak(listx,query_terms):

  ##Nested loop to calculate consecutive positions
  try:


    index=len(query_terms)
    index=index-1
    for item1 in listx[0]:
      for item2 in listx[1]:
        if index >2 :
          for item3 in listx[2]:
            if index>3:
              for item4 in listx[3]:
                if index>4:
                  for item5 in listx[4]:
                    if item5 ==item4 +1 and item4==item3+1 and item2==item1+1 and item3 ==item2+1:
                      return 1
                else:
                  if item4==item3+1 and item2==item1+1 and item3 ==item2+1:
                    return 1
            else:
              if item2==item1+1 and item3 ==item2+1:
                return 1
        else:
          if item2 ==item1+1:
            return 1
  except:
    print("Sorry shaktimaan !")
  return 0

import csv

#dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}
w = csv.writer(open("output.csv", "w"))
for key, val in Dict.items():
    w.writerow([key, val])