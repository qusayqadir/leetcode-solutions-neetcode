class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        """
        :type flowerbed: List[int]
        :type n: int
        :rtype: bool
        """
        # need to fig out the difference between len(flowerbed) - 1 and len(flowerbed)
        # use len(array_name) when looping 
        for i in range(len(flowerbed)) and n != 0:

            if flowerbed[i] == 0: 
                # array len is 1 
                if i == 0 and len(flowerbed) == 1: 
                    flowerbed[i] = 1
                    n -= 1
                # if first index or last index is 0 
                # use len(array_name) when you need to forcibly check the last index of the array 
                if len(flowerbed) > 1 and ((i == 0 and flowerbed[i+1] == 0) or (i == len(flowerbed)-1 and flowerbed[i-1] == 0)): 
                    flowerbed[i] = 1 
                    n -=1 
                # general case, mid array 
                if (i > 0 and flowerbed[i-1] == 0) and ( i < len(flowerbed) - 1 and flowerbed[i+1] == 0): 
                    flowerbed[i] = 1 
                    n-=1 

        return n == 0
                

                
class Solution2(object):
    def canPlaceFlowers(self, flowerbed, n):
        """
        :type flowerbed: List[int]
        :type n: int
        :rtype: bool
        """
        f = [0] + flowerbed + [0] 
        # skip the new [0] and [0] at the end which is @ len(f) - 1 
        for i in range(1, len(f) - 1): 
            if f[i-1] == 0 and f[i] == 0 and f[i+1] == 0: 
                f[i] = 1 
                n -= 1 

        return n == 0 

