"""
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. It will also keep a move log.
"""
from operator import truediv


class GameState:
    def __init__(self):
        # Board is a 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'B', 'R', 'N', 'p'
        # "- -" - represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnmoves, 'R': self.getRookmoves, 'N': self.getKnightmoves,
                              'B': self.getBishopmoves, 'Q': self.getQueenmoves, 'K': self.getKingmoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        #update the king's location if moved
        if move.pieceMoved[1] == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved[1] == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update the king's position if needed
            if move.pieceMoved[1] == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved[1] == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        #2.) for each move, make the move
        for i in range(len(moves)-1,-1,-1): #when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3.) generate all opponent's move
            #4.) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5.) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:  #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square r, c'''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False

    def  getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function according to the piece type
        return moves
    '''get all possible moves for a pawn'''
    def getPawnmoves(self,r,c,moves):


        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c]=="--": #one step move
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--": #two step initial move
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0 and self.board[r-1][c-1][0]=="b": #capturing enemy on right side
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7 and self.board[r-1][c+1][0]=="b": #capturing enemy on the left side
                moves.append(Move((r,c),(r-1,c+1),self.board))


        else: #black pawn moves
            if self.board[r+1][c]=="--": #one step move
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--": #2 step intial move
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0 and self.board[r+1][c-1][0]=="w": #capturing enemy on right side
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7 and self.board[r+1][c+1][0]=="w": #capturing enemy on left side
                moves.append(Move((r,c),(r+1,c+1),self.board))





    '''get all possible moves for a rook'''
    def getRookmoves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor='b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if 0<=endrow<8 and 0<=endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece=="--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0]==enemyColor:
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        break
                    else:
                        break
                else:
                    break
    #

    def getKnightmoves(self,r,c,moves):
        knightmoves= ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor='w' if self.whiteToMove else 'b'
        for m in knightmoves:
            endrow=r+m[0]
            endcol=c+m[1]
            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]!=allyColor:
                    moves.append(Move((r,c),(endrow,endcol),self.board))



    def getBishopmoves(self,r,c,moves):
        directions=((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor='b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if 0<=endrow<8 and 0<=endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece=="--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0]==enemyColor:
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        break
                    else:
                        break
                else:
                    break






    def getQueenmoves(self,r,c,moves):
        self.getRookmoves(r,c,moves)
        self.getBishopmoves(r,c,moves)
    def getKingmoves(self,r,c,moves):
        kingmoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor='w' if self.whiteToMove else 'b'
        for i in range(8):
            endrow=r+kingmoves[i][0]
            endcol=c+kingmoves[i][1]

            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]!=allyColor:
                    moves.append(Move((r,c),(endrow,endcol),self.board))






class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    '''Overridig the equals method to compare moves'''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # You can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




