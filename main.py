from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition , SlideTransition , WipeTransition , ShaderTransition, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.image import Image
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

class PopupContent(BoxLayout):
    pass

class GameColor():
    colorhash = {'Red':Color(0.99609,0.32031,0.32031),'Green':Color(0.15625,0.85546,0.46875),'Blue':Color(0.16406,0.75000,0.82421),'White':Color(1,1,1),'Yellow':Color(0.99609,0.88281,0.32031),'Sblue':Color(0,1,1),'Pink':Color(0.99609,0.37890,0.49609),'Gray':Color(0.2,0.2,0.2),'Orange':Color(1,0.5,0),'Cream':Color(1,1,.5),'Purple':Color(0.48047,0.41016,0.73437)}
    colorhashList = {'Red':[0.99609,0.32031,0.32031],'Green':[0.15625,0.85546,0.46875],'Blue':[0.16406,0.75000,0.82421],'White':[1,1,1],'Yellow':[0.99609,0.88281,0.32031],'Sblue':[0,1,1],'Pink':[0.99609,0.37890,0.49609],'Gray':[0.2,0.2,0.2],'Orange':[1,0.5,0],'Cream':[1,1,.5],'Purple':[0.48047,0.41016,0.73437]}
    
    def getColor(self,color):
        return self.colorhash[color]
    def getColorRGB(self,color):
        return self.colorhashList[color]

class GamePlate(Widget):
    color = 'White'
    text = ''
    star = False
    img = ObjectProperty(None)

    def hasStar(self):
        if self.star:
            self.canvas.add(Color(0,0,0))
            self.canvas.add(Ellipse(size=[10,10],pos=self.pos))

    def setFlag(self):
        self.img.source = 'images/flag_2.png'

    def changeColor(self, mycolor):
        self.color = mycolor
        self.canvas.children[0].rgb = GameColor().getColorRGB(mycolor)
        #self.canvas.add(GameColor().getColor(mycolor))
        #self.canvas.add(Rectangle(size=self.size,pos=self.pos))

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
    object_map = [[]]
    
    def readMap(self,map_table,color_table,size):
        self.gridsize = size
        self.map_table = [[x for x in y] for y in map_table]
        self.color_table = [[x for x in y] for y in color_table]
        self.object_map = []
        for x in color_table:
            tmp = []
            for y in x:
                if y != 'White':
                    tmp.append(True)
                else:
                    tmp.append(False)
            self.object_map.append(tmp)

    def getGridColor(self,x,y):
        for g in self.children:
            if g.id == 'm'+str(x)+str(y):
                return g.getColor()

    def updateGridPos(self):
        for x in self.children:
            #print x.id
            pr = int(x.id[1])
            pc = int(x.id[2])
            self.gridpos[pr][pc] = (x.center_x,x.center_y)

    def createGridPos(self, num):
        self.gridpos = [[(0,0) for x in xrange(num)] for y in xrange(num)]

    def updateItem(self, x, y):
        if self.object_map[x][y]:
            self.object_map[x][y] = False
            return 1
        else:
            return 0

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
    startgrid = [0,0]
    endgrid = [1,1]
    ball_color = 'White'
    distance = 1.0
    img = ObjectProperty(None)

    #self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius

    def ballAnimation(self,next_grid):
        next_pos = self.parent.gamemap.gridpos[next_grid[0]][next_grid[1]]
        #print "Next_pos" , next_pos
        #next_pos = self.parent.gamemap.gridpos[0][1]
        ani = Animation(x=next_pos[0]-self.size[0]/2.0,y=next_pos[1]-self.size[1]/2.0,duration=0.1)
        #self.changeColor()
        #ani = Animation(x=self.x+50,y=self.y+50,step=1/60.0)
        ani.start(self)
        self.changeGrid(next_grid[0],next_grid[1])
        #self.changeGrid(1,2)

    def changeGrid(self,x,y):
        self.ballgrid[0] = x
        self.ballgrid[1] = y

    def setFirstStat(self,start,end,color):
        self.ballgrid[0] = self.oldgrid[0] = start[0]
        self.ballgrid[1] = self.oldgrid[1] = start[1]
        self.startgrid[0] = start[0]
        self.startgrid[1] = start[1]
        self.endgrid[0] = end[0]
        self.endgrid[1] = end[1]
        self.changeColor(color)

    def changePos(self,x,y):
        self.x = x
        self.y = y
    
    def changeColor(self,color):
        #self.canvas.clear()
        #for x in dir(self.canvas):
        #    print x,getattr(self.canvas,x)
        #print self.canvas.children
        #print dir(self.canvas.children[1])
        #print self.canvas.children[1].needs_redraw
        #self.canvas.children[3].rgb = GameColor().getColorRGB(color)
        self.ball_color = color
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
        #self.img = Image(source='images/robot_down.png')
        #self.add_widget(self.img)
        #Clock.schedule_interval(self.smoothBall,1.0/100000)

class GamePopup(Widget):
    next_s = ObjectProperty(None)
    re_s = ObjectProperty(None)
    scr_l = ObjectProperty(None)

class GameTab(Widget):
    stage_id = 0
    score = 0
    starrequire = []
    stagelabel = ObjectProperty(None)
    gameball = ObjectProperty(None)
    gamemap = ObjectProperty(None)
    gamecontrol = ObjectProperty(None)
    gamescore = ObjectProperty(None)
    stepmethod = ''
    color_direction = {}
    gamepopup = ObjectProperty(None)
    gamerun = ObjectProperty(None)
    haspopup = False
    goenable = False
    
    def updateBallColor(self):
        r,c = self.gameball.ballgrid
        next_color = self.gamemap.getGridColor(r,c)
        if next_color != 'White':
            self.gameball.changeColor(next_color)

    def closePopup(self):
        self.haspopup = False

    def checkEndGrid(self):
        if self.gameball.endgrid == self.gameball.ballgrid and self.haspopup == False:
            self.changeStep('')
            self.haspopup = True
            """
            btn = Button(text='Next Stage')
            popup = Popup(title='Mission Accomplish',
                content=Label(text='HAHAHA'),
                size_hint=(0.5, 0.5),
                )
            popup.bind(on_dismiss=callback)
            popup.open()
            """
            self.gamepopup = GamePopup(size=Window.size)
            self.add_widget(self.gamepopup)
            self.gamepopup.next_s.center = self.center
            self.gamepopup.next_s.center_x = self.center_x - 75
            self.gamepopup.re_s.center = self.center
            self.gamepopup.re_s.center_x = self.center_x + 75
            self.gamepopup.scr_l.center = self.center
            self.gamepopup.scr_l.center_y = self.center_y + 125
            self.gamepopup.scr_l.text = 'You got\n' + str(self.score) + ' point'
            if self.score > 1:
                self.gamepopup.scr_l.text+='s'
            print "ENDDING"
            self.score = 0
            #self.readStage(self.stage_id+1)

    def toggle(self):
        print "MEOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        self.goenable = not self.goenable
        print self.goenable
        if not self.goenable:
            self.resetStage()
        print "SCORE ",self.score
        self.gamecontrol.gamecontrolcommand.submitButton()
        self.color_direction = self.gamecontrol.gamecontrolcommand.command_hash

    def resetStage(self):
        self.changeStep('')
        self.remove_widget(self.gamepopup)
        i,j = 0,0
        for x in self.gamemap.color_table:
            j = 0
            for y in x:
                if y != 'White':
                    self.gamemap.object_map[i][j] = True
                j+=1
            i+=1
        self.score = 0
        print "StartGrid", self.gameball.startgrid
        self.gameball.img.source = 'images/robot_down.png'
        self.gameball.changeGrid(self.gameball.startgrid[0],self.gameball.startgrid[1])
        
    def readStage(self,num_stage):
        # Open stage file
        o_file = open('maps/'+str(num_stage)+'.in')
        file_map = map(lambda x: x.strip(),o_file.readlines())
        o_file.close()
        ######
        self.clear_widgets()
        self.score = 0
        self.stage_id = num_stage
        num_color = int(file_map[1])
        map_size = int(file_map[0])
        color_list = file_map[2].split()
        self.color_direction = { c:'' for c in color_list}
        color_table = []
        for ct in file_map[3:3+map_size]:
            color_table.append(ct.split())
        start_pos = map(int,file_map[3+map_size].split())
        end_pos = map(int,file_map[3+map_size+1].split())
        self.starrequire = map(int,file_map[3+map_size+2].split())
        #file_map.close()
        print self.center ,"C_Center"
        # Create GameMap
        sizing = min(Window.size)*0.8
        print self.center ,"CENTER BEFORE CREATE MAP"
        self.gamemap = GameMap(map_t=[] ,color_t=color_table,si=map_size,size_hint=(None,None),size=(sizing,sizing),center_x=self.center_x,center_y=self.center_y,rows=map_size,cols=map_size,spacing=0)
        self.add_widget(self.gamemap)
        self.gamemap.center_x = self.center_x
        self.gamemap.center_y = self.center_y
        print self.gamemap.gridpos
        #self.gamemap.size_hint=(0.1,0.1)
        #self.gamemap.size=(500,500)
        print self.gamemap.size,self.gamemap.size_hint,"GAMEMAP SIZE"
        print self.gamemap.center ,"GAMEMAP CENTER"
        # Create GameBall
        self.gameball = GameBall(size=[50,50],pos=[500,100])
        self.add_widget(self.gameball)
        self.gameball.setFirstStat(start_pos, end_pos,color_table[start_pos[0]][start_pos[1]])
        st_x,st_y = self.gamemap.gridpos[1][1]
        self.gameball.pos = (st_x - self.gameball.size[0]/2.0,st_y-self.gameball.size[1]/2.0) 
        print self.gameball.pos , "GAMEBALL POS INIT"
        
        # Create GameControl
        self.gamecontrol = GameControl(color_list=color_list)
            #self.gamecontrol = GameControlFunction(color_list=color_list)
        self.add_widget(self.gamecontrol)
        
        # Create ToggleButton
        self.gamerun = ToggleButton(size=[50,50],pos=[330,70] ,on_press=lambda x: self.toggle(),background_normal='images/remote_play.png',background_down='images/remote_stop.png')
        self.add_widget(self.gamerun)
        #self.gamerun.bind(on_press=self.toggle)
        self.goenable = False
        self.haspopup = False

        # Create Label
        self.stagelabel = Label(text='Stage'+str(self.stage_id),font_size=75)
        self.add_widget(self.stagelabel)
        self.stagelabel.top = self.top
        self.stagelabel.center_x = self.center_x

    def changeStep(self, way):
        self.stepmethod = way
    
    def ballControl(self):
        now_grid = [self.gameball.ballgrid[0],self.gameball.ballgrid[1]]
        if self.stepmethod == 'U':
            now_grid[0] -=1
            self.gameball.img.source = 'images/robot_up.png'
        elif self.stepmethod == 'D':
            now_grid[0] +=1
            self.gameball.img.source = 'images/robot_down.png'
        elif self.stepmethod == 'L':
            now_grid[1] -=1
            self.gameball.img.source = 'images/robot_left.png'
        elif self.stepmethod == 'R':
            now_grid[1] +=1
            self.gameball.img.source = 'images/robot_right.png'
        if now_grid[0]<0:
            now_grid[0] = 0
        if now_grid[0]>=self.gamemap.gridsize:
           now_grid[0] = self.gamemap.gridsize-1
        if now_grid[1]<0:
            now_grid[1] = 0
        if now_grid[1]>=self.gamemap.gridsize:
            now_grid[1] = self.gamemap.gridsize-1
        self.changeStep('')
        #print "Compare :",self.gameball.ballgrid,self.gameball.startgrid
        self.gameball.ballAnimation(now_grid)

    def pt(self,x):
        if self.haspopup:
            return 
        #self.gameball.size = [30,30]
        #self.gameball.
        """
        print "xx" 
        print "GameTab Center",self.center
        print "GameTab size",self.size
        #self.gamemap.center = self.center
        print self.children
        for x in self.children[1].children:
            print x.center
            #print x.id
        """
        self.gamemap.updateGridPos()
        tmpc = ['Red','Blue','Green','White']
        tmps = [True,False]
        for x in self.gamemap.children:
            x.changeColor(x.color)
            if self.gameball.endgrid == map(int,[x.id[1],x.id[2]]):
                x.setFlag()
                print "YYYYYYYYYY"
                print self.gameball.endgrid
            else:
                x.clear_widgets()
            #x.star = tmps[randint(0,1)]
        """    #x.hasStar()
        print self.gamemap.gridpos
        print self.children[0].center, "zzzz"
        print self.children[0].size,self.children[0]
        print self.center,self"""
        bpos = self.gameball.ballgrid
        #print bpos
        tmpst = ['U','D','L','R']
        if self.goenable:
            self.updateBallColor()
            self.changeStep(self.color_direction[self.gameball.ball_color])
        if self.stepmethod != '':
            self.checkEndGrid()
        self.ballControl()
        self.score += self.gamemap.updateItem(self.gameball.ballgrid[0],self.gameball.ballgrid[1])
        #self.gamescore.text = str(self.score)
        #self.gameball.changePos(self.children[1].children[bpos[0]].center_x-radius,self.children[1].children[bpos[1]].center_y-radius)
        #self.gameball.changePos(self.gamemap.gridpos[bpos[0]][bpos[1]][0]-radius,self.gamemap.gridpos[bpos[0]][bpos[1]][1]-radius)
        #self.gameball.changeColor()
        #self.gameball.center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = self.children[1].children[randint(0,15)].center
        #self.children[0].center = tup

    def __init__(self,**kwargs):
        super(GameTab,self).__init__(**kwargs)
        self.pos = [0,0]
        self.size = Window.size
        print self.size,"GAMETAB WINDOW SIZE"
        print self.center,"GAMETAB CENTER INIT"
        self.readStage(1)
        Clock.schedule_interval(self.pt,0.5)

class GameControlCommand(FloatLayout):
    offset = 400
    origin_pos = [0,0]
    position = []
    grep = False
    i = 0
    command_hash = {}

    def submitButton(self):
        tmp = GameControlFunction.color
        for i in xrange(len(GameControlFunction.obj_push)):
            if GameControlFunction.obj_push[i] == 0:
                self.command_hash[tmp[i]] = ''
            else:
                self.command_hash[tmp[i]] = GameControlFunction.obj_push[i].id

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
        """
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print GameControlFunction.number
        print GameControlFunction.color
        print GameControlFunction.push
        print GameControlFunction.obj_push
        """
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
            #print "BUG PAO WA SASSSSSSSSSSS"
            #print solve
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

    def __init__(self,colorNum,**kwargs):
        super(GameControlCommand, self).__init__(**kwargs)
        data = ['U','D','L','R']
        index = 0
        for x in xrange(5):
            for y in xrange(5):
                type_button = data[index]
                index+=1
                for z in xrange(colorNum+2):
                    if type_button == 'U':
                        self.add_widget(Button(background_normal='images/up.png',background_down='images/up_c.png',id=type_button,size_hint=[.1, .1],pos=[50+3*50,70+x*50]))
                    elif type_button == 'D':
                        self.add_widget(Button(background_normal='images/down.png',background_down='images/down_c.png',id=type_button,size_hint=[.1, .1],pos=[50+4*50,70+x*50]))
                    elif type_button == 'R':
                        self.add_widget(Button(background_normal='images/right.png',background_down='images/right_c.png',id=type_button,size_hint=[.1, .1],pos=[50+3*50,20+x*50]))
                    elif type_button == 'L':
                        self.add_widget(Button(background_normal='images/left.png',background_down='images/left_c.png',id=type_button,size_hint=[.1, .1],pos=[50+4*50,20+x*50]))
                if index >= len(data):
                        break
            if index >= len(data):
                break
        self.position = []
        for x in self.children:
            a,b = x.pos
            self.position.append([a,b])
        """
        print self.children
        print self.position
        print len(self.children),len(self.position)
        print "*******************************************"
        """
class GameControlFunction(FloatLayout):
    start = 50
    offset = 2
    push = [False]
    obj_push = [0]
    block_pos = []
    color = []
    number = 0

    def __init__(self,color_list,**kwargs):
        super(GameControlFunction, self).__init__(**kwargs)
        #f = open("input.txt")
        #self.color = f.readlines()[0].split(' ')
        #f.close()
        GameControlFunction.number = len(color_list)
        GameControlFunction.color = [c for c in color_list]
        GameControlFunction.push = [False]*len(color_list)
        GameControlFunction.obj_push = [0]*len(color_list)
        """
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        print color_list
        print GameControlFunction.number
        print GameControlFunction.color
        print GameControlFunction.push
        print GameControlFunction.obj_push
        """
        index = 0
        GameControlFunction.block_pos = []
        for x in xrange(GameControlFunction.number):
            self.canvas.add(GameColor().getColor(GameControlFunction.color[x]))
            """
            if GameControlFunction.color[x] == 'Red':
                self.canvas.add(GameColor.getcolor('Red'))
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
            """
            self.canvas.add(Rectangle(size=(50, 49),pos=(10+index*self.offset + index*50,20+self.start)))
            GameControlFunction.block_pos.append([10+index*self.offset + index*50,20+self.start])
            index+=1
            if index > 2:
                index = 0
                self.start -= 50

class ReleaseButton(FloatLayout):
    pass

class GameScreen(Screen):
    pass
class StartScreen(Screen):
    def toGameScreen(self):
        self.parent.current = 'gs'

class GameControl(Widget):
    gamecontrolcommand = ObjectProperty(None)
    gamecontrolfunction = ObjectProperty(None)
    
    def __init__(self,color_list,**kwargs):
        super(GameControl, self).__init__(**kwargs)
        self.gamecontrolfunction = GameControlFunction(color_list=color_list)
        self.add_widget(self.gamecontrolfunction)
        self.gamecontrolcommand = GameControlCommand(len(color_list))
        self.add_widget(self.gamecontrolcommand)

class LokiColorApp(App):
    def build(self):
        Config.set('graphics','maxfps','300')
        Config.set('graphics','width','384')
        Config.set('graphics','height','640')
        Config.write()
        sm = ScreenManager(transition=FadeTransition())
        st = StartScreen(name='st')
        gs = GameScreen(name='gs')
        sm.add_widget(st)
        sm.add_widget(gs)
        #sm.switch_to(st)
        #Clock.schedule_interval(game.update,1/60.0)
        return sm

if __name__ == '__main__':
    LokiColorApp().run()
