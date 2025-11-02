class MinStack(object):
    import math
    def __init__(self):
        self.stack = []
        self.curMin = None

    def push(self, val):
        """
        :type val: int
        :rtype: None
        """
        if len(self.stack) == 0: 
            self.curMin = val 
        else: 
            self.curMin = min(self.curMin, val) 

        self.stack.append(val)
        
    #O(n) only if whats been popped is the curMin,
    # then u need to refind it 
    def pop(self):
        """
        :rtype: None
        """
        temp = self.stack.pop()
        if temp == self.curMin: 
            if len(self.stack) > 0: 
                self.curMin = self.stack[0]
                for i in range(len(self.stack)): 
                    self.curMin = min(self.curMin, self.stack[i])
            else: 
                self.curMin = None
        

        

    def top(self):
        """
        :rtype: int
        """
        top = self.stack.pop() 
        self.stack.append(top) 
        return top 

        # return self.stacl[-1]
        # return self.stack[len(self.stack)-1]
        

    def getMin(self):
        """
        :rtype: int
        """
        return self.curMin 
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()


#====================================================
class MinStack(object):

    def __init__(self):
        self.curStack = [] 
        self.minStack = []
        self.curMin = None

    #O(1) 
    def push(self, val):
        """
        :type val: int
        :rtype: None
        """
        self.curStack.append(val)
        if self.curMin == None: 
            self.curMin = val 
        else: 
            self.curMin = min(self.curMin, val) 
        
        self.minStack.append(self.curMin) 

        
    #O(1)
    def pop(self):
        """
        :rtype: None
        """
        self.curStack.pop() 
        self.minStack.pop() 
        if len(self.minStack) > 0:
            self.curMin = self.minStack[-1]
        else: 
            self.curMin = None 
        
    #O(1)
    def top(self):
        """
        :rtype: int
        """
        return self.curStack[-1] 

    def getMin(self):
        """
        :rtype: int
        """
        return self.curMin


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()

#=============================Another Solution O(2n), without keeping track of curMin variable================================================================================================
class MinStack(object):

    def __init__(self):
        self.curStack = [] 
        self.minStack = []

    def push(self, val):
        """
        :type val: int
        :rtype: None
        """
        self.curStack.append(val)       
        if len(self.minStack) > 0: 
            self.minStack.append(min(val, self.minStack[-1])) 
        else: 
            self.minStack.append(val)

        

    def pop(self):
        """
        :rtype: None
        """
        self.curStack.pop() 
        self.minStack.pop() 

    def top(self):
        """
        :rtype: int
        """
        return self.curStack[-1] 

    def getMin(self):
        """
        :rtype: int
        """
        return self.minStack[-1]
