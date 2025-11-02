class Solution(object):
    def dailyTemperatures(self, temp):
        """
        :type temperatures: List[int]
        :rtype: List[int]
        """

        res = [0] * len(temp)
        stack = [] 

        for index, value in enumerate(temp): 
            while stack and stack[-1][-1] < value: 
                tempIndex, tempValue = stack.pop() 
                res[tempIndex] = index - tempIndex
            stack.append((index,value))
        
        return res 