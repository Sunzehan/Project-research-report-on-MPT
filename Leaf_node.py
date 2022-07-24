from Node import node
from ethereum import utils
#说明这个文件构建的是一个trie的叶子节点类
#用于后续功能实现的调用！

class LeafNode(node):

    def __init__(self, k, v):
        self.hash = ""
        self.keyEnd = ""
        self.value = ""
        self.Addnode(k, v)

    def printNode(self, Level):
        space = "    " * Level
        print(space, "LeafNode : ")
        if self.prefix == 2:
            print(space, ["20" + self.keyEnd, self.value])
            
        elif self.prefix == 3:
            print(space, ["3" + self.keyEnd, self.value])
            
    def Addnode(self, k, v):
        if len(k) % 2 == 0:
            # 以奇数结尾的key标记的叶子节点！
            self.prefix = 2
        else:
            # 以偶数结尾的key标记的叶子节点！
            self.prefix = 3
        self.keyEnd = k
        self.value = v
        self.HashNode()
        return self.hash

    def HashNode(self):
        if self.prefix == 2:
            self.hash = self.encode_node([bytes.fromhex("20" + self.keyEnd), bytes(self.value, 'utf-8')])  # 偶數

        elif self.prefix == 3:
            self.hash = self.encode_node([bytes.fromhex("3" + self.keyEnd), bytes(self.value, 'utf-8')])  # 奇數
        return self.hash

    def UpdateValue(self, address, value):
        if address == self.keyEnd:
            self.value = value
            self.HashNode()
            return True
        else:
            return False

    def checkExist(self, address):
        if self.keyEnd == address:
            return True
        else:
            return False

    def UpdateKeyEnd(self, k):
        self.keyEnd = k
        self.HashNode()

    def gethash(self):
        return self.hash
