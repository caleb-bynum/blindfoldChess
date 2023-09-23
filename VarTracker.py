import chess
import chess.engine

class VarTracker:
    def __init__(self):
        self.user_move = ""
        self.user_color = True
        self.output_box_text = ""
        self.invalid_move = False
        self.engine_move = ""
        self.engine_level = 5
        self.show_board = False
        self.user_resigned = False 
        self.should_output_speech = False
        
       
  
