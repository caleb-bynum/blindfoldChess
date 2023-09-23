# Author: Caleb Bynum
# This is the main/driver program to run my blindfold chess project


import chess
import pygame as pg

# init chess board class
board = chess.Board() 
print(board)
print(board.board_fen())

#init pygame
pg.init()
screen = pg.display.set_mode((800,1000))
pg.draw.rect
#init user parameters
user_color = True #True is white, ...
user_move = ""
engine_level = 1 #level from 1-10


#ask color you want to play as/if you want to quit
#ask engine level (1-10)


#Functions
#loop exit flag
continue_game = True
# GAME LOOP
while continue_game:
    #check if game is over (stalemate, checkmate, insuff material)
    if board.is_checkmate():
        if board.turn:
            #black wins
            pass
        else:
            #white wins 
            pass

    if board.is_insufficient_material():
        pass
        # draw by insuff material

    if board.is_stalemate():
        #draw by stalemate
        pass

    if board.can_claim_threefold_repetition():
        #draw by repitition
        pass
        #if so, print result to pygame
        #make infinite loop
   
 
    #read move from user
    if user_move == "q" or user_move == "quit":
        break
    #if move is "q" or "quit", break loop
    elif user_move == "t" or user_move == "toggle":
        continue
    #else if move is "toggle" or "t", 
        #use pygame to remove/add pieces 
        #continue
    elif user_move in board.legal_moves:
        board.push_lan(user_move) 
    #else if is_legal_move
        #then push_lan(move)
    else:
        continue 
    #else say ILLEGAL MOVE in pygame, continue


    #check if game is over (stalemate, checkmate, insuff material)
    if board.is_checkmate():
        if board.turn:
            #black wins
            pass
        else:
            #white wins 
            pass

    if board.is_insufficient_material():
        pass
        # draw by insuff material

    if board.is_stalemate():
        #draw by stalemate
        pass

    if board.can_claim_threefold_repetition():
        #draw by repitition
        pass
        #if so, print result to pygame
        #make infinite loop


    #generate engine move
    #add to board

    #update board state thru pygame
    pass
    
    
    
    
    
     
