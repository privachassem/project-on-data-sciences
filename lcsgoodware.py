# -*- coding: utf-8 -*-

import xlrd, os
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from sklearn import preprocessing
from xlwt import Workbook
from androguard.core.bytecodes.apk import APK
from tkinter.filedialog import askopenfilename, askdirectory

perm = list()
class VectorGroupPermis:
    def __init__(self, apk, pos):
        self.data = []
        self.don = []
        self.apk = APK(str(apk))
        self.pos = pos
        self.main()
        
    # On recupere les permitions des APK
    def getVectorOfXml(self):
        data_permission = []
        for elt in self.apk.get_permissions():
            permis = elt.split('.')
            if 'permission' in permis:
                data_permission.append(permis[-1])
        perm.append(data_permission)
        
        return perm

    # construction de notre lcs pour tous les apks malware
    def lcs(self):  

        S = self.getVectorOfXml()
        first_lcs = S[0]

        for liste in S:
            
            second_lcs = liste

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

            first_lcs = lcs_set
        return lcs_set

    
    # Creer le fichier excel
    def setVector(self, vector):
        liste = []
        for colVal in vector:
            
            liste.append(colVal)

        for item in liste:
            for k, elt in enumerate(item):
                ligne = feuil.row(self.pos)
                ligne.write(k, elt)    
        book.save('lcsgoodware.xls')

    
    def main(self):
        a = self.lcs()
        self.setVector(a)
        print(a)
        
        
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