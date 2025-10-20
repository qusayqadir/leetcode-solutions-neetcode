from collections import deque
class Solution(object):
    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        rows, cols = len(grid),  len(grid[0])
        visited = set()
        numIsland = 0 

        def check(grid, r, c): 

            if r >= 0 and r < rows and c >= 0 and c < cols: 
                if (r,c) not in visited: 
                    if grid[r][c] != '0': 
                        return True 
            return False 


        def bfs(grid, i, j): 
            queue = deque() 
            queue.append([i,j])
            visited.add((i,j))
            
            while queue: 
                r, c = queue.popleft() 

                if check(grid, r + 1 , c): 
                    queue.append([r+1, c])
                    visited.add((r+1, c))

                if check(grid, r -1, c): 
                    queue.append([r-1, c])
                    visited.add((r-1, c))
                
                if check(grid, r, c + 1 ): 
                    queue.append([r, c + 1])
                    visited.add((r, c+1))
                
                if check (grid, r, c - 1): 
                    queue.append([r,c-1])
                    visited.add((r, c-1))


        for r in range(rows): 
            for c in range(cols): 
                if grid[r][c] == '1' and (r,c) not in visited: 
                    bfs(grid, r, c) 
                    numIsland += 1 

        return numIsland
