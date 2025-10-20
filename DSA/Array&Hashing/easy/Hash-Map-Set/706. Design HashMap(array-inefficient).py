class MyHashMap:

    def __init__(self):
        self.size = 10000001
        # use None for empty 
        self.array = [None] * self.size

    def put(self, key: int, value: int) -> None:

        self.array[key] = value 

    def get(self, key: int) -> int:

        if self.array[key] != None: 
            return self.array[key]
        return -1 
    
    def remove(self, key: int) -> None:
        self.array[key] = None
        # self.array[key].pop()
        


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)

# inefficient space usage 
# no collision handling 
# missing hash function 
