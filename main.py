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
from kivy.graphics import Color,Ellipse
from random import randint
from math import *
from sys import exit

class LokiColorG(Widget):
    pass

class GameMap(GridLayout):
    gridsize = 4
    gridpos = [[]]

    def updateGridPos(self):
        for x in self.children:
            print x.id
            pr = int(x.id[1])
            pc = int(x.id[2])
            self.gridpos[pr][pc] = (x.center_x,x.center_y)

    def createGridPos(self, num):
        self.gridpos = [[(0,0) for x in xrange(num)] for y in xrange(num)]

    def __init__(self,**kwargs):
        super(GameMap, self).__init__(**kwargs)
        for x in xrange(4):
            for y in xrange(4):
                self.add_widget(Button(id='m'+str(x)+str(y),size=[100,100],text=str(x)+' '+str(y)))
        for x in self.children:
            print x.pos,x.parent.pos,x.text,x.center_x,x.center_y
        print self.pos,self.center_x,self.center_y
        self.createGridPos(self.gridsize)
        self.updateGridPos()
        print self.gridpos
    
class GameBall(Widget):
    ballgrid = [1,1]

    def changePos(self,x,y):
        self.x = x
        self.y = y
    
    def changeColor(self):
        self.canvas.clear()
        self.canvas.add(Color(randint(0,100)/100.0,randint(0,100)/100.0,randint(0,100)/100.0))    
        self.canvas.add(Ellipse(size=self.size,pos=self.pos))

    def __init__(self,**kwargs):
        super(GameBall,self).__init__(**kwargs)

class GameTab(Widget):
    gameball = ObjectProperty(None)
    gamemap = ObjectProperty(None)

    def pt(self,x):
        #self.gameball.size = [30,30]
        #self.gameball.
        print "xx" 
        print self.children
        for x in self.children[1].children:
            print x.center
            #print x.id
        self.gamemap.updateGridPos()
        print self.gamemap.gridpos
        print self.children[0].center, "zzzz"
        print self.children[0].size,self.children[0]
        print self.center,self
        radius = self.gameball.size[0]/2.0
        bpos = self.gameball.ballgrid
        print bpos
        #self.gameball.changePos(self.children[1].children[bpos[0]].center_x-radius,self.children[1].children[bpos[1]].center_y-radius)
        self.gameball.changePos(self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius,self.gamemap.gridpos[bpos[0]][bpos[1]][1]-radius)
        self.gameball.changeColor()
        #self.gameball.center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = tup

    def __init__(self,**kwargs):
        super(GameTab,self).__init__(**kwargs)
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
