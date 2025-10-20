# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        #edge case, either list is empty 
        if not list1: 
            return list2 
        if not list2: 
            return list1 
        
        if list1.val <= list2.val: 
            head = list1
            ptr1 = list1.next 
            ptr2 = list2 
        else: 
            head = list2 
            ptr1 = list1
            ptr2 = list2.next 
        
        curr = head 
        while ptr1 and ptr2: 
            if ptr1.val <= ptr2.val: 
                curr.next = ptr1 
                ptr1 = ptr1.next 
            else: 
                curr.next = ptr2 
                ptr2 = ptr2.next 
            
            curr = curr.next 
        
        if not ptr1: 
            curr.next = ptr2 
        if not ptr2: 
            curr.next = ptr1 
        
        return head 
