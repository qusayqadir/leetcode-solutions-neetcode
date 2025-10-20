class Solution(object):
    def calPoints(self, operations):
        """
        :type operations: List[str]
        :rtype: int
        """
        scores = []
        for operation in operations: 
            if operation.isnumeric() or operation[0] == '-': 
                print(operation)
                scores.append(int(operation)) 
            elif operation == '+': 
                num1 = scores.pop()
                num2 = scores.pop()
                scores += [num2, num1, num1 + num2] 
            elif operation == 'D': 
                num = scores.pop() 
                scores += [num, num * 2] 
            elif operation == 'C': 
                scores.pop() 
            print(scores)
        sum = 0
        for score in scores: 
            sum += score
        return sum 

# !!!!----------HOW IT SHUOLD HAVE BEEN DONE WITH STACKS? (less code and simplier) ---------!!!!
class Solution(object):
    def calPoints(self, operations):
        """
        :type operations: List[str]
        :rtype: int
        """
        scores = [] 
        for op in operations: 
            if op == '+': 
                scores += [scores[-1] + scores[-2]] 
            elif op == 'D': 
                scores += [scores[-1] * 2 ]
            elif op =='C':
                scores.pop() 
            else: 
                scores.append(int(op))
        return sum(scores)