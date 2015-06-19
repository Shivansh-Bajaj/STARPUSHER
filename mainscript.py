import random,copy,pygame,os,sys,time
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
    levelno=0
    screen=pygame.display.set_mode((screenwidth,screenheight))
    screen.fill(blue)
    allimages = {'uncovered goal': pygame.image.load('RedSelector.png').convert_alpha(),
                  'covered goal': pygame.image.load('Selector.png').convert_alpha(),
                  'star': pygame.image.load('Star.png').convert_alpha(),
                  'corner': pygame.image.load('Wall_Block_Tall.png').convert_alpha(),
                  'wall': pygame.image.load('Wood_Block_Tall.png').convert_alpha(),
                  'inside floor': pygame.image.load('Plain_Block.png').convert_alpha(),
                  'outside floor': pygame.image.load('Grass_Block.png').convert_alpha(),
                  'title': pygame.image.load('star_title.png').convert_alpha(),
                  'solved': pygame.image.load('star_solved.png').convert_alpha(),
                  'rock': pygame.image.load('Rock.png').convert_alpha(),
                  'short tree': pygame.image.load('Tree_Short.png').convert_alpha(),
                  'tall tree': pygame.image.load('Tree_Tall.png').convert_alpha(),
                  'ugly tree': pygame.image.load('Tree_Ugly.png').convert_alpha(),
                  }
    playerno=1
    player=[pygame.image.load('princess.png').convert_alpha(),
            pygame.image.load('boy.png').convert_alpha(),
            pygame.image.load('catgirl.png').convert_alpha(),
            pygame.image.load('horngirl.png').convert_alpha(),
            pygame.image.load('pinkgirl.png').convert_alpha()]
    global goal1
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
    global enelement,allimages,mapelement
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
                message_display('solved',(screenwidth/2,screenheight/2))
                pygame.event.wait()
                makemap(level,player,levelno,playerno)
        for event in pygame.event.get():
            move=None
            moved=False
            makemap(level,player,levelno,playerno)
            if event.type==KEYDOWN:
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
    backcopy=mapcomplete(level[levelno]['level'],startx,starty)
    mapsurf=drawmap(level[levelno],backmap,player[playerno])
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
            startgame['startgame']['stars'][i]=(starx+xofset,stary+yofset)
    if (x+xofset,y+yofset) in startgame['walls']:
        return False
    startgame['startgame']['startpos']=(x+xofset,y+yofset)
    return True
def mapcomplete(level,startx,starty):
    levelcopy=None
    levelcopy=copy.deepcopy(level)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy)):
            if levelcopy[x][y] in ('$','.','@','*'):
                levelcopy[x][y]=' '
    insidearea(levelcopy,startx,starty)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy[0])):
            if levelCopy[x][y] == '#':
                if (isWall(levelCopy, x, y-1) and isWall(levelCopy, x+1, y)) or \
                   (isWall(levelCopy, x+1, y) and isWall(levelCopy, x, y+1)) or \
                   (isWall(levelCopy, x, y+1) and isWall(levelCopy, x-1, y)) or \
                   (isWall(levelCopy, x-1, y) and isWall(levelCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'
    return levelcopy
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
def iswall(level,x,y):
    if x<0 or y<0 or x>len(level)-1 or y>len(level)-1:
        return False
    else:
        if level[x][y]=='#' or level[x][y]=='x':
            return True
    return False
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
    gamesurf.fill(blue)
    for x in range(len(level)):
        for y in range(len(levelcopy[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if levelcopy[x][y] in mapelement:
                block=mapelement[level[x][y]]
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
import random,copy,pygame,os,sys,time
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
    levelno=0
    screen=pygame.display.set_mode((screenwidth,screenheight))
    screen.fill(blue)
    allimages = {'uncovered goal': pygame.image.load('RedSelector.png').convert_alpha(),
                  'covered goal': pygame.image.load('Selector.png').convert_alpha(),
                  'star': pygame.image.load('Star.png').convert_alpha(),
                  'corner': pygame.image.load('Wall_Block_Tall.png').convert_alpha(),
                  'wall': pygame.image.load('Wood_Block_Tall.png').convert_alpha(),
                  'inside floor': pygame.image.load('Plain_Block.png').convert_alpha(),
                  'outside floor': pygame.image.load('Grass_Block.png').convert_alpha(),
                  'title': pygame.image.load('star_title.png').convert_alpha(),
                  'solved': pygame.image.load('star_solved.png').convert_alpha(),
                  'rock': pygame.image.load('Rock.png').convert_alpha(),
                  'short tree': pygame.image.load('Tree_Short.png').convert_alpha(),
                  'tall tree': pygame.image.load('Tree_Tall.png').convert_alpha(),
                  'ugly tree': pygame.image.load('Tree_Ugly.png').convert_alpha(),
                  }
    playerno=1
    player=[pygame.image.load('princess.png').convert_alpha(),
            pygame.image.load('boy.png').convert_alpha(),
            pygame.image.load('catgirl.png').convert_alpha(),
            pygame.image.load('horngirl.png').convert_alpha(),
            pygame.image.load('pinkgirl.png').convert_alpha()]
    global goal1
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
    global enelement,allimages,mapelement
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
                message_display('solved',(screenwidth/2,screenheight/2))
                pygame.event.wait()
                makemap(level,player,levelno,playerno)
        for event in pygame.event.get():
            move=None
            moved=False
            makemap(level,player,levelno,playerno)
            if event.type==KEYDOWN:
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
    backcopy=mapcomplete(level[levelno]['level'],startx,starty)
    mapsurf=drawmap(level[levelno],backmap,player[playerno])
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
            startgame['startgame']['stars'][i]=(starx+xofset,stary+yofset)
    if (x+xofset,y+yofset) in startgame['walls']:
        return False
    startgame['startgame']['startpos']=(x+xofset,y+yofset)
    return True
def mapcomplete(level,startx,starty):
    levelcopy=None
    levelcopy=copy.deepcopy(level)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy)):
            if levelcopy[x][y] in ('$','.','@','*'):
                levelcopy[x][y]=' '
    insidearea(levelcopy,startx,starty)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy[0])):
            if levelCopy[x][y] == '#':
                if (isWall(levelCopy, x, y-1) and isWall(levelCopy, x+1, y)) or \
                   (isWall(levelCopy, x+1, y) and isWall(levelCopy, x, y+1)) or \
                   (isWall(levelCopy, x, y+1) and isWall(levelCopy, x-1, y)) or \
                   (isWall(levelCopy, x-1, y) and isWall(levelCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'
    return levelcopy
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
def iswall(level,x,y):
    if x<0 or y<0 or x>len(level)-1 or y>len(level)-1:
        return False
    else:
        if level[x][y]=='#' or level[x][y]=='x':
            return True
    return False
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
    gamesurf.fill(blue)
    for x in range(len(level)):
        for y in range(len(levelcopy[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if levelcopy[x][y] in mapelement:
                block=mapelement[level[x][y]]
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
import random,copy,pygame,os,sys,time
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
    levelno=0
    screen=pygame.display.set_mode((screenwidth,screenheight))
    screen.fill(blue)
    allimages = {'uncovered goal': pygame.image.load('RedSelector.png').convert_alpha(),
                  'covered goal': pygame.image.load('Selector.png').convert_alpha(),
                  'star': pygame.image.load('Star.png').convert_alpha(),
                  'corner': pygame.image.load('Wall_Block_Tall.png').convert_alpha(),
                  'wall': pygame.image.load('Wood_Block_Tall.png').convert_alpha(),
                  'inside floor': pygame.image.load('Plain_Block.png').convert_alpha(),
                  'outside floor': pygame.image.load('Grass_Block.png').convert_alpha(),
                  'title': pygame.image.load('star_title.png').convert_alpha(),
                  'solved': pygame.image.load('star_solved.png').convert_alpha(),
                  'rock': pygame.image.load('Rock.png').convert_alpha(),
                  'short tree': pygame.image.load('Tree_Short.png').convert_alpha(),
                  'tall tree': pygame.image.load('Tree_Tall.png').convert_alpha(),
                  'ugly tree': pygame.image.load('Tree_Ugly.png').convert_alpha(),
                  }
    playerno=1
    player=[pygame.image.load('princess.png').convert_alpha(),
            pygame.image.load('boy.png').convert_alpha(),
            pygame.image.load('catgirl.png').convert_alpha(),
            pygame.image.load('horngirl.png').convert_alpha(),
            pygame.image.load('pinkgirl.png').convert_alpha()]
    global goal1
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
    global enelement,allimages,mapelement
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
                message_display('solved',(screenwidth/2,screenheight/2))
                pygame.event.wait()
                makemap(level,player,levelno,playerno)
        for event in pygame.event.get():
            move=None
            moved=False
            makemap(level,player,levelno,playerno)
            if event.type==KEYDOWN:
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
    backcopy=mapcomplete(level[levelno]['level'],startx,starty)
    mapsurf=drawmap(level[levelno],backmap,player[playerno])
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
            startgame['startgame']['stars'][i]=(starx+xofset,stary+yofset)
    if (x+xofset,y+yofset) in startgame['walls']:
        return False
    startgame['startgame']['startpos']=(x+xofset,y+yofset)
    return True
def mapcomplete(level,startx,starty):
    levelcopy=None
    levelcopy=copy.deepcopy(level)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy)):
            if levelcopy[x][y] in ('$','.','@','*'):
                levelcopy[x][y]=' '
    insidearea(levelcopy,startx,starty)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy[0])):
            if levelCopy[x][y] == '#':
                if (isWall(levelCopy, x, y-1) and isWall(levelCopy, x+1, y)) or \
                   (isWall(levelCopy, x+1, y) and isWall(levelCopy, x, y+1)) or \
                   (isWall(levelCopy, x, y+1) and isWall(levelCopy, x-1, y)) or \
                   (isWall(levelCopy, x-1, y) and isWall(levelCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'
    return levelcopy
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
def iswall(level,x,y):
    if x<0 or y<0 or x>len(level)-1 or y>len(level)-1:
        return False
    else:
        if level[x][y]=='#' or level[x][y]=='x':
            return True
    return False
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
    gamesurf.fill(blue)
    for x in range(len(level)):
        for y in range(len(levelcopy[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if levelcopy[x][y] in mapelement:
                block=mapelement[level[x][y]]
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
import random,copy,pygame,os,sys,time
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
    levelno=0
    screen=pygame.display.set_mode((screenwidth,screenheight))
    screen.fill(blue)
    allimages = {'uncovered goal': pygame.image.load('RedSelector.png').convert_alpha(),
                  'covered goal': pygame.image.load('Selector.png').convert_alpha(),
                  'star': pygame.image.load('Star.png').convert_alpha(),
                  'corner': pygame.image.load('Wall_Block_Tall.png').convert_alpha(),
                  'wall': pygame.image.load('Wood_Block_Tall.png').convert_alpha(),
                  'inside floor': pygame.image.load('Plain_Block.png').convert_alpha(),
                  'outside floor': pygame.image.load('Grass_Block.png').convert_alpha(),
                  'title': pygame.image.load('star_title.png').convert_alpha(),
                  'solved': pygame.image.load('star_solved.png').convert_alpha(),
                  'rock': pygame.image.load('Rock.png').convert_alpha(),
                  'short tree': pygame.image.load('Tree_Short.png').convert_alpha(),
                  'tall tree': pygame.image.load('Tree_Tall.png').convert_alpha(),
                  'ugly tree': pygame.image.load('Tree_Ugly.png').convert_alpha(),
                  }
    playerno=1
    player=[pygame.image.load('princess.png').convert_alpha(),
            pygame.image.load('boy.png').convert_alpha(),
            pygame.image.load('catgirl.png').convert_alpha(),
            pygame.image.load('horngirl.png').convert_alpha(),
            pygame.image.load('pinkgirl.png').convert_alpha()]
    global goal1
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
    global enelement,allimages,mapelement
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
                message_display('solved',(screenwidth/2,screenheight/2))
                pygame.event.wait()
                makemap(level,player,levelno,playerno)
        for event in pygame.event.get():
            move=None
            moved=False
            makemap(level,player,levelno,playerno)
            if event.type==KEYDOWN:
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
    backcopy=mapcomplete(level[levelno]['level'],startx,starty)
    mapsurf=drawmap(level[levelno],backmap,player[playerno])
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
            startgame['startgame']['stars'][i]=(starx+xofset,stary+yofset)
    if (x+xofset,y+yofset) in startgame['walls']:
        return False
    startgame['startgame']['startpos']=(x+xofset,y+yofset)
    return True
def mapcomplete(level,startx,starty):
    levelcopy=None
    levelcopy=copy.deepcopy(level)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy)):
            if levelcopy[x][y] in ('$','.','@','*'):
                levelcopy[x][y]=' '
    insidearea(levelcopy,startx,starty)
    for x in range(len(levelcopy)):
        for y in range(len(levelcopy[0])):
            if levelCopy[x][y] == '#':
                if (isWall(levelCopy, x, y-1) and isWall(levelCopy, x+1, y)) or \
                   (isWall(levelCopy, x+1, y) and isWall(levelCopy, x, y+1)) or \
                   (isWall(levelCopy, x, y+1) and isWall(levelCopy, x-1, y)) or \
                   (isWall(levelCopy, x-1, y) and isWall(levelCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'
    return levelcopy
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
def iswall(level,x,y):
    if x<0 or y<0 or x>len(level)-1 or y>len(level)-1:
        return False
    else:
        if level[x][y]=='#' or level[x][y]=='x':
            return True
    return False
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
    gamesurf.fill(blue)
    for x in range(len(level)):
        for y in range(len(levelcopy[x])):
            rect=pygame.Rect((x * blockwidth, y * blockbaseheight, blockwidth, blockheight))
            if levelcopy[x][y] in mapelement:
                block=mapelement[level[x][y]]
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
