"""
GUI object has been made, implementing will be a bit annoying with current setup
Will probably require restructuring code
-Current issue is that pygame display is made outside of every function so need to run that after 
making the gui selection

Fix collision as sometimes get stuck in the wall and can only move out after fiddling with it
Create Enemy AI
Add "animation" for treads?

To make a rudimentary player 2, player has become a list, as has enemies. Will need to set up an if statement
to fill enemies with either players or enemies depending on mode, but everything within should work the same
May not even be necessary to have a class known as enemy. Might be required if we are to use an AI as code
could get messy
"""

import pygame
import random
import sys
import time
import math
import gui

# Initialize Window
WIDTH = 1200
HEIGHT = WIDTH * 9/16
def init():
    global WIN 
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tanks!')

# Load Images
GREEN_TANK = pygame.transform.scale(pygame.image.load("./assets/green_tank.png"), (15*5, 16*5))
BLUE_TANK = pygame.transform.scale(pygame.image.load("./assets/blue_tank.png"), (15*5, 16*5))
BG = pygame.transform.scale(pygame.image.load("./assets/background.png"), (WIDTH, HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load("./assets/bullet.png"), (5*3, 5*4))

class Tank():
    COOLDOWN = 50

    def __init__(self, x, y, hit = False):
        self.x = x
        self.y = y
        self.hit = hit

        self.tank_img = None
        self.bullet_img = None
        self.tank_newimg = None
        self.face = None
        self.bullets = []
        self.cooldown_counter = 0
    
    def draw(self, window):
        self.tank_newimg = pygame.transform.rotate(self.tank_img, self.face-90)
        self.mask = pygame.mask.from_surface(self.tank_newimg)
        window.blit(self.tank_newimg, (self.x - self.tank_newimg.get_width()/2, self.y - self.tank_newimg.get_height()/2))

        for bullet in self.bullets:
            bullet.draw(window)

    def shoot(self, vel):
        if self.cooldown_counter == 0:
            coord = pygame.math.Vector2(1,1)
            coord.from_polar((60,self.face))
            print("bullet", coord)
            bullet = Bullet(self.x-10+coord.x ,self.y-10-coord.y, self.bullet_img, self.get_angle(), vel)
            WIN.blit(bullet.img, (bullet.x,bullet.y))
            self.bullets.append(bullet)
            self.cooldown_counter = 1


    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

# Probably move to super class so enemy can use
# need to check for collision with wall -> may cause issue with enemy check
# new method for enemy collision? perhaps if to check if class is tank
    def move_bullet(self, obstacles, otherTanks):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move()
            overlap = False
            for tank in otherTanks:
                if bullet.collision(tank):
                    self.bullets.remove(bullet)
                    print(bullet.x, bullet.y)
                    otherTanks.remove(tank)
            for i, obstacle in enumerate(obstacles):
                if bullet.overlap(obstacle):
                    overlap = True
                    index = i
                    break
            if overlap:
                side = bullet.sideCheck(obstacles[index])
                if side=="left":
                        bullet.vx *= -1
                        bullet.face = 180 - bullet.face
                        bullet.ricochet += 1
                        bullet.move()
                elif side == "right":
                        bullet.vx *= -1
                        bullet.face = 180 - bullet.face
                        bullet.ricochet += 1
                        bullet.move()
                elif side == "top":
                        bullet.vy *= -1
                        bullet.face *= -1
                        bullet.ricochet += 1
                        bullet.move()
                elif side == "bottom":
                        bullet.vy *= -1
                        bullet.face *= -1
                        bullet.ricochet += 1
                        bullet.move()
                else:
                    print('error')
            if bullet.ricochet > 3:
                self.bullets.remove(bullet)

    def get_width(self):
        return self.tank_newimg.get_width()
    
    def get_height(self):
        return self.tank_newimg.get_height()
    
    def get_angle(self):
        return self.face
    
class Player(Tank):
    def __init__(self, x, y, hit = False, tankColor = GREEN_TANK):
        super().__init__(x, y, hit)
        self.tank_img = tankColor
        self.tank_newimg = self.tank_img
        self.bullet_img = BULLET
        self.face = 90
        self.mask = pygame.mask.from_surface(self.tank_img)

    def rotate(self, angle):
        self.face += angle


    def get_angle(self):
        return self.face

class Enemy(Tank):
    def __init__(self, x, y, hit = False):
        super().__init__(x, y, hit)
        self.tank_img = BLUE_TANK
        self.tank_newimg = BLUE_TANK
        self.bullet_img = BULLET
        self.face = 90
        self.mask = pygame.mask.from_surface(self.tank_img)

class Bullet():
    def __init__(self, x, y, img, face, vel):
        self.x = x
        self.y = y
        self.img = img
        self.face = face
        self.newimg = None
        self.ricochet = 0
        self.mask = pygame.mask.from_surface(self.img)
        self.vx = vel*math.cos(self.face*math.pi/180)
        self.vy = vel*math.sin(self.face*math.pi/180)

    def draw(self,window):
        r = 45
        # window.blit(self.img, (self.x, self.y))
        self.newimg = pygame.transform.rotate(self.img, self.face - 90)
        window.blit(self.newimg, (self.x, self.y))
        

    def move(self):
        self.x += self.vx
        self.y -= self.vy

    def overlap(self, obstacle):        
        offset = [obstacle.x - self.x, obstacle.y - self.y]
        return self.mask.overlap(obstacle.mask, offset) != None
    
    def collision(self, tank):        
        offset = [(tank.x-tank.get_width()/2) - self.x, (tank.y-tank.get_height()/2) - self.y]
        return self.mask.overlap(tank.mask, offset) != None
    
    def sideCheck(self, obstacle):
        vert = self.x+self.get_width()/2 <= obstacle.pos[0] + obstacle.size[0]\
                and self.x+self.get_width()/2 >= obstacle.pos[0]
        horz = self.y+self.get_height()/2 >= obstacle.pos[1] \
                and self.y+self.get_height() <= obstacle.pos[1] + obstacle.size[1]
        if self.y < obstacle.pos[1] + obstacle.size[1] and self.vy > 0 and vert:
            return "bottom"
        elif self.y + self.get_height() > obstacle.pos[1] and self.vy < 0 and vert:
            return "top"
        if self.x + self.get_width() > obstacle.pos[0] and self.vx < 0 and horz:
            return "left"
        elif self.x < obstacle.pos[0] + obstacle.pos[0] and self.vx > 0 and horz:
            return "right"
        
    
    def get_width(self):
        return self.img.get_width()
    
    def get_height(self):
        return self.img.get_height()
    
    def get_angle(self):
        return self.face
    
class Obstacle():
    def __init__(self, x, y, w, h):
        self.pos = [x, y] #top left of rect
        self.x = self.pos[0]
        self.y = self.pos[1] #too lazy to change everything with pos to x and y THIS IS WHY YOU STANDARDIZE
        self.size = [w, h]
        self.color = (143, 94, 8)
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.mask = pygame.mask.from_surface(self.surf)


    def draw(self, window):
        window.blit(self.surf, self.pos)
        newmask = self.mask
        newmask
        # window.blit(newmask.to_surface(), (self.pos[0], self.pos[1]+self.size[1]))
        # window.blit(self.mask.to_surface(),self.pos)

def main():
    print('start')
    playing = True
    clock = pygame.time.Clock()
    players = [Player(100, HEIGHT/2, False, GREEN_TANK)]
    # player = Player(100, HEIGHT/2)
    vel = 2
    rotation = (3.5)
    enemies = [Player(1100, HEIGHT/2, False, BLUE_TANK)]
    walls = [Obstacle(0, 0, WIDTH, 10),
            Obstacle(0, 0, 10, HEIGHT),
            Obstacle(WIDTH - 10, 0, 10, HEIGHT),
            Obstacle(0, HEIGHT - 10, WIDTH, 10), #everything above this is borders
            Obstacle(200, 150, 20, 350),
            Obstacle(WIDTH/2, 0, 20, 150),
            Obstacle(200, 150, 200, 20),
            Obstacle(200, 500, 200, 20),
            Obstacle(WIDTH-220, 150, 20, 350),
            Obstacle(WIDTH/2, HEIGHT-150, 20, 150),
            Obstacle(WIDTH-400, 150, 200, 20),
            Obstacle(WIDTH-400,500, 200, 20),
            Obstacle(WIDTH/2-150, HEIGHT/2, 300, 20)]

    # draw and update display
    def redraw():
        WIN.fill((220, 150, 75))
        for player in players:
            player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for wall in walls:
            wall.draw(WIN)
        """
        Mask displays
        # rect1 = pygame.Surface((5,5))
        # rect2 = pygame.Surface((5,5))
        # rect3 = pygame.Surface((5,5))
        # rect4 = pygame.Surface((5,5))
        # rect1.fill((255,0,0))
        # rect2.fill((255,0,0))
        # rect3.fill((255,255,255))
        # rect4.fill((255,0,255))
        # WIN.blit(rect1,(player.x-player.get_width()/2,player.y-player.get_height()/2))
        # WIN.blit(rect2,(player.x,walls[0].pos[1]+walls[0].size[1]))
        # # print(vely)
        # WIN.blit(rect3,(player.x, walls[0].size[1]))
        # WIN.blit(rect4,(player.x,player.y-player.get_height()/2-vely-walls[0].size[1]))
        # pygame.draw.circle(WIN,(255,0, 255), (player.x + 10, player.y + 10), 47, 5)
        """
        """
        bullet radius check
        rect1 = pygame.Surface((200,5))
        rect1.fill((255,0,0))
        coord = pygame.math.Vector2(3,4)
        coord.from_polar((60,player.face))
        print("rect: ",coord)
        WIN.blit(rect1,(player.x-10+coord.x,player.y-12-coord.y))
        """
        pygame.display.update()

    # Movement collision post check
    def collision(tank, obstacles, direction, vx, vy, objType = "wall"):
        checks = []
        tankposx = (tank.x-tank.get_width()/2)
        tankposy = (tank.y-tank.get_height()/2)
        tempvelx = vx
        tempvely = vy
        tankoffsx = 0
        tankoffsy = 0
        # print([tempvelx, tempvely])
        if direction == 'neg':
            tempvelx = tempvelx*-1
            tempvely = tempvely*-1
              
        for obstacle in obstacles:
            if objType == 'tank':
                tankoffsx = obstacle.get_width()/2
                tankoffsy = obstacle.get_height()/2
                
            offset = [obstacle.x - tankoffsx - tankposx, obstacle.y - tankoffsy - tankposy]
            checks.append(tank.mask.overlap(obstacle.mask, offset) != None)

        if True in checks:
            tank.x -= tempvelx
            tank.y += tempvely

    # game loop
    while playing:
        redraw()

        # if quit, end process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        
        velx = vel*math.cos(players[0].face*math.pi/180)
        vely = vel*math.sin(players[0].face*math.pi/180)

        velx2 = vel*math.cos(enemies[0].face*math.pi/180)
        vely2 = vel*math.sin(enemies[0].face*math.pi/180)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            players[0].rotate(rotation)
        if keys[pygame.K_d]:
            players[0].rotate(-rotation)
        if keys[pygame.K_w]:
            players[0].x += velx
            players[0].y -= vely
            collision(players[0], walls, "pos", velx, vely)
            collision(players[0], enemies, "pos", velx, vely, 'tank')
        if keys[pygame.K_s]:
            players[0].x -= velx
            players[0].y += vely
            collision(players[0], walls, "neg", velx, vely)
            collision(players[0], enemies, "neg",velx ,vely, 'tank')
        if keys[pygame.K_SPACE]:
            players[0].shoot(vel*2)

        #------!!!!!!!!!!-----------PLAYER 2 CODE---------!!!!!!!!!!!!-----------
        if keys[pygame.K_KP4]:
            enemies[0].rotate(rotation)
        if keys[pygame.K_KP6]:
            enemies[0].rotate(-rotation)
        if keys[pygame.K_KP8]:
            enemies[0].x += velx2
            enemies[0].y -= vely2
            collision(enemies[0], walls, "pos", velx2, vely2)
            collision(enemies[0], players, "pos",velx2,vely2, 'tank')
        if keys[pygame.K_KP5]:
            enemies[0].x -= velx2
            enemies[0].y += vely2
            collision(enemies[0], walls, "neg",velx2,vely2)
            collision(enemies[0], players, "neg",velx2,vely2, 'tank')
        if keys[pygame.K_RSHIFT]:
            enemies[0].shoot(vel*2)

        # players[0].move_bullet(walls,enemies)
        players[0].move_bullet(walls, enemies)
        if(not enemies):
            pygame.quit()
            #Display enemy win screen
            return
        
        enemies[0].move_bullet(walls, players)

        if(not players):
            pygame.quit()
            #Display player win screen
            return
        # for enemy in enemies:
        #     enemy.move_bullet(walls, player)
        clock.tick(120)

def screenDisplay():     
    quit = False   
    while(quit == False):
        titleScreen = gui.TitleScreen()
        if(titleScreen.mode == 1):
            print('KILLED!')
            init()
            main()
        elif(titleScreen.mode == 4):
            quit = True

screenDisplay()