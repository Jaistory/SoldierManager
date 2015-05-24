__author__ = 'joochangbin'

import datetime, time
from Global import *


AssignmentCode = enum('NONE', 'EXCHANGE', 'CONSTRUCTION', 'ADMINISTRATOR','COMPUTATION', 'ALL')
SoldierGrade = enum('SECOND', 'PRIVATE_FIRST', 'CORPORAL', 'SERGANT')
SoldierRank = enum('JUNIOR', 'SENIOR')
WorkTime = enum('MORNING', 'AFTERNOON', 'EVENING', 'NIGHT')
WorkTiredness = enum(CONSTRUCTION = 2,
                     MORNING = 1,              #8:30 ~ 12:30
                     AFTERNOON = 2,            #12:30 ~ 18:30
                     EVENING = 3,              #18:30 ~ 24:00
                     NIGHT = 4,                #24:00 ~ 8:30
                     LABORATORY_MORNING = 1,
                     LABORATORY_AFTERNOON = 2,
                     COMMAND_ROOM_WORK = 4,
                     EXTRA = 1)

Condition = enum('NORMAL', 'HOLIDAY', 'CONFINEMENT', 'COMBAT', 'FIVE_WAIT_TEAM', 'HOPITALIZATION', 'PRUDENCE')
DinningTime = enum('MORNING', 'LAUNCH', 'EVENING')

class Conditions:
    startDate = datetime.date
    endDate = datetime.date
    condition = Condition.NORMAL

    def __init__(self, sDate, eDate, currentCondition):
        self.startDate = sDate
        self.endDate = eDate
        self.condition = currentCondition


class Soldier:
    code = 0
    name = 'empty'
    rank = SoldierRank.JUNIOR
    grade = SoldierGrade.SECOND
    assignmentCode = AssignmentCode.NONE
    conditions = Conditions
    todayWork = 0
    totalWork = 0
    #monthWork
    #holiday
    #denningTime

    def __init__(self, rank, grade, assign, condition, todayWork, totalWork):
        self.rank = rank
        self.grade = grade
        self.assignmentCode = assign
        self.conditions = condition
        self.todayWork = todayWork
        self.totalWork = totalWork

