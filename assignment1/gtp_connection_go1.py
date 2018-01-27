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
        
        pointArray = []                         # holds the different points that make up territories 
        territoryArray = []                     # holds the territory boarders 
        correctionFactor = self.board.size+2    # adjustment factor for board to make computation easier 
        blackScore = 0                          # score for black player 
        whiteScore = 0                          # score for white player 
        scoreBoard = self.board.board           # copy of board to manipulate 
        
        # go through board and run bfs to find territories 
        for i in range(len(scoreBoard)):
            if scoreBoard[i] == 0:
                points,territory = self._explore_bfs(i-correctionFactor, scoreBoard, correctionFactor)
                pointArray.append(points)
                territoryArray.append(territory)
                for p in points:
                    # mark all with neutral territory = 9
                    scoreBoard[p+correctionFactor] = 9
                
        # check which player it belongs to and change it to theirs
        # Black territory = 7; White territory = 8; Neutral territory = 9
        if len(territoryArray) > 1:
            # multiple territories exist, need to determine who they belong to 
            # else neutral and don't change them 
            
            for i in range(0, len(territoryArray)):
                isBlack = False         # keeps track of if territory belongs black 
                isWhite = False         # keeps track of if territory belongs white
                colorSet = set()        # keeps track of colors in territory boarder 
                
                for point in territoryArray[i]:
                    colorSet.add(scoreBoard[point + correctionFactor])
                
                if 1 in colorSet:
                    isBlack = True 
                if 2 in colorSet:
                    isWhite = True
                
                if isBlack and not isWhite:
                    # mark all black 
                    for point in pointArray[i]:
                        scoreBoard[point+correctionFactor] = 7
                    
                elif not isBlack and isWhite:
                    # mark all white 
                    for point in pointArray[i]:
                        scoreBoard[point+correctionFactor] = 8
        
        # everything is accounted for or neutral territory 
        # parse through board and count stones
        whiteScore, blackScore = self._count_stones(scoreBoard, correctionFactor)
        
        # determine winner 
        if whiteScore > blackScore:
            self.respond("W+"+str(whiteScore-blackScore))
        elif whiteScore < blackScore:
            self.respond("B+"+str(blackScore-whiteScore))
        else:
            self.respond("0")
                
    def _count_stones(self, scoreBoard, correctionFactor):
        """ 
        Count the number of white and black stones on board + territories + komi 
        
        param :
        
        return :
        """
        whiteCount = 0
        blackCount = 0
        
        for i in range(correctionFactor,len(scoreBoard)):
            if scoreBoard[i] == 1:
                blackCount += 1
            elif scoreBoard[i] == 7:
                blackCount += 1 
                scoreBoard[i] = 0
            elif scoreBoard[i] == 2:
                whiteCount += 1
            elif scoreBoard[i] == 8:
                whiteCount += 1
                scoreBoard[i] = 0
            elif scoreBoard[i] == 9:
                scoreBoard[i] = 0
            
        whiteCount += self.komi
            
        return whiteCount, blackCount 
    
    def _explore_bfs(self, point, scoreBoard, correctionFactor):
        """ 
        Runs BFS search starting from point  
        
        param : point: index of point to start from 
        param : scoreBoard: copy of board 
        param : correctionFactor: amount to adjust index by (for walls)
        
        return : Closed: points in closed territory 
        return : Territory: points that make up boarders of territory 
        """
        Open = []
        Territory = set()
        Open.append(point)
        Closed = set()
        while Open:
            v = Open.pop(0)
            Closed.add(v)
            for child in self._neighbors(v):
                if scoreBoard[child+correctionFactor] == 0 and child not in Closed:
                    if child not in Open:
                        Open.append(child)
                elif scoreBoard[child+correctionFactor] in [1,2]:
                    Territory.add(child)
        return Closed, Territory
    
    # copied from simple_board.py in util
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
    
        
        
        
        
        
        
        
        
        