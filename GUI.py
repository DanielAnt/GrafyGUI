from tkinter import *
from tkinter import ttk, colorchooser, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from Grafy import *
from PIL import Image, ImageTk
from math import *
import sys
import time
import random

sys.setrecursionlimit(2000)




class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.line_width=2
        self.draw_ratio=int(2)
        self.switch_variable = StringVar(value="")
        self.selected=False
        self.remove=False
        self.showcords=IntVar()
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

################# Buttons #################
        self.draw_button = Radiobutton(self.buttons, text="AddNode",variable=self.switch_variable,indicatoron=False, value="draw", height=1)
        self.draw_Entry= Entry(self.buttons,width=5,justify=RIGHT)
        self.select_button = Radiobutton(self.buttons, text="Select",variable=self.switch_variable,indicatoron=False, value="select", height=1)
        self.removeNode_button = Button(self.buttons, text="Remove Node", command=self.remove_node, height=1)
        self.unEdge_button = Radiobutton(self.buttons, text="UnEdge",variable=self.switch_variable,indicatoron=False, value="drawUndirected", height=1)
        self.edge_wage_entry= Entry(self.buttons,width=5,justify=RIGHT)
        self.directedEdge_button = Radiobutton(self.buttons, text="directedEdge",variable=self.switch_variable,indicatoron=False, value="drawDirected", height=1)
        self.buttonPrint= Button(self.buttons,text = "Print", command= self.print_graph, height=1)
        self.draw_graph_button= Button(self.buttons,width=10,text="Draw graph", command=self.draw_graph)
    #    self.var1=IntVar()
    #    self.directed_CheckButton= Checkbutton(self.controls, text="Directed",selectcolor="black", variable=self.var1)
        self.wage_var=IntVar()
        self.wage_graph = Checkbutton(self.controls, text="Draw Wages",selectcolor="black", variable=self.wage_var)

############ Buttons.pack #################
        self.draw_Entry.pack(side="left",fill=Y, expand=True)
        self.draw_button.pack(side="left",fill=Y, expand=True)
        self.removeNode_button.pack(side="left",fill=Y, expand=True)
        self.edge_wage_entry.pack(side="left",fill=Y, expand=True)
        self.unEdge_button.pack(side="left",fill=Y, expand=True)
        self.directedEdge_button.pack(side="left",fill=Y, expand=True)
        self.select_button.pack(side="left",fill=Y, expand=True)
        self.buttonPrint.pack(side="left")
        self.draw_graph_button.pack(side="left")
    #    self.directed_CheckButton.pack(side="left")
        self.wage_graph.pack(side="left")
        self.controls.pack(side=TOP,fill=X, expand=False)

############ Canvas #############################

    #    self.print=Canvas(self.master,height=400,width=300, bg=self.color_bg)
    #    self.print.pack(side=LEFT,fill=Y,expand=False)
        self.print_space=Text(self.master,width=10,bg="white",relief=SUNKEN)
        self.print_space.pack(side=LEFT,fill=Y,expand=False)

        self.c=Canvas(self.master,width=1300,height=900,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)
#        self.c.bind("<Motion>",self.moved)
#        self.tag=self.c.create_text(10,10, text="", anchor="nw")

############# Cascades ##############################

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.graphmenu= Menu(self.menu)
        self.menu.add_cascade(label='Add graph', menu=self.graphmenu)
        self.graphmenu.add_command(label='Adjacency matrix',command=self.graph_add_adj)
        self.graphmenu.add_command(label='Incidence matrix',command=self.graph_add_inc)
        self.graphmenu.add_command(label='Adjacency list',command=self.graph_add_adjlist)
        self.graphmenu.add_command(label='Type in',command=self.type_in)
        self.editmenu= Menu(self.menu)
        self.menu.add_cascade(label='Edit graph', menu=self.editmenu)
        self.editmenu.add_command(label='Edit adjacency matrix',command=self.adj_matrix_edit)
        self.editmenu.add_command(label='Edit incidence matrix',command=self.inc_matrix_edit)
        self.testmenu= Menu(self.menu)
        self.menu.add_cascade(label='Functions', menu=self.testmenu)
        self.testmenu.add_command(label='Display paths',command=self.graph_tests)
        self.testmenu.add_command(label='Print output',command=self.graph_prints_display)
        self.coloring_graph = Menu(self.menu)
        self.menu.add_cascade(label='Coloring Graph', menu=self.coloring_graph)
        self.coloring_graph.add_command(label='By adjacency matrix',command=lambda: self.coloring("adj_mat"))
        self.coloring_graph.add_command(label='By node deg',command=lambda: self.coloring("node_deg"))
        self.coloring_graph.add_command(label='By random',command=lambda: self.coloring("node_random"))
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label='Options',menu=self.optionmenu)
        self.optionmenu.add_command(label='Clear',command=lambda: self.clear_canvas(self.c))
        self.optionmenu.add_command(label='Exit',command=self.master.destroy)
        self.devmenu = Menu(self.menu)
        self.menu.add_cascade(label='DEVTOOLS',menu=self.devmenu)
        self.devmenu.add_command(label='Graph Data',command=self.open_dev_window)
        self.file = Menu(self.menu)
        self.menu.add_cascade(label='file',menu=self.file)
        self.file.add_command(label='Save',command=self.save)
        self.file.add_command(label='Load',command=self.load)


    #def moved(self,event):
    #    print(self.showcords.get())
    #    if self.showcords.get()==1:
    #        self.c.itemconfigure(self.print, text=(event.x,event.y))

    def remove_node(self):
        if self.selected==True:
            self.remove=True
            graf.remove_node(self.node)
        if self.remove==True:
            self.clear_canvas_without_removing_graph(self.c)
            self.draw_edges(self.c)
            self.draw_nodes(self.c)
            self.remove=False
            self.node=None
            self.selected=False
        else:
            messagebox.showerror("Error", "Select node that you want to remove") # removes selected node

    def tools(self,task):
        self.tool=task   # changes tool used with mouse1

    def graph_temp(self):
        print("lol")
###############################################
##############CLEARING CANVAS##################

    def clear_canvas(self,canvas):
        canvas.delete(ALL)
        graf.clear_graph()

    def clear_canvas_without_removing_graph(self,canvas):
        canvas.delete(ALL)

###############################################
#########Printing Methods######################

    def print_graph_adj_matrix(self):
        if len(graf.nodes)>0:
            graf.convert_to_adj_matrix()
            length=sqrt(len(graf.adjacency_matrix))
            first=True
            text=""
            for row in range(int(length)):
                if first==True:
                    text+="[ "
                    first=False
                else:
                    text+="\r\n[ "
                next=True
                for column in range(int(length)):
                    if str(row)+"-"+str(column) in graf.adjacency_matrix:
                        if next==True:
                            text+=str(graf.adjacency_matrix[str(row)+"-"+str(column)])
                            next=False
                        else:
                            text+=" , "
                            text+=str(graf.adjacency_matrix[str(row)+"-"+str(column)])
                text+=" ]"
            return text

    def print_graph_inc_matrix(self):
        if len(graf.nodes)>0:
            graf.convert_to_inc_matrix()
            number_of_nodes=len(graf.pointer)
            matrix_length=len(graf.incidence_matrix)
            number_of_columns=matrix_length/number_of_nodes
            first=True
            text=""
            for row in range(int(number_of_nodes)):
                if first==True:
                    text+="[ "
                    first=False
                else:
                    text+="\r\n[ "
                next=True
                for column in range(int(number_of_columns)):
                    if str(row)+"-"+str(column) in graf.incidence_matrix:
                        if next==True:
                            text+=str(graf.incidence_matrix[str(row)+"-"+str(column)])
                            next=False
                        else:
                            text+=" , "
                            text+=str(graf.incidence_matrix[str(row)+"-"+str(column)])
                text+=" ]"
            return text

    def print_graph_adj_list(self):
        if len(graf.nodes)>0:
            text=""
            graf.convert_to_adj_list()
            for node in graf.adj_list:
                text+=str(node)+" : ( "
                first=True
                for key in graf.adj_list[node]:
                    if first==True:
                        text+=str(key)
                        first=False
                    else:
                        text+=", "
                        text+=str(key)
                text+=" )\r\n"
            return text

###############################################
#########Display Methods######################

    def draw_nodes(self,canvas):
        for source in graf.nodes:
            canvas.create_image(graf.return_X(source),graf.return_Y(source), image=photo)
            canvas.create_text(graf.return_X(source)+15,graf.return_Y(source)-20,fill="darkblue",font="Times 14 bold", text=source)    #draw graph nodes

    def draw_edges(self,canvas):
        graf.convert_to_adj_list()
        graf.times_has_been_drawn={}
        for index in graf.edge_quantity:
            graf.times_has_been_drawn[index]=0
        for node1 in graf.adj_list:
            for node2 in graf.adj_list[node1]:
                    #canvas.create_line(graf.cordsX[node1],graf.cordsY[node1],graf.cordsX[node2],graf.cordsY[node2],width=self.line_width,fill="red",smooth=True)    #draw graph edges
                    self.create_line_arc(node1,node2,canvas)

    def print_graph(self):
        text=graf.name
        text+="\n"
        for source in graf.nodes:
            text+=str(source)
            text+=":\n"
            for keys in graf.nodes[source]:
                text+=str(keys)
                if self.wage_var.get()==1:
                    text+="-"
                    text+=str(graf.edge_wage[keys])
                text+="\n"
            text+="\n"
        self.print_into_printspace(text)

    def print_text_into_printspace(self,text_to_print):
        self.print_space.delete("1.0",END)
        self.print_space.insert(INSERT, text_to_print, ("a"))
        self.print_space.tag_config("a",foreground="black",font="times 11")

    def create_line_arc(self,node1,node2,canvas):
        if node1==node2:
            self.temp=graf.times_has_been_drawn[node1+node2]
            if self.temp%2==0:
                canvas.create_oval(graf.return_X(node1)-15-5*self.temp,graf.return_Y(node1)+15+5*self.temp,graf.return_X(node1)+1*self.temp,graf.return_Y(node1)-1*self.temp,width=2)
            else:
                canvas.create_oval(graf.return_X(node1)-15-5*(self.temp-1),graf.return_Y(node1)-15-5*(self.temp-1),graf.return_X(node1)+1*self.temp,graf.return_Y(node1)+1*self.temp,width=2)
            self.temp+=1
            graf.times_has_been_drawn[node1+node2]=self.temp
        else:
            if graf.times_has_been_drawn[node1+node2]==0 and graf.times_has_been_drawn[node1+node2]<graf.edge_quantity[node1+node2]:
                x=graf.return_X(node1)
                y=graf.return_Y(node1)
                x1=graf.return_X(node2)
                y1=graf.return_Y(node2)
                if x==x1:
                    x+=1
                if y==y1:
                    y+=1
                if self.wage_var.get()==1:
                    z=10
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
                canvas.create_line(graf.return_X(node1),graf.return_Y(node1),graf.return_X(node2),graf.return_Y(node2),width=self.line_width,fill="black",smooth=True)    #draw graph edges
                if self.wage_var.get()==1:
                    canvas.create_text(X_wynik2,Y_wynik2,fill="darkblue",font="Times 14 bold", text=graf.edge_wage[node1+node2])
                self.temp=graf.times_has_been_drawn[node1+node2]
                self.temp+=1
                graf.times_has_been_drawn[node1+node2]=self.temp
                graf.times_has_been_drawn[node2+node1]=self.temp
            else:
                if graf.times_has_been_drawn[node1+node2] < graf.edge_quantity[node1+node2]:
                    ratio = graf.edge_quantity[node1+node2]-graf.times_has_been_drawn[node1+node2]
                    if ratio<=2:
                        z=25
                    if ratio>2 and ratio<=4:
                        z=45
                    if ratio>4 and ratio<=6:
                        z=65
                    if ratio>6 and ratio<=8:
                        z=85
                    if ratio>8:
                        z=105
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
                    if self.wage_var.get()==1:
                        z=z+10
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
                        X_wage1=float((-VarB+sqrt(DELTA))/(2*VarA))
                        X_wage2=float((-VarB-sqrt(DELTA))/(2*VarA))
                        Y_wage1=a1*X_wynik1+b1
                        Y_wage2=a1*X_wynik2+b1
                    if ratio % 2 == 0:
                        canvas.create_line(graf.return_X(node1),graf.return_Y(node1),X_wynik1,Y_wynik1,graf.return_X(node2),graf.return_Y(node2),width=self.line_width,fill="black",smooth=True)    #draw graph edges
                        if self.wage_var.get()==1:
                            canvas.create_text(X_wage1,Y_wage1,fill="darkblue",font="Times 14 bold", text=graf.edge_wage[node1+node2])
                    else:
                        canvas.create_line(graf.return_X(node1),graf.return_Y(node1),X_wynik2,Y_wynik2,graf.return_X(node2),graf.return_Y(node2),width=self.line_width,fill="black",smooth=True)    #draw graph edges
                        if self.wage_var.get()==1:
                            canvas.create_text(X_wage2,Y_wage2,fill="darkblue",font="Times 14 bold", text=graf.edge_wage[node1+node2])


                    self.temp=graf.times_has_been_drawn[node1+node2]
                    self.temp+=1
                    graf.times_has_been_drawn[node1+node2]=self.temp
                    graf.times_has_been_drawn[node2+node1]=self.temp

    def draw_graph(self):
        self.clear_canvas_without_removing_graph(self.c)
        self.draw_edges(self.c)
        self.draw_nodes(self.c)

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
            if e.x>self.old_x-10 and e.x<self.old_x+10 and e.y>self.old_y-10 and e.y<self.old_y+10:
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
                            self.draw_graph()
                    else:
                        messagebox.showerror("Error", "You can't add more then one node with the same name")

        if self.tool=="drawUndirected":
            self.new_x=e.x
            self.new_y=e.y
            start_node=None
            end_node=None
            for source in graf.cordsX:
                if list(graf.cordsX[source])[0]>self.old_x-10 and list(graf.cordsX[source])[0]<self.old_x+10 and list(graf.cordsY[source])[0]>self.old_y-10 and list(graf.cordsY[source])[0]<self.old_y+10:
                    start_node=source
                if list(graf.cordsX[source])[0]>self.new_x-10 and list(graf.cordsX[source])[0]<self.new_x+10 and list(graf.cordsY[source])[0]>self.new_y-10 and list(graf.cordsY[source])[0]<self.new_y+10:
                    end_node=source
            if start_node!=None and end_node!=None:
                if self.edge_wage_entry.get() and self.edge_wage_entry.get().isnumeric():
                    if self.edge_wage_entry.get().isnumeric:
                        graf.add_edge_undirected(start_node,end_node,self.edge_wage_entry.get())
                        self.draw_graph()
                    else:
                        messagebox.showerror("Error", "Edge wage must be numeric")
                else:
                    graf.add_edge_undirected(start_node,end_node)
                    self.draw_graph()


        if self.tool=="drawDirected":
            self.new_x=e.x
            self.new_y=e.y
            start_node=None
            end_node=None
            for source in graf.cordsX:
                if list(graf.cordsX[source])[0]>self.old_x-10 and list(graf.cordsX[source])[0]<self.old_x+10 and list(graf.cordsY[source])[0]>self.old_y-10 and list(graf.cordsY[source])[0]<self.old_y+10:
                    start_node=source
                if list(graf.cordsX[source])[0]>self.new_x-10 and list(graf.cordsX[source])[0]<self.new_x+10 and list(graf.cordsY[source])[0]>self.new_y-10 and list(graf.cordsY[source])[0]<self.new_y+10:
                    end_node=source
            if start_node!=None and end_node!=None:
                graf.add_edge_directed(start_node,end_node)
                self.draw_graph()


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
        self.graph_add_window = Toplevel()
        self.graph_add_window.grab_set()
        self.graph_add_window.attributes("-topmost",True)
        self.graph_add_window.title('Adajacency matrix')
        self.graph_add_window.resizable(False,False)
        self.frame_one=Frame(self.graph_add_window,width=100,height=500,borderwidth=2,relief='sunken')
        self.frame_one.pack(side="left",fill=BOTH, expand=False)
        self.nodeQuantity_Label=Label(self.frame_one,font="Times 10 italic bold",text='How many Nodes?')
        self.nodeQuantity_Entry= Entry(self.frame_one,width=15,justify=RIGHT)
        self.nodeQuantity_Button= Button(self.frame_one,width=15,text="Submit",command=self.NodeQuantity_Submit)
        self.nodeQuantity_Label.pack(side=TOP)
        self.nodeQuantity_Entry.pack(side=TOP)
        self.nodeQuantity_Button.pack(side=TOP)

    def NodeQuantity_Submit(self):
        if self.nodeQuantity_Entry.get().isnumeric():
            self.temp_NodeQuantity=int(self.nodeQuantity_Entry.get())
            self.matrix_window= Toplevel()
            self.matrix_window.grab_set()
            self.matrix_window.resizable(False,False)
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
                for column in range(self.temp_NodeQuantity):
                    index=str(row)+str(column)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    matrix_entry.insert(END,"0")
                    matrix_entry.grid(row=row,column=column,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.matrix_adj_submit)
            self.adjacency_matrix_submit.pack(side=TOP)
        else:
            messagebox.showerror("Error", "You need to enter a number") #submits the number from graph_add_adj entry

    def matrix_adj_submit(self):
        self.clear_canvas(self.c)
        self.matrix_error=False
        length=sqrt(len(self.entry_matrix))
        for row in range(int(length)):
            for column in range(int(length)):
                if self.entry_matrix[str(row)+str(column)].get().isnumeric():
                    if self.entry_matrix[str(row)+str(column)].get()==self.entry_matrix[str(column)+str(row)].get():
                        graf.create_adj_matrix(str(row)+str(column),self.entry_matrix[str(column)+str(row)].get())
                    else:
                        self.matrix_error=True
                        break;
                else:
                    self.matrix_error=True
                    break;

        if self.matrix_error==False:
            graf.convert_adj_matrix(self.temp_NodeQuantity,self.draw_ratio)
            self.draw_graph()
            self.matrix_window.destroy() # submits entered matrix into graph and draws it
        else:
            messagebox.showerror("Error", "Wrong data in matrix")
            graf.adjacency_matrix={} #clears adj_matrix

    def adj_matrix_edit(self):
        if len(graf.nodes)>0:
            graf.convert_to_adj_matrix()
            self.temp_NodeQuantity=int(sqrt(len(graf.adjacency_matrix)))
            print("len",len(graf.adjacency_matrix))
            print("nodequantity",self.temp_NodeQuantity)
            self.matrix_window= Toplevel()
            self.matrix_window.grab_set()
            self.matrix_window.resizable(False,False)
            self.matrix_window.attributes("-topmost",True)
            self.matrix_window.title("Adjacency matrix")
            self.frame_two=Frame(self.matrix_window,relief='sunken')
            self.frame_two.pack(side="left",fill=BOTH, expand=False)
            self.matrix_label=Label(self.frame_two,font="Times 10 italic bold", text="Enter matrix values")
            self.matrix_label.pack(side=TOP)
            self.entry_matrix={}
            self.matrix_frame=Frame(self.frame_two)
            self.matrix_frame.pack(side=TOP)
            matrix_label=Label(self.matrix_frame,text="~")
            matrix_label.grid(row=0,column=0,stick="nsew")
            for row in range(self.temp_NodeQuantity):
                for column in range(self.temp_NodeQuantity):
                    index=str(row)+"-"+str(column)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    if row==0 and column==0:
                        matrix_label_X=Label(self.matrix_frame,text=graf.reversedpointer[str(column)])
                        matrix_label_Y=Label(self.matrix_frame,text=graf.reversedpointer[str(row)])
                        matrix_label_X.grid(row=row,column=column+1,stick="nsew")
                        matrix_label_Y.grid(row=row+1,column=column,stick="nsew")
                        matrix_entry.insert(END,graf.adjacency_matrix[str(row)+"-"+str(column)])
                        matrix_entry.grid(row=row+1,column=column+1,stick="nsew")
                    elif row==0 and column!=0:
                        matrix_label_X=Label(self.matrix_frame,text=graf.reversedpointer[str(column)])
                        matrix_label_X.grid(row=row,column=column+1,stick="nsew")
                        matrix_entry.insert(END,graf.adjacency_matrix[str(row)+"-"+str(column)])
                        matrix_entry.grid(row=row+1,column=column+1,stick="nsew")
                    elif column==0 and row!=0:
                        matrix_label_Y=Label(self.matrix_frame,text=graf.reversedpointer[str(row)])
                        matrix_label_Y.grid(row=row+1,column=column,stick="nsew")
                        matrix_entry.insert(END,graf.adjacency_matrix[str(row)+"-"+str(column)])
                        matrix_entry.grid(row=row+1,column=column+1,stick="nsew")
                    else:
                        matrix_entry.insert(END,graf.adjacency_matrix[str(row)+"-"+str(column)])
                        matrix_entry.grid(row=row+1,column=column+1,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.adj_matrix_edit_submit)
            self.adjacency_matrix_submit.pack(side=TOP)
        else:
            messagebox.showerror("Error", "Graph is empty")

    def adj_matrix_edit_submit(self):
        self.matrix_error=False
        length=sqrt(len(self.entry_matrix))

        for row in range(int(length)):
            for column in range(int(length)):
                if self.entry_matrix[str(row)+"-"+str(column)].get().isnumeric():
                    if self.entry_matrix[str(row)+"-"+str(column)].get()==self.entry_matrix[str(column)+"-"+str(row)].get():
                        graf.create_adj_matrix(str(row)+"-"+str(column),self.entry_matrix[str(row)+"-"+str(column)].get())
                    else:
                        self.matrix_error=True
                        break;
                else:
                    self.matrix_error=True
                    break;

        if self.matrix_error==False:
            for node in graf.nodes:
                for node1 in graf.nodes:
                    if node+node1 in graf.edge_quantity:
                        for i in range(graf.edge_quantity[node+node1]):
                            graf.remove_edge(node,node1)
            graf.convert_adj_matrix_edit()
            self.draw_graph()
            self.matrix_window.destroy()
        else:
            messagebox.showerror("Error", "Graph is empty")


###############################################

###############################################
#######ADDING GRAPH BY INCIDENCE MATRIX #######

    def graph_add_inc(self):
        self.graph_add_window = Toplevel()
        self.graph_add_window.grab_set()
        self.graph_add_window.attributes("-topmost",True)
        self.graph_add_window.title('Incidence matrix')
        self.graph_add_window.resizable(False,False)
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

    def Quantity_Submit(self):
        if self.nodeQuantity_Entry.get().isnumeric() and self.edgeQuantity_Entry.get().isnumeric():
            self.temp_NodeQuantity=int(self.nodeQuantity_Entry.get())
            self.temp_EdgeQuantity=int(self.edgeQuantity_Entry.get())
            self.matrix_window= Toplevel()
            self.matrix_window.grab_set()
            self.matrix_window.attributes("-topmost",True)
            self.matrix_window.title("Incidence matrix")
            self.matrix_window.resizable(False,False)
            self.graph_add_window.destroy()
            self.frame_two=Frame(self.matrix_window,relief='sunken')
            self.frame_two.pack(side="left",fill=BOTH, expand=False)
            self.matrix_label=Label(self.frame_two,font="Times 10 italic bold", text="Enter matrix values")
            self.matrix_label.pack(side=TOP)
            self.entry_matrix={}
            self.matrix_frame=Frame(self.frame_two)
            self.matrix_frame.pack(side=TOP)
            for row in range(self.temp_NodeQuantity):
                for column in range(self.temp_EdgeQuantity):
                    index=str(row)+str(column)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    matrix_entry.insert(END,"0")
                    matrix_entry.grid(row=row,column=column,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.matrix_inc_submit)
            self.adjacency_matrix_submit.pack(side=TOP)

    def matrix_inc_submit(self):
        self.clear_canvas(self.c)
        self.matrix_error=False
        for column in range(self.temp_EdgeQuantity):
            i=0
            for row in range(self.temp_NodeQuantity):
                i+=int(self.entry_matrix[str(row)+str(column)].get())
                if self.entry_matrix[str(row)+str(column)].get().isnumeric():
                    if int(self.entry_matrix[str(row)+str(column)].get())==1 or int(self.entry_matrix[str(row)+str(column)].get())==0 or int(self.entry_matrix[str(row)+str(column)].get())==2:
                        graf.create_inc_matrix(str(row)+str(column),self.entry_matrix[str(row)+str(column)].get())
                    else:
                        self.matrix_error=True
                        break;
                else:
                    self.matrix_error=True
                    break;
            if i!=2 and i!=0:
                self.matrix_error=True
                break
        if self.matrix_error==False:
            graf.convert_inc_matrix(self.temp_NodeQuantity,self.temp_EdgeQuantity,self.draw_ratio)
            self.draw_graph()
            self.matrix_window.destroy() # submits entered matrix into graph and draws it
        else:
            graf.incidence_matrix={} #submits matrix
            messagebox.showerror("Error", "Wrong data")

    def inc_matrix_edit(self):
        if len(graf.nodes)>0:
            graf.convert_to_inc_matrix()
            self.temp_NodeQuantity=int(len(graf.pointer))
            matrix_length=len(graf.incidence_matrix)
            self.temp_EdgeQuantity=int(matrix_length/self.temp_NodeQuantity)

            self.matrix_window= Toplevel()
            self.matrix_window.grab_set()
            self.matrix_window.attributes("-topmost",True)
            self.matrix_window.title("Incidence matrix")
            self.matrix_window.resizable(False,False)

            self.frame_two=Frame(self.matrix_window,relief='sunken')
            self.frame_two.pack(side="left",fill=BOTH, expand=False)
            self.matrix_label=Label(self.frame_two,font="Times 10 italic bold", text="Enter matrix values")
            self.matrix_label.pack(side=TOP)
            self.entry_matrix={}
            self.matrix_frame=Frame(self.frame_two)
            self.matrix_frame.pack(side=TOP)

            for row in range(int(self.temp_NodeQuantity)):
                for column in range(int(self.temp_EdgeQuantity)):
                    index=str(row)+"-"+str(column)
                    matrix_entry= Entry(self.matrix_frame,width=3)
                    matrix_entry.insert(END,graf.incidence_matrix[str(row)+"-"+str(column)])
                    if column==0:
                        matrix_label=Label(self.matrix_frame,text=graf.reversedpointer[str(row)])
                        matrix_label.grid(row=row,column=column,stick="nsew")
                        matrix_entry.grid(row=row,column=column+1,stick="nsew")
                    else:
                        matrix_entry.grid(row=row,column=column+1,stick="nsew")
                    self.entry_matrix[index]=matrix_entry
            self.adjacency_matrix_submit= Button(self.frame_two, width=15,text="Submit",command=self.inc_matrix_edit_submit)
            self.adjacency_matrix_submit.pack(side=TOP)

    def inc_matrix_edit_submit(self):
        self.matrix_error=False
        for column in range(int(self.temp_EdgeQuantity)):
            i=0
            for row in range(int(self.temp_NodeQuantity)):
                i+=int(self.entry_matrix[str(row)+"-"+str(column)].get())
                if self.entry_matrix[str(row)+"-"+str(column)].get().isnumeric():
                    if int(self.entry_matrix[str(row)+"-"+str(column)].get())==1 or int(self.entry_matrix[str(row)+"-"+str(column)].get())==0 or int(self.entry_matrix[str(row)+"-"+str(column)].get())==2:
                        graf.create_inc_matrix(str(row)+str(column),self.entry_matrix[str(row)+"-"+str(column)].get())
                    else:
                        self.matrix_error=True
                        break;
                else:
                    self.matrix_error=True
                    break;
            if i!=2 and i!=0:
                self.matrix_error=True
                break

        if self.matrix_error==False:
            for node in graf.nodes:
                for node1 in graf.nodes:
                    if node+node1 in graf.edge_quantity:
                        for i in range(graf.edge_quantity[node+node1]):
                            graf.remove_edge(node,node1)
            graf.convert_inc_matrix_edit(self.temp_NodeQuantity,self.temp_EdgeQuantity)
            self.draw_graph()
            self.matrix_window.destroy() # submits entered matrix into graph and draws it
        else:
            graf.incidence_matrix={} #submits matrix
            messagebox.showerror("Error", "Wrong data")

###############################################

###############################################
#######ADDING GRAPH BY ADJACENCY LIST#########

    def graph_add_adjlist(self):
        #window
        self.graph_adj_list = Toplevel()
        self.graph_adj_list.grab_set()
        self.graph_adj_list.geometry("285x280")
        self.graph_adj_list.resizable(False,False)
        self.graph_adj_list.attributes("-topmost",True)
        self.graph_adj_list.title('Adajacency list')

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
        self.clear_canvas(self.c)
        nodequantity=len(self.adj_list_nodes)
        radius=150*self.draw_ratio if nodequantity > 5 else 100*self.draw_ratio # adjust radius of circle that the graph is drawn on depending on nodequantity
        i=0
        for index in self.adj_list_nodes:
            graf.add_node(index,round(sin(2*pi/nodequantity*i)*radius+(225+(self.draw_ratio-1)*50)),round(cos(2*pi/nodequantity*i)*radius+(225+(self.draw_ratio-1)*50)))
            i+=1
        for index in self.adj_list_nodes:
            for index1 in self.adj_list_nodes:
                for keys in self.adj_list_nodes[index]:
                    if index+index1==keys:
                        graf.add_edge_directed(index,index1)
        self.draw_graph()
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
###############################################

###############################################
############### Type in #######################

    def type_in(self):
        self.type_in_window= Toplevel()
        self.type_in_window.grab_set()
        self.type_in_window.attributes("-topmost",True)
        self.type_in_window.title('Type in functions')
        self.type_in_window.resizable(False,False)
        self.type_in_frame= Frame(self.type_in_window)
        self.type_in_frame.pack(fill=BOTH, expand=False)

        ##### ADD NODE ##########
        self.type_in_add_node_label=Label(self.type_in_frame,text="ADD NODE")
        self.type_in_add_node_label_node=Label(self.type_in_frame,text="Node")
        self.type_in_add_node_label_cordX=Label(self.type_in_frame,text="Cord X")
        self.type_in_add_node_label_cordY=Label(self.type_in_frame,text="Cord Y")
        self.type_in_add_node_entry_name= Entry(self.type_in_frame,width=8)
        self.type_in_add_node_entry_cordX= Entry(self.type_in_frame,width=8)
        self.type_in_add_node_entry_cordY= Entry(self.type_in_frame,width=8)
        self.type_in_add_node_button_submit= Button(self.type_in_frame,text="Submit", command=self.type_in_add_node,width=4)

        ##### ADD EDGE ##########
        self.type_in_add_edge_label=Label(self.type_in_frame,text="ADD EDGE")
        self.type_in_add_edge_label_node1=Label(self.type_in_frame,text="Node")
        self.type_in_add_edge_label_node2=Label(self.type_in_frame,text="Node")
        self.type_in_add_edge_label_wage=Label(self.type_in_frame,text="Wage")
        self.type_in_add_edge_entry_node1= Entry(self.type_in_frame,width=8)
        self.type_in_add_edge_entry_node2= Entry(self.type_in_frame,width=8)
        self.type_in_add_edge_entry_wage= Entry(self.type_in_frame,width=8)
        self.type_in_add_edge_button_submit= Button(self.type_in_frame,text="Submit", command=self.type_in_add_edge,width=4)

        ### REMOVE NODE ########
        self.type_in_remove_node_label=Label(self.type_in_frame,text="REMOVE NODE")
        self.type_in_remove_node_label_node=Label(self.type_in_frame,text="Node")
        self.type_in_remove_node_entry= Entry(self.type_in_frame,width=8)
        self.type_in_remove_node_button_submit= Button(self.type_in_frame,text="Submit", command=self.type_in_remove_node,width=4)

        #### REMOVE EDGE ########
        self.type_in_remove_edge_label=Label(self.type_in_frame,text="REMOVE EDGE")
        self.type_in_remove_edge_label.node1=Label(self.type_in_frame,text="Node")
        self.type_in_remove_edge_label.node2=Label(self.type_in_frame,text="Node")
        self.type_in_remove_edge_entry_node1= Entry(self.type_in_frame,width=8)
        self.type_in_remove_edge_entry_node2= Entry(self.type_in_frame,width=8)
        self.type_in_remove_edge_button_submit= Button(self.type_in_frame,text="Submit", command=self.type_in_remove_edge,width=4)

        ### CHANGE WAGE #######
        self.type_in_change_wage_label=Label(self.type_in_frame,text="CHANGE WAGE")
        self.type_in_change_wage_label_node1=Label(self.type_in_frame,text="Node")
        self.type_in_change_wage_label_node2=Label(self.type_in_frame,text="Node")
        self.type_in_change_wage_label_wage=Label(self.type_in_frame,text="Wage")
        self.type_in_change_wage_entry_node1= Entry(self.type_in_frame,width=8)
        self.type_in_change_wage_entry_node2= Entry(self.type_in_frame,width=8)
        self.type_in_change_wage_entry_wage= Entry(self.type_in_frame,width=8)
        self.type_in_change_wage_button_submit= Button(self.type_in_frame,text="Submit", command=self.type_in_change_wage,width=4)

        n=0
        ##### ADD NODE GRID ##########
        self.type_in_add_node_label.grid(row=n+1 ,column=0 )
        self.type_in_add_node_label_node.grid(row=n ,column=1 )
        self.type_in_add_node_label_cordX.grid(row=n ,column=2 )
        self.type_in_add_node_label_cordY.grid(row=n ,column=3 )
        self.type_in_add_node_entry_name.grid(row=n+1 ,column=1 )
        self.type_in_add_node_entry_cordX.grid(row=n+1 ,column=2 )
        self.type_in_add_node_entry_cordY.grid(row=n+1 ,column=3 )
        self.type_in_add_node_button_submit.grid(row=n+1 ,column=4 )

        n+=2

        ##### ADD EDGE GRID ##########
        self.type_in_add_edge_label.grid(row=n+1 ,column=0 )
        self.type_in_add_edge_label_node1.grid(row=n ,column=1 )
        self.type_in_add_edge_label_node2.grid(row=n ,column=2 )
        self.type_in_add_edge_label_wage.grid(row=n ,column=3 )
        self.type_in_add_edge_entry_node1.grid(row=n+1 ,column=1 )
        self.type_in_add_edge_entry_node2.grid(row=n+1 ,column=2 )
        self.type_in_add_edge_entry_wage.grid(row=n+1 ,column=3 )
        self.type_in_add_edge_button_submit.grid(row=n+1 ,column=4 )

        n+=2

        ##### REMOVE NODE #############
        self.type_in_remove_node_label.grid(row=n+1 , column=0 )
        self.type_in_remove_node_label_node.grid(row=n , column=1 )
        self.type_in_remove_node_entry.grid(row=n+1 , column=1 )
        self.type_in_remove_node_button_submit.grid(row=n+1 , column=4 )
        n+=2

        ##### REMOVE EDGE GRID ##########
        self.type_in_remove_edge_label.grid(row=n+1 , column=0 )
        self.type_in_remove_edge_label.node1.grid(row=n , column=1 )
        self.type_in_remove_edge_label.node2.grid(row=n, column=2 )
        self.type_in_remove_edge_entry_node1.grid(row=n+1 , column=1 )
        self.type_in_remove_edge_entry_node2.grid(row=n+1 , column=2 )
        self.type_in_remove_edge_button_submit.grid(row=n+1 , column=4 )
        n+=2

        ##### CHANGE WAGE GRID ##########
        self.type_in_change_wage_label.grid(row=n+1 , column=0 )
        self.type_in_change_wage_label_node1.grid(row=n , column=1 )
        self.type_in_change_wage_label_node2.grid(row=n , column=2 )
        self.type_in_change_wage_label_wage.grid(row=n , column=3 )
        self.type_in_change_wage_entry_node1.grid(row=n+1 , column=1 )
        self.type_in_change_wage_entry_node2.grid(row=n+1 , column=2 )
        self.type_in_change_wage_entry_wage.grid(row=n+1 , column=3 )
        self.type_in_change_wage_button_submit.grid(row=n+1 , column=4 )

        self.type_in_window.mainloop()

    def type_in_add_node(self):
        if self.type_in_add_node_entry_name.get() not in graf.nodes and self.type_in_add_node_entry_cordX.get() and self.type_in_add_node_entry_cordY.get():
            graf.add_node(self.type_in_add_node_entry_name.get(),self.type_in_add_node_entry_cordX.get(),self.type_in_add_node_entry_cordY.get())
            self.draw_graph()
        else:
            messagebox.showerror("Error", "Wrong data")

    def type_in_add_edge(self):
        if self.type_in_add_edge_entry_node1.get() in graf.nodes and self.type_in_add_edge_entry_node2.get() in graf.nodes:
            if self.type_in_add_edge_entry_wage.get():
                if self.type_in_add_edge_entry_wage.get().isnumeric():
                    graf.add_edge_undirected(self.type_in_add_edge_entry_node1.get(),self.type_in_add_edge_entry_node2.get(),self.type_in_add_edge_entry_wage.get())
                    self.draw_graph()
                else:
                    messagebox.showerror("Error", "Wage must be a number")
            else:
                graf.add_edge_undirected(self.type_in_add_edge_entry_node1.get(),self.type_in_add_edge_entry_node2.get())
                self.draw_graph()
        else:
            messagebox.showerror("Error", "There are no such a nodes")

    def type_in_remove_node(self):
        if self.type_in_remove_node_entry.get() in graf.nodes:
            graf.remove_node(self.type_in_remove_node_entry.get())
            self.draw_graph()
        else:
            messagebox.showerror("Error", "There is no such a node")

    def type_in_remove_edge(self):
        if self.type_in_remove_edge_entry_node1.get() and self.type_in_remove_edge_entry_node2.get() and self.type_in_remove_edge_entry_node2.get()+self.type_in_remove_edge_entry_node1.get() in graf.edge_quantity:
            graf.remove_edge(self.type_in_remove_edge_entry_node1.get(),self.type_in_remove_edge_entry_node2.get())
            self.draw_graph()
        else:
            messagebox.showerror("Error", "There is no such an edge")

    def type_in_change_wage(self):
        if self.type_in_change_wage_entry_wage.get() and self.type_in_change_wage_entry_node1.get() and self.type_in_change_wage_entry_node2.get():
            if self.type_in_change_wage_entry_wage.get().isnumeric() and self.type_in_change_wage_entry_node1.get()+self.type_in_change_wage_entry_node2.get() in graf.edge_wage:
                graf.change_wage(self.type_in_change_wage_entry_node1.get(),self.type_in_change_wage_entry_node2.get(),self.type_in_change_wage_entry_wage.get())
                self.draw_graph()
            else:
                messagebox.showerror("Error", "There is no such an edge or wage is not a number")
        else:
            messagebox.showerror("Error", "Entrys are empty")


###############################################

#############################################
############# FUNCTIONS TESTS ###############

    def graph_tests(self):
        self.graph_tests_window= Toplevel()
        self.graph_tests_window.grab_set()
    #    self.graph_tests_window.resizable(False,False)
        self.graph_tests_window.attributes("-topmost", 1)
        self.graph_tests_window.title('Tests')
        self.graph_tests_window_buttonwidth=17

        ######### Frames ##################
        self.graph_tests_buttons_frame=Frame(self.graph_tests_window)
        self.graph_tests_canvas_frame=Frame(self.graph_tests_window)
        self.graph_tests_buttons_frame.pack(side="left",fill=BOTH, expand=False)
        self.graph_tests_canvas_frame.pack(side="left",fill=BOTH, expand=True)

        ####### Buttons ##################
        self.graph_tests_find_eulerian_cycle=Button(self.graph_tests_buttons_frame,justify=CENTER,wraplength=150, text="Search for eulerian cycle/path",width=self.graph_tests_window_buttonwidth,command=self.graph_tests_eulerian)
        self.graph_tests_hamilton_button=Button(self.graph_tests_buttons_frame,text="Hamiltons test",width=self.graph_tests_window_buttonwidth,command=self.graph_tests_hamilton)
    #    self.graph_tests_BFS_entry=Entry(self.graph_tests_buttons_frame,justify="center")
    #    self.graph_tests_BFS_button=Button(self.graph_tests_buttons_frame,text="BFS",width=self.graph_tests_window_buttonwidth,command=self.graph_test_BFS)
    #    self.graph_tests_DFS_entry=Entry(self.graph_tests_buttons_frame,justify="center")
    #    self.graph_tests_DFS_button=Button(self.graph_tests_buttons_frame,text="BFS",width=self.graph_tests_window_buttonwidth)

        n=0

        self.graph_tests_find_eulerian_cycle.grid(row=n,column=0)

        n+=1

        self.graph_tests_hamilton_button.grid(row=n,column=0,)

    #    n+=1

    #    self.graph_tests_BFS_entry.grid(row=n,column=0)

    #    n+=1

    #    self.graph_tests_BFS_button.grid(row=n,column=0)

    #    n+=1

    #    self.graph_tests_DFS_entry.grid(row=n,column=0)

    #    n+=1

    #    self.graph_tests_DFS_button.grid(row=n,column=0)

        ######## Canvas ##################
        self.graph_tests_canvas=Canvas(self.graph_tests_canvas_frame,width=600,height=500, bg="white")
        self.graph_tests_canvas.pack(fill=BOTH,expand=True)
        self.graph_tests_text=Text(self.graph_tests_canvas_frame,height=1)
        self.graph_tests_text.pack(side=BOTTOM)

    def graph_tests_eulerian(self):
        if len(graf.nodes)>0:
            self.graph_tests_canvas.delete(ALL)
            test=self.eulerian_test()
            if test==0:
                displayed_text="Graph isn't eulerian"
            if test==1:
                displayed_text="Graph has eulerian cycle"
            if test==2:
                displayed_text="Graph has eulerian path"
            self.graph_tests_text.delete("1.0",END)
            self.graph_tests_text.insert(INSERT, displayed_text)
            if test>0:
                self.draw_nodes(self.graph_tests_canvas)
                self.graph_tests_canvas.update()
                time.sleep(2)
                text=self.printforall("novariable","draw")
                text=text.splitlines()
                self.graph_tests_prepare_for_drawing()
                first=True
                for line in text:
                    if first==True:
                        first=False
                        continue
                    else:
                        nodes=line.split()
                        i=0
                        for node in nodes:
                            if i==0:
                                node1=str(node)
                                displayed_text+=" "+node1+"->"
                            if i==1:
                                node2=str(node)
                                displayed_text+=node2
                            i+=1
                        self.graph_tests_create_line(node1,node2,self.graph_tests_canvas)
                        self.graph_tests_text.delete("1.0",END)
                        self.graph_tests_text.insert(INSERT, displayed_text)
                        self.graph_tests_canvas.update()
                        time.sleep(2)

        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_tests_hamilton(self):
        if len(graf.nodes)>0:
            self.graph_tests_canvas.delete(ALL)
            self.draw_nodes(self.graph_tests_canvas)
            self.graph_tests_canvas.update()
            time.sleep(2)
            text=self.hamilton_test()
            self.graph_tests_prepare_for_drawing()
            first=True
            text=text.splitlines()
            for line in text:
                if first==True:
                    displayed_text=line+" "
                    self.graph_tests_text.delete("1.0",END)
                    self.graph_tests_text.insert(INSERT, displayed_text)
                    first=False
                    continue
                else:
                    nodes=line.split()
                    first=True
                    for node in nodes:
                        displayed_text+=node+" "
                        if first==True:
                            start_node=str(node)
                            first=False
                        elif first!=True and node in graf.nodes:
                            self.graph_tests_create_line(start_node,node,self.graph_tests_canvas)
                            self.graph_tests_text.delete("1.0",END)
                            self.graph_tests_text.insert(INSERT, displayed_text)
                            self.graph_tests_canvas.update()
                            time.sleep(2)
                            start_node=node
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_test_BFS(self):
        self.graph_tests_print_text(self.BFS())

    def graph_tests_prepare_for_drawing(self):
        graf.convert_to_adj_list()
        graf.times_has_been_drawn={}
        for index in graf.edge_quantity:
            graf.times_has_been_drawn[index]=0

    def graph_tests_create_line(self,node1,node2,canvas,ratio=1):
        node_x=graf.return_X(node1)
        node_y=graf.return_Y(node1)
        node2_x=graf.return_X(node2)
        node2_y=graf.return_Y(node2)
        if node1==node2:
            self.temp=graf.times_has_been_drawn[node1+node2]
            if self.temp%2==0:
                canvas.create_oval(node_x-15-5*self.temp,node_y+15+5*self.temp,node_x+1*self.temp,node_y-1*self.temp,width=2)
            else:
                canvas.create_oval(node_x-15-5*(self.temp-1),node_y-15-5*(self.temp-1),node_x+1*self.temp,node_y+1*self.temp,width=2)
            self.temp+=1
            graf.times_has_been_drawn[node1+node2]=self.temp
        else:
            if graf.times_has_been_drawn[node1+node2]==0 and graf.times_has_been_drawn[node1+node2]<graf.edge_quantity[node1+node2]:
                z=10
                x=node_x
                y=node_y
                x1=node2_x
                y1=node2_y
                if x==x1:
                    x+=1
                if y==y1:
                    y+=1
                if self.wage_var.get()==1:
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
                canvas.create_line(node_x,node_y,node2_x,node2_y,width=self.line_width, arrow=LAST,fill="black",smooth=True)    #draw graph edges
                if self.wage_var.get()==1:
                    canvas.create_text(X_wynik2,Y_wynik2,fill="darkblue",font="Times 12 bold", text=graf.edge_wage[node1+node2])
                self.temp=graf.times_has_been_drawn[node1+node2]
                self.temp+=1
                graf.times_has_been_drawn[node1+node2]=self.temp
                graf.times_has_been_drawn[node2+node1]=self.temp
            else:
                if graf.times_has_been_drawn[node1+node2] < graf.edge_quantity[node1+node2]:
                    ratio = graf.edge_quantity[node1+node2]-graf.times_has_been_drawn[node1+node2]
                    if ratio<=2:
                        z=20
                    if ratio>2 and ratio<=4:
                        z=35
                    if ratio>4 and ratio<=6:
                        z=50
                    if ratio>6 and ratio<=8:
                        z=70
                    if ratio>8:
                        z=90
                    x=node_x
                    y=node_y
                    x1=node2_x
                    y1=node2_y
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
                    if self.wage_var.get()==1:
                        z=z+10
                        x=node_x
                        y=node_y
                        x1=node2_x
                        y1=node2_y
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
                        X_wage1=float((-VarB+sqrt(DELTA))/(2*VarA))
                        X_wage2=float((-VarB-sqrt(DELTA))/(2*VarA))
                        Y_wage1=a1*X_wynik1+b1
                        Y_wage2=a1*X_wynik2+b1
                    if ratio % 2 == 0:
                        canvas.create_line(node_x,node_y,X_wynik1,Y_wynik1,node2_x,node2_y,width=self.line_width, arrow=LAST,fill="black",smooth=True)    #draw graph edges
                        if self.wage_var.get()==1:
                            canvas.create_text(X_wage1,Y_wage1,fill="darkblue",font="Times 12 bold", text=graf.edge_wage[node1+node2])
                    else:
                        canvas.create_line(node_x,node_y,X_wynik2,Y_wynik2,node2_x,node2_y,width=self.line_width, arrow=LAST,fill="black",smooth=True)    #draw graph edges
                        if self.wage_var.get()==1:
                            canvas.create_text(X_wage2,Y_wage2,fill="darkblue",font="Times 12 bold", text=graf.edge_wage[node1+node2])


                    self.temp=graf.times_has_been_drawn[node1+node2]
                    self.temp+=1
                    graf.times_has_been_drawn[node1+node2]=self.temp
                    graf.times_has_been_drawn[node2+node1]=self.temp


###############################################

#############################################
############# FUNCTIONS PRINTS ##############

    def graph_prints_display(self):
        self.graph_prints_display_window= Toplevel()
        self.graph_prints_display_window.grab_set()
        self.graph_prints_display_window.resizable(True,True)
        self.graph_prints_display_window.attributes("-topmost", 1)
        self.graph_prints_display_window.title('Tests')
        self.graph_prints_display_window_buttonwidth=17

        ######### Frames ##################
        self.graph_prints_display_buttons_frame=Frame(self.graph_prints_display_window)
        self.graph_prints_display_text_frame=Frame(self.graph_prints_display_window)
        self.graph_prints_display_buttons_frame.pack(side="left",fill=BOTH, expand=False)
        self.graph_prints_display_text_frame.pack(side="left",fill=BOTH, expand=True)

        ####### Buttons ##################
        self.graph_prints_display_adjacency_button=Button(self.graph_prints_display_buttons_frame, text="Print adjacency matrix",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_adjacency)
        self.graph_prints_display_graph_prints_display_clear=Button(self.graph_prints_display_buttons_frame,justify=CENTER,wraplength=150, text="Clear",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_clear)
        self.graph_prints_display_incidency_button=Button(self.graph_prints_display_buttons_frame,text="Print incidence matrix",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_incidence)
        self.graph_prints_display_adj_list_button=Button(self.graph_prints_display_buttons_frame,text="Print adjacency list",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_adj_list)
        self.graph_prints_display_is_eulerian=Button(self.graph_prints_display_buttons_frame, text="Eulerian Test",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_is_eulerian_function)
        self.graph_prints_display_find_eulerian_cycle_entry=Entry(self.graph_prints_display_buttons_frame,justify="center")
        self.graph_prints_display_find_eulerian_cycle=Button(self.graph_prints_display_buttons_frame,justify=CENTER,wraplength=150, text="Search for eulerian cycle/path",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_eulerian)
        self.graph_prints_display_hamilton_button=Button(self.graph_prints_display_buttons_frame,text="Hamiltons test",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_hamilton)
        self.graph_prints_display_BFS_entry=Entry(self.graph_prints_display_buttons_frame,justify="center")
        self.graph_prints_display_BFS_button=Button(self.graph_prints_display_buttons_frame,text="BFS",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_BFS)
        self.graph_prints_display_DFS_entry=Entry(self.graph_prints_display_buttons_frame,justify="center")
        self.graph_prints_display_DFS_button=Button(self.graph_prints_display_buttons_frame,text="DFS",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_DFS)
        self.graph_prints_display_critcal_edge=Button(self.graph_prints_display_buttons_frame,text="Critical edge",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_critcal_edge_test)
        self.graph_prints_display_SPW_entry_one=Entry(self.graph_prints_display_buttons_frame,justify="center")
        self.graph_prints_display_SPW_entry_two=Entry(self.graph_prints_display_buttons_frame,justify="center")
        self.graph_prints_display_SPW_button=Button(self.graph_prints_display_buttons_frame,text="Shortest Path",width=self.graph_prints_display_window_buttonwidth,command=self.graph_prints_display_SPW)


        ###### TEXT ######
        self.text_window=Text(self.graph_prints_display_text_frame,bg="white",width=80)
        self.text_window.pack(fill=BOTH, expand=True)

        ######################## GRID ############################
        n=0

        self.graph_prints_display_adjacency_button.grid(row=n ,column=0)

        n+=1

        self.graph_prints_display_incidency_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_adj_list_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_is_eulerian.grid(row=n ,column=0)

        n+=1

        self.graph_prints_display_find_eulerian_cycle_entry.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_find_eulerian_cycle.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_hamilton_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_BFS_entry.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_BFS_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_DFS_entry.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_DFS_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_critcal_edge.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_SPW_entry_one.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_SPW_entry_two.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_SPW_button.grid(row=n,column=0)

        n+=1

        self.graph_prints_display_graph_prints_display_clear.grid(row=n,column=0)

#########################################################

    def graph_prints_display_clear(self):
        self.text_window.delete('1.0', END)

    def graph_prints_display_adj_list(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text("Graphs adjacency list")
            self.graph_prints_display_text(self.print_graph_adj_list())
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_adjacency(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text("Graphs adjacency matrix")
            self.graph_prints_display_text(self.print_graph_adj_matrix())

        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_incidence(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text("Graphs incidence matrix")
            self.graph_prints_display_text(self.print_graph_inc_matrix())
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_is_eulerian_function(self):
        if len(graf.nodes)>0:
            test=self.eulerian_test()
            if test==0:
                text="Graph isn't eulerian"
            if test==1:
                text="Graph has eulerian cycle"
            if test==2:
                text="Graph has eulerian path"
            self.graph_prints_display_text(text)
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_eulerian(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text(self.printforall(self.graph_prints_display_find_eulerian_cycle_entry.get(),"No"))
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_hamilton(self):
        if len(graf.nodes)>0:
            text=self.hamilton_test()
            self.graph_prints_display_text(text)
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_BFS(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text("Breadth First Search")
            self.graph_prints_display_text(self.BFS(self.graph_prints_display_BFS_entry.get()))
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_DFS(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text("Depth First Search")
            self.graph_prints_display_text(self.DFS(self.graph_prints_display_DFS_entry.get()))
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_critcal_edge_test(self):
        if len(graf.nodes)>0:
            self.graph_prints_display_text(self.critical_edge())
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_SPW(self):
        if len(graf.nodes)>1:
            if self.graph_prints_display_SPW_entry_one.get() in graf.nodes and self.graph_prints_display_SPW_entry_two.get() in graf.nodes:
                self.graph_prints_display_text(self.SPW(self.graph_prints_display_SPW_entry_one.get(),self.graph_prints_display_SPW_entry_two.get()))
            elif self.graph_prints_display_SPW_entry_one.get() in graf.nodes and not self.graph_prints_display_SPW_entry_two.get():
                self.graph_prints_display_text(self.SPW_all(self.graph_prints_display_SPW_entry_one.get()))
            elif self.graph_prints_display_SPW_entry_two.get() in graf.nodes and not self.graph_prints_display_SPW_entry_one.get():
                self.graph_prints_display_text(self.SPW_all(self.graph_prints_display_SPW_entry_two.get()))
            else:
                messagebox.showerror("Error", "There are no such a nodes")
        else:
            messagebox.showerror("Error", "Graph has no nodes")

    def graph_prints_display_text(self,text):
        self.text_window.insert(END, text,("a"))
        self.text_window.insert(END, "\r\n",("a"))
        self.text_window.tag_config("a",foreground="black",font="times 11")
        self.text_window.pack()

######## Create visited={}##################

    def createVisited(self):
        graf.convert_to_adj_list()
        visited={}
        for index in graf.adj_list:
            visited[index]=False
        return visited


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
        visited=self.createVisited()
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

############################################

###############################################
######    Euler path/cycle    ################

    def printforall(self,var1="novariable",var="yes"):
        self.text=""
        graf.convert_to_adj_list()
        if var1!="novariable" and str(var1) in graf.nodes:
            u=var1
        else:
            u=list(graf.nodes)[0]
            for node in graf.nodes:
                if len(graf.nodes[u])>len(graf.nodes[node]):
                    u=node
        if self.eulerian_test()==1 or self.eulerian_test()==2:
            if self.eulerian_test()==1 and len(graf.edge_quantity)>0:
                if var=="draw":
                    self.text=("Cycle\r\n")
                else:
                    self.text="Cycle\r\n"
            if self.eulerian_test()==2 and len(graf.edge_quantity)>0:
                if var=="draw":
                    self.text=("Path\r\n")
                else:
                    self.text="Path\r\n"
            for i in graf.adj_list:
                if len(graf.adj_list[i]) %2 != 0:
                    u=i
                    break
            self.printEuler(u,var)
            if var!="yes":
                return self.text
        else:
            if var=="draw":
                self.text="Graph isn't eulerian"
                return 0
            else:
                self.text="Graph isn't eulerian"
                return self.text

    def printEuler(self,u,var):
        for v in graf.adj_list[u]:
            if self.validNextEdge(u,v):
                if var=="draw":
                    self.text+=u+" "+v
                    self.text+="\r\n"
                else:
                    self.text+=u+"->"+v+" "
                self.rmvEdge(u,v)
                self.printEuler(v,var)

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
######    Hamilton path/cycle    ##############

    def hamilton_test(self):
        self.text=""
        self.consistency=True
        self.path=[]
        self.longestPath=[]
        graph_len=len(graf.nodes)
        if graph_len < 2:
            self.text=("Graph has one or fewer nodes")
            self.consistency=False
        graf.convert_to_adj_list()
        visited=self.createVisited()
        for index in graf.adj_list:
            if len(graf.adj_list[index])<1:
                self.consistency=False
                break;
        if self.consistency==True:
            u=list(graf.adj_list.keys())[0]
            self.isConsistent(visited, u)
        for index in visited:
            if visited[index]==False:
        #        print("Graph isn't consistent")
                self.consistency=False
                self.text="Graph isn't consistent"
                return self.text
        if self.consistency==True:
            self.path=[]
            self.pathvisited={}
            self.u=list(graf.adj_list.keys())[0]
            for node in graf.nodes:
                if len(graf.nodes[node])<len(graf.nodes[self.u]):
                    self.u=node
            self.findPath(self.u)
            return self.text

    def isConsistent(self,visited,index):
        visited[index]=True
        for i in graf.adj_list[index]:
            if visited[i]==False:
                self.isConsistent(visited,i)

    def findPath(self,index):
        found=False
        self.tempstr=""
        self.path.append(index)
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
            if len(self.path)==len(graf.adj_list) and self.u in graf.adj_list[index]:
                if self.u in graf.adj_list[index]:
                    if len(graf.nodes[self.u])>1:
                        self.path.append(self.u)
                        self.text="Found hamiltons cycle\r\n"
                    else:
                        self.text="Found hamiltons path\r\n"
            #        print(self.path)
                    self.text=self.convert_to_text(self.path)
                    return self.text
                else:
            #        print("Longest path")
            #        print(self.longestPath)
                    self.text=self.convert_to_text(self.longestPath)
                    return self.text
            else:
                h=self.path.pop()
                if len(self.path)==0:
            #        print("Longest path",self.longestPath)
                    self.text="Path\r\n"
                    self.text=self.convert_to_text(self.longestPath)
                    return self.text
                else:
                    i=self.path.pop()
                    self.findPath(i)

    def convert_to_text(self,converted_object):
        first=True
        for key in converted_object:
            if first==True:
                self.text+=" "
                self.text+=key
                first=False
            else:
                self.text+=" -> "+key
        return self.text

###############################################
######    Breadth First Search   ##############

    def BFS(self,var="novariable"):
        self.temp_string=""

        if var!="novariable" and str(var) in graf.nodes:
            s=var
        else:
            s=list(graf.nodes)[0]
        visited=self.createVisited()
        queue=[]
        queue.append(s)
        visited[s]=True
        while queue:
            s=queue.pop(0)
            self.temp_string+=str(s)
            self.temp_string+="-"
            for i in graf.adj_list[s]:
                if visited[i]==False:
                    queue.append(i)
                    visited[i]=True
        self.temp_string=self.temp_string[:-1]
        return self.temp_string

###############################################
######    Depth First Search   ##############

    def DFS(self,var="novariable"):
        self.temp_string=""
        if var!="novariable" and str(var) in graf.nodes:
            v=var
        else:
            v=list(graf.nodes)[0]
        visited=self.createVisited()
        self.DFSfunction(v,visited)
        self.temp_string=self.temp_string[:-1]
        return self.temp_string

    def DFSfunction(self,v,visited):
        visited[v]=True
        self.temp_string+=str(v)
        self.temp_string+=("-")
        for i in graf.adj_list[v]:
            if visited[i]==False:
                self.DFSfunction(i,visited)

###############################################
######### SEARCH for critcal edge #############

    def critical_edge(self):
        self.text=""
        self.critical_edges=[]
        for node1 in graf.nodes:
            for node2 in graf.nodes:
                if node1+node2 in graf.edge_quantity:
                    self.consistency=True
                    graf.convert_to_adj_list()
                    self.isitcritical(node1,node2)

        if len(self.critical_edges)<1:
            self.text+="There is no critical edges"
            return self.text
        else:
            return self.text

    def isitcritical(self,node1,node2):
        visited=self.createVisited()
        self.isConsistent(visited,node1)
        for index in visited:
            if visited[index]==False:
                self.text="Graph isn't consistent"
                self.consistency=False
                break;
        if self.consistency==True:
            graf.remove_edge(node1,node2)
            for nodes in graf.adj_list:
                visited[nodes]=False
            self.isConsistent(visited,node1)
            for index in visited:
                if visited[index]==False:
                    if node1+node2 not in self.critical_edges:
                        self.text+="Edge "
                        self.text+=str(node1)+str(node2)
                        self.text+=" is critical\r\n"
                        self.critical_edges.append(node1+node2)
                        self.critical_edges.append(node2+node1)
                        break;
            graf.add_edge_undirected(node1,node2)

###############################################
#########Shortest path from to#################

    def SPW(self,start_node,end_node):
        self.node_wage={}
        self.node_path={}
        visited=self.createVisited()
        if self.areConnected(visited,start_node,end_node)==True:
            self.visited=self.createVisited()
            self.current_node=start_node
            self.node_wage[self.current_node]=0
            self.node_path[self.current_node]=""
            while self.visited[end_node]==False:
                self.looking_for_shorest_path()

            self.text=str(start_node)
            for node in self.node_wage:
                if node==end_node:
                    self.text+=str(self.node_path[node])+"\r\n"
                    self.text+="Path wage "+str(self.node_wage[node])
            return self.text
        else:
            return "Nodes aren't connected"

    def areConnected(self,visited,start_node,end_node):
        visited[start_node]=True
        for i in graf.adj_list[start_node]:
            if visited[i]==False:
                self.areConnected(visited,i,end_node)
        if visited[end_node]==True:
            return True
        else:
            return False

    def looking_for_shorest_path(self):
        self.visited[self.current_node]=True
        for node in graf.adj_list[self.current_node]:                              ### adds node
            if self.visited[node]==False:
                if node not in self.node_wage:
                    self.node_wage[node]=int(self.node_wage[self.current_node])+int(graf.edge_wage[self.current_node+node])
                    self.node_path[node]=str(self.node_path[self.current_node])+"->"+str(node)
                else:
                    if self.node_wage[node]>int(self.node_wage[self.current_node])+int(graf.edge_wage[self.current_node+node]):
                        self.node_wage[node]=int(self.node_wage[self.current_node])+int(graf.edge_wage[self.current_node+node])
                        self.node_path[node]=str(self.node_path[self.current_node])+"->"+str(node)
        self.available=[]
        for node in self.visited:
            if self.visited[node]==False and node in self.node_wage:
                self.available.append(node)
        self.current_node=None
        for node in self.available:                                   ### searches for next node with lowest wage
            if self.current_node==None:
                self.current_node=node
            if self.node_wage[node]<self.node_wage[self.current_node] and self.visited[node]==False:
                self.current_node=node


###############################################
#########Shortest path for all #################

    def SPW_all(self,start_node):
        self.node_wage={}
        self.node_path={}
        self.availablenodes=[]
        self.text=""
        isConsistent=True
        visited=self.createVisited()
        self.isConsistent(visited,start_node)
        i=0
        for node in visited:
            if visited[node]==True:
                i+=1
        if i>0:
            self.visited=self.createVisited()
            self.current_node=start_node
            self.node_wage[self.current_node]=0
            self.node_path[self.current_node]=""
            while i>0:
                self.looking_for_shorest_path()
                i-=1

            self.text="Shortest paths from node "+str(start_node)+"\r\n"
            for node in self.node_wage:
                if node!=start_node:
                    self.text+="to node "+node+"\r\n"
                    self.text+=str(start_node)+self.node_path[node]+"\r\n"
                    self.text+="Path length= "+str(self.node_wage[node])+"\r\n"
            return self.text
        else:
            self.text="Nodes aren't connected"
            return self.text


###############################################
#########Shortest path from to#################

    def coloring(self,type="adjmat"):
        if len(graf.nodes)>0:
            visited=self.createVisited()
            u=list(graf.nodes)[0]
            self.nodeslist=[]
            self.colors=["blue","green","yellow","black","red","brown","orange"]
            text="Color rank\r\n"
            i=1
            for color in self.colors:
                text+=color+" is "+str(i)+"\r\n"
                i+=1
            self.print_text_into_printspace(text)
            self.groups={}
            self.colored={}


            for color in self.colors:
                self.groups[color]=[]

            if type=="node_random":
                for node in graf.nodes:
                    self.nodeslist.append(node)
                u=random.choice(self.nodeslist)

            if type=="node_deg":
                for index in graf.adj_list:
                    if len(graf.adj_list[u])<len(graf.adj_list[index]):
                        u=index

            self.groups["blue"].append(u)

            if type=="node_random":
                self.color_random(visited,u)
            if type=="adj_mat":
                self.color_adj_mat(visited,u)
            if type=="node_deg":
                self.color_node_deg(visited,u)


            for color in self.groups:
                for nodes in self.groups[color]:
                    self.c.create_oval(graf.return_X(nodes)-8,graf.return_Y(nodes)-8,graf.return_X(nodes)+8,graf.return_Y(nodes)+8,width=1,fill=str(color))

        else:
            messagebox.showerror("Error", "Graf has no nodes")

    def color_adj_mat(self,visited,u):
        visited[u]=True

        for index in graf.nodes:
            if visited[index]==False:
                for color in self.groups:
                    nextcolor=False
                    for nodes in graf.adj_list[index]:
                        if nodes in self.groups[color]:
                            nextcolor=True
                    if nextcolor==False:
                        self.groups[color].append(index)
                        self.color_adj_mat(visited,index)
                        break;

    def color_node_deg(self,visited,u):
        visited[u]=True
        chosen_node=False

        for node in graf.nodes:
            if visited[node]==False:
                chosen_node=node

        if chosen_node!=False:
            for index in graf.adj_list:
                if len(graf.adj_list[chosen_node])<len(graf.adj_list[index]) and visited[index]==False:
                    chosen_node=index
            for color in self.groups:
                nextcolor=False
                for nodes in graf.adj_list[chosen_node]:
                    if nodes in self.groups[color]:
                        nextcolor=True
                if nextcolor==False:
                    self.groups[color].append(chosen_node)
                    self.color_node_deg(visited,chosen_node)
                    break;

    def color_random(self,visited,u):
        visited[u]=True
        i=0
        for node in self.nodeslist:
            if node==u:
                break
            i+=1
        self.nodeslist.pop(i)

        chosen_node=u

        if self.nodeslist:
            while visited[chosen_node]==True:
                chosen_node=random.choice(self.nodeslist)

        if visited[chosen_node]==False:
            for color in self.groups:
                nextcolor=False
                for nodes in graf.adj_list[chosen_node]:
                    if nodes in self.groups[color]:
                        nextcolor=True
                if nextcolor==False:
                    self.groups[color].append(chosen_node)
                    self.color_random(visited,chosen_node)
                    break;



###############################################




###############################################
###### Dev options ###########################
    def open_dev_window(self):
        self.dev_window= Toplevel()
        self.dev_window.grab_set()
        self.dev_window.attributes("-topmost",True)
        self.dev_window.title('Dev Tools')
        self.dev_window.resizable(False,False)

        self.dev_window_frame=Frame(self.dev_window)
        self.dev_window_frame.pack(fill=BOTH, expand=False)

        self.dev_print_grafnodes= Button(self.dev_window_frame,text="Print GRAF.NODES",command=lambda: print(graf.nodes))
        self.dev_print_cordsX= Button(self.dev_window_frame,text="Print cordsX",command=lambda: print(graf.cordsX) )
        self.dev_print_cordsY= Button(self.dev_window_frame,text="Print cordsY",command=lambda: print(graf.cordsY))
        self.dev_print_edge_quantity= Button(self.dev_window_frame,text="Print edge quantity",command=lambda: print(graf.edge_quantity))
        self.dev_print_adjacencymatrix= Button(self.dev_window_frame,text="Print ADJACENCY",command= self.print_graph_adj_matrix)
        self.dev_print_incidencematrix= Button(self.dev_window_frame,text="Print var incmatrix",command=lambda: print(graf.incidence_matrix))
        self.dev_print_euler= Button(self.dev_window_frame,text="Print INCIDENCE MATRIX",command=self.print_graph_inc_matrix)
        self.dev_print_adj_list= Button(self.dev_window_frame,text="Print adj_list",command=lambda: print(graf.adj_list))
        self.dev_print_euler_cycles= Button(self.dev_window_frame,text="Eulerian cycles/paths",command=self.printforall)
        self.dev_add_node_label=Label(self.dev_window_frame,text="ADD NODE")
        self.dev_add_node_entry_name= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_entry_cordX= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_entry_cordY= Entry(self.dev_window_frame,width=4)
        self.dev_add_node_button_submit= Button(self.dev_window_frame,text="Submit", command=self.dev_add_node,width=4)
        self.dev_add_edge_label=Label(self.dev_window_frame,text="ADD EDGE")
        self.dev_add_edge_entry_node1= Entry(self.dev_window_frame,width=4)
        self.dev_add_edge_entry_node2= Entry(self.dev_window_frame,width=4)
        self.dev_add_edge_entry_wage= Entry(self.dev_window_frame,width=4)
        self.dev_add_edge_button_submit= Button(self.dev_window_frame,text="Submit", command=self.dev_add_edge,width=4)
        self.dev_remove_edge_label=Label(self.dev_window_frame,text="REMOVE EDGE")
        self.dev_remove_edge_entry_node1= Entry(self.dev_window_frame,width=4)
        self.dev_remove_edge_entry_node2= Entry(self.dev_window_frame,width=4)
        self.dev_remove_edge_button_submit= Button(self.dev_window_frame,text="Submit", command=self.dev_remove_edge,width=4)
        self.dev_hamilton= Button(self.dev_window_frame,text="Convert to adj mat", command= graf.convert_to_adj_matrix,width=15)
        self.dev_bfs_label=Label(self.dev_window_frame,text="BFS")
        self.dev_bfs_entry= Entry(self.dev_window_frame,width=4)
        self.dev_bfs_button= Button(self.dev_window_frame,width=15,text="Submit", command=self.BFS)
        self.dev_dfs_label=Label(self.dev_window_frame,text="DFS")
        self.dev_dfs_entry= Entry(self.dev_window_frame,width=4)
        self.dev_dfs_button= Button(self.dev_window_frame,width=15,text="Submit", command=self.DFS)
        self.dev_critical_edges= Button(self.dev_window_frame,width=15,text="Critical Edges", command=self.critical_edge)
        self.dev_draw_graph= Button(self.dev_window_frame,width=15,text="COLORING", command=self.coloring)
        self.dev_checkout= Checkbutton(self.dev_window_frame,width=15,text="Dev_checkout", variable=self.showcords)
        self.dev_SPW_node= Entry(self.dev_window_frame,width=4)
        self.dev_shortest_path_wage= Button(self.dev_window_frame,width=15,text="Shortest Wage Path", command=lambda: self.SPW_all(self.dev_SPW_node.get()))
        self.dev_SPW_for_all_node1= Entry(self.dev_window_frame,width=4)
        self.dev_SPW_for_all_node2= Entry(self.dev_window_frame,width=4)
        self.dev_shortest_path_wage_for_all= Button(self.dev_window_frame,width=15,text="Shortest Wage Path", command=lambda: self.SPW(self.dev_SPW_for_all_node1.get(),self.dev_SPW_for_all_node2.get()))


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
        self.dev_add_edge_label.grid(row=10,column=0)
        self.dev_add_edge_entry_node1.grid(row=10,column=1)
        self.dev_add_edge_entry_node2.grid(row=10,column=2)
        self.dev_add_edge_entry_wage.grid(row=10,column=3)
        self.dev_add_edge_button_submit.grid(row=10,column=4)
        self.dev_remove_edge_label.grid(row=11,column=0)
        self.dev_remove_edge_entry_node1.grid(row=11,column=1)
        self.dev_remove_edge_entry_node2.grid(row=11,column=2)
        self.dev_remove_edge_button_submit.grid(row=11,column=3)
        self.dev_hamilton.grid(row=12,column=0)
        self.dev_bfs_label.grid(row=13,column=0)
        self.dev_bfs_entry.grid(row=13,column=1)
        self.dev_bfs_button.grid(row=13,column=2)
        self.dev_dfs_label.grid(row=14,column=0)
        self.dev_dfs_entry.grid(row=14,column=1)
        self.dev_dfs_button.grid(row=14,column=2)
        self.dev_critical_edges.grid(row=15,column=0)
        self.dev_draw_graph.grid(row=16,column=0)
        self.dev_checkout.grid(row=17,column=0)
        self.dev_shortest_path_wage.grid(row=18,column=0)
        self.dev_SPW_node.grid(row=19,column=0)
        self.dev_shortest_path_wage.grid(row=19,column=1)
        self.dev_SPW_for_all_node1.grid(row=20,column=0)
        self.dev_SPW_for_all_node2.grid(row=20,column=1)
        self.dev_shortest_path_wage_for_all.grid(row=20,column=2)

    def dev_add_node(self):
        if self.dev_add_node_entry_name.get() not in graf.nodes and self.dev_add_node_entry_cordX.get() and self.dev_add_node_entry_cordY.get():
            graf.add_node(self.dev_add_node_entry_name.get(),self.dev_add_node_entry_cordX.get(),self.dev_add_node_entry_cordY.get())
            self.draw_graph()
        else:
            messagebox.showerror("Error", "NIE")

    def dev_add_edge(self):
        if self.dev_add_edge_entry_node1.get() in graf.nodes and self.dev_add_edge_entry_node2.get() in graf.nodes:
            if self.dev_add_edge_entry_wage.get():
                if self.dev_add_edge_entry_wage.get().isnumeric():
                    graf.add_edge_undirected(self.dev_add_edge_entry_node1.get(),self.dev_add_edge_entry_node2.get(),self.dev_add_edge_entry_wage.get())
                    self.draw_graph()
                else:
                    messagebox.showerror("Error", "Wage must be a number")
            else:
                graf.add_edge_undirected(self.dev_add_edge_entry_node1.get(),self.dev_add_edge_entry_node2.get())
                self.draw_graph()
        else:
            messagebox.showerror("Error", "NIE")

    def dev_remove_edge(self):
        if self.dev_remove_edge_entry_node1.get() and self.dev_remove_edge_entry_node2.get() and self.dev_remove_edge_entry_node2.get()+self.dev_remove_edge_entry_node1.get() in graf.edge_quantity:
            graf.remove_edge(self.dev_remove_edge_entry_node1.get(),self.dev_remove_edge_entry_node2.get())
            self.draw_graph()
        else:
            messagebox.showerror("Error", "NIE")

    def save(self):
        graf.convert_to_adj_list()
        f=asksaveasfile(mode='w',defaultextension=".txt")
    #    filename="Savedgraf.txt"
    #    f=open(filename,"w+")
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
                f.write(str(index))
                f.write(" ")
                f.write(str(keys))
                f.write(" ")
                f.write(str(graf.edge_wage[str(index)+str(keys)]))
                f.write("\r\n")

        f.close()

    def load(self):
        self.clear_canvas(self.c)
        filename=askopenfilename()
    #    filename="Savedgraf.txt"
        f=open(filename,"r")
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
                        node1=str(y)
                    if i==1:
                        node2=str(y)
                    if i==2:
                        edge_wage=int(y)
                    i+=1
                graf.add_edge_directed(node1,node2)
                graf.change_wage(node1,node2,edge_wage)
        f.close()
        self.draw_graph()






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
