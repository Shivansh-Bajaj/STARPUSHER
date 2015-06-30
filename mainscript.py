import random,copy,pygame,os,sys,time
from pygame.locals import *
FPS=30
lightblue=(0,0,55)
pink=(233,110,233)
white=(225,225,225)
black=(0,0,0)
green=(0,200,0)
blue=(0,170,225)
FPSclock=pygame.time.Clock()
blockwidth=50
blockheight=85
background=pygame.image.load(os.path.join('pic','untitled.jpg'))
blockbaseheight=40
screenwidth,screenheight=800,600
file='levelfile.txt'
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('music','song.ogg'))
intro=pygame.mixer.Sound(os.path.join('music','intro.ogg'))
match=pygame.mixer.Sound(os.path.join('music','match.ogg'))
end=pygame.mixer.Sound(os.path.join('music','applause.ogg'))
def music(i):
    if i=='play':
        pygame.mixer.music.play(-1)
    elif i=='stop':
        pygame.mixer.music.stop()
    elif i=='pause':
        pygame.mixer.music.pause()
    elif i=='unpause':
        pygame.mixer.music.unpause()
def solveddisplay():
    music('stop')
    message_display('SOLVED',(screenwidth/2,screenheight/2))
    while True:
        if pygame.event.wait():
            break
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
    screen.fill(white)
    screen.blit(background,(0,0))
    start=pygame.image.load(os.path.join('pic','startnow.png'))
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
    intro.play()
    playmusic='play'
    music(playmusic)
    pygame.init()
    levelno=0
    screen=pygame.display.set_mode((screenwidth,screenheight))
    screen.fill(green)
    allimages = {'uncovered goal': pygame.image.load(os.path.join('pic','RedSelector.png')).convert_alpha(),
                  'covered goal': pygame.image.load(os.path.join('pic','Selector.png')).convert_alpha(),
                  'star': pygame.image.load(os.path.join('pic','Star.png')).convert_alpha(),
                  'corner': pygame.image.load(os.path.join('pic','Wall_Block_Tall.png')).convert_alpha(),
                  'wall': pygame.image.load(os.path.join('pic','Wood_Block_Tall.png')).convert_alpha(),
                  'inside floor': pygame.image.load(os.path.join('pic','Plain_Block.png')).convert_alpha(),
                  'outside floor': pygame.image.load(os.path.join('pic','Grass_Block.png')).convert_alpha(),
                  'title': pygame.image.load(os.path.join('pic','star_title.png')).convert_alpha(),
                  'solved': pygame.image.load(os.path.join('pic','star_solved.png')).convert_alpha(),
                  'rock': pygame.image.load(os.path.join('pic','Rock.png')).convert_alpha(),
                  'short tree': pygame.image.load(os.path.join('pic','Tree_Short.png')).convert_alpha(),
                  'tall tree': pygame.image.load(os.path.join('pic','Tree_Tall.png')).convert_alpha(),
                  'ugly tree': pygame.image.load(os.path.join('pic','Tree_Ugly.png')).convert_alpha(),
                  }
    playerno=1
    player=[pygame.image.load(os.path.join('pic','princess.png')).convert_alpha(),
            pygame.image.load(os.path.join('pic','boy.png')).convert_alpha(),
            pygame.image.load(os.path.join('pic','catgirl.png')).convert_alpha(),
            pygame.image.load(os.path.join('pic','horngirl.png')).convert_alpha(),
            pygame.image.load(os.path.join('pic','pinkgirl.png')).convert_alpha()]
    global goal1
    global enelement,allimages,mapelement
    goal1=allimages['uncovered goal']
    enelement={
            '.': goal1,
            '@': player[playerno],
            '$': allimages['star']
            }
    mapelement={
            '#': allimages['wall'],
            'x':allimages['corner'],
            ' ':allimages['outside floor'],
            'i':allimages['inside floor']
            }
    crashed = False
    global levelfinish
    levelfinish=False
    level=loadlevel(file)
    while not crashed:
        if levelfinished(level,levelno)==True:
            if levelno==len(level)-1:
                message_display('game complete',(screenwidth/2,screenheight/2))
            else:
                makemap(level,player,levelno,playerno)
                levelno+=1
                music('stop')
                end.play()
                solveddisplay()
                pygame.event.wait()
                end.stop()
                music(playmusic)
                makemap(level,player,levelno,playerno)
        for event in pygame.event.get():
            move=None
            moved=False
            makemap(level,player,levelno,playerno)
            if event.type==KEYDOWN:
                if event.key==K_m:
                    if playmusic=='play' or playmusic=='unpause':
                        music('pause')
                        playmusic='pause'
                    elif playmusic=='pause':
                        playmusic='play'
                        music('unpause')
                if event.key==K_r:
                    reset()
                if event.key==K_UP:
                    move='up'
                if event.key==K_DOWN:
                    move='down'
                if event.key==K_RIGHT:
                    move='right'
                if event.key==K_LEFT:
                    move='left'
                if event.key==K_ESCAPE:
                    crashed=True
                    terminate()
                moved=makemove(move,level[levelno])
                if event.key==K_w:
                    playerno+=1
                    if playerno>=len(player):
                        playerno=0
                if event.key==K_s:
                    playerno-=1
                    if playerno<0:
                        playerno=len(player)-1
            if event.type==QUIT:
                crashed=True
                terminate()
        pygame.display.update()
#       clock.tick(60)
def levelfinished(levelobj,levelno):
    for goal in levelobj[levelno]['goals']:
        if goal not in levelobj[levelno]['startgame']['stars']:
            return False
    return True
def makemap(level,player,levelno,playerno):
    (startx,starty)=level[levelno]['startgame']['startpos']
    backcopy=mapcomplete(level[levelno],startx,starty)
    mapsurf=drawmap(level[levelno],backcopy,player[playerno])
    mapsurfrect=mapsurf.get_rect()
    mapsurfrect.center=(screenwidth/2,screenheight/2)
    screen.blit(mapsurf,mapsurfrect)
def makemove(move,startgame):
    xofset=0
    yofset=0
    (x,y)=startgame['startgame']['startpos']
    if move=='up':
        xofset=0
        yofset=-1
    elif move=='down':
        xofset=0
        yofset=1
    elif move=='left':
        xofset=-1
        yofset=0
    elif move=='right':
        xofset=1
        yofset=0
    elif move==None:
        xofset=0
        yofset=0
    for i in range(len(startgame['startgame']['stars'])):
        (starx,stary)=startgame['startgame']['stars'][i]
        if (x+xofset,y+yofset)==startgame['startgame']['stars'][i]:
            if (starx+xofset,stary+yofset) in startgame['walls']:
                return False
            if (starx+xofset,stary+yofset) in startgame['startgame']['stars']:
                return False
            if (starx+xofset,stary+yofset) in startgame['goals']:
                match.play()
            startgame['startgame']['stars'][i]=(starx+xofset,stary+yofset)
    if (x+xofset,y+yofset) in startgame['walls']:
        return False
    startgame['startgame']['startpos']=(x+xofset,y+yofset)
    return True
def isWall(level,x,y):
    if x<0 or y<0 or x>len(level)-1 or y>len(level)-1:
        return False
    else:
        if level[x][y]=='#' or level[x][y]=='x':
            return True
    return False

def insidearea(level,x,y):
    if level[x][y]==' ':
        level[x][y]=='i'
    if x < len(level) - 1 and level[x+1][y]==' ':
        insidearea(level,x+1,y)
    if x < 1 and level[x-1][y]==' ':
        insidearea(level,x-1,y)
    if y < len(level) - 1 and level[x][y+1]==' ':
        insidearea(level,x,y+1)
    if x < 1 and level[x][y+1]==' ':
        insidearea(level,x,y-1)
def mapcomplete(level,startx,starty):
    levelcopy=copy.deepcopy(level['level'])
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy)):
            if levelcopy[x][y] in ('$','.','@','*'):
                levelcopy[x][y]=' '
    insidearea(levelcopy,startx,starty)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy[0])):
            if levelcopy[x][y] == '#':
                if (isWall(levelcopy, x, y-1) and isWall(levelcopy, x+1, y)) or \
                   (isWall(levelcopy, x+1, y) and isWall(levelcopy, x, y+1)) or \
                   (isWall(levelcopy, x, y+1) and isWall(levelcopy, x-1, y)) or \
                   (isWall(levelcopy, x-1, y) and isWall(levelcopy, x, y-1)):
                    levelcopy[x][y] = 'x'
    return levelcopy
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
                if len(levels[i])>maxwidth:
                    maxwidth=len(levels[i])
            for i in range(len(levels)):
                levels[i]+=' '*(maxwidth-len(levels[i]))
            for x in range(len(levels[0])):
                level.append([])
            for x in range(len(levels)):
                for y in range(maxwidth):
                    level[y].append(levels[x][y])
            originx=None
            originy=None
            goals=[]
            stars=[]
            walls=[]
            for x in range(maxwidth):
                for y in range(len(level[x])):
                    if level[x][y]=='@':
                        originx=x
                        originy=y
                    if level[x][y]=='$':
                        stars.append((x,y))
                    if level[x][y]=='.':
                        goals.append((x,y))
                    if level[x][y]=='#':
                        walls.append((x,y))
            startobj= {
                'startpos':(originx,originy),
                'steps':0,
                'stars':stars
                }  

            levelobj={
                'walls':walls,
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
    
def drawmap(levelobj,levelcopy,playerimg):
    level=levelobj['level']
    gamesurfwidth=len(level)*blockwidth
    gamesurfheight=(len(level[0])-1)*blockbaseheight+blockheight
    gamesurf=pygame.Surface((gamesurfwidth,gamesurfheight))
    gamesurf.fill(green)
    for x in range(len(level)):
        for y in range(len(levelcopy[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if levelcopy[x][y] in mapelement:
                block=mapelement[levelcopy[x][y]]
            gamesurf.blit(block,rect)
            if (x,y) in levelobj['goals']:
                if (x,y) in levelobj['startgame']['stars']:
                    gamesurf.blit(allimages['covered goal'],rect)
                else:
                    gamesurf.blit(allimages['uncovered goal'],rect)
            if (x,y) in levelobj['startgame']['stars']:
                gamesurf.blit(allimages['star'],rect)
            if (x,y)==levelobj['startgame']['startpos']:
                gamesurf.blit(playerimg,rect)
    return gamesurf
startscreen1()
#if __name__=='__main__':
#   main()
