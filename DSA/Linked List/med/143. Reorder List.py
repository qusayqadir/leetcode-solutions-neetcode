# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # find mid
        fast = slow = head
        # (fast.next so we know there is a place for slow to go to tahts not none)
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

        # reverse mid till end
        ptr = slow
        prev = None
        while ptr:
            temp = ptr.next
            ptr.next = prev
            prev = ptr
            ptr = temp

        curr = head
        l1 = curr
        l2 = prev
        switch = 0

        while curr.next:
            if switch == 0:
                l1 = curr.next
                curr.next = l2
                curr = curr.next
                l2 = l2.next
                switch += 1
            else:
                curr.next = l1
                curr = curr.next
                l1 = l1.next
                switch -= 1


        # take the head, and go through both pointers and construct new list