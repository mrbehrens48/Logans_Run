# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:18:23 2020
this one shows every 1000th episode as it trains the q-table.
@author: mrbeh
"""

#creating arenas for machine learning in pygame. 

import pygame
import numpy as np
import matplotlib.pyplot as plt # for plotting stuff
import pickle #for saving files (the Q-table in this case)
from matplotlib import style #for makeing the plots pretty
import time #for keeping track of saved Q tables

style.use("ggplot")

pygame.init()

SIZE = 10 #size of the environment (10x10 square)
HM_EPISODES = 10000 #number of playthroughs used for training
MOVE_PENALTY = 1 #the penalty for taking a movement action
FETCH_REWARD = 500 #the reward for getting to the food!
COLLECT_REWARD = 200

EPS_DECAY = 0.9999 #epsilon will decay over time, so that we transition from an explore to exploit phenotype


start_q_table = None #if we have a table we want to load, this should be the file name instead of NONE
#start_q_table = 'qtable-1587118803.pickle'
epsilon = 0.5 #to choose random actions
#epsilon = 0
SHOW_EVERY = 1000 #render the environment every 1000 games, so we can see what is happening
#SHOW_EVERY = 1

LEARNING_RATE = 0.1 #q parameter
DISCOUNT = 0.95 #preference for future rather than immediate reward

display_width = 1000
display_height = 1000
FPS = 10
black = (0,0,0)
white = (255,255,255)
green = (22,118,51)

dog_size = 100
dog_speed = display_width/SIZE

stick_size = 150
stick_speed = display_width/SIZE

owner_size = 300
grass_number = 20

bin_size = display_width/SIZE


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
        self.x = 0
        self.y = 0
        self.direction = 0
    def __sub__(self,other):
        return (self.x-other.x, self.y-other.y)
    def action(self,action):
        if action == 4:
            self.direction = 4
            x_change = 0
            y_change = dog_speed
        elif action == 5:
            self.direction = 5
            x_change = -dog_speed
            y_change = dog_speed
        elif action == 3:
            self.direction = 3
            x_change = dog_speed
            y_change = dog_speed
            
        elif action == 0:
            self.direction = 0
            x_change = 0
            y_change = -dog_speed
        elif action == 7:
            self.direction = 7
            x_change = -dog_speed
            y_change = -dog_speed
        elif action == 1:
            self.direction = 1
            x_change = dog_speed
            y_change = -dog_speed
        elif action == 6:
            self.direction = 6
            x_change = -dog_speed
            y_change = 0
        elif action == 2:
            self.direction = 2
            x_change = dog_speed
            y_change = 0
        else:
            self.direction = 9
            x_change = 0
            y_change = 0

        self.x += x_change
        self.y += y_change 
        if self.x > display_width-dog_size:
            self.x = display_width-dog_size
        if self.x < 0:
            self.x = 0
        if self.y > display_height-dog_size:
            self.y = display_height-dog_size
        if self.y < 0:
            self.y = 0
            
    def move(self,ticker):
        if self.direction == 9:
            if ticker % 15 <7:
                if self.stick == True:
                    gameDisplay.blit(logan_stick_img,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_sit_img,(self.x,self.y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_stick_img2,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_sit_img2,(self.x,self.y))
            #print('sitting')
        elif self.direction == 0:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_up_stick_img,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_up_img,(self.x,self.y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_up_stick_img2,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_up_img2,(self.x,self.y))
            #print('running up')
        elif self.direction == 1 or self.direction == 2 or self.direction == 3:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_right_stick_img,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_right_img,(self.x,self.y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_right_stick_img2,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_right_img2,(self.x,self.y))
            #print('running left')
        elif self.direction == 4:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_down_stick_img,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_down_img,(self.x,self.y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_down_stick_img2,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_down_img2,(self.x,self.y))
            #print('running down')
        elif self.direction == 5 or self.direction == 6 or self.direction == 7:
            if ticker % 10 <4:
                if self.stick == True:
                    gameDisplay.blit(logan_run_left_stick_img,(self.x,self.y))
                else: 
                    gameDisplay.blit(logan_run_left_img,(self.x,self.y))
            else:
                if self.stick == True:
                    gameDisplay.blit(logan_run_left_stick_img2,(self.x,self.y))
                else: 
                   gameDisplay.blit(logan_run_left_img2,(self.x,self.y))
            #print('running right')
   
class Stick:
    def __init__(self):
        self.x = 0
        self.y = 0
    def __sub__(self,other):
        return (self.x-other.x, self.y-other.y)
    def move(self):
        gameDisplay.blit(stick_img,(self.x,self.y))

class Owner:
    def __init__(self):
        self.x = 0
        self.y = 0
    def __sub__(self,other):
        return (self.x-other.x, self.y-other.y)
    def move(self):
        gameDisplay.blit(michael_img,(self.x,self.y))
        
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
logan.direction = 9
ticker = 0
stick.x = (display_width*0.45)
stick.y = display_height*0.45
michael.x = (display_width*0.1)
michael.y = display_height*0.7
fetch = False
collect = False

def reset():  
    logan.x = (display_width*0.2)
    logan.y = display_height*0.8
    logan.direction = 9
    ticker = 0
    stick.x = np.random.randint(display_width-display_width/2,display_width-100)
    stick.y = np.random.randint(0,display_height-display_height/2)
    michael.x = (display_width*0.1)
    michael.y = display_height*0.7
    fetch = False
    collect = False
    reward = 0
 

if start_q_table is None:
    #initialize the Q table
    q_table = {}
    for i in range(-SIZE,SIZE):
        for ii in range(-SIZE,SIZE):
            for iii in range(-SIZE,SIZE):
                for iv in range(-SIZE,SIZE):
                    q_table[((i,ii),(iii,iv))]= [np.random.uniform(-10,0) for i in range(10)]
                    
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

episode_rewards = [] #this will track the rewards achieved each epidose
reset()

font = pygame.font.Font('freesansbold.ttf', 32) 
font2 = pygame.font.Font('freesansbold.ttf', 24) 
  




########Begin the training                    
for episode in range(HM_EPISODES):
    reset()
    episode_reward = 0
    
    if episode % SHOW_EVERY == 0:
        print(f"on #{episode}, epsilon is {epsilon}")
        print(f"{SHOW_EVERY} ep mean score: {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False
    
    #show = True
    for i in range (200):
        
        obs = (tuple(np.round_(np.divide((logan-michael),bin_size))), tuple(np.round_(np.divide((logan-stick),bin_size)))) 
        if show == True:
            event = pygame.event.get()
            #keys = pygame.key.get_pressed()
        if np.random.random() > epsilon:
            #get the action
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0,8)
        #take the action
        logan.action(action)
    
        ticker += 1
        
        #if logan runs into the stick, give hime the stick
        if abs((logan.x)-(stick.x)) < 100 and abs((logan.y)-(stick.y)) < 100:
                logan.stick = True
                collect = True
        #if logan runs into michael, and he has the stick, take the stick, add to the fetch count, and throw the stick to a new location
        if abs(logan.x-michael.x) < 100 and abs(logan.y-michael.y) < 100:
            if logan.stick == True:
                stick.x = np.random.randint(display_width-display_width/2,display_width-100)
                stick.y = np.random.randint(0,display_height-display_height/2)
                #stick.move(stick_x, stick_y)
                fetch_count += 1
                fetch = True
            logan.stick = False
            
                
        if logan.stick == True: #if logan has the stick, get the stick off the screen
            stick.x = 1000
            stick.y = 1000
        
        #DISTROBUTE REWARDS
        if fetch == True: 
            reward = FETCH_REWARD
            fetch = False
        elif collect == True:
            reward = COLLECT_REWARD
            collect = False
        else:
            reward = -MOVE_PENALTY
            
        if show == True:
            gameDisplay.fill(green)
            grass.place(ticker) 
            text = font.render(f"Sticks Fetched: {fetch_count}", True, black, white)
            gameDisplay.blit(text, (0,0))     
            debug_text = font2.render(f"episode: {episode},  reward: {episode_reward}", True, black, white)
            text = font.render(f"Sticks Fetched: {fetch_count}", True, black, white) 
            good_boy_text = font.render('Good Boy = True', True, black, white)  
            gameDisplay.blit(text, (0,0))
            gameDisplay.blit(debug_text, (0,100))
            gameDisplay.blit(good_boy_text, (0,50))
            michael.move()
            stick.move()
            logan.move(ticker)
            pygame.display.update()
            clock.tick(FPS) 
        #new_obs = ((logan-michael), (logan-stick))
        new_obs = (tuple(np.round_(np.divide((logan-michael),bin_size))), tuple(np.round_(np.divide((logan-stick),bin_size)))) 
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]    
        
        if reward == FETCH_REWARD:
            new_q = FETCH_REWARD
        else:
            new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q
        
        episode_reward += reward
        if reward == FETCH_REWARD:
            break
    print(f"episode: {episode}, score: {episode_reward}")
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY


moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode = 'valid')
plt.plot([i for i in range(len(moving_avg))],moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle","wb") as f:
    pickle.dump(q_table,f)
    
    
pygame.quit()
quit()
