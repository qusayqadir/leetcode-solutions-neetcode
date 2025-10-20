class MyHashSet:

    def __init__(self):
        # self.set = [None] * 1000
        self.set = []

    def add(self, key: int) -> None:
        
        if key in self.set: 
            return 
        # else: 
        #     # if self.set is filled, make the list larger 
        #     if self.set[len(self.set)] not None: 
        #         self.set = self.set.append([None] * len(self.set)*2)
            
        self.set.append(key)

    def remove(self, key: int) -> None:
        #remove it, does the array dynamically resize itself 
        if key in self.set: 
            self.set.remove(key)
        return 
        
    def contains(self, key: int) -> bool:
        if key in self.set: 
            return True 
        return False 
        


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)