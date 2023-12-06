import pygame
import random as rd
import setting as st
import math 
from pygame import mixer
screen = pygame.display.set_mode((st.screen_width,st.screen_length))

#someFunction
def isCollision(x,y,u,v):
    if math.sqrt((x-u)*(x-u) + (y-v)*(y-v)) <= 40:
        return True
    return False

#player
playerImg = pygame.image.load("player.png")
class Player:
    def __init__(self):
        self.x = st.playerX
        self.y = st.playerY
        self.xChange = 0
        self.yChange = 0
    def move(self,movement):
        if movement == "left":
            self.xChange = -st.playerSpeed
        elif movement ==  "right":
            self.xChange = st.playerSpeed
        elif movement == "up":
            self.yChange = -st.playerSpeed
        elif movement ==  "down":
            self.yChange = st.playerSpeed
        elif movement == "xStop":
            self.xChange = 0
        elif movement == "yStop":
            self.yChange = 0
    def rePosition(self):
        self.x += self.xChange
        self.y += self.yChange
    def showPosition(self):
        screen.blit(playerImg,(self.x,self.y))
        
##bulletUp
bulletUpImg = pygame.image.load("bulletUp.png")
class BulletUp:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.yChange = 0
        self.bullet_state = "ready"
    def shoot(self):
        if self.bullet_state == "ready":
            self.yChange = -st.bulletSpeed
            self.bullet_state = "shoot"
        elif self.bullet_state == "shoot":
            if self.y <= 0:
                self.bullet_state = "ready"
    def rePosition(self):
        self.y += self.yChange
    def showPosition(self):
        screen.blit(bulletUpImg,(self.x,self.y))

##bulletDown
bulletDownImg = pygame.image.load("bulletDown.png")

#enemy
enemyImg = pygame.image.load("enemy.png")
class Enemy:
    def __init__(self,x,y):
        self.bulletPos = 0
        self.bulletState = "ready"
        self.x = x 
        self.y = y
        self.shootingFlag = rd.randint(0,300)
        self.state = "alive"
  
    def rePosition(self):
        self.y += st.enemySpeed
    def showPosition(self):
        screen.blit(enemyImg,(self.x,self.y))
    def shootingPosition(self):
        if self.bulletState == "ready":
            screen.blit(bulletDownImg,(self.x,self.y))
        else:
            self.bulletPos += st.bulletDownSpeed
            screen.blit(bulletDownImg,(self.x,self.bulletPos))

#Initilize objects
player = Player()
bulletUp = []
for i in range(st.numberOfBullet):
    bulletUp.append(BulletUp(player.x,player.y))

enemy = []
for i in range(st.numberOfEnemy):
    enemy.append(Enemy(1000,1000))

#text
pygame.font.init()
score = 0
score_font = pygame.font.Font("freesansbold.ttf",32)
def showScore(x,y):
    scoreText = score_font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(scoreText,(x,y))

#sound
pygame.mixer.init()
backgroundSound = mixer.Sound("background.wav")
backgroundSound.set_volume(0.2)
backgroundSound.play(-1)   #play in a loop

explosionSound = mixer.Sound("explosion.wav")
shootSound = mixer.Sound("shoot.wav")

backgroundImg = pygame.image.load("backgroundpic.jpg")

running = True
while running:
    screen.blit(backgroundImg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move("left")
            elif event.key == pygame.K_RIGHT:
                player.move("right")
            elif event.key == pygame.K_UP:
                player.move("up")
            elif event.key == pygame.K_DOWN:
                player.move("down")
            elif event.key == pygame.K_SPACE:
                for i in range(st.numberOfBullet):
                    if bulletUp[i].bullet_state == "ready":
                        bulletUp[i].shoot()
                        shootSound.play()
                        break
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.move("xStop")
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.move("yStop")
    
    for i in range(st.numberOfBullet):
        if bulletUp[i].bullet_state == "ready":
            bulletUp[i].__init__(player.x,player.y)
        elif bulletUp[i].bullet_state == "shoot":
            bulletUp[i].shoot()
        bulletUp[i].rePosition()
        bulletUp[i].showPosition()
    
    for i in range(st.numberOfEnemy):
        if enemy[i].state == "dead":
            enemy[i].__init__(rd.randint(0,950),st.enemyY)
        elif enemy[i].state == "alive":
            for j in range(st.numberOfBullet):
                if (isCollision(enemy[i].x,enemy[i].y,bulletUp[j].x,bulletUp[j].y) and bulletUp[j].bullet_state == "shoot"): 
                    enemy[i].state = "dead"
                    score += 1
                    explosionSound.play()
                if enemy[i].y >= 1000:
                    enemy[i].state = "dead"
        if enemy[i].state == "alive":
            if int(enemy[i].y) == enemy[i].shootingFlag:
                enemy[i].bulletState = "shoot"
                enemy[i].bulletPos = enemy[i].y
            if isCollision(player.x,player.y,enemy[i].x,enemy[i].y):
                explosionSound.play()
                running = False
        if enemy[i].bulletState == "shoot":
            if isCollision(player.x,player.y,enemy[i].x,enemy[i].bulletPos):
                explosionSound.play()
                running = False
        
        enemy[i].shootingPosition() 
        enemy[i].showPosition()
        enemy[i].rePosition()     
    
    showScore(10,10)
    player.rePosition()
    player.showPosition()
    
    pygame.display.update()