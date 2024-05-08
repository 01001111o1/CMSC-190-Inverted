from heapq import heappush, heappop
import numpy as np

# Knight's x and y movement
moves = [[1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]

def is_safe(x, y, board):
    return 1 if (0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == 0) else 0

def get_degree(x, y, board):
    c = 0
    for i in range(8):
        c += is_safe(*np.add([x, y], moves[i]), board)
    return c

def generateKTM(x, y, board):
    
    p = 1
    board[x][y] = p
    
    for _ in range(len(board) * len(board[0])):
        pq = []

        for i in range(8):

            nx, ny = np.add([x, y], moves[i])
            
            if is_safe(nx, ny, board):
                degree = get_degree(nx, ny, board)
                heappush(pq, (degree, i))
        
        if len(pq) > 0:
            ( _ , i ) = heappop(pq)
            x, y = np.add([x, y], moves[i])
            p += 1
            board[x][y] = p

    return board

# for r in range(3, 20):
#     for c in range(3, 20):
#         counter = 0
#         for i in range(r):
#             for j in range(c):
#                 board = np.zeros((r, c))
#                 counter += generateKTM(i, j, board)
#         if counter == r * c:
#             print(r, c)   

# r, c = 9, 8
# for i in range(r):
#     for j in range(c):
#         board = np.zeros((r, c))
#         print(i, j, generateKTM(i, j, board))

#board = np.zeros((9, 8))
#print(generateKTM(5, 7, board))