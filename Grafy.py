from math import sin, pi, cos
class Graf:

    def __init__(self, name="Graf"):
        self.name = name
        self.nodes = {}
        self.edge_quantity={}
        self.edge_wage={}
        self.adj_list={}
        self.adjacency_matrix={}
        self.incidence_matrix={}
        self.cordsX = {}
        self.cordsY = {}
        self.edgeCordsX= {}
        self.edgeCordsY= {}
        self.times_has_been_drawn={}
        self.pointer={}   ##### for numerating nodes (important for conversion from list to matrix) #####


################ Adding and removing stuff from graph ####################
    def add_node(self, node_1,cordX,cordY):
        node=str(node_1)
        self.nodes[node]=[]
        if node not in self.cordsX:
            self.cordsX[node]=[]
        if node not in self.cordsY:
            self.cordsY[node]=[]
        self.cordsX[node].append(int(cordX))
        self.cordsY[node].append(int(cordY)) # addes node with cordx and cordy

    def change_wage(self,node1,node2,wage):
        if node1+node2 in self.edge_wage:
            self.edge_wage[str(node1)+str(node2)]=int(wage)

    def remove_node(self,node_1): #removes node
        self.temp_node=str(node_1)
        del self.nodes[self.temp_node]
        del self.cordsX[self.temp_node]
        del self.cordsY[self.temp_node]
        for index in self.nodes:
            i=0
            for keys in self.nodes[index]:
                if str(index)+self.temp_node==str(keys):
                    self.nodes[index].pop(i)
                i+=1
        for index in self.nodes:
            if index+self.temp_node in self.edge_quantity:
                del self.edge_quantity[index+self.temp_node]
            if self.temp_node+index in self.edge_quantity:
                del self.edge_quantity[self.temp_node+index]

    def remove_edge(self,node1,node2):
        remove_first=False
        remove_second=False
        temp_second_edgequantity_equal_one=False
        temp_first_edgequantity_equal_one=False
        for nodes in self.nodes:
            i=0
            for keys in self.nodes[nodes]:
                if node1+node2==keys and nodes==node1 and remove_first==False:
                    self.nodes[nodes].pop(i)
                    remove_first=True
                if node2+node1==keys and nodes==node2 and remove_second==False:
                    self.nodes[nodes].pop(i)
                    remove_second=True
                i+=1
        for edges in self.edge_quantity:
            if node1+node2==edges:
                if self.edge_quantity[edges]==1:
                    temp_first_edgequantity_equal_one=True
                else:
                    self.edge_quantity[edges]-=1
            if node2+node1==edges:
                if self.edge_quantity[edges]==1:
                    temp_second_edgequantity_equal_one=True
                else:
                    self.edge_quantity[edges]-=1
        if temp_first_edgequantity_equal_one==True:
            del self.edge_quantity[node1+node2]
        if temp_second_edgequantity_equal_one==True:
            del self.edge_quantity[node2+node1]
            self.convert_to_adj_list()

    def add_edge_undirected(self, node_1, node_2, wage=1):
        node1=str(node_1)
        node2=str(node_2)
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        if node1!=node2:
            self.temp_node=node1
            self.temp_node+=node2
            self.nodes[node1].append(self.temp_node)
            self.edge_wage[self.temp_node]=wage
            self.add_edge_quantity(self.temp_node)

            self.temp_node=node2
            self.temp_node+=node1
            self.nodes[node2].append(self.temp_node)
            self.edge_wage[self.temp_node]=wage  # addes undirected edge
            self.add_edge_quantity(self.temp_node)
        else:
            self.temp_node=node1
            self.temp_node+=node2
            self.nodes[node1].append(self.temp_node)
            self.edge_wage[self.temp_node]=wage
            self.add_edge_quantity(self.temp_node)

    def add_edge_directed(self, node1, node2, wage=1):
        if node2 not in self.nodes:
            self.nodes[node2]=[]
        if node1 not in self.nodes:
            self.nodes[node1]=[]
        self.temp_node=node1
        self.temp_node+=node2
        self.nodes[node1].append(self.temp_node)
        self.edge_wage[self.temp_node]=wage # addes directed edge
        self.add_edge_quantity(self.temp_node)

    def add_edge_quantity(self,temp):
        if temp not in self.edge_quantity:
            self.edge_quantity[temp]=0
        temp_quantity=self.edge_quantity[temp]
        temp_quantity+=1
        self.edge_quantity[temp]=temp_quantity

########### For creaing graph from adj matrix ##############

    def create_adj_matrix(self,index_1,keys):
        index=str(index_1)
        self.adjacency_matrix[index]=[]
        self.adjacency_matrix[index].append(keys) #takes adj_matrix from GUI class and pass it to self.adjacency_matrix

    def convert_adj_matrix(self,nodequantity,draw_ratio_var=1):
        radius=150*(draw_ratio_var-1) if nodequantity > 5 else 100*(draw_ratio_var-1) # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for name in range(nodequantity):
            self.add_node(name,round(sin(2*pi/nodequantity*i)*radius+(225+(draw_ratio_var-1)*80)),round(cos(2*pi/nodequantity*i)*radius+(225+(draw_ratio_var-1)*80)))
            i+=1
        for index in self.adjacency_matrix:
            for keys in self.adjacency_matrix[index]:
                if index[0]>=index[1]:
                    for i in range(int(keys)):
                        self.add_edge_undirected(index[0],index[1]) #converts_matrix into graph

######### Functions for creating graph from incidence matrix #########
    def create_inc_matrix(self, index_1,keys):
        index=str(index_1)
        self.incidence_matrix[index]=[]
        self.incidence_matrix[index].append(keys)

    def convert_inc_matrix(self, nodequantity, edgequantity,draw_ratio_var=1):
        radius=150*(draw_ratio_var-1) if nodequantity > 5 else 100*(draw_ratio_var-1) # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for name in range(nodequantity):
            self.add_node(name,round(sin(2*pi/nodequantity*i)*radius+(225+(draw_ratio_var-1)*80)),round(cos(2*pi/nodequantity*i)*radius+(225+(draw_ratio_var-1)*80)))
            i+=1
        for i in range(edgequantity):
            node1=None
            node2=None
            for l in range(nodequantity):
                index=str(l)+str(i)
                if self.incidence_matrix[index]==['1'] and node1!=None:
                    node2=str(l)
                if self.incidence_matrix[index]==['1'] and node1==None:
                    node1=str(l)
                if node1 and node2:
                    self.add_edge_undirected(node1,node2)
                    node1=None
                    node2=None

########### Utility stuff ############################
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
        return float(self.cordx) # returns cordX of node

    def return_Y(self,node):
        self.cordy=self.cordsY[node].pop()
        self.cordsY[node].append(self.cordy)
        return float(self.cordy) # retruns cordY of node

########### CONVERSIONS #########################

    def convert_to_adj_list(self):
        self.adj_list={}
        for index in self.nodes:
            self.adj_list[str(index)]=[]
            for index2 in self.nodes:
                for keys in self.nodes[index]:
                    if index+index2==keys:
                        self.adj_list[str(index)].append(str(index2))

    def convert_to_adj_matrix(self):
        self.convert_to_adj_list()
        i=0
        for nodes in self.nodes:
            self.pointer[nodes]=str(i)
            i+=1
        self.ignorednodes=[]
        for node in self.nodes:
            for key in self.nodes:
                if key not in self.ignorednodes:
                    if node+key in self.edge_quantity:
                        self.adjacency_matrix[self.pointer[node]+self.pointer[key]]=self.edge_quantity[node+key]
                        self.adjacency_matrix[self.pointer[key]+self.pointer[node]]=self.edge_quantity[node+key]
                    else:
                        self.adjacency_matrix[self.pointer[node]+self.pointer[key]]=0
                        self.adjacency_matrix[self.pointer[key]+self.pointer[node]]=0
            self.ignorednodes.append(node)

    def convert_to_inc_matrix(self):
        i=0
        for nodes in self.nodes:
            self.pointer[nodes]=str(i)
            i+=1
        i=0
        self.ignorednodes=[]
        for node in self.nodes:
            for key in self.nodes:
                if node+key not in self.ignorednodes:
                    if node+key in self.edge_quantity:
                        self.ignorednodes.append(node+key)
                        self.ignorednodes.append(key+node)
                        for quantity in range(int(self.edge_quantity[node+key])):
                            for nodenumber in range(len(self.pointer)):
                                if str(nodenumber)==str(self.pointer[node]) or str(nodenumber)==str(self.pointer[key]):
                                    self.incidence_matrix[str(nodenumber)+str(i)]=1
                                else:
                                    self.incidence_matrix[str(nodenumber)+str(i)]=0
                            i+=1
