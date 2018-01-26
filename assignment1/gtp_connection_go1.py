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
        
        scoreBoard = self.board
        for i in range(len(scoreBoard)):
            if scoreBoard[i] == 0:
                points,territory, scoreBoard = _explore_bfs(i)
                for p in points:
                    pass
    
    def _explore_bfs(self,point, scoreBoard):
        Open = []
        Territory = set()
        Open.append(point)
        Closed = set()
        while Open:
            v = Open.pop(0)
            Closed.add(v)
            for child in self._neighbors(v):
                if scoreBoard[child+5] == 0 and child not in Closed:
                    if child not in Open:
                        Open.append(child)
                elif scoreBoard[child+5] in [1,2]:
                    Territory.add(child)
        return Closed, Territory, scoreBoard