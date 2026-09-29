from Collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, q, p) -> bool: 
        if p is None and q is None: 
            return True 

        if (q is None and p) or (q and p is None): 
            return False 
        
        if q.val != p.val: 
            return False 
        
        return self.isSameTree(q.left, p.left) and self.isSameTree(q.right, p.right)
        
    def isSubtree(self, root: TreeNode | None, subRoot: TreeNode | None) -> bool:
        
        queue = deque([root])
        while queue: 
            node = queue.popleft() 
            if node.val == subRoot.val : 
                if self.isSameTree(node, subRoot): 
                    return True 
    
            if node.left: 
                queue.append(node.left) 
            if node.right: 
                queue.append(node.right) 

        return False

    def isSubtreeRecursive(self, root: TreeNode | None, subRoot: TreeNode | None) -> bool:
        
        if root is None: 
            return False 

        if root.val == subRoot.val : 
            if self.isSameTree(root, subRoot): 
                return True 
        
        return self.isSubtreeRecursive(root.left, subRoot) or self.isSubtreeRecursive(root.right, subRoot)

