import pygame
from pygame.draw import *
from random import randint
from math import sin
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]

score = 0

dt = 1
class ball:
    ''' Создание класса шаров '''
    def __init__(self):
        ''' Функция создания шара '''
        self.x = randint(100, 1100) # значение координаты x центра шара
        self.y = randint(100, 700) # значение координаты y центра шара
        self.r = randint(10, 30) # значение радиуса шара
        self.rare = randint(7,9) # Значение rare 9 соответствует появлению редкого шара
        if self.rare == 9:
            self.color = COLORS[6] # Редкому шару присваиваем белый цвет
        else:
            self.color = COLORS[randint(0, 5)] # Обычным шарам присваиваем не белые цвета из списка

        self.velocity_x = randint(-3, 3) # значение горизонтальной составляющей скорости
        self.velocity_y = randint(-3, 3) # значение вертикальной составляющей скорости

    def new_ball(self):
        ''' Функция обновления шара'''
        self.x = randint(100, 1100)
        self.y = randint(100, 700)
        self.r = randint(10, 30)
        self.rare = randint(7,9)
        if self.rare == 9:
            self.color = COLORS[6]
        else:
            self.color = COLORS[randint(0, 5)]
        self.velocity_x = randint(-3, 3)
        self.velocity_y = randint(-3, 3)

    def move_common(self):
        ''' Функция движения обычного шара'''
        if self.x > 1200 - self.r:
            self.velocity_x = - abs(self.velocity_x) * randint(30, 70)/50 # изменение скорости при столкновении с правой стенкой
        elif self.x < self.r:
            self.velocity_x = abs(self.velocity_x) * randint(30, 70)/50 # изменение скорости при столкновении с левой стенкой
        if self.y > 800 - self.r:
            self.velocity_y = - abs(self.velocity_y) * randint(30, 70)/50 # изменение скорости при столкновении с нижней стенкой стенкой
        elif self.y < self.r:
            self.velocity_y = abs(self.velocity_y) * randint(30, 70)/50 # изменение скорости при столкновении с верхней стенкой
        self.x = self.x + dt * self.velocity_x # движение по оси x
        self.y = self.y + dt * self.velocity_y # движение по оси y
        circle(screen, self.color, (self.x, self.y), self.r)

    def move_special(self):
        ''' Функция движения редкого шара'''
        global t
        if self.x > 1200 + self.r:
            self.x = - self.x + 1200 # переход шара при его выходе за правую стенку
        elif self.x < - self.r:
            self.x = 1200 - self.x # переход шара при его выходе за левую стенку
        if self.y > 800 + self.r:
            self.y = - self.y + 800 # переход шара при его выходе за нижнюю стенку
        elif self.y < - self.r:
            self.y = 800 - self.y # переход шара при его выходе за верхнюю стенку
        self.x = self.x + dt * (self.velocity_x*sin(t/100) + self.velocity_x) # движение по оси x
        self.y = self.y + dt * self.velocity_y # движение по оси y
        circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        ''' Функция присваивания шару движения в зависимости от его редкости'''
        if self.rare == 9:
            self.move_special()
        else:
            self.move_common()

    def check(self):
        ''' Функция проверки на попадание и присвоения очков'''
        global score
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance = (mouse_x - self.x)**2 + (mouse_y - self.y)**2
        if distance <= self.r**2: # Условие попадания
            if self.rare == 9:
                count = 2 *((10000 / (self.r ** 2)) // 1) # присвоение очков за редкий шар
            else:
                count = ((10000 / (self.r ** 2)) // 1) # присвоение очков за обычный шар
            score = score + count
            self.new_ball()
            print('Great!', score)

k = 5  # количество шаров

s = [0] * k
pygame.display.update()
clock = pygame.time.Clock()
finished = False

correct = False

while not correct: # проверка на корректность имени
    name = input('Введите имя(6 символов)')
    if len(name) == 6:
        correct = True
i = -1
t = -1

while not finished:
    clock.tick(FPS)
    t += 1
    if (t % 60 == 0) and (t // 60 < k): # формирование массива шаров
        s[t // 60] = ball()    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for n in range(0, k):
                if s[n] != 0:
                    s[n].check()
    for n in range(0, k):
        if s[n] != 0:
            s[n].move()
        for i in range (n,k): # отскакивание шаров друг от друга
            if (s[n] != 0 ) and (s[i] != 0):
                if (s[n].x - s[i].x)**2 + (s[n].y - s[i].y)**2 <= (s[i].r + s[n].r)**2: 
                    s[n].velocity_x = -s[n].velocity_x
                    s[n].velocity_y = -s[n].velocity_y
                    s[i].velocity_x = -s[i].velocity_x
                    s[i].velocity_y = -s[i].velocity_y
                    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
count = 0
with open('test.txt', 'r') as file: # подсчет строк в файле
    for line in file:
        count += 1
ind = 0
f1 = ''
f2 = ''
with open('test.txt', 'r') as f: # поиск рейтинга игрока
    f = open('test.txt', 'r')
    line = f.readline()
    while ind < count:
        if score < float(line[6:len(line)]):
            line = f.readline()
            ind += 1
        else:
            break
with open('test.txt', 'r') as f: # добавление строки с позицией игрока
    for n in range (0, ind):
        f1 = f1 + f.readline()
    for n in range (ind, count):
        f2 = f2 + f.readline()
if ind == count:
    with open('test.txt', 'w') as f:
        f.write('\n'.join([f1,name+' '+str(score)]))
elif ind == 0:
    with open('test.txt', 'w') as f:
        f.write('\n'.join([name+' '+str(score),f2]))
else:
    with open('test.txt', 'w') as f:
        f.write(f1+name+' '+str(score)+'\n'+f2)
