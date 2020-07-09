#import os
#print(os.getcwd())
#import re as regex
#import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt 


def mainprogramme():
    printlines(1)
    selection=input("Please select Mode-  \n            UPDATION - 1 :\n            REPORTS  - 2 :\n            QUIT     - 3 :")
    if int(selection)==1:
        update_mode=True
        add_records_menu()
        return
    elif int(selection)==2:
        update_mode=False
        show_records_menu()
        return
    else:
        print("Thanks for using.\nClosing App")
#        donot_quit=False
        return

districtshortNames=["ALP","EKM","IDK","KGD","KKD","KLM","KNR","KTM","MPM","PKD","PTA","TSR","TVM","WYD"]
districtNames={'ALP':"Alappuzha",
                'EKM':"Ernakulam",
                'IDK':"Idukki",
                'KGD':"Kasargod",
                'KKD':"Kozhikkode",
                'KLM':"Kollam",
                'KNR':"Kannur",
                'KTM':"Kottayam",
                'MPM':"Malappuram",
                'PKD':"Palakkad",
                'PTA':"Pathanamthitta",
                'TSR':"Thrissur",
                'TVM':"Thiruvananthapuram",
                'WYD':"Wayanad"}

def print_districts(name="ALL"):
    for x in districtshortNames:
        print(x," - ",districtNames[x])

def printlines(num=1):
    if num==1:
        print("---------------------------------------------------------------------------")
    else:
        print("===========================================================================")        


# ############################## UPDATION MENU STARTS HERE #############################
def add_records_menu():
    printlines(2)
    vk=True    #loop for records menu choice 10-50
    print("\n*****UPDATION MODE*****\n")
    while vk:
        print("Type your option :\n\n       '10' for Adding\n       '50' for Return to Main Menu\n\n")
        s=input("Enter  your Choice :-> ")
        if int(s)==10:
            add_records()            
        elif int(s)==50:
            mainprogramme()       
            vk=False
        else:
            print("Please select a valid option")
            mainprogramme()                   
            vk=False
    return

def add_records():
    todays=input("Enter date to update DD-MM-YYYY :")
    print_districts()
    num_dists=input("How many districts?\n Be verycareful while entering details.\n Enter Number of Districts (1-14) : ")
    print("Add for ",num_dists,": Districts")
    file_lastline=get_lastrecordline()
    covid19dataFile1=open("COVID19DATA.csv","a")
    #find the last 'IDX' number in the csv file. new data will be added with existing number +1
    new_index=last_IDX(file_lastline)+1
    for x in range(0,int(num_dists)):
        print(districtshortNames)
        z1=input("Type District code : " )
        z2=input("     Confirmed Nos : ")
        z3=input("     Recovered Nos : ")
        z4=input("        Active Nos : ")
        z5=input("         Death Nos : ")
        dataline1=str(new_index) + "," + str.upper(z1) + "," + str(todays) + "," + str.upper(z2) + ',' + str.upper(z3) + "," + str.upper(z4) + "," + str.upper(z5) + "\n"
        new_index+=1
        print("Updating:",dataline1)
        covid19dataFile1.write(dataline1)
    covid19dataFile1.close()
    ## future update need to check duplicate district while updating
    return

def get_lastrecordline():
    covid19dataFile=open("COVID19DATA.csv","a")
    file_lastline=covid19dataFile.tell()
    print("last line",file_lastline)
    covid19dataFile.close()
    return file_lastline

def last_IDX(file_lastline):
    file3=pd.read_csv("COVID19DATA.csv")
    mynewdf=pd.DataFrame(file3)
    num=mynewdf.loc[mynewdf.IDX.max()-1].IDX
    return num

'''
def print_lastrecord():
    codatatxt=open("COVID19DATA.csv","r")
    codatatxt.seek(file_lastline)
    sks=codatatxt.readlines()
    print(type(sks),": sks:",sks)
    lastNum=str(sks)
    lastNum=lastNum[2:5]
    lastNum2=int(lastNum)
    print("sky=",lastNum2)
    print("text:",lastNum2)
    return lastNum2 # returns last number to add one more

            '''
 

# ############################## REPORT MENU STARTS HERE #############################
def show_records_menu():
    ak=True    #loop for records menu choice 100-500
    printlines(2)
    print("\n*****VIEW MODE*****\n")
    printlines(1)    
    #opening file for easy and fast access
    file1=pd.read_csv("COVID19DATA.csv")
    mydf=pd.DataFrame(file1)
  
    while ak:
        print("\n You can Choose various reporting from the below options.\n Select it by choosing the 3 digit number.\n Close Plot window to return to app.\n       '100' for Current Status\n       '200' for DistrictWise \n       '300' for Recovery Trend\n       '400' for Confirmed Trend\n       '500' for Death Trend\n       '600' for Active Trend\n       '700' for Daywise Confirmation\n       '800' for Daywise Recovery\n       '1000' for Exit\n")
        s=input("Enter  your Choice :-> ")
        if int(s)==100:
            show_currentstatus(mydf)
        elif int(s)==200:
            show_districtwise(mydf)            
        elif int(s)==300:
            show_recoverytrend(mydf)            
        elif int(s)==400:
            show_confirmedtrend(mydf)            
        elif int(s)==500:
            show_deathtrend(mydf)            
        elif int(s)==600:
            show_activetrend(mydf)            
        elif int(s)==700:
            show_daywiseconfirmations(mydf)            
        elif int(s)==800:
            show_daywiserecovery(mydf)            
        else:
            print("Not selected a valid option. going back to previous Menu. Please select a valid Option")
            mainprogramme()
            ak=False
    return

# ############################## REPORT FUNDTIONS STARTS HERE #############################

def show_currentstatus(mydf):
    printlines(2)
    print("100 Showing current status")
    printlines(2)
    print("Data updated Till:",mydf.loc[mydf.IDX.max()-1].Date)
    myshowdf=mydf
    myshowdf["Currently Active"]=mydf.Confirmed-mydf.Recovered-mydf.Death
    myshowdf[['Confirmed','Recovered',"Currently Active",'Death']].sum().plot(kind="bar",legend=[mydf.columns],label="Kerala State Current Covid-19 Status",color=['blue',"green",'yellow',"red"])
    plt.show()
    return

def show_districtwise(mydf):
    printlines(2)    
    print("200 Showing District wise status")
    printlines(2)    
    mydf.groupby('District') [['District','Confirmed','Recovered','Death']].sum().plot(kind="bar",legend=[mydf.columns],color=["blue","green","red"])
    plt.show()
    return

def show_recoverytrend(mydf):
    printlines(2)    
    print("300 :Showing Recovery Trend")
    printlines(2)    
    mydf.set_index(mydf.IDX)
    mydf[mydf.Recovered>=0].groupby(mydf.District).Recovered.sum().plot.bar(x=mydf.District,y=mydf.Recovered,legend=[mydf.columns],color="green")
    plt.show()
    return

def show_confirmedtrend(mydf):
    printlines(2)    
    print("400 :Showing Current Status")
    printlines(2)    
    mydf.set_index(mydf.IDX)
    mydf[mydf.Confirmed >=0].groupby(mydf.District).Confirmed.sum().plot.bar(x=mydf.District, y=mydf.Confirmed,legend=[mydf.columns])
    plt.show()    
    return

def show_deathtrend(mydf):
    printlines(2)    
    print("500 :Showing Death Status")
    printlines(2)    
    mydf.set_index(mydf.IDX)
    mydf[mydf.Death >=0].groupby(mydf.District).Death.sum().plot.bar(x=mydf.District, y=mydf.Death,legend=[mydf.columns],color='red')
    plt.show()    
    return

def show_activetrend(mydf):
    printlines(2)    
    print("600 :Showing Current Status")
    printlines(2)    
    #calculate active casesTHIS  is tricky since the new additions are only for particular districts. so always need to check full data
    myshowdf=mydf
    myshowdf["CurrentlyActive"]=mydf.Confirmed-mydf.Recovered-mydf.Death
    myshowdf.groupby(myshowdf.District).CurrentlyActive.sum().plot(kind="bar",legend=[mydf.columns],label="Active Cases",color=['yellow'])
    plt.show()
    return

def show_daywiseconfirmations(mydf):
    printlines(2)    
    print("700 :Showing Daywise Confirmation Trend")
    printlines(2)    
    file2=pd.read_csv("COVID19DATA.csv")
    mynewdf=pd.DataFrame(file2)
    mynewdf['NewDate']=pd.to_datetime(mynewdf.Date,utc=False)
    mynewdf.set_index('NewDate')
    mynewdf.groupby('NewDate').Confirmed.sum().plot(kind="bar",legend=[mynewdf.columns],label="Daywise Confirmation Status")
    plt.show()
    return

def show_daywiserecovery(mydf):
    printlines(2)
    print("800 :Showing Daywise Recovery Trend")
    printlines(2)    
    file2=pd.read_csv("COVID19DATA.csv")
    mynewdf=pd.DataFrame(file2)
    mynewdf['NewDate']=pd.to_datetime(mynewdf.Date, utc=False)
    mynewdf.set_index('NewDate')
    mynewdf.groupby('NewDate').Recovered.sum().plot(kind="bar",legend=[mynewdf.columns],label="Daywise Recovered Status")
    plt.show()
    return


# ############################## PROGRAMME STARTS HERE #############################

printlines(2)
print("\n Welcome to State Covid Updator")
update_mode=False # common for below two
report_choice=True  # default report choice
#update_mode=0
#donot_quit=True
mainprogramme()