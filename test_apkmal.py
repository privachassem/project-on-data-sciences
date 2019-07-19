# -*- coding: utf-8 -*-

import xlrd, os
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from sklearn import preprocessing
import csv
from xlwt import Workbook
from androguard.core.bytecodes.apk import APK
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame
import numpy as np


perm = list()
lcsper =['ACCESS_NETWORK_STATE', 'GET_ACCOUNTS', 'INTERNET', 'WAKE_LOCK', 'VIBRATE', 'INSTALL_SHORTCUT', 'RECEIVE', 'WRITE_EXTERNAL_STORAGE', 'C2D_MESSAGE']

class VectorGroupPermis:

    def __init__(self, apk):
        self.data = []
        self.val = []
        self.apk = APK(str(apk))
        self.main()

    # On recupere les permitions de APK
    def getVectorOfXml(self):
        data_permission = []
        for elt in self.apk.get_permissions():
            permis = elt.split('.')
            if 'permission' in permis:
                data_permission.append(permis[-1])
        return data_permission 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
# construction de notre lcs1 = perm + lcsmal 

    def lcs(self,elt):
        dataPermis = self.getVectorOfXml()
        m = len(dataPermis)
        n = len(elt)
        counter = [[0]*(n+1) for x in range(m+1)]
        longest = 0
        lcs_set = list()
        for i in range(m):
            for j in range(n):
                if dataPermis[i] == elt[j]:
                    c = counter[i][j] + 1
                    counter[i+1][j+1] = c
                    if c > longest:
                        lcs_set = list()
                        longest = c
                        lcs_set.append(dataPermis[i-c+1:i+1])  
                    elif c == longest:
                        lcs_set.append(dataPermis[i-c+1:i+1])

        return lcs_set

    # comparaison du lcs1 et du lcs si intersection alors 1 sinon 0
    def assertPermissionMalisiusOrNot(self, apkPermissions):

        var = list()
        for i, k in enumerate(apkPermissions):
            if k[0] in lcsper:
                var.append(1)
            else:
                var.append(0)
        print(var)
        return var

    #charger notre lcs dans un tableau numpy
    def charger_numpy(self):
        a = self.lcs(self.getVectorOfXml())
        self.liste_numpy = np.array(self.assertPermissionMalisiusOrNot(a))
        return self.liste_numpy

    # charger notre lcs dans notre pandas
    def charger_pandas(self): 
        c = self.charger_numpy()
        d = c.T     
        self.famille_pandas_df = pd.DataFrame(c)
        somme1 = self.famille_pandas_df.T
        somme = somme1.sum()
        print(somme)
        for item in somme:
            if item > 0:
                print("l'application est goodware")
            else:
                print("l'application est non goodware")

        return self.famille_pandas_df


    def main(self):
        print("***********************")
        self.charger_pandas()
        print("************************")

if __name__=="__main__":

    apk = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    VectorGroupPermis(apk)
    print("Opération terminé avec succès")


