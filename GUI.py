from tkinter import *
from tkinter import ttk, colorchooser
from Grafy import *
from PIL import Image, ImageTk




class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.switch_variable = StringVar(value="off")
        self.drawWidgets()
        self.tools(self.switch_variable)
        #self.c.bind('<B1-Motion>',self.paint)#drwaing the line
        self.c.bind('<ButtonPress-1>',self.Cords)
        self.c.bind('<ButtonRelease-1>',self.reset)


    def drawWidgets(self):
        self.controls=Frame(self.master,padx=5,pady=5,bg="black")
        self.buttons=Frame(self.controls,padx=3,pady=3, bd=2,relief="sunken")
        self.buttons.pack(side=LEFT)
        self.draw_button = Radiobutton(self.buttons, text="AddNode",variable=self.switch_variable,indicatoron=False, value="draw", height=1)
        self.draw_Entry= Entry(self.buttons,width=5,justify=RIGHT)
        self.select_button = Radiobutton(self.buttons, text="Select",variable=self.switch_variable,indicatoron=False, value="select", height=1)
        #self.removeNode_button = Button(self.buttons, text="Remove Node", height=1)
        #self.removeNode_Entry= Entry(self.buttons,width=5,justify=RIGHT)
        self.unEdge_button = Radiobutton(self.buttons, text="UnEdge",variable=self.switch_variable,indicatoron=False, value="drawUndirected", height=1)
        self.buttonPrint= Button(self.buttons,text = "Print", command= self.print_graph, height=1)
        self.draw_Entry.pack(side="left",fill=Y, expand=True)
        self.draw_button.pack(side="left",fill=Y, expand=True)
        #self.removeNode_Entry.pack(side="left",fill=Y, expand=True)
        #self.removeNode_button.pack(side="left",fill=Y, expand=True)
        self.unEdge_button.pack(side="left",fill=Y, expand=True)
        self.select_button.pack(side="left",fill=Y, expand=True)
        self.buttonPrint.pack(side="left")
        self.controls.pack(side=TOP,fill=X, expand=False)

        self.print=Canvas(self.master,height=400,width=100, bg=self.color_bg)
        self.print.pack(side=LEFT,fill=Y,expand=False)



        self.c=Canvas(self.master,width=500,height=400,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)


        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label='Options',menu=self.optionmenu)
        self.optionmenu.add_command(label='Clear',command=self.clear_canvas)
        self.optionmenu.add_command(label='Exit',command=self.master.destroy)


    def clear_canvas(self):
        self.c.delete(ALL)
        graf.clear_graph()

    def tools(self,task):
        self.tool=task

    def print_graph(self):
        self.print.delete(ALL)
        self.text=graf.name
        self.text+="\n"
        for source in graf.nodes:
            self.text+=source
            self.text+=":\n"
            for keys in graf.nodes[source]:
                self.text+=keys
                self.text+="\n"

        #self.label= Label(self.print,font="Times 10 italic bold", text=self.text, width=15)
        self.print.create_text(25,200,fill="darkblue",font="Times 10 italic bold", text=self.text)



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
                        self.new_x=round(e.x,-1)
                        self.new_y=round(e.y,-1)
                        graf.add_node(self.draw_Entry.get(),self.new_x, self.new_y)
                        #self.c.create_line(self.new_x,self.new_y,self.new_x,self.new_y,width=10,fill="black",capstyle=ROUND,smooth=True)
                        self.c.create_image(self.new_x,self.new_y, image=photo)
                        self.c.create_text(self.new_x+10,self.new_y-15,fill="darkblue",font="Times 10 italic bold", text=self.draw_Entry.get())
                    else:
                        print("You can't add more then one node with the same name")

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
                                                    self.c.create_line(graf.cordsX[source],graf.cordsY[source],graf.cordsX[keys],graf.cordsY[keys],width=1,fill="black",capstyle=ROUND,smooth=True)
                                                    graf.add_edge_undirected(source,keys)

        if self.tool=="select":
            self.new_x=e.x
            self.new_y=e.y
            for source in graf.cordsX:
                for i in range(self.old_x-10,self.old_x+10):
                    if i in graf.cordsX[source]:

                        for k in range(self.old_y-20,self.old_y+20):
                            if k in graf.cordsY[source]:
                                self.c.create_image(graf.cordsX[source],graf.cordsY[source], image=selectedPhoto)










if __name__ == '__main__':

    graf= Graf()
    root = Tk()
    image = Image.open("plusresized.jpg")
    photo = ImageTk.PhotoImage(image)
    selected = Image.open("plusselected.jpg")
    selectedPhoto = ImageTk.PhotoImage(selected)
    main(root)
    root.title('Application')

    root.mainloop()



"""
class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line
        self.c.bind('<ButtonRelease-1>',self.reset)

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas
        self.old_x = None
        self.old_y = None

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e


    def clear(self):
        self.c.delete(ALL)

    def change_fg(self):  #changing the pen color
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #changing the background color canvas
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 5,pady = 5)
        Label(self.controls, text='Pen Width:',font=('arial 18')).grid(row=0,column=0)
        self.slider = ttk.Scale(self.controls,from_= 5, to = 100,command=self.changeW,orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0,column=1,ipadx=30)
        self.controls.pack(side=LEFT)

        self.c = Canvas(self.master,width=500,height=400,bg=self.color_bg,)
        self.c.pack(fill=BOTH,expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Brush Color',command=self.change_fg)
        colormenu.add_command(label='Background Color',command=self.change_bg)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options',menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas',command=self.clear)
        optionmenu.add_command(label='Exit',command=self.master.destroy)



if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Application')
    root.mainloop()
"""
