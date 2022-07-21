from Node import node
from ethereum import utils
from BranchNodeClass import BranchNode
from ExtensionNodeClass import ExtensionNode
from LeafNode import LeafNode
#这里需要import我们之前上传的节点类
import os
import rlp
from ethereum import utils
from ethereum.utils import to_string
from ethereum.abi import is_string
import copy
from ethereum.utils import decode_hex, ascii_chr, str_to_bytes
from ethereum.utils import encode_hex
from ethereum.fast_rlp import encode_optimized
#本程序是构建了一个MPT类，调用之前上传的三个节点类构建一个功能性的Merkle Patricia Trie

rlp_encode = encode_optimized


class MerklePatriciaTrie:

    def __init__(self):
        self.root = None
        self.roothash = ""

    def AddNode(self, address, value):
        # 检查root是否为空
        if self.root == None:
            self.root = LeafNode(address, value)
            return

        # 检查root是否存在
        # 如果检查结果是root存在，那么root将不能参加加减运算，而只能进行更新
        if self.checkExist(address):
            print("self node is already exist")
            return

        # 如果现在的node是 leaf node => 那么替换为extension
        if self.root.__class__ == LeafNode:
            subaddress = self.longest(self.root.keyEnd, address)
            tempExtension = ExtensionNode(subaddress)
            tempExtension.Addnode(address, value)
            tempExtension.Addnode(self.root.keyEnd, self.root.value)
            self.root = tempExtension

        # 如果现在的node是 Branch node => 我们可以直接进行加法运算
        elif self.root.__class__ == BranchNode:
            self.root.Addnode(address, value)

        # 如果现在的node是 Extension node
        elif self.root.__class__ == ExtensionNode:
            # 如果第一个地址（key）相同我们可以直接进行加法运算
            # 如果sharedNibble后续匹配的时候沒有完全一样，那么会进入extension类中的addnode函数进一步处理！
            if self.root.sharedNibble[0] == address[0]:
                self.root.Addnode(address, value)

            else:
                # 如果第一个地址（key）就不相同那么root需要换成Branch node，说明他并不是根节点
                # 于是对于root更换操作不放在extension节点类中进行处理，而是放在MPT类中进行处理
                tempBranch = BranchNode()
                index = int(self.root.sharedNibble[0])
                self.root.ChangeShared(self.root.sharedNibble[1:len(self.root.sharedNibble)])
                # self.root.sharedNibble = self.root.sharedNibble[1:len(self.root.sharedNibble)]
                tempBranch.HexArray[index] = self.root
                tempBranch.Addnode(address, value)
                self.root = tempBranch

        # self.root.printNode(0)

    def checkExist(self, address):
        return self.root.checkExist(address)

    def UpdateValue(self, address, value):
        if not self.checkExist(address):
            print("self node is not exist")
            return

        Result = self.root.UpdateValue(address, value)
        self.root.HashNode()
        return Result

    def print(self):
        temp = self.root
        temp.printNode(0)
        if type(self.root.hash) == bytes:
            self.roothash = self.root.hash.hex()
        else:
            self.roothash = self.encode_node(self.root.HashNode())
            self.roothash = self.roothash.hex()

        print(self.roothash)

    def encode_node(self, node):
        # if node == BLANK_NODE:
        #     return BLANK_NODE
        rlpnode = rlp_encode(node)

        hashkey = utils.sha3(rlpnode)
        return hashkey

    def longest(self, a, b):
        sub = ""
        for i in range(len(a)):
            if a[i] == b[i]:
                sub += a[i]
            else:
                break
        return sub

    def rest(self, sub, origin):
        temp = ""
        for i in range(len(sub)):
            temp += origin[i]
        return temp

