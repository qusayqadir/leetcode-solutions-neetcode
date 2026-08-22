# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:

        curr1, curr2 = l1, l2 
        sum1 = sum2 = 0 
        pwr = 0 
        while curr1: 
            sum1 += curr1.val * 10**pwr
            pwr += 1 
            curr1 = curr1.next 
        pwr=0 

        while curr2: 
            sum2 += curr2.val * 10**pwr
            pwr +=1 
            curr2 = curr2.next 
        
        target =  sum2 + sum1

        head = ListNode(0)
        curr = head 

        if target == 0: 
            return head

        while target: 
            if target == 0: 
                curr.next = ListNode(0)
                break 
            curr.next = ListNode(target % 10)
            curr = curr.next 
            target = target // 10 



        # what if linked list length = 1 none.next? 
        return head.next 



        