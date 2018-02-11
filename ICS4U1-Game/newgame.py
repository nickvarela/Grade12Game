#This program was written by Nichalus Varela for ICS4U1 Summitive Game Project. 
import pygame, os, random
from pygame.locals import *
import time
import math
os.environ['SDL_VIDEODRIVER']='windib'

#set up window
WINDOWWIDTH = 683 
WINDOWHEIGHT = 384
LEFTWALL = 22
RIGHTWALL = 661
BOTTOMWALL = 356
TOPWALL = 28

#set up the colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#set up the frame rate
FRAMERATE = 30

#constants used for the directions
DOWNLEFT = 1
DOWN = 2
DOWNRIGHT = 3
LEFT = 4
RIGHT = 6
UPLEFT = 7
UP = 8
UPRIGHT = 9

BULLETLIMIT = 4 #constant used to limit the ammount of bullets on the screen at a time

def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)

def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename).convert_alpha()
    return image, image.get_rect()

def display_title(windowSurface):
    """ This function displays the title screen """
    bg = pygame.image.load("background.png")
    windowSurface.blit(bg, (0,0))
    basicFont = pygame.font.SysFont("steamer", 100)
    subFont = pygame.font.SysFont("Papyrus", 20)
    subheight = 175
    height = WINDOWHEIGHT/4
    width = WINDOWWIDTH/4
    title = "THE ARENA"
    text = ["1. Start Game", "2. Instructions", "3. Exit Game"]
    drawText(title, basicFont, windowSurface, width-30, height, RED)
    for i in range(len(text)):
        drawText(text[i], subFont, windowSurface,25+ WINDOWWIDTH/3, subheight, WHITE)
        subheight += 30
    pygame.display.update()
    
def display_instructions(windowSurface):
    """This function displays the instructions screen"""
    windowSurface.fill(WHITE)
    bg = pygame.image.load("instructions.png")
    windowSurface.blit(bg, (0,0))
    toptext = ["Use w-a-s-d to move and press the arrow keys to shoot", "Press any key to play"]
    font = pygame.font.SysFont("Courier", 20)
    height = 10
    width = 25
    for i in range(len(toptext)):
        drawText(toptext[i], font, windowSurface,width, height, BLACK)
        height += 20
        width += 160
    waiting = True
    pygame.display.update()
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                waiting = False

def gameover(windowSurface,score):
    """This function displays the game over screen"""
    windowSurface.fill(BLACK)
    basicFont = pygame.font.SysFont("Papyrus", 20)
    gotext = ["GAME OVER", "Waves defeated: "+str(score), "1. Try Again", "2. Main Menu", "3. Exit Game"]
    height = 100
    for i in range(len(gotext)):
        drawText(gotext[i], basicFont, windowSurface,25+ WINDOWWIDTH/3, height, RED)
        height += 40
    pygame.display.update()
    
def options():
    """This function allows the user to input 1, 2, or 3, with 3 always terminating the program"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('1'):
                    waiting = False
                    return True
                elif event.key == ord('2'):
                    waiting = False
                    return False
                elif event.key == ord('3'):
                    terminate()

    
def display_menu(windowSurface):
    """This functions displays the diffuculty selection screen"""
    bg = pygame.image.load("background.png")
    windowSurface.blit(bg, (0,0))
    basicFont = pygame.font.SysFont("Papyrus", 20)
    menutext = ["Select Dificulty", "1. Easy", "2. Medium", "3. Intense"]
    height = 100
    for i in range(len(menutext)):
        drawText(menutext[i], basicFont, windowSurface, 100, height, WHITE)
        height += 40
    pygame.display.update()

def level_select():
    """This function takes the user's input of either 1, 2, or 3 and sets the speed of the enemies and their health"""
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type== KEYDOWN:
                if event.key == ord('1'):
                    greenspeed = 3
                    bluespeed = 6
                    redspeed = 4
                    health = 1
                    numenemies = 6
                    selected = True
                    
                elif event.key == ord('2'):
                    greenspeed = 4
                    bluespeed = 8
                    redspeed = 5
                    health = 2
                    numenemies = 8
                    selected = True
                    
                elif event.key == ord('3'):
                    greenspeed = 5
                    bluespeed = 10
                    redspeed = 6
                    health = 3
                    numenemies = 10
                    selected = True
                    
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
    stats = [greenspeed, bluespeed, redspeed, health, numenemies]
    return stats

def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Player(pygame.sprite.Sprite):
    """ The player controlled by the user """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = [] #The list for the player's walking animation
        self.damagelist = [] #The list for the player's invincibility animation
        #load the images used for the player to the computer's RAM
        self.image, self.rect = load_image("playerflash.png")
        self.damagelist.append(self.image)
        self.image, self.rect = load_image("walk1.png")
        self.imagelist.append(self.image)
        self.damagelist.append(self.image)
        self.image, self.rect = load_image("walk2.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("walk3.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("walk4.png")
        self.imagelist.append(self.image)
        self.image = self.imagelist[0]
        self.slot = 0
        self.dmgslot = 0

        #Position the player in the centre of the screen
        self.rect.centerx = WINDOWWIDTH /2
        self.rect.centery = WINDOWHEIGHT / 2
        self.speed = 6
        self.health = 3
        self.inv = False
        self.starttime = 0

    def update(self):
        """ Change the position of the player's rectangle """
        keystate = pygame.key.get_pressed() #creates a list of all keys pressed in an instance.
        #If any key is pressed the player goes through its walking animation.
        if keystate[K_a] or keystate[K_d] or keystate[K_w] or keystate[K_s]:
            self.slot += 1
            if self.slot == len(self.imagelist):
                self.slot = 0
            self.image = self.imagelist[self.slot]
        #all if statements to allow for diagonal movement.
        if keystate[K_a]:
            self.rect.left -= self.speed
        if keystate[K_d]:
            self.rect.right += self.speed
        if keystate[K_w]:
            self.rect.top -= self.speed
        if keystate[K_s]:
            self.rect.bottom += self.speed
        #The player is unable to pass these "walls" to make the walls in the background look real.
        if self.rect.left < LEFTWALL: 
            self.rect.left = LEFTWALL
        if self.rect.right > RIGHTWALL:
            self.rect.right = RIGHTWALL
        if self.rect.top < TOPWALL:
            self.rect.top = TOPWALL
        if self.rect.bottom > BOTTOMWALL:
            self.rect.bottom = BOTTOMWALL
        #When the player is damaged they gain a brief period of invincibility, during this time the player will flash.
        if self.inv == True:
            endtime = time.time()
            for i in range(1):
                self.dmgslot += 1
                if self.dmgslot == len(self.damagelist):
                    self.dmgslot = 0
                self.image = self.damagelist[self.dmgslot]
            if endtime-self.starttime > 1:
                self.inv = False

class GreenEnemy(pygame.sprite.Sprite):
    """ The green enemy follows the player until it kills the player, or is killed """
    def __init__(self, player, health, speed):
        self.playerxpos = player.rect.centerx
        self.playerypos = player.rect.centery
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = [] #the list used to animate the enemy
        self.slot = 0
        #load the images for the enemy to the computer's RAM
        self.image, self.rect = load_image("green1.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("green2.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("green3.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("green4.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("green5.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("green6.png")
        self.imagelist.append(self.image)
        self.image = self.imagelist[0]
        self.speed = speed
        self.health = health
        self.colour = "green"

    def update(self):
        #Loop the enemie's animation as long as it is updating on the screen
        for i in range(1):
            if self.slot == len(self.imagelist):
                self.slot = 0
            self.image = self.imagelist[self.slot]
            self.slot+=1
        #Vectors to find the player's location so the enemy can follow the player
        self.dx = self.rect.centerx - self.playerxpos #difference between player and enemies (x-coord)
        self.dy = self.rect.centery - self.playerypos #difference betweem player and enemies (y-coord)
        self.hyp = math.hypot(self.dx, self.dy) #distance between enemy and player.
        
        if self.hyp > 6: #The hypotenuse must be greater than the player's movespeed(6) to avoid the enemy stuttering when it reaches the player.
            self.dx = self.dx/self.hyp
            self.dy = self.dy/self.hyp
            #The enemy travels along the constantly updating hypotenuse to follow the player
            self.rect.centerx -= int(self.dx *self.speed)
            self.rect.centery -= int(self.dy *self.speed)

class BlueEnemy(pygame.sprite.Sprite):
    """ The blue enemy follows the player on a 2, 3, or 4 second delay and does not stop until it reaches the player's previous location, it kills the player, or it is killed """
    def __init__(self, player, health, speed):
        self.playerxpos = player.rect.centerx
        self.playerypos = player.rect.centery
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = [] #the list used to animate the enemy
        self.slot = 0
        #load the images for the enemy to the computer's RAM
        self.image, self.rect = load_image("blue1.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("blue2.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("blue3.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("blue4.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("blue5.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("blue6.png")
        self.imagelist.append(self.image)
        self.image = self.imagelist[0]
        self.speed = speed
        self.health = health
        self.colour = "blue"
        self.starttime = time.time()

    def update(self):
        #Loop the enemie's animation as long as it is updating on the screen
        for i in range(1):
            if self.slot == len(self.imagelist):
                self.slot = 0
            self.image = self.imagelist[self.slot]
            self.slot+=1
        #Vectors to find the player's location so the enemy can follow the player
        self.dx = self.rect.centerx - self.playerxpos #difference between player and enemies (x-coord)
        self.dy = self.rect.centery - self.playerypos #difference betweem player and enemies (y-coord)
        self.hyp = math.hypot(self.dx, self.dy) #distance between enemy and player.

        if self.hyp > 6: #The hypotenuse must be greater than the player's movespeed(6) to avoid the enemy stuttering when it reaches the player.
            self.dx = self.dx/self.hyp
            self.dy = self.dy/self.hyp
            #The enemy travels along the constantly updating hypotenuse to follow the player
            self.rect.centerx -= int(self.dx *self.speed)
            self.rect.centery -= int(self.dy *self.speed)
            
class RedEnemy(pygame.sprite.Sprite):
    """ The red enemy moves independantly of the player. It moves diagonally and bounces off the walls. It does not stop until either it dies or the player dies """
    def __init__(self, health, speed):
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = [] #the list used to animate the enemy
        self.slot = 0
        #load the images for the enemy to the computer's RAM
        self.image, self.rect = load_image("red1.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("red2.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("red3.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("red4.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("red5.png")
        self.imagelist.append(self.image)
        self.image, self.rect = load_image("red6.png")
        self.imagelist.append(self.image)
        self.image = self.imagelist[0]
        self.speed = speed
        self.health = health
        self.dir = DOWNLEFT
        self.colour = "red"

    def update(self):
        #Loop the enemie's animation as long as it is updating on the screen
        for i in range(1):
            if self.slot == len(self.imagelist):
                self.slot = 0
            self.image = self.imagelist[self.slot]
            self.slot+=1
        #set up the directions for the enemy to move
        if self.dir == DOWNLEFT:
            self.rect.left -= self.speed
            self.rect.top += self.speed
        elif self.dir == DOWNRIGHT:
            self.rect.left += self.speed
            self.rect.top += self.speed
        elif self.dir == UPLEFT:
            self.rect.left -= self.speed
            self.rect.top -= self.speed
        elif self.dir == UPRIGHT:
            self.rect.left += self.speed
            self.rect.top -= self.speed
        #if the enemy hits any of the walls
        if self.rect.top < TOPWALL: #If the enemy moves past the top.
            if self.dir == UPLEFT:
                self.dir = DOWNLEFT
            elif self.dir == UPRIGHT:
                self.dir = DOWNRIGHT
        elif self.rect.bottom > BOTTOMWALL: #If the enemy moves past the bottom.
            if self.dir == DOWNLEFT:
                self.dir = UPLEFT
            elif self.dir == DOWNRIGHT:
                self.dir = UPRIGHT
        elif self.rect.left < LEFTWALL: #If the enemy moves past the left.
            if self.dir == DOWNLEFT:
                self.dir = DOWNRIGHT
            elif self.dir == UPLEFT:
                self.dir = UPRIGHT
        elif self.rect.right > RIGHTWALL: #If the enemy moves past the right.
            if self.dir == DOWNRIGHT:
                self.dir = DOWNLEFT
            elif self.dir == UPRIGHT:
                self.dir = UPLEFT

class Bullet(pygame.sprite.Sprite):
    """ The bullet is fired from the center of the player. There cannot be more than 4 on the screen at the same time. Deals 1 damage to enemies. """
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.direction = direction
        self.speed = 10  

    def update(self):
        if self.direction == UP:
            self.rect.top += -1*self.speed
        elif self.direction == DOWN:
            self.rect.bottom += self.speed
        elif self.direction == RIGHT:
            self.rect.right += self.speed
        elif self.direction == LEFT:
            self.rect.left += -1*self.speed
        #If a bullet hits a wall it will disappear.
        if self.rect.bottom > BOTTOMWALL or self.rect.top < TOPWALL or self.rect.right > RIGHTWALL or self.rect.left < LEFTWALL:
            self.kill()

class Game():
    """ The game class """
    def __init__(self, stats):
        pygame.mixer.init() #initialized mixer enabling sounds
        #load all of the sounds for the game
        self.bullet_sound = pygame.mixer.Sound("bullet.wav")
        self.spawn_sound = pygame.mixer.Sound("summonsound.wav")
        self.enemyhit_sound = pygame.mixer.Sound("enemyhit.wav")
        self.enemydies_sound = pygame.mixer.Sound("enemydies.wav")
        self.playerhit_sound = pygame.mixer.Sound("playerhit.wav")
        self.playerdies_sound = pygame.mixer.Sound("playerdies.wav")
        pygame.mixer.music.load("EnemyApproaching.wav")
        pygame.mixer.music.set_volume(0.5)
        self.score = 0 #after a game over the player's score is set back to 0
        self.all_sprites = pygame.sprite.Group() #all_sprites is used to update all sprites on the screen at the same time
        self.bullets = pygame.sprite.Group() #bullets contains all of the bullets on the screen at the same time
        self.enemies = pygame.sprite.Group() #enemies contains all of the enemies on the screen at the same time
        self.player = Player()
        self.all_sprites.add(self.player) #adds the player to all_sprites
        self.greenspeed = stats[0] #assigns the speed of the green enemy
        self.bluespeed = stats[1] #assigns the speed of the blue enemy
        self.redspeed = stats[2] #assigns the speed of the red enemy
        self.enemyhealth = stats[3] #assigns the health of the enemies
        self.numenemies = stats[4] #assigns the number of enemies to be spawned each wave
        self.starttime = time.time() #starts the timer
        self.game_over = False
        self.fill_list() #fills the list of enemies
        pygame.mixer.music.play(-1,0.0)
    def fill_list(self):
        """ This function fills the list randomly from the three enemy types and gives each enemy a random corner to spawn in """
        self.locations = [(30,30), (30,WINDOWHEIGHT-30), (WINDOWWIDTH-30, 30), (WINDOWWIDTH-30, WINDOWHEIGHT-30)]
        for i in range(self.numenemies):
            
            slot = random.randrange(3)
            
            if slot == 0:
                enemy = GreenEnemy(self.player, self.enemyhealth, self.greenspeed)
            elif slot == 1:
                enemy = BlueEnemy(self.player, self.enemyhealth, self.bluespeed)
            else:
                enemy = RedEnemy(self.enemyhealth, self.redspeed)
                
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
        for anenemy in self.enemies:
            anenemy.rect.topleft = self.locations[random.randrange(len(self.locations))]
        self.spawn_sound.play() #plays the spawn sound effect at the start of every wave+          
            
    def process_events(self, windowSurface):
        """ proccess all external events such as keyboard presses """
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if len(self.bullets) < BULLETLIMIT: #Limits the ammount of bullets on the screen at a time
                    if event.key == K_UP: #fires a bullet up
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, UP)
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        self.bullet_sound.play() #plays the firing sound effect

                    if event.key == K_DOWN: #fires a bullet down                        
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, DOWN)
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        self.bullet_sound.play() #plays the firing sound effect

                    if event.key == K_LEFT: #fires a bullet left 
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, LEFT)
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        self.bullet_sound.play() #plays the firing sound effect

                    if event.key == K_RIGHT: #fires a bullet right
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, RIGHT)
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        self.bullet_sound.play() #plays the firing sound effect
                    
                    

    def display_frame(self, windowSurface):
        """draws everything on the screen during gameplay"""
        bg = pygame.image.load("background.png")
        windowSurface.blit(bg, (0,0))
        font = pygame.font.SysFont("Steamer", 30)
        text = ["Lives: "+str(self.player.health), "Waves Defeated: "+str(self.score)] #displays the player's lives and waves defeated
        width = 0
        for i in range(len(text)):
            drawText(text[i], font, windowSurface,width, 0, WHITE)
            width += WINDOWWIDTH-200
        self.all_sprites.draw(windowSurface)
        pygame.display.update()

    def run_logic(self):
        """ deals with all sprite collisions"""
        if not self.game_over:
            for anenemy in self.enemies:
                if anenemy.colour == "green": #if the enemy is green it will always be given the player's position
                    anenemy.playerxpos = self.player.rect.centerx
                    anenemy.playerypos = self.player.rect.centery
                elif anenemy.colour == "blue":
                    endtime = time.time()
                    if endtime-anenemy.starttime > random.randrange(2,5): #if the enemy is blue it will be given the player's position with a 2 to 4 second delay.
                        anenemy.playerxpos = self.player.rect.centerx
                        anenemy.playerypos = self.player.rect.centery
                        anenemy.starttime = time.time()

                if anenemy in self.all_sprites:
                    enemy_hit_list = pygame.sprite.spritecollide(anenemy, self.bullets, True)
                    if len(enemy_hit_list) > 0: #if a bullet hits an enemy the enemy loses 1 health point
                        anenemy.health -= 1
                        self.enemyhit_sound.play() #plays the enemy hit sound
                        if anenemy.health < 1: #if the enemy loses all health points it dies
                            anenemy.kill() 
                            self.enemydies_sound.play() #plays the enemy death sound

                if self.player.inv == False:
                    player_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
                    if len(player_hit_list) > 0: #if an enemy hits the player the player loses a life
                        self.player.health -= 1
                        if self.player.health < 1: #if the player loses all of their lives they die and it's game over
                            self.player.kill()
                            self.playerdies_sound.play() #play the player death sound
                            self.game_over = True
                            pygame.mixer.music.stop()
                        self.player.inv = True
                        self.player.starttime = time.time()
                        self.playerhit_sound.play() #plays the player hit sound

                if len(self.enemies) == 0: #if all enemies on screen are defeated spawn a list full of new ones
                    self.score += 1
                    if self.player.health < 10:
                        self.player.health += 1
                    self.fill_list()
                    
            self.all_sprites.update()

def main():
    """ the main line of the program """
    pygame.init() #initialize pygame
    mainClock = pygame.time.Clock() #initializes the main clock
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #initializes the window surface
    pygame.display.set_caption('Welcome to The Arena') #Sets the caption
    display_title(windowSurface)  
    title_selection = options()
    if title_selection: #if the player chose 1 they are sent to choose the dificulty then play the game
        display_menu(windowSurface)
        stats = level_select()
        game = Game(stats)
    else: #if the player chose 2 they are sent to the instructions screen before choosing dificulty and playing the game
        display_instructions(windowSurface)
        display_menu(windowSurface)
        stats = level_select()
        game = Game(stats)
        
    while True:
        while game.game_over: #when the game is over the player can choose to try again, return to the main menu, or to exit the game
            gameover(windowSurface,game.score)
            option_chosen = options()
            if option_chosen: #if the player chooses 1 they are sent back into the action with the dificulty they previously chose
                game = Game(stats)
            else: #if the player chooses 2 they are sent back to the main menu
                display_title(windowSurface)
                title_selection = options()
                if title_selection:
                    display_menu(windowSurface)
                    stats = level_select()
                    game = Game(stats)
                else:
                    display_instructions(windowSurface)
                    display_menu(windowSurface)
                    stats = level_select()
                    game = Game(stats)

        starttime = time.time()
        
        game.process_events(windowSurface)
        
        game.run_logic()
        
        game.display_frame(windowSurface)
        
        mainClock.tick(FRAMERATE)
        
        endtime=time.time()
        if endtime - starttime > 1:
            starttime = time.time()

main()
