# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 18:21:54 2016
Pulls the location name and yearly totals for analysis and returns it in a list of dictionaries
@author: Connor Moore
"""

from geojsoncollection import toPoint, containCheck
import csv
import re



def csvScope(filename, neighborList ,returnList=[], nameString='LOCATION', monthString='YTD'): 
    #print(os.getcwd())
    regex = re.compile('[^a-zA-Z]')
    nameString = regex.sub('',nameString)
    monthString = regex.sub('',monthString)
    if nameString == '':
        nameString = "LOCATION"
    if monthString == '':
       monthString = "YTD"
    i=0
    for i in range(len(filename)):
#        print(i)
#        print(filename[i])
        numpat = re.compile('[^0-9]')
        year = numpat.sub('',filename[i])
        #print(year)
        f = open(filename[i])
        csv_f = csv.DictReader(f)    
        if nameString == 'LOCATION':
           j = 0
           for row in csv_f:
                   if row['ADDRESS'] == '':
                        break
                   else:
                        address = row['ADDRESS'] + ' Chicago'
                        point = toPoint(address)
                        check = containCheck(point, neighborList)
                   temp= {}
                   value = row[monthString.upper()]
                   if  value.isdigit():
                        temp = dict({'Library Name':row[nameString],'Address'  : address, monthString+', '+ year: value, 'Point': point})
                        temp.update(check)
                   else:
                        temp = dict({'Library Name':row[nameString],'Address'  : address, monthString+', '+ year: 0,'Point': point})
                        temp.update(check)
                   if i==0:
                        returnList.append(temp)
                   else:
                        name = row[nameString]
                        checker(name,returnList,temp)
                   j=j+1
                   #print(i,j, temp)                  
                
        else:
            for row in csv_f:
                if row['ADDRESS'] == '':
                    break
                else:
                    address = row['ADDRESS'] + ' Chicago'
                    point = toPoint(address)
                    check = containCheck(point, neighborList)
                orary = ''
                value = 0
                temp= {}
                if row[monthString.upper()].isdigit():
                   value = (int(row[monthString.upper()]))
                #will contain both the name and yearly totals.
                orary = (regex.sub('',row['LOCATION'])).lower()
                if orary == (nameString).lower():
                    temp = dict({'Library Name ': nameString.upper(), 'Address' : address,
                                monthString+', '+ year: value, 'Point': point })
                    temp.update(check)
                if i==0:
                    returnList.append(temp)
                else:
                    name = row[nameString]
                    checker(name,returnList,temp)
                j=j+1
                #print(i,j)
        f.close()
        i = i+1
    return returnList
    
    
def checker(name, returnList, temp, indexer=0):
    if indexer < len(returnList):
        keys = list(returnList[indexer].values())
        if name in keys:
            returnList[indexer].update(temp)
            return True
        else:
            return checker(name,returnList,temp,(indexer+1))
    else:
        returnList.append(temp)
        return False
    