# -*- coding: utf-8 -*-
# changement des librairies python.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


lcsper =['ACCESS_NETWORK_STATE', 'GET_ACCOUNTS', 'INTERNET', 'WAKE_LOCK', 'VIBRATE', 'INSTALL_SHORTCUT', 'RECEIVE', 'WRITE_EXTERNAL_STORAGE', 'C2D_MESSAGE']

class VectorGroupPermis:

    def __init__(self, apk, pos):
        self.data = []
        self.don = []
        self.apk = APK(str(apk))
        self.pos = pos
        self.main()
        
    # On recupere les permitions des APK
    def getVectorOfXml(self):
        perm = []
        data_permission = []
        for elt in self.apk.get_permissions():
            permis = elt.split('.')
            if 'permission' in permis:
                data_permission.append(permis[-1])
        perm.append(data_permission)
        
        return perm

    # construction de notre lcs pour tous les apks malware
    def lcs(self):  
        liste = []
        vector = self.getVectorOfXml()
        for elt in vector:
            
            first_lcs = elt
            second_lcs = lcsper
            m = len(first_lcs) 
            n = len(second_lcs)

            counter = [[0]*(n+1) for x in range(m+1)]
            longest = 0
            lcs_set = list()
        
            for i in range(m):
                for j in range(n):   
                    if first_lcs[i] == second_lcs[j]:
                        c = counter[i][j] + 1
                        counter[i+1][j+1] = c
                        if c > longest:
                            lcs_set = list()
                            longest = c
                            lcs_set.append(first_lcs[i-c+1:i+1])
                        elif c == longest:
                            lcs_set.append(first_lcs[i-c+1:i+1]) 
                    else:
                        continue
            
            liste.append(lcs_set) 

        return liste
    
    # Creer le fichier excel
    def setVector(self, vector):
        liste = list()
        for item in vector:
            for ite in item:
                liste.append(ite)
        for k, elt in enumerate(liste):
            ligne = feuil.row(self.pos)
            ligne.write(k, str(elt))
        ligne.write(k + 1, str(0))    
        book.save('lcsapkgoodtest0.xls')

    def main(self):
        a = self.lcs()
        print(a)
        self.setVector(a)


if __name__=="__main__":
    directory = askdirectory()
    file = os.listdir(directory)
    book = Workbook()
    feuil = book.add_sheet('feuille 1')
    pos = 0
    for apk in file:
        try:
            apk = directory + '/' + apk
            VectorGroupPermis(apk, pos)
            pos += 1
        except:
            continue
    print("Opération terminé avec succès")