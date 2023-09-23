import pygame as pg # game UI
import chess # game logic
import chess.engine # for stockfish integration
import sys # for sys.exit()
import time # for time.sleep()
from VarTracker import * # to track variables manipulated in game loops
import pyttsx3 # enables speech output
import threading # for TTS thread
import queue # TTS buffer queue
import random


########################### API initialization and constant definitions #######################
in_game = True
pg.init()

engine = chess.engine.SimpleEngine.popen_uci("/Users/cjb/code/credera/blindfoldchess/s/14/bin/stockfish")
voice = pyttsx3.init()
while in_game:

    AQUA = (31,181,192)
    FPS = 60
    PINKISH = (232,28,137)

    window = (800,900)
    board_size = (800,800)
    square_size = (100,100)

    pg.display.set_caption('Chess Trainer')
    screen = pg.display.set_mode(window)

    input_box = pg.Rect(0,800,200,100)
    output_box = pg.Rect(200, 800, 400,100)
    toggle_box = pg.Rect(600,800,200,100)
    color_hide = (10,200,60)
    color_show = (12,240,65)
    color_input_inactive = pg.Color('lightskyblue3')
    color_input_active = pg.Color('dodgerblue2')
    color = color_input_inactive
    toggle_color = color_show
    active = False
    text = ""
    font = pg.font.Font("helvetica.ttf",32)
    small_font = pg.font.Font("helvetica.ttf",25)

    clock = pg.time.Clock()

    background = pg.Surface(screen.get_size())

    screen.fill((0,0,0))


    vt = VarTracker() # holds variables manipulated in loops


    ################################## Load game sprites ###############################
    # Load Board PNG
    boardImgUnscaled = pg.image.load('board.png')
    boardImg = pg.transform.scale(boardImgUnscaled, board_size).convert()

    #Load Piece PNGs
    bB = pg.image.load('bB.png')
    bB.set_colorkey((0,0,0))
    bB = pg.transform.scale(bB, square_size)

    wB = pg.image.load('wB.png')
    wB.set_colorkey((0,0,0))
    wB = pg.transform.scale(wB,square_size)

    bK = pg.image.load('bK.png')
    bK.set_colorkey((0,0,0))
    bK = pg.transform.scale(bK, square_size)

    wK = pg.image.load('wK.png')
    wK.set_colorkey((0,0,0))
    wK = pg.transform.scale(wK, square_size)

    bN = pg.image.load('bN.png')
    bN.set_colorkey((0,0,0))
    bN = pg.transform.scale(bN, square_size)

    wN = pg.image.load('wN.png')
    wN.set_colorkey((0,0,0))
    wN = pg.transform.scale(wN, square_size)

    bR = pg.image.load('bR.png')
    bR.set_colorkey((0,0,0))
    bR = pg.transform.scale(bR, square_size)

    wR = pg.image.load('wR.png')
    wR.set_colorkey((0,0,0))
    wR = pg.transform.scale(wR, square_size)

    bQ = pg.image.load('bQ.png')
    bQ.set_colorkey((0,0,0))
    bQ = pg.transform.scale(bQ, square_size)

    wQ = pg.image.load('wQ.png')
    wQ.set_colorkey((0,0,0))
    wQ = pg.transform.scale(wQ, square_size)

    bp = pg.image.load('bp.png')
    bp.set_colorkey((0,0,0))
    bp = pg.transform.scale(bp, square_size)

    wp = pg.image.load('wp.png')
    wp.set_colorkey((0,0,0))
    wp = pg.transform.scale(wp, square_size)


    # Mapping of FENstring piece notation to piece image objects
    pieces = {  'P' : wp,
                'p' : bp,
                'B' : wB,
                'b' : bB,
                'N' : wN,
                'n' : bN,
                'R' : wR,
                'r' : bR,
                'Q' : wQ,
                'q' : bQ,
                'K' : wK,
                'k' : bK  }



    ############################ Board and Piece rendering functions ######################
    def blitBoard(x,y): # only renders board
        screen.blit(boardImg, (x,y))


    def blitPiece(x,y, pieceImg): # only renders piece
        screen.blit(pieceImg, (x,y))


    def parseAndBlit(fen, is_white): # parses FEN, renders board, renders piece, ouputs rendering
        blitBoard(0,0)

        rowStrings = fen.split('/')
        rows = [] #double array with each entry being a single char from the FEN string
        
        for rs in rowStrings:
            rows.append([c for c in rs])
        if is_white: 
            y = 0
            for row in rows:
                x = 0
                for char in row:
                    if char.isdigit():       
                        x += int(char) * square_size[0]
                    else:
                        blitPiece(x, y, pieces[char])  
                        x += square_size[0]
                y += square_size[1]
        else:
            y = 700
            for row in rows:
                x = 700
                for char in row:
                    if char.isdigit():       
                        x -= int(char) * square_size[0]
                    else:
                        blitPiece(x, y, pieces[char])  
                        x -= square_size[0]
                y -= square_size[1]
            


    ######################### Initial board render ###########################
    board = chess.Board() 
    parseAndBlit(board.board_fen(), vt.user_color)



    ############################## Beginning of Game (start menu component -- ask user for color) ###################
    move_on = False
    while not move_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                engine.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Changes color of input box if clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if toggle_box.collidepoint(event.pos):
                    toggle_color = color_show if vt.show_board else color_hide
                    vt.show_board = not vt.show_board 
                color = color_input_active if active else color_input_inactive

            if event.type == pg.KEYDOWN:
                # tracks user keyboard input into box
                if active:
                    if event.key == pg.K_RETURN:
                        move_on = True
                        if text == "w" or text == "white":
                            vt.user_color = True
                        else:
                            vt.user_color = False 
                        text = '' # reset texxt box
                    
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render output rectangle and text
        output_surface = font.render("white or black?", True, (0,0,0))
        pg.draw.rect(screen,PINKISH, output_box)
        screen.blit(output_surface, (output_box.x+5, output_box.y+5))

        
        # Render input text and rectangle
        text_surface = font.render(text, True, (0,0,0))
        width = max(200,text_surface.get_width() + 20)
        input_box.w = width
        pg.draw.rect(screen, color, input_box)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))


        # Render toggle box text and rectangle
        pg.draw.rect(screen, toggle_color, toggle_box)


        blitBoard(0,0)


        # update display and tick
        pg.display.flip()
        clock.tick(FPS)



    ########################## start menu component -- ask user for engine level #################
    move_on = False

    while not move_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                engine.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Changes color of input box if clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if toggle_box.collidepoint(event.pos):
                    toggle_color = color_show if vt.show_board else color_hide
                    vt.show_board = not vt.show_board 
                color = color_input_active if active else color_input_inactive

            if event.type == pg.KEYDOWN:
                # tracks user keyboard input into box
                if active:
                    if event.key == pg.K_RETURN:
                        move_on = True
                        vt.engine_level = int(text)
                        text = '' # reset texxt box
                    
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        # Render output rectangle and text
        output_surface = font.render("Engine Difficulty? (1-10)", True, (0,0,0))
        pg.draw.rect(screen,PINKISH, output_box)
        screen.blit(output_surface, (output_box.x+5, output_box.y+5))

        
        # Render input text and rectangle
        text_surface = font.render(text, True, (0,0,0))
        width = max(200,text_surface.get_width() + 20)
        input_box.w = width
        pg.draw.rect(screen, color, input_box)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))


        # Render toggle box text and rectangle
        toggle_surf = font.render("Toggle blindfold", True, (0,0,0)) 
        pg.draw.rect(screen, toggle_color, toggle_box)


        blitBoard(0,0)


        # update display and tick
        pg.display.flip()
        clock.tick(FPS)



    ####################### Setup before blindfold trainer loop ####################
    #convert engine level to engine time
    engine_time = vt.engine_level / 200
    # setup if user if black
    if not vt.user_color:
        cur_move = engine.play(board, chess.engine.Limit(time = engine_time)).move 
        vt.engine_move = board.san(cur_move)
        board.push(cur_move)



########## Thread that outputs speech(auto-starting thread)  #########
    class TTSThread(threading.Thread):
        def __init__(self,queue):
            threading.Thread.__init__(self)
            self.queue = queue
            self.daemon = True
            self.start()

        def run(self):
            tts_engine = pyttsx3.init()
            tts_engine.startLoop(False)
            t_running = True
    
            while t_running:
                if self.queue.empty():
                    tts_engine.iterate()
                else:
                    data = self.queue.get()
                    if data == "exit":
                        t_running = False
                    else:
                        tts_engine.say(data)
            tts_engine.endLoop()


# queue for putting speech comoponents
    q = queue.Queue()
    tts_thread = TTSThread(q) 

    #################### blindfold trainer loop (main loop) #################
    exit = False # terminate game loop

    # GAME LOOP
    while not exit:
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = True  
                pg.quit()
                engine.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Changes color of input box if clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if toggle_box.collidepoint(event.pos):
                    toggle_color = color_show if vt.show_board else color_hide
                    vt.show_board = not vt.show_board 
                color = color_input_active if active else color_input_inactive
            
            if event.type == pg.KEYDOWN:
                # tracks user keyboard input into box
                if active:
                    if event.key == pg.K_RETURN:
                        vt.should_output_speech = True
                        if text == "r" or text == "resign":
                            vt.user_resigned = True                       
                        vt.user_move = text #store current user move

                        text = '' # reset texxt box
                        try:
                            board.push_san(vt.user_move)
                    
                            cur_move = engine.play(board, chess.engine.Limit(time = engine_time)).move
                            vt.engine_move = board.san(cur_move)
                            board.push(cur_move)

                            vt.invalid_move = False
                        except ValueError:
                            vt.invalid_move = True
                    
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        # Render new board state only if user input valid move
        if not vt.invalid_move:
            fen = board.board_fen()
            parseAndBlit(fen, vt.user_color)
        
        # populate output box text
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                vt.output_box_text = "Checkmate! Black wins"
            else:
                vt.output_box_text = "Checkmate! White wins"
            exit = True
        elif board.is_stalemate():
            vt.output_box_text = "Draw by stalemate!"
            exit = True
        elif board.can_claim_threefold_repetition():
            vt.output_box_text = "Draw by repitition!"
            exit = True
        elif board.is_insufficient_material():
            vt.output_box_text = "Draw by insufficient material!"
            exit = True
        elif vt.user_resigned:  
            exit = True
            if vt.user_color:
                vt.output_box_text = ("Black wins by resignation!")
            else:
                vt.output_box_text = ("White wins by resignation!")
        elif vt.invalid_move:
            vt.output_box_text = "Invalid move, try again"
        else:
            vt.output_box_text = "Engine plays: " + vt.engine_move
            
                
        # Render output rectangle and text
        output_surface = font.render(vt.output_box_text, True, (0,0,0))
        pg.draw.rect(screen,PINKISH, output_box)
        screen.blit(output_surface, (output_box.x+5, output_box.y+5))


        # Speak output as well
        if (vt.should_output_speech):
            q.put(vt.output_box_text)
            vt.should_output_speech = False


        
        # Render input text and rectangle
        text_surface = font.render(text, True, (0,0,0))
        width = max(200,text_surface.get_width() + 20)
        input_box.w = width
        pg.draw.rect(screen, color, input_box)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))


        # Render toggle box text and rectangle
        toggle_surface = small_font.render("Toggle blindfold", True, (0,0,0)) 
        pg.draw.rect(screen, toggle_color, toggle_box)
        screen.blit(toggle_surface, (toggle_box.x+5, toggle_box.y+5))
        # reset loop controls
        vt.user_move = ""


        # hide board if needed
        if not vt.show_board:
            blitBoard(0,0)


        # update display and tick
        pg.display.flip()
        clock.tick(FPS)


    move_on = False
    time.sleep(4)
    while not move_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                engine.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Changes color of input box if clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if toggle_box.collidepoint(event.pos):
                    toggle_color = color_show if vt.show_board else color_hide
                    vt.show_board = not vt.show_board 
                color = color_input_active if active else color_input_inactive

            if event.type == pg.KEYDOWN:
                # tracks user keyboard input into box
                if active:
                    if event.key == pg.K_RETURN:
                        move_on = True
                        if text == "y" or text == "yes":
                            in_game = True
                        else:
                            in_game = False
                        text = '' # reset texxt box
                    
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        # Render output rectangle and text
        output_surface = font.render("Play again? yes or no", True, (0,0,0))
        pg.draw.rect(screen,PINKISH, output_box)
        screen.blit(output_surface, (output_box.x+5, output_box.y+5))

        
        # Render input text and rectangle
        text_surface = font.render(text, True, (0,0,0))
        width = max(200,text_surface.get_width() + 20)
        input_box.w = width
        pg.draw.rect(screen, color, input_box)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))


        # Render toggle box text and rectangle
        toggle_surf = font.render("Toggle blindfold", True, (0,0,0)) 
        pg.draw.rect(screen, toggle_color, toggle_box)

        #render board state
        fen = board.board_fen()
        parseAndBlit(fen, vt.user_color)

        pg.display.flip()
        clock.tick(FPS)





pg.quit()
engine.quit()
sys.exit()
