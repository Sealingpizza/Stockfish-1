import chess
import chess.engine
import numpy as np

def parsePGNToDataset(pgnFile):
  boardArray = [] #2d array of chess.Boards()
  stockfishArray = []
  DEPTH = 5
  
  #load pgn file
  temp = open("master_games/" + pgnFile, "r")
  f=list(temp)

  gamesLeft = True
  while(gamesLeft == True):
      board = chess.Board()

      #get list index of the game moves
      num = 3
      for i in f[3:]:
          if(i.find("1. ") != -1):
              gameIndex = num
              break;
          else:
              num+=1 

      #get array of moves in string form    
      moveString = f[num].split("}")
      moveList = []
      trackerNum = 0
    
      for move in moveString[:len(moveString)-1:]:
        if(trackerNum == 0):
            moveIndex = move.find(".") + 2
            moveList.append(move[moveIndex:move.find(" ", moveIndex)])
            trackerNum +=1
            
        else:
            moveIndex = 2
            moveList.append(move[moveIndex:move.find(" ", moveIndex)])
            trackerNum-=1
           
      #store all board positions z

      for move in moveList: 
          boardArray.append(boardToArray(board)) 
          stockfishArray.append(getStockfishScore(board, DEPTH))
          board.push_san(move)
        
      #splice together new list for loop and end loop if done
      j = gameIndex + 1
      if(gameIndex + 1 >= len(f)):
          gamesLeft = False
      else:
          for i in f[gameIndex + 1:]:
              if(i.find("[") != -1):
                  del f[0:j]
                  break
              else:
                  j+=1

  temp.close()
  return((boardArray), stockfishArray)

def getStockfishScore(board, depth):
  with chess.engine.SimpleEngine.popen_uci("stockfish/14.1/stockfish14.exe") as stockfish:
    result = stockfish.analyse(board, chess.engine.Limit(depth=depth))
    score = result['score'].white().score()
    return score
  
def boardToArray(board):
    boardString = board.epd()
    boardArray = []
    pieceCharToInt = {
        'P': 1,  
        'p': -1,  
        'N': 2,    
        'n': -2, 
        'B': 3,   
        'b': -3,  
        'R': 4,   
        'r': -4,
        'Q': 5,   
        'q': -5,  
        'K': 6,     
        'k': -6     
    }
    
    
    pieces = boardString.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        finalRow = []
        for piece in row:
            if piece.isdigit():
                for row in range(0, int(piece)):
                    finalRow.append(0)
            else:
                finalRow.append(pieceCharToInt[piece])
        boardArray = boardArray + (finalRow)
    return (boardArray)
    
