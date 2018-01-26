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

class GtpConnectionGo1(gtp_connection.GtpConnection):
    
    
    
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
        self.commands["hello"] = self.hello_cmd
        self.commands["score"] = self.score_cmd
    

    def hello_cmd(self, args):
        """ Dummy Hello Command """
        self.respond("Hello! " + self.go_engine.name)
    
    def score_cmd(self, args):
        """ Scoring function for Assignment 1 """
        
        pointArray = []
        territoryArray = []
        
        correctionFactor = self.board.size+2
        
        scoreBoard = self.board.board
        for i in range(len(scoreBoard)):
            if scoreBoard[i] == 0:
                points,territory = self._explore_bfs(i-correctionFactor, scoreBoard, correctionFactor)
                pointArray.append(points)
                territoryArray.append(territory)
                for p in points:
                    scoreBoard[p+correctionFactor] = 9
                
        self.respond(str(scoreBoard)+"\n"+str(self.board.get_twoD_board())+"\n"+str(pointArray)+"\n"+str(territoryArray))
        #self.respond(str(scoreBoard)+"\n"+str(self.board.get_empty_positions(1)))
    
    def _explore_bfs(self, point, scoreBoard, correctionFactor):
        Open = []
        Territory = set()
        Open.append(point)
        Closed = set()
        while Open:
            v = Open.pop(0)
            Closed.add(v)
            for child in self._neighbors(v):
                #if self._in_bounds(scoreBoard, child+correctionFactor):
                if scoreBoard[child+correctionFactor] == 0 and child not in Closed:
                    if child not in Open:
                        Open.append(child)
                elif scoreBoard[child+correctionFactor] in [1,2]:
                    Territory.add(child)
        return Closed, Territory
    
    # copied from simple_board.py
    def _neighbors(self,point):
        """
        All neighbors of the point
        Arguments
        ---------
        point

        Returns
        -------
        points : list of int
            coordinate of points which are neighbors of the given point
        """
        #row,col = self._point_to_coord(point)
        #if 0 <= row <= self.size+1 and 0 <= col <= self.size+1:
        return [point-1, point+1, point-self.board.NS, point+self.board.NS]
        #else:
        #    raise ValueError("This point is out of range!")
    
    def _in_bounds(self, scoreBoard, index):
        """ 
        Checks if in bounds 
        
        returns : True if in bounds, False if not
        """
        
        try:
            test = scoreBoard[index]
            return True
        except:
            return False
        
        
        
        
        
        
        
        
        