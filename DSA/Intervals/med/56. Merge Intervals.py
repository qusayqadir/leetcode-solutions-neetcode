class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        
        #O(n)
        #sort based off start time 
        intervals.sort(key=lambda x : x[0])
        res=[intervals[0]]

        for interval in intervals[1:]: 

            if res: 
                if res[-1][1] >= interval[0]: 
                    end = max(res[-1][1], interval[1])
                    temp = res.pop()
                    res.append([temp[0], end])
                else: 
                    res.append(interval)
        
        return res
