# -*- encoding=utf8 -*-
__author__ = "RicharKW"

from airtest.core.api import *
import random
import sys
import pickle
import datetime

auto_setup(__file__)


# -*-------- Grid Info -------------*-
num2use0   = 2
ClickM     = (220, 960) #(200, 1068) #(445, 1200)
ClickTimes = 0

#adClose2   = (843, 42)
#adClose1   = (830, 90)
adClose    = (840, 65)
adClose    = (847, 35) #(830-851; 34-63)

firstP = (85, 350)
hv_step = 120 # hang
CellN = 7 * 9
thoHold = CellN - 14
cactusXY = (85+1*hv_step, 350)

global thisRunAd  # Mark The stone ads
global thisRunEd  # Mark The energy ads
global timeOut    # Mark The output times

pkl_file = open('Params.pkl', 'rb')
startime_stone = pickle.load(pkl_file)   # For the stone ads
startime_energ = startime_stone          # For the stone ads
thisRunAd = pickle.load(pkl_file)
thisRunEd = pickle.load(pkl_file)
try: 
    timeOut = pickle.load(pkl_file)
except:
    print("No timeOut.")
    timeOut = startime_stone
else:
    print("timeOut Exists.")
    
pkl_file.close()

#thisRunAd = 0
#thisRunEd = 0


# -*-------- Functions -------------*-
def saveParam():
    global thisRunAd  # Mark The stone ads
    global thisRunEd  # Mark The energy ads
    global timeOut    # Mark The output times
    # Pickle dictionary using protocol 0.
    # [time, Ad, Ed]
    output = open('Params.pkl', 'wb')
    pickle.dump(datetime.datetime.now(), output) # Pickle the list using the highest protocol available.
    pickle.dump(thisRunAd, output)
    pickle.dump(thisRunEd, output)
    pickle.dump(timeOut, output)
    output.close()
    

def existQ(v, threS=None):
    try:
        pos = loop_find(v, threshold=threS, timeout=0.1, interval=0.1)
    except TargetNotFoundError:
        return False
    else:
        return pos
    
    
def forExisits(v, times=7, threS=None):
    for i in range(1, times+1):
        if threS:
            pos = existQ(v, threS)
        else:
            pos = exists(v)
        if pos:
            break
        sleep(0.78)
    return pos


def ExTouch(v, threS=None):
    try:
        if threS:
            pos = existQ(v, threS)
        else:
            pos = exists(v)
        if pos:
            touch(pos)
        return pos
    except:
        print("Fun ExTouch is error!")
        return False
    else:
        print("Extouch Fin.")

    
def randPoint(xy, scleP=7): 
    """
    Find a random point within the target 
    
    :input xy: should must be a [tuple/list] type with [four] coordinates
    :return: the random point within the pic range.

    """
    try:
        if not(isinstance(xy, tuple)):
            xy = existQ(xy)
        pos = (random.randint(xy[0][0]+scleP, xy[2][0]-scleP), random.randint(xy[0][1]+scleP, xy[2][1]-scleP))
    except TypeError:
        print("The type of the input is not correct!")
    else:
        return pos

    
def findAll(v, threshold = 0.9):
    xy = []
    try:
        if existQ(v):
            xyall = find_all(v)
            for i in xyall:
                if i['confidence'] >= threshold:
                    #xy.append(i['result'])
                    xy.append(randPoint(i['rectangle']))
    except TypeError:
        print("TypeError")
    else:
        print("FindALl Success")
    return xy


def xClouse(slTime=2):
    ExTouch(Template(r"Quit.png"), 0.91)
    sleep(slTime)
    
    
def whileTouch(startFig, endFig, threshold = 0.9, randrange = 4, intervalT = 2):
    try:
        xy = existQ(startFig, threshold)
        touch(xy)
        sleep(0.5)
        while 1:
            if existQ(endFig, threshold):
                break
            else:
                touch(xy)
                sleep(intervalT)
    except TypeError:
        print("TypeError")
    else:
        print("FindALl Success")
    

def isinterval():
    stetime = datetime.datetime.now()
    sleep(1)
    while (datetime.datetime.now() - stetime).seconds < 90:
        sleep(2.5)
        xClouse(1)
        xy = exists(Template(r"tpl1665818065176.png", record_pos=(-0.318, -0.831), resolution=(900, 1600)))
        if xy:
            break

def ReBackDay():  
    if ExTouch(Template(r"SessionButten.png", record_pos=(-0.408, 0.408), resolution=(900, 1600)), 0.9):
        isinterval()
    sleep(1.5)
    

def ReBack():
    xy = existQ(Template(r"Cake.png"), 0.91)
    if xy:
        print("In host!")
    else:
        ReBackDay()
        xy = exists(Template(r"tpl1690297089682.png", record_pos=(0.357, -0.136), resolution=(1600, 900)))
        if xy:
            double_click(xy)
            sleep(10)
            
        '''
        if exists(Template(r"WeiChat.png")):
            swipe((463, 151), (399, 1322), duration = 0.7, steps = 2)
            sleep(2)
            xy = exists(Template(r"TEntry.png"))
            # Template(r"tpl1675229297903.png", record_pos=(-0.408, -0.68), resolution=(900, 1600))
            
            if xy:
                touch(xy)
                isinterval()
                sleep(2)
            ReBackDay()
       ''' 
        xy = existQ(Template(r"Cake.png"), 0.91)
        
        if not(xy):
            temp1 = existQ(Template(r"tpl1682395042057.png", record_pos=(-0.004, 0.166), resolution=(900, 1600)), 0.9)
            temp2 = existQ(Template(r"QueDing.png", record_pos=(0.001, 0.167), resolution=(900, 1600)), 0.9)
            if temp1:
                double_click(temp1)
                sleep(1)
                isinterval()

            elif temp2:
                double_click(temp2)     
                sleep(1)
                isinterval()
            
        xy = existQ(Template(r"Cake.png"), 0.91)
        if not(xy):
            ExTouch(Template(r"BackToMain.png", record_pos=(-0.421, 0.773), resolution=(900, 1600)), 0.9)
            isinterval()
            ReBackDay()
        

    
def SellThenReturn(xyP, times=1):
    try:
        for i in range(0, 4):
            click(xyP)
            sleep(0.2)
            if existQ(Template(r"SellButten.png", record_pos=(0.272, 0.734), resolution=(900, 1600)), 0.91):
                break
        sleep(0.2)
        for i in range(0, times):
            sleep(0.5)
            ExTouch(Template(r"SellButten.png", record_pos=(0.272, 0.734), resolution=(900, 1600)), 0.91)
            sleep(0.5)
            ExTouch(Template(r"ReBack.png", record_pos=(0.272, 0.769), resolution=(900, 1600)), 0.91)
    except:
        print("Sell Wrong! See ref.line 84")
    else:
        print("SellThenReturn success!!")


def adGo():
    xy = forExisits(Template(r"Watch.png"))
    if xy: 
        click(xy)
        sleep(34)
        #ExTouch(Template(r"tpl1671847517109.png", record_pos=(0.454, -0.854), resolution=(900, 1600)), 0.81)
        #click(adClose1)
        #sleep(1.5)
        if ExTouch(Template(r"tpl1691545477745.png", record_pos=(0.463, -0.853), resolution=(900, 1600)), 0.75):
            sleep(2.5)
            click((869, 32))
        else:
            click(adClose)
            sleep(3)
            click(adClose)
        while 1:
              
            
            if existQ(Template(r"tpl1688391212929.png", record_pos=(-0.007, -0.746), resolution=(900, 1600)), 0.9):
                break
            elif existQ(Template(r"tpl1665818065176.png", record_pos=(-0.318, -0.831), resolution=(900, 1600)), 0.9):
                break
            elif existQ(Template(r"Quit.png"), 0.91):
                break
            else:
                click(adClose)
                sleep(2.5)
        sleep(3)
        return True
    else:
        return False

        
def adGo2():
    xy = forExisits(Template(r"Watch.png"))
    if xy:
        click(xy)
        sleep(37.5)
        click(adClose)
        sleep(2.5)
        while 1:
            if existQ(Template(r"isAdFin.png"), 0.92):
                touch(Template(r"goOn.png"))
                sleep(5)
                click(adClose)
                sleep(2.5)
            if existQ(Template(r"tpl1688391149591.png", record_pos=(-0.004, -0.743), resolution=(900, 1600)), 0.9):
                break
            elif existQ(Template(r"tpl1665818065176.png", record_pos=(-0.318, -0.831), resolution=(900, 1600)), 0.9):
                break
            elif existQ(Template(r"Quit.png"), 0.91):
                break
            else:
                click(adClose)
                sleep(2.5)
        sleep(3)
        return True
    else:
        return False

    
    

def WatchAd():
    global startime_energ
    sleep(2)
    if existQ(Template(r"tpl1686196248401.png", record_pos=(0.0, -0.606), resolution=(900, 1600)), 0.80):
        touch((781, 247))
        sleep(1)
    try:
        xy = forExisits(Template(r"EnerP1.png"))
        if xy:
            touch(xy)
            sleep(3) 
            
            for i in range(0, 4):
                #xy = existQ(Template(r"tpl1682225939161.png", record_pos=(0.146, -0.066), resolution=(900, 1600)), 0.91)
                xy = existQ(Template(r"tpl1690298153755.png", record_pos=(0.157, 0.034), resolution=(900, 1600)), 0.91)
                if xy:
                    touch(xy)
                    sleep(2)
                    adGo()
                    break
                else:
                    swipe((314, 383), (305, 1247), duration = 0.7, steps = 4)
                    sleep(3)
        
        xClouse(1)
        xClouse(1)
        ReBack()
        startime_energ = datetime.datetime.now()

    except:
        print("Ad watching is wrong!!")
    else:
        print("Ad watching Successed!!")
        
        
def WatchStone():
    global thisRunAd
    whileTouch(Template(r"tpl1665818065176.png"), Template(r"EnerP1.png"), 0.86, 4, 1)
    whileTouch(Template(r"EnerP1.png"), Template(r"tpl1688116874698.png", record_pos=(0.003, -0.744), resolution=(900, 1600)),  0.86, 4, 1)
     
    for i in range(0, 2):
        #xy = existQ(Template(r"Roll.png"), 0.9)
        xy = existQ(Template(r"tpl1690298034558.png", record_pos=(0.157, -0.339), resolution=(900, 1600)), 0.9)
        if xy:
            touch(xy)
            sleep(1)
            if adGo():
                sleep(1)
                xy = forExisits(Template(r"HaoDe.png"), 4)
                if xy:
                    touch(xy)
                    sleep(2)
                    break
            else:
                print("No stone ads")
                break
        else:
            click((620, 240))
            swipe((314, 383), (305, 1247), duration = 0.7, steps = 4)
            sleep(4)
    
    
    for i in range(0, 10):
        xy = existQ(Template(r"tpl1688391212929.png", record_pos=(-0.007, -0.746), resolution=(900, 1600)), 0.9)
        if xy:
            break
        else:
            whileTouch(Template(r"tpl1665818065176.png"), Template(r"EnerP1.png"), 0.86, 4, 1)
            whileTouch(Template(r"EnerP1.png"), Template(r"tpl1688116874698.png", record_pos=(0.003, -0.744), resolution=(900, 1600)),  0.86, 4, 1)
            sleep(1)
            double_click((614, 240))

    for i in range(0, 4):
        #xy = existQ(Template(r"tpl1682225971414.png", record_pos=(0.147, -0.268), resolution=(900, 1600)), 0.91)
        xy = existQ(Template(r"tpl1690298101357.png", record_pos=(0.149, 0.38), resolution=(900, 1600)), 0.91)
        if xy:
            touch(xy)
            sleep(1)
            if adGo():
                print("RunSuccess")
                thisRunAd += 1
                break
            else:
                thisRunAd = 10
        else:
            click((620, 240))
            swipe((305, 1247), (314, 383), duration = 0.7, steps = 4)
            sleep(4)            
        
    xClouse(1)

    ReBackDay()
    #except:
        #print("Stones_Ad watching is wrong!!")
        #thisRunAd = 10
    #else:
        #print("Stones_Ad watching Successed!!")    
        
        
def WatchStone2():
    global thisRunAd
    

    ExTouch(Template(r"BackToMain.png", record_pos=(-0.421, 0.773), resolution=(900, 1600)), 0.9)
    sleep(1.2)
    
    for i in range(0, 20):
        xy = exists(Template(r"GiftsEn.png", record_pos=(-0.416, -0.456), resolution=(900, 1600)))
        if xy:
            touch(xy)
            sleep(2)
            break
        else:
            ExTouch(Template(r"BackToMain.png", record_pos=(-0.421, 0.773), resolution=(900, 1600)), 0.9)
            sleep(1)
            
    for i in range(0, 20):
        xy = existQ(Template(r"tpl1688116874698.png", record_pos=(0.003, -0.744), resolution=(900, 1600)), 0.9)
        if xy:
            touch((620, 240))
            sleep(0.2)
            touch((620, 240))
            break
        else:
            ExTouch(Template(r"GiftsEn.png", record_pos=(-0.416, -0.456), resolution=(900, 1600)))
            sleep(1)
    sleep(2)        
    for i in range(0, 4):
        #xy = existQ(Template(r"Roll.png"), 0.9)
        xy = existQ(Template(r"tpl1690298034558.png", record_pos=(0.157, -0.339), resolution=(900, 1600)), 0.9)
        if xy:
            touch(xy)
            sleep(1)
            if adGo():
                sleep(1)
                xy = forExisits(Template(r"HaoDe.png"), 10)
                if xy:
                    touch(xy)
                    sleep(2)
                    break
            else:
                print("No stone ads")
        else:
            click((620, 240))
            swipe((314, 383), (305, 1247), duration = 0.7, steps = 4)
            sleep(4)
    
    
    for i in range(0, 20):
        xy = existQ(Template(r"tpl1688391212929.png", record_pos=(-0.007, -0.746), resolution=(900, 1600)), 0.9)
        if xy:
            break
        else:
            ExTouch(Template(r"GiftsEn.png", record_pos=(-0.416, -0.456), resolution=(900, 1600)))
            sleep(1)
            double_click((614, 240))

    for i in range(0, 4):
        #xy = existQ(Template(r"tpl1682225971414.png", record_pos=(0.147, -0.268), resolution=(900, 1600)), 0.91)
        xy = existQ(Template(r"tpl1690298101357.png", record_pos=(0.149, 0.38), resolution=(900, 1600)), 0.91)
        if xy:
            touch(xy)
            sleep(1)
            if adGo():
                print("RunSuccess")
                thisRunAd += 1
                break
            else:
                thisRunAd = 10
        else:
            click((620, 240))
            swipe((305, 1247), (314, 383), duration = 0.7, steps = 4)
            sleep(4)            
        
    xClouse(1)

    ReBackDay()
    #except:
        #print("Stones_Ad watching is wrong!!")
        #thisRunAd = 10
    #else:
        #print("Stones_Ad watching Successed!!")


def CleanList():
    temp = findAll(Template(r"Coin1.png", resolution=(900, 1600)))
    if len(temp) > 0:
        for i in temp:
            double_click(i)
            
            
    temp = findAll(Template(r"Coin4.png", resolution=(900, 1600)))
    if len(temp) > 0:
        for i in temp:
            double_click(i)
            

def getStars():
    try:
        Point2 = {'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': []} 

        Point2['Lv1'] = findAll(Template(r"Star1.png"), 0.8)   
        Point2['Lv2'] = findAll(Template(r"Star2.png"), 0.8)
        Point2['Lv3'] = findAll(Template(r"Star3.png"), 0.8)
        Point2['Lv4'] = findAll(Template(r"Star4.png"), 0.8)
        Point2['Lv5'] = findAll(Template(r"Star5.png"), 0.8)

        for i in range(1, 4+1):
            while len(Point2['Lv' + str(i)]) > 1:
                temp1 = Point2['Lv' + str(i)].pop()
                temp2 = Point2['Lv' + str(i)].pop()
                click(temp1)
                swipe(temp1, temp2, duration = 0.5, steps = 3)
                Point2['Lv' + str(i+1)].append(temp2)

        for i in Point2['Lv5']:
            double_click(i)
    except:
        print("getStars is wrong!!")
    else:
        print("getStars Successed!!")

        
def getActs():
    try:
        Point2 = {'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': []} 

        Point2['Lv1'] = findAll(Template(r"tpl1695139769237.png", record_pos=(0.266, 0.057), resolution=(900, 1600)), 0.87)   
        Point2['Lv2'] = findAll(Template(r"tpl1695139838150.png", record_pos=(0.403, 0.311), resolution=(900, 1600)), 0.87)
        Point2['Lv3'] = findAll(Template(r"tpl1695139856680.png", record_pos=(0.272, 0.316), resolution=(900, 1600)), 0.77)
        Point2['Lv4'] = findAll(Template(r"tpl1695139886652.png", record_pos=(0.257, 0.313), resolution=(900, 1600)), 0.87)

        for i in range(1, 3+1):
            while len(Point2['Lv' + str(i)]) > 1:
                temp1 = Point2['Lv' + str(i)].pop()
                temp2 = Point2['Lv' + str(i)].pop()
                swipe(temp1, temp2, duration = 0.5, steps = 3)
                Point2['Lv' + str(i+1)].append(temp2)

        for i in Point2['Lv4']:
            double_click(i)
    except:
        print("getStars is wrong!!")
    else:
        print("getStars Successed!!")
        
        
def getNum_foggy():
    try:
        Point2 = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': [], 'Lv8': [], 'Lv9': []} 

        Point2['Lv0'] = findAll(Template(r"M0.png"), 0.91) 
        Point2['Lv1'] = findAll(Template(r"M1.png"), 0.91)   
        Point2['Lv2'] = findAll(Template(r"M2.png"), 0.91)
        Point2['Lv3'] = findAll(Template(r"M3.png"), 0.91)
        Point2['Lv4'] = findAll(Template(r"M4.png"), 0.91)
        Point2['Lv5'] = findAll(Template(r"M5.png"), 0.91)
        Point2['Lv6'] = findAll(Template(r"M6.png"), 0.91)
        Point2['Lv7'] = findAll(Template(r"M7.png"), 0.91)
        Point2['Lv8'] = findAll(Template(r"M8.png"), 0.91)
        return(Point2)
    except:
        print("getNum_foggy is wrong!!")
    else:
        print("getNum_foggy Successed!!")

        
def getNum():
    try:
        Point2 = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': [], 'Lv8': [], 'Lv9': []} 

        Point2['Lv0'] = findAll(Template(r"S0.png"), 0.91)   
        Point2['Lv1'] = findAll(Template(r"S1.png"), 0.91)   
        Point2['Lv2'] = findAll(Template(r"S2.png"), 0.91)
        Point2['Lv3'] = findAll(Template(r"S3.png"), 0.91)
        Point2['Lv4'] = findAll(Template(r"S4.png"), 0.91)
        Point2['Lv5'] = findAll(Template(r"S5.png"), 0.91)
        Point2['Lv6'] = findAll(Template(r"S6.png"), 0.91)
        Point2['Lv7'] = findAll(Template(r"S7.png"), 0.91)
        Point2['Lv8'] = findAll(Template(r"S8.png"), 0.91)
        Point2['Lv9'] = findAll(Template(r"S9.png"), 0.91)
        return(Point2)
    except:
        print("getNum_foggy is wrong!!")
    else:
        print("getNum_foggy Successed!!")

        
def clickZippo(times = 1):
    count = 0
    while count < times:
        double_click(point)
        if exists(Template(r"Quit.png")):
            WatchAd()
        else:
            count += 1
            
def clickCactus(point=cactusXY, times=6):
    count = 1
    while count < times:
        double_click(point)
        if exists(Template(r"Quit.png")):
            WatchAd()
        else:
            count += 1

            
def clickNums(targetNum=0, amounts=1):
    amounts = 2**targetNum * amounts
    click(firstP)
    count = 0
    while count < amounts:
        click(firstP)
        if exists(Template(r"Quit.png")):
            WatchAd()
        else:
            count += 1
            
    Point = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': []}
    Point['Lv0'] = findAll(Template(r"S0.png"))
    amounts = len(Point['Lv0'])
    for i in range(0, targetNum):
        maxT = int(amounts/(2**(i+1)))
        for j in range(0, maxT):
            temp1 = Point['Lv' + str(i)].pop()
            temp2 = Point['Lv' + str(i)].pop()
            click(temp1)
            swipe(temp1, temp2, duration = 0.6, steps = 3)
            sleep(0.1)
            Point['Lv' + str(i+1)].append(temp2)
    return Point['Lv' + str(targetNum)]


def CoinAndEn():
    for i in range(0, 10):
        if ExTouch(Template(r"ShopP.png")):
            break
    sleep(3)
    for i in range(0, 10):
        if exists(Template(r"CoinLM.png")):
            ExTouch(Template(r"FreeButt.png"))
            break
        else:
            if not(ExTouch(Template(r"ShopP.png"))):
                swipe((314, 383), (305, 1247), duration = 0.7, steps = 2)
                sleep(2)
                
    sleep(1)
    ExTouch(Template(r"EnBox1.png"))
    sleep(3.5)
    
    
    for i in range(0, 5):
        xy = forExisits(Template(r"Free.png"), 4)
        if xy:
            touch(xy)
            sleep(2)
            xy = existQ(Template(r"Watch.png"), 0.9)
            if xy:
                adGo()
                sleep(2)
                break

    xClouse(1)
    xClouse(1)
    xClouse(1)

    
    
def hourGift():
    if ExTouch(Template(r"hourGift.png"), 0.9):
        sleep(3)
        ExTouch(Template(r"LingQu.png"), 0.8)
    xClouse(0.2)

    
def getSH1():
    try:
        Point2 = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': [], 'Lv8': [], 'Lv9': []} 

        Point2['Lv0'] = findAll(Template(r"tpl1682408241912.png", record_pos=(0.124, 0.172), resolution=(900, 1600)), 0.91)   
        Point2['Lv1'] = findAll(Template(r"tpl1682408268878.png", record_pos=(0.134, 0.177), resolution=(900, 1600)), 0.91)   
        Point2['Lv2'] = findAll(Template(r"tpl1682408278491.png", record_pos=(-0.001, 0.312), resolution=(900, 1600)), 0.91)
        Point2['Lv3'] = findAll(Template(r"tpl1682408290577.png", record_pos=(0.128, 0.176), resolution=(900, 1600)), 0.92)
        Point2['Lv4'] = findAll(Template(r"tpl1682505202298.png", record_pos=(-0.132, 0.318), resolution=(900, 1600)), 0.92)
        return(Point2)
    except:
        print("getSH1 is wrong!!")
    else:
        print("getSH1 Successed!!")

        
def getSH2():
    try:
        Point2 = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': [], 'Lv8': [], 'Lv9': []} 

        Point2['Lv0'] = findAll(Template(r"tpl1682408123048.png", record_pos=(-0.266, 0.312), resolution=(900, 1600)), 0.91)
        Point2['Lv1'] = findAll(Template(r"tpl1682408140424.png", record_pos=(-0.269, 0.311), resolution=(900, 1600)), 0.91)   
        Point2['Lv2'] = findAll(Template(r"tpl1682408172927.png", record_pos=(-0.273, 0.311), resolution=(900, 1600)), 0.91)
        return(Point2)
    except:
        print("getSH2 is wrong!!")
    else:
        print("getSH2 Successed!!")
        
def getSH3():
    try:
        Point2 = {'Lv0': [], 'Lv1': [], 'Lv2': [], 'Lv3': [], 'Lv4': [], 'Lv5': [], 'Lv6': [], 'Lv7': [], 'Lv8': [], 'Lv9': []} 

        Point2['Lv0'] = findAll(Template(r"tpl1682507590772.png", record_pos=(0.271, 0.309), resolution=(900, 1600)), 0.91)   
        Point2['Lv1'] = findAll(Template(r"tpl1682507605891.png", record_pos=(0.129, 0.173), resolution=(900, 1600)), 0.91)   
        Point2['Lv2'] = findAll(Template(r"tpl1682507620653.png", record_pos=(0.13, 0.458), resolution=(900, 1600)), 0.91)
        Point2['Lv3'] = findAll(Template(r"tpl1682507637798.png", record_pos=(-0.01, 0.311), resolution=(900, 1600)), 0.91)
        Point2['Lv4'] = findAll(Template(r"tpl1682507654353.png", record_pos=(0.127, 0.448), resolution=(900, 1600)), 0.91)
        Point2['Lv5'] = findAll(Template(r"tpl1682507668867.png", record_pos=(0.132, 0.464), resolution=(900, 1600)), 0.91)
        Point2['Lv6'] = findAll(Template(r"tpl1682507705577.png", record_pos=(0.134, 0.438), resolution=(900, 1600)), 0.91)
        #Point2['Lv7'] = findAll(Template(r"S7.png"), 0.91)
        #Point2['Lv8'] = findAll(Template(r"S8.png"), 0.91)
        #Point2['Lv9'] = findAll(Template(r"S9.png"), 0.91)
        return(Point2)
    except:
        print("getSH3 is wrong!!")
    else:
        print("getSH3 Successed!!")
        
        
def someHelp(xyP=(445, 1200), times=1):
    global thisRunEd
    try:
        temp = existQ(Template(r"BackToMain.png", record_pos=(-0.421, 0.773), resolution=(900, 1600)))
        if temp:
            click(temp)
            sleep(1.2)
        isinterval()
        for i in range(0, 5):
            hourGift()
            xy = exists(Template(r"tpl1666183280723.png", record_pos=(-0.376, 0.688), resolution=(900, 1600)))
            if xy:
                sleep(2)
                click(xy)
                break
        sleep(2)
        isinterval()
        sleep(2)
        SellThenReturn(xyP, times)
        sleep(1)
        if thisRunEd < 1:
            CoinAndEn()
            thisRunEd += 1
            saveParam()

        click(temp)
        sleep(1.2)
        isinterval()
        hourGift()
        xy = existQ(Template(r"SessionButten.png", record_pos=(-0.408, 0.408), resolution=(900, 1600)))
        if xy:
            touch(xy)
        isinterval()
    except:
        print("Click wronging, see ref.line 525")
        ReBack()
    else:
        print("someHelp success!")

        
def someHelp2(xyP=(109, 836)):
    global thisRunEd
    global timeOut    # Mark The output times
    try:
        tempout = existQ(Template(r"BackToMain.png", record_pos=(-0.421, 0.773), resolution=(900, 1600)))
        if tempout:
            click(tempout)
            sleep(1.2)
        isinterval()
        for i in range(0, 5):
            hourGift()
            xy = exists(Template(r"tpl1666183280723.png", record_pos=(-0.376, 0.688), resolution=(900, 1600)))
            if xy:
                sleep(2)
                click(xy)
                break
        sleep(2)
        isinterval()
        sleep(2)
        
        Num1 = getSH1()
        if len(Num1['Lv' + str(4)]) < 2:
            for i in range(0, 5):
                while len(Num1['Lv' + str(i)]) > 1:
                    temp1 = Num1['Lv' + str(i)].pop()
                    temp2 = Num1['Lv' + str(i)].pop()
                    # click(temp1)
                    swipe(temp1, temp2, duration = 0.5, steps = 3)
                    sleep(0.1)
                
        Num2 = getSH2()
        if len(Num2['Lv' + str(2)]) < 2:
            for i in range(0, 3):
                while len(Num2['Lv' + str(i)]) > 1:
                    temp1 = Num2['Lv' + str(i)].pop()
                    temp2 = Num2['Lv' + str(i)].pop()
                    # click(temp1)
                    swipe(temp1, temp2, duration = 0.5, steps = 3)
                    sleep(0.1)
        
        # for the inputs:
        click(xyP)
        temp = existQ(Template(r"JiaSu.png", record_pos=(0.9467, 0.9269), resolution=(900, 1600)), 0.9)
        if temp:
            print("ON CD!")
        else:
            temp = existQ(Template(r"tpl1682505104648.png", record_pos=(0.127, 0.771), resolution=(900, 1600)), 0.9)
            if temp:
                temp = Num1['Lv' + str(4)].pop
                swipe(temp, xyP, duration = 0.5, steps = 3)
                sleep(0.2)
                temp = Num1['Lv' + str(4)].pop
                swipe(temp, xyP, duration = 0.5, steps = 3)
                sleep(0.2)
                temp = Num2['Lv' + str(2)].pop
                swipe(temp, xyP, duration = 0.5, steps = 3)
                sleep(0.2)
                timeOut = datetime.datetime.now()
            else:
                clickCactus(xyP, 6)
                Num1 = getSH3()
                for i in range(0, 7):
                    while len(Num1['Lv' + str(i)]) > 1:
                        temp1 = Num1['Lv' + str(i)].pop()
                        temp2 = Num1['Lv' + str(i)].pop()
                        #click(temp1)
                        swipe(temp1, temp2, duration = 0.5, steps = 3)
                        sleep(0.1)
                
        sleep(1)
        if thisRunEd < 1:
            CoinAndEn()
            thisRunEd += 1
            
        saveParam()
        click(tempout)
        sleep(1.2)
        isinterval()
        hourGift()
        xy = existQ(Template(r"SessionButten.png", record_pos=(-0.408, 0.408), resolution=(900, 1600)))
        if xy:
            touch(xy)
        isinterval()
    except:
        print("Click wronging, see ref.line 525")
        ReBack()
    else:
        print("someHelp success!")
        
            
    # -*----------------- Main -----------------------*-
while 1:

    try:
        ReBack()


        click(cactusXY)
        sleep(0.5)

        temp = existQ(Template(r"JiaSu.png", record_pos=(0.9467, 0.9269), resolution=(900, 1600)), 0.9)
        print(temp)
        if temp:
            sleep(10)
        else:
            clickCactus()
            sleep(1)
            # =========== main part
            Num_f = getNum_foggy()
            Num   = getNum()    
            usedN = 0

            diffN = len(Num_f['Lv0']) - len(Num['Lv0'])
            if diffN > 0:
                temp = clickNums(0, diffN)
                for i in temp:
                    Num['Lv0'].append(i)
                print(Num['Lv0'])

            for i in range(0, 8+1):
                if i < num2use0+1:
                    diffN = len(Num_f['Lv' + str(i)]) - len(Num['Lv' + str(i)])
                    if diffN > 0:
                        temp = clickNums(i, diffN)    
                        for item in temp:
                            Num['Lv' + str(i)].append(item)
                while len(Num['Lv' + str(i)]) > 0:
                    if len(Num_f['Lv' + str(i)]) < 1:
                        while len(Num['Lv' + str(i)]) > i+2:
                            temp1 = Num['Lv' + str(i)].pop()
                            temp2 = Num['Lv' + str(i)].pop()
                            # click(temp1)
                            swipe(temp1, temp2, duration = 0.5, steps = 3)
                            sleep(0.1)
                            Num['Lv' + str(i+1)].append(temp2)
                        break
                    tempN = Num['Lv' + str(i)].pop()
                    tempF = Num_f['Lv' + str(i)].pop()
                    # click(tempN)
                    swipe(tempN, tempF, duration = 0.5, steps = 3)
                    sleep(0.1)
                    Num['Lv' + str(i+1)].append(tempF)



                usedN += len(Num['Lv' + str(i)])
                usedN += len(Num_f['Lv' + str(i)])

            for i in Num['Lv9']:
                click(i)
                click(Template(r"SellButten.png", record_pos=(0.272, 0.734), resolution=(900, 1600)))

            if usedN > thoHold:
                count = 0
                for i in range(0, 8+1):
                    while len(Num['Lv' + str(i)]) > 1:
                        temp1 = Num['Lv' + str(i)].pop()
                        temp2 = Num['Lv' + str(i)].pop()
                        # click(temp1)
                        swipe(temp1, temp2, duration = 0.5, steps = 3)
                        sleep(0.1)
                        count += 1
                        if count > 5:
                            break
                    if count > 5:
                        break
            sleep(4)
            getStars()
            getActs()
            CleanList()

            if thisRunAd < 6:
                sleep(3*60)
            else:
                sleep(12*60)

            # =========== main part end

        print("Main Run Fin......")
        if ClickTimes > 0:
            someHelp(ClickM, ClickTimes)
        elif thisRunEd < 1:
            someHelp(ClickM, ClickTimes)


        if thisRunAd < 6:
            endtime = datetime.datetime.now()                     
            if (endtime - startime_stone).seconds >= 120:
                WatchStone()
                startime_stone = datetime.datetime.now()
                saveParam()
                sleep(2*60)

        endtime = datetime.datetime.now()    
        if endtime.day != startime_stone.day:
            thisRunAd = 0
            thisRunEd = 0
            saveParam()
        '''    
        if (endtime - timeOut).seconds >= 4*60*60:
            someHelp2()
        '''    
        if endtime.hour > 22:
            if (endtime - startime_energ).seconds >= 120:
                touch(Template(r"tpl1665818065176.png", record_pos=(-0.318, -0.831), resolution=(900, 1600)))
                WatchAd()
                startime_energ = datetime.datetime.now()
                saveParam()
        #if endtime.hour == 6:     
            #break
        
    except:
        print("Main wronging, see ref.line 881")
        ReBack()
    else:
        print("main success!")      



        
        
        
        
        
# All the test:
'''
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
poco("肥鹅健身房").click()
poco(text="奖励将于 24 秒后发放").click()
poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.webkit.WebView").child("android.webkit.WebView").offspring("main").child("android.view.View").offspring("video-safe").child("android.view.View")[0].child("android.view.View").click()
poco("wnWebFivePoints").click()
poco(text="恭喜获得奖励").click()
poco(text="ams_icon_video_sigle_logo").click()
poco("android.widget.ImageView").click()


poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.webkit.WebView").child("android.webkit.WebView").offspring("main").child("android.view.View").child("android.view.View").child("android.view.View")[1].child("android.view.View").child("android.view.View")[2].click()
poco("android.widget.ImageView").click()
poco("android.widget.ImageView").click()
poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.webkit.WebView").child("android.webkit.WebView").offspring("main").child("android.view.View").offspring("video-safe").child("android.view.View")[0].child("android.view.View").child("android.view.View")[2].click()
poco("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.webkit.WebView").child("android.webkit.WebView").offspring("main").child("android.view.View").offspring("video-safe").child("android.view.View")[0].child("android.view.View").child("android.view.View")[2].click()
poco(text="此图片未加标签。打开右上角的“更多选项”菜单即可获取图片说明。").click()
poco("android.widget.ImageView").click()
'''
