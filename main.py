from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition , SlideTransition , WipeTransition , ShaderTransition, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics import Color,Ellipse,Rectangle
from kivy.graphics.instructions import Canvas
from kivy.animation import Animation
from random import randint
from math import *
from sys import exit


class LokiColorG(Widget):
    pass

class GameColor():
    colorhash = {'Red':Color(1,0,0),'Green':Color(0,1,0),'Blue':Color(0,0,1),'White':Color(1,1,1),'Yellow':Color(1,1,0),'Sblue':Color(0,1,1),'Pink':Color(1,0,0.6),'Gray':Color(0.2,0.2,0.2),'Orange':Color(1,0.5,0),'Cream':Color(1,1,.5),'Purple':Color(0.8,0,1)}
    colorhashList = {'Red':[1,0,0],'Green':[0,1,0],'Blue':[0,0,1],'White':[1,1,1],'Yellow':[1,1,0],'Sblue':[0,1,1],'Pink':[1,0,0.6],'Gray':[0.2,0.2,0.2],'Orange':[1,0.5,0],'Cream':[1,1,.5],'Purple':[0.8,0,1]}
    
    def getColor(self,color):
        return self.colorhash[color]
    def getColorRGB(self,color):
        return self.colorhashList[color]

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

    def getColor(self):
        return self.color

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

    def getGridColor(self,x,y):
        for g in self.children:
            if g.id == 'm'+str(x)+str(y):
                return g.getColor()

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
    distance = 1.0

    #self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius

    def ballAnimation(self,next_grid):
        next_pos = self.parent.gamemap.gridpos[next_grid[0]][next_grid[1]]
        print "Next_pos" , next_pos
        #next_pos = self.parent.gamemap.gridpos[0][1]
        ani = Animation(x=next_pos[0]-self.size[0]/2.0,y=next_pos[1]-self.size[1]/2.0)
        #self.changeColor()
        #ani = Animation(x=self.x+50,y=self.y+50,step=1/60.0)
        ani.start(self)
        self.changeGrid(next_grid[0],next_grid[1])
        #self.changeGrid(1,2)

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
    
    def changeColor(self,color):
        #self.canvas.clear()
        #for x in dir(self.canvas):
        #    print x,getattr(self.canvas,x)
        print self.canvas.children
        print dir(self.canvas.children[1])
        print self.canvas.children[1].needs_redraw
        self.canvas.children[0].rgb = GameColor().getColorRGB(color)
        #self.clear_widgets()
        #my_canvas = Canvas()
        #my_canvas.add(GameColor().getColor('Green'))
        #my_canvas.add(Ellipse(size=self.size,pos=self.pos))
        #self.canvas = my_canvas
        #self.canvas.add(Color(randint(0,100)/100.0,randint(0,100)/100.0,randint(0,100)/100.0))    
        #self.canvas.children[0]=(Color(1,1,0))
        #self.canvas.children[2]=(Ellipse(size=self.size,pos=self.pos))
        #self.canvas.ask_update()
        #self.add_widget(pic)

    def __init__(self,**kwargs):
        super(GameBall,self).__init__(**kwargs)
        #Clock.schedule_interval(self.smoothBall,1.0/100000)

class GameTab(Widget):
    num_stage = 0
    gameball = ObjectProperty(None)
    gamemap = ObjectProperty(None)
    stepmethod = ''
    goenable = False
    
    def updateBallColor(self):
        r,c = self.gameball.ballgrid
        next_color = self.gamemap.getGridColor(r,c)
        if next_color != 'White':
            self.gameball.changeColor(next_color)

    def toggle(self):
        self.goenable = not self.goenable

    def readStage(self):
        # Open stage file
        num_color = 3
        map_size = 6
        color_list = ['Red','Green','Blue']
        #color_table = [['Blue','White','White','White','White'],['White','White','Green','White','White'],['Red','White','White','White','Red','White'],['White','White','Red','White','White'],['Red','White','White','White','White']]
        color_table = [['Blue','White','White','White','White','Blue'],['White','White','Green','Red','White','White'],['Red','White','White','White','Red','White','Blue'],['White','White','Red','White','White','Green'],['Red','White','Blue','White','White','White'],['White','White','Green','Red','White','White']]
        map_table = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        start_pos = [1,1]
        end_pos = [4,4]
        print self.center ,"C_Center"
        # Create GameMap
        self.gamemap = GameMap(map_t=map_table ,color_t=color_table,si=map_size,size=[400,400],center=self.center,rows=map_size,cols=map_size,spacing=0,size_hint=[None,None])
        self.add_widget(self.gamemap)
        # Create GameBall
        self.gameball = GameBall(size=[50,50])
        self.add_widget(self.gameball)
        self.gameball.setFirstStat(start_pos, end_pos)

    def changeStep(self, way):
        self.stepmethod = way

    def ballControl(self):
        now_grid = [self.gameball.ballgrid[0],self.gameball.ballgrid[1]]
        if self.stepmethod == 'U':
            now_grid[0] -=1
        elif self.stepmethod == 'D':
            now_grid[0] +=1
        elif self.stepmethod == 'L':
            now_grid[1] -=1
        elif self.stepmethod == 'R':
            now_grid[1] +=1
        if now_grid[0]<0:
            now_grid[0] = 0
        if now_grid[0]>=self.gamemap.gridsize:
           now_grid[0] = self.gamemap.gridsize-1
        if now_grid[1]<0:
            now_grid[1] = 0
        if now_grid[1]>=self.gamemap.gridsize:
            now_grid[1] = self.gamemap.gridsize-1
        self.changeStep('')
        print "Compare :",now_grid,self.gameball.ballgrid
        self.gameball.ballAnimation(now_grid)

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
        if self.stepmethod != '':
            self.updateBallColor()
            self.ballControl()
        #self.gameball.changePos(self.children[1].children[bpos[0]].center_x-radius,self.children[1].children[bpos[1]].center_y-radius)
        #self.gameball.changePos(self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius,self.gamemap.gridpos[bpos[0]][bpos[1]][1]-radius)
        #self.gameball.changeColor()
        #self.gameball.center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = tup

    def __init__(self,**kwargs):
        super(GameTab,self).__init__(**kwargs)
        self.pos = [0,0]
        self.readStage()
        Clock.schedule_interval(self.pt,1)

class GameControlCommand(FloatLayout):
    offset = 400
    origin_pos = [0,0]
    position = []
    grep = False
    i = 0
    def submitButton(self):
        submit = {}
        tmp = GameControlFunction.color
        for i in xrange(len(GameControlFunction.obj_push)):
            if GameControlFunction.obj_push[i] == 0:
                submit[tmp[i]] = ''
            else:
                submit[tmp[i]] = GameControlFunction.obj_push[i].id
        print submit
    def releaseButton(self):
        for x in GameControlFunction.obj_push:
            if x !=0:
                self.children[self.children.index(x)].pos = self.position[self.children.index(x)]
        GameControlFunction.push = [False]*GameControlFunction.number
        GameControlFunction.obj_push = [0]*GameControlFunction.number

    def on_touch_move(self, touch):
        if self.grep == False:
            for d in self.children:
                x,y = d.pos
                if x < touch.x and x+50 > touch.x and y < touch.y and y+50 > touch.y:
                    self.grep = True
                    self.i = self.children.index(d)
                    self.origin_pos = [x,y]
                    break
        else:
            self.children[self.i].pos = [touch.x-25,touch.y-25]

    def on_touch_up(self, touch):
        if self.grep == True:
            ## solve ##
            solve = []
            boolean = False
            for j in range(len(GameControlFunction.push)):
                click_x,click_y = self.children[self.i].pos
                block_x,block_y = GameControlFunction.block_pos[j]
                x_min = sorted([click_x , click_x+50 , block_x , block_x+50])
                y_min = sorted([click_y , click_y+50 , block_y , block_y+50])
                if (x_min[0:2] != [click_x,click_x+50] and x_min[0:2] != [block_x,block_x+50]) and (y_min[0:2] != [click_y,click_y+50] and y_min[0:2] != [block_y,block_y+50]):
                    solve.append([j,(x_min[2]-x_min[1])*(y_min[2]-y_min[1])])
            index = 0
            if len(solve) == 0:
                self.children[self.i].pos = self.position[self.i]
                if self.children[self.i] in GameControlFunction.obj_push:
                    GameControlFunction.push[GameControlFunction.obj_push.index(self.children[self.i])] = False
                    GameControlFunction.obj_push[GameControlFunction.obj_push.index(self.children[self.i])] = 0
                self.grep = False
                #self.update()
                return 
            elif len(solve) == 1:
                index = solve[0][0]
                boolean = self.move(self.i,index)
            else:
                if solve[0][1] >= solve[1][1]:
                    index = solve[0][0]
                    if GameControlFunction.push[index] == True:
                        index = solve[1][0]
                        if GameControlFunction.push[index] == True:
                            index = solve[0][0]
                    boolean = self.move(self.i,index)
                else :
                    index = solve[1][0]
                    if GameControlFunction.push[index] == True:
                        index = solve[0][0]
                        if GameControlFunction.push[index] == True:
                            index = solve[1][0]
                    boolean = self.move(self.i,index)
            ## solve ##
            if boolean:
                self.children[self.i].pos = self.origin_pos
            self.grep = False
            #self.update()

    def move(self,i,index):
        if GameControlFunction.push[index] == True:
            self.children[self.children.index(GameControlFunction.obj_push[index])].pos = self.position[self.children.index(GameControlFunction.obj_push[index])]
            GameControlFunction.push[index] = False
            GameControlFunction.obj_push[index] = 0

            self.children[i].pos = GameControlFunction.block_pos[index]
            GameControlFunction.push[index] = True
            GameControlFunction.obj_push[index] = self.children[i]
            return False

        elif GameControlFunction.push[index] == False:
            self.children[i].pos = GameControlFunction.block_pos[index]
            if self.children[i] in GameControlFunction.obj_push:
                GameControlFunction.push[GameControlFunction.obj_push.index(self.children[i])] = False
                GameControlFunction.obj_push[GameControlFunction.obj_push.index(self.children[i])] = 0
            GameControlFunction.push[index] = True
            GameControlFunction.obj_push[index] = self.children[i]
            return False
        return True

    def update(self):
        num_obj = 6-GameControlFunction.obj_push.count(0)
        all_obj = []
        for i in range(6):
            if GameControlFunction.obj_push[i] != 0:
                all_obj.append(i)
        run = 0
        for i in all_obj:
            if i != run: 
                self.move(self.children.index(GameControlFunction.obj_push[i]),run)
            run+=1

    def __init__(self,**kwargs):
        super(GameControlCommand, self).__init__(**kwargs)
        data = ['U','D','L','R']
        index = 0
        for x in xrange(5):
            for y in xrange(5):
                type_button = data[index]
                index+=1
                for z in xrange(len(GameControlFunction.color)+2):
                    if type_button == 'U':
                        self.add_widget(Button(background_normal='images/up.png',background_down='images/up_c.png',id=type_button,size_hint=[.1, .1],pos=[400+y*50,self.offset+x*50]))
                    elif type_button == 'D':
                        self.add_widget(Button(background_normal='images/down.png',background_down='images/down_c.png',id=type_button,size_hint=[.1, .1],pos=[400+y*50,self.offset+x*50]))
                    elif type_button == 'R':
                        self.add_widget(Button(background_normal='images/right.png',background_down='images/right_c.png',id=type_button,size_hint=[.1, .1],pos=[400+y*50,self.offset+x*50]))
                    elif type_button == 'L':
                        self.add_widget(Button(background_normal='images/left.png',background_down='images/left_c.png',id=type_button,size_hint=[.1, .1],pos=[400+y*50,self.offset+x*50]))
                if index >= len(data):
                        break
            if index >= len(data):
                break
        for x in self.children:
            a,b = x.pos
            self.position.append([a,b])

class GameControlFunction(FloatLayout):
    start = 400
    offset = 2
    push = [False]
    obj_push = [0]
    block_pos = []
    color = []
    number = 0

    def __init__(self,**kwargs):
        super(GameControlFunction, self).__init__(**kwargs)
        f = open("input.txt")
        self.color = f.readlines()[0].split(' ')
        f.close()
        GameControlFunction.number = int(self.color[0])
        GameControlFunction.color = self.color[1:]
        GameControlFunction.push = [False]*self.number
        GameControlFunction.obj_push = self.obj_push*self.number
        index = 0
        for x in xrange(GameControlFunction.number):
            if GameControlFunction.color[x] == 'Red':
                self.canvas.add(Color(1,0,0))
            elif GameControlFunction.color[x] == 'Green':
                self.canvas.add(Color(0,1,0))
            elif GameControlFunction.color[x] == 'Blue':
                self.canvas.add(Color(0,0,1))
            elif GameControlFunction.color[x] == 'Yellow':
                self.canvas.add(Color(1,1,0))
            elif GameControlFunction.color[x] == 'Sblue':
                self.canvas.add(Color(0,1,1))
            elif GameControlFunction.color[x] == 'Pink':
                self.canvas.add(Color(1,0,.6))
            elif GameControlFunction.color[x] == 'Gray':
                self.canvas.add(Color(.2,.2,.2))
            elif GameControlFunction.color[x] == 'White':
                self.canvas.add(Color(1,1,1))
            elif GameControlFunction.color[x] == 'Orange':
                self.canvas.add(Color(1,.5,0))
            elif GameControlFunction.color[x] == 'Cream':
                self.canvas.add(Color(1,1,.5))
            elif GameControlFunction.color[x] == 'Purple':
                self.canvas.add(Color(.8,0,1))
            self.canvas.add(Rectangle(size=(50, 50),pos=(50 + index*self.offset + index*50,self.start)))
            self.block_pos.append([50 + index*self.offset + index*50,self.start])
            index+=1
            if index > 5:
                index = 0
                self.start -= 70

class ReleaseButton(FloatLayout):
    pass

class GameScreen(Screen):
    pass

class GameControl(Screen):
    pass

class LokiColorApp(App):
    def build(self):
        Config.set('graphics','maxfps',300)
        Config.write()
        sm = ScreenManager()
        #sm.switch_to(GameControl(name='gg'))
        sm.switch_to(GameScreen(name='gg'))
        #Clock.schedule_interval(game.update,1/60.0)
        return sm

if __name__ == '__main__':
    LokiColorApp().run()
