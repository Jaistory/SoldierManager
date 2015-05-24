__author__ = 'joochangbin'

import random
from soldier import *
from datetime import datetime
#from Global import *

class Workable:
    exchangeCount = 0
    constructionCount = 0
    computationCount = 0
    juniorCount = 0
    seniorCount = 0
    total = 0

    def __init__(self, exCount, conCount, comCount, juCount, seCount, total):
        self.exchangeCount = exCount
        self.constructionCount = conCount
        self.computationCount = comCount
        self.juniorCount = juCount
        self.seniorCount = seCount
        self.total = total


class ExchangeWorkManage:
    totalSoldierArray = [0 for _ in range(20)]
    exchangeSoldierArray = [0 for _ in range(10)]
    constructSoldierArray = [0 for _ in range(10)]
    adminSoldierArray = [0 for _ in range(10)]

    workable = Workable

    NEED_WORK_SOLDIER = 8
    WORK_TIME_GAP = 4

    def distributeSoldier(self, assignCode):
        """

        :rtype : Array
        """
        soldierArray = [0 for _ in range(5)]

        if assignCode == AssignmentCode.EXCHANGE:
            soldierArray = self.exchangeSoldierArray
        elif assignCode == AssignmentCode.CONSTRUCTION:
            soldierArray = self.constructSoldierArray
        elif assignCode == AssignmentCode.ADMINISTATOR:
            soldierArray = self.adminSoldierArray
        elif assignCode == AssignmentCode.TOTAL:
            soldierArray = self.totalSoldierArray

        return soldierArray

    def workableSoldier(self, assignCode, rank, date):
        #soldierArray = [0 for _ in range(5)]
        #tmpSoldier = Soldier
        result = 0
        #count = 0

        soldierArray = self.distributeSoldier(assignCode)
        for i in range(len(soldierArray)-1):
            tmpSoldier = soldierArray[i]
            if tmpSoldier.conditions.condition == Condition.NORMAL or tmpSoldier.conditions.condition == Condition.COMBAT:
                if tmpSoldier.conditions.startDate >= date and tmpSoldier.conditions.endDate <= date:
                    if tmpSoldier.rank == rank or rank == SoldierRank.NONE:
                        result += 1
        return result

    def getWorkableSoldierCount(self, date):
        self.workable.exchangeCount = self.workableSoldier(AssignmentCode.EXCHANGE, SoldierGrade.NONE, date)
        self.workable.constructionCount = self.workableSoldier(AssignmentCode.CONSTRUCT, SoldierGrade.NONE, date)
        self.workable.computationCount = self.workableSoldier(AssignmentCode.ADMINISTRATOR, SoldierGrade.NONE, date)
        self.workable.juniorCount = self.workableSoldier(AssignmentCode.ALL, SoldierGrade.JUNIOR, date)
        self.workable.seniorCount = self.workableSoldier(AssignmentCode.ALL, SoldierGrade.SENIOR, date)

    def abstractSoldierArray(self, assignCode, rank, date):
        soldierArray = []
        #tmpSoldierArray = []
        #count = 0
        self.getWorkableSoldierCount(date)

        tmpSoldierArray = self.distributeSoldier(assignCode)
        for i in range(len(tmpSoldierArray)-1):
            soldier = tmpSoldierArray[i]
            if self.workable.total < 8 and soldier.rank == rank:
                if soldier.conditions.condition == Condition.NORMAL or soldier.conditions.condition == Condition.COMBAT:
                    if soldier.conditions.startDate <= date and soldier.conditions.endDate >= date:
                        soldierArray[i] = soldier
                        j += 1
                        # else:
                        # if soldier.rank  == rank:
                        #    for k in

        return soldierArray

    def sortWorktiredness(self, assignCode):
        soldierArray = []
        count = 0
        #i = 0
        #j = 0

        if assignCode == AssignmentCode.EXCHANGE:
            soldierArray = self.exchangeSoldierArray
            count = self.workable.exchangeCount
        elif assignCode == AssignmentCode.CONSTRUCTION:
            soldierArray = self.constructSoldierArray
            count = self.workable.constructionCount
        elif assignCode == AssignmentCode.ADMINISTATOR:
            soldierArray = self.adminSoldierArray
            count = self.workable.computationCount
        elif assignCode == AssignmentCode.TOTAL:
            soldierArray = self.totalSoldierArray
            count = self.workable.total

        for i in range(count):
            stand = soldierArray[i].totalWork
            j = i + 1
            #warning j is not used
            for j in range(count):
                if stand > soldierArray[i].totalWork:
                    tmpSoldier = soldierArray[i]
                    soldierArray[i] = soldierArray[j]
                    soldierArray[j] = tmpSoldier

        return soldierArray

    def sameRatioWork(self, soldierArray):
        sameRatioWorkArray = []
        #i = 0
        #j = 0
        #k = 0
        #stand = 0

        for i in range(0, (len(soldierArray)-1)):
            stand = soldierArray[i].totalWork
            k = i
            for j in range(i+1, len(soldierArray)-1):
                if stand == soldierArray[j].totalWork:
                    k = j
                else:
                    break

            numSet = set(i, k)
            sameRatioWorkArray.append(numSet)
            i = k

        return sameRatioWorkArray

    def branchWorkTime(k, totalNeeds):
        result = WorkTime.NIGHT
        caseDic = {1 : WorkTime.EVENING,
                   2 : WorkTime.AFTERNOON,
                   3 : WorkTime.MORNING}

        if k != 4:
            result = caseDic.get(k%4)

        return result

    def setDrawLotsForTurn(self, soldierArray, selectedNumArray, sameRatioWork, currentDate, work):
        result = 0
        sameRatioWorkArray = list(sameRatioWork)

        random.seed(datetime.now())
        if sameRatioWorkArray[0] == sameRatioWorkArray[1]:
            #setCalendarEvent
            result = -1
        else:
            check = False
            while 1:
                result = random.randint(0, sameRatioWorkArray[len(sameRatioWorkArray)-1])
                for i in range(0, len(selectedNumArray)-1):
                    if selectedNumArray[i] == result:
                        if check != True:
                            check = False
                        else:
                            check = True
                if check == True:
                    break

            #setCalendarEvent
        return result

    def makeDayWork(self, rankArray, currentDate, needCount):
        #result = 0
        #gap = 0
        work = WorkTime.NIGHT
        selectedNumArray = []
        sameRatioArray = []
        totalNeeds =  self.NEED_WORK_SOLDIER - len(rankArray)

        random.seed(datetime.now())
        rankArrayLen = len(rankArray)
        if rankArrayLen >= totalNeeds:
            gap = rankArray[rankArrayLen].totalWork - rankArray[0].totalWork
            if gap >= self.WORK_TIME_GAP:
                sameRatioArray = self.sameRatioWork(rankArray)
                r = 0
                for k in range(0, totalNeeds-1):
                    work = self.branchWorkTime(k, totalNeeds)
                    check = self.setDrawLotsForTurn(rankArray, selectedNumArray, sameRatioArray[r], currentDate, work)
                    if check == -1:
                        r += 1
                    else:
                        selectedNumArray[len(selectedNumArray)] = check
            else:
                randNum = 0
                for k in range(0, totalNeeds):
                    randNum = random.randint(0, len(rankArray)-1)
                    work = self.branchWorkTime(k, totalNeeds)
                    #self.setCalendarEvent(currentDate, rankArray[randNum], work)
                    rankArray.remove(randNum)


    def makeExchangeDayWork(self, currentDate):
        #seniorArray = []
        #juniorArray = []
        result = 0

        self.sortWorktiredness(self, AssignmentCode.ALL)
        seniorArray = self.abstractSoldierArray(self, AssignmentCode.ALL, SoldierRank.SENIOR, currentDate)
        juniorArray = self.abstractSoldierArray(self, AssignmentCode.ALL, SoldierRank.JUNIOR, currentDate)

        self.getWorkableSoldierCount(self, currentDate)

        if len(juniorArray) < 4:
            needCount = self.NEED_WORK_SOLDIER - juniorArray.__len__()  # NEED_WORK_SOLDIER 8

        needCount = self.makeDayWork(seniorArray, currentDate, needCount)
        needCount = self.makeDayWork(juniorArray, currentDate, needCount)
        if needCount != 0:
            result = -1

        return result

    def makeWeekWork(self):
        #warning this section get a current date and start date
        currentDate = datetime.datetime(0, 0, 0)
        startDate = currentDate
        endDate = datetime.datetime(0, 0, 0)
        i = 0
        for i in range(startDate.day, endDate.day):
            self.makeExchangeDayWork(currentDate)
            i += 1
