class Graf:

    def __init__(self, name="Graf"):
        self.name = name
        self.nodes = {}
        self.cordsX = {}
        self.cordsY = {}


    def add_node(self, node,cordX,cordY):
        self.nodes[node]=[]
        if node not in self.cordsX:
            self.cordsX[node]=[]
        if node not in self.cordsY:
            self.cordsY[node]=[]
        self.cordsX[node].append(cordX)
        self.cordsY[node].append(cordY)

    def add_edge_undirected(self, node1, node2):
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        if node2 not in self.nodes[node1]:
            self.nodes[node1].append(node2)
        if node1 not in self.nodes[node2]:
            self.nodes[node2].append(node1)

    def add_edge_directed(self, node1, node2):
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        self.nodes[node1].append(node2)

    def clear_graph(self):
        self.__init__()

    def print_graph(self):
        print(self.name)
        for source in self.nodes:
            print(source,":")
            for keys in self.nodes[source]:
                print(keys)


#    def remove_Node(self,node):

    #    self.nodes.pop(node, node)









## TESTS

#graf=Graf()
#graf.add_node('B',0,0)
#graf.add_node('A',150,300)
#graf.add_node('C',100,200)

#graf.add_edge_undirected('A','B')
#graf.add_edge_undirected('A','C')
#graf.add_edge_undirected('B','A')
#graf.remove_Node('B')

#graf.print_graph()


#graf.add_edge_undirected('A','B')
#graf.add_edge_undirected('A','R')
#graf.add_edge_undirected('B','B')
#graf.add_edge_undirected('B','B')
#graf.add_edge_directed('A','D')
#graf.print_graph()
#graf.add_edge_undirected('C','B')
#print(graf.nodes)
#print(graf.edges)
#graf.print_graph()
