# Project-research-report-on-MPT
**Merkle Patricia Trie方案研究报告**

了一下午写完了ECMH的测试程序，晚上了解一下对于改进默克树的原理。
正好我们也有merkel tree相关的project，之后我们将进行相关的实现过程，
复习一下课程中讲述的相关理论

**Merkle Tree原理**

Merkle Tree是一种数据结构，用来验证计算机之间存储和传输数据的一致性，

首先如果使用朴素的方法进行一致性的验证需要消耗大量的存储和网络资源，如比对计算机之间的所有数据；

使用Merkle Tree，只需要比对merkle root（根节点）就可以达到相同的效果。整个过程，简单的描述如下：

   **将数据通过哈希之后放置在叶子节点之中；**
   
   **将相邻两个数据的哈希值组合在一起，得出一个新的哈希值；**
   
   **依次类推，直到只有一个节点也就是根节点；**
   
   **在验证另外的计算机拥有和本机相同的数据时，只需验证其提供的根节点和自己的根节点一致即可。**
   
换句话说这棵树的hash值作为节点，是自下而上构建的。

Merke Tree使用了加密哈希算法来快速验证数据一致性，常用的加密哈希算法有SHA-256，SHA-3，Blake2等，

该加密算法可以保持对任意的输入数据可以进行高效计算，对于相同的输入有相同的输出的同时兼具了单向性（从哈希值无法推断出原信息）抗碰撞性。

对于整棵树的输入即使只有很小的改变，输出的树节点也会有极大不同。

Merkel tree示例如图所示：

![图片](https://user-images.githubusercontent.com/107350922/179985741-3634cc97-d627-46bb-9c58-0bf09e4467a6.png)【1】

而在区块链应用Bitcoin网络中，存储的数据为转移Bitcoin的交易信息（订单往来），如“sunzehan发送给apple 10个比特币”，通过使用Merkle Tree，除了上面提到的验证各个节点之间的数据一致性，还可以用来快速验证一个交易是否属于某个区块（轻节点只需要下载很少的数据就可以验证交易的有效性）。

例如上图所示，如果某用户要验证交易生成的订单hash值=3b95是否在某个区块之中，需要依赖的数据仅仅是0d16,5c71, 和 merkle root=6c0a。

**Merkle Patricia Trie原理**

Patria Trie也是一种树形的数据结构，常用的使用场景包括：搜索引擎的自动补全功能；IP路由等。Trie的特点是，某节点的key是从根节点到该节点的路径，即不同的key有相同前缀时，它们共享前缀所对应的路径。

所以这种数据结构的应用场景多为用于快速查找前缀相同的数据，内存开销较少。如以下数据及对应的trie表示为：

![图片](https://user-images.githubusercontent.com/107350922/179990030-7169c99e-7e5a-45ba-9ef2-08e9ec517479.png)【2】

Merkle Patricia Trie（下面简称MPT），在Trie的基础上，给每个节点计算了一个哈希值，在Substrate（一种规格的树结构，每个节点最多有16个子节点：）中，该值通过对节点内容进行加密hash算法如Blake2运算取得，用来索引数据库和计算merkle root。也就是说，MPT用到了两种key的类型。

一种是Trie路径所对应的key，由runtime模块的存储单元决定。使用Substrate开发的应用链，它所拥有的各个模块的存储单元会通过交易进行修改，成为链上状态（简称为state）。每个存储单元的状态都是通过键值对以trie节点的形式进行索引或者保存的，这里键值对的value是原始数据（如数值、布尔）的SCALE编码结果，并作为MPT节点内容的一部分进行保存；key是模块、存储单元等的哈希组合，且和存储数据类型紧密相关，如：

  单值类型（即Storage Value），它的key是Twox128(module_prefix) ++ Twox128(storage_prefix)；
  
  简单映射类型（即map），可以表示一系列的键值数据，它的存储位置和map中的键相关，即Twox128(module_prefix) + Twox128(storage_prefix) + hasher(encode(map_key))；
  
  链接映射类型（即linked_map），和map类似，key是Twox128(module_prefix) + Twox128(storage_prefix) + hasher(encode(map_key))；它的head存储在Twox128(module) + Twox128("HeadOf" + storage_prefix)；
  
  双键映射类型（即double_map），key是twox128(module_prefix) + twox128(storage_prefix) + hasher1(encode(map_key1)) + hasher2(encode(map_key2))。【3】

计算key所用到 Twox128 是一种非加密的哈希算法，计算速度非常快，但去除了一些严格的要求，如抗碰撞、混淆性等，从而无法保证安全性，适用于输入固定且数量有限的场景中。module_prefix通常是模块的实例名称；storage_prefix通常是存储单元的名称；原始的key通过SCALE编码器进行编码，再进行哈希运算，这里的哈希算法是可配置的--根据输入来源是否可信作为判断依据，调整hash函数的使用，如用户输入可以认为是不不可信的，则使用Blake2（也是默认的哈希算法），否则可以使用Twox。

另一种是数据库存储和计算merkle root使用的key，可以通过对节点内容进行哈希运算得到，在键值数据库（即RocksDB，和LevelDB相比，RocksDB有更多的性能优化和特性）中索引相应的trie节点。【4】

Trie节点主要有三类，即叶子节点（Leaf）、有值分支节点（BranchWithValue）和无值分支节点（BranchNoValue）；有一个特例，当trie本身为空的时候存在唯一的空节点（Empty）。根据类型不同，trie节点存储内容有稍许不同，通常会包含header、trie路径的部分key、children节点以及value。下面举一个具体例子。

![图片](https://user-images.githubusercontent.com/107350922/180148217-3fe69513-a078-4bc9-974b-93331bafc389.png)

如果对于上表的数据

**参考资料：**

【1】https://baike.baidu.com/item/%E6%A2%85%E5%85%8B%E5%B0%94%E6%A0%91/22456281?fr=aladdin

【2】https://blog.csdn.net/shangsongwww/article/details/119272573

【3】https://zhuanlan.zhihu.com/p/32924994

【4】https://www.jianshu.com/p/5e2483413537?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

