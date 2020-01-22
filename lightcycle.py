#
#    __           ________      _______      ___   ___      _________   ______       __  __     ______       __           ______      
#   /_/\         /_______/\    /______/\    /__/\ /__/\    /________/\ /_____/\     /_/\/_/\   /_____/\     /_/\         /_____/\     
#   \:\ \        \__.::._\/    \::::__\/__  \::\ \\  \ \   \__.::.__\/ \:::__\/     \ \ \ \ \  \:::__\/     \:\ \        \::::_\/_    
#    \:\ \          \::\ \      \:\ /____/\  \::\/_\ .\ \     \::\ \    \:\ \  __    \:\_\ \ \  \:\ \  __    \:\ \        \:\/___/\   
#     \:\ \____     _\::\ \__    \:\\_  _\/   \:: ___::\ \     \::\ \    \:\ \/_/\    \::::_\/   \:\ \/_/\    \:\ \____    \::___\/_  
#      \:\/___/\   /__\::\__/\    \:\_\ \ \    \: \ \\::\ \     \::\ \    \:\_\ \ \     \::\ \    \:\_\ \ \    \:\/___/\    \:\____/\ 
#       \_____\/   \________\/     \_____\/     \__\/ \::\/      \__\/     \_____\/      \__\/     \_____\/     \_____\/     \_____\/ 
#                                                                                                                                  
# By Marco
# Ver. 1.0
#
#
# Goals
# - Networking
# - A.I CPU
# - Main dictionary to hold constants



import os, sys, time, random
import pygame
import pygame.gfxdraw
from pygame.locals import *


class Player:
    def __init__(self,x,y,color,x_speed,y_speed,alive,current_rect):
        '''The class that deals with any information associated to the player(s)'''
        self.x = x
        self.y = y
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.alive = alive
        self.current_rect = current_rect

class AI:
    def __init__(self,x,y,color,x_speed,y_speed,current_rect):
        '''The class that deals with any information associated to the AI'''
        self.color = color
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.current_rect = current_rect

    def mirror(self,Player):
        '''A method that mirrors the player's movement for the Mirror Gamemode'''
        self.x_speed = Player.x_speed*-1
        self.y_speed = Player.y_speed*-1
    
class Game:
    def __init__(self,gamemode,players,previous_pos):
        '''The class that deals with any information about the game'''
        self.gamemode = gamemode
        self.players = players
        self.previous_pos = previous_pos

    def increase_players(self):
        '''Increases the number of players by 1 unless the maximum is reached'''
        if self.players != 4:
            self.players += 1

    def decrease_players(self):
        '''Decreases the number of players by 1 unless the minimum is reached'''
        if self.players != 1:
            self.players -= 1
        
def message_to_screen(text,color,font,x_aligned,y_aligned,x_pos=None,y_pos=None):
    '''
    A function that renders and blits the given text to the screen

    text: The desired text to be blit to the screen as a string
    color: The color of the text as an RGB tuple
    font: The font of the text created through Pygame.font.Font()
    x_aligned: Boolean: 'True' for the text to be centered on the x-axis, 'False' otherwise
    y_aligned: Boolean: 'True' for the text to be centered on the y-axis, 'False' otherwise
    x_pos: The x-coordinate of the text, used if x_aligned == False
    y_pos: The y-coordinate of the text, used if y_aligned == False
    
    '''
    rendered_text = font.render(text,True,color)
    if x_aligned and y_aligned:
        screen.blit(rendered_text, [screen_x/2 - rendered_text.get_width()/2, screen_y/2 - rendered_text.get_height()/2])
    elif x_aligned:
        screen.blit(rendered_text, [screen_x/2 - rendered_text.get_width()/2, y_pos])
    elif y_aligned:
        screen.blit(rendered_text, [x_pos, screen_y/2 - rendered_text.get_height()/2])
    else:
        screen.blit(rendered_text, [x_pos,y_pos])

def message_to_button(text,color,font,button_x,button_y,button_width,button_height):
    '''
    A function that renders and blits text to the center of a button

    text: The desired text to be blit to the screen as a string
    color: The color of the text as an RGB tuple
    font: The font of the text created through Pygame.font.Font()
    button_x: The x-coordinate of the button as an int
    button_y: The y-coordinate of the button as an int
    button_width: The width of the button as an int
    button_height: The height of the button as an int

    '''
    rendered_text = font.render(text,True,color)
    screen.blit(rendered_text, [button_x+(button_width/2)-rendered_text.get_width()/2,button_y+(button_height/2)-rendered_text.get_height()/2])

def music_pause():
    '''
    A function that pauses the music
    '''
    pygame.mixer.music.pause()

def music_unpause():
    '''
    A function that unpauses the music
    '''
    pygame.mixer.music.unpause()

def button_handler(text,button_x,button_y,button_width,button_height,color,highlighted_color,action=None,game_class=None,player_class_list=None):
    '''
    A function that handles all button interactions

    text: The desired text to be blit to the button as a string
    button_x: The x-coordinate of the button as an int
    button_y: The y-coordinate of the button as an int
    button_width: The width of the button as an int
    button_height: The height of the button as an int
    color: The color of the button when the cursor is not on it as an RGB tuple
    highlighted_color: The color of the button when the cursor is on it as an RGB tuple
    action: (NOT REQUIRED) The desired result of clicking the button as a string used in the function
    game_class: (NOT REQUIRED) A game_class object
    player_class_list: (NOT REQUIRED) A player class or CPU class object
        
    '''
    mousepos = pygame.mouse.get_pos()
    mousepress = pygame.mouse.get_pressed()
    if button_x < mousepos[0] < button_x + button_width and button_y < mousepos[1] < button_y + button_height:
        pygame.draw.rect(screen, highlighted_color, (button_x,button_y,button_width,button_height))
        if mousepress[0] == 1:
            if action == "controls": # Checks if the user wants to go to the controls screen
                control_screen(positions)
            elif action == "main": # Checks if the user wants to go to the start screen
                start_screen(positions)
            elif action == "gamemode": # Checks if the user wants to go to the gamemode screen from the main screen
                gamemode_screen(positions)
            elif action  == "gamemode2": # Checks if the user wants to go to the gamemode screen from the color selection screen
                game_class.gamemode = None
                gamemode_screen(positions)
            elif action == "player increase": # Checks if the user wants to increase the number of players
                game_class.increase_players()
                time.sleep(0.1)
            elif action == "player decrease": # Checks if the user wants to decrease the number of players
                game_class.decrease_players()
                time.sleep(0.1)
            elif action == "color1": # Checks if the user wants to go to the color screen for the Mirror Gamemode
                game_class.gamemode = "mirror"
                color_screen(game_class)
            elif action == "color2": # Checks if the user wants to go to the color screen for the Free For All Gamemode
                game_class.gamemode = "free for all"
                color_screen(game_class)
            elif action == "red": # Subsequent lines deal with the player choosing a color
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = red
                        break
                    elif player_class_list[i].color == red:
                        break
            elif action == "orange":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = orange
                        break
                    elif player_class_list[i].color == orange:
                        break
            elif action == "yellow":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = yellow
                        break
                    elif player_class_list[i].color == yellow:
                        break
            elif action == "blue":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = blue
                        break
                    elif player_class_list[i].color == blue:
                        break
            elif action == "purple":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = purple
                        break
                    elif player_class_list[i].color == purple:
                        break
            elif action == "pink":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = pink
                        break
                    elif player_class_list[i].color == pink:
                        break
            elif action == "green":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = green
                        break
                    elif player_class_list[i].color == green:
                        break
            elif action == "turquoise":
                for i in range(len(player_class_list)):
                    if player_class_list[i].color == None:
                        player_class_list[i].color = turquoise
                        break
                    elif player_class_list[i].color == turquoise:
                        break
            elif action == "game": # Checks if the user wants to start the game
                game_countdown(player_class_list,game_class)
            elif action == "mute":  # Mutes the music
                music_pause()
            elif action == "unmute": # Plays the music
                music_unpause()
    else:
        pygame.draw.rect(screen, color, (button_x,button_y,button_width,button_height))
    message_to_button(text,black,button_font,button_x,button_y,button_width,button_height)

def intro_background():
    '''
    A function that draws the background of the intro sequence
    '''  
    screen.fill((0,0,0))
    pygame.draw.rect(screen,yellow,(507,50,10,50))
    pygame.draw.rect(screen,yellow,(507,200,10,50))
    pygame.draw.rect(screen,yellow,(507,350,10,50))
    pygame.draw.rect(screen,yellow,(507,500,10,50))
    pygame.draw.rect(screen,yellow,(507,650,10,50))
    pygame.draw.rect(screen,yellow,(507,800,10,50))
    pygame.draw.rect(screen,yellow,(507,950,10,50))
    pygame.draw.rect(screen,light_grey,(0,0,80,1024))
    pygame.draw.rect(screen,light_grey,(944,0,80,1024))
    pygame.draw.rect(screen,grey,(0,20,80,10))
    pygame.draw.rect(screen,grey,(0,120,80,10))
    pygame.draw.rect(screen,grey,(0,220,80,10))
    pygame.draw.rect(screen,grey,(0,320,80,10))
    pygame.draw.rect(screen,grey,(0,420,80,10))
    pygame.draw.rect(screen,grey,(0,520,80,10))
    pygame.draw.rect(screen,grey,(0,620,80,10))
    pygame.draw.rect(screen,grey,(0,720,80,10))
    pygame.draw.rect(screen,grey,(0,820,80,10))
    pygame.draw.rect(screen,grey,(0,920,80,10))
    pygame.draw.rect(screen,grey,(0,1020,80,10))
    pygame.draw.rect(screen,grey,(944,20,80,10))
    pygame.draw.rect(screen,grey,(944,120,80,10))
    pygame.draw.rect(screen,grey,(944,220,80,10))
    pygame.draw.rect(screen,grey,(944,320,80,10))
    pygame.draw.rect(screen,grey,(944,420,80,10))
    pygame.draw.rect(screen,grey,(944,520,80,10))
    pygame.draw.rect(screen,grey,(944,620,80,10))
    pygame.draw.rect(screen,grey,(944,720,80,10))
    pygame.draw.rect(screen,grey,(944,820,80,10))
    pygame.draw.rect(screen,grey,(944,920,80,10))
    pygame.draw.rect(screen,grey,(944,1020,80,10))

def intro_animation():
    '''
    A function that deals with the intro sequence's animation
    '''
    pygame.mixer.music.load("8-bit explosion.mp3")
    for i in range(150):
        pygame.draw.rect(screen,red,(180,1024-2*i,8,8))
        pygame.draw.rect(screen,green,(397,1024-2*i,8,8))
        pygame.draw.rect(screen,blue,(844,1024-2*i,8,8))
        pygame.draw.rect(screen,pink,(627,1024-2*i,8,8))
        pygame.display.update()
    for u in range(54):
        pygame.draw.rect(screen,blue,(844,724-2*u,8,8))
        pygame.draw.rect(screen,pink,(627,724-2*u,8,8))
        pygame.draw.rect(screen,red,(180+2*u,724,8,8))
        pygame.draw.rect(screen,green,(397-2*u,724,8,8))
        pygame.display.update()
        if u == 5:
            pygame.mixer.music.play(1)
    for j in range(54):
        pygame.draw.rect(screen,red,(288,724-2*j,8,8))
        pygame.draw.rect(screen,blue,(844-2*j,616,8,8))
        pygame.draw.rect(screen,pink,(627+2*j,616,8,8))
        pygame.display.update()
        if j == 5:
            pygame.mixer.music.play(1)
    for k in range(230):
        pygame.draw.rect(screen,blue,(736,616-2*k,8,8))
        pygame.draw.rect(screen,red,(288,616-2*k,8,8))
        pygame.display.update()
    for l in range(111):
        pygame.draw.rect(screen,blue,(736-2*l,156,8,8))
        pygame.draw.rect(screen,red,(288+2*l,156,8,8))
        pygame.display.update()
        if l == 40:
            pygame.mixer.music.play(1)
    for m in range(40):
        screen.fill((55+m*5,55+m*5,55+m*5))
        pygame.display.update()
    time.sleep(2)
    for n in range(18):
        screen.fill((255-n*15,255-n*15,255-n*15))
        pygame.display.update()
    pygame.mixer.music.stop()

def background_animation(positions):
    '''
    A function that deals with the background animation seens on the Main Menu, Control Screen, Gamemode Screen, and End Game Screen

    positions: A list holding the positions of the rectangles in the background animation

    '''
    pygame.draw.rect(screen, white, (positions[3][0],positions[3][1],8,8))
    pygame.draw.rect(screen, yellow, (positions[2][0],positions[2][1],8,8))
    pygame.draw.rect(screen, light_green, (positions[1][0],positions[1][1],8,8))    
    pygame.draw.rect(screen, pink, (positions[0][0],positions[0][1],8,8))
    pygame.draw.rect(screen, orange, (positions[4][0],positions[4][1],8,8))
    pygame.draw.rect(screen, purple, (positions[5][0],positions[5][1],8,8))
    pygame.draw.rect(screen, dark_blue, (positions[6][0],positions[6][1],8,8))    
    pygame.draw.rect(screen, turquoise, (positions[7][0],positions[7][1],8,8))
    pygame.draw.rect(screen, red, (positions[8][0],positions[8][1],8,8))
    pygame.draw.rect(screen, light_red, (positions[9][0],positions[9][1],8,8))
    pygame.draw.rect(screen, light_purple, (positions[10][0],positions[10][1],8,8))
    pygame.draw.rect(screen, green, (positions[11][0],positions[11][1],8,8))
    pygame.draw.rect(screen, blue, (positions[12][0],positions[12][1],8,8))
    pygame.draw.rect(screen, light_blue, (positions[13][0],positions[13][1],8,8))
    pygame.draw.rect(screen, neon_blue, (positions[14][0],positions[14][1],8,8))
    pygame.draw.rect(screen, light_grey, (positions[15][0],positions[15][1],8,8))
    pygame.draw.rect(screen, grey, (positions[16][0],positions[16][1],8,8))
    for i in range(1,6):
        pygame.gfxdraw.box(screen,(positions[0][0]-8*i,positions[0][1],8,8),(248,71,233,260-40*i))
        pygame.gfxdraw.box(screen,(positions[1][0]-8*i,positions[1][1],8,8),(120,255,120,260-40*i))
        pygame.gfxdraw.box(screen,(positions[2][0]-8*i,positions[2][1],8,8),(234,249,4,260-40*i))       
        pygame.gfxdraw.box(screen,(positions[3][0]-8*i,positions[3][1],8,8),(255,255,255,260-40*i))
        pygame.gfxdraw.box(screen,(positions[4][0]-8*i,positions[4][1],8,8),(255,128,0,260-40*i))
        pygame.gfxdraw.box(screen,(positions[5][0]-8*i,positions[5][1],8,8),(102,0,204,260-40*i))
        pygame.gfxdraw.box(screen,(positions[6][0]-8*i,positions[6][1],8,8),(0,0,153,260-40*i))       
        pygame.gfxdraw.box(screen,(positions[7][0]-8*i,positions[7][1],8,8),(0,204,204,260-40*i))
        pygame.gfxdraw.box(screen,(positions[8][0]-8*i,positions[8][1],8,8),(255,80,80,260-40*i))
        pygame.gfxdraw.box(screen,(positions[9][0]-8*i,positions[9][1],8,8),(255,120,120,260-40*i))
        pygame.gfxdraw.box(screen,(positions[10][0]-8*i,positions[10][1],8,8),(178,102,255,260-40*i))
        pygame.gfxdraw.box(screen,(positions[11][0]-8*i,positions[11][1],8,8),(20,255,80,260-40*i))
        pygame.gfxdraw.box(screen,(positions[12][0]-8*i,positions[12][1],8,8),(80,80,255,260-40*i))
        pygame.gfxdraw.box(screen,(positions[13][0]-8*i,positions[13][1],8,8),(120,120,255,260-40*i))
        pygame.gfxdraw.box(screen,(positions[14][0]-8*i,positions[14][1],8,8),(25,238,238,260-40*i))
        pygame.gfxdraw.box(screen,(positions[15][0]-8*i,positions[15][1],8,8),(171,172,159,260-40*i))
        pygame.gfxdraw.box(screen,(positions[16][0]-8*i,positions[16][1],8,8),(96,96,96,260-40*i))
    for u in range(len(positions)):
        if positions[u][0] > 1060:
            positions[u][0] = random.randrange(-1000,-100,50)
            positions[u][1] = random.randrange(1,1024,50)
        else:
            positions[u][0] += 2

def start_screen(positions):
    '''
    A function that draws the Start Screen    

    positions: A list holding the positions of the rectangles in the background animation
    
    '''
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
        screen.fill(black)
        background_animation(positions)
        message_to_screen("Lightcycle",neon_blue,title_font,True,False,0,100)
        message_to_screen("By Marco",neon_blue,subtitle_font,True,False,0,220)
        message_to_screen("Ver. 1.0",light_green,button_font,True,False,0,20)
        button_handler("Controls",200,800,200,120,red, light_red,"controls")
        button_handler("Play",624,800,200,120,blue,light_blue,"gamemode")
        button_handler("Mute",894,10,120,60,grey,light_grey,"mute",None,None)
        button_handler("Unmute",10,10,120,60,grey,light_grey,"unmute",None,None)
        pygame.display.update()
        clock.tick(120)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def control_screen(positions):
    '''
    A function that draws the Control screen

    positions: A list holding the positions of the rectangles in the background animation

    '''
    control_screen = True
    while control_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control_screen = False
        screen.fill(black)
        background_animation(positions)
        message_to_screen("Controls",neon_blue,controls_title_font,True,False,None,100)
        message_to_screen("Player 1",red,player_title_font,False,False,50,350)
        message_to_screen("Player 2",green,player_title_font,False,False,320,350)
        message_to_screen("Player 3",blue,player_title_font,False,False,570,350)
        message_to_screen("Player 4",purple,player_title_font,False,False,820,350)
        message_to_screen("Up: W",light_red,player_title_font,False,False,75,500)
        message_to_screen("Down: S",light_red,player_title_font,False,False,55,600)
        message_to_screen("Left: A",light_red,player_title_font,False,False,60,700)
        message_to_screen("Right: D",light_red,player_title_font,False,False,50,800)
        message_to_screen("Up: /\\",light_green,player_title_font,False,False,340,500)
        message_to_screen("Down: \\/",light_green,player_title_font,False,False,325,600)
        message_to_screen("Left: <",light_green,player_title_font,False,False,335,700)
        message_to_screen("Right: >",light_green,player_title_font,False,False,330,800)
        message_to_screen("Up: F",light_blue,player_title_font,False,False,600,500)
        message_to_screen("Down: V",light_blue,player_title_font,False,False,575,600)
        message_to_screen("Left: C",light_blue,player_title_font,False,False,575,700)
        message_to_screen("Right: B",light_blue,player_title_font,False,False,570,800)
        message_to_screen("Up: U",light_purple,player_title_font,False,False,850,500)
        message_to_screen("Down: J",light_purple,player_title_font,False,False,830,600)
        message_to_screen("Left: H",light_purple,player_title_font,False,False,830,700)
        message_to_screen("Right: K",light_purple,player_title_font,False,False,820,800)
        button_handler("Back",10,10,120,60,grey,light_grey,"main")
        pygame.display.update()
        clock.tick(120)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def gamemode_screen(positions):
    '''
    A function that draws the gamemode screen

    positions: A list holding the positions of the rectangles in the background animation

    '''
    gamemode_screen = True
    game = Game(None,1,[])
    while gamemode_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamemode_screen = False
        screen.fill(black)
        background_animation(positions)
        pygame.draw.rect(screen,light_grey,(0,0,20,1024))
        pygame.draw.rect(screen,light_grey,(20,0,1004,20))
        pygame.draw.rect(screen,light_grey,(1004,20,20,1004))
        pygame.draw.rect(screen,light_grey,(20,1004,1004,20))
        pygame.draw.rect(screen,light_grey,(90,364,350,350))
        pygame.draw.rect(screen,light_grey,(584,364,350,350))
        button_handler("Back",30,30,120,60,grey,light_grey,"main")
        button_handler("+",934,30,60,60,grey,light_grey,"player increase",game)
        button_handler("-",800,30,60,60,grey,light_grey,"player decrease",game)
        if game.players == 1:
            button_handler("Mirror Mode",110,384,310,310,green,light_green,"color1",game)
        else:
            button_handler("Unavailable",110,384,310,310,dark_green,dark_green,"none")
        if game.players != 1:
            button_handler("Free For Fall",604,384,310,310,turquoise,neon_blue,"color2",game)
        else:
            button_handler("Unavailable",604,384,310,310,dark_turquoise,dark_turquoise,"none")
        message_to_screen(str(game.players),white,button_font,False,False,893,45)
        message_to_screen("Players",white,button_font,False,False,845,100)
        pygame.display.update()
        clock.tick(120)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def color_screen(game_class):
    '''
    A function that draws the control screen

    game_class: A game_class object

    '''
    time.sleep(0.2)
    color_screen = True
    players_lst = []
    players_lst.append(Player(40,508,None,8,0,True,None))
    if game_class.gamemode == "mirror":
        players_lst.append(AI(976,508,light_grey,-8,0,None))
    else:
        if game_class.players >= 2:
            players_lst.append(Player(976,508,None,-8,0,True,None))
        if game_class.players >= 3:
            players_lst.append(Player(508,40,None,0,8,True,None))
        if game_class.players == 4:
            players_lst.append(Player(508,976,None,0,-8,True,None))
    while color_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                color_screen = False
        screen.fill(black)
        pygame.draw.rect(screen,grey,(0,0,20,1024)) 
        pygame.draw.rect(screen,grey,(20,0,1004,20)) 
        pygame.draw.rect(screen,grey,(1004,20,20,1004))
        pygame.draw.rect(screen,grey,(20,1004,1004,20))
        pygame.draw.rect(screen,grey,(20,500,984,20))
        button_handler("",20,20,230,480,red,light_red,"red",None,players_lst)
        button_handler("",270,20,236,480,yellow,light_yellow,"yellow",None,players_lst)
        button_handler("",526,20,236,480,blue,light_blue,"blue",None,players_lst)
        button_handler("",782,20,222,480,purple,light_purple,"purple",None,players_lst)
        button_handler("",20,520,230,484,orange,light_orange,"orange",None,players_lst)
        button_handler("",270,520,236,484,pink,light_pink,"pink",None,players_lst)
        button_handler("",526,520,236,484,green,light_green,"green",None,players_lst)
        button_handler("",782,520,222,484,turquoise,light_turquoise,"turquoise",None,players_lst)
        pygame.draw.rect(screen,grey,(250,0,20,1024))
        pygame.draw.rect(screen,grey,(506,0,20,1024))
        pygame.draw.rect(screen,grey,(762,0,20,1024))
        button_handler("B",0,0,20,20,light_grey,grey,"gamemode2",game_class)
        for i in range(len(players_lst)):
            if players_lst[i].color == None:
                message_to_screen(("Choose your color: Player "+str(i+1)),white,subtitle_font,True,True)
                break
            if players_lst[i].color == red:
                button_handler(("Player "+str(i+1)),20,20,230,480,dark_red,dark_red,"none",None,players_lst)
            if players_lst[i].color == yellow:
                button_handler(("Player "+str(i+1)),270,20,236,480,dark_yellow,dark_yellow,"none",None,players_lst)
            if players_lst[i].color == orange:
                button_handler(("Player "+str(i+1)),20,520,230,484,dark_orange,dark_orange,"none",None,players_lst)
            if players_lst[i].color == purple:
                button_handler(("Player "+str(i+1)),782,20,222,480,dark_purple,dark_purple,"none",None,players_lst)
            if players_lst[i].color == pink:
                button_handler(("Player "+str(i+1)),270,520,236,484,dark_pink,dark_pink,"none",None,players_lst)
            if players_lst[i].color == blue:
                button_handler(("Player "+str(i+1)),526,20,236,480,dark_blue,dark_blue,"none",None,players_lst)
            if players_lst[i].color == green:
                button_handler(("Player "+str(i+1)),526,520,236,484,dark_green,dark_green,"none",None,players_lst)
            if players_lst[i].color == turquoise:
                button_handler(("Player "+str(i+1)),782,520,222,484,dark_turquoise,dark_turquoise,"none",None,players_lst)
        total = 0
        for u in range(len(players_lst)):
            if players_lst[u].color != None:
                total +=1
        if total == len(players_lst):
            game_countdown(players_lst,game_class)
        else:
            pygame.display.update()
        clock.tick(120)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def game_countdown_background(players_lst,game_class):
    '''
    A function that draws the background of the game coundown

    game_class: A game_class object
    players_lst: A list of player-class objects

    '''
    screen.fill(black)
    pygame.draw.rect(screen,grey,(0,0,20,1024)) 
    pygame.draw.rect(screen,grey,(20,0,1004,20)) 
    pygame.draw.rect(screen,grey,(1004,20,20,1004))
    pygame.draw.rect(screen,grey,(20,1004,1004,20))
    if game_class.gamemode == "mirror":
        pygame.draw.rect(screen,players_lst[0].color,(40,508,8,8))
        pygame.draw.rect(screen,light_grey,(976,508,8,8))
    elif game_class.players == 2:
        pygame.draw.rect(screen,players_lst[0].color,(40,508,8,8))
        pygame.draw.rect(screen,players_lst[1].color,(976,508,8,8))
    elif game_class.players == 3:
        pygame.draw.rect(screen,players_lst[0].color,(40,508,8,8))
        pygame.draw.rect(screen,players_lst[1].color,(976,508,8,8))
        pygame.draw.rect(screen,players_lst[2].color,(508,40,8,8))
    else:
        pygame.draw.rect(screen,players_lst[0].color,(40,508,8,8))
        pygame.draw.rect(screen,players_lst[1].color,(976,508,8,8))
        pygame.draw.rect(screen,players_lst[2].color,(508,40,8,8))
        pygame.draw.rect(screen,players_lst[3].color,(508,976,8,8))
    pygame.display.update()

def game_countdown(players_lst,game_class):
    '''
    A function that handles the game countdown

    game_class: A game_class object
    players_lst: A list of player-class objects
    
    '''
    game_countdown_background(players_lst,game_class)
    time.sleep(2)
    message_to_screen("3",red,title_font,True,True)
    pygame.display.update()
    time.sleep(1)
    game_countdown_background(players_lst,game_class)
    message_to_screen("2",orange,title_font,True,True)
    pygame.display.update()
    time.sleep(1)
    game_countdown_background(players_lst,game_class)
    message_to_screen("1",yellow,title_font,True,True)
    pygame.display.update()
    time.sleep(1)
    game_countdown_background(players_lst,game_class)
    message_to_screen("Go",green,title_font,True,True)
    pygame.display.update()
    time.sleep(1)
    game_screen(players_lst,game_class)

def game_screen(players_lst,game_class):
    '''
    A function that handles the game, its rules, and all keyboard inputs

    game_class: A game_class object
    players_lst: A list of player-class objects
    
    '''
    game_countdown_background(players_lst,game_class)
    game_screen = True
    mirror_gamemode = 0
    players_lst[0] = Player(40,508,players_lst[0].color,8,0,True,None) # Deals with creating an appropriate number of player classes
    if game_class.players >= 2:
        players_lst[1] = Player(976,508,players_lst[1].color,-8,0,True,None)
    if game_class.gamemode == "mirror":
        players_lst[1] = AI(976,508,players_lst[1].color,-8,0,None)
    if game_class.players >= 3:
        players_lst[2] = Player(508,40,players_lst[2].color,0,8,True,None)
    if game_class.players == 4:
        players_lst[3] = Player(508,976,players_lst[3].color,0,-8,True,None)
    game_class.previous_pos = []
    game_class.previous_pos.append(pygame.draw.rect(screen,grey,(0,0,20,1024)))
    game_class.previous_pos.append(pygame.draw.rect(screen,grey,(20,0,1004,20)) )
    game_class.previous_pos.append(pygame.draw.rect(screen,grey,(1004,20,20,1004)))
    game_class.previous_pos.append(pygame.draw.rect(screen,grey,(20,1004,1004,20)))
    if game_class.gamemode == "mirror":
        mirror_gamemode = 1
    while game_screen: # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen = False
            elif event.type == pygame.KEYDOWN:
                if players_lst[0].alive == True: # Player 1 keyboard inputs
                    if event.key == pygame.K_a and players_lst[0].x_speed != 8: # Ensures the player can't go backward
                        players_lst[0].x_speed = -8
                        players_lst[0].y_speed = 0
                    elif event.key == pygame.K_d and players_lst[0].x_speed != -8:
                        players_lst[0].x_speed = 8
                        players_lst[0].y_speed = 0
                    elif event.key == pygame.K_w and players_lst[0].y_speed != 8:
                        players_lst[0].x_speed = 0
                        players_lst[0].y_speed = -8
                    elif event.key == pygame.K_s and players_lst[0].y_speed != -8:
                        players_lst[0].x_speed = 0
                        players_lst[0].y_speed = 8
                    if game_class.gamemode == "mirror":
                        players_lst[1].mirror(players_lst[0])
                if game_class.gamemode == "free for all": # Only allows other keyboard inputs if the gamemode isn't a 1 player mode
                    if len(players_lst) >= 2 and players_lst[1].alive == True: # Keyboard inputs for players 2
                        if event.key == pygame.K_LEFT and players_lst[1].x_speed != 8:
                            players_lst[1].x_speed = -8
                            players_lst[1].y_speed = 0
                        elif event.key == pygame.K_RIGHT and players_lst[1].x_speed != -8:
                            players_lst[1].x_speed = 8
                            players_lst[1].y_speed = 0 
                        elif event.key == pygame.K_UP and players_lst[1].y_speed != 8:
                            players_lst[1].x_speed = 0
                            players_lst[1].y_speed = -8
                        elif event.key == pygame.K_DOWN and players_lst[1].y_speed != -8:
                            players_lst[1].x_speed = 0
                            players_lst[1].y_speed = 8
                    if len(players_lst) >= 3  and players_lst[2].alive == True: # Keyboard inputs for player 3
                        if event.key == pygame.K_c and players_lst[2].x_speed != 8:
                            players_lst[2].x_speed = -8
                            players_lst[2].y_speed = 0
                        elif event.key == pygame.K_b and players_lst[2].x_speed != -8:
                            players_lst[2].x_speed = 8
                            players_lst[2].y_speed = 0
                        elif event.key == pygame.K_f and players_lst[2].y_speed != 8:
                            players_lst[2].x_speed = 0
                            players_lst[2].y_speed = -8
                        elif event.key == pygame.K_v and players_lst[2].y_speed != -8:
                            players_lst[2].x_speed = 0
                            players_lst[2].y_speed = 8
                    if len(players_lst) == 4 and players_lst[3].alive == True: # Keyboard inputs for player 4
                        if event.key == pygame.K_h and players_lst[3].x_speed != 8:
                            players_lst[3].x_speed = -8
                            players_lst[3].y_speed = 0
                        elif event.key == pygame.K_k and players_lst[3].x_speed != -8:
                            players_lst[3].x_speed = 8
                            players_lst[3].y_speed = 0
                        elif event.key == pygame.K_u and players_lst[3].y_speed != 8:
                            players_lst[3].x_speed = 0
                            players_lst[3].y_speed = -8
                        elif event.key == pygame.K_j and players_lst[3].y_speed != -8:
                            players_lst[3].x_speed = 0
                            players_lst[3].y_speed = 8

        if players_lst[0].alive == True: # The following lines of codes deals with checking if there is a winner
            game_class.previous_pos.append(pygame.draw.rect(screen,players_lst[0].color,(players_lst[0].x+players_lst[0].x_speed,players_lst[0].y+players_lst[0].y_speed,8,8)))
            players_lst[0].current_rect = pygame.draw.rect(screen,players_lst[0].color,(players_lst[0].x+players_lst[0].x_speed,players_lst[0].y+players_lst[0].y_speed,8,8))
            players_lst[0].x += players_lst[0].x_speed
            players_lst[0].y += players_lst[0].y_speed
        if (game_class.players >= 2 and players_lst[1].alive == True) or game_class.gamemode =="mirror":
            game_class.previous_pos.append(pygame.draw.rect(screen,players_lst[1].color,(players_lst[1].x+players_lst[1].x_speed,players_lst[1].y+players_lst[1].y_speed,8,8)))
            players_lst[1].current_rect = pygame.draw.rect(screen,players_lst[1].color,(players_lst[1].x+players_lst[1].x_speed,players_lst[1].y+players_lst[1].y_speed,8,8))
            players_lst[1].x += players_lst[1].x_speed
            players_lst[1].y += players_lst[1].y_speed
        if game_class.players >= 3 and players_lst[2].alive == True:
            game_class.previous_pos.append(pygame.draw.rect(screen,players_lst[2].color,(players_lst[2].x+players_lst[2].x_speed,players_lst[2].y+players_lst[2].y_speed,8,8)))
            players_lst[2].current_rect = pygame.draw.rect(screen,players_lst[2].color,(players_lst[2].x+players_lst[2].x_speed,players_lst[2].y+players_lst[2].y_speed,8,8))
            players_lst[2].x += players_lst[2].x_speed
            players_lst[2].y += players_lst[2].y_speed
        if game_class.players == 4 and players_lst[3].alive == True:
            game_class.previous_pos.append(pygame.draw.rect(screen,players_lst[3].color,(players_lst[3].x+players_lst[3].x_speed,players_lst[3].y+players_lst[3].y_speed,8,8)))
            players_lst[3].current_rect = pygame.draw.rect(screen,players_lst[3].color,(players_lst[3].x+players_lst[3].x_speed,players_lst[3].y+players_lst[3].y_speed,8,8))
            players_lst[3].x += players_lst[3].x_speed
            players_lst[3].y += players_lst[3].y_speed
        for i in range(len(game_class.previous_pos)-game_class.players - mirror_gamemode): # Deals with collision
            if game_class.players == 2 or game_class.gamemode == "mirror":
                if (players_lst[0].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    if game_class.gamemode == "mirror":
                        message_to_screen("AI Wins",white,controls_title_font,True,True)
                    else:
                        message_to_screen("Player 2 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
                elif (players_lst[1].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    message_to_screen("Player 1 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
            if game_class.players == 3:
                if (players_lst[0].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[0].alive = False
                if (players_lst[1].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[1].alive = False
                if (players_lst[2].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[2].alive = False
            elif game_class.players == 4:
                if (players_lst[0].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[0].alive = False
                if (players_lst[1].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[1].alive = False
                if (players_lst[2].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[2].alive = False
                if (players_lst[3].current_rect).colliderect(game_class.previous_pos[i]) == 1:
                    players_lst[3].alive = False
        if game_class.players == 3 or game_class.players == 4:
            total_alive = 0
            for i in range(len(players_lst)):
                if players_lst[i].alive == True:
                    total_alive += 1
            if total_alive == 1: # Checks for a winner
                if players_lst[0].alive == True:
                    message_to_screen("Player 1 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
                elif players_lst[1].alive == True:
                    message_to_screen("Player 2 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
                elif players_lst[2].alive == True:
                    message_to_screen("Player 3 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
                else:
                    message_to_screen("Player 4 Wins",white,controls_title_font,True,True)
                    pygame.display.update()
                    time.sleep(3)
                    game_over_screen(players_lst,game_class,positions)
        pygame.display.update()
        clock.tick(120)
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def game_over_screen(players_lst,game_class,positions):
    '''
    A function that draws the Game Over screen

    game_class: A game_class object
    players_lst: A list of player-class objects
    positions: A list of positions of the rectangles in the background animation
    
    '''
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
        screen.fill(black)
        background_animation(positions)
        button_handler("Play Again",200,150,250,250,turquoise,light_turquoise,"game",game_class,players_lst)
        button_handler("Main Menu",574,150,250,250,pink,light_pink,"main",None,None)
        button_handler("Gamemodes",200,650,250,250,purple,light_purple,"gamemode",None,None)
        if game_class.gamemode == "free for all":
            button_handler("Colors",574,650,250,250,green,light_green,"color2",game_class,players_lst)
        else:
            button_handler("Colors",574,650,250,250,green,light_green,"color1",game_class,players_lst)
        pygame.display.update()
    pygame.display.quit()
    pygame.quit()
    sys.exit()

# PyGame Initialization
pygame.init()
clock = pygame.time.Clock()

# Creating the positions list for the background animation
positions = [] # Global variable for a seamless transition of the animation between screens
for j in range(17):
    positions.append([random.randrange(-1000,-100,50),random.randrange(1,1024,50)])
    
# Fonts
title_font = pygame.font.Font("Vermin Vibes 1989 by Chequered Ink.ttf", 150)
subtitle_font = pygame.font.Font("Vermin Vibes 1989 by Chequered Ink.ttf",30)
button_font = pygame.font.Font("8-bit-pusab.ttf",15)
controls_title_font = pygame.font.Font("8-bit-pusab.ttf",85)
player_title_font = pygame.font.Font("8-bit-pusab.ttf",20)

# Colors
red = (255,80,80) 
light_red = (255,120,120) 
dark_red = (255,30,80)
orange = (255,128,0)
light_orange = (255,170,0)
dark_orange = (255,90,0)
purple = (102,0,204) 
light_purple = (178,102,255)
dark_purple = (80,0,204)
green = (20,255,80) 
light_green = (120,255,120)
dark_green = (52,111,43)
blue = (80,80,255) 
light_blue = (120,120,255) 
neon_blue = (25,238,238) 
dark_blue = (0,0,153) 
turquoise = (0,204,204)
light_turquoise = (0,224,204)
dark_turquoise = (0,170,204)
pink = (255,100,255)
light_pink = (255,150,255)
dark_pink = (255,65,255)
yellow = (255,255,150)
light_yellow = (255,255,200)
dark_yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255) 
light_grey = (171,172,159)
grey = (96,96,96)

# Window size and Screen
screen_x,screen_y = 1024,1024
screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Lightcycle")

# Starts the game
intro_background()
intro_animation()
pygame.mixer.music.load("Daft Punk - Derezzed (8-bit NES version).mp3")
pygame.mixer.music.play(-1)
start_screen(positions)

