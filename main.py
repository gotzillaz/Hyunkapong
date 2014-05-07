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

Builder.load_string("""
<GameBall>:
    size: 30,30
    canvas: 
        Color:
            rgba: 1,0,0,1
        Ellipse:
            pos: self.pos
            size: 30,30

<GameMap>:
    size: 500,500
    center_x: self.parent.center_x
    center_y: self.parent.center_y
    rows: 4
    cols: 4
    spacing: 0

<GameScreen>:
    gameball: bb
    gamemap: gg

    GameMap:
        id: gg
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        size_hint: None,None
    
    GameBall:
        id: bb
        center: self.center
""")
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
    def __init__(self,**kwargs):
        super(GameBall,self).__init__(**kwargs)

class GameScreen(Screen):
    gameball = ObjectProperty(None)
    gamemap = ObjectProperty(None)

    def pt(self,x):
        print "xx" 
        print self.children
        for x in self.children[1].children:
            print x.center
        print self.children[0].center, "zzzz"
        print self.children[0].size,self.children[0]
        print self.center,self
        self.gameball.center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = tup

    def __init__(self,**kwargs):
        super(GameScreen,self).__init__(**kwargs)
        Clock.schedule_interval(self.pt,1)

class LokiColorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.switch_to(GameScreen(name='gg'))
        #Clock.schedule_interval(game.update,1/60.0)
        return sm

if __name__ == '__main__':
    LokiColorApp().run()
