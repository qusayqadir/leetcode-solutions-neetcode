class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:

        res = []
        n = len(intervals)
        i = 0

        #O(n)
        
        #ends before it starts 
        while i < n and intervals[i][1] <  newInterval[0]: 
            res.append(intervals[i])
            i+=1

        #
        while i < n and intervals[i][0] <= newInterval[1]: 
            minstart = min(intervals[i][0], newInterval[0])
            maxend = max(intervals[i][1], newInterval[1])
            newInterval = [minstart, maxend]
            i += 1
        
        res.append(newInterval)
        # res.append(intervals[1:])

        while i < n: 
            res.append(intervals[i])
            i+=1 

        return res 

        



            

            

    #if inteval starts before newInteval and ends before 
    #if inteval starts before new interval and ends after 
    #if interval starts after and end before inteval 
    #if interval starts after and ends after interval 

    #if interval starts after newInteval end 

        print(res)