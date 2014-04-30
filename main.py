from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from math import *

class LokiColorG(Widget):
    pass

class LokiColorApp(App):
    def build(self):
        game = LokiColorG()
        #Clock.schedule_interval(game.update,1/60.0)
        return game

if __name__ == '__main__':
    LokiColorApp().run()
