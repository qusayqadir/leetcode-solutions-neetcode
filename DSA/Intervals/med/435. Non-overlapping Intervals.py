class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Your code goes here
        intervals.sort(key=lambda x: x[1])
        count = 1
        if len(intervals) == 0:
            return 0 

        end=intervals[0][1]     

        for interval in intervals[1:]: 
            if interval[0] >= end: 
                count+=1 
                end = interval[1]

        return len(intervals) - count 
