#!/usr/bin/python3
# Set the path to your python3 above

# Set up relative path for util; sys.path[0] is directory of current program
import os, sys
utilpath = sys.path[0] + "/../util/"
sys.path.append(utilpath)

from gtp_connection_go2 import GtpConnectionGo2
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard

class Go2():
    def __init__(self):
        """
        Player that selects moves randomly from the set of legal moves.
        With the fill-eye filter.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go2"
        self.version = 0.1

    def get_move(self,board, color):
        return GoBoardUtil.generate_random_move(board,color,True)
    
    def solve(self, board, komi):
        copy_board = SimpleGoBoard(board.size)        
        copy_board = GoBoardUtil.copyb2b(board, board)
        
        # depth limit
        d = 7
        
        success, score = self.negamaxBoolean(copy_board, copy_board.current_player, komi, d)
        print("!!!!!!!!!!!!!!!!!!", success, score)
        return 1, "a1"
    
    def negamaxBoolean(self, board, color, komi, d):
        
        LegalMoves = GoBoardUtil.generate_legal_moves(board, color).split()
        
        if len(LegalMoves) == 0 or d == 0:
            winning_color, score = board.score(komi)
            if winning_color == color:
                return True, score
            else:
                return False, score
            
        losing_moves = []
        
        #print(LegalMoves)
        #print(GoBoardUtil.generate_legal_moves(board, color))
        
        for m in LegalMoves:
         
        #for m in GoBoardUtil.generate_legal_moves(board, color).split():
            
            move = GoBoardUtil.move_to_coord(m, board.size)
            move = board._coord_to_point(move[0],move[1])
            
            
            board.move(move, color)   
            
            #print(board.board)
            
            success, points = self.negamaxBoolean(board, GoBoardUtil.opponent(color), komi, d-1)
            success = not success 
            board.undo_move()
            
            print("\n", m, move, color, success)
            
            if success:
                return True, str(points) + str([m])
            
            if losing_moves == []:
                losing_moves = str(points) + str([m])
                
        return False, losing_moves
            
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnectionGo2(Go2(), board)
    con.start_connection()

if __name__=='__main__':
    run()
