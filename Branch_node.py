from Node import node
from LeafNode import LeafNode
from ethereum import utils
#说明这个文件构建的是一个trie的分支节点类
#用于后续功能实现的调用！

class BranchNode(node):

    def __init__(self):
        self.HexArray = [""] * 16
        self.value = ""
        self.hash = ""

    def printNode(self, Level):
        space = "    " * Level
        print(space, "BranchNode : ")

        for index in range(16):
            if self.HexArray[index] != "":
                print(space, index)
                self.HexArray[index].printNode(Level + 1)
        print(space, self.value)

    def Addnode(self, k, v):
        # 若 k = ""，表示是到 extension node address就沒了
        # 该extension node value可以记录在 branch node 下
        if k == "":
            self.value = v
            return
        index = int(k[0], 16)
        # 延迟import 防止circular import死循环或者溢出
        from ExtensionNodeClass import ExtensionNode
        if self.HexArray[index] != "":
            # 如果目前处于leaf的状态
            if self.HexArray[index].__class__ == LeafNode:
                # 先把目前leaf存下來
                Leaf = self.HexArray[index]
                # 找出目前leaf和新增node之间最长的substring
                subaddress = self.longest(Leaf.keyEnd, k[1:len(k)])
                # 创建扩展节点
                tempExtension = ExtensionNode(subaddress[0:len(subaddress)])
                # 扩展节点下的Branch Node加入新增node
                tempExtension.Addnode(k[1:len(k)], v)
                # 扩展节点下的Branch Node加入已存在的leaf
                # 注意此处不用做substring
                tempExtension.Addnode(Leaf.keyEnd[0:len(Leaf.keyEnd)], Leaf.value)
                # HexArray临时数组其中存储的节点从leaf节点变成了我们刚创建的扩展节点
                self.HexArray[index] = tempExtension
            # 若目前是扩展节点
            elif self.HexArray[index].__class__ == ExtensionNode:
                self.HexArray[index].Addnode(k[1:len(k)], v)


        else:
            self.HexArray[index] = LeafNode(k[1:len(k)], v)

        # 这里不确定要不要hash，决定最终再一起哈希吧
        self.HashNode()
        return self.hash

    def HashNode(self):
        arr = [b""] * 17
        for index in range(16):
            if self.HexArray[index] != "":
                arr[index] = self.HexArray[index].HashNode()

        if self.value != "":
            arr[16] = bytes(self.value, 'utf-8')

        self.hash = self.encode_node(arr)
        return self.hash

    def UpdateValue(self, address, value):
        index = int(address[0], 16)
        if self.HexArray[index] != "":
            return self.HexArray[index].UpdateValue(address[1:len(address)], value)
        else:
            return False

    def checkExist(self, address):
        index = int(address[0], 16)
        if self.HexArray[index] != "":
            return self.HexArray[index].checkExist(address[1:len(address)])
        else:
            return False
        
#保留用于调试的代码
# test = BranchNode()
# test.Addnode("29293",“12313")
# test.Addnode("243243","9997")
# test.printNode(0)
# print(test.HashNode())