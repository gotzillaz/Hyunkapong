from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition , SlideTransition , WipeTransition , ShaderTransition, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics import Color,Ellipse,Rectangle
from random import randint
from math import *
from sys import exit


class LokiColorG(Widget):
    pass

class GameColor():
    colorhash = {'Red':Color(1,0,0),'Green':Color(0,1,0),'Blue':Color(0,0,1),'White':Color(1,1,1),'Yellow':Color(1,1,0),'Sblue':Color(0,1,1),'Pink':Color(1,0,0.6),'Gray':Color(0.2,0.2,0.2),'Orange':Color(1,0.5,0),'Cream':Color(1,1,.5),'Purple':Color(0.8,0,1)}
    
    def getColor(self,color):
        return self.colorhash[color]

class GamePlate(Widget):
    color = 'White'
    text = ''
    star = False

    def hasStar(self):
        if self.star:
            self.canvas.add(Color(0,0,0))
            self.canvas.add(Ellipse(size=[10,10],pos=self.pos))

    def changeColor(self, mycolor):
        self.color = mycolor
        self.canvas.clear()
        self.canvas.add(GameColor().getColor(mycolor))
        self.canvas.add(Rectangle(size=self.size,pos=self.pos))

    def __init__(self,color,**kwargs):
        super(GamePlate, self).__init__(**kwargs)
        self.color = color
        self.changeColor(self.color)

class GameMap(GridLayout):
    gridsize = 5
    gridpos = [[]]
    color_table = [[]]
    map_table = [[]]
    
    def readMap(self,map_table,color_table,size):
        self.gridsize = size
        self.map_table = [[x for x in y] for y in map_table]
        self.color_table = [[x for x in y] for y in color_table]

    def updateGridPos(self):
        for x in self.children:
            print x.id
            pr = int(x.id[1])
            pc = int(x.id[2])
            self.gridpos[pr][pc] = (x.center_x,x.center_y)

    def createGridPos(self, num):
        self.gridpos = [[(0,0) for x in xrange(num)] for y in xrange(num)]

    def __init__(self,map_t,color_t,si,**kwargs):
        super(GameMap, self).__init__(**kwargs)
        self.readMap(map_t,color_t,si)
        for x in xrange(self.gridsize):
            for y in xrange(self.gridsize):
                self.add_widget(GamePlate(id='m'+str(x)+str(y),size=[100,100],text=str(x)+' '+str(y),color=self.color_table[x][y]))
                #self.add_widget(Button(id='m'+str(x)+str(y),size=[100,100],text=str(x)+' '+str(y)))
        for x in self.children:
            print x.pos,x.parent.pos,x.text,x.center_x,x.center_y
        print self.pos,self.center_x,self.center_y
        self.createGridPos(self.gridsize)
        self.updateGridPos()
        print self.gridpos
    
class GameBall(Widget):
    ballgrid = [0,0]
    oldgrid = [0,0]
    endgrid = [1,1]
    ball_color = 'White'
    #self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius
    def smoothBall(self,tt):
        if self.ballgrid != self.oldgrid:
            dx = self.ballgrid[0] - self.oldgrid[0]
            dy = self.ballgrid[1] - self.oldgrid[1]
            if dx!=0:
                dx/=abs(dx)
            if dy!=0:
                dy/=abs(dy)
            self.pos[0]+=dy*5.0
            self.pos[1]-=dx*5.0
            self.changeColor()
            nextpos = self.parent.gamemap.gridpos[self.ballgrid[0]][self.ballgrid[1]]
            print abs(nextpos[0]-self.pos[0]-self.size[0]/2) , abs(nextpos[1]-self.pos[1]-self.size[0]/2), bool(abs(dy)),bool(abs(dx)),"NOW"
            if abs((nextpos[0]-self.pos[0]-self.size[0]/2))<= 0 and bool(abs(dy)) or (abs(nextpos[1]-self.pos[1]-self.size[1]/2) <= 0 and bool(abs(dx))):
                self.oldgrid[0] = self.ballgrid[0]
                self.oldgrid[1] = self.ballgrid[1]
                print "FIN"
        else:
            #print self.parent,"AAAAAAAAAAAA"
            self.pos[0] = self.parent.gamemap.gridpos[self.ballgrid[0]][self.ballgrid[1]][0]-self.size[0]/2
            self.pos[1] = self.parent.gamemap.gridpos[self.ballgrid[0]][self.ballgrid[1]][1]-self.size[1]/2

    def changeGrid(self,x,y):
        self.ballgrid[0] = x
        self.ballgrid[1] = y

    def setFirstStat(self,start,end):
        self.ballgrid[0] = self.oldgrid[0] = start[0]
        self.ballgrid[1] = self.oldgrid[1] = start[1]
        self.endgrid[0] = end[0]
        self.endgrid[1] = end[1]

    def changePos(self,x,y):
        self.x = x
        self.y = y
    
    def changeColor(self):
        self.canvas.clear()
        self.canvas.add(Color(randint(0,100)/100.0,randint(0,100)/100.0,randint(0,100)/100.0))    
        self.canvas.add(GameColor().getColor('Green'))
        self.canvas.add(Ellipse(size=self.size,pos=self.pos))

    def __init__(self,**kwargs):
        super(GameBall,self).__init__(**kwargs)
        Clock.schedule_interval(self.smoothBall,1/60.0)

class GameTab(Widget):
    num_stage = 0
    gameball = ObjectProperty(None)
    gamemap = ObjectProperty(None)
    stepmethod = ''
    goenable = False

    def toggle(self):
        self.goenable = not self.goenable

    def readStage(self):
        # Open stage file
        num_color = 3
        map_size = 5
        color_list = ['Red','Green','Blue']
        color_table = [['White','White','White','White','White'],['White','White','White','White','White'],['White','White','White','White','White'],['White','White','White','White','White'],['White','White','White','White','White']]
        map_table = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        start_pos = [1,1]
        end_pos = [4,4]
        print self.center ,"KUY"
        self.gamemap = GameMap(map_t=map_table ,color_t=color_table,si=map_size,size=[400,400],center=self.center,rows=map_size,cols=map_size,spacing=5,size_hint=[None,None])
        self.add_widget(self.gamemap)
        self.gameball = GameBall(size=[50,50])
        self.add_widget(self.gameball)
        #self.gamemap.readMap(map_table, color_table, map_size)
        self.gameball.setFirstStat(start_pos, end_pos)

    def changeStep(self, way):
        self.stepmethod = way

    def ballControl(self):
        if self.stepmethod == 'U':
            self.gameball.ballgrid[0] -=1
        elif self.stepmethod == 'D':
            self.gameball.ballgrid[0] +=1
        elif self.stepmethod == 'L':
            self.gameball.ballgrid[1] -=1
        elif self.stepmethod == 'R':
            self.gameball.ballgrid[1] +=1
        if self.gameball.ballgrid[0]<0:
            self.gameball.ballgrid[0] = 0
        if self.gameball.ballgrid[0]>=self.gamemap.gridsize:
            self.gameball.ballgrid[0] = self.gamemap.gridsize-1
        if self.gameball.ballgrid[1]<0:
            self.gameball.ballgrid[1] = 0
        if self.gameball.ballgrid[1]>=self.gamemap.gridsize:
            self.gameball.ballgrid[1] = self.gamemap.gridsize-1
        self.changeStep('')

    def pt(self,x):
        #self.gameball.size = [30,30]
        #self.gameball.
        print "xx" 
        print "GameTab Center",self.center
        print "GameTab size",self.size
        self.gamemap.center = self.center
        print self.children
        for x in self.children[1].children:
            print x.center
            #print x.id
        self.gamemap.updateGridPos()
        tmpc = ['Red','Blue','Green','White']
        tmps = [True,False]
        for x in self.gamemap.children:
            x.changeColor(x.color)
            #x.star = tmps[randint(0,1)]
            #x.hasStar()
        print self.gamemap.gridpos
        print self.children[0].center, "zzzz"
        print self.children[0].size,self.children[0]
        print self.center,self
        radius = self.gameball.size[0]/2.0
        bpos = self.gameball.ballgrid
        print bpos
        tmpst = ['U','D','L','R']
        if self.goenable:
            self.changeStep(tmpst[randint(0,3)])
        self.ballControl()
        #self.gameball.changePos(self.children[1].children[bpos[0]].center_x-radius,self.children[1].children[bpos[1]].center_y-radius)
        #self.gameball.changePos(self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius,self.gamemap.gridpos[bpos[0]][bpos[1]][1]-radius)
        self.gameball.changeColor()
        #self.gameball.center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = tup

    def __init__(self,**kwargs):
        super(GameTab,self).__init__(**kwargs)
        self.pos = [0,0]
        self.readStage()
        Clock.schedule_interval(self.pt,1)

class GameScreen(Screen):
    pass

class LokiColorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.switch_to(GameScreen(name='gg'))
        #Clock.schedule_interval(game.update,1/60.0)
        return sm

if __name__ == '__main__':
    LokiColorApp().run()
