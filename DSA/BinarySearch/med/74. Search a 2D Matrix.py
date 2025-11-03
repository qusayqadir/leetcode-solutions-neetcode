class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        m, n = len(matrix), len(matrix[0]) - 1 
        rowL, rowR = 0, len(matrix) - 1 


        while rowL <= rowR: 
            
            midRow= (rowL+rowR) // 2

            colL, colR = 0, n

            # chosen the correct matrix Row 
            if matrix[midRow][0] <= target <= matrix[midRow][n]: 

                while colL <= colR: 

                    midCol = (colL + colR) // 2 

                    if target == matrix[midRow][midCol]: 
                        return True 

                    elif target > matrix[midRow][midCol]: 
                        colL = midCol + 1 

                    elif target < matrix[midRow][midCol]: 
                        colR = midCol - 1

                return False 
        
            elif target < matrix[midRow][0]:
                rowR = midRow - 1 
            elif target > matrix[midRow][n]: 
                rowL = midRow + 1 
            
        return False 

