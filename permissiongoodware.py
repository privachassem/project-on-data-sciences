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
        
    # On recupere les permitions des APKs
    def getVectorOfXml(self):
        data_permission = []
        for elt in self.apk.get_permissions():
            permis = elt.split('.')
            if 'permission' in permis:
                data_permission.append(permis[-1])
        return data_permission

    # Creer le fichier excel
    def setVector(self, vector):
        liste = []
        for colVal in vector:
            
            liste.append(colVal)
    
        for k, elt in enumerate(liste):
            ligne = feuil.row(self.pos)
            ligne.write(k, elt)    
        book.save('listepermission.xls')

    def main(self):
        a = self.getVectorOfXml()
        self.setVector(a)
        print(a)
                
if __name__=="__main__":
    directory = askdirectory()
    file = os.listdir(directory)
    book = Workbook()
    feuil = book.add_sheet('feuille 1')
    pos = 0
    for apk in file:
        apk = directory + '/' + apk
        VectorGroupPermis(apk, pos)
        pos += 1

    print("Opération terminé avec succès")