class Solution(object):
    def checkValid(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: bool
        """       
        row, col = len(matrix), len(matrix[0])

        for i in range(row): 
            colSet = set()
            for j in range(col):  
                if matrix[i][j] not in colSet and 1 <= matrix[i][j] <= len(matrix): 
                    colSet.add(matrix[i][j])
                else: 
                    return False 


        for j in range(col): 
            rowSet = set()
            for i in range(row): 
                if matrix[i][j] not in rowSet and 1 <= matrix[i][j] <= len(matrix): 
                    rowSet.add(matrix[i][j])
                else: 
                    return False 
        return True 
        


