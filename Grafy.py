class Graf:

    def __init__(self, name="Graf"):
        self.name = name
        self.nodes = {}
        self.adjacency_matrix={}
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

    def create_Adj_Matrix(self,node, matrix):
        self.adjacency_matrix[node]=[]
        self.adjacency_matrix[node].append(matrix)

    def convert_matrix(self):
        if self.adjacency_matrix:
            for name in self.adjacency_matrix:
                for keys in self.adjacency_matrix[name]:
                    self.temp=0
                    for numbers in keys:
                        self.temp+=1
                        if int(numbers)==1 and self.temp==1:
                            self.add_edge_undirected(name,'A')
                        if int(numbers)==1 and self.temp==2:
                            self.add_edge_undirected(name,'B')
                        if int(numbers)==1 and self.temp==3:
                            self.add_edge_undirected(name,'C')
                        if int(numbers)==1 and self.temp==4:
                            self.add_edge_undirected(name,'D')
                        if int(numbers)==1 and self.temp==5:
                            self.add_edge_undirected(name,'E')
                        if int(numbers)==1 and self.temp==6:
                            self.add_edge_undirected(name,'F')
        #else:

    def clear_graph(self):
        self.__init__()

    def print_graph(self):
        print(self.name)
        for source in sorted(self.nodes):
            print(source,":")
            for keys in self.nodes[source]:
                print(keys)

    def return_X(self,node):
        self.cordx=self.cordsX[node].pop()
        self.cordsX[node].append(self.cordx)
        return self.cordx

    def return_Y(self,node):
        self.cordy=self.cordsY[node].pop()
        self.cordsY[node].append(self.cordy)
        return self.cordy

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
