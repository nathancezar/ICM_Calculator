# -*- coding: UTF-8 -*-
__author__ = 'Equipe-ECV'

import csv
import argparse
import pathlib


class calculateICMByCsv():
    def __init__(self, args):
        self._path = args["path"]
        self._csvList = []
        self._potholeList = []
        self._drenageList = []
        self._signalList = []
        self._clearingList = []
        self._crackList = []
        self._patchList = []
        self._icmPerKm = []
        self._maxKm = 0
        self._ICM = 0
        self._IP = 0
        self._IC = 0

    def getFilesList(self, path):
        return list(pathlib.Path(self._path).rglob("*.csv"))

    def openCSVFile(self, filesList):
        for csvFile in filesList:
            with open(csvFile, mode='r') as csvFile:
                csvFile.seek(0)
                csvReader = csv.DictReader(csvFile)
                for row in csvReader:
                    self._csvList.append(row)
                    rowKm = int(row["Km"])
                    if rowKm > self._maxKm:
                        self._maxKm = rowKm

    def separateByType(self):
        for row in self._csvList:
            rowType = row["Tipo"]
            if rowType == "Drenagem":
                self._drenageList.append(row)
            elif rowType == "Placa":
                self._signalList.append(row)
            elif rowType == "Buraco":
                self._potholeList.append(row)
            elif rowType == "Rocada":
                self._clearingList.append(row)
            elif rowType == "Trinca":
                self._crackList.append(row)
            elif rowType == "Remendo":
                self._patchList.append(row)

    def calculatePothole(self, Kilometer) :
        valor = 0
        index = ""
        situationList = [float(x["Situacao"]) for x in \
                        self._potholeList if int(x["Km"]) == Kilometer]
        situation = sum(situationList)
        if situation < 2 and situation > 0:
            valor = 0.25
            index = "Baixo"
        elif situation > 2 and situation < 5:
            valor = 0.5
            index = "Medio"
        elif situation > 5:
            valor = 1
            index = "Alto"
        return valor, index

    def calculatePatch(self, Kilometer) :
        valor = 0
        index = ""
        situationList = [float(x["Situacao"]) for x in \
                        self._patchList if int(x["Km"]) == Kilometer]
        situation = sum(situationList)
        if situation < 2 and situation > 0:
            valor = 0.25
            index = "Baixo"
        elif situation > 2 and situation < 5:
            valor = 0.5
            index = "Medio"
        elif situation > 5:
            valor = 1
            index = "Alto"
        return valor, index

    def calculateCrack(self, Kilometer) :
        valor = 0
        index = ""
        situationList = [float(x["Situacao"]) for x in \
                        self._crackList if int(x["Km"]) == Kilometer]
        situation = sum(situationList)
        if situation < 10 and situation > 0:
            valor = 0.25
            index = "Baixo"
        elif situation > 10 and situation < 50:
            valor = 0.5
            index = "Medio"
        elif situation > 50 :
            valor = 1
            index = "Alto"
        return valor, index

    def calculateClearing(self, Kilometer) :
        good, regular, bad = 0, 0, 0
        for row in self._clearingList :
            km = int(row["Km"])
            situation = row["Situacao"]
            if km == Kilometer :
                if situation == "Bom":
                    good += 1
                elif situation == "Regular":
                    regular += 1
                else :
                    bad += 1
        if (good + regular + bad) > 0 :
            return 0.25, "Bom"
        else :
            return 1, "Ruim"

    def calculateDrenage(self, Kilometer) :
        good, regular, bad = 0, 0, 0
        for row in self._drenageList :
            situation = row["Situacao"]
            if int(row["Km"]) == Kilometer :
                if situation == "Bom":
                    good += 1
                elif situation == "Regular":
                    regular += 1
                else :
                    bad += 1
        if (good + regular + bad) > 0 :
            return 0.25, "Bom"
        else :
            return 1, "Ruim"

    def calculateSignal(self, Kilometer) :
        good, regular, bad = 0, 0, 0
        for row in self._signalList :
            if int(row["Km"]) == Kilometer :
                if row["Situacao"] == "Bom":
                    good += 1
                elif row["Situacao"] == "Regular":
                    regular += 1
                else :
                    bad += 1
        if (good + regular + bad) > 0 :
            return 0.25, "Bom"
        else :
            return 1, "Ruim"

    def calculateICM(self, Kilometer) :
        pothole, potholeIndex = self.calculatePothole(Kilometer)
        patch, patchIndex = self.calculatePatch(Kilometer)
        crack, crackIndex = self.calculateCrack(Kilometer)
        clearing, clearingIndex = self.calculateClearing(Kilometer)
        drenage, drenageIndex = self.calculateDrenage(Kilometer)
        signal, signalIndex = self.calculateSignal(Kilometer)

        self._IP = (pothole * 50) + (patch * 30) + (crack * 20)
        self._IC = (clearing * 30) + (drenage * 20) + (signal * 50)
        self._ICM = (self._IP * 0.70) + (self._IC * 0.30)

        return potholeIndex, patchIndex, crackIndex, clearingIndex, \
               drenageIndex, signalIndex

    def calculateAllICM(self) :
        for i in range(self._maxKm):
            potholeIndex, patchIndex, crackIndex, clearingIndex, \
            drenageIndex, signalIndex = self.calculateICM(i+1)
            self._icmPerKm.append([i+1, potholeIndex, patchIndex,crackIndex,
                                  clearingIndex, drenageIndex, signalIndex,
                                  "{:.2f}".format(self._IP),
                                  "{:.2f}".format(self._IC),
                                  "{:.2f}".format(self._ICM)])

    def saveCsvFile(self, lista):
        fileName = self._path + "/{0}-Result.csv".format(
                   pathlib.Path(self._path).name)
        with open(fileName, mode='w') as newFile:
            writer = csv.writer(newFile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Km', 'Buraco', 'Remendo', 'Trinca', 'Rocada',
                            'Drenagem', 'Sinalizacao', 'IP', 'IC' , 'ICM'])
            writer.writerows(lista)

    def run(self):
        filesList = self.getFilesList(self._path)
        self.openCSVFile(filesList)
        self.separateByType()
        self.calculateAllICM()
        self.saveCsvFile(self._icmPerKm)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,
                    help="path to csv file")
    args = vars(ap.parse_args())
    grf = calculateICMByCsv(args)
    grf.run()
