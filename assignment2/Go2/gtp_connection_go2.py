"""
Module for playing games of Go using GoTextProtocol

This code is based off of the gtp module in the Deep-Go project
by Isaac Henrion and Aamos Storkey at the University of Edinburgh.
"""
import traceback
import sys
import os
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL
import gtp_connection
import numpy as np
import re
import timeit
from simple_board import SimpleGoBoard

TIMELIMIT = 1

class GtpConnectionGo2(gtp_connection.GtpConnection):
    
    #timelimit = 1
    
    def __init__(self, go_engine, board, outfile = 'gtp_log', debug_mode = False):
        """
        GTP connection of Go1

        Parameters
        ----------
        go_engine : GoPlayer
            a program that is capable of playing go by reading GTP commands
        komi : float
            komi used for the current game
        board: GoBoard
            SIZExSIZE array representing the current board state
        """
        gtp_connection.GtpConnection.__init__(self, go_engine, board, outfile, debug_mode)
        self.commands["go_safe"] = self.safety_cmd
        self.argmap["go_safe"] = (1, 'Usage: go_safe {w,b}')
        #self.timelimit = 1
        self.commands["timelimit"] = self.timelimit_cmd
        self.commands["solve"] = self.solve_cmd
        
    def timelimit_cmd(self, args):
        """ TO IMPLEMENT, takes arg: seconds """
        try:
            if int(args[0]) >= 1 and int(args[0]) <= 100:
                TIMELIMIT = int(args[0])
                self.go_engine.changeTimeLimit(TIMELIMIT)
            self.respond("")
        except Exception as e:
            self.respond('Error: {}'.format(str(e)))
    
    def solve_cmd(self, args):
        """ TO IMPLEMENT """
        winner, move = self.go_engine.solve(self.board, self.go_engine.komi)
        if winner == GoBoardUtil.opponent(self.board.current_player):
            self.respond(GoBoardUtil.int_to_color(winner))
        elif winner == self.board.current_player:
            self.respond(GoBoardUtil.int_to_color(winner) + " " + move)
        else:
            self.respond("unknown")
            
    def solve_cmd2(self, args):
        """ TO IMPLEMENT """
        color = args[0]
        print(color)
        if color == 'b':
            color = 1
        else:
            color = 2
        print(color)
        winner, move = self.go_engine.solve_for_color(self.board, color, self.go_engine.komi)
        print(winner, move)
            
        if winner == GoBoardUtil.opponent(self.board.current_player):
            return False
        elif winner == self.board.current_player:
            return move
        else:
            return -1
  
  
        
    def safety_cmd(self, args):
        try:
            color= GoBoardUtil.color_to_int(args[0].lower())
            safety_list = self.board.find_safety(color)
            safety_points = []
            for point in safety_list:
                x,y = self.board._point_to_coord(point)
                safety_points.append(GoBoardUtil.format_point((x,y)))
            self.respond(safety_points)
        except Exception as e:
            self.respond('Error: {}'.format(str(e)))

    def genmove_cmd(self, args):
        """
        generate a move for the specified color

        Arguments
        ---------
        args[0] : {'b','w'}
            the color to generate a move for
            it gets converted to  Black --> 1 White --> 2
            color : {0,1}
            board_color : {'b','w'}
        """
        
        
        move = self.solve_cmd2(args[0])
        print(move)
        
        if move != False and move != -1:
            
            if move != None:
                move_temp = GoBoardUtil.move_to_coord(move, self.board.size)
                move_temp = self.board._coord_to_point(move_temp[0],move_temp[1])
            else:
                move_temp = move
            self.board.move(move_temp, color)              
            self.respond(move)
        
        else:
            # if it is False or -1
            try:
                board_color = args[0].lower()
                color = GoBoardUtil.color_to_int(board_color)
                self.debug_msg("Board:\n{}\nko: {}\n".format(str(self.board.get_twoD_board()),
                                                              self.board.ko_constraint))
                move = self.go_engine.get_move(self.board, color)
                if move is None:
                    self.respond("pass")
                    return
        
                if not self.board.check_legal(move, color):
                    move = self.board._point_to_coord(move)
                    board_move = GoBoardUtil.format_point(move)
                    self.respond("Illegal move: {}".format(board_move))
                    raise RuntimeError("Illegal move given by engine")
        
                # move is legal; play it
                self.board.move(move,color)
        
                self.debug_msg("Move: {}\nBoard: \n{}\n".format(move, str(self.board.get_twoD_board())))
                move = self.board._point_to_coord(move)
                board_move = GoBoardUtil.format_point(move)
                self.respond(board_move)
            except Exception as e:
                self.respond('Error: {}'.format(str(e)))    