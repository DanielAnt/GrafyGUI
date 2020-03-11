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
        self.switch_variable = StringVar(value="draw")
        self.selected=False
        self.remove=False
        self.entry={}
        self.drawWidgets()
        self.tools(self.switch_variable)
        self.c.bind('<ButtonPress-1>',self.Cords)
        self.c.bind('<ButtonRelease-1>',self.reset)



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
        self.graphmenu.add_command(label='Macierz sąsiedzctwa',command=self.graph_add)
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label='Options',menu=self.optionmenu)
        self.optionmenu.add_command(label='Clear',command=self.clear_canvas)
        self.optionmenu.add_command(label='Exit',command=self.master.destroy)


    def clear_canvas(self):
        self.c.delete(ALL)
        graf.clear_graph()
        self.print.delete(ALL)

    def clear_canvas_remove_node(self):
        self.c.delete(ALL)
        self.print.delete(ALL)

    def tools(self,task):
        self.tool=task

    def print_graph(self):
        self.print.delete(ALL)
        self.text=graf.name
        self.text+="\n"
        for source in sorted(graf.nodes):
            self.text+=source
            self.text+=":\n"
            for keys in graf.nodes[source]:
                self.text+=keys
                self.text+="\n"
        self.print.create_text(50,200,fill="darkblue",font="Times 10 italic bold", text=self.text)

    def Cords(self,e):
        if self.tool!=self.switch_variable.get():
            self.tools(self.switch_variable.get())
        self.old_x= e.x
        self.old_y= e.y

    def reset(self,e):

        if self.tool=="draw":
            if e.x==self.old_x and e.y==self.old_y:
                if not self.draw_Entry.get():
                    print("There is no letter")
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
                                    break;

    def remove_node(self):
        if self.selected==True:
            self.remove=True
            temp_graf= Graf()
            for source in graf.nodes:
                if self.node!=source:
                    self.corx=graf.cordsX[source].pop()
                    self.cory=graf.cordsY[source].pop()
                    temp_graf.add_node(source,self.corx,self.cory)
                    for keys in graf.nodes[source]:
                        if self.node!=keys:
                            temp_graf.nodes[source].append(keys)

        if self.remove==True:
            graf.nodes=temp_graf.nodes
            graf.cordsX=temp_graf.cordsX
            graf.cordsY=temp_graf.cordsY
            self.clear_canvas_remove_node()
            for source in graf.nodes:
                self.c.create_image(graf.return_X(source),graf.return_Y(source), image=photo)
                self.c.create_text(graf.return_X(source)+10,graf.return_Y(source)-15,fill="darkblue",font="Times 10 italic bold", text=source)
            for source in graf.nodes:
                for keys in graf.nodes[source]:
                    if self.var1.get()==1:
                        self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys], arrow='last',width=1,fill="red",smooth=True)
                    else:
                        self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",smooth=True)

            temp_graf=None
            self.remove=False
            self.node=None
            self.selected=False
        else:
            messagebox.showerror("Error", "Select node that you want to remove")

    def graph_add(self):
        self.graph_add_window = Tk()
        self.graph_add_window.title('Add graph')
        self.frame_one=Frame(self.graph_add_window,width=100,height=500,borderwidth=2,relief='sunken')
        self.frame_two=Frame(self.graph_add_window,width=400,height=500,relief='sunken')
        self.frame_one.pack(side="left",fill=BOTH, expand=False)
        self.frame_two.pack(side="left",fill=BOTH, expand=False)
        self.nodeQuantity_Label=Label(self.frame_one,font="Times 10 italic bold",text='How many Nodes?')
        self.nodeQuantity_Entry= Entry(self.frame_one,width=15,justify=RIGHT)
        self.nodeQuantity_Button= Button(self.frame_one,width=15,text="Submit",command=self.NodeQuantity_Submit)
        self.nodeQuantity_Label.pack(side=TOP)
        self.nodeQuantity_Entry.pack(side=TOP)
        self.nodeQuantity_Button.pack(side=TOP)
        self.graph_add_window.mainloop()

    def NodeQuantity_Submit(self):
        if self.nodeQuantity_Entry.get().isnumeric() and int(self.nodeQuantity_Entry.get())<=10:
            i=0
            self.names=["A","B","C","D","E","F","G","H","I","J"]
            for name in self.names:
                if int(self.nodeQuantity_Entry.get())>i:
                    self.e= Entry(self.frame_two,width=25,justify=RIGHT)
                    self.e.pack(side=TOP)
                    self.entry[name]= self.e
                i+=1
            #self.entryButton= Button(self.frame_two,width=25,text="Submit",command=self.create_Adjacency_Matrix)
            self.entryButton= Button(self.frame_two,width=25,text="Submit",command=self.create_Adjacency_Matrix)
            self.entryButton.pack(side=TOP)

    def print_entry(self):
        text=""
        if self.entry:
            for name in self.entry:
                text+=str(self.entry[name].get())
        print(text)

    def create_Adjacency_Matrix(self):
        if int(self.nodeQuantity_Entry.get())==len(self.entry["A"].get()):
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
                    for keys in graf.nodes[name]:
                        self.c.create_line(graf.cordsX[name],graf.cordsY[name],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="red",smooth=True)
            self.entry={}
            self.graph_add_window.destroy()
        else:
            messagebox.showerror("Error", "Wrong matrix parameters")

                #graf.clear_graph()
                #graf.add_node('A',100,100)
                #graf.add_node('B',50,150)
                #graf.add_node('C',150,150)
                #graf.add_node('D',75,200)
                #graf.add_node('E',125,200)



                #for source in graf.nodes:
                #    self.c.create_text(graf.return_X(source)+10,graf.return_Y(source)-15,fill="darkblue",font="Times 10 italic bold", text=source)
                #for source in graf.nodes:
                #    for keys in graf.nodes[source]:
                #        self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys], arrow='last',width=1,fill="red",smooth=True)

                #self.entryOne= Entry(self.frame_two,width=25,justify=RIGHT)
                #self.entryTwo= Entry(self.frame_two,width=25,justify=RIGHT)
                #self.entryThree= Entry(self.frame_two,width=25,justify=RIGHT)
                #self.entryFour= Entry(self.frame_two,width=25,justify=RIGHT)
                #self.entryFive= Entry(self.frame_two,width=25,justify=RIGHT)
                #self.entryButton= Button(self.frame_two,width=25,text="Submit")
                #self.entryOne.pack(side=TOP)
                ##self.entryTwo.pack(side=TOP)
                #self.entryThree.pack(side=TOP)
                #self.entryFour.pack(side=TOP)
                #self.entryFive.pack(side=TOP)
                #self.entryButton.pack(side=TOP)










if __name__ == '__main__':

    graf= Graf()
    root = Tk()
    image = Image.open("node.jpg")
    photo = ImageTk.PhotoImage(image)
    selected = Image.open("nodeselected.jpg")
    selectedPhoto = ImageTk.PhotoImage(selected)
    main(root)
    root.title('Application')

    root.mainloop()
