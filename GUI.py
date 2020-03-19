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
        self.file = Menu(self.menu)
        self.menu.add_cascade(label='file',menu=self.file)
        self.file.add_command(label='Save',command=self.save)
        self.file.add_command(label='Load',command=self.load)




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
        graf.convert_to_adj_list()
        graf.times_has_been_drawn={}
        for index in graf.edge_quantity:
            graf.times_has_been_drawn[index]=0
        for node1 in graf.adj_list:
            for node2 in graf.adj_list[node1]:
                    #self.c.create_line(graf.cordsX[node1],graf.cordsY[node1],graf.cordsX[node2],graf.cordsY[node2],width=1,fill="red",smooth=True)    #draw graph edges
                    self.create_line_arc(node1,node2)

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

    def create_line_arc(self,node1,node2):
        if node1==node2:
            #self.c.create_oval(graf.return_X(node1)+25,graf.return_Y(node1)+25,graf.return_X(node1),graf.return_Y(node1))
            self.c.create_line(graf.return_X(node1)+5,graf.return_Y(node1)+5,graf.return_X(node1),graf.return_Y(node1)-35,graf.return_X(node1)-35,graf.return_Y(node1)-35,graf.return_X(node1)-35,graf.return_Y(node1),graf.return_X(node2)+5,graf.return_Y(node2)+5,width=1,fill="red",smooth=True)    #draw graph edges


        else:
            if graf.edge_quantity[node1+node2]==1:
                self.c.create_line(graf.return_X(node1),graf.return_Y(node1),graf.return_X(node2),graf.return_Y(node2),width=1,fill="red",smooth=True)    #draw graph edges
                self.temp=graf.times_has_been_drawn[node1+node2]
                self.temp+=1
                graf.times_has_been_drawn[node1+node2]=self.temp
                graf.times_has_been_drawn[node2+node1]=self.temp
            else:
                if graf.times_has_been_drawn[node1+node2] < graf.edge_quantity[node1+node2]:
                    ratio = graf.edge_quantity[node1+node2]-graf.times_has_been_drawn[node1+node2]
                    if ratio<=2:
                        z=15
                    if ratio>2 and ratio<=4:
                        z=30
                    if ratio>4 and ratio<=6:
                        z=50
                    if ratio>6 and ratio<=8:
                        z=70
                    if ratio>8:
                        z=90
                    x=graf.return_X(node1)
                    y=graf.return_Y(node1)
                    x1=graf.return_X(node2)
                    y1=graf.return_Y(node2)
                    if x==x1:
                        x+=1
                    if y==y1:
                        y+=1
                    ymid=(y+y1)/2
                    xmid=(x+x1)/2
                    a1=-(x-x1)/(y-y1)
                    b1=ymid-xmid*a1
                    VarA=float((1+a1**2))
                    VarB=float(((-2)*xmid+2*a1*b1-2*a1*ymid))
                    VarC=float((xmid**2)+(b1**2)-2*b1*ymid+(ymid**2)-(z**2))
                    DELTA=float(VarB**2-4*VarA*VarC)
                    X_wynik1=float((-VarB+sqrt(DELTA))/(2*VarA))
                    X_wynik2=float((-VarB-sqrt(DELTA))/(2*VarA))
                    Y_wynik1=a1*X_wynik1+b1
                    Y_wynik2=a1*X_wynik2+b1
                    if ratio % 2 == 0:
                        self.c.create_line(graf.return_X(node1),graf.return_Y(node1),X_wynik1,Y_wynik1,graf.return_X(node2),graf.return_Y(node2),width=1,fill="red",smooth=True)    #draw graph edges
                    else:
                        self.c.create_line(graf.return_X(node1),graf.return_Y(node1),X_wynik2,Y_wynik2,graf.return_X(node2),graf.return_Y(node2),width=1,fill="red",smooth=True)    #draw graph edges
                    self.temp=graf.times_has_been_drawn[node1+node2]
                    self.temp+=1
                    graf.times_has_been_drawn[node1+node2]=self.temp
                    graf.times_has_been_drawn[node2+node1]=self.temp

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
                                                    graf.add_edge_undirected(source,keys)
                                                    self.clear_canvas_without_removing_graph()
                                                    self.draw_nodes()
                                                    self.draw_edges()
                                                    #self.c.create_line(graf.return_X(source),graf.return_Y(source),graf.return_Y(source),graf.return_X(keys),graf.return_X(keys),graf.return_Y(keys),width=1,fill="red",smooth=True)
                                                    #self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",arrow='last',capstyle=ROUND,smooth=True)


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
        self.node_get_button=Button(self.frame_buttons,text="GET",width=10, command=self.get_adj_list)

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
        self.node_get_button.grid(row=5,column=0)

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
        #    if self.edge_listbox_available_nodes.get(ANCHOR) not in self.adj_list_nodes[self.temp_chosen_node]: #checks if given edge is already in graph
            i=0
            for index in self.adj_list_nodes: #adds given edge do graph
                for index1 in self.adj_list_nodes:
                    if index+index1==self.edge_listbox_available_nodes.get(ANCHOR):
                #        if self.edge_listbox_available_nodes.get(ANCHOR) not in self.adj_list_nodes[self.temp_chosen_node]:
                        if i==0:
                            self.adj_list_nodes[index].append(index+index1)
                            self.adj_list_nodes[index1].append(index1+index)
                            i+=1
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
        for index in self.adj_list_nodes:
            for index1 in self.adj_list_nodes:
                for keys in self.adj_list_nodes[index]:
                    if index+index1==keys:
                        graf.add_edge_directed(index,index1)
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
                    #if index!=index2 and index+index2 not in self.adj_list_nodes[index]:
                    self.edge_listbox_available_nodes.insert(END, index+index2)

#### Import graf into  adj list ######

    def get_adj_list(self):
        self.adj_list_nodes={}
        for index in graf.nodes:
            self.adj_list_nodes[index]=[]
            for keys in graf.nodes[index]:
                self.adj_list_nodes[index].append(keys)

        for index in self.adj_list_nodes:
            self.node_listbox.insert(END,index)
        print(self.adj_list_nodes)

###############################################

###############################################
###### Eulerian Test #########################
    def eulerian_test(self):
        graf.convert_to_adj_list()
        if self.isConnected()==False:
            return 0
        else:
            odd=0
            for index in graf.adj_list:
                if len(graf.adj_list[index]) % 2 !=0:
                    odd+=1
            if odd==0:
                return 1
            elif odd==2:
                return 2
            elif odd>2:
                return 0

    def isConnected(self):
        visited={}
        for index in graf.adj_list:
            visited[index]=False
        i=0
        for index in graf.adj_list:
            if len(graf.adj_list[index])>=1:
                break;
            i+=1
        if i == len(graf.adj_list)-1:
            return True
        self.DFSUtil(index,visited)
        for index in graf.adj_list:
            if visited[index]==False and len(graf.adj_list[index])>0:
                return False
        return True

    def DFSUtil(self,v,visited):
        visited[v]=True
        for i in graf.adj_list[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited)

###############################################

###############################################
######    Euler path/circle    ################

    def printforall(self):
        graf.convert_to_adj_list()
        u=list(graf.adj_list.keys())[0]
        if self.eulerian_test()==1 or self.eulerian_test()==2:
            if self.eulerian_test()==1 and len(graf.edge_quantity)>0:
                print("cykl")
            if self.eulerian_test()==2 and len(graf.edge_quantity)>0:
                print("ścieżka")
            for i in graf.adj_list:
                if len(graf.adj_list[i]) %2 != 0:
                    u=i
                    break
            self.printEuler(u)
        else:
            print("Graf nie ma cyklu ani ścieżki eulera")

    def printEuler(self,u):
        for v in graf.adj_list[u]:
            if self.validNextEdge(u,v):
                print(u,"-",v),
                self.rmvEdge(u,v)
                self.printEuler(v)

    def Count(self,v,visited):
        count=1
        visited[v]=True
        for i in graf.adj_list[v]:
            if visited[i]==False:
                count=count+self.Count(i,visited)
        return count

    def validNextEdge(self,u, v):
        if len(graf.adj_list[u])==1:
            return True
        else:
            visited={}
            for index in graf.adj_list:
                visited[index]=False
            count1=self.Count(u,visited)

            self.rmvEdge(u,v)
            visited={}
            for index in graf.adj_list:
                visited[index]=False
            count2=self.Count(u,visited)

            self.addEdge(u,v)

            return False if count1 > count2 else True

    def rmvEdge(self,u,v):
        i=0
        for index in graf.adj_list[u]:
            if index==v:
                graf.adj_list[u].pop(i)
                break;
            i+=1
        i=0
        for index in graf.adj_list[v]:
            if index==u:
                graf.adj_list[v].pop(i)
                break;
            i+=1

    def addEdge(self,u,v):
        graf.adj_list[u].append(v)
        graf.adj_list[v].append(u)

###############################################
######    Euler path/circle    ################

    def hamilton_test(self):
        self.iterations=0
        self.consistency=True
        self.wtf=False
        self.path=[]
        self.longestPath=[]
        graph_len=len(graf.nodes)
        if graph_len < 2:
            print("Graph has one or fewer nodes")
            self.wtf=True
        graf.convert_to_adj_list()
        visited={}
        for index in graf.adj_list:
            visited[index]=False
        for index in graf.adj_list:
            if len(graf.adj_list[index])<1:
                self.consistency=False
                break;
        if self.consistency==True and self.wtf==False:
            u=list(graf.adj_list.keys())[0]
            self.isConsistent(visited, u)
        for index in visited:
            if visited[index]==False:
                print("Graph isn't consistent")
                self.wtf=True
                break;
        if self.wtf==False:
            self.path=[]
            self.pathvisited={}
            self.u=list(graf.adj_list.keys())[0]
            self.findPath(self.u)

    def isConsistent(self,visited,index):
        visited[index]=True
        for i in graf.adj_list[index]:
            if visited[i]==False:
                self.isConsistent(visited,i)

    def findPath(self,index):
        found=False
        self.tempstr=""
        self.path.append(index)
        print("trasa dla path",self.path)
        for keys in self.path:
            self.tempstr+=str(keys)
        if len(self.path)>len(self.longestPath):
            self.longestPath=[]
            for keys in self.path:
                self.longestPath.append(keys)
        if self.tempstr not in self.pathvisited:
            self.pathvisited[self.tempstr]=[]
        for i in graf.adj_list[index]:
            if i not in self.path:
                if i not in self.pathvisited[self.tempstr]:
                    found=True
                    break;
        if found==True:
            self.pathvisited[self.tempstr].append(i)
            self.findPath(i)
        if found!=True:
            if len(self.path)==len(graf.adj_list) and self.u in graf.adj_list[index] or self.iterations>150000:
                if self.u in graf.adj_list[index]:
                    if len(graf.nodes[self.u])>1:
                        self.path.append(self.u)
                        print("Found cycle")
                    else:
                        print("Found path")
                    print(self.path)
                    return 0
                else:
                    print("Longest path")
                    print(self.longestPath)
                    return 0
            else:
                self.iterations+=1
                h=self.path.pop()
                try:
                    i=self.path.pop()
                except (IndexError):
                    print("Longest path")
                    print(self.longestPath)
                    return 0
                self.findPath(i)





    #    if self.path
    #    self.path.pop()
    #    self.isConsistent(visited,self.path.pop())








###############################################
###### Dev options ###########################
    def open_dev_window(self):
        self.dev_window= Tk()
        self.dev_window.geometry("500x400")
        self.dev_window.attributes("-topmost",True)
        self.dev_window.title('Adajacency matrix')
        self.dev_window.resizable(False,False)

        self.dev_window_frame=Frame(self.dev_window)
        self.dev_window_frame.pack(fill=BOTH, expand=False)

        self.dev_print_grafnodes= Button(self.dev_window_frame,text="Print GRAF.NODES",command=lambda: print(graf.nodes))
        self.dev_print_cordsX= Button(self.dev_window_frame,text="Print cordsX",command=lambda: print(graf.cordsX) )
        self.dev_print_cordsY= Button(self.dev_window_frame,text="Print cordsY",command=lambda: print(graf.cordsY))
        self.dev_print_edge_quantity= Button(self.dev_window_frame,text="Print edge quantity",command=lambda: print(graf.edge_quantity))
        self.dev_print_adjacencymatrix= Button(self.dev_window_frame,text="Print adjacencymatrix",command=lambda: print(graf.adjacency_matrix))
        self.dev_print_incidencematrix= Button(self.dev_window_frame,text="Print incmatrix",command=lambda: print(graf.incidence_matrix))
        self.dev_print_euler= Button(self.dev_window_frame,text="Eulerian Test",command=self.eulerian_test)
        self.dev_print_adj_list= Button(self.dev_window_frame,text="Print adj_list",command=lambda: print(graf.adj_list))
        self.dev_print_euler_cycles= Button(self.dev_window_frame,text="Eulerian cycles/paths",command=self.printforall)
        self.dev_add_node_label=Label(self.dev_window_frame,text="ADD NODE")
        self.dev_add_node_entry_name= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_entry_cordX= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_entry_cordY= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_button_submit= Button(self.dev_window_frame,text="Submit", command=self.dev_add_node,width=4)
        self.dev_hamilton= Button(self.dev_window_frame,text="Hamilton test", command=self.hamilton_test,width=15)

        self.dev_print_grafnodes.grid(row=0,column=0)
        self.dev_print_cordsX.grid(row=1,column=0)
        self.dev_print_cordsY.grid(row=2,column=0)
        self.dev_print_edge_quantity.grid(row=3,column=0)
        self.dev_print_adjacencymatrix.grid(row=4,column=0)
        self.dev_print_incidencematrix.grid(row=5,column=0)
        self.dev_print_adj_list.grid(row=6,column=0)
        self.dev_print_euler.grid(row=7,column=0)
        self.dev_print_euler_cycles.grid(row=8,column=0)
        self.dev_add_node_label.grid(row=9,column=0)
        self.dev_add_node_entry_name.grid(row=9,column=1)
        self.dev_add_node_entry_cordX.grid(row=9,column=2)
        self.dev_add_node_entry_cordY.grid(row=9,column=3)
        self.dev_add_node_button_submit.grid(row=9,column=4)
        self.dev_hamilton.grid(row=10,column=0)


        self.dev_window.mainloop()

    def dev_add_node(self):
        if self.dev_add_node_entry_name.get() not in graf.nodes:
            graf.add_node(self.dev_add_node_entry_name.get(),self.dev_add_node_entry_cordX.get(),self.dev_add_node_entry_cordY.get())
            self.draw_nodes()
            self.draw_edges()
        else:
            messagebox.showerror("Error", "NIE")

    def save(self):
        graf.convert_to_adj_list()
        f=open("savedgraf.txt","w+")
        for index in graf.nodes:
            f.write(index)
            f.write(" ")
            for keys in graf.cordsX[index]:
                f.write(str(keys))
            f.write(" ")
            for keys in graf.cordsY[index]:
                f.write(str(keys))
            f.write("\r\n")
        f.write("\r\n")
        for index in graf.adj_list:
            for keys in graf.adj_list[index]:
                f.write(index)
                f.write(" ")
                f.write(keys)
                f.write("\r\n")
        f.close()

    def load(self):
        self.clear_canvas()
        f=open("savedgraf.txt","r")
        method="node"
        f1= f.readlines()
        for x in f1:
            if not x.strip():
                method="edge"
                continue
            if method=="node":
                data=x.split()
                i=0
                for y in data:
                    if i==0:
                        node=str(y)
                    if i==1:
                        cordx=float(y)
                    if i==2:
                        cordy=float(y)
                    i+=1
                graf.add_node(node,cordx,cordy)
            if method=="edge":
                data=x.split()
                i=0
                for y in data:
                    if i==0:
                        node1=y
                    if i==1:
                        node2=y
                    i+=1
                graf.add_edge_directed(node1,node2)
        f.close()
        self.draw_nodes()
        self.draw_edges()






if __name__ == '__main__':

    def on_closing():
    #    if messagebox.askokcancel("Quit", "Do you want to quit?"):
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
