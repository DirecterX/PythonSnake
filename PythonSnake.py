import pygame
import random
import sys
import os
from configparser import ConfigParser


class Node:
    def __init__(self,data,next=None):
        self.data = data 
        if next is not None:
            self.next = next
        else :
            self.next = None
    def getData(self):
        return self.data
    def getNext(self):
        return self.next
    def setData(self,data):
        self.data = data
    def setNext(self,next):
        self.next = next

class LinkedList:
    def __init__(self,head=None):
        if head is None:
            self.head = None
            self.tail = None
            self.size = 0
        else:
            self.head = head
            t = self.head
            self.size = 1
            while t.next is not None:
                    t = t.next
                    self.size +=1
                    self.tail = t
    
    def __str__(self):
        s = ""
        h = self.head
        while h is not None:
            if h.next is not None:
                s += str(h.data)+","
            else :
                s += str(h.data)+""
            h = h.next   
        if self.SizeLL()==0:
            s="List is empty"
        return s

    def isEmpty(self):
        return self.size == 0

    def SizeLL(self):
        return self.size

    def append(self, data):
        p = Node(data)
        if self.head is None:
            self.head = p
        else:
            t = self.head
            while t.next is not None:
                t=t.next
            t.next = p
        self.size+=1

    def ConvertToArr(self):
        lenght = self.SizeLL()
        Arr = []
        Current = self.head 
        while (Current != None):
            Arr.append(Current.data)
            Current = Current.next

        return Arr
        
    def DeleteFirstNode(self):
        temp = self.head
        self.head = self.head.next
        temp = None

    def FindLenght(self):
        current = self.head
        count = 0
        while (current != None):
            count = count + 1
            current = current.next
        return count

class InsertionSort:
    def sort(self,array):
        count = 0
        for i in range(1,len(array)):
            current = array[i]
            j = i - 1
            while (j >= 0 and current > array[j]):
                array[j+1] = array[j]
                j -= 1
                count += 1
                #print(j,array)
            array[j+1] = current

class GamePage:
    def __init__(self):
        self.gameStart = False
        self.gameOver = False
        self.hardMode = False
        self.ranking = False
    def getGameStart(self):
        return self.gameStart
    def getGameOver(self):
        return self.gameOver
    def getHardMode(self):
        return self.hardMode
    def getRanking(self):
        return self.ranking    
    def setGameStart(self,value):
        self.gameStart = value
    def setGameOver(self,value):
        self.gameOver = value
    def setHardMode(self,value):
        self.hardMode = value
    def setRanking(self,value):
        self.ranking = value




# Loading Config 
config_object = ConfigParser()
config_object.read('setting.ini')
setting = config_object["GAMESETTING"]
ranking = config_object["RANKING"]

def resource_path(relative_path): #สำหรับเรียกpathที่อยู่ในโฟลเดอร์เดียวกันจากที่ไหนก็ได้ 
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()
gp = GamePage()

# Colors
white = (255, 255, 255) # rgb format
red = (255, 0, 0)
black = (0, 0, 0)
bGreen = (50, 60, 23)

# Game window
screen_width = int(setting["width"])
screen_height = int(setting["height"])
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bg_url = resource_path('resource/bg.png')
main_url = resource_path('resource/Main.png')
ranking_url = resource_path('resource/ranking.png')
gameOver_url = resource_path('resource/gameover.png')
icon_url = resource_path('resource/icon.png')



bg_game = pygame.image.load(bg_url)
Main_Bg = pygame.image.load(main_url)
ranking_Bg = pygame.image.load(ranking_url)
gameOver_Bg = pygame.image.load(gameOver_url)
img_icon = pygame.image.load(icon_url)
pygame.display.set_icon(img_icon)

# Game Title
pygame.display.set_caption("Python Snake")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 35)



def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

# -----------Draw snake body on screen (Read value from linked list)------------------*********************************
def draw_sneak(gameWindow, color, snake_body, snake_size): 
    snake = snake_body.head
    while snake.next != None:
        x = snake.data[0] #  x,y in snake_body:
        y = snake.data[1]  
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size]) # draw sneak
        snake = snake.next # เลื่อนไป Node ต่อไป
    else: # กรณีเริ่มเกม next node = None
        x = snake.data[0] #  x,y in snake_body:
        y = snake.data[1]  
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size]) # draw sneak

#--- Check score is on Ranking ? ---
def CheckScore(score):
    #--- reading ranking score from file---
    first = int(ranking["first"])
    second = int(ranking["second"])
    third = int(ranking["third"])
    #--- Checking score ----
    if score > first or score > second or score > third:         
        return True
    else:
        return False

#------ Ranking Score (Insertion Sort)-----*******************************************************
def sortScore(score):
    #--- reading ranking score from file---
    first = int(ranking["first"])
    second = int(ranking["second"])
    third = int(ranking["third"])

    if score > first or score > second or score > third:
         #--- append value to List ---
        arrScore = []
        arrScore.append(first)
        arrScore.append(second)
        arrScore.append(third)
        arrScore.append(score)

        #--- create object for sort--
        sortedScore = InsertionSort()
        sortedScore.sort(arrScore)

        #---Write Ranking score to File ---
        ranking["first"] = str(arrScore[0])
        ranking["second"] = str(arrScore[1])
        ranking["third"] = str(arrScore[2])

        with open('setting.ini', 'w') as conf:
            config_object.write(conf)

        return True
    else:
        return False

def button(screen, position, text):
    font = pygame.font.SysFont('Arial', 35)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (200, 200, 200), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (200, 200, 200), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (200, 200, 200), (x, y, w , h))
    return screen.blit(text_render, (x, y))


# Game Loop
def gameloop():
    exit_game = False
    game_over = gp.gameOver
    hard_mode = gp.hardMode
    game_start = gp.gameStart
    snake_x = 55
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_body = LinkedList()
    snake_length = 1

    food_x = random.randint(20, screen_width-20)
    food_y = random.randint(60, screen_height -20)
    score = 0
    init_velocity = int(setting["velocity"])
    snake_size = 30 
    fps = 60   # frames per sec
    while not exit_game:
        #-------------GAME OVER----------------#
        if gp.getGameOver():
            #gameWindow.fill(white)
            gameWindow.blit(gameOver_Bg,[0,0])
            #text_screen("Game Over!", red, 315, 100)
            text_screen("Your Score : "+str(score*10), red, 300, 170)
            #text_screen("Retry : 'Enter'", red, 50, 500)
            if CheckScore(score*10):
                text_screen("You are on Ranking !!", red, 250, 240)
            
            b1 = button(gameWindow, (330, 500), "Retry")
            b2 = button(gameWindow, (480, 500), "Menu")


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sortScore(score*10)
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        sortScore(score*10)
                        gp.setGameStart(True)
                        gp.setGameOver(False)
                        gameloop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if b1.collidepoint(pygame.mouse.get_pos()):
                        sortScore(score*10)
                        gp.setGameStart(True)
                        gp.setGameOver(False)
                        gameloop()
                    if b2.collidepoint(pygame.mouse.get_pos()):
                        sortScore(score*10)                   
                        gp.setGameStart(False)
                        gp.setGameOver(False)
                        gp.setRanking(False)
                        gameloop()

        #---------------GAME START----------------------
        elif gp.getGameStart(): 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_ESCAPE:                   
                        gp.setGameStart(False)
                        gp.setGameOver(False)
                        gp.setRanking(False)

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20: # เงื่อนไขกินอาหาร 25 = Hitbox เวลากินอาหาร
               
                #--Hard Mode--
                if gp.getHardMode():
                    score +=2   # เพิ่มคะแนนเมื่อกินอาหารได้
                    init_velocity+=0.5  #เพิ่ม speed งูทุกครั้งที่กิน
                #--Normal Mode --
                else:
                     score +=1 # เพิ่มคะแนนเมื่อกินอาหารได้

                food_x = random.randint(20, screen_width - 30)  # Random ตำแหน่งอาหารใหม่ เมื่ออาหารถูกกิน
                food_y = random.randint(60, screen_height - 30)
                snake_length +=5      #เพิ่มความยาวของงูเมื่อกินอาหารได้  <<-- BigO = 5(n)+2(หัวและหาง ตอนเริ่ม)

            gameWindow.blit(bg_game,[0,0])
            text_screen("Score: " + str(score * 10), red, 650, 5)  # Update คะแนนเมื่อกิน
            pygame.draw.rect(gameWindow, red, [food_x, food_y, 20, 20]) # วาดอาหารลงบนจอ
            #pygame.draw.circle(gameWindow, red, (food_x, food_y), 10)
            pygame.draw.line(gameWindow, black, (0,40), (900,40),5)


            Create_Body = []  # สร้างร่างงูเพิ่ม
            Create_Body.append(int(snake_x)) #ใส่ตำแหน่ง x,y ที่สร้าง
            Create_Body.append(int(snake_y))
            snake_body.append(Create_Body) # นำที่สร้างใส่ร่างงูที่สร้างเพิ่ม ใส่ Linked List
            

            #print(snake_body)
            if snake_body.FindLenght()>snake_length:  #เงื่อนไขเช็คกันการสร้างงูยาวเกินขนาดปัจจุบัน 
                snake_body.DeleteFirstNode()

            if Create_Body in snake_body.ConvertToArr()[:-1]:
                gp.setGameOver(True)
                gp.setGameStart(False) 
                #game_over = True
                #game_start = False

            if snake_x<0 or snake_x>screen_width-20 or snake_y<50 or snake_y>screen_height-20:
                gp.setGameOver(True)
                gp.setGameStart(False) 
                #game_over = True
                #game_start = False
            draw_sneak(gameWindow, bGreen, snake_body, snake_size) #Drawing Snake body
       
       #---------------Ranking---------------------------
        elif gp.getRanking():
            gameWindow.blit(ranking_Bg,[0,0])
            #gameWindow.fill(white)
            first = ranking["first"]
            second = ranking["second"]
            third = ranking["third"]

            #text_screen("Leader Board", red, 315, 100)
            text_screen("1st  : "+first, red, 350, 185)
            text_screen("2nd : "+second, red, 350, 260)
            text_screen("3rd  : "+third, red, 350, 335)
            b1 = button(gameWindow, (50, 550), "Back")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        gp.setGameStart(False)
                        gp.setGameOver(False)
                        gp.setRanking(False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if b1.collidepoint(pygame.mouse.get_pos()):                        
                        gp.setGameStart(False)
                        gp.setGameOver(False)
                        gp.setRanking(False)
                
        #-----------MENU-------------------------
        else: 
            gameWindow.blit(Main_Bg,[0,0])

            #text_screen("Start Game", red, 500, 300)
            #text_screen("Leader Board", red, 500, 400)
            #text_screen("Enter to Start", red, 315, 100)

            b1 = button(gameWindow, (560, 500), "Quit")
            b2 = button(gameWindow, (560, 360), "Normal")
            b3 = button(gameWindow, (730, 360), "Hard")
            b4 = button(gameWindow, (560, 450), "Ranking")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if b1.collidepoint(pygame.mouse.get_pos()):
                        exit_game = True
                    elif b2.collidepoint(pygame.mouse.get_pos()):
                        gp.setHardMode(False)
                        gp.setGameStart(True)
                        gp.setGameOver(False)
                        gp.setRanking(False)
                    elif b3.collidepoint(pygame.mouse.get_pos()):
                        gp.setHardMode(True)
                        gp.setGameStart(True)
                        gp.setGameOver(False)
                        gp.setRanking(False)
                    elif b4.collidepoint(pygame.mouse.get_pos()):                        
                        gp.setGameStart(False)
                        gp.setGameOver(False)
                        gp.setRanking(True)




        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

 
gameloop()
