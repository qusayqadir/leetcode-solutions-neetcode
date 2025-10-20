class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        output = []
        left, right = 0, len(matrix[0])
        top, bottom = 0, len(matrix) 

        while left < right and top < bottom: 
            # left to right 
            for i in range(left, right): 
                output.append(matrix[top][i])
            top += 1 

            # top to bottom 
            for i in range(top, bottom):
                output.append(matrix[i][right - 1])
            right -= 1 
            if not (left < right and top < bottom): 
                break
            # right to left
            for i in range(right - 1, left - 1, -1):
                output.append(matrix[bottom - 1][i])
            bottom -= 1 

            # down to top
            for i in range(bottom - 1, top - 1, -1): 
                output.append(matrix[i][left]) 
            left += 1
            
        return output


