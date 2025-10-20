class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """


        rows, cols = len(board), len(board[0])

        for i in range(rows): 
            rowSet = set()
            for j in range(cols): 
                if board[i][j] == '.':
                    continue 
                if board[i][j] in rowSet: 
                    return False
                
                rowSet.add(board[i][j])

        for i in range(cols): 
            colSet = set()
            for j in range(rows): 
                
                if board[j][i] == '.':
                    continue 
                if board[j][i] in colSet: 
                    return False 
                colSet.add(board[j][i])

        for square in range(9): 
            sqaureSet = set() 
            for i in range(3): 
                for j in range(3): 
                    r = (square//3) * 3 + i 
                    c = (square % 3) * 3 + j
                    if board[r][c] == '.':
                        continue 
                    if board[r][c] in sqaureSet: 
                        return False 
                    
                    sqaureSet.add(board[r][c])
        
        return True 