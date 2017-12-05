import pygame
from PowerChess import * 

class Square:
   def __init__(self,colour):
      self.initial_colour = colour
      self.colour = colour
      self.powerup = None
      self.piece = None
   
   def add_piece(self, piece, new_pos):
      self.piece = piece
      self.piece.pos = new_pos

   def remove_piece(self):
      self.piece = None

   def is_square_empty(self):
      if piece == None:
         return True
      return False 

class Player():
   def __init__(self,colour, connection):
      self.colour = colour
      self.connection = connection



class Piece:
   def __init():
      return

class Pawn(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "Pawn"
      if colour == "white":
         self.picture = pygame.image.load("images/whitepawn.png")
      else:
         self.picture = pygame.image.load("images/blackpawn.png")


   def is_legal(self, new_pos,board):
      if self.colour == "white":
         if self.pos > 47 and self.pos < 56: #if it hasn't moved yet
            if self.pos - new_pos == 16 and board[self.pos - 8].piece == None:
               return (board[new_pos].piece == None)
         if self.pos - new_pos == 8 and board[new_pos].piece == None:
            return True
         if (self.pos - new_pos) in [7,9] and board[new_pos].piece != None:
            return True
         return False
      else:
         if self.pos > 7 and self.pos < 16: #if it hasn't moved yet 
            if new_pos - self.pos == 16 and board[self.pos + 8].piece == None:
               return (board[new_pos].piece == None)
         if new_pos - self.pos == 8 and board[new_pos].piece == None:
            return True
         if (new_pos - self.pos) in [7,9] and board[new_pos].piece != None:
            return True
         return False
class Rook(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "Rook"
      if colour == "white":
         self.picture = pygame.image.load("images/whiterook.png")
      else:
         self.picture = pygame.image.load("images/blackrook.png")

   def is_legal(self, new_pos,board):
      #first test moving forwards
      i = 8
      while (self.pos + i) > -1 and (self.pos + i) < 64:
         if (self.pos+i) == new_pos:
            return True
         if board[self.pos+i].piece != None:
            break
         i += 8
      #now test moving backwards
      i = 8
      while (self.pos - i) > -1 and (self.pos - i) < 64:
         if (self.pos-i) == new_pos:
            return True
         if board[self.pos-i].piece != None:
            break
         i += 8
      #now moving right
      i = 1
      while i < 8 and new_pos > self.pos:
         if (self.pos+i) == new_pos:
            return True
         if (self.pos+i+1) % 8 == 0 or board[self.pos+1].piece != None:
            break
         i += 1
      #now move left
      i = 1
      while i < 8 and self.pos > new_pos:
         if (self.pos-i) == new_pos:
            return True
         if (self.pos-i) % 8 == 0 or board[self.pos-1].piece != None:
            return False
         i += 1

      return False

class Knight(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "Knight"
      if colour == "white":
         self.picture = pygame.image.load("images/whiteknight.png")
      else:
         self.picture = pygame.image.load("images/blackknight.png")

   def is_legal(self, new_pos,board):
      return (self.pos - new_pos) in [-17, -15, -10, -6, 6, 10, 15, 17] and abs(self.pos//8 - new_pos //8)!= 0

class Bishop(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "Bishop"
      if colour == "white":
         self.picture = pygame.image.load("images/whitebishop.png")
      else:
         self.picture = pygame.image.load("images/blackbishop.png")

   def is_legal(self, new_pos,board):
      #first test moving forwards and right
      i = 9
   
      while (self.pos + i) > -1 and (self.pos + i) < 64:
         if (self.pos+i) == new_pos:
            return True
         if board[self.pos+i].piece != None or (self.pos+i+1) % 8 == 0:
            break
         i += 9
      #now test moving backwards and right
      i = 9
      while (self.pos - i) > -1 and (self.pos - i) < 64:
         if (self.pos-i) == new_pos:
            return True
         if board[self.pos-i].piece != None or (self.pos-i) % 8 == 0:
            break
         i += 9
      #now moving forwards and left
      i = 7
      while (self.pos + i) > -1 and (self.pos + i) < 64:
         if (self.pos+i) == new_pos:
            return True
         if board[self.pos+i].piece != None or (self.pos+i) % 8 == 0:
            break
         i += 7
      #finally backwards and right
      i = 7
      while (self.pos - i) > -1 and (self.pos - i) < 64:
         if (self.pos-i) == new_pos:
            return True
         if board[self.pos-i].piece != None or (self.pos-i+1) % 8 == 0:
            break
         i += 7
      return False

class Queen(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "Queen"
      if colour == "white":
         self.picture = pygame.image.load("images/whitequeen.png")
      else:
         self.picture = pygame.image.load("images/blackqueen.png")

   def is_legal(self, new_pos,board):
      bishop = Bishop(self.colour,self.pos)
      rook = Rook(self.colour,self.pos)
      return bishop.is_legal(new_pos,board) or rook.is_legal(new_pos,board)

class King(Piece): 
   def __init__(self, colour,pos):
      self.colour = colour
      self.pos = pos
      self.pieceType = "King"
      if colour == "white":
         self.picture = pygame.image.load("images/whiteking.png")
      else:
         self.picture = pygame.image.load("images/blackking.png")

   def is_legal(self, new_pos,board):
      if self.pos % 8 == 0: 
         return (self.pos - new_pos) in [-9,-8,-1,7,8]
      if self.pos % 8 == 7: 
         return (self.pos - new_pos) in [-8,-7,1,8,9]
      else:
         return (self.pos - new_pos) in [-9,-8,-7,-1,1,7,8,9]
