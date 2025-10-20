from typing import Optional 
class ListNode: 
    def __init__(self, key : int, next : Optional['ListNode'] = None):
        self.key = key 
        self.next = next

class MyHashSet:

    def __init__(self):
        self.hash_set = [ListNode(-1) for _ in range(10000)] 

    def __hash(self, key:int) -> int: 
        return key % len(self.hash_set) 

    def add(self, key: int) -> None:
        
        index = self.__hash(key) 
        curr = self.hash_set[index]
        while curr.next: 
            if curr.next.key == key: 
                return 
            curr = curr.next
        curr.next = ListNode(key)

    def remove(self, key: int) -> None:
        index = self.__hash(key) 
        curr = self.hash_set[index]
        while curr.next: 
            if curr.next.key == key: 
                curr.next = curr.next.next 
                return 
            curr = curr.next       

    def contains(self, key: int) -> bool:
        index = self.__hash(key) 
        curr = self.hash_set[index]
        while curr.next: 
            if curr.next.key == key: 
                return True
            curr = curr.next 
        return False 


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)