from Node import node
from LeafNode import LeafNode
from Node import node
from ethereum import utils
from BranchNodeClass import BranchNode
from LeafNode import LeafNode
#说明这个文件构建的是一个trie的扩展节点类
#用于后续功能实现的调用！
#综合使用


class ExtensionNode(node):

    def __init__(self, shared):
        self.prefix = ""
        self.sharedNibble = ""
        self.hash = ""
        # 首先设定 sharedNibble & prefix，作为初始化
        self.ChangeShared(shared)
        self.nextNode = BranchNode()

    def printNode(self, Level):
        space = "    " * Level
        print(space, "ExtensionNode : ")
        if self.prefix == 0:
            print(space, ["00" + self.sharedNibble])

        elif self.prefix == 1:
            print(space, ["1" + self.sharedNibble])
        self.nextNode.printNode(Level + 1)

    def Addnode(self, k, v):
        # 如果输入的地址和sharedNibble 一致 => 添加node 在 branchNode下
        if self.longest(self.sharedNibble, k) == self.sharedNibble:
            self.nextNode.Addnode(self.rest(self.sharedNibble, k), v)
        # 如果输入的地址和sharedNibble 不一致 => 扩展节点重置（清空）同时调用之前node值恢复
        else:
            # 重置Extension Node
            currentNode = self
            # newExtensionNode作为保留current node的功能
            # (sharedNibble会再进行更新)
            newExtensionNode = ExtensionNode(self.sharedNibble)
            newExtensionNode.nextNode = currentNode.nextNode
            #当前节点就会更新成新的sharednibble, 以及接上新的分支
            self.ChangeShared(self.longest(self.sharedNibble, k))
            self.nextNode = BranchNode()
            # newExtensionNode置换为sharednibble，即换成current node sharedNibble 剩下的部分
            # ex. old cur.share = "34679", new cur.share = "12679" => newExtensionNode.share = "679"
            newExtensionNode.ChangeShared(self.rest(self.sharedNibble, newExtensionNode.sharedNibble))
            # 但"679"并不是真正的sharednibble, 因为6会是放在branch node的index（索引）
            indexFornewExtensionNode = int(newExtensionNode.sharedNibble[0], 16)
            # sharedNibble去除index "6" => "79" 
            newExtensionNode.ChangeShared(newExtensionNode.sharedNibble[1:len(newExtensionNode.sharedNibble)])
            # branch node下面接上extension node
            self.nextNode.HexArray[indexFornewExtensionNode] = newExtensionNode
            # node都接上了再接要加入的新node
            self.nextNode.Addnode(self.rest(self.sharedNibble, k), v)

        self.HashNode()
        return self.hash

    def HashNode(self):
        if self.prefix == 0:
            self.hash = self.encode_node([bytes.fromhex("00" + self.sharedNibble), self.nextNode.HashNode()])

        elif self.prefix == 1:
            self.hash = self.encode_node([bytes.fromhex("1" + self.sharedNibble), self.nextNode.HashNode()])
        return self.hash

    def UpdateValue(self, address, value):
        if len(self.longest(self.sharedNibble, address)) >= 0:
            return self.nextNode.UpdateValue(self.rest(self.sharedNibble, address), value)

        else:
            return False

    def checkExist(self, address):
        if self.longest(self.sharedNibble, address) == self.sharedNibble:
            return self.nextNode.checkExist(self.rest(self.sharedNibble, address))
        else:
            return False

    def ChangeShared(self, shared):
        self.sharedNibble = shared
        if len(self.sharedNibble) % 2 == 0:
            # 以奇数结尾的key标记的叶子节点！
            self.prefix = 0

        else:
            # 以偶数结尾的key标记的叶子节点！
            self.prefix = 1

# test = ExtensionNode("12")
# test.Addnode("1234","56")
# test.printNode(0)
