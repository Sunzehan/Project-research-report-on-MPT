testcase = {'7c3002ad756d76a643cb09cd45409608abb642d9': '10',
            '7c303333756d555643cb09cd45409608abb642d9': '20',
            '7c303333756d777643cb09c999409608abb642d9': '30',
            '7c303333756d777643cb09caaa409608abb642d9': '40',
            '111102ad756d76a643cb09cd45409608abb642d9': '50'}
#测试数据模拟md文件中的第三张图片生成的数据
#注意需要import之前写的MPT class
#test1---新节点的生成（原先是空节点）
#测试的运行结果会放在md文件最后进行展示

from MPT import MerklePatriciaTrie

Tests = []
Tests.append(testcase)
for Test in Tests:
    Tree = MerklePatriciaTrie()
    for item in Test:
        Tree.AddNode(item, Test[item])
    Tree.print()

#test2更新节点，原先节点非空，为了代码的完整性这里加入insert操作
#由于在test1中已经将空节点设置add为testcase，所这里并不需要insert操作！
# Insert = {'7c3002ad756d76a643cb09cd45409608abb642d9': '10',
#           '7c303333756d555643cb09cd45409608abb642d9': '20',
#           '7c303333756d777643cb09c999409608abb642d9': '30',
#           '7c303333756d777643cb09caaa409608abb642d9': '40',
#           '111102ad756d76a643cb09cd45409608abb642d9': '50'}

# Update
Update = {
    '7c3002ad756d76a643cb09cd45409608abb642d9': '8',
    '7c303333756d777643cb09c999409608abb642d9': '24',
    '7c303333756d777643cb09caaa409608abb642d9': '42'
}
InsertNew = {'11113333756d76a643cb09cd45409608abb642d9': '6'}

from MPT import MerklePatriciaTrie

Tree = MerklePatriciaTrie()
for item in Insert:
    Tree.AddNode(item, Insert[item])

for item in Update:
    Tree.UpdateValue(item, Update[item])

for item in InsertNew:
    Tree.AddNode(item, InsertNew[item])

Tree.print()
