from collections import deque 
# FIFO 
class Solution(object):
    def orangesRotting(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        row, col = len(grid), len(grid[0])
        freshOranges = 0 
        queue = deque() 
        time = 0

        for i in range(row): 
            for j in range(col): 
                if grid[i][j] == 1:
                    freshOranges += 1 
                elif grid[i][j] == 2:
                    queue.append([i,j])
                    #right, left adj, up , down adj

        if freshOranges == 0: 
            return 0        
        direction = [[1,0],[-1,0], [0,1],[0,-1]]
        
        while queue and freshOranges > 0:
            for _ in range(len(queue)):
                i, j = queue.popleft()
                for drow, dcol in direction: 
                    tempRow  = i + drow 
                    tempCol = j + dcol
                    if 0 <= tempRow <= row - 1 and 0 <= tempCol <= col - 1 and  grid[tempRow][tempCol] == 1 :
                        grid[tempRow][tempCol] = 2
                        queue.append( [tempRow, tempCol])
                        freshOranges -= 1 
            
            time += 1 

        return time if freshOranges == 0 else -1 

