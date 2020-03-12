from math import sin, pi, cos
class Graf:

    def __init__(self, name="Graf"):
        self.name = name
        self.nodes = {}
        self.edge_wage={}
        self.adjacency_matrix={}
        self.incidence_matrix={}
        self.cordsX = {}
        self.cordsY = {}
        self.edgeCordsX= {}
        self.edgeCordsY= {}


    def add_node(self, node_1,cordX,cordY):
        node=str(node_1)
        self.nodes[node]=[]
        if node not in self.cordsX:
            self.cordsX[node]=[]
        if node not in self.cordsY:
            self.cordsY[node]=[]
        self.cordsX[node].append(cordX)
        self.cordsY[node].append(cordY) # addes node with cordx and cordy

    def add_edge_undirected(self, node_1, node_2, wage=1):
        node1=str(node_1)
        node2=str(node_2)
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        if node1+node2 not in self.nodes[node1]:
            self.temp_node=node1
            self.temp_node+=node2
            self.nodes[node1].append(self.temp_node)
            self.edge_wage[self.temp_node]=wage
        if node2+node1 not in self.nodes[node2]:
            self.temp_node=node2
            self.temp_node+=node1
            self.nodes[node2].append(self.temp_node)
            self.edge_wage[self.temp_node]=wage  # addes undirected edge

    def add_edge_directed(self, node1, node2, wage=1):
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        self.temp=node1
        self.temp+=node2
        self.nodes[node1].append(self.temp)
        self.edge_wage[self.temp]=wage # addes directed edge

    def create_adj_matrix(self,index_1,keys):
        index=str(index_1)
        self.adjacency_matrix[index]=[]
        self.adjacency_matrix[index].append(keys) #takes adj_matrix from GUI class and pass it to self.adjacency_matrix

    def convert_adj_matrix(self,nodequantity):
        radius=150 if nodequantity > 5 else 100 # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for name in range(nodequantity):
            self.add_node(name,round(sin(2*pi/nodequantity*i)*radius+225,0),round(cos(2*pi/nodequantity*i)*radius+225,0))
            i+=1
        for index in self.adjacency_matrix:
            for keys in self.adjacency_matrix[index]:
                if int(keys)==1:
                    self.add_edge_undirected(index[0],index[1]) #converts_matrix into graph

    def print_adj_matrix(self):
        print(self.adjacency_matrix) #prints adjacency_matrix

    def create_inc_matrix(self, index_1,keys):
        index=str(index_1)
        self.incidence_matrix[index]=[]
        self.incidence_matrix[index].append(keys)

    def convert_inc_matrix(self, nodequantity, edgequantity):
        radius=150 if nodequantity > 5 else 100 # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for name in range(nodequantity):
            self.add_node(name,round(sin(2*pi/nodequantity*i)*radius+225,0),round(cos(2*pi/nodequantity*i)*radius+225,0))
            i+=1
        for i in range(edgequantity):
            node1=None
            node2=None
            for l in range(nodequantity):
                index=str(l)+str(i)
                for keys in self.incidence_matrix[index]:
                    if int(keys)==1 and node1!=None:
                        node2=str(l)
                    if int(keys)==1 and node1==None:
                        node1=str(l)
                if node1 and node2:
                    self.add_edge_undirected(node1,node2)

    def print_inc_matrix(self):
        print(self.incidence_matrix)

    def clear_graph(self):
        self.__init__() #clear graph

    def print_graph(self):
        print(self.name)
        for source in sorted(self.nodes):
            print(source,":")
            for keys in self.nodes[source]:
                print(keys) #prints

    def return_X(self,node):
        self.cordx=self.cordsX[node].pop()
        self.cordsX[node].append(self.cordx)
        return self.cordx # returns cordX of node

    def return_Y(self,node):
        self.cordy=self.cordsY[node].pop()
        self.cordsY[node].append(self.cordy)
        return self.cordy # retruns cordY of node










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
