class MyHashMap:

    def __init__(self):
        self.size = 1000 
        self.bucket = [[] for _ in range(self.size)]
        
        # #0                  #1              #2 
        # [ [ [],[],[],[] ], [ [],[],[],[] ], [ [],[],[],[] ] ]

    #helper function
    def hash(self, key: int) -> int: 
        return key % self.size

    def put(self, key: int, value: int) -> None:
        
        hashkey = self.hash(key)
        bucket =  self.bucket[hashkey] 

        for i, (k,v) in enumerate(bucket): 
            if k == key: 
                bucket[i] = (key, value) 
                return 
       
        #key does not exist, and it to the end of the bucket
        bucket.append((key,value))  

        #enumerate gives index, and element @ the same index 

    def get(self, key: int) -> int:
        
        hashkey = self.hash(key)
        bucket =  self.bucket[hashkey] 
        for i, (k,v) in enumerate(bucket): 
            if k == key: 
                return v
        return -1 

    def remove(self, key: int) -> None:
        hashkey = self.hash(key)
        bucket =  self.bucket[hashkey] 
        for i, (k,v) in enumerate(bucket): 
            if k == key: 
                bucket.pop(i)
                return 


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)