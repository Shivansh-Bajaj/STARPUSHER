import random,copy,pygame,os,sys
from pygame.locals import *
FPS=30
lightblue=(0,0,55)
white=(225,225,225)
black=(0,0,0)
green=(0,200,0)
blue=(0,170,225)
FPSclock=pygame.time.Clock()
blockwidth=50
blockheight=85
blockbaseheight=40
screenwidth,screenheight=800,600
file='levelfile.txt'
class player:
    def __init__(self):
        pass        
def terminate():
    pygame.quit()
    sys.exit()
def startscreen1():
    pygame.init()
    screen=pygame.display.set_mode((screenwidth,screenheight))
    global screen
    screen.fill(blue)
    message_display("STAR PUSHER 1.01",(400,300))
    start=pygame.image.load('startnow.png')
    screen.blit(start,(300,400))
    while True:    
        for event in pygame.event.get():
            if event.type==QUIT:
                crashed=True
                terminate()
            if event.type==MOUSEBUTTONDOWN:
                (x,y)=event.pos
                if x>300 and x<500 and y>400 and y<450:
                    main()
        pygame.display.update()
        FPSclock.tick(15)
def text_object(text,font):     
    textsurface=font.render(text,True,white)
    return textsurface,textsurface.get_rect()
def message_display(text,cenpos):
    largetext=pygame.font.Font('freesansbold.ttf',72)
    textsurf,textrect=text_object(text,largetext)
    textrect.center=cenpos
    screen.blit(textsurf,textrect)
    pygame.display.update()
def reset():
    pass
def main():
    pygame.init()
    
    screen=pygame.display.set_mode((screenwidth,screenheight))
    i=1
    allimages = {'uncovered goal': pygame.image.load('RedSelector.png').convert_alpha(),
                  'covered goal': pygame.image.load('Selector.png').convert_alpha(),
                  'star': pygame.image.load('Star.png').convert_alpha(),
                  'corner': pygame.image.load('Wall_Block_Tall.png').convert_alpha(),
                  'wall': pygame.image.load('Wood_Block_Tall.png').convert_alpha(),
                  'inside floor': pygame.image.load('Plain_Block.png').convert_alpha(),
                  'outside floor': pygame.image.load('Grass_Block.png').convert_alpha(),
                  'title': pygame.image.load('star_title.png').convert_alpha(),
                  'solved': pygame.image.load('star_solved.png').convert_alpha(),
                  'princess': pygame.image.load('princess.png').convert_alpha(),
                  'boy': pygame.image.load('boy.png').convert_alpha(),
                  'catgirl': pygame.image.load('catgirl.png').convert_alpha(),
                  'horngirl': pygame.image.load('horngirl.png').convert_alpha(),
                  'pinkgirl': pygame.image.load('pinkgirl.png').convert_alpha(),
                  'rock': pygame.image.load('Rock.png').convert_alpha(),
                  'short tree': pygame.image.load('Tree_Short.png').convert_alpha(),
                  'tall tree': pygame.image.load('Tree_Tall.png').convert_alpha(),
                  'ugly tree': pygame.image.load('Tree_Ugly.png').convert_alpha(),
                  'obama': pygame.image.load('obama.png').convert_alpha()}
   
    enelement={
            '.': allimages['uncovered goal'],
            '@': allimages['boy'],
            '$': allimages['star']
            }
    mapelement={
            '#': allimages['wall'],
            '1': allimages['outside floor']
            }
    
    global enelement,allimages,mapelement
    crashed = False
    level=loadlevel(file)
    
    mapsurf=drawmap(level.level['level'])
    mapsurfrect=mapsurf.get_rect()
    mapsurfrect.center=(screenwidth/2,screenheight/2)
    screen.blit(mapsurf,mapsurfrect)
    
    while not crashed:
        for event in pygame.event.get():
            if event.type==QUIT:
                crashed=True
                terminate()
          
        pygame.display.update()
#       clock.tick(60)
def loadlevel(file):
    levelfile=open(file,'r')
    content=levelfile.readlines() +['\r\n']
    levelfile.close()
    mapobj=[]
    levels=[]
    levelno=0
    level=[]
    for lineno in range(len(content)):
        line=content[lineno].rstrip('\r\n')
        if ';' in line:
            line=line[:line.find(';')]
        if line!='':
            levels.append(line)
        elif line=='' and len(levels)>0:
            maxwidth=-1
            for i in range(len(levels)):
                if len(levels)>maxwidth:
                    maxwidth=len(levels)
            for i in range(len(levels)):
                levels+=' '*(maxwidth-len(levels[i]))
            for x in range(len(levels[0])):
                level.append([])
            for x in range(len(levels)):
                for y in range(maxwidth):
                    level[y].append(levels[x][y])
            originx=None
            originy=None
            goals=[]
            stars=[]
            for x in range(maxwidth):
                for y in range(len(level[x])):
                    if level[x][y]=='@':
                        originx=x
                        originy=y
                    if level[x][y]=='$':
                        stars.append((x,y))
                    if level[x][y]=='.':
                        goals.append((x,y))
            startobj= {
                'startpos':(originx,originy),
                'steps':0,
                'stars':stars
                }  

            levelobj={
                'width':maxwidth,
                'height':len(level),
                'level':level,
                'goals':goals,
                'startgame':startobj
                }
            mapobj.append(levelobj)
            level=[]
            levels=[]
            startobj={}
            levelno+=1
    return mapobj
    
def drawmap(level):
    gamesurfwidth=len(level)*blockwidth
    gamesurfheight=(len(level[0])-1)*blockbaseheight+blockheight
    gamesurf=pygame.Surface((gamesurfwidth,gamesurfheight))
    gamesurf.fill(blue)
    for x in range(len(level)):
        for y in range(len(level[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if level[x][y] in mapelement:
                block=mapelement[level[x][y]]
            else:
                block=allimages['inside floor']
            gamesurf.blit(block,rect)
            if level[x][y]=='.':
                gamesurf.blit(allimages['uncovered goal'],rect)
            if level[x][y]=='$':
                gamesurf.blit(allimages['star'],rect)
            if level[x][y]=='@':
                gamesurf.blit(allimages['boy'],rect)
    return gamesurf
startscreen1()
#if __name__=='__main__':
#   main()
