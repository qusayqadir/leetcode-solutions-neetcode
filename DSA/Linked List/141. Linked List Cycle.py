# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def hasCycle(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        # how to check self loop? and this will time-out
        # # zero elements in the list 
        if not head: 
            return False 
        slow, fast = head, head 
        #make fast move twice as fast, if its ever None, that means there is no cycle 
        while fast and fast.next:
            # this does not work, how to check if its the same node??

            # if slow.val == fast.val and slow.next == fast.next: 
            #     return True 

            # this just default checks if its the same node, irrespective of next nodes and and current node value 
            slow = slow.next 
            fast = fast.next.next
            
            if slow == fast: 
                return True  
        
        return False 
            