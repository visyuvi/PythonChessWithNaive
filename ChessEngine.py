# File for determining valid moves etc. It stores info about the current state of a chess game.


class GameState:

    # "--" represents an empty space with no piece
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a move as a parameter  and executes it (this will not work for castling, pawn promotion and en-passant 
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # to undo later or to  keep history of the moves
        self.whiteToMove = not self.whiteToMove  # swap players

    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # Make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # not considering checks as of now

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = [ Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)

                    if piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves

    '''
    Get all the pawn moves for the pawn located at r,c  and add these to the list 
    '''

    def getPawnMoves(self, r, c, moves):
        pass

    '''
    Get all the pawn moves for the rook located at r,c  and add these to the list 
    '''

    def getRookMoves(self, r, c, moves):
        pass


class Move:
    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in rankToRows.items()}
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
        print(self.moveID)

    '''Overriding the equals method'''

    def __eq__(self, other):
        print(other.moveID)
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # can be modified to look  like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]