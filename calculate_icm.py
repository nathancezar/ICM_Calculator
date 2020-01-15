# -*- coding: UTF-8 -*-
__author__ = 'Equipe-ECV'

from database.controller import Controller


class IcmCalculator():
    def __init__(self):
        self._results = []
        self._ICM = 0
        self._IP = 0
        self._IC = 0
        self._controller = Controller([])

    def calculateAllICM(self, highway, direction, contract) :
        """
            Calculates the ICM of all kilometers in the highway, counting only
            post processed items.
        """
        if self._controller.verifyContractAndHighway(contract, highway):
            self._results = self._controller.getResults(highway, direction)

        kmList = []
        for line in self._results:
            km = int(line['Km_Calc'])
            if km not in kmList:
                kmList.append(km)

        for km in kmList:
            IP, IC, ICM, totalPothole, totalPatch, totalCrack, totalClearing, \
            totalDrainage, totalSignal = self.calculateICM(km)

            calculatedIcm = {
                "highway": highway,
                "km": km,
                "direction": direction,
                "pothole": totalPothole,
                "repair": totalPatch,
                "crack": totalCrack,
                "clearing": totalClearing,
                "signal": totalSignal,
                "drainage": totalDrainage,
                "ICP": IP,
                "ICC": IC,
                "ICM": ICM
            }
            self._controller.insertIcm(calculatedIcm)

    def calculateICM(self, Kilometer) :
        """
            Calculates the kilometer ICM sent as a parameter
        """
        pothole, totalPothole = self.calculatePothole(Kilometer)
        patch, totalPatch = self.calculatePatch(Kilometer)
        crack, totalCrack = self.calculateCrack(Kilometer)
        clearing, totalClearing = self.calculateClearing(Kilometer)
        drenage, totalDrainage = self.calculateDrainage(Kilometer)
        signal, totalSignal = self.calculateSignal(Kilometer)
        IP = (pothole * 50) + (patch * 30) + (crack * 20)
        IC = (clearing * 30) + (drenage * 20) + (signal * 50)
        ICM = (IP * 0.70) + (IC * 0.30)

        return IP, IC, ICM, totalPothole, totalPatch, totalCrack, \
               totalClearing, totalDrainage, totalSignal

    def calculatePothole(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 1:
                total = int(dic['total'])
                self._results.remove(dic)
                break
        if total <= 2 and total >= 0:
            return 0.25, total
        elif total > 2 and total <= 5:
            return 0.5, total
        elif total > 5:
            return 1, total

    def calculatePatch(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 2:
                total = int(dic['total'])
                self._results.remove(dic)
                break
        if total <= 2 and total >= 0:
            return 0.25, total
        elif total > 2 and total <= 5:
            return 0.5, total
        elif total > 5:
            return 1, total

    def calculateCrack(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 3:
                total = float(dic['total'])
                self._results.remove(dic)
                break
        if total <= 10 and total >= 0:
            return 0.25, total
        elif total > 10 and total <= 50:
            return 0.5, total
        elif total > 50:
            return 1, total

    def calculateClearing(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 5:
                total = float(dic['total'])
                self._results.remove(dic)
                break
        if total <= 10 and total >= 0:
            return 0.25, total
        elif total > 10 and total <= 50:
            return 0.5, total
        elif total > 50:
            return 1, total

    def calculateDrainage(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 4:
                total = int(dic['total'])
                self._results.remove(dic)
                break
        if total <= 2 and total >= 0:
            return 0.25, total
        elif total > 2 and total <= 5:
            return 0.5, total
        elif total > 5:
            return 1, total

    def calculateSignal(self, Kilometer) :
        total = 0
        for dic in self._results:
            if int(dic['Km_Calc']) == Kilometer and dic['item'].id == 8:
                total = int(dic['total'])
                self._results.remove(dic)
                break
        if total <= 2 and total >= 0:
            return 0.25, total
        elif total > 2 and total <= 5:
            return 0.5, total
        elif total > 5:
            return 1, total
