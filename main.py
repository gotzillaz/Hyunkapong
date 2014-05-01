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
from math import *
from sys import exit

Builder.load_string("""
<GameMap>:
    size: 50,50
    center_x: self.parent.center_x
    center_y: self.parent.center_y
    rows: 4
    cols: 4
    spacing: 0

<GameScreen>:
    gamemap: gg
    
    GameMap:
        id: gg
        size: 100,100
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        size_hint: None,None
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

class GameScreen(Screen):
    def pt(self,x):
        print self.center_x,self.center_y
        print self.x,self.y
        print Window.size
        print self.children[0].pos

    def __init__(self,**kwargs):
        super(GameScreen,self).__init__(**kwargs)
        Clock.schedule_interval(self.pt,1/60)

class LokiColorApp(App):
    def build(self):
        #game = LokiColorG()
        sm = ScreenManager()
        sm.switch_to(GameScreen())
        #Clock.schedule_interval(game.update,1/60.0)
        return sm

if __name__ == '__main__':
    LokiColorApp().run()
