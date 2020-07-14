# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:18:23 2020

@author: mrbeh
"""

#creating arenas for machine learning in pygame. 

import pygame
import numpy as np

pygame.init()

display_width = 800
display_height = 600
FPS = 30
black = (0,0,0)
white = (255,255,255)
green = (22,118,51)

dog_size = 100
speed = dog_size/10

stick_size = 150
stick_speed = stick_size/5

owner_size = 300
grass_number = 20


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Logan\'s Run')



clock = pygame.time.Clock()
crashed = False

#load all of the images for the logan animation and resize them to dog_size
logan_sit_img = pygame.image.load('logan_alpha.png')
logan_sit_img.convert_alpha()
logan_sit_img = pygame.transform.scale(logan_sit_img, (dog_size,dog_size))
logan_sit_img2 = pygame.image.load('logan two alpha.png')
logan_sit_img2.convert_alpha()
logan_sit_img2 = pygame.transform.scale(logan_sit_img2, (dog_size,dog_size))
logan_run_left_img = pygame.image.load('logan run left one alpha.png')
logan_run_left_img.convert_alpha()
logan_run_left_img = pygame.transform.scale(logan_run_left_img, (dog_size,dog_size))
logan_run_left_img2 = pygame.image.load('logan run left two alpha.png')
logan_run_left_img2.convert_alpha()
logan_run_left_img2 = pygame.transform.scale(logan_run_left_img2, (dog_size,dog_size))
logan_run_up_img = pygame.image.load('logan run up alpha.png')
logan_run_up_img.convert_alpha()
logan_run_up_img = pygame.transform.scale(logan_run_up_img, (dog_size,dog_size))
logan_run_up_img2 = pygame.image.load('logan run up two alpha.png')
logan_run_up_img2.convert_alpha()
logan_run_up_img2 = pygame.transform.scale(logan_run_up_img2, (dog_size,dog_size))
logan_run_down_img = pygame.image.load('logan run down alpha.png')
logan_run_down_img.convert_alpha()
logan_run_down_img = pygame.transform.scale(logan_run_down_img, (dog_size,dog_size))
logan_run_down_img2 = pygame.image.load('logan run down two alpha.png')
logan_run_down_img2.convert_alpha()
logan_run_down_img2 = pygame.transform.scale(logan_run_down_img2, (dog_size,dog_size))
logan_run_right_img = pygame.transform.flip(logan_run_left_img, True, False)
logan_run_right_img2 = pygame.transform.flip(logan_run_left_img2, True, False)

#load the images with logan and the stick
logan_stick_img = pygame.image.load('logan stick alpha.png')
logan_stick_img.convert_alpha()
logan_stick_img = pygame.transform.scale(logan_stick_img, (dog_size,dog_size))
logan_stick_img2 = pygame.image.load('logan two stick alpha.png')
logan_stick_img2.convert_alpha()
logan_stick_img2 = pygame.transform.scale(logan_stick_img2, (dog_size,dog_size))
logan_run_left_stick_img = pygame.image.load('logan run left one stick alpha.png')
logan_run_left_stick_img.convert_alpha()
logan_run_left_stick_img = pygame.transform.scale(logan_run_left_stick_img, (dog_size,dog_size))
logan_run_left_stick_img2 = pygame.image.load('logan run left two stick alpha.png')
logan_run_left_stick_img2.convert_alpha()
logan_run_left_stick_img2 = pygame.transform.scale(logan_run_left_stick_img2, (dog_size,dog_size))
logan_run_up_stick_img = pygame.image.load('logan run up alpha.png')
logan_run_up_stick_img.convert_alpha()
logan_run_up_stick_img = pygame.transform.scale(logan_run_up_stick_img, (dog_size,dog_size))
logan_run_up_stick_img2 = pygame.image.load('logan run up two alpha.png')
logan_run_up_stick_img2.convert_alpha()
logan_run_up_stick_img2 = pygame.transform.scale(logan_run_up_stick_img2, (dog_size,dog_size))
logan_run_down_stick_img = pygame.image.load('logan run down stick alpha.png')
logan_run_down_stick_img.convert_alpha()
logan_run_down_stick_img = pygame.transform.scale(logan_run_down_stick_img, (dog_size,dog_size))
logan_run_down_stick_img2 = pygame.image.load('logan run down two stick alpha.png')
logan_run_down_stick_img2.convert_alpha()
logan_run_down_stick_img2 = pygame.transform.scale(logan_run_down_stick_img2, (dog_size,dog_size))
logan_run_right_stick_img = pygame.transform.flip(logan_run_left_stick_img, True, False)
logan_run_right_stick_img2 = pygame.transform.flip(logan_run_left_stick_img2, True, False)

#download the images for the stick and michael
stick_img = pygame.image.load('stick alpha.png')
stick_img.convert_alpha()
stick_img = pygame.transform.scale(stick_img, (stick_size,stick_size))

michael_img = pygame.image.load('michael cartoon alpha.png')
michael_img.convert_alpha()
michael_img = pygame.transform.scale(michael_img, (100,150))

grass_img = pygame.image.load('grass1.png')
grass_img.convert_alpha()


class Dog:  
    def __init__(self):
        self.stick = False
    def move(self, direction,ticker,dog_x,dog_y):
        if direction == 9:
            if ticker % 15 <7:
                if self.stick == True:
                    gameDisplay.blit(logan_stick_img,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_sit_img,(dog_x,dog_y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_stick_img2,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_sit_img2,(dog_x,dog_y))
            #print('sitting')
        elif direction == 0:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_up_stick_img,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_up_img,(dog_x,dog_y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_up_stick_img2,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_up_img2,(dog_x,dog_y))
            #print('running up')
        elif direction == 1 or direction == 2 or direction == 3:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_right_stick_img,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_right_img,(dog_x,dog_y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_right_stick_img2,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_right_img2,(dog_x,dog_y))
            #print('running left')
        elif direction == 4:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_down_stick_img,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_down_img,(dog_x,dog_y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_down_stick_img2,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_down_img2,(dog_x,dog_y))
            #print('running down')
        elif direction == 5 or direction == 6 or direction == 7:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_left_stick_img,(dog_x,dog_y))
                else: 
                    gameDisplay.blit(logan_run_left_img,(dog_x,dog_y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_left_stick_img2,(dog_x,dog_y))
                else: 
                   gameDisplay.blit(logan_run_left_img2,(dog_x,dog_y))
            #print('running right')
class Stick:
    def move(self, x, y):
        gameDisplay.blit(stick_img,(x,y))

class Owner:
    def move(self,x,y):
        gameDisplay.blit(michael_img,(x,y))
        
class Grass:
    def __init__(self):
        self.grass_x = np.random.uniform(0,display_width,grass_number)
        self.grass_y = np.random.uniform(0,display_height,grass_number)
    
    def place(self,ticker):
        for i in range(grass_number):
             gameDisplay.blit(grass_img,(self.grass_x[i],self.grass_y[i]))
       
logan = Dog()
stick = Stick()  
michael = Owner()
grass = Grass()    
dog_x = (display_width*0.2)
dog_y = display_height*0.8

fetch_count = 0
x_change = 0
y_change = 0
#car_speed = 0
direction = 9
ticker = 0
stick_x = (display_width*0.45)
stick_y = display_height*0.45
owner_x = (display_width*0.1)
owner_y = display_height*0.7

font = pygame.font.Font('freesansbold.ttf', 32) 
font2 = pygame.font.Font('freesansbold.ttf', 24) 
  
# create a text suface object, 
# on which text is drawn on it. 
text = font.render(f"Sticks Fetched: {fetch_count}", True, black, white) 
good_boy_text = font.render('Good Boy = True', True, black, white)  
# create a rectangular object for the 
# text surface object 
textRect = text.get_rect()  
good_boy_Rect = good_boy_text.get_rect() 
  
# set the center of the rectangular object. 
textRect.center = (display_width // 2, display_height // 2) 
good_boy_Rect.center = (display_width // 2, display_height // 2) 
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)
            '''
        [button1, button2, button3] = pygame.mouse.get_pressed()
        if button1 == True:
            [stick_x,stick_y] = pygame.mouse.get_pos()
            stick_x = stick_x - stick_size/2
            stick_y = stick_y - stick_size/2
            '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            direction = 4
            x_change = 0
            y_change = speed
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            direction = 5
            x_change = -speed
            y_change = speed
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            direction = 3
            x_change = speed
            y_change = speed
            
        elif keys[pygame.K_UP] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            direction = 0
            x_change = 0
            y_change = -speed
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            direction = 7
            x_change = -speed
            y_change = -speed
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            direction = 1
            x_change = speed
            y_change = -speed
        elif keys[pygame.K_LEFT]:
            direction = 6
            x_change = -speed
            y_change = 0
        elif keys[pygame.K_RIGHT]:
            direction = 2
            x_change = speed
            y_change = 0
        else:
            direction = 9
            x_change = 0
            y_change = 0

             
    dog_x += x_change
    dog_y += y_change 
    if dog_x > display_width-dog_size:
        dog_x = display_width-dog_size
    if dog_x < 0:
        dog_x = 0
    if dog_y > display_height-dog_size:
        dog_y = display_height-dog_size
    if dog_y < 0:
        dog_y = 0
    ticker += 1
    
    
    gameDisplay.fill(green)
    grass.place(ticker) 
    text = font.render(f"Sticks Fetched: {fetch_count}", True, black, white)
    gameDisplay.blit(text, (0,0))     
    debug_text = font2.render(f"dog: ({dog_x},{dog_y},  stick: ({stick_x},{stick_y})", True, black, white)
    gameDisplay.blit(text, (0,0))
    #gameDisplay.blit(debug_text, (0,100))
    gameDisplay.blit(good_boy_text, (0,50))    
    if abs((dog_x)-(stick_x)) < 30 and abs((dog_y)-(stick_y)) < 30:
        logan.stick = True
    if abs(dog_x-owner_x) < 50 and abs(dog_y-owner_y) < 50:
        if logan.stick == True:
            stick_x = np.random.randint(display_width-display_width/2,display_width-100)
            stick_y = np.random.randint(0,display_height-display_height/2)
            stick.move(stick_x, stick_y)
            fetch_count += 1
        logan.stick = False
        
    if logan.stick == True:
        stick_x = 1000
        stick_y = 1000
    michael.move(owner_x,owner_y)
    stick.move(stick_x,stick_y)
    logan.move(direction,ticker,dog_x,dog_y)
         
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
