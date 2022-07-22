import abc
import os
import rlp
from ethereum import utils
from ethereum.utils import to_string
from ethereum.abi import is_string
import copy
from ethereum.utils import decode_hex, ascii_chr, str_to_bytes
from ethereum.utils import encode_hex
from ethereum.fast_rlp import encode_optimized

rlp_encode = encode_optimized

#节点类，将之前写的节点之间的操作在集成一下
class node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def printNode():
        return NotImplemented

    @abc.abstractmethod
    def Addnode():
        return NotImplemented

    @abc.abstractmethod
    def UpdateValue():
        return NotImplemented

    @abc.abstractmethod
    def checkExist():
        return NotImplemented

    def encode_node(self, node):
        rlpnode = rlp_encode(node)
        if len(rlpnode) < 32:
            return node
        hashkey = utils.sha3(rlpnode)
        return hashkey
    
#判定是否超过节点数据的最大长度
    def longest(self, a, b):
        sub = ""
        for i in range(len(a)):
            if a[i] == b[i]:
                sub += a[i]
            else:
                break
        return sub
#node中将the rest of key级联到data部分的最后
    def rest(self, sub, origin):
        temp = ""
        for i in range(len(sub), len(origin)):
            temp += origin[i]
        return 