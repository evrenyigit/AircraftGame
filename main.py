# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:00:28 2021

@author: evren
"""

import pygame
import winsound
import random
pygame.font.init()
pygame.init()
pygame.mixer.music.load('voice.wav') # Çalışmadı winsound ile başka bir ses ekledim

#Ekran ayarları
WIDTH=800
HEIGHT=650
Screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pirireis Aircraft Game")

Player= pygame.image.load("tank.png") #Ateş edeceğimiz image
Others = pygame.image.load("enemy.png") #Düşman image
Laser = pygame.image.load("bullet.png") #Ettiğimiz ateşi lazer olarak ayarladım
Background = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH,HEIGHT)) #arka plan :)

class Aircraft: #birinci classım bu classı hem uçak savar hem de uçaklar için kullanacağım
    
    COUNT = 30
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img=None
        self.bullet=None
        self.lasers = []
        self.lasers1 = []
        self.lasers2 = []
        self.counter=0
        
    def window(self,wind):
        wind.blit(self.img,(self.x,self.y))
        for laser in self.lasers:
            laser.window(wind)
        for laser1 in self.lasers1:
            laser1.window(wind)
        for laser2 in self.lasers2:
            laser2.window(wind)
            
        
    def Time(self):
        if self.counter >= self.COUNT:
            self.counter = 0
        elif self.counter > 0:
            self.counter += 1
        
        
class Anti_Aircraft(Aircraft): #Aircrafttaki bazı özellikleri yine kullanacağım için inherite ettim
    
    def __init__(self,x,y):
        
        super().__init__(x,y) #fonksiyonları tekrar yazmamıza gerek yok super() bu işi bizim için yapar
        self.img= Player
        self.bullet= Laser
        self.mask= pygame.mask.from_surface(self.img)
        
    def Boom(self):
        if self.counter==0:
            laser = Gun(self.x,self.y,self.bullet)
            self.lasers.append(laser)
            self.counter=1
            
    def Boom1(self):
        if self.counter==0:
            laser1 = Gun(self.x,self.y,self.bullet)
            self.lasers1.append(laser1)
            self.counter=1
            
    def Boom2(self):
        if self.counter==0:
            laser2 = Gun(self.x,self.y,self.bullet)
            self.lasers2.append(laser2)
            self.counter=1
        
    def moveLaser(self,vel,objs):
        self.Time()
        for laser in self.lasers:
            laser.move(vel)
            if laser.outOfScreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.outOfScreenn(WIDTH):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        frequency = 250
                        duration = 10  
                        winsound.Beep(frequency, duration)
                        #pygame.mixer.music.play(-1)
                #pygame.mixer.music.stop()
    def moveLaserLeft(self,vel,objs):
        self.Time()
        for laser1 in self.lasers1:
            laser1.moveleft(vel)
            if laser1.outOfScreenn(WIDTH):
                self.lasers1.remove(laser1)
            elif laser1.outOfScreenn(WIDTH):
                self.lasers1.remove(laser1)
            else:
                for obj in objs:
                    if laser1.collision(obj):
                        objs.remove(obj)
                        self.lasers1.remove(laser1)
                        frequency = 250  
                        duration = 10  
                        winsound.Beep(frequency, duration)
                       # pygame.mixer.music.play(-1)
                #pygame.mixer.music.stop()
                        
    def moveLaserRight(self,vel,objs):
        self.Time()
        for laser2 in self.lasers2:
            laser2.moveright(vel)
            if laser2.outOfScreenn(WIDTH):
                self.lasers2.remove(laser2)
            elif laser2.outOfScreenn(WIDTH):
                self.lasers2.remove(laser2)
            else:
                for obj in objs:
                    if laser2.collision(obj):
                        objs.remove(obj)
                        self.lasers2.remove(laser2)
                        frequency = 250  
                        duration = 10  
                        winsound.Beep(frequency, duration)

                       # pygame.mixer.music.play(-1)
               # pygame.mixer.music.stop()

class Enemy(Aircraft):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = Others
        self.mask = pygame.mask.from_surface(self.img)
        
    def move(self, velocity): #Vuracağımız uçakların hareket kontrolü
    
        self.x += velocity
        
class Gun:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=Laser
        self.mask = pygame.mask.from_surface(self.img)
        
    def window(self,wind):
        wind.blit(self.img,(self.x,self.y))
        
    def move(self, velocity):
        self.y += velocity
        
        #self.x += velocity
        
    def moveleft(self, velocity):
        self.x += velocity 
        self.y += velocity
        
    def moveright(self, velocity):
        self.x -= velocity 
        self.y += velocity
        
    def outOfScreen(self, height):
        return not(self.y < height and self.y > 0)
    
    def outOfScreenn(self, width):
        return not(self.x < width and self.x > 0)
    
    def collision(self, obj):
        return collide(self, obj)
    
def collide (obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main_menu(): #oyuna başlamak için arayüz menüsü gibi bir şey atamak istedim bu çeşitlendirilebilir
    starting_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        Screen.blit(Background , (0,0))
        starting_label = starting_font.render("Press the mouse to play",1,(255,255,255))
        Screen.blit(starting_label, (WIDTH/2 - starting_label.get_width()/2,500))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                
    pygame.quit()
    
def main():
    run = True
    lost = False
    lost_Count=0
    FPS = 60 #Oyunun hızı
    score = 0 
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    enemies = []
    times = 5
    enemy_vel = 1
    laser_vel = 5
    
    Bombarder=Anti_Aircraft(350,550)
    
    clock = pygame.time.Clock()
    
    def passing_screen():
        
        Screen.blit(Background,(0,0))
        lives_label = main_font.render(f"Lives : {lives}",3,(0,255,0))
        score_label = main_font.render(f"Score : {score}",0,(255,255,255))
        
        Screen.blit(lives_label, (WIDTH - score_label.get_width(),HEIGHT - score_label.get_height()-lives_label.get_height()))
        Screen.blit(score_label, (WIDTH - score_label.get_width(),HEIGHT - score_label.get_height()))
        
        for enemy in enemies:
            enemy.window(Screen)
            
        
        Bombarder.window(Screen)

        if lost:
            lost_label = lost_font.render("** You Lost **",2,(255,0,0))
            Screen.blit(lost_label, (WIDTH/2-lost_label.get_width()/2,HEIGHT/2))

        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        passing_screen()
        
        if lives <= 0:
            lost = True
            lost_Count+=1
            
        if lost:
            if lost_Count > 3: # Kaybettikten 3 saniye sonra program kapanacak
                run = False
            else:
                continue
            
        if len(enemies) == 0:
            times += 5
            for i in range(times):
                 # ekranın gözükmeyen sol tarafından random oluşan uçaklar gelecek
                enemy = Enemy(random.randrange(-1500,-100), random.randrange(50,HEIGHT-250))
                enemies.append(enemy)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        Bombarder.moveLaser(-laser_vel,enemies)
        Bombarder.moveLaserLeft(-laser_vel,enemies)
        Bombarder.moveLaserRight(-laser_vel,enemies)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            Bombarder.Boom()
        elif keys[pygame.K_a]:
            Bombarder.Boom1()
        elif keys[pygame.K_b]:
            Bombarder.Boom2()
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            #sürekli oluşup kalan objeler işlemciyi yorar bu yüzden bunları remove ediyorum
            #aynı zamanda kalan 3 canımın azalmasını da bu şekilde sayıyorum.
            if enemy.x + 90 > WIDTH: 
                lives -= 1
                enemies.remove(enemy)
           #◘ else:
            #    if enemies.remove(enemy):
             #       score+=10


                        
main_menu()

main()
                