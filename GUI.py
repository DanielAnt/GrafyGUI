from tkinter import *
from tkinter import ttk, colorchooser, messagebox
from Grafy import *
from PIL import Image, ImageTk
from math import *




class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.switch_variable = StringVar(value="")
        self.selected=False
        self.remove=False
        self.entry={}
        self.adj_list_nodes={}
        self.drawWidgets()
        self.tools(self.switch_variable)
        self.c.bind('<ButtonPress-1>',self.Cords)
        self.c.bind('<ButtonRelease-1>',self.reset) # init

    def drawWidgets(self):
        self.controls=Frame(self.master,padx=5,pady=5,bg="black")
        self.buttons=Frame(self.controls,padx=3,pady=3, bd=2,relief="sunken")
        self.buttons.pack(side=LEFT)
        self.draw_button = Radiobutton(self.buttons, text="AddNode",variable=self.switch_variable,indicatoron=False, value="draw", height=1)
        self.draw_Entry= Entry(self.buttons,width=5,justify=RIGHT)
        self.select_button = Radiobutton(self.buttons, text="Select",variable=self.switch_variable,indicatoron=False, value="select", height=1)
        self.removeNode_button = Button(self.buttons, text="Remove Node", command=self.remove_node, height=1)
        self.unEdge_button = Radiobutton(self.buttons, text="UnEdge",variable=self.switch_variable,indicatoron=False, value="drawUndirected", height=1)
        self.directedEdge_button = Radiobutton(self.buttons, text="directedEdge",variable=self.switch_variable,indicatoron=False, value="drawDirected", height=1)
        self.buttonPrint= Button(self.buttons,text = "Print", command= self.print_graph, height=1)
        self.var1=IntVar()
        self.directed_CheckButton= Checkbutton(self.controls, text="directed", variable=self.var1)
        self.draw_Entry.pack(side="left",fill=Y, expand=True)
        self.draw_button.pack(side="left",fill=Y, expand=True)
        self.removeNode_button.pack(side="left",fill=Y, expand=True)
        self.unEdge_button.pack(side="left",fill=Y, expand=True)
        self.directedEdge_button.pack(side="left",fill=Y, expand=True)
        self.select_button.pack(side="left",fill=Y, expand=True)
        self.buttonPrint.pack(side="left")
        self.directed_CheckButton.pack(side="left")
        self.controls.pack(side=TOP,fill=X, expand=False)


        self.print=Canvas(self.master,height=400,width=300, bg=self.color_bg)
        self.print.pack(side=LEFT,fill=Y,expand=False)


        self.c=Canvas(self.master,width=500,height=400,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)


        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.graphmenu= Menu(self.menu)
        self.menu.add_cascade(label='Add graph', menu=self.graphmenu)
        self.graphmenu.add_command(label='Macierz sąsiedzctwa',command=self.graph_add_adj)
        self.graphmenu.add_command(label='Macierz incydencji',command=self.graph_add_inc)
        self.graphmenu.add_command(label='Macierz lista sąsiedzctwa',command=self.graph_add_adjlist)
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label='Options',menu=self.optionmenu)
        self.optionmenu.add_command(label='Clear',command=self.clear_canvas)
        self.optionmenu.add_command(label='Exit',command=self.master.destroy)
        self.devmenu = Menu(self.menu)
        self.menu.add_cascade(label='DEVTOOLS',menu=self.devmenu)
        self.devmenu.add_command(label='Graph Data',command=self.open_dev_window)

    def remove_node(self):
        if self.selected==True:
            self.remove=True
            graf.remove_node(self.node)
        if self.remove==True:
            self.clear_canvas_without_removing_graph()
            self.draw_nodes()
            self.draw_edges()
            self.remove=False
            self.node=None
            self.selected=False
        else:
            messagebox.showerror("Error", "Select node that you want to remove") # removes selected node

    def tools(self,task):
        self.tool=task   # changes tool used with mouse1


###############################################
##############CLEARING CANVAS##################

    def clear_canvas(self):
        self.c.delete(ALL)
        graf.clear_graph()
        self.print.delete(ALL)  # clears canvas and graph

    def clear_canvas_without_removing_graph(self):
        self.c.delete(ALL)
        self.print.delete(ALL)  #clear canvas without clearing graph

###############################################


###############################################
#########Display Methods######################
    def draw_nodes(self):
        for source in graf.nodes:
            self.c.create_image(graf.return_X(source),graf.return_Y(source), image=photo)
            self.c.create_text(graf.return_X(source)+10,graf.return_Y(source)-15,fill="darkblue",font="Times 10 italic bold", text=source)    #draw graph nodes

    def draw_edges(self):
        for node1 in graf.nodes:
            for node2 in graf.nodes:
                if str(node1)+str(node2) in graf.edge_wage:
                    self.c.create_line(graf.cordsX[node1],graf.cordsY[node1],graf.cordsX[node2],graf.cordsY[node2],width=1,fill="red",smooth=True)    #draw graph edges

    def print_graph(self):
        self.print.delete(ALL)
        self.text=graf.name
        self.text+="\n"
        for source in graf.nodes:
            self.text+=str(source)
            self.text+=":\n"
            for keys in graf.nodes[source]:
                self.text+=str(keys)
                self.text+="\n"
        self.print.create_text(50,200,fill="darkblue",font="Times 10 italic bold", text=self.text)   #prints graph on canvas

###############################################

###############################################
####### MOUSE CANVAS FUNCTIONS################
    def Cords(self,e):
        if self.tool!=self.switch_variable.get():
            self.tools(self.switch_variable.get())
        self.old_x= e.x
        self.old_y= e.y     # press mouse1

    def reset(self,e):

        if self.tool=="draw":
            if e.x==self.old_x and e.y==self.old_y:
                if not self.draw_Entry.get():
                    messagebox.showerror("Error", "You need to enter a letter")
                else:
                    if self.draw_Entry.get() not in graf.nodes:
                        self.new_x=int(50 * round(float(e.x)/50))
                        self.new_y=int(25 * round(float(e.y)/25))
                        self.exist=False
                        for keys in graf.cordsX:
                            if self.new_x in graf.cordsX[keys] and self.new_y in graf.cordsY[keys]:
                                self.exist=True
                                messagebox.showerror("Error", "You can't place two nodes in the same place")
                        if self.exist==False:
                            graf.add_node(self.draw_Entry.get(),self.new_x, self.new_y)
                            #self.c.create_line(self.new_x,self.new_y,self.new_x,self.new_y,width=10,fill="black",capstyle=ROUND,smooth=True)
                            self.c.create_image(self.new_x,self.new_y, image=photo)
                            self.c.create_text(self.new_x+10,self.new_y-15,fill="darkblue",font="Times 10 italic bold", text=self.draw_Entry.get())
                    else:
                        messagebox.showerror("Error", "You can't add more then one node with the same name")

        if self.tool=="drawUndirected":
            self.new_x=e.x
            self.new_y=e.y
            for source in graf.cordsX:
                for i in range(self.old_x-10,self.old_x+10):
                    if i in graf.cordsX[source]:
                        for k in range(self.old_y-20,self.old_y+20):
                            if k in graf.cordsY[source]:
                                for keys in graf.cordsX:
                                    for j in range(self.new_x-10,self.new_x+10):
                                        if j in graf.cordsX[keys]:
                                            for l in range(self.new_y-10,self.new_y+10):
                                                if l in graf.cordsY[keys]:
                                                    self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",smooth=True)
                                                    #self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",arrow='last',capstyle=ROUND,smooth=True)
                                                    graf.add_edge_undirected(source,keys)

        if self.tool=="drawDirected":
            self.new_x=e.x
            self.new_y=e.y
            for source in graf.cordsX:
                for i in range(self.old_x-10,self.old_x+10):
                    if i in graf.cordsX[source]:
                        for k in range(self.old_y-20,self.old_y+20):
                            if k in graf.cordsY[source]:
                                for keys in graf.cordsX:
                                    for j in range(self.new_x-10,self.new_x+10):
                                        if j in graf.cordsX[keys]:
                                            for l in range(self.new_y-10,self.new_y+10):
                                                if l in graf.cordsY[keys]:
                                                    #self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",smooth=True)
                                                    self.c.create_line(graf.return_X(source),graf.return_Y(source),graf.return_X(keys),graf.return_Y(keys),width=1,fill="red",arrow='last',capstyle=ROUND,smooth=True)
                                                    graf.add_edge_directed(source,keys)

        if self.tool=="select":
            self.new_x=e.x
            self.new_y=e.y
            for source in graf.cordsX:
                for i in range(self.old_x-10,self.old_x+10):
                    if i in graf.cordsX[source]:
                        for k in range(self.old_y-20,self.old_y+20):
                            if k in graf.cordsY[source]:
                                if self.selected==False:
                                    self.c.create_image(graf.cordsX[source],graf.cordsY[source], image=selectedPhoto)
                                    self.node=source
                                    self.selected=True
                                    break;
                                if self.selected==True and self.node==source:
                                    self.c.create_image(graf.cordsX[source],graf.cordsY[source], image=photo)
                                    self.node=None
                                    self.selected=False
                                    break;    # depress mouse1
###############################################

###############################################
#####ADDING GRAPH BY ADJACENCY MATRIX#########

    def graph_add_adj(self):
        self.graph_add_window = Tk()
        self.graph_add_window.attributes("-topmost",True)
        self.graph_add_window.title('Adajacency matrix')
        self.frame_one=Frame(self.graph_add_window,width=100,height=500,borderwidth=2,relief='sunken')
        self.frame_one.pack(side="left",fill=BOTH, expand=False)
        self.nodeQuantity_Label=Label(self.frame_one,font="Times 10 italic bold",text='How many Nodes?')
        self.nodeQuantity_Entry= Entry(self.frame_one,width=15,justify=RIGHT)
        self.nodeQuantity_Button= Button(self.frame_one,width=15,text="Submit",command=self.NodeQuantity_Submit)
        self.nodeQuantity_Label.pack(side=TOP)
        self.nodeQuantity_Entry.pack(side=TOP)
        self.nodeQuantity_Button.pack(side=TOP)
        self.graph_add_window.mainloop() #opens new window and ask for number of nodes for adjacency matrix

    def NodeQuantity_Submit(self):
        if self.nodeQuantity_Entry.get().isnumeric():
            self.temp_NodeQuantity=int(self.nodeQuantity_Entry.get())
            self.matrix_window=Tk()
            self.matrix_window.attributes("-topmost",True)
            self.matrix_window.title("Adjacency matrix")
            self.graph_add_window.destroy()
            self.frame_two=Frame(self.matrix_window,relief='sunken')
            self.frame_two.pack(side="left",fill=BOTH, expand=False)
            self.matrix_label=Label(self.frame_two,font="Times 10 italic bold", text="Enter matrix values")
            self.matrix_label.pack(side=TOP)
            self.entry_matrix={}
            self.matrix_frame=Frame(self.frame_two)
            self.matrix_frame.pack(side=TOP)
            for row in range(self.temp_NodeQuantity):
                for collumns in range(self.temp_NodeQuantity):
                    index=str(row)+str(collumns)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    matrix_entry.insert(END,"0")
                    matrix_entry.grid(row=row,column=collumns,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.matrix_adj_submit)
            self.adjacency_matrix_submit.pack(side=TOP)
            self.graph_add_window.mainloop()
        else:
            messagebox.showerror("Error", "You need to enter a number") #submits the number from graph_add_adj entry

    def matrix_adj_submit(self):
        self.clear_canvas()
        self.matrix_error=False
        for index in self.entry_matrix:
            for keys in self.entry_matrix[index].get():
                if keys.isnumeric():
                    if int(keys)==1 or int(keys)==0:
                        graf.create_adj_matrix(index,keys)
                    else:
                        print(keys)
                        self.matrix_error=True
                        break;
                else:
                    print(keys)
                    self.matrix_error=True
                    break;
        if self.matrix_error==False:
            graf.convert_adj_matrix(self.temp_NodeQuantity)
            self.draw_nodes()
            self.draw_edges()
            self.matrix_window.destroy() # submits entered matrix into graph and draws it
        else:
            messagebox.showerror("Error", "Wrong data in matrix")
            graf.adjacency_matrix={} #submits matrix
###############################################

###############################################
#######ADDING GRAPH BY INCIDENCE MATRIX #######

    def graph_add_inc(self):
        self.graph_add_window = Tk()
        self.graph_add_window.attributes("-topmost",True)
        self.graph_add_window.title('Incidence matrix')
        self.frame_one=Frame(self.graph_add_window,width=100,height=500,borderwidth=2,relief='sunken')
        self.frame_one.pack(side="left",fill=BOTH, expand=False)
        self.nodeQuantity_Label=Label(self.frame_one,font="Times 10 italic bold",text='Number of nodes?')
        self.nodeQuantity_Entry= Entry(self.frame_one,width=15,justify=RIGHT)
        self.edgeQuantity_Label=Label(self.frame_one,font="Times 10 italic bold",text='Number of edges?')
        self.edgeQuantity_Entry= Entry(self.frame_one,width=15,justify=RIGHT)
        self.Quantity_Button= Button(self.frame_one,width=15,text="Submit",command=self.Quantity_Submit)
        self.nodeQuantity_Label.pack(side=TOP)
        self.nodeQuantity_Entry.pack(side=TOP)
        self.edgeQuantity_Label.pack(side=TOP)
        self.edgeQuantity_Entry.pack(side=TOP)
        self.Quantity_Button.pack(side=TOP,pady=5)
        self.graph_add_window.mainloop() #opens new window and ask for number of nodes and edges for incidence matrix

    def Quantity_Submit(self):
        if self.nodeQuantity_Entry.get().isnumeric() and self.edgeQuantity_Entry.get().isnumeric():
            self.temp_NodeQuantity=int(self.nodeQuantity_Entry.get())
            self.temp_EdgeQuantity=int(self.edgeQuantity_Entry.get())
            self.matrix_window=Tk()
            self.matrix_window.attributes("-topmost",True)
            self.matrix_window.title("Adjacency matrix")
            self.graph_add_window.destroy()
            self.frame_two=Frame(self.matrix_window,relief='sunken')
            self.frame_two.pack(side="left",fill=BOTH, expand=False)
            self.matrix_label=Label(self.frame_two,font="Times 10 italic bold", text="Enter matrix values")
            self.matrix_label.pack(side=TOP)
            self.entry_matrix={}
            self.matrix_frame=Frame(self.frame_two)
            self.matrix_frame.pack(side=TOP)
            for row in range(self.temp_NodeQuantity):
                for collumns in range(self.temp_EdgeQuantity):
                    index=str(row)+str(collumns)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    matrix_entry.insert(END,"0")
                    matrix_entry.grid(row=row,column=collumns,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.matrix_inc_submit)
            self.adjacency_matrix_submit.pack(side=TOP)
            self.matrix_window.mainloop() # submits the data from graph_add_inc

    def matrix_inc_submit(self):
        self.clear_canvas()
        self.matrix_error=False
        for index in self.entry_matrix:
            for keys in self.entry_matrix[index].get():
                if keys.isnumeric():
                    if int(keys)==1 or int(keys)==0:
                        graf.create_inc_matrix(index,keys)
                    else:
                        self.matrix_error=True
                        break;
                else:
                    self.matrix_error=True
                    break;
        if self.matrix_error==False:
            graf.convert_inc_matrix(self.temp_NodeQuantity,self.temp_EdgeQuantity)
            self.draw_nodes()
            self.draw_edges()

            self.matrix_window.destroy() # submits entered matrix into graph and draws it
        else:
            messagebox.showerror("Error", "Wrong data in matrix")
            graf.incidence_matrix={} #submits matrix

###############################################

###############################################
#######ADDING GRAPH BY ADJACENCY LIST#########

    def graph_add_adjlist(self):
        #window
        self.graph_adj_list = Tk()
        self.graph_adj_list.geometry("285x280")
        self.graph_adj_list.resizable(False,False)
        self.graph_adj_list.attributes("-topmost",True)
        self.graph_adj_list.title('Adajacency matrix')

        #frames
        self.frame_buttons= Frame(self.graph_adj_list,width=50,height=50,padx=1)
        self.frame_nodes= Frame(self.graph_adj_list,width=50,height=50,padx=1)
        self.frame_edges= Frame(self.graph_adj_list,width=50,height=50,padx=1)

        #frame buttons
        self.node_label=Label(self.frame_buttons,font="Times 10 italic bold",text='Node name')
        self.node_list_entry=Entry(self.frame_buttons,width=15,justify=RIGHT)
        self.node_add_button=Button(self.frame_buttons,text="Add",width=10,command=self.graph_adj_list_add_node)
        self.node_remove_button=Button(self.frame_buttons,text="Remove",width=10, command=self.graph_adj_list_remove_node)
        self.node_submit_button=Button(self.frame_buttons,text="Submit",width=10, command=self.graph_adj_list_submit)

        #frame nodes
        self.node_listbox= Listbox(self.frame_nodes, width=8,height=10,justify=RIGHT)
        self.node_button_show_edges= Button(self.frame_nodes, width=3, text=">>", command=self.chose_node)

        #frame edges
        self.edge_listbox_available_nodes=Listbox(self.frame_edges,width=10,height=5,justify=RIGHT)
        self.edge_add_button=Button(self.frame_edges,text="Add",width=7, command= self.graph_adj_list_add_edge)
        self.edge_listbox_added_nodes=Listbox(self.frame_edges,width=10,height=5,justify=RIGHT)
        self.edge_remove_button=Button(self.frame_edges,text="Remove",width=7, command= self.graph_adj_list_remove_edge)

        #frames.grid()
        self.frame_buttons.grid(row=0,column=0,sticky="nsew")
        self.frame_nodes.grid(row=0,column=1,sticky="nsew")
        self.frame_edges.grid(row=0,column=2,sticky="nsew")

        #frame_buttons.grid()
        self.node_label.grid(row=0,column=0)
        self.node_list_entry.grid(row=1,column=0)
        self.node_add_button.grid(row=2,column=0)
        self.node_remove_button.grid(row=3,column=0)
        self.node_submit_button.grid(row=4,column=0)

        #frame nodes.grid()
        self.node_listbox.grid(row=0,column=0)
        self.node_button_show_edges.grid(row=1,column=0)


        #frame edges.grid()
        self.edge_listbox_available_nodes.grid(row=0,column=0)
        self.edge_add_button.grid(row=1,column=0)
        self.edge_listbox_added_nodes.grid(row=2,column=0)
        self.edge_remove_button.grid(row=3,column=0)

        self.graph_adj_list.mainloop()


    def graph_adj_list_add_node(self):
        if self.node_list_entry.get():      # checks if there an entry
            self.if_node_already_in_list=False
            self.temp_node=self.node_list_entry.get()
            self.list_node=self.node_listbox.get(0,END)
            for keys in self.list_node:    # checks if this node is already in the list
                if keys==self.temp_node:
                    self.if_node_already_in_list=True
            if self.if_node_already_in_list==False:   # adds node to adj_list_nodes
                self.node_listbox.insert(END,self.temp_node)
                self.adj_list_nodes[self.node_list_entry.get()]=[]
            else:
                messagebox.showerror("Error", "There is already a node with this name")
        else:
            messagebox.showerror("Error", "Entry box can't be empty")

    def graph_adj_list_remove_node(self):
        if self.node_listbox.get(ANCHOR):   #checks if any of list entrys is selected
            for index in self.adj_list_nodes: #searches for edges with givien node like AB and BA etc
                i=0
                for keys in self.adj_list_nodes[index]:
                    if index+self.node_listbox.get(ANCHOR)==keys or self.node_listbox.get(ANCHOR)+index==keys:
                        self.adj_list_nodes[index].pop(i)
                    i+=1
            del self.adj_list_nodes[str(self.node_listbox.get(ANCHOR))] # delete chosen node
            #clears listboxes
            self.node_listbox.delete(ANCHOR)
            self.edge_listbox_available_nodes.delete(0,END)
            self.edge_listbox_added_nodes.delete(0,END)

    def chose_node(self):
        if self.node_listbox.get(ANCHOR): # check if any listentry is selected
            self.temp_chosen_node=self.node_listbox.get(ANCHOR) #saves chosen node so it remebers it while using other buttons
            self.edge_listbox_available_nodes.delete(0,END)
            self.edge_listbox_added_nodes.delete(0,END)
            self.display_edge_listbox_added_nodes()
            self.display_edge_listbox_available_nodes()

    def graph_adj_list_add_edge(self):
        if self.edge_listbox_available_nodes.get(ANCHOR): #checks if good listentry is selected
            if self.edge_listbox_available_nodes.get(ANCHOR) not in self.adj_list_nodes[self.temp_chosen_node]: #checks if given edge is already in graph
                for index in self.adj_list_nodes: #adds given edge do graph
                    for index1 in self.adj_list_nodes:
                        if index+index1==self.edge_listbox_available_nodes.get(ANCHOR):
                            if self.edge_listbox_available_nodes.get(ANCHOR) not in self.adj_list_nodes[self.temp_chosen_node]:
                                self.adj_list_nodes[index].append(index+index1)
                                self.adj_list_nodes[index1].append(index1+index)
            self.display_edge_listbox_added_nodes()
            self.display_edge_listbox_available_nodes()

    def graph_adj_list_remove_edge(self):
        if self.edge_listbox_added_nodes.get(ANCHOR): # checks if good listentry is selected
            for index in self.adj_list_nodes: #searches for nodes of edge that is going to be removed
                for index1 in self.adj_list_nodes:
                    if self.edge_listbox_added_nodes.get(ANCHOR)==index+index1:
                        self.temp_node1=index
                        self.temp_node2=index1
                        break;
            for index in self.adj_list_nodes: #removes selected edge
                i=0
                for keys in self.adj_list_nodes[index]:
                    if keys==self.temp_node1+self.temp_node2:
                        self.adj_list_nodes[index].pop(i)
                    if keys==self.temp_node2+self.temp_node1:
                        self.adj_list_nodes[index].pop(i)
                    i+=1
            self.display_edge_listbox_added_nodes()
            self.display_edge_listbox_available_nodes()

    def graph_adj_list_submit(self):  # submits input data into graph and then draws it
        self.clear_canvas()
        nodequantity=len(self.adj_list_nodes)
        radius=150 if nodequantity > 5 else 100 # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for index in self.adj_list_nodes:
            graf.add_node(index,round(sin(2*pi/nodequantity*i)*radius+225,0),round(cos(2*pi/nodequantity*i)*radius+225,0))
            i+=1
            for index1 in self.adj_list_nodes:
                for keys in self.adj_list_nodes[index]:
                    if index+index1==keys:
                        graf.add_edge_undirected(index,index1)
        self.draw_nodes()
        self.draw_edges()
        self.adj_list_nodes={}
        self.node_listbox.delete(0,END)
        self.edge_listbox_added_nodes.delete(0,END)
        self.edge_listbox_available_nodes.delete(0,END)

##### adj_list window listboxes display functionn ###
    def display_edge_listbox_added_nodes(self):
        self.edge_listbox_added_nodes.delete(0,END)
        for index in self.adj_list_nodes: # display added edges
            if index==self.temp_chosen_node:
                for keys in self.adj_list_nodes[index]:
                    self.edge_listbox_added_nodes.insert(END,keys)

    def display_edge_listbox_available_nodes(self):
        self.edge_listbox_available_nodes.delete(0,END)
        for index in self.adj_list_nodes: # display available edges
            if self.temp_chosen_node==index:
                for index2 in self.adj_list_nodes:
                    if index!=index2 and index+index2 not in self.adj_list_nodes[index]:
                        self.edge_listbox_available_nodes.insert(END, index+index2)

###############################################


    def open_dev_window(self):
        self.dev_window= Tk()
        self.dev_window.geometry("250x250")
        self.dev_window.attributes("-topmost",True)
        self.dev_window.title('Adajacency matrix')
        self.dev_window.resizable(False,False)

        self.dev_window_frame=Frame(self.dev_window)
        self.dev_window_frame.pack(fill=BOTH, expand=False)

        self.dev_print_grafnodes= Button(self.dev_window_frame,text="Print GRAF.NODES",command=lambda: print(graf.nodes))
        self.dev_print_cordsX= Button(self.dev_window_frame,text="Print cordsX",command=lambda: print(graf.cordsX) )
        self.dev_print_cordsY= Button(self.dev_window_frame,text="Print cordsY",command=lambda: print(graf.cordsY))
        self.dev_print_adjacencymatrix= Button(self.dev_window_frame,text="Print adjacencymatrix",command=lambda: print(graf.adjacency_matrix))
        self.dev_print_incidencematrix= Button(self.dev_window_frame,text="Print incmatrix",command=lambda: print(graf.incidence_matrix))

        self.dev_print_grafnodes.grid(row=0,column=0)
        self.dev_print_cordsX.grid(row=1,column=0)
        self.dev_print_cordsY.grid(row=2,column=0)
        self.dev_print_adjacencymatrix.grid(row=3,column=0)
        self.dev_print_incidencematrix.grid(row=4,column=0)
        self.dev_window.mainloop()


"""
    def print_entry(self):
        text=""
        if self.entry:
            for name in self.entry:
                text+=str(self.entry[name].get())
        print(text) # prints entry does nothing ATM (test function)


    def create_Adjacency_Matrix(self):
        self.clear_canvas()
        self.temp=int(self.nodeQuantity_Entry.get())
        i=1
        for name in self.entry:
            graf.create_Adj_Matrix(name,self.entry[name].get())
            graf.add_node(name,round(sin(2*pi/self.temp*i)*100+200,0),round(cos(2*pi/self.temp*i)*100+200,0))
            i+=1
        graf.convert_matrix()
        for name in graf.nodes:
            self.c.create_image(round(graf.return_X(name),0),round(graf.return_Y(name),0), image=photo)
            self.c.create_text(graf.return_X(name)+10,graf.return_Y(name)-15,fill="darkblue",font="Times 10 italic bold", text=name)
        for node1 in graf.nodes:
            for node2 in graf.nodes:
                if node1+node2 in graf.edge_wage:
                    self.c.create_line(graf.cordsX[node1],graf.cordsY[node1],graf.cordsX[node2],graf.cordsY[node2],width=1,fill="red",smooth=True)
        self.entry={}
            self.graph_add_window.destroy()  # DOES NOTHING ATM

"""



if __name__ == '__main__':

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            quit()


    graf= Graf()
    root = Tk()
    image = Image.open("node.jpg")
    photo = ImageTk.PhotoImage(image)
    selected = Image.open("nodeselected.jpg")
    selectedPhoto = ImageTk.PhotoImage(selected)
    main(root)
    root.title('Grafy')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
