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
from random import randint
from math import *
from sys import exit

class LokiColorG(Widget):
    pass

class GameMap(GridLayout):
    def __init__(self,**kwargs):
        super(GameMap, self).__init__(**kwargs)
        for x in xrange(4):
            for y in xrange(4):
                self.add_widget(Button(id='m'+str(x)+str(y),size=(50,50),text=str(x)+' '+str(y)))
        for x in self.children:
            print x.pos,x.parent.pos,x.text,x.center_x,x.center_y
        print self.pos,self.center_x,self.center_y
    
class GameBall(Widget):
    def changePos(self,x,y):
        self.x = x
        self.y = y
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
        print self.children[0].center, "zzzz"
        print self.children[0].size,self.children[0]
        print self.center,self
        radius = self.gameball.size[0]/2
        self.gameball.changePos(self.children[1].children[randint(0,15)].center_x-radius,self.children[1].children[randint(0,15)].center_y-radius)
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
