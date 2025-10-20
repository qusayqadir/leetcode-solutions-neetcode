class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """ 

        duplicate = set()
        for num in nums: 
            if num in duplicate: 
                return True 
            else: 
                duplicate.add(num) 
        return False
        
        # ## if len(set(nums)) != len(nums):
        #         return True 
        #     return False

