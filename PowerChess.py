import sys
import pygame
import random
import socket
from pygame.locals import *
from ChessClasses import *


#Images
WHITESQR = pygame.image.load("images/white.png")
BLACKSQR = pygame.image.load("images/black.png")
GREENSQR = pygame.image.load("images/greenPowerUpSquare.png")
BLUESQR = pygame.image.load("images/bluePowerUpSquare.png")
REDSQR = pygame.image.load("images/redPowerUpSquare.png")
YELLOWSQR = pygame.image.load("images/yellow.png")
MainView = pygame.image.load("images/MainView.png")
WhitesTurn = pygame.image.load("images/Whites-turn.png")
BlacksTurn = pygame.image.load("images/Blacks-turn.png")
BlackWins = pygame.image.load("images/BlackWins.png")
WhiteWins = pygame.image.load("images/WhiteWins.png")
OpeningScreen = pygame.image.load("images/Opening Screen.png")
Background = pygame.image.load("images/blueBackgroud.png")
Offline = pygame.image.load("images/offline.png")

WHITE =         (216,216,216)
BLACK =         ( 39, 39, 39)

global board
global player

def set_up_board():
   board = [0] * 64
   square_colour = WHITESQR
   for i in range(64):
      board[i] = Square(square_colour)
      if (i+1) % 8 != 0:
         square_colour = change_colour(square_colour)
   board[0].piece = Rook("black", 0)
   board[7].piece = Rook("black", 7)
   board[56].piece = Rook("white", 56)
   board[63].piece = Rook("white", 63)
   board[1].piece = Knight("black", 1)
   board[6].piece = Knight("black", 6)
   board[57].piece = Knight("white", 57)
   board[62].piece = Knight("white", 62)
   board[2].piece = Bishop("black", 2)
   board[5].piece = Bishop("black", 5)
   board[58].piece = Bishop("white", 58)
   board[61].piece = Bishop("white", 61)
   board[3].piece = Queen("black", 3)
   board[59].piece = Queen("white", 59)
   board[4].piece = King("black", 4)
   board[60].piece = King("white", 60)
   for i in range(8,16):
      board[i].piece = Pawn("black", i)
   for i in range(48,56):
      board[i].piece = Pawn("white", i)
   return board

def draw_board():
   row = 0
   column = 0
   for i in range(64):
      if row == 8:
         column += 1
         row = 0
      DISPLAY.blit(board[i].colour, (row * 60, column * 60))
      row+= 1
   for i in range(0,64):
      if board[i].piece != None:
         DISPLAY.blit(board[i].piece.picture, (i%8 * 60, i//8 * 60))
   pygame.display.update()

def welcome_screen():
    global player
    while True:
        for event in pygame.event.get():
            DISPLAY.blit(OpeningScreen,(0,0))
            DISPLAY.blit(Offline,(250,340))
            pygame.display.update()

            if event.type == QUIT:
                quit_game()

            if event.type == MOUSEBUTTONUP:
               if event.pos[0] > 250 and event.pos[0] < 550 and event.pos[1] > 240 and event.pos[1] < 300: #join game button
                  hostname = socket.gethostname()
                  host = socket.gethostbyname(hostname)
                  DISPLAY.blit(Background,(0,0))
                  myfont = pygame.font.SysFont('Comic Sans MS', 30)
                  textsurface = myfont.render("Waiting for player to join...", True, WHITE)
                  DISPLAY.blit(textsurface,(100,140))
                  textsurface = myfont.render("They'll need your IP address:"+host, True, WHITE)
                  DISPLAY.blit(textsurface,(100,240))
                  pygame.display.update()
                  port = 8002

                  s = socket.socket()
                  s.bind((host,port))
                  s.listen(1000)
                  c, addr = s.accept()
                  player = Player("white", c)
                  return chess_game()

               elif event.pos[0] > 250 and event.pos[0] < 550 and event.pos[1] > 140 and event.pos[1] < 200: #create game button
                  host = get_host()
                  port = 8002
                  s = socket.socket()
                  s.connect((host,port))
                  player = Player("black", s)
                  return chess_game()

               elif event.pos[0] > 250 and event.pos[0] < 550 and event.pos[1] > 340 and event.pos[1] < 400:
                  player = Player("both", None)
                  return chess_game()

def get_host():
    IP = ""
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    IP = IP[:-1]
                elif event.key == K_RETURN:
                    return IP
                else:
                   IP += event.unicode

        DISPLAY.fill(BLACK)
        DISPLAY.blit(Background,(0,0))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Enter host's IP:" + IP, True, WHITE)
        DISPLAY.blit(textsurface,(140,200))
        pygame.display.update()

def chess_game():
    global board
    DISPLAY.blit(MainView,(0, 0))
    DISPLAY.blit(WhitesTurn,(555, 20))
    turn_colour = "white"
    turn = 1;
    board = set_up_board()
    while True:
        draw_board()
        pygame.display.update()
        if player.colour == "both": #offline game
           item_pos = choose_piece(turn_colour)
           
        elif turn_colour == player.colour:
            item_pos = choose_piece(turn_colour)
            player.connection.send(str(item_pos).encode('utf-8'))

        else:
            item_pos = player.connection.recv(1024)
            item_pos = item_pos.decode("utf-8")

        item_pos = int(item_pos)
        row = item_pos //8
        column = item_pos % 8
        if board[item_pos].piece != None and board[item_pos].piece.colour == turn_colour:
           DISPLAY.blit(YELLOWSQR,((column)*60, (row)*60))
           DISPLAY.blit(board[item_pos].piece.picture,((column)*60, (row)*60))
           pygame.display.update()
           move_made = move_to(item_pos,column,row,turn_colour)
           if move_made:
              turn_colour = change_turn(turn_colour)
              turn += 1
              if (turn % 7) == 0:
                 turn_on_powerup(turn_colour)


def move_to(starting_pos,row,column,turn_colour):
   while True:
      for event in pygame.event.get():
          if player.colour == "both": #offline game
            item_pos = choose_piece(turn_colour)
           
          elif turn_colour == player.colour:
             item_pos = choose_piece(turn_colour)
             player.connection.send(str(item_pos).encode('utf-8'))

          else:
             item_pos = player.connection.recv(1024)
             item_pos = item_pos.decode("utf-8")
             
          move_pos = int(item_pos)

          if board[starting_pos].colour == "white":
             DISPLAY.blit(WHITESQR,((row)*60, (column)*60))
          else:
             DISPLAY.blit(BLACKSQR,((row)*60, (column)*60))
          if board[starting_pos].piece != None:
             DISPLAY.blit(board[starting_pos].piece.picture,((row)*60, (column)*60))
             pygame.display.update()
          if not is_legal_move(move_pos, starting_pos, turn_colour):
                #print("Illegal move")
                return False
          else:
             new_pos = move_pos
             if board[new_pos].piece != None:
                if board[new_pos].piece.pieceType == "King":
                   if turn_colour == "white":
                      whitewins()
                   else:
                      blackwins()
                board[new_pos].remove_piece()
             board[new_pos].add_piece(board[starting_pos].piece, new_pos) #moves piece to new position
             board[starting_pos].remove_piece()
             if board[new_pos].powerup != None:
                board[new_pos].colour = board[new_pos].initial_colour
                draw_board()
                pygame.display.update()
                if board[new_pos].powerup == "blue":
                   blue_powerup(turn_colour)
                if board[new_pos].powerup == "green":
                   green_powerup(turn_colour)
                if board[new_pos].powerup == "red":
                   red_powerup(turn_colour)
                board[new_pos].powerup = None
               # print("legal move")
             return True

def is_legal_move(new_pos, starting_pos,colour):
   if board[new_pos].piece != None:
      if board[new_pos].piece.colour == colour:
         return False #always false
   if starting_pos == new_pos:
      return False
   return board[starting_pos].piece.is_legal(new_pos,board)



def change_turn(colour):
   if colour == "white":
      DISPLAY.blit(BlacksTurn,(555, 20))
      return "black"
   DISPLAY.blit(WhitesTurn,(555, 20))
   return "white"

def change_colour(colour):
   if colour == WHITESQR:
      return BLACKSQR
   return WHITESQR

def choose_piece(turn_colour):
   while True:
      for event in pygame.event.get():
         if event.type == QUIT:
             quit_game()
            
         if event.type == KEYUP:
             if turn_colour == "white":
                blackwins() # due to forfeit
             else:
                whitewins()
         if event.type == MOUSEBUTTONUP:
            column = event.pos[0] // 60
            row = event.pos[1] // 60
            return column + (row*8)


def turn_on_powerup(turn_colour):
   random_square = random.randint(0,63)
   while board[random_square].piece != None or board[random_square].powerup != None:
      random_square = random.randint(0,63)
   powerups = ["red","red","red","green","blue"]
   random_powerup = random.randint(0, 4)
   if player.colour == "white":
      player.connection.send(str(random_square).encode('utf-8'))
      player.connection.send(str(random_powerup).encode('utf-8'))
   elif player.colour == "black":
      random_square = player.connection.recv(1024)
      random_square = random_square.decode("utf-8")
      random_powerup = player.connection.recv(1024)
      random_powerup = random_powerup.decode("utf-8")
   print(random_square)
   random_square = int(random_square)
   random_powerup = int(random_powerup)
   powerup = powerups[random_powerup]
   row = random_square //8
   column = random_square % 8
   board[random_square].powerup = powerup
   if powerup == "blue":
      board[random_square].colour = BLUESQR
   if powerup == "green":
      board[random_square].colour = GREENSQR
   if powerup == "red":
      board[random_square].colour = REDSQR

def red_powerup(turn_colour):
   while True:
      if player.colour == "both":
         item_pos = choose_piece(turn_colour)
          
      elif turn_colour == player.colour:
         item_pos = choose_piece(turn_colour)
         player.connection.send(str(item_pos).encode('utf-8'))

      else:
         item_pos = player.connection.recv(1024)
         item_pos = item_pos.decode("utf-8")
             
             
      item_pos = int(item_pos)
      row = item_pos //8
      column = item_pos % 8
      if board[item_pos].piece != None and board[item_pos].piece.colour == turn_colour:
         DISPLAY.blit(YELLOWSQR,((column)*60, (row)*60))
         DISPLAY.blit(board[item_pos].piece.picture,((column)*60, (row)*60))
         pygame.display.update()
         move_made = move_to(item_pos,column,row,turn_colour)
         if move_made:
            return 


def blue_powerup(colour):
   if colour == "black":
      range = [8,9,10,11,12,13,14,15]
   else:
      range =[48,49,50,51,52,53,54,55]
   for i in range:
      if board[i].piece == None and colour == "black":
         piece = Pawn("black",i)
         board[i].add_piece(piece, i)
         row = i//8
         col = i % 8

   for i in range:
      if board[i].piece == None and colour == "white":
         piece = Pawn("white",i)
         board[i].add_piece(piece, i)
         row = i//8
         col = i % 8
   return

def green_powerup(colour):
   random_square = random.randint(0,63)
   while board[random_square].piece != None or board[random_square].powerup != None or besideKing(random_square, colour) == True:
      random_square = random.randint(0,63)
   if player.colour == "white":
      player.connection.send(str(random_square).encode('utf-8'))
   elif player.colour == "black":
      random_square = player.connection.recv(1024)
      random_square = random_square.decode("utf-8")
   random_square = int(random_square)

   row = random_square //8
   column = random_square % 8
   queen_pos = find_king(colour)
   if colour == "white":
       print(board[queen_pos].piece)
       new_king = King("black", random_square)
       board[random_square].add_piece(new_king,random_square)
       board[queen_pos].remove_piece()

   if colour == "black":
       print(board[queen_pos].piece)
       new_king = King("white", random_square)
       board[random_square].add_piece(new_king, random_square)
       board[queen_pos].remove_piece()
      
def find_king(colour):
   if colour == "white":
      colour = "black"
   else:
      colour = "white"
   i = 0
   while True:
      if board[i].piece != None:
         if board[i].piece.colour == colour and board[i].piece.pieceType == "King": #there should be 2 kings on the board at all times
            return i
      i += 1
   			
def besideKing(random_square, colour):
   for i in [-9,-8,-7,-1,1,7,8,9]:
      if (random_square + i) < 64 and (random_square + i) > 1 and board[random_square+i].piece != None: #if its in range and has a piece
         if board[random_square+i].piece.colour == colour and board[random_square+i].piece.pieceType == "king":
            return True
   return False

def whitewins():
   DISPLAY.blit(WhiteWins,(0,0))
   pygame.display.update()
   pygame.time.wait(500) #shows end screen for 5 seconds  
   quit_game()

def blackwins():
   DISPLAY.blit(BlackWins,(0,0))
   pygame.display.update()
   pygame.time.wait(500)
   quit_game()

def main():
    global DISPLAY
    pygame.init()
    pygame.display.set_caption('Power Chess')
    DISPLAY = pygame.display.set_mode((800, 480))


    while True:
        welcome_screen()

def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
