# dfs pattern 
def dfs(node): 
    if node is None: 
        return 
    # process current node

    dfs(node.left) 
    dfs(node.right) 

#graphs need to track visted nodes to avoid infinite loops 

def dfs(node, visited):
    if node in visited:
        return
    
    visited.add(node)
    
    for neighbor in node.neighbors:
        dfs(neighbor, visited)


# sum of nodes 
def dfs(node): 
    if node is None: 
        return 0 
    
    #base case: left node 
    if node.left is None and node.right is None: 
        return node.val 
    
    #left subtree
    left = dfs(node.left) 
    #right subtree
    right = dfs(node.right) 

    return left + right + node.val  

    # each recursive call returned the sum of the subtree rooted at the current node. ]


# find the maximum value in the tree 
# if i am at a node in the tree, what values do i need from my left and right subtress to find the max val for my subtree? 

# max val from left subtree, and max val in my right subtree. 
# max val in my subtree is the max of those two values and thw value of my node 

def maxValue(node):
    if node is None: 
        return float('inf')

    if node.left is None and node.right is None: 
        return node.val 

    left = maxValue(node.left)
    right = maxValue(node.right)
    return max(left, right, node.val)
