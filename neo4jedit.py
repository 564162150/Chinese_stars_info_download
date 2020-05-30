# coding:utf-8
from py2neo import Graph, Node, Relationship,NodeMatcher

##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', username='neo4j', password='jinglunfaking')

def deleteneo4j():
    graph.run('MATCH (n) DETACH DELETE n')


def starneo4j(sstarname,relation,starname):
    #节点数据
    #查询源人名是否已创建，如果已创建则直接取值，如果没创建，则创建
    node_1=graph.run("match(x) where x.title=\'%s\' return x" % (sstarname)).data()
    if node_1==[]:
        node_1 = Node('stars',label='stars', title=sstarname)
    else:
        node_1 = node_1[0]['x']
    node_2 = Node('stars',label='stars', title=starname)
    graph.create(node_2)

    node_1_guanxi=Relationship(node_1, relation , node_2)
    graph.create(node_1_guanxi)




# ##创建结点
# test_node_1 = Node(label='stars', name='皇帝')
# test_node_2 = Node(label='stars', name='皇后')
# test_node_3 = Node(label='stars', name='公主')
# graph.create(test_node_1)
# graph.create(test_node_2)
# graph.create(test_node_3)


# ##创建关系
# # 分别建立了test_node_1指向test_node_2和test_node_2指向test_node_1两条关系，关系的类型为"丈夫、妻子"，两条关系都有属性count，且值为1。
# node_1_zhangfu_node_1 = Relationship(test_node_1, '丈夫', test_node_2)
# node_1_zhangfu_node_1['count'] = 1
# node_2_qizi_node_1 = Relationship(test_node_2, '妻子', test_node_1)
# node_2_munv_node_1 = Relationship(test_node_2, '母女', test_node_3)
#
# node_2_qizi_node_1['count'] = 1
#
# graph.create(node_1_zhangfu_node_1)
# graph.create(node_2_qizi_node_1)
# graph.create(node_2_munv_node_1)
#
# print(graph)
# print(test_node_1)
# print(test_node_2)
# print(node_1_zhangfu_node_1)
# print(node_2_qizi_node_1)
# print(node_2_munv_node_1)
#
# a=graph.run('match (n) return n').data()
#
# for i in a:
#     print(i)