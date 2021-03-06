# -*- coding: utf-8 -*-




import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import time 
import datetime
# creazione matrice
import pandas as pd
#import datetime as dt
import numpy as np
from random import shuffle
#import logging, sys
#from logging import handlers

begin = time.time()

pd.options.mode.chained_assignment = None 

Dateflag=True
#maxTotal=2815
maxTotal=input("Please insert the value of the bigger activity that Optima can manage: ")
maxTotal=int(maxTotal)
warningcounter=0
problemscounter=0
listsheetscapacityEXT=['SSO', 'PRIMARY', 'SECONDARY', 'SPECIAL 1', 'SPECIAL 2', 'SPECIAL 3', 'SPECIAL 4', 'SPECIAL 5', 'SPECIAL 6', 'HIRING', 'Country', 'Region', 'SUPPLIER NAME', 'WTR']
listsheetscapacity=['Technician/Equipment: SSO ID', 'PRIMARY', 'SECONDARY', 'SPECIAL 1', 'SPECIAL 2', 'SPECIAL 3', 'SPECIAL 4', 'SPECIAL 5', 'SPECIAL 6', 'Billable date', 'Country', 'Region', 'Employer', 'WTR', 'IS GLOBAL']
listsheetsdemand=["Activity Unique Id", "Prime Contractor","Region","Country", "Technical Skill", "Days Per Week", "Hours Per Day","Activity Start Date",	"Activity End Date", "Total", "SSO" ]
listsheestkt=['LT_ST_Countries', 'LegalEntityRestrictions', 'MobilizationLeadTime', 'CostMatrixForSupplier', 'TECHNICAL SKILL', 'AreaRegionCountry','EXT_MobilizationLeadTime', 'EXT_percentuali']
flagKT=True
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("Report Cleaner"+".log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
        self.log.flush()

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        
        pass    

sys.stdout = Logger()


if os.path.isfile('./KT_REGOLE.xlsx')!=True:
    print("ERROR in 'KT_REGOLE.xlsx':"+" KT_REGOLE.xlsx doesn't exist or is written in wrong way"+"\n")
    problemscounter+=1
else:
    ktregolepd= pd.ExcelFile('KT_REGOLE.xlsx')
    for i in listsheestkt:
        if i not in ktregolepd.sheet_names:
            problemscounter+=1
            print("ERROR in 'KT_REGOLE.xlsx': "+ str(i)+" sheet doesn't exist or is written in wrong way"+"\n")
            print("the tool is not able to test other input files, please check 'KT_REGOLE.xlsx' '\n ")
            flagKT=False
            
    if flagKT==True:
        restrictionspd = pd.read_excel("KT_REGOLE.xlsx", sheet_name="LegalEntityRestrictions")
        restrictionspdtrue = restrictionspd.loc[restrictionspd['IsAllowed']==True]
        restrictionspdtrue.set_index(['PrimeContractor','Employer', 'InstallationCountry'], inplace=True)
        listrestrictions=restrictionspdtrue.index.tolist()
        restrictionspdtrue.reset_index(inplace =True)
        restrictions2pd = pd.read_excel("KT_REGOLE.xlsx", sheet_name="MobilizationLeadTime")
        restrictions2pd =restrictions2pd.loc[restrictions2pd['LeadTimeInDays'] ==1000]
        restrictions2pdEXT = pd.read_excel("KT_REGOLE.xlsx", sheet_name="EXT_MobilizationLeadTime")
        restrictions2pdEXT=restrictions2pdEXT.loc[restrictions2pdEXT['LeadTimeInDays'] ==1000]
        
#        restrictions2pd['FSECountry']=restrictions2pd['FSECountry'].str.strip()
#        restrictions2pd['InstallationCountry']=restrictions2pd['InstallationCountry'].str.strip()
#        restrictions2pd['FSECountry']=restrictions2pd['FSECountry'].str.title()
#        restrictions2pd['InstallationCountry']=restrictions2pd['InstallationCountry'].str.title()
#        
#        restrictions2pdEXT['SUPPLIER NAME']=restrictions2pdEXT['SUPPLIER NAME'].str.strip()
#        restrictions2pdEXT['Installation Country']=restrictions2pdEXT['Installation Country'].str.strip()
#        restrictions2pdEXT['SUPPLIER NAME']=restrictions2pdEXT['SUPPLIER NAME'].str.title()
#        restrictions2pdEXT['Installation Country']=restrictions2pdEXT['Installation Country'].str.title()
#        
        
        
        countriespd=pd.read_excel("KT_REGOLE.xlsx", sheet_name="LT_ST_Countries")
        costmatrixspd=pd.read_excel("KT_REGOLE.xlsx", sheet_name="CostMatrixForSupplier")
        skillpd=pd.read_excel("KT_REGOLE.xlsx", sheet_name="TECHNICAL SKILL")
        ARCpd=pd.read_excel("KT_REGOLE.xlsx", sheet_name="AreaRegionCountry")
        supplierpd= pd.read_excel("KT_REGOLE.xlsx", sheet_name="EXT_percentuali")
        
       

        
        listCountry=ARCpd['CountryName'].tolist()
        listRegion=ARCpd['Region'].unique().tolist()
        listPrimeContractor=restrictionspd['PrimeContractor'].unique().tolist()
        listSkill=skillpd['OPTIMA SKILL'].unique().tolist()
        listEmployer=restrictionspd['Employer'].unique().tolist()
        listSupplier=supplierpd['SUPPLIER NAME'].unique().tolist()
        
        listFSEcMLT=restrictions2pd['FSECountry'].unique().tolist()
        listINScMLT=restrictions2pd['InstallationCountry'].unique().tolist()
        for i in listFSEcMLT:
            if i not in listCountry:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx', sheet 'MobilizationLeadTime': '" + str(i)+ "' 'FSECountry' in is missing in 'AreaRegionCountry' sheet'"+"\n")
        
        for i in listINScMLT:
            if i not in listCountry:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx','sheet 'MobilizationLeadTime': '" + str(i)+ "' 'InstallationCountry' is missing in 'AreaRegionCountry' sheet,"+"\n")
        
        listFSEsMLTEXT=restrictions2pdEXT['SUPPLIER NAME'].unique().tolist()
        listINScMLTEXT=restrictions2pdEXT['Installation Country'].unique().tolist()
        for i in listFSEsMLTEXT:
            if i not in listSupplier:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx', sheet 'EXT_MobilizationLeadTime': '" + str(i)+ " 'SUPPLIER NAME' is missing in 'EXT_percentuali' sheet"+"\n")
        
        for i in listINScMLTEXT:
            if i not in listCountry:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx',sheet 'EXT_MobilizationLeadTime': '" + str(i)+ " 'InstallationCountry' is missing in 'AreaRegionCountry' sheet,"+"\n")
       
        listregCM=costmatrixspd['Region_DEMAND'].unique().tolist()
        for i in listregCM:
            if i not in listRegion:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx',  sheet 'CostMatrixForSupplier': '" + str(i)+ "' 'Region_DEMAND' is missing in 'AreaRegionCountry' sheet'"+"\n")

        listcouCM=costmatrixspd['COUNTRY_OF_DEMAND'].unique().tolist()
        for i in listcouCM:
            if i not in listCountry:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx', sheet 'CostMatrixForSupplier': '" + str(i)+ "' 'COUNTRY_OF_DEMAND' is missing in 'AreaRegionCountry' sheet"+"\n")

        listsupCM=costmatrixspd['SUPPLIER NAME'].unique().tolist() 
        for i in listsupCM:
            if i not in listSupplier:
                problemscounter+=1
                print("ERROR in 'KT_REGOLE.xlsx', sheet 'CostMatrixForSupplier' :'" + str(i)+ "' 'SUPPLIER NAME' is missing in 'EXT_percentuali' sheet"+"\n")

       
        if os.path.isfile('./capacity.xlsx')!=True:
            problemscounter+=1
            print("ERROR in 'capacity.xlsx':"+" file doesn't exist or is written in wrong way"+"\n")
        else:
            capacity= pd.ExcelFile("capacity.xlsx")
            capacitypd= pd.read_excel("capacity.xlsx")
            problemscounterc=0
#            capacitypd['Country']=capacitypd['Country'].str.strip()
#            capacitypd['Country']=capacitypd['Country'].str.title()
            
            
            listlablcapacity=capacitypd.columns.tolist()
            if len(capacity.sheet_names) != 1:
                problemscounter+=1
                print("ERROR in 'capacity.xlsx':"+"file must have one sheet, the file has "+str(len(capacity.sheet_names))+" sheets:"+ str(capacity.sheet_names)+"\n")
            else:
                for i in listsheetscapacity:
                        if i not in listlablcapacity:
                            print("ERROR in 'capacity.xlsx':"+ "field '"+str(i)+ "' is missing or is written in wrong way"+"\n")
                doubleSSO=capacitypd['Technician/Equipment: SSO ID'].value_counts()
                
                if len(capacitypd.loc[~capacitypd['Technician/Equipment: SSO ID'].astype(str).str.isdigit(), 'Technician/Equipment: SSO ID'].tolist())>0:
                    problemscounterc+=1
                    print("ERROR in 'capacity.xlsx':" + str(capacitypd.loc[~capacitypd['Technician/Equipment: SSO ID'].astype(str).str.isdigit(), 'Technician/Equipment: SSO ID'].tolist()) + " in 'Technician/Equipment: SSO ID' column is not a integer \n")
                
                if sum(doubleSSO[doubleSSO>1]) >0:
                    problemscounterc+=1
                    print("ERROR in 'capacity.xlsx':"+ "Found duplicate 'Technician/Equipment: SSO ID':\n"+ str(doubleSSO[doubleSSO>1])+"\n")#check duplicate SSO
                
                if problemscounterc > 0:
                    print("the tool is not able to test 'capacity.xlsx' file, please check 'capacity.xlsx' '\n ")
                    problemscounter+=problemscounterc
                else:
                    capacitypd.set_index('Technician/Equipment: SSO ID', inplace=True)
                    
                    if capacitypd['IS GLOBAL'].dtype != bool:
                        problemscounter+=1
                        print("ERROR in 'capacity.xlsx': 'IS GLOBAL' field contains not boolean values, the column must contains only True or False value, check column 'IS GLOBAL' in 'capacity.xlsx' file \n")
        
                    for i in capacitypd.index:
                        if capacitypd['PRIMARY'][i] not in listSkill and pd.isnull(capacitypd['PRIMARY'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['PRIMARY'][i]) + "'"+  " PRIMARY skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['SECONDARY'][i] not in listSkill and pd.isnull(capacitypd['SECONDARY'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SECONDARY'][i]) + "'"+  " SECONDARY skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['SPECIAL 1'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 1'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 1'][i]) + "'"+  " SPECIAL 1 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['SPECIAL 2'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 2'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 2'][i]) + "'"+  " SPECIAL 2 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['SPECIAL 3'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 3'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 3'][i]) + "'"+  " SPECIAL 3 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['SPECIAL 4'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 4'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 4'][i]) + "'"+  " SPECIAL 4 skill is not in 'KT_REGOLE.xlsx' \n")    
                        if capacitypd['SPECIAL 5'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 5'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 5'][i]) + "'"+  " SPECIAL 5 skill is not in 'KT_REGOLE.xlsx' \n")    
                        if capacitypd['SPECIAL 6'][i] not in listSkill and pd.isnull(capacitypd['SPECIAL 6'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['SPECIAL 6'][i]) + "'"+  " SPECIAL 6 skill is not in 'KT_REGOLE.xlsx' \n")   
                        if type(capacitypd['Billable date'][i]) != datetime.datetime and type(capacitypd['Billable date'][i]) != pd._libs.tslibs.timestamps.Timestamp:
                            problemscounter+=1
                            print("ERROR in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '" + str(capacitypd['Billable date'][i]) + " in 'Billable date' field is not in datetime format \n")
                        if capacitypd['Country'][i] not in listCountry:
                            problemscounter+=1
                            print("ERROR in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '"+ str(capacitypd['Country'][i])+"'"+ " Country is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['Region'][i] not in listRegion:
                            problemscounter+=1
                            print("ERROR in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '"+ str(capacitypd['Region'][i])+"'"+ " Region is not in 'KT_REGOLE.xlsx' \n")
                        if capacitypd['Employer'][i] not in listEmployer:
                            problemscounter+=1
                            print("ERROR in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '"+ str(capacitypd['Employer'][i])+"'"+ " Employer is not in 'KT_REGOLE.xlsx' \n")
                        if  pd.isnull(capacitypd['WTR'][i]) == True or type(capacitypd['WTR'][i]) == str:
                            problemscounter+=1
                            print("ERROR in 'capacity.xlsx', 'Technician/Equipment: SSO ID': '" + str(i) + "': '"+ str(capacitypd['WTR'][i])+"'"+ " in 'WTR' field is empty or written in wrong way \n")
                       
        if os.path.isfile('./external_capacity.xlsx')!=True:
            problemscounter+=1
            print("ERROR in 'external_capacity.xlsx':"+" file doesn't exist or is written in wrong way"+"\n")
        else:
            capacityEXT= pd.ExcelFile("external_capacity.xlsx")
            capacityEXTpd= pd.read_excel("external_capacity.xlsx")
            problemscountercEXT=0
            listlablEXTcapacity=capacityEXTpd.columns.tolist()
            if len(capacityEXT.sheet_names) != 1:
                problemscounter+=1
                print("ERROR in 'external_capacity.xlsx':"+"filr must have one sheet, the file has "+str(len(capacity.sheet_names))+" sheets:"+ str(capacity.sheet_names)+"\n")
            else:
                for i in listsheetscapacityEXT:
                        if i not in listlablEXTcapacity:
                            print("ERROR in 'external_capacity.xlsx':"+ "field '"+str(i)+ "' is missing or is written in wrong way"+"\n")
                doubleSSOEXT=capacityEXTpd['SSO'].value_counts()
                
                if len(capacityEXTpd.loc[~capacityEXTpd['SSO'].astype(str).str.isdigit(), 'SSO'].tolist())>0:
                    problemscountercEXT+=1
                    print("ERROR in 'external_capacity.xlsx':" + str(capacityEXTpd.loc[~capacityEXTpd['SSO'].astype(str).str.isdigit(), 'SSO'].tolist()) + " in 'SSO' column is not a integer \n")
                
                if sum(doubleSSOEXT[doubleSSOEXT>1]) >0:
                    problemscountercEXT+=1
                    print("ERROR in 'external_capacity.xlsx':"+ "Found duplicate 'SSO':\n"+ str(doubleSSO[doubleSSO>1])+"\n")#check duplicate SSO
                
                if problemscountercEXT > 0:
                    print("the tool is not able to test 'external_capacity.xlsx' file, please check 'external_capacity.xlsx' '\n ")
                    problemscounter+=problemscountercEXT
                else:
                    capacityEXTpd.set_index('SSO', inplace=True)
                    
                    for i in capacityEXTpd.index:
                        if capacityEXTpd['PRIMARY'][i] not in listSkill and pd.isnull(capacityEXTpd['PRIMARY'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['PRIMARY'][i]) + "'"+  " PRIMARY skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['SECONDARY'][i] not in listSkill and pd.isnull(capacityEXTpd['SECONDARY'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SECONDARY'][i]) + "'"+  " SECONDARY skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['SPECIAL 1'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 1'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 1'][i]) + "'"+  " SPECIAL 1 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['SPECIAL 2'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 2'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 2'][i]) + "'"+  " SPECIAL 2 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['SPECIAL 3'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 3'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 3'][i]) + "'"+  " SPECIAL 3 skill is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['SPECIAL 4'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 4'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 4'][i]) + "'"+  " SPECIAL 4 skill is not in 'KT_REGOLE.xlsx' \n")    
                        if capacityEXTpd['SPECIAL 5'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 5'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 5'][i]) + "'"+  " SPECIAL 5 skill is not in 'KT_REGOLE.xlsx' \n")    
                        if capacityEXTpd['SPECIAL 6'][i] not in listSkill and pd.isnull(capacityEXTpd['SPECIAL 6'][i]) != True:
                            warningcounter+=1
                            print("WARNING in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SPECIAL 6'][i]) + "'"+  " SPECIAL 6 skill is not in 'KT_REGOLE.xlsx' \n")   
                        if type(capacityEXTpd['HIRING'][i]) != datetime.datetime and type(capacityEXTpd['HIRING'][i]) != pd._libs.tslibs.timestamps.Timestamp:
                            problemscounter+=1
                            print("ERROR in 'external_capacity.xlsx, 'SSO': '" + str(i) + "': '" + str(capacityEXTpd['HIRING'][i]) + " in 'HIRING' field is not in datetime format \n")
                        if capacityEXTpd['Country'][i] not in listCountry:
                            problemscounter+=1
                            print("ERROR in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['Country'][i])+"'"+ " Country is not in 'KT_REGOLE.xlsx' \n")
                        if capacityEXTpd['Region'][i] not in listRegion:
                            problemscounter+=1
                            print("ERROR in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['Region'][i])+"'"+ " Region is not in 'KT_REGOLE.xlsx'\n")
                        if capacityEXTpd['SUPPLIER NAME'][i] not in listSupplier:
                            problemscounter+=1
                            print("ERROR in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['SUPPLIER NAME'][i])+"'"+ " SUPPLIER NAME is not in 'KT_REGOLE.xlsx' sheet 'EXT_percentuali' \n")
                        if  pd.isnull(capacityEXTpd['WTR'][i]) == True or type(capacityEXTpd['WTR'][i]) == str:
                            problemscounter+=1
                            print("ERROR in 'external_capacity.xlsx', 'SSO': '" + str(i) + "': '"+ str(capacityEXTpd['WTR'][i])+"'"+ " in 'WTR' field is empty or written in wrong way \n")
                          
                        
        if os.path.isfile('./demand.xlsx')!=True:
            print("ERROR in 'demand.xlsx':"+" file doesn't exist or is written in wrong way"+"\n")
            problemscounter+=1
        else:
            
            skillcapacityINT= capacitypd['PRIMARY'].unique().tolist()
            skillcapacityINT.extend(capacitypd['SECONDARY'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 1'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 2'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 3'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 4'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 5'].unique().tolist())
            skillcapacityINT.extend(capacitypd['SPECIAL 6'].unique().tolist())
            skillcapacityINT=list(set(skillcapacityINT))
            
            skillcapacityEXT= capacityEXTpd['PRIMARY'].unique().tolist()
            skillcapacityEXT.extend(capacityEXTpd['SECONDARY'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 1'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 2'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 3'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 4'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 5'].unique().tolist())
            skillcapacityEXT.extend(capacityEXTpd['SPECIAL 6'].unique().tolist())
            skillcapacityEXT=list(set(skillcapacityEXT))
            
            demand= pd.ExcelFile("demand.xlsx")
            demandpd= pd.read_excel("demand.xlsx")
            demandpd['Datetime preassigned']=True
            listlabl=demandpd.columns.tolist()
            
            listemplCap= capacitypd['Employer'].unique().tolist()
            
            problemcounterD=0
            if len(demand.sheet_names) != 1:
                problemcounterD+=1
                print("ERROR in 'demand.xlsx':"+"file must have one sheet, the file has "+str(len(demand.sheet_names))+" sheets:"+ str(demand.sheet_names)+"\n")
            else:
                for i in listsheetsdemand:
                    if i not in listlabl:
                        print("ERROR in 'demand.xlsx':"+ "field '"+str(i)+ "' is missing or is written in wrong way"+"\n")
                doubleaui=demandpd['Activity Unique Id'].value_counts()
                
                if len(demandpd.loc[~demandpd['Activity Unique Id'].astype(str).str.isdigit(), 'Activity Unique Id'].tolist())>0:
                    problemcounterD+=1
                    print("ERROR in 'demand.xlsx':" + str(demandpd.loc[~demandpd['Activity Unique Id'].astype(str).str.isdigit(), 'Activity Unique Id'].tolist()) + " 'in Activity Unique Id' column is not a integer \n")
                
                if sum(doubleaui[doubleaui>1]) >0:
                    problemcounterD+=1
                    print("ERROR in 'demand.xlsx':"+ "Found duplicate 'Activity Unique Id':\n"+ str(doubleaui[doubleaui>1])+"\n")#check duplicate AUI
                                   
                if problemcounterD > 0:
                    print("the tool is not able to test 'demand.xlsx' file, please check 'demand.xlsx' '\n ")
                else:    
                    demandpd.set_index('Activity Unique Id', inplace=True)
                    for i in demandpd.index:
                        if demandpd['Country'][i] not in listCountry:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '"+ str(demandpd['Country'][i])+"'"+ " Country is not in 'KT_REGOLE.xlsx' \n")
                        if demandpd['Region'][i] not in listRegion:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '"+ str(demandpd['Region'][i])+"'"+ " Region is not in 'KT_REGOLE.xlsx' \n")
                        if demandpd['Technical Skill'][i] not in listSkill:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '"+ str(demandpd['Technical Skill'][i])+"'"+ " Technical Skill is not in 'KT_REGOLE.xlsx' \n")
                        if demandpd['Prime Contractor'][i] not in listPrimeContractor:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '"+ str(demandpd['Prime Contractor'][i])+"'"+ " Prime Contractor is not in 'KT_REGOLE.xlsx' \n")
                        if demandpd['Total'][i]> maxTotal:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '" + "'Total' field is greater than maximum value ammitted \n")
                       
                        if demandpd['Technical Skill'][i] not in skillcapacityINT and demandpd['Technical Skill'][i] not in skillcapacityEXT:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '" +str(demandpd['Technical Skill'][i]) + "' is not available in internal and external capacity \n")
                        else:
                             if demandpd['Technical Skill'][i] not in skillcapacityINT:
                                 warningcounter+=1
                                 print("WARNING in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '" +str(demandpd['Technical Skill'][i]) + "' is not available in internal capacity \n")
###############################################################################################################################################################################################################                            
################################## Pressigment Date#################################                            
                            
                        if 'Start Month' and 'End Month' in listlabl:
                              demandpd1 = demandpd.loc[demandpd['Activity End Date'].isnull()]
                              demandpd1 = demandpd1.loc[demandpd['Activity Start Date'].isnull()]
                           
                            
                            
                            
                              demandpd=demandpd.loc[demandpd['Datetime preassigned']==False]
                            
                              print('ok')
                               
                                
###############################################################################################################################################################################################################                                 
                        else:
                            
                                if type(demandpd['Activity Start Date'][i]) != datetime.datetime and type(demandpd['Activity Start Date'][i]) != pd._libs.tslibs.timestamps.Timestamp :
                                    problemscounter+=1
                                    Dateflag==False
                                    print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '" + str(demandpd['Activity Start Date'][i]) + "' in 'Activity Start Date' field is not in datetime format \n")
                                if type(demandpd['Activity End Date'][i]) != datetime.datetime and type(demandpd['Activity End Date'][i]) != pd._libs.tslibs.timestamps.Timestamp :
                                    problemscounter+=1
                                    Dateflag==False
                                    print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': '" + str(demandpd['Activity End Date'][i]) + "' in 'Activity End Date' field is not in datetime format \n")
                                if Dateflag==True:
                                    if demandpd['Activity End Date'][i] < demandpd['Activity Start Date'][i]:
                                         print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"':  'Activity End Date' must be greater than 'Activity Start Date' \n")
                       
                        flagrest=False
                        listemplCap= capacitypd['Employer'].unique().tolist()    
                        listmepdem=restrictionspdtrue.loc[restrictionspdtrue['PrimeContractor']==demandpd['Prime Contractor'][i]]['Employer'].tolist()
                        listcountryforbidden=restrictions2pd.loc[restrictions2pd['InstallationCountry']==demandpd['Country'][i]]['FSECountry'].tolist()
                        listcountryforbiddenEXT=restrictions2pdEXT.loc[restrictions2pdEXT['Installation Country']==demandpd['Country'][i]]['SUPPLIER NAME'].tolist()
                        for j in listemplCap:
                            if j in listmepdem:
                                
                                flagrest=True
                                break
                            
                            else:
                                listcosuppl=capacitypd.loc[capacitypd['Employer']==j]['Country'].unique().tolist()
                                for k in listcosuppl:
                                    if k not in listcountryforbidden:
                                        
                                        flagrest=True
                                
                                        break
                                    
                        if flagrest==False:
                            warningcounter+=1
                            print("WARNING in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': "+ " there are not SSO in internal capacity with correct visa requirements \n"  )
                            for n in listSupplier:
                                
                                if n not in listcountryforbiddenEXT:
                                    flagrest=True
                                    break
                        if flagrest==False:
                            problemscounter+=1
                            print("ERROR in 'demand.xlsx', 'Activity Unique Id' :'"+ str(i) +"': "+ " there are not SSO in internal capacity and external capacity with correct visa requirements \n"  )
                                
                            
                             
                        
                    
end=time.time()
print('##############################################################################################################\n')
print('Warnings found:' + str(warningcounter)+ "\n")
print('ERRORS found:' + str(problemscounter)+ "\n")






if problemscounter==0:
    
    print('CONGRATULATIONS! Input files are ready for OPTIMA! \n')
    
else:
    
    print('Check input files before run OPTIMA \n')


#print("done in:", int(end-begin), "sec")                  


################################################################################################################

#class Logger(object):
#    def __init__(self):
#        self.terminal = sys.stdout
#        self.log = open("programmable_OPTIMA.log", "w")
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message)  
#        self.log.flush()
#
#    def flush(self):
#        #this flush method is needed for python 3 compatibility.
#        #this handles the flush command by doing nothing.
#        #you might want to specify some extra behavior here.
#        
#        pass    
#
#sys.stdout = Logger()

###############################################################################################################



###############################################################################################################
###############################################################################################################
print("Do you want to run OPTIMA? write 'y' if you want to start ")

runGO=input()

if runGO=="y":
    
    
    print('---------------------------------------------------------------------')
    print("""\
      ___  ____ _____ ___ __  __    _            ____  
     / _ \|  _ \_   _|_ _|  \/  |  / \    __   _|___ \ 
    | | | | |_) || |  | || |\/| | / _ \   \ \ / / __) |
    | |_| |  __/ | |  | || |  | |/ ___ \   \ V / / __/ 
     \___/|_|    |_| |___|_|  |_/_/   \_\   \_/ |_____|
                                                       
              _              _       _                         _   _           _              
     ___  ___| |__   ___  __| |_   _| | ___ _ __    ___  _ __ | |_(_)_ __ ___ (_)_______ _ __ 
    / __|/ __| '_ \ / _ \/ _` | | | | |/ _ \ '__|  / _ \| '_ \| __| | '_ ` _ \| |_  / _ \ '__|
    \__ \ (__| | | |  __/ (_| | |_| | |  __/ |    | (_) | |_) | |_| | | | | | | |/ /  __/ |   
    |___/\___|_| |_|\___|\__,_|\__,_|_|\___|_|     \___/| .__/ \__|_|_| |_| |_|_/___\___|_|   
                                                        |_|                                   
    
                        """)
    print('---------------------------------------------------------------------')
    ###############################################################################################################	
    ###############################################################################################################
    
    print("loading data in progress...")
    
    #+++++++++++++++++++++++++EXCEL IMPORT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    mat = pd.read_excel("demand.xlsx")#file excel DEMAND
    tse = pd.read_excel("capacity.xlsx")#file excel CAPACITY
    restrictions = pd.read_excel("KT_REGOLE.xlsx", sheet_name="LegalEntityRestrictions")
    
    #restrictions['IsAllowed']==restrictions['IsAllowed'].str.strip()
    #restrictions['IsAllowed']==restrictions['IsAllowed'].str.title()
    
    restrictionsfalse = restrictions.loc[restrictions['IsAllowed']==False]
    restrictions2 = pd.read_excel("KT_REGOLE.xlsx", sheet_name="MobilizationLeadTime")
    restrictions2['FSECountry']=restrictions2['FSECountry'].str.strip()
    restrictions2['InstallationCountry']=restrictions2['InstallationCountry'].str.strip()
    restrictions2['FSECountry']=restrictions2['FSECountry'].str.title()
    restrictions2['InstallationCountry']=restrictions2['InstallationCountry'].str.title()
    mat['Country']=mat['Country'].str.strip()
    mat['Country']=mat['Country'].str.title()
    tse['Country']=tse['Country'].str.strip()
    tse['Country']=tse['Country'].str.title()
    tse['Value']=0
    #restrictions2.loc[restrictions2['InstallationCountry']].str.strip(inplace=True)
    
    
    
    restr_copy=restrictions.copy()
    
    #restr_copy2=restrictions2.copy()
    
    dfcoutryspec= restrictions2.loc[restrictions2['FSECountry']=='*']
    dfcoutryspec.set_index(['InstallationCountry'], inplace=True)
    listcountryspecialtmp=dfcoutryspec.index.tolist()
    listcountryspecial=list(set(listcountryspecialtmp))
    
    
    restrictionsfalse.set_index(['PrimeContractor','Employer', 'InstallationCountry'], inplace=True)
    restrictions2.set_index(['FSECountry','InstallationCountry'] , inplace=True)
    
    listarest1= restrictionsfalse.index.tolist()
    listarest2=restrictions2.index.tolist()
    
    #+++++++++++++++++++++++++EXCEL IMPORT++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    #dfmat = pd.DataFrame(np.zeros((len(mat),(max (mat['Activity End Date']) - min(mat['Activity Start Date'])).days+1)),mat['Activity Unique Id'], columns=pd.bdate_range(min(mat['Activity Start Date']),max (mat['Activity End Date']) , freq='D'))
    #dftime = pd.DataFrame(np.zeros((len(mat),(max (mat['Activity End Date']) - min(mat['Activity Start Date'])).days+1)),mat['Activity Unique Id'], columns=pd.bdate_range(min(mat['Activity Start Date']),max (mat['Activity End Date']) , freq='D'))
    dfsso = pd.DataFrame(np.zeros((len(tse),(max (mat['Activity End Date']) - min(mat['Activity Start Date'])).days+1)),tse['Technician/Equipment: SSO ID'], columns=pd.bdate_range(min(mat['Activity Start Date']),max (mat['Activity End Date']) , freq='D'))
    
    listatse=tse['Technician/Equipment: SSO ID'].tolist()
    
    p=tse[tse['SECONDARY'].isnull()]
    s=p[p['SPECIAL 1'].isnull()]
    
    listapureprimary=s['Technician/Equipment: SSO ID'].tolist()
    
    sp1=tse[tse['SPECIAL 1'].notnull()]
    listaspecial1=sp1['Technician/Equipment: SSO ID'].tolist()
    
    sp2=tse[tse['SPECIAL 2'].notnull()]
    listaspecial2=sp2['Technician/Equipment: SSO ID'].tolist()
    
    sp3=tse[tse['SPECIAL 3'].notnull()]
    listaspecial3=sp3['Technician/Equipment: SSO ID'].tolist()
    
    sp4=tse[tse['SPECIAL 4'].notnull()]
    listaspecial4=sp4['Technician/Equipment: SSO ID'].tolist()
    
    sp5=tse[tse['SPECIAL 5'].notnull()]
    listaspecial5=sp5['Technician/Equipment: SSO ID'].tolist()
    
    sp6=tse[tse['SPECIAL 6'].notnull()]
    listaspecial6=sp6['Technician/Equipment: SSO ID'].tolist()
    
    
    shuffle(listaspecial1)
    shuffle(listaspecial2)
    shuffle(listaspecial3)
    shuffle(listaspecial4)
    shuffle(listaspecial5)
    shuffle(listaspecial6)
    shuffle(listapureprimary)
    shuffle(listatse)
    
    
    tse.set_index('Technician/Equipment: SSO ID', inplace=True)
    ascendent = mat.sort_values(by='Total',ascending=False)
    tse['Initial WTR']=tse['WTR']
    ascendent.set_index('Activity Unique Id', inplace=True)
    
    
    #dfmat[:]=0
    dfsso[:]=0
    #ascendent['SSO']=0
    ascendent['Skill']=0
    ascendent['Experience level']=0
    ascendent['CountryFSE']=0
    ascendent['RegionFSE']=0
    ascendent['Employer']=0
    ascendent['IsGlobalFSE']=0
    ascendent['contractor']=0
    ascendent['supplier']=0
    ascendent['SSO'].fillna(0, inplace=True)
    ascendent['Assigned by Optima']=False
    ascendent['Preassigned']=False
    ascendent['Macroskill']=0
    CoutryAGG=pd.read_excel("KT_REGOLE.xlsx", sheet_name="TECHNICAL SKILL")
    CoutryAGG.set_index(['OPTIMA SKILL'],inplace=True)
    ############################### PARTIAL ASSIGNED DEMAND WTR UPDATE #######################################
    for i in ascendent.index:
        if type(CoutryAGG['AGGREGATE SKILL'][ascendent['Technical Skill'][i]])==str:
            ascendent['Macroskill'][i]=CoutryAGG['AGGREGATE SKILL'][ascendent['Technical Skill'][i]]
        else:
            ascendent['Macroskill'][i]=CoutryAGG['AGGREGATE SKILL'][ascendent['Technical Skill'][i]].tolist()[0]
        
        if ascendent['SSO'][i] !=0 and ascendent['SSO'][i] in listatse :
            
            tse['WTR'][ascendent['SSO'][i]]-=ascendent['Total'][i]
           
            ascendent['Preassigned'][i]=True
            ascendent['CountryFSE'][i]=tse['Country'][ascendent['SSO'][i]]
            ascendent['RegionFSE'][i]=tse['Region'][ascendent['SSO'][i]]
            ascendent['Employer'][i]=tse['Employer'][ascendent['SSO'][i]]
            ascendent['IsGlobalFSE']=tse['IS GLOBAL'][ascendent['SSO'][i]]
            
            if tse['PRIMARY'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='PRIMARY'
                ascendent['Skill'][i]= tse['PRIMARY'][ascendent['SSO'][i]]
            elif tse['SECONDARY'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SECONDARY'
                ascendent['Skill'][i]= tse['SECONDARY'][ascendent['SSO'][i]]
            elif tse['SPECIAL 1'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 1'
                ascendent['Skill'][i]= tse['SPECIAL 1'][ascendent['SSO'][i]]
            elif tse['SPECIAL 2'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 2'
                ascendent['Skill'][i]= tse['SPECIAL 2'][ascendent['SSO'][i]]
            elif tse['SPECIAL 3'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 3'
                ascendent['Skill'][i]= tse['SPECIAL 3'][ascendent['SSO'][i]]
            elif tse['SPECIAL 4'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 4'
                ascendent['Skill'][i]= tse['SPECIAL 4'][ascendent['SSO'][i]]
            elif tse['SPECIAL 5'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 5'
                ascendent['Skill'][i]= tse['SPECIAL 5'][ascendent['SSO'][i]]
            elif tse['SPECIAL 6'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 6'
                ascendent['Skill'][i]= tse['SPECIAL 6'][ascendent['SSO'][i]]
            else:
                ascendent['Experience level'][i]='No experience in capacity'
                ascendent['Skill'][i]= 'no skill in capacity'
    
            dfsso.loc[ascendent['SSO'][i],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i
    
    ##########################################################################################################
    
    print("done!")
    
    
    
    
    
    
    print ("data elaboration in progress...")
    
    
    
    def allocator(skill, lista):
        AscCon = ascendent.loc[ascendent['SSO'] == 0]
        for i in AscCon.index:
                               
            for j,n in enumerate(lista):
                if ascendent['Country'][i] in listcountryspecial and ascendent['Country'][i] != tse['Country'][n]:
                    continue
                else:
                    
                    if tse[skill][n] != ascendent['Technical Skill'][i] or tse["Billable date"][n] > ascendent['Activity Start Date'][i] or tse['IS GLOBAL'][n]== True or (ascendent['Prime Contractor'][i], tse['Employer'][n],ascendent['Country'][i]) in listarest1 or (tse['Country'][n],ascendent['Country'][i]) in listarest2  :#skill check and billable date
                        continue
                    else:            
                        if tse['WTR'][n] >= ascendent['Total'][i]:# WTR check
                            if int(dfsso.loc[[n],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]+datetime.timedelta(days=1)].sum(axis=1)) == 0  :#overlap check
                                dfsso.loc[n,ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i #timetable sheet compiling
                                ascendent['SSO'][i]= n# SSO solution compiling
                                AscCon['SSO'][i]=n    
                                ascendent['Skill'][i]= tse[skill][n]# Skill solution compiling
                                ascendent['Experience level'][i]= skill# Skill level experience
                                ascendent['CountryFSE'][i]= tse['Country'][n]
                                ascendent['RegionFSE'][i]= tse['Region'][n]
                                ascendent['IsGlobalFSE'][i]= tse['IS GLOBAL'][n]
                                ascendent['Employer'][i]= tse['Employer'][n]
                                tse['WTR'][n]-=ascendent['Total'][i]# remove time worked from WTR
                                ascendent['Assigned by Optima'][i]=True
                                AscCon = AscCon.loc[AscCon['SSO'] == 0]
                                break
    
    def allocatordpo(skill, lista, dpo):
        AscCon = ascendent.loc[ascendent['SSO'] == 0]
    
        for i in AscCon.index:
            
                
            for j,n in enumerate(lista):
                if ascendent['Country'][i] in listcountryspecial and ascendent['Country'][i] != tse['Country'][n]:
                    continue
                else:
                
                    if tse[skill][n] != ascendent['Technical Skill'][i] or tse["Billable date"][n] > ascendent['Activity Start Date'][i] or tse[dpo][n] != ascendent[dpo][i] or tse['IS GLOBAL'][n]== True or (ascendent['Prime Contractor'][i], tse['Employer'][n],ascendent['Country'][i]) in listarest1 or (tse['Country'][n],ascendent['Country'][i]) in listarest2  :#skill check and billable date
                        continue
                    else:            
                        if tse['WTR'][n] >= ascendent['Total'][i]:# WTR check
                            if int(dfsso.loc[[n],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]+datetime.timedelta(days=1)].sum(axis=1)) == 0  :#overlap check
                                dfsso.loc[n,ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i #timetable sheet compiling
                                ascendent['SSO'][i]= n# SSO solution compiling
                                AscCon['SSO'][i]=n 
                                ascendent['Skill'][i]= tse[skill][n]# Skill solution compiling
                                ascendent['Experience level'][i]= skill# Skill level experience
                                ascendent['CountryFSE'][i]= tse['Country'][n]
                                ascendent['RegionFSE'][i]= tse['Region'][n]
                                ascendent['IsGlobalFSE'][i]= tse['IS GLOBAL'][n]
                                ascendent['Employer'][i]= tse['Employer'][n]
                                tse['WTR'][n]-=ascendent['Total'][i]# remove time worked from WTR
                                ascendent['Assigned by Optima'][i]=True
                                AscCon = AscCon.loc[AscCon['SSO'] == 0]
                                break
    
    def allocatorglb(skill, lista):
        AscCon = ascendent.loc[ascendent['SSO'] == 0]
    
        for i in AscCon.index:
            
                
            for j,n in enumerate(lista):
                if ascendent['Country'][i] in listcountryspecial and ascendent['Country'][i] != tse['Country'][n]:
                    continue
                else:
                    if tse[skill][n] != ascendent['Technical Skill'][i] or tse["Billable date"][n] > ascendent['Activity Start Date'][i] or tse['IS GLOBAL'][n]== False or (ascendent['Prime Contractor'][i], tse['Employer'][n],ascendent['Country'][i]) in listarest1 or (tse['Country'][n],ascendent['Country'][i]) in listarest2:#skill check and billable date
                        continue
                    else:            
                        if tse['WTR'][n] >= ascendent['Total'][i]:# WTR check
                            if int(dfsso.loc[[n],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]+datetime.timedelta(days=1)].sum(axis=1)) == 0  :#overlap check
                                dfsso.loc[n,ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i #timetable sheet compiling
                                ascendent['SSO'][i]= n# SSO solution compiling
                                AscCon['SSO'][i]=n 
                                ascendent['Skill'][i]= tse[skill][n]# Skill solution compiling
                                ascendent['Experience level'][i]= skill# Skill level experience
                                ascendent['CountryFSE'][i]= tse['Country'][n]
                                ascendent['RegionFSE'][i]= tse['Region'][n]
                                ascendent['IsGlobalFSE'][i]= tse['IS GLOBAL'][n]
                                ascendent['Employer'][i]= tse['Employer'][n]
                                tse['WTR'][n]-=ascendent['Total'][i]# remove time worked from WTR
                                ascendent['Assigned by Optima'][i]=True
                                AscCon = AscCon.loc[AscCon['SSO'] == 0]
                                break
                                
    
    #def allocatorpsglb(lista):
    #    AscCon = ascendent.loc[ascendent['SSO'] == 0]
    #    for i in AscCon.index:
    #        
    #        
    #        for j,n in enumerate(listatse):
    #            if ascendent['Country'][i] in listcountryspecial and ascendent['Country'][i] != tse['Country'][n]:
    #                continue
    #            else:
    #            
    #                if tse['PRIMARY'][n] == ascendent['Technical Skill'][i]  and tse['IS GLOBAL'][n]== True :
    #                    if  tse["Billable date"][n] > ascendent['Activity Start Date'][i] or (ascendent['Prime Contractor'][i], tse['Employer'][n],ascendent['Country'][i]) in listarest1 or (tse['Country'][n],ascendent['Country'][i]) in listarest2:#skill check and billable date
    #                        continue
    #                    else:            
    #                        if tse['WTR'][n] >= ascendent['Total'][i]:# WTR check
    #                            if int(dfsso.loc[[n],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]+datetime.timedelta(days=1)].sum(axis=1)) == 0  :#overlap check
    #                                dfsso.loc[n,ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i #timetable sheet compiling
    #                                ascendent['SSO'][i]= n# SSO solution compiling
    #                                AscCon['SSO'][i]=n
    #                                ascendent['Skill'][i]= tse['PRIMARY'][n]# Skill solution compiling
    #                                ascendent['Experience level'][i]= 'PRIMARY'# Skill level experience
    #                                ascendent['CountryFSE'][i]= tse['Country'][n]
    #                                ascendent['RegionFSE'][i]= tse['Region'][n]
    #                                ascendent['IsGlobalFSE'][i]= tse['IS GLOBAL'][n]
    #                                ascendent['Employer'][i]= tse['Employer'][n]
    #                                tse['WTR'][n]-=ascendent['Total'][i]# remove time worked from WTR
    #                                ascendent['Assigned by Optima'][i]=True
    #                                AscCon = AscCon.loc[AscCon['SSO'] == 0]
    #                                break
    #            
    #            
    #                elif tse['SECONDARY'][n] == ascendent['Technical Skill'][i]  and tse['IS GLOBAL'][n]== True:
    #                    if  tse["Billable date"][n] > ascendent['Activity Start Date'][i] or (ascendent['Prime Contractor'][i], tse['Employer'][n],ascendent['Country'][i]) in listarest1 or (tse['Country'][n],ascendent['Country'][i]) in listarest2:#skill check and billable date
    #                        continue
    #                    else:            
    #                        if tse['WTR'][n] >= ascendent['Total'][i]:# WTR check
    #                            if int(dfsso.loc[[n],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]+datetime.timedelta(days=1)].sum(axis=1)) == 0  :#overlap check
    #                                dfsso.loc[n,ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i #timetable sheet compiling
    #                                ascendent['SSO'][i]= n# SSO solution compiling
    #                                AscCon['SSO'][i]=n
    #                                ascendent['Skill'][i]= tse['SECONDARY'][n]# Skill solution compiling
    #                                ascendent['Experience level'][i]= 'SECONDARY'# Skill level experience
    #                                ascendent['CountryFSE'][i]= tse['Country'][n]
    #                                ascendent['RegionFSE'][i]= tse['Region'][n]
    #                                ascendent['IsGlobalFSE'][i]= tse['IS GLOBAL'][n]
    #                                ascendent['Employer'][i]= tse['Employer'][n]
    #                                tse['WTR'][n]-=ascendent['Total'][i]# remove time worked from WTR
    #                                ascendent['Assigned by Optima'][i]=True
    #                                AscCon = AscCon.loc[AscCon['SSO'] == 0]
    #                                break
    
    
    
    allocatordpo('PRIMARY',listapureprimary,'Country')
    allocatordpo('PRIMARY',listatse,'Country')
    allocatordpo('SECONDARY',listatse,'Country')
    allocatordpo('SPECIAL 1',listaspecial1,'Country')
    allocatordpo('SPECIAL 2',listaspecial2,'Country')
    allocatordpo('SPECIAL 3',listaspecial3,'Country')
    allocatordpo('SPECIAL 4',listaspecial4,'Country')
    allocatordpo('SPECIAL 5',listaspecial5,'Country')
    allocatordpo('SPECIAL 6',listaspecial6,'Country')
    
    print('Country allocated ')
    
    allocatordpo('PRIMARY',listapureprimary,'Region')
    allocatordpo('PRIMARY',listatse,'Region')
    allocatordpo('SECONDARY',listatse,'Region')
    allocatordpo('SPECIAL 1',listaspecial1,'Region')
    allocatordpo('SPECIAL 2',listaspecial2,'Region')
    allocatordpo('SPECIAL 3',listaspecial3,'Region')
    allocatordpo('SPECIAL 4',listaspecial4,'Region')
    allocatordpo('SPECIAL 5',listaspecial5,'Region')
    allocatordpo('SPECIAL 6',listaspecial6,'Region')
    
    print('Region allocated')
    
    
    allocatorglb('PRIMARY',listapureprimary)
    allocatorglb('PRIMARY',listatse)
    allocatorglb('SECONDARY',listatse)
    allocatorglb('SPECIAL 1',listaspecial1)
    allocatorglb('SPECIAL 2',listaspecial2)
    allocatorglb('SPECIAL 3',listaspecial3)
    allocatorglb('SPECIAL 4',listaspecial4)
    allocatorglb('SPECIAL 5',listaspecial5)
    allocatorglb('SPECIAL 6',listaspecial6)
     
    
    print('Global allocated')
    
    
    
    allocator('PRIMARY',listatse)
    allocator('PRIMARY',listapureprimary)
    allocator('SECONDARY',listatse)
    allocator('SPECIAL 1',listaspecial1) 
    allocator('SPECIAL 2',listaspecial2)   
    allocator('SPECIAL 3',listaspecial3) 
    allocator('SPECIAL 4',listaspecial4) 
    allocator('SPECIAL 5',listaspecial5)
    allocator('SPECIAL 6',listaspecial6) 
                
    print('all internal FSE allocated')
    
    
    print("done!")
    
    
    
    
    print('starting allocation contractors')
    
    mat_cost= pd.read_excel("KT_REGOLE.xlsx",sheet_name="CostMatrixForSupplier")
    contractors= pd.read_excel("external_capacity.xlsx")
    dfssoC = pd.DataFrame(np.zeros((len(contractors),(max (mat['Activity End Date']) - min(mat['Activity Start Date'])).days+1)),contractors['SSO'], columns=pd.bdate_range(min(mat['Activity Start Date']),max (mat['Activity End Date']) , freq='D'))
    lisC = contractors['SSO'].tolist()
    contractors['Initial WTR']=contractors['WTR']
    restrictionsC = pd.read_excel("KT_REGOLE.xlsx", sheet_name="EXT_MobilizationLeadTime")
    ascendent['cost']=0
    ascendent['supplier']=0
    restrictionsC=restrictionsC.loc[restrictionsC['LeadTimeInDays'] ==1000]
    restrictionsC.set_index(['SUPPLIER NAME','Installation Country'] , inplace=True)
    listarestC=restrictionsC.index.tolist()
    
    contractors.set_index(['SSO'], inplace=True)
    ascendent['contractor']=False
    for i in ascendent.index:
        
        if ascendent['SSO'][i] !=0 and ascendent['SSO'][i] in lisC :
    
            contractors['WTR'][ascendent['SSO'][i]]-=ascendent['Total'][i]
            
            dfssoC.loc[ascendent['SSO'][i],ascendent['Activity Start Date'][i]:ascendent['Activity End Date'][i]] = i
            ascendent['Preassigned'][i]=True
            ascendent['contractor'][i]=True
            ascendent['supplier'][i]=contractors['SUPPLIER NAME'][ascendent['SSO'][i]]
            
            if contractors['PRIMARY'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='PRIMARY'
                ascendent['Skill'][i]= contractors['PRIMARY'][ascendent['SSO'][i]]
            elif contractors['SECONDARY'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SECONDARY'
                ascendent['Skill'][i]= contractors['SECONDARY'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 1'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 1'
                ascendent['Skill'][i]= contractors['SPECIAL 1'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 2'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 2'
                ascendent['Skill'][i]= contractors['SPECIAL 2'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 3'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 3'
                ascendent['Skill'][i]= contractors['SPECIAL 3'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 4'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 4'
                ascendent['Skill'][i]= contractors['SPECIAL 4'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 5'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 5'
                ascendent['Skill'][i]= contractors['SPECIAL 5'][ascendent['SSO'][i]]
            elif contractors['SPECIAL 6'][ascendent['SSO'][i]] == ascendent['Technical Skill'][i]:
                ascendent['Experience level'][i]='SPECIAL 6'
                ascendent['Skill'][i]= contractors['SPECIAL 6'][ascendent['SSO'][i]]
            else:
                ascendent['Experience level'][i]='No experience in capacity'
                ascendent['Skill'][i]= 'no skill in capacity'
    
    
    coverage = pd.read_excel("KT_REGOLE.xlsx", sheet_name="EXT_percentuali")
    cosvsort=coverage.sort_values(by='PERCENTUALE', ascending=False)
    
    
    
    AscCon = ascendent.loc[ascendent['SSO'] == 0]
    unfilledTotal=AscCon['Total'].sum()+ascendent.loc[ascendent['contractor']==True]['Total'].sum()
    cosvsort.reset_index(inplace=True)
    for i in cosvsort.index :
        print("allocating",cosvsort.loc[i]['SUPPLIER NAME'])
        listcon=contractors.loc[contractors['SUPPLIER NAME'] == cosvsort.loc[i]['SUPPLIER NAME']].index.tolist()
        AscCon = ascendent.loc[ascendent['SSO'] == 0]
        listcontrac = AscCon.index.tolist()
        obtained=ascendent.loc[ascendent['supplier']==cosvsort.loc[i]['SUPPLIER NAME']]['Total'].sum()
        treshold = unfilledTotal /100 * cosvsort.loc[i]['PERCENTUALE']
        mat_cost_fil = mat_cost.loc[mat_cost['SUPPLIER NAME'] ==cosvsort.loc[i]['SUPPLIER NAME']]
        mat_cost_fil.set_index(['Region_DEMAND','COUNTRY_OF_DEMAND'], inplace=True)
        listCouReg = mat_cost_fil.index.tolist() 
       
        for j in AscCon.index:
            if (AscCon.loc[j]['Region'],AscCon.loc[j]['Country']) not in listCouReg:
                AscCon['cost'][j]=10000
            else:
                AscCon['cost'][j]=mat_cost_fil.loc[(AscCon.loc[j]['Region'],AscCon.loc[j]['Country'])]['COST']
                  
        AscCon['cost']=AscCon['cost']*-1
        AscCon=AscCon.sort_values(by=['cost','Total'], ascending=False)
        
        for n in listcontrac:
            if (cosvsort.loc[i]['SUPPLIER NAME'],ascendent['Country'][n]) in listarestC:
                
                continue
            if obtained == treshold:
                break
        
            else:
                for k in listcon:
    
                    
                    if AscCon['Total'][n]+obtained > treshold :
                        break 
                    
                    if  ascendent['SSO'][n] !=0 or contractors["HIRING"][k] > AscCon['Activity Start Date'][n]  or  int(dfssoC.loc[[k],AscCon['Activity Start Date'][n]:AscCon['Activity End Date'][n]+datetime.timedelta(days=1)].sum(axis=1)) != 0 or AscCon['SSO'][n] !=0 or contractors['WTR'][k] < AscCon['Total'][n]:
                        continue
                    else:
                        if contractors['PRIMARY'][k] == AscCon['Technical Skill'][n] or contractors['SECONDARY'][k] == AscCon['Technical Skill'][n] or contractors['SPECIAL 1'][k] == AscCon['Technical Skill'][n] or contractors['SPECIAL 2'][k] == AscCon['Technical Skill'][n] or contractors['SPECIAL 3'][k] == AscCon['Technical Skill'][n]or contractors['SPECIAL 4'][k] == AscCon['Technical Skill'][n]or contractors['SPECIAL 5'][k] == AscCon['Technical Skill'][n]or contractors['SPECIAL 6'][k] == AscCon['Technical Skill'][n]:
                            dfssoC.loc[k,ascendent['Activity Start Date'][n]:ascendent['Activity End Date'][n]] = n 
                            ascendent['SSO'][n]= k# SSO solution compiling
                            AscCon['SSO'][n]= k
                            ascendent['contractor'][n]=True
                            ascendent['supplier'][n]=cosvsort.loc[i]['SUPPLIER NAME']
                            ascendent['cost'][n]=AscCon['cost'][n]*-1
                            contractors['WTR'][k]-=ascendent['Total'][n]
                            ascendent['Assigned by Optima'][n]=True
                            obtained += ascendent['Total'][n]
                            
                            if contractors['PRIMARY'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='PRIMARY'
                                ascendent['Skill'][n]= contractors['PRIMARY'][k]
                            elif contractors['SECONDARY'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SECONDARY'
                                ascendent['Skill'][n]= contractors['SECONDARY'][k]
                            elif contractors['SPECIAL 1'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 1'
                                ascendent['Skill'][n]= contractors['SPECIAL 1'][k]
                            elif contractors['SPECIAL 2'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 2'
                                ascendent['Skill'][n]= contractors['SPECIAL 2'][k]
                            elif contractors['SPECIAL 3'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 3'
                                ascendent['Skill'][n]= contractors['SPECIAL 3'][k]
                            elif contractors['SPECIAL 4'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 4'
                                ascendent['Skill'][n]= contractors['SPECIAL 4'][k]
                            elif contractors['SPECIAL 5'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 5'
                                ascendent['Skill'][n]= contractors['SPECIAL 5'][k]
                            elif contractors['SPECIAL 6'][k] == AscCon['Technical Skill'][n]:
                                ascendent['Experience level'][n]='SPECIAL 6'
                                ascendent['Skill'][n]= contractors['SPECIAL 6'][k]
                              
                            AscCon = AscCon.loc[AscCon['SSO'] == 0]
                            listcontrac = AscCon.index.tolist()
                            break
    #                        if obtained == treshold:
    #                            break
                            
                            
                     
            
                     
    print('contractors allocated')
    
    
    print("splitting data in months/quarter")
    
    import datetime
    asccopy=ascendent.copy()
    
    ascendent1=asccopy.copy()
    asccopy.reset_index(inplace=True)
    asccopy['Month']=0
    asccopy['Quarter']=0
    asccopy['hour per month']=0
    
    asccopy['Allert Month Hour']= False
    Q1=[1,2,3]
    Q2=[4,5,6]
    Q3=[7,8,9]
    Q4=[10,11,12]
    
    limM=373
    
    
    splitted=pd.DataFrame()
    
    
    for i in ascendent1.index:
        sumh=0
        deltaM = ascendent1['Activity End Date'][i].month-ascendent1['Activity Start Date'][i].month +1
        daysT=(ascendent1['Activity End Date'][i]-ascendent1['Activity Start Date'][i]).days+1
        hpd=int(ascendent1['Total'][i]/daysT)
        startM=pd.date_range(start=ascendent1['Activity Start Date'][i], end=ascendent1['Activity End Date'][i], freq='MS')
        
        endM=pd.date_range(start=ascendent1['Activity Start Date'][i], end=ascendent1['Activity End Date'][i], freq='M')
        startM=endM+datetime.timedelta(days=1)
        
        if deltaM>1:
            for j in range(deltaM):
    
                if j==0:
                    activity=[asccopy.loc[asccopy["Activity Unique Id"] == i]]
    
                    
                    activity[0]['Activity End Date']=endM[j]
                    activity[0]['hour per month']=hpd*((activity[0]['Activity End Date']-ascendent1['Activity Start Date'][i]).astype('timedelta64[D]')+1)
                    sumh=sumh+activity[0]['hour per month']
                    activity[0]['Month']=activity[0]['Activity End Date'].dt.month
                    if (activity[0]['Month'].values) in Q1:
                        activity[0]['Quarter']=1
                    elif  (activity[0]['Month'].values) in Q2:
                        activity[0]['Quarter']=2
                    elif  (activity[0]['Month'].values) in Q3:
                        activity[0]['Quarter']=3
                    elif  (activity[0]['Month'].values) in Q4:
                        activity[0]['Quarter']=4
                    
        
                    mh=activity[0]['hour per month'].tolist()
                    if mh[0]>limM:
                      activity[0]['Allert Month Hour']=True
     
                    splitted=splitted.append([activity[0]],ignore_index=True)
                    
                    
                        
                    
                elif j==deltaM-1 and j!=0:
                    activity=[asccopy.loc[asccopy["Activity Unique Id"] == i]]
                    activity[0]['Activity Start Date']=startM[j-1]
                    activity[0]['hour per month']=ascendent1['Total'][i]-sumh
                    activity[0]['Month']=activity[0]['Activity End Date'].dt.month
                    if (activity[0]['Month'].values) in Q1:
                        activity[0]['Quarter']=1
                    elif  (activity[0]['Month'].values) in Q2:
                        activity[0]['Quarter']=2
                    elif  (activity[0]['Month'].values) in Q3:
                        activity[0]['Quarter']=3
                    elif  (activity[0]['Month'].values) in Q4:
                        activity[0]['Quarter']=4
                    mh=activity[0]['hour per month'].tolist()
                    if mh[0]>limM:
                      activity[0]['Allert Month Hour']=True
    
                    splitted=splitted.append([activity[0]],ignore_index=True)
                else:
                    activity[0]['Activity End Date']=endM[j]
                    activity[0]['Activity Start Date']=startM[j-1]
                    activity[0]['hour per month']=hpd*((activity[0]['Activity End Date']-activity[0]['Activity Start Date']).astype('timedelta64[D]')+2)
                    sumh=sumh+activity[0]['hour per month']
                    
                    activity[0]['Month']=activity[0]['Activity End Date'].dt.month
                    if (activity[0]['Month'].values) in Q1:
                        activity[0]['Quarter']=1
                    elif  (activity[0]['Month'].values) in Q2:
                        activity[0]['Quarter']=2
                    elif  (activity[0]['Month'].values) in Q3:
                        activity[0]['Quarter']=3
                    elif  (activity[0]['Month'].values) in Q4:
                        activity[0]['Quarter']=4
    
                    mh=activity[0]['hour per month'].tolist()
                    if mh[0]>limM:
                      activity[0]['Allert Month Hour']=True
                    splitted=splitted.append([activity[0]],ignore_index=True)
        else:
            activity=[asccopy.loc[asccopy["Activity Unique Id"] == i]]
    
            
            activity[0]['Month']=activity[0]['Activity End Date'].dt.month
            if (activity[0]['Month'].values) in Q1:
                activity[0]['Quarter']=1
            elif  (activity[0]['Month'].values) in Q2:
                activity[0]['Quarter']=2
            elif  (activity[0]['Month'].values) in Q3:
                activity[0]['Quarter']=3
            elif  (activity[0]['Month'].values) in Q4:
                activity[0]['Quarter']=4
            
            activity[0]['hour per month']=ascendent1['Total'][i]
            mh=activity[0]['hour per month'].tolist()
            if mh[0]>limM:
                activity[0]['Allert Month Hour']=True
            
            
    
            splitted=splitted.append([activity[0]],ignore_index=True)
            
    print('done!')
    
    
    #write output in excel file
    print(" writing data in excel file")
    
    if os.path.isdir("./output")==False:
        os.mkdir("./output")
    
    
    
    
    writer =pd.ExcelWriter("output/result"+str(int(time.time()))+".xlsx")
    workbook  = writer.book
    splitted.to_excel(writer,sheet_name='demand compiled by month')
    ascendent.to_excel(writer,sheet_name='demand compiled')
    dfsso.to_excel(writer,sheet_name='timetable internal')
    dfssoC.to_excel(writer,sheet_name='timetable contractors')
    tse.to_excel(writer, sheet_name='Capacity')
    contractors.to_excel(writer, sheet_name='Capacity Contractors')
    workbook  = writer.book
    
    zoom=75
    
    tse1=tse.copy()
    tse0=tse.copy()
    tseC=tse1.dropna(subset=['PRIMARY'])
    tse0['PRIMARY'].fillna("no primary in capacity", inplace=True)
    
    cell_formatW=workbook.add_format()
    cell_formatW.set_font_color('white')
    cell_formatL = workbook.add_format()
    cell_formatL.set_pattern(1)  # This is optional when using a solid fill.
    cell_formatL.set_bg_color('lime')
    cell_formatB=workbook.add_format()
    cell_formatB.set_bold()
    
    
    #listRegFse=tse['Region'].unique().tolist()
    listregionC=tse['Region'].unique().tolist()
    listMacroS=ascendent['Macroskill'].unique().tolist()
    
    listregion=ascendent['Region'].unique().tolist()
    listprimaryCD=tseC["PRIMARY"].unique().tolist()
    listcontrC=cosvsort["SUPPLIER NAME"].tolist()  
    
    worksheet0 =workbook.add_worksheet("Demand_Macroskill")
    
    
    listMacroS.remove('other')
    for i in range(len(listMacroS)):
        worksheet0.write('''A'''+str(i+2),listMacroS[i])
    worksheet0.write('B1', 'Capacity required')
    
    for i in range(len(listMacroS)):
        worksheet0.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!X:X,A'''+str(i+2)+''')''')
        
    chartsheet0 = workbook.add_chartsheet('Demand by Macroskill')
    bold = workbook.add_format({'bold': 1})
    
    chart0= workbook.add_chart({'type': 'column'})
    
    for col_num0 in range(1,2):
           chart0.add_series({
            'name':       ['Demand_Macroskill', 0, col_num0],
            'categories': ['Demand_Macroskill', 1, 0, len(listMacroS), 0],
            'values':     ['Demand_Macroskill', 1, col_num0, len(listMacroS), col_num0],
            'gap':        30,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True}},
            
        })
    
    # Add a chart title  
    #chart0.set_size({'width': 1280, 'height': 800})
    
    chart0.set_title ({'name': 'Demand by Macroskill'}) 
    
    chart0.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart0.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart0.set_style(7)
    
    chartsheet0.set_chart(chart0)
    chartsheet0.set_zoom(zoom)
    
    #chartsheet0.activate()
    
    worksheet01 =workbook.add_worksheet("Capacity_Region")
    
    
    
    for i in range(len(listregionC)):
        worksheet01.write('''A'''+str(i+2),listregionC[i])
    
    worksheet01.write('B1', 'Capacity available')
    
    
    
    for i in range(len(listregionC)):
        worksheet01.write_formula('''B'''+str(i+2),'''=SUMIF(Capacity!L:L,A'''+str(i+2)+''',Capacity!S:S)''')
     
        
    chartsheet01 = workbook.add_chartsheet('Capacity available by Region')
    
    
    chart01= workbook.add_chart({'type': 'column'})
    
    for col_num01 in range(1,2):
           chart01.add_series({
            'name':       ['Capacity_Region', 0, col_num01],
            'categories': ['Capacity_Region', 1, 0, len(listregionC), 0],
            'values':     ['Capacity_Region', 1, col_num01, len(listregionC), col_num01],
            'gap':        30,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True}},
            
        })  
        
    
    # Add a chart title   
    chart01.set_title ({'name': 'Capacity available by Region'}) 
    
    chart01.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart01.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart01.set_style(7)
    
    chartsheet01.set_chart(chart01)
    chartsheet01.set_zoom(zoom)
    
    
    #chartsheet01.activate()    
        
    
    worksheet02 =workbook.add_worksheet("Capacity_Primary")
    
    listrprimaryC=tse0['PRIMARY'].unique().tolist()
    
    
    for i in range(len(listrprimaryC)):
        worksheet02.write('''A'''+str(i+2),listrprimaryC[i])
    
    worksheet02.write('B1', 'Capacity available')
    
    for i in range(len(listrprimaryC)):
        worksheet02.write_formula('''B'''+str(i+2),'''=SUMIF(Capacity!B:B,A'''+str(i+2)+''',Capacity!S:S)''')
    
        
    chartsheet02 = workbook.add_chartsheet('Capacity available by Primary')
    
    
    chart02= workbook.add_chart({'type': 'column'})
    
    for col_num02 in range(1,2):
           chart02.add_series({
            'name':       ['Capacity_Primary', 0, col_num02],
            'categories': ['Capacity_Primary', 1, 0, len(listrprimaryC), 0],
            'values':     ['Capacity_Primary', 1, col_num02, len(listrprimaryC), col_num01],
            'gap':        20,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True,'rotation': 270}},
            
        })  
        
    # Add a chart title   
    chart02.set_title ({'name': 'Capacity available by Primary Skill'}) 
    
    chart02.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart02.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart02.set_style(7)
    
    chartsheet02.set_chart(chart02)
    chartsheet02.set_zoom(zoom)
    
    #chartsheet02.activate() 
    
    
        
    worksheet1 = workbook.add_worksheet("totalone")
    
    worksheet1.write('A2', 'Total')
    worksheet1.write('B1', 'Total')
    worksheet1.write('A3', 'Detail')
    worksheet1.write_formula('B2', "=SUM('demand compiled'!K:K)")
    
    worksheet1.write('C1', 'Internal')
    worksheet1.write_formula('C3','''=SUMIF('demand compiled'!R:R,"<>0",'demand compiled'!K:K)''')
    
    worksheet1.write('D1', 'External')
    worksheet1.write_formula('D3','''=SUMIF('demand compiled'!U:U,"<>0",'demand compiled'!K:K)''')
    
    worksheet1.write('E1', 'GAP')
    worksheet1.write_formula('E3','=B2-C3-D3')
    #worksheet1.hide()
    #worksheet.hide()
    #worksheet  = workbook.add_worksheet(worksheet)
    chartsheet = workbook.add_chartsheet('TOTAL COVERAGE')
    bold = workbook.add_format({'bold': 1})
    
    chart= workbook.add_chart({'type': 'column', 'subtype': 'percent_stacked'})
    
    for col_num in range(1,5):
           chart.add_series({
            'name':       ['totalone', 0, col_num],
            'categories': ['totalone', 1, 0, 2, 0],
            'values':     ['totalone', 1, col_num, 2, col_num],
            'gap':        25,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 20,'bold': True}},
            
        })
    
    # Add a chart title   
    chart.set_title ({'name': 'Total Coverage'}) 
    
    chart.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart.set_style(7)
    
    chartsheet.set_chart(chart)
    chartsheet.set_zoom(zoom)
    
    #chartsheet.activate()
    
    worksheet2 = workbook.add_worksheet("region_cov")
    
    
    
    for i in range(len(listregion)):
        worksheet2.write('''A'''+str(i+2),listregion[i])
    
    worksheet2.write('B1', 'Internal')
    worksheet2.write('C1', 'External')
    worksheet2.write('D1', 'Gap')
    for i in range(len(listregion)):
        worksheet2.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"FALSE",'demand compiled'!C:C,A'''+str(i+2)+''')''')
        worksheet2.write_formula('''C'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"TRUE",'demand compiled'!C:C,A'''+str(i+2)+''')''')
        worksheet2.write_formula('''D'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"=0",'demand compiled'!C:C,A'''+str(i+2)+''')''')
    
    chartsheet2 = workbook.add_chartsheet('Coverage by Demand Region')
    bold = workbook.add_format({'bold': 1})
    chart2= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    
    
    for col_num1 in range(1,4):
           chart2.add_series({
            'name':       ['region_cov', 0, col_num1],
            'categories': ['region_cov', 1, 0, len(listregion), 0],
            'values':     ['region_cov', 1, col_num1, len(listregion), col_num1],
            'gap':        30,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True}},
            
        })
    chart2.set_title ({'name': 'Coverage by Demand Region'}) 
    
    chart2.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart2.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart2.set_style(7)
    
    chartsheet2.set_chart(chart2)
    
    chartsheet2.set_zoom(zoom)
    
    #chartsheet2.activate()
    
    
    worksheet3 = workbook.add_worksheet("Skill_cov")
    
    
    for i in range(len(listMacroS)):
        worksheet3.write('''A'''+str(i+2),listMacroS[i])
    worksheet3.write('B1', 'Internal')
    worksheet3.write('C1', 'External')
    worksheet3.write('D1', 'Gap')
    
    for i in range(len(listMacroS)):
        worksheet3.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"FALSE",'demand compiled'!X:X,A'''+str(i+2)+''')''')
        worksheet3.write_formula('''C'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"TRUE",'demand compiled'!X:X,A'''+str(i+2)+''')''')
        worksheet3.write_formula('''D'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"=0",'demand compiled'!X:X,A'''+str(i+2)+''')''')
    
    
    chartsheet3 = workbook.add_chartsheet('Skill coverage')
    
    chart3= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})    
    
    for col_num2 in range(1,4):
           chart3.add_series({
            'name':       ['Skill_cov', 0, col_num2],
            'categories': ['Skill_cov', 1, 0, len(listMacroS), 0],
            'values':     ['Skill_cov', 1, col_num2, len(listMacroS), col_num2],
            'gap':        30,
            
            
        })
        
    chart3.set_title ({'name': 'Coverage by Macro Skill'}) 
    
    chart3.set_x_axis({'date_axis': True})
    chart3.set_table()
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart3.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart3.set_style(7)
    
    chartsheet3.set_chart(chart3)
    
    chartsheet3.set_zoom(zoom)
    #chartsheet3.activate()
    
    worksheet31 = workbook.add_worksheet("Skill coverage by Region")
    
    
    for i in range(len(listMacroS)):
        worksheet31.write('''A'''+str(i+2),listMacroS[i],cell_formatB)
    worksheet31.write('B1', 'Internal',cell_formatB)
    worksheet31.write('C1', 'External',cell_formatB)
    worksheet31.write('D1', 'Gap',cell_formatB)
    
    for i in range(len(listregion)):
        worksheet31.write('''AZ'''+str(i),listregion[i],cell_formatW)
        
    
    
    worksheet31.write('F2',"",cell_formatL)
    worksheet31.write('F1',"REGION:",cell_formatB)
    
    worksheet31.data_validation('F2', {'validate': 'list','source': '=$AZ$1:$AZ$8','input_message': 'REGION'})
    
    for i in range(len(listMacroS)):
        worksheet31.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"FALSE",'demand compiled'!X:X,A'''+str(i+2)+''','demand compiled'!C:C,F2)''')
        worksheet31.write_formula('''C'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0",'demand compiled'!T:T,"TRUE",'demand compiled'!X:X,A'''+str(i+2)+''','demand compiled'!C:C,F2)''')
        worksheet31.write_formula('''D'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"=0",'demand compiled'!X:X,A'''+str(i+2)+''','demand compiled'!C:C,F2)''')
    
    #worksheet31.insert_chart('A7', chart)
    #worksheet31.set_column('A:E', None, None, {'hidden': True})
    #chartsheet31 = workbook.add_chartsheet('Skill coverage')
    #
    chart31= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})    
    
    
    for col_num2 in range(1,4):
           chart31.add_series({
            'name':       ['Skill coverage by Region', 0, col_num2],
            'categories': ['Skill coverage by Region', 1, 0, len(listMacroS), 0],
            'values':     ['Skill coverage by Region', 1, col_num2, len(listMacroS), col_num2],
            'gap':        30,
            
            
        })
    chart31.set_size({'width': 1280, 'height': 800})
    
    chart31.set_title ({'name': 'Skill coverage by Region'}) 
    
    chart31.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart31.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart31.set_style(7)
    
    
    
    worksheet31.insert_chart('G1', chart31)
    
    
    worksheet32 = workbook.add_worksheet("Cross Region Matrix")
    alf1=['B','C','D','E','F','G','H','I']
    for i in range(len(listregionC)):
        worksheet32.write('A'+str(i+2),listregionC[i],cell_formatB )
        
    
    for i in range(len(listregion)):
        worksheet32.write(str(alf1[i])+'''1''',listregion[i],cell_formatB)
    
    #=SUMIFS('demand compiled'!K:K,'demand compiled'!C:C,B1,'demand compiled'!Q:Q,A2)
    for i in range(len(listregionC)):
        for j in range(len(listregion)):
            worksheet32.write_formula(str(alf1[j])+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!Q:Q,A'''+str(i+2)+''','demand compiled'!C:C,'''+str(alf1[j])+'''1)''')
    
    
    worksheet33 = workbook.add_worksheet("Cross Region Matrix by Mskill")
    alf1=['B','C','D','E','F','G','H','I']
    for i in range(len(listregionC)):
        worksheet33.write('A'+str(i+2),listregionC[i],cell_formatB )
        
    
    for i in range(len(listregion)):
        worksheet33.write(str(alf1[i])+'''1''',listregion[i],cell_formatB)
    
    for i in range(len(listMacroS)):
        worksheet33.write('''AZ'''+str(i),listMacroS[i],cell_formatW)
    
    worksheet33.write('K2',"",cell_formatL)
    worksheet33.write('K1',"Macro Skill:",cell_formatB)
    worksheet33.data_validation('K2', {'validate': 'list','source': '=$AZ$1:$AZ$16','input_message': 'Macro Skill'})
    
    #=SUMIFS('demand compiled'!K:K,'demand compiled'!C:C,B1,'demand compiled'!Q:Q,A2)
    for i in range(len(listregionC)):
        for j in range(len(listregion)):
            worksheet33.write_formula(str(alf1[j])+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!Q:Q,A'''+str(i+2)+''','demand compiled'!C:C,'''+str(alf1[j])+'''1,'demand compiled'!X:X,K2)''')
    
    
    
    
    
    
    worksheet4 = workbook.add_worksheet("Util_region")
    
    
    for i in range(len(listregionC)):
        worksheet4.write('''A'''+str(i+2),listregionC[i])
        
    worksheet4.write('B1', 'Assigned')
    worksheet4.write('C1', 'Not Assigned')  
    #worksheet4.write_column('E1',listregionC)
    for i in range(len(listregionC)):
        worksheet4.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!L:L,"<>0", 'demand compiled'!Q:Q,A'''+str(i+2)+''')''')
        worksheet4.write_formula('''C'''+str(i+2),'''=SUMIFS(Capacity!O:O,Capacity!L:L,A'''+str(i+2)+''')''')
    
    
    chartsheet4 = workbook.add_chartsheet('Utilization by Region')
    chart4= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
      
    for col_num3 in range(1,3):
           chart4.add_series({
            'name':       ['Util_region', 0, col_num3],
            'categories': ['Util_region', 1, 0, len(listregionC), 0],
            'values':     ['Util_region', 1, col_num3, len(listregionC), col_num3],
            'gap':        30,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True}},
            
        })
    
    chart4.set_title ({'name': 'Utilization by Region'}) 
    
    chart4.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart4.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart4.set_style(7)
    
    chartsheet4.set_chart(chart4)
    
    chartsheet4.set_zoom(zoom)
    #chartsheet4.activate()
    
    
    
    worksheet5 =workbook.add_worksheet("Utilization by Primary Skill")
    
    
    
    
    
    
    
    for i in range(len(listprimaryCD)):
        worksheet5.write('''A'''+str(i+2),listprimaryCD[i],cell_formatB)
    
    worksheet5.write('B1', 'Capacity assigned',cell_formatB)
    worksheet5.write('C1', 'Capacity not assigned',cell_formatB)
    
    
    for i in range(len(listprimaryCD)):
        worksheet5.write_formula('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!O:O,"PRIMARY",'demand compiled'!F:F,A'''+str(i+2)+''')''')
        worksheet5.write_formula('''C'''+str(i+2),'''=IF(Capacity_Primary!B'''+str(i+2)+'''-B'''+str(i+2)+'''<0,0,Capacity_Primary!B'''+str(i+2)+'''-B'''+str(i+2)+''')''')
     
    
    #chartsheet5 = workbook.add_chartsheet('Utilization by Primary Skill')
    
    chart5= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})      
        
      
    for col_num5 in range(1,3):
           chart5.add_series({
            'name':       ['Utilization by Primary Skill', 0, col_num5],
            'categories': ['Utilization by Primary Skill', 1, 0, len(listprimaryCD), 0],
            'values':     ['Utilization by Primary Skill', 1, col_num5, len(listprimaryCD), col_num5],
            'gap':        30,
            
            
        })
        
    chart5.set_size({'width': 1280, 'height': 800})
    chart5.set_title ({'name': 'Utilization by Primary Skill'}) 
    #chart5.set_table()
    chart5.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart5.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart5.set_style(7)
    worksheet5.insert_chart('E1', chart5)
    #chartsheet5.set_chart(chart5)
    
    
    #chartsheet5.activate()
    
    
    
    worksheet10 =workbook.add_worksheet("Contractor distribution")
    
      
    alf = ['B','C','D','E']
    worksheet10.write('A2', 'Total')
    worksheet10.write('B1', 'Contractor distribution')
    #=SUMIFS('demand compiled'!K:K,'demand compiled'!T:T,TRUE,'demand compiled'!U:U,A3)
    for i in range(0,4):
        worksheet10.write('A'+str(i+3), str(listcontrC[i]))
        worksheet10.write('B'+str(i+3),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!T:T,TRUE,'demand compiled'!U:U,A'''+str(i+3)+''')''')
    worksheet10.write('A7', 'Others')
    worksheet10.write('B2','''=SUMIF('demand compiled'!T:T,TRUE,'demand compiled'!K:K)''')
    worksheet10.write('B7','''==SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,"<>"&A3,'demand compiled'!U:U,"<>"&A4,'demand compiled'!U:U,"<>"&A5,'demand compiled'!U:U,"<>"&A6,'demand compiled'!T:T,TRUE)''')
    
    chartsheet10 = workbook.add_chartsheet('Contractors distibution')
    
    chart10= workbook.add_chart({'type': 'column'}) 
    
    for row_num10 in range(1,7):
           chart10.add_series({
            'name':       ['Contractor distribution', row_num10, 0],
            'categories': ['Contractor distribution', 0, 1, 0, 6],
            'values':     ['Contractor distribution', row_num10, 1, row_num10, 1],
            'gap':        15,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 15,'bold': True}},
            
        })
    
    chart10.set_title({'name': 'Contractor Distribution'}) 
    
    chart10.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart10.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart10.set_style(7)
    
    chartsheet10.set_chart(chart10)
    chartsheet10.set_zoom(zoom)
    
    #chartsheet10.activate() 
    
    worksheet11 =workbook.add_worksheet("Contractor_Macro")  
     
    for i in range(0,4):  
        worksheet11.write(str(alf[i])+'''1''',str(listcontrC[i]))
    worksheet11.write('F1', 'Others')
    for i in range(len(listMacroS)):
        worksheet11.write('''A'''+str(i+2),listMacroS[i])
    
    
    for i in range(0,4): 
        for j in range(len(listMacroS)):
            worksheet11.write(str(alf[i])+str(j+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,'''+str(alf[i]+'''1,'demand compiled'!X:X,A'''+str(j+2)+''')'''))
    
    
    for i in range(len(listMacroS)):
        worksheet11.write('''F'''+str(i+2), '''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,"<>"&B1,'demand compiled'!U:U,"<>"&C1,'demand compiled'!U:U,"<>"&D1,'demand compiled'!U:U,"<>"&E1,'demand compiled'!T:T,TRUE,'demand compiled'!X:X,A'''+str(i+2)+''')''')
    #
    chartsheet11 = workbook.add_chartsheet('Contractors by Macro skill')
    chart11= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
      
    for col_num11 in range(1,6):
           chart11.add_series({
            'name':       ['Contractor_Macro', 0, col_num11],
            'categories': ['Contractor_Macro', 1, 0, len(listMacroS), 0],
            'values':     ['Contractor_Macro', 1, col_num11, len(listMacroS), col_num11],
            'gap':        20,
            
            
        })
    
    chart11.set_title ({'name': 'Contractors by Macro skill'}) 
    
    chart11.set_x_axis({'date_axis': True})
    chart11.set_table()
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart11.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart11.set_style(7)
    
    chartsheet11.set_chart(chart11)
    chartsheet11.set_zoom(zoom)
    
    #chartsheet11.activate()
    
    worksheet12 =workbook.add_worksheet("Contractor_Region") 
    
    for i in range(0,4):  
        worksheet12.write(str(alf[i])+'''1''',str(listcontrC[i]))
    worksheet12.write('F1', 'Others')
    
    for i in range(len(listregion)):
        worksheet12.write('''A'''+str(i+2),listregion[i])
    
    for i in range(0,4): 
        for j in range(len(listregion)):
            worksheet12.write(str(alf[i])+str(j+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,'''+str(alf[i]+'''1,'demand compiled'!C:C,A'''+str(j+2)+''')'''))
    
    
    for i in range(len(listregion)):
        worksheet12.write('''F'''+str(i+2), '''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,"<>"&B1,'demand compiled'!U:U,"<>"&C1,'demand compiled'!U:U,"<>"&D1,'demand compiled'!U:U,"<>"&E1,'demand compiled'!T:T,TRUE,'demand compiled'!C:C,A'''+str(i+2)+''')''')
    
    
    chartsheet12 = workbook.add_chartsheet('Contractors by Demand Region')
    chart12= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
      
    for col_num12 in range(1,6):
           chart12.add_series({
            'name':       ['Contractor_Region', 0, col_num12],
            'categories': ['Contractor_Region', 1, 0, len(listregion), 0],
            'values':     ['Contractor_Region', 1, col_num12, len(listregion), col_num12],
            'gap':        20,
            
            
        })
    #chart12.set_size({'width': 1280, 'height': 800})
        
    chart12.set_title ({'name': 'Contractors by Demand Region'}) 
    chart12.set_table()
    chart12.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart12.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart12.set_style(7)
    
    chartsheet12.set_chart(chart12)
    chartsheet12.set_zoom(zoom)
    
    #chartsheet12.activate()
    
    
    worksheet13 = workbook.add_worksheet("Util_contr_Supp")
    for i in range(0,4):  
        worksheet13.write('''A'''+str(i+2),str(listcontrC[i]))
    worksheet13.write('A6', 'Others')
    worksheet13.write('B1', 'Assigned')
    worksheet13.write('C1', 'Not Assigned')
    
    
    for i in range(0,4): 
        worksheet13.write('''B'''+str(i+2),'''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,A'''+str(i+2)+''')''' )
        worksheet13.write('''C'''+str(i+2),'''=SUMIFS('Capacity Contractors'!R:R,'Capacity Contractors'!C:C,A'''+str(i+2)+''')-B'''+str(i+2))
    
    worksheet13.write('B6', '''=SUMIFS('demand compiled'!K:K,'demand compiled'!U:U,"<>"&A2,'demand compiled'!U:U,"<>"&A3,'demand compiled'!U:U,"<>"&A4,'demand compiled'!U:U,"<>"&A5,'demand compiled'!U:U,"<>0")''')
    worksheet13.write('C6', '''=SUMIFS('Capacity Contractors'!R:R,'Capacity Contractors'!C:C,"<>"&A2,'Capacity Contractors'!C:C,"<>"&A3,'Capacity Contractors'!C:C,"<>"&A4,'Capacity Contractors'!C:C,"<>"&A5)-B6''')
    
    chartsheet13 = workbook.add_chartsheet('Utilization Supplier')
    chart13= workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
      
    for col_num13 in range(1,3):
           chart13.add_series({
            'name':       ['Util_contr_Supp', 0, col_num13],
            'categories': ['Util_contr_Supp', 1, 0, 5, 0],
            'values':     ['Util_contr_Supp', 1, col_num13, 5, col_num13],
            'gap':        30,
            'data_labels': {'value': True,'num_format': '0','font': {'name': 'Consolas','size': 10,'bold': True}},
            
        })
    
    chart13.set_title ({'name': 'Utilization Supplier'}) 
    
    chart13.set_x_axis({'date_axis': True})
    
    # Add x-axis label  
    #chart.set_x_axis({'name': 'Test number'}) 
      
    # Add y-axis label  
    chart13.set_y_axis({'name': 'Total hours'}) 
      
    # Set an Excel chart style. 
    chart13.set_style(7)
    
    chartsheet13.set_chart(chart13)
    
    chartsheet13.set_zoom(zoom)
    #chartsheet13.activate()
    
    worksheet0.hide()
    worksheet01.hide()
    worksheet02.hide()
    worksheet1.hide()
    worksheet2.hide()
    worksheet3.hide()
    worksheet4.hide()
    worksheet10.hide()
    worksheet12.hide()
    worksheet13.hide()
    worksheet11.hide()
    
    workbook.close()
    writer.save()

    
    print("done!")
    
    
    
                
    end=time.time()
    
    print(" done in:", int(end-begin), "sec")  
    
    
    print("\n")
    
    totalDEM=sum(ascendent["Total"])
    gap =ascendent.loc[ascendent["SSO"]==0]
    result=ascendent.loc[ascendent["SSO"]!=0]
    resultINT=result.loc[result["contractor"]==False]
    resultEXT=result.loc[result["contractor"]==True]
    print("The total coverage assigned to internal FSEs is: "+"{:.2%}".format(sum(resultINT["Total"])/totalDEM))
    print("\n")
    print("The total coverage assigned to external FSEs is: "+"{:.2%}".format(sum(resultEXT["Total"])/totalDEM))
    print("\n")
    print("The total GAP is: "+"{:.2%}".format(sum(gap["Total"])/totalDEM))
    
    print("\n-- OPTIMA run completed. --\n" ) 
    input("\n-- press Enter to close the command window --\n" ) 
    print("Bye Bye")
    
else:
    print("Bye Bye")
    
