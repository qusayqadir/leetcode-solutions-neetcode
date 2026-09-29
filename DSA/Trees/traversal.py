class TreeNode: 
    def __init__(self, val=0, left=None, right=None): 
        self.val = val 
        self.left = left 
        self.right = right


def preorder_traversal(root): 
    if root is None: 
        return 
    
    print(root.val)
    preorder_traversal(root.left)
    preorder_traversal(root.rigtht) 


def inorder_traversal(root): 

    if root is None: 
        return 
    
    inorder_traversal(root.left)
    print(root.val)
    inorder_traversal(root.right) 


def postorder_traversal(root): 

    if root is None: 
        return 
    
    postorder_traversal(root.left) 
    postorder_traversal(root.right)
    print(root.val)

#dfs 
# root, left, right
def preorder(root): 
    if not root: 
        return [] 

    stack = [root] 
    result = []

    while stack: 
        node = stack.pop() 
        result.append(node.val) 

        # NEED TO PUSH RIGHT FIRST SO LEFT CAN BE PROCESSED FIRST
        if node.right: 
            stack.append(node.rigth) 
        if node.left: 
            stack.append(node.left)

    return result 



