# Project-research-report-on-MPT
Merkle Patricia Trie方案研究报告
了一下午写完了ECMH的测试程序，晚上了解一下对于改进默克树的原理。
正好我们也有merkel tree相关的project，之后我们将进行相关的实现过程，
复习一下课程中讲述的相关理论

Merkle Tree是一种数据结构，用来验证计算机之间存储和传输数据的一致性，

首先如果使用朴素的方法进行一致性的验证需要消耗大量的存储和网络资源，如比对计算机之间的所有数据；

使用Merkle Tree，只需要比对merkle root（根节点）就可以达到相同的效果。整个过程，简单的描述如下：

   **将数据通过哈希之后放置在叶子节点之中；**
   
   **将相邻两个数据的哈希值组合在一起，得出一个新的哈希值；**
   
   **依次类推，直到只有一个节点也就是根节点；**
   
   **在验证另外的计算机拥有和本机相同的数据时，只需验证其提供的根节点和自己的根节点一致即可。**
