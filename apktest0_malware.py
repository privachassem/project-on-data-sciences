# -*- coding: utf-8 -*-

import xlrd, os
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from sklearn import preprocessing
import csv
from xlwt import Workbook
from androguard.core.bytecodes.apk import APK
from tkinter.filedialog import askopenfilename, askdirectory
import pandas as pd
from pandas import DataFrame
import numpy as np


perm = list()
lcsper =['INTERNET', 'WAKE_LOCK', 'CHANGE_WIFI_STATE', 'ACCESS_WIFI_STATE', 
        'READ_LOGS', 'ACCESS_FINE_LOCATION', 'WRITE_CONTACTS', 'READ_CONTACTS', 
        'WRITE_SMS', 'CALL_PHONE', 'KILL_BACKGROUND_PROCESSES', 'GET_TASKS', 'RECEIVE_SMS',
        'READ_PHONE_STATE', 'READ_HISTORY_BOOKMARKS', 'READ_SMS', 'RECEIVE_BOOT_COMPLETED',	
        'ACCESS_NETWORK_STATE', 'PROCESS_OUTGOING_CALLS', 'SEND_SMS', 'ACCESS_COARSE_UPDATES', 'RECEIVE_MMS']

class VectorGroupPermis:

    def __init__(self, pos):
        self.document = xlrd.open_workbook("apk.xls")
        self.feuille = self.document.sheet_by_index(0)
        self.cols = self.feuille.ncols
        self.rows = self.feuille.nrows
        self.data = []
        self.val = []
        self.pos = pos
        self.main()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    
    # Recuperer les elements du fichier excel
    def getVectorOfSheet(self):
        for col in range(0, self.cols):
            self.val = []
            for row in range(0, self.rows):
                self.val += [str(self.feuille.cell_value(rowx=row, colx=col)).upper()]
            self.data.append(self.val)
        return self.data

    # Creer le fichier excel
    def setVector(self, vector):
        liste = []
        for colVal in vector:
            
            liste.append(colVal)

        for k, elt in enumerate(liste):
            ligne = feuil.row(self.pos)
            ligne.write(k, str(elt))    
        book.save('resultatcomp.xls')

    # On verifi si la permission est dangereuse(1) ou non(0)
    def assertPermissionMalisiusOrNot(self, apkPermissions):

        liste = list()
        for i, k in enumerate(apkPermissions): 
            var = list()
            for j, item in enumerate(k):
                if apkPermissions[i][j] in lcsper:
                    var.append(1)
                else:
                    var.append(0)
            liste.append(var)
        return liste

    #charger notre lcs dans un tableau numpy
    def charger_numpy(self):
        a = self.getVectorOfSheet()
        self.liste_numpy = np.array(self.assertPermissionMalisiusOrNot(a))
        return self.liste_numpy

    # charger notre lcs dans notre pandas
    def charger_pandas(self): 
        c = self.charger_numpy()
        d = c.T     
        self.famille_pandas_df = pd.DataFrame(d)
        somme1 = self.famille_pandas_df.T
        somme = somme1.sum()

        self.famille_pandas_df['somme'] = (somme)
        decision = []
        pourcentage = []
        total = 22
        bien = 0
        mal = 0

        for item in somme:
            pour = (item/total)*100
            pourcentage.append(pour)
            if item > 0:
                bien += 1
                decision.append('malware')
            else:
                mal += 1
                decision.append('goodware')
        self.famille_pandas_df['decision'] = (decision)
        self.famille_pandas_df['degré en pourcentage (%)'] = (pourcentage)
        decision = np.array(decision)
        self.famille_pandas_df = pd.DataFrame(self.famille_pandas_df)

        print(bien,mal)

        
        with pd.ExcelWriter('resultat_apkmalware.xls') as writer:
            self.famille_pandas_df.to_excel(writer, sheet_name='resultatmalware', startcol=1)
            
        return somme


    def main(self):
        d = self.charger_pandas()
        a = self.getVectorOfSheet()
        b = self.assertPermissionMalisiusOrNot(a)
        print(d)
        print('***************************************************************')
        print(b)
        print('***************************************************************')

if __name__=="__main__":
    book = Workbook()
    feuil = book.add_sheet('feuille 1') 
    pos = 0
    for i in range(100):
        pos += 1
    VectorGroupPermis(pos)
    print("Opération terminé avec succès")


