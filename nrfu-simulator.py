import random
import math
from collections import defaultdict
from tkinter import *
import time

root = Tk()

canvas = Canvas(root,width = 500, height = 500)
canvas.pack(expand = YES)

from PIL import Image, ImageTk

homeImage = ImageTk.PhotoImage(Image.open("home-icon.png"))
blueDot = ImageTk.PhotoImage(Image.open("blue_dot.gif"))

ASSIGNMENT_SIZE=30

class Dwelling() :
    def __init__(self,coords) :
        self.coords=coords
        self.attempts=0
        self.resolved=False
        
    def __str__(self):
        return "Dwelling at X:" + str(self.coords[0]) + " Y:" + str(self.coords[1]) + " with " + str(self.attempts) + " attempt(s)"
        
    def __repr__(self):
        return "Dwelling(("+str(self.coords[0])+","+str(self.coords[1])+"))"
        
    def __hash__(self):
        return 13*self.coords[0]+29*self.coords[1]
    
    def __eq__(self, other):
        return self.coords[0]==other.coords[0] and self.coords[1]==other.coords[1]

class RandomgNRFUTest() :
    def __init__(self,dwellings) :
        self.universe=dwellings
        self.outstanding=list(dwellings)
        self.resolved=set()
        self.assigned=set()
        self.initCoords=(100,100)
        
    def playOneStep(self) :
        canvas.delete(ALL)
        turnOutstanding=list(self.assigned)
        currentCoords=self.initCoords
        turnDistance=0
        canvas.create_image(self.initCoords[0], self.initCoords[1], image = homeImage)
        # Visit all the dwellings
        while(len(turnOutstanding)>0) :
            (nextDwelling, distance) = RandomgNRFUTest.findNextClosest(currentCoords,turnOutstanding)
            #DEBUG : print("Next closest is : " + str(nextDwelling))
            canvas.create_line(currentCoords[0], currentCoords[1], nextDwelling.coords[0], nextDwelling.coords[1])
            canvas.create_image(nextDwelling.coords[0], nextDwelling.coords[1], image = blueDot)
            turnOutstanding.remove(nextDwelling)
            currentCoords=nextDwelling.coords
            turnDistance+=distance
            draw = random.random()
            nextDwelling.attempts=nextDwelling.attempts+1
            if ((nextDwelling.attempts<3 and draw<0.3) or draw<0.25) :
                nextDwelling.resolved=True
                self.outstanding.remove(nextDwelling)
                self.resolved.add(nextDwelling)
                self.assigned.remove(nextDwelling)
        root.update_idletasks()
        time.sleep(2)
        # Complete assignment
        self.completeAssignment()
        return turnDistance
        
    def play(self) :
        self.completeAssignment()
        totalDistance = 0
        for i in range(1,21) :
            print("Playing turn : " + str(i))
            distance=self.playOneStep()
            print("Turn played with {0:.2f} distance".format(distance))
            totalDistance+=distance
        print("Finished the 20 turns with a total distance of {0:.2f}".format(totalDistance))
        self.printFinalDistribution()
        root.quit()
        
    def completeAssignment(self) :
        while len(self.assigned)<ASSIGNMENT_SIZE and len(self.outstanding)>len(self.assigned) :
            self.assigned.add(random.sample(self.outstanding,1)[0])
            
    def printFinalDistribution(self) :
        print("Resolution : {0} out of {1}".format(len(self.resolved),len(self.universe)))
        print("Attempt distribution :")
        tally = defaultdict(int)
        c = RandomgNRFUTest.tallyAccumulator(tally)
        c.send(None)
        for aDwelling in self.universe :
            c.send(aDwelling)
        for key in sorted(tally.keys()):
            print("{0} attempt(s): {1}".format(key,tally.get(key)))
    
    @staticmethod    
    def tallyAccumulator(t):
        try:
            while True:
                k = (yield)
                t[k.attempts] += 1
        except GeneratorExit:
            pass
    
    @staticmethod    
    def findNextClosest(currentCoords,remainingDwellings) :
        minDistance = 1000000
        currentClosest = None
        for aDwelling in remainingDwellings :
            dist = RandomgNRFUTest.calcDistance(currentCoords,aDwelling.coords)
            if dist<minDistance :
                minDistance=dist
                currentClosest=aDwelling
        return (currentClosest,minDistance)
            
    @staticmethod
    def calcDistance(coords1,coords2) :
        return math.sqrt((coords2[0]-coords1[0])**2+(coords2[1]-coords1[1])**2)
        
        
def createDwellings(number) :
    dwellings=set()
    for i in range(number+1) :
        dwellings.add(Dwelling((random.randrange(0,500),random.randrange(0,500))))
    
    print(dwellings)
    
standardDwellings = [Dwelling((104,24)), Dwelling((408,29)), Dwelling((329,347)), Dwelling((154,355)), Dwelling((320,210)), Dwelling((33,480)), Dwelling((107,470)), Dwelling((405,243)), Dwelling((82,34)), Dwelling((496,273)), Dwelling((454,292)), Dwelling((433,19)), Dwelling((299,291)), Dwelling((177,427)), Dwelling((480,210)), Dwelling((145,431)), Dwelling((21,416)), Dwelling((311,498)), Dwelling((135,224)), Dwelling((163,351)), Dwelling((414,311)), Dwelling((40,55)), Dwelling((77,321)), Dwelling((238,249)), Dwelling((463,219)), Dwelling((125,300)), Dwelling((64,45)), Dwelling((491,348)), Dwelling((62,258)), Dwelling((440,18)), Dwelling((67,304)), Dwelling((32,413)), Dwelling((460,80)), Dwelling((442,300)), Dwelling((287,299)), Dwelling((475,3)), Dwelling((81,188)), Dwelling((404,388)), Dwelling((400,178)), Dwelling((481,495)), Dwelling((178,66)), Dwelling((315,381)), Dwelling((52,476)), Dwelling((70,468)), Dwelling((311,360)), Dwelling((24,277)), Dwelling((107,28)), Dwelling((416,172)), Dwelling((495,278)), Dwelling((441,161)), Dwelling((120,305)), Dwelling((458,436)), Dwelling((253,123)), Dwelling((253,34)), Dwelling((151,221)), Dwelling((236,254)), Dwelling((494,421)), Dwelling((270,451)), Dwelling((288,390)), Dwelling((396,183)), Dwelling((319,147)), Dwelling((465,11)), Dwelling((234,120)), Dwelling((55,266)), Dwelling((336,352)), Dwelling((142,439)), Dwelling((378,404)), Dwelling((497,492)), Dwelling((334,212)), Dwelling((454,17)), Dwelling((386,330)), Dwelling((396,255)), Dwelling((416,458)), Dwelling((316,107)), Dwelling((281,448)), Dwelling((78,45)), Dwelling((63,405)), Dwelling((365,411)), Dwelling((92,251)), Dwelling((463,438)), Dwelling((426,31)), Dwelling((231,401)), Dwelling((42,486)), Dwelling((327,147)), Dwelling((295,232)), Dwelling((446,259)), Dwelling((104,318)), Dwelling((434,241)), Dwelling((378,478)), Dwelling((218,338)), Dwelling((375,34)), Dwelling((114,255)), Dwelling((320,10)), Dwelling((335,74)), Dwelling((70,6)), Dwelling((145,140)), Dwelling((93,443)), Dwelling((260,320)), Dwelling((15,218)), Dwelling((65,337)), Dwelling((456,303)), Dwelling((354,490)), Dwelling((106,107)), Dwelling((235,473)), Dwelling((251,254)), Dwelling((228,465)), Dwelling((42,136)), Dwelling((36,280)), Dwelling((393,332)), Dwelling((370,484)), Dwelling((395,120)), Dwelling((445,27)), Dwelling((346,1)), Dwelling((441,358)), Dwelling((299,446)), Dwelling((225,338)), Dwelling((241,119)), Dwelling((479,83)), Dwelling((109,249)), Dwelling((288,381)), Dwelling((228,55)), Dwelling((411,185)), Dwelling((86,49)), Dwelling((70,480)), Dwelling((107,477)), Dwelling((285,172)), Dwelling((237,335)), Dwelling((217,344)), Dwelling((363,158)), Dwelling((52,65)), Dwelling((424,322)), Dwelling((155,443)), Dwelling((117,492)), Dwelling((25,219)), Dwelling((415,382)), Dwelling((62,132)), Dwelling((231,480)), Dwelling((168,14)), Dwelling((369,489)), Dwelling((497,8)), Dwelling((370,251)), Dwelling((117,320)), Dwelling((334,11)), Dwelling((261,397)), Dwelling((449,101)), Dwelling((47,140)), Dwelling((33,217)), Dwelling((37,74)), Dwelling((407,332)), Dwelling((42,72)), Dwelling((74,199)), Dwelling((433,462)), Dwelling((61,417)), Dwelling((127,317)), Dwelling((426,183)), Dwelling((343,291)), Dwelling((167,370)), Dwelling((470,93)), Dwelling((419,469)), Dwelling((476,232)), Dwelling((243,266)), Dwelling((129,176)), Dwelling((471,100)), Dwelling((62,277)), Dwelling((460,240)), Dwelling((309,308)), Dwelling((306,380)), Dwelling((202,3)), Dwelling((453,385)), Dwelling((410,78)), Dwelling((462,240)), Dwelling((311,449)), Dwelling((376,212)), Dwelling((167,443)), Dwelling((172,174)), Dwelling((152,97)), Dwelling((56,352)), Dwelling((390,273)), Dwelling((47,215)), Dwelling((229,275)), Dwelling((441,392)), Dwelling((353,149)), Dwelling((450,438)), Dwelling((65,137)), Dwelling((425,470)), Dwelling((232,306)), Dwelling((164,234)), Dwelling((214,332)), Dwelling((203,217)), Dwelling((361,325)), Dwelling((150,29)), Dwelling((192,434)), Dwelling((414,264)), Dwelling((342,367)), Dwelling((324,22)), Dwelling((474,167)), Dwelling((224,350)), Dwelling((32,295)), Dwelling((219,282)), Dwelling((182,87)), Dwelling((374,37)), Dwelling((248,340)), Dwelling((213,497)), Dwelling((225,280)), Dwelling((78,346)), Dwelling((87,342)), Dwelling((71,279)), Dwelling((84,132)), Dwelling((188,368)), Dwelling((10,236)), Dwelling((169,306)), Dwelling((35,13)), Dwelling((11,377)), Dwelling((275,47)), Dwelling((457,212)), Dwelling((329,447)), Dwelling((427,50)), Dwelling((349,85)), Dwelling((288,183)), Dwelling((78,136)), Dwelling((36,367)), Dwelling((340,19)), Dwelling((41,365)), Dwelling((473,205)), Dwelling((474,30)), Dwelling((344,159)), Dwelling((219,427)), Dwelling((479,28)), Dwelling((308,458)), Dwelling((156,103)), Dwelling((84,65)), Dwelling((219,287)), Dwelling((303,320)), Dwelling((321,312)), Dwelling((273,263)), Dwelling((416,58)), Dwelling((149,319)), Dwelling((76,493)), Dwelling((351,158)), Dwelling((18,378)), Dwelling((188,302)), Dwelling((305,179)), Dwelling((181,164)), Dwelling((142,111)), Dwelling((313,105)), Dwelling((257,342)), Dwelling((72,496)), Dwelling((439,261)), Dwelling((127,401)), Dwelling((234,424)), Dwelling((117,194)), Dwelling((313,36)), Dwelling((36,19)), Dwelling((13,100)), Dwelling((308,321)), Dwelling((86,350)), Dwelling((109,481)), Dwelling((214,63)), Dwelling((309,321)), Dwelling((178,168)), Dwelling((73,427)), Dwelling((196,372)), Dwelling((196,389)), Dwelling((331,453)), Dwelling((446,119)), Dwelling((216,333)), Dwelling((357,371)), Dwelling((270,57)), Dwelling((335,381)), Dwelling((490,453)), Dwelling((73,499)), Dwelling((111,482)), Dwelling((434,196)), Dwelling((224,153)), Dwelling((462,466)), Dwelling((184,379)), Dwelling((97,65)), Dwelling((297,258)), Dwelling((11,484)), Dwelling((39,495)), Dwelling((302,468)), Dwelling((174,455)), Dwelling((366,369)), Dwelling((105,204)), Dwelling((196,22)), Dwelling((330,245)), Dwelling((383,6)), Dwelling((422,416)), Dwelling((146,212)), Dwelling((245,72)), Dwelling((263,64)), Dwelling((46,232)), Dwelling((123,480)), Dwelling((76,360)), Dwelling((469,184)), Dwelling((473,112)), Dwelling((84,300)), Dwelling((108,88)), Dwelling((424,205)), Dwelling((364,232)), Dwelling((277,130)), Dwelling((350,474)), Dwelling((91,356)), Dwelling((315,185)), Dwelling((247,498)), Dwelling((157,256)), Dwelling((91,215)), Dwelling((491,177)), Dwelling((389,364)), Dwelling((427,347)), Dwelling((287,198)), Dwelling((18,223)), Dwelling((451,125)), Dwelling((307,119)), Dwelling((64,440)), Dwelling((157,116)), Dwelling((119,345)), Dwelling((474,186)), Dwelling((199,142)), Dwelling((47,269)), Dwelling((248,217)), Dwelling((450,6)), Dwelling((281,132)), Dwelling((452,126)), Dwelling((311,48)), Dwelling((6,326)), Dwelling((182,459)), Dwelling((217,161)), Dwelling((379,442)), Dwelling((368,165)), Dwelling((317,188)), Dwelling((285,273)), Dwelling((416,285)), Dwelling((343,389)), Dwelling((316,196)), Dwelling((167,115)), Dwelling((305,124)), Dwelling((233,439)), Dwelling((155,474)), Dwelling((164,470)), Dwelling((163,188)), Dwelling((44,171)), Dwelling((100,358)), Dwelling((319,48)), Dwelling((164,400)), Dwelling((346,36)), Dwelling((132,132)), Dwelling((358,172)), Dwelling((441,458)), Dwelling((456,340)), Dwelling((49,240)), Dwelling((450,484)), Dwelling((70,236)), Dwelling((270,424)), Dwelling((271,346)), Dwelling((184,39)), Dwelling((229,372)), Dwelling((317,262)), Dwelling((263,145)), Dwelling((452,133)), Dwelling((488,115)), Dwelling((372,26)), Dwelling((174,319)), Dwelling((168,259)), Dwelling((373,379)), Dwelling((198,175)), Dwelling((117,282)), Dwelling((2,263)), Dwelling((432,141)), Dwelling((459,352)), Dwelling((473,264)), Dwelling((419,359)), Dwelling((212,240)), Dwelling((407,82)), Dwelling((156,124)), Dwelling((355,247)), Dwelling((5,404)), Dwelling((76,231)), Dwelling((435,494)), Dwelling((120,141)), Dwelling((376,450)), Dwelling((85,298)), Dwelling((354,460)), Dwelling((193,391)), Dwelling((293,205)), Dwelling((365,245)), Dwelling((207,123)), Dwelling((34,251)), Dwelling((432,426)), Dwelling((226,236)), Dwelling((344,254)), Dwelling((164,476)), Dwelling((131,279)), Dwelling((10,404)), Dwelling((266,360)), Dwelling((410,13)), Dwelling((470,198)), Dwelling((121,72)), Dwelling((389,305)), Dwelling((24,45)), Dwelling((95,437)), Dwelling((78,21)), Dwelling((143,345)), Dwelling((227,237)), Dwelling((439,354)), Dwelling((445,422)), Dwelling((461,203)), Dwelling((300,487)), Dwelling((325,476)), Dwelling((311,129)), Dwelling((89,17)), Dwelling((271,430)), Dwelling((403,89)), Dwelling((113,265)), Dwelling((153,200)), Dwelling((331,51)), Dwelling((68,169)), Dwelling((355,111)), Dwelling((489,51)), Dwelling((327,265)), Dwelling((474,480)), Dwelling((66,100)), Dwelling((84,92)), Dwelling((276,6)), Dwelling((339,331)), Dwelling((448,141)), Dwelling((189,90)), Dwelling((307,134)), Dwelling((381,454)), Dwelling((169,196)), Dwelling((121,218)), Dwelling((123,429)), Dwelling((460,137)), Dwelling((290,72)), Dwelling((458,138)), Dwelling((380,173)), Dwelling((1,343)), Dwelling((327,56)), Dwelling((426,153)), Dwelling((174,478)), Dwelling((413,230)), Dwelling((439,289)), Dwelling((216,36)), Dwelling((68,68)), Dwelling((307,66)), Dwelling((417,158)), Dwelling((66,386)), Dwelling((7,201)), Dwelling((67,386)), Dwelling((6,484)), Dwelling((273,435)), Dwelling((37,329)), Dwelling((369,39)), Dwelling((405,376)), Dwelling((426,296)), Dwelling((493,478)), Dwelling((310,419)), Dwelling((494,266)), Dwelling((109,368)), Dwelling((80,28)), Dwelling((103,159)), Dwelling((368,111)), Dwelling((370,322)), Dwelling((59,179)), Dwelling((149,139)), Dwelling((460,494)), Dwelling((7,415)), Dwelling((369,394)), Dwelling((318,417)), Dwelling((167,61)), Dwelling((323,203)), Dwelling((391,102)), Dwelling((286,8)), Dwelling((392,243)), Dwelling((255,22)), Dwelling((31,405)), Dwelling((410,94)), Dwelling((168,485)), Dwelling((493,57)), Dwelling((93,346)), Dwelling((247,450)), Dwelling((44,188)), Dwelling((372,253)), Dwelling((413,376)), Dwelling((467,140)), Dwelling((391,386)), Dwelling((464,274)), Dwelling((155,351)), Dwelling((231,388)), Dwelling((98,236)), Dwelling((348,336)), Dwelling((61,253)), Dwelling((477,420)), Dwelling((493,343)), Dwelling((98,167)), Dwelling((237,246)), Dwelling((354,335)), Dwelling((470,107)), Dwelling((497,130)), Dwelling((448,152))]

standardDwellings = set(standardDwellings)

test=RandomgNRFUTest(standardDwellings)

root.after(5,test.play)
root.mainloop()