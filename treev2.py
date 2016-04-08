import pygame, sys, math, random, time
from pygame.locals import*

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
#set up window
windowX = 720
windowY = 480
DISPLAYSURF = pygame.display.set_mode((windowX,windowY))

pygame.display.set_caption('TREEEE')

#set up colors

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)

points = [] #all growing and dead points stored here

shade = pygame.Surface((windowX,windowY)) #bake a transparent surface
shade.fill(BLACK)
shade.set_alpha(5)


def green():
     '''returns a random shade of green'''
     return (0,random.randint(100,255), 0)
def leaf(point):
     '''makes a leaf at point location'''
     size = 10 #change this for leafe size
     width = 4 #change this for leafe width
     a,b = point[0], point[1]
     angle = random.random()*math.pi*2
     c = a+ math.cos(angle)*size
     d = b+ math.sin(angle)*size
     pygame.draw.line(DISPLAYSURF,green(),(a,b),(c,d),width)
     
def split(point):
     '''splits a branch'''
     point[4] = False
     amt = [2,2,2,2,2,2,3] #variability in branching
     a = random.choice(amt)
     for _ in range(a): 
          x, y = point[0], point[1]
          angle = random.random()*math.pi/2 + math.pi/4
          size = point[3]/a
          c = point[5]
          points.append([x,y, angle, size, True, c])
          
def grow(point):
     '''grows a branch'''
     if point[4]: #checks if it should grow
          angle = point[2]
          if random.random() < .5:
               #range [0,1] change to set rate of winding
               angle += random.random()*math.pi/15 - math.pi/30
          if angle < 0: angle = 0
          if angle > math.pi : angle = math.pi
          point[2] = angle
          
          point[0] += math.cos(angle)*1
          point[1] -= math.sin(angle)*1
          if point[3] <=3 and random.random() < (0.3 - point[3]/10):
               #range [0,1] change to set rate of leafing
               leaf(point)
               pass
          if random.random() < .007:
               #range [0,1] change to set rate of new branches forming
               split(point)
          if random.random() < .02 and point[3] < 1.1:
               #range [0,1] change to set rate of death
               point[4] = False
          point[3]*= 0.998 # makes branch a bit smaller
          
          return 1 # for dings
     return 0
def draw(point):
     '''draws a branch'''
     if point[4]: #checks if it should grow
          p, r = (int(point[0]),int(point[1])), int(point[3])
          pygame.draw.circle(DISPLAYSURF,point[5],p,r)
                   


DISPLAYSURF.fill(BLACK)
while True: ##main game loop
     
     ding = 0
     for _ in range(10):
          for p in points:
               #kill branch if out of bounds
               if  -20 > p[0] > windowX+20 or -20> p[1]: p[4] = False
               ding += grow(p)
               draw(p)
##     if random.random() < 0.1 and ding:
##               DISPLAYSURF.blit(shade,(0,0))
##     print('ding:',ding)
     for event in pygame.event.get():
          if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                    DISPLAYSURF.blit(shade,(0,0))
                    for _ in range(3):
                         mposX, mposY = pygame.mouse.get_pos()
                         angle = random.random()*math.pi/2 + math.pi/4
                         size = 10
                         c = random.randint(10,45) #makes a shade of brown
                         points.append([mposX,mposY, angle, size, True, (c+100,c,c)])
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
     pygame.display.update()
     fpsClock.tick(FPS)
