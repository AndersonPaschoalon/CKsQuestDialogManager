# pylint: disable=C0103,C0111,W0614,W0401,C0200,C0325
import csv
import tkinter as tk
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
from tkinter import *
from PyUtils.ScreenInfo import ScreenInfo


class T3CsvEditor():

    cellList = []
    currentCells = []
    currentCell = None

    def __init__(self, master=None):
        self.root = tk.Tk()
        self.frame = tk.Frame(master)
        self.frame.grid()


        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))

        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = tk.Frame(self.frame)
        self.frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.fcanvas = tk.Canvas(self.frame_canvas, bg="yellow")
        self.fcanvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.fcanvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.createDefaultWidgets()
        self.filename = ""
        self.frame.master.wm_maxsize(1200, 650)

    def onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    def run_app(self, filename="", label_key="Key", label_value="Value"):
        self.filename = filename
        menubar = Menu(self.frame)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_command(label="Save Values", command=self.saveCells)
        menubar.add_command(label="Exit", command=self.frame.quit)
        self.frame.master.title("CsvDic Editor [" + filename + "]")
        self.frame.master.config(menu=menubar)
        default_font = tkinter.font.nametofont("TkTextFont")
        default_font.configure(family="Helvetica")
        self.frame.option_add("*Font", default_font)
        self.loadCells(filename)
        #self.frame.mainloop()
        self.root.mainloop()

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j >= len(self.currentCells[0]) - 1 ):
                        j = -1
                    self.currentCells[i][j+1].focus()
        return "break"

    def focus_left(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j == 0):
                        j = len(self.currentCells[0])
                    self.currentCells[i][j-1].focus()
        return "break"

    def focus_up(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(i < 0):
                        i = len(self.currentCells)
                    self.currentCells[i-1][j].focus()
        return "break"

    def focus_down(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if i >= len(self.currentCells) - 1:
                        i = -1
                    self.currentCells[i+1][j].focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    def saveFile(self, event):
        self.saveCells()

    def createDefaultWidgets(self):
        w, h = 7, 1
        self.frame.sizeX = 4
        self.frame.sizeY = 6
        self.frame.defaultCells = []
        for i in range(self.frame.sizeY):
            self.frame.defaultCells.append([])
            for j in range(self.frame.sizeX):
                self.frame.defaultCells[i].append([])

        for i in range(self.frame.sizeY):
            for j in range(self.frame.sizeX):
                tmp = Text(self.frame, width=w, height=h, wrap=tkinter.WORD)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                tmp.insert(END, "")
                tmp.grid(padx=0, pady=0, column=j, row=i)
                self.frame.defaultCells[i][j] = tmp
                self.cellList.append(tmp)
        self.frame.defaultCells[0][0].focus_force()
        self.currentCells = self.frame.defaultCells
        self.currentCell = self.currentCells[0][0]

    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while(len(self.cellList) > 0):
            for cell in self.cellList:
                # print str(i) + str(j)
                cell.destroy()
                self.cellList.remove(cell)

    def loadCells(self, filename):
        ary = []
        col = -1
        rows = []
        # get array size & get contents of rows
        with open(filename, "r") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)
                print("col:" + str(col))
                print("row:" + str(row))

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])
        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                print("row(i,j)=<" + str(rows[i][j]) + ">")
                ary[i][j] = rows[i][j]
        self.removeCells()
        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if(len(ary[i][j]) >= mx):
                    mx = len(ary[i][j])
        w = mx
        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])
        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                txt_width = w if w < 100 else 100
                tmp = Text(self.frame, width=txt_width, height=1, wrap=tkinter.NONE)
                #tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                tmp.insert(END, ary[i][j])
                if j == 0:
                    tmp.configure(state='disabled')
                #if(i == 0):
                #    tmp.config(font=("Helvetica", 10, tkinter.font.BOLD))
                #    #tmp.config(relief=FLAT, bg=app.master.cget('bg'))
                #    tmp.config(relief=FLAT, bg=self.master.cget('bg'))
                loadCells[i][j] = tmp
                tmp.focus_force()
                #tmp.wraplength=300
                self.cellList.append(tmp)
                tmp.grid(padx=0, pady=0, column=j, row=i)
        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]

    def saveCells(self):
        #filename = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Save File", filetypes=(
        #    ("csv files", "*.csv"), ("all files", "*.*")), defaultextension=".csv")
        vals = []
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                vals.append(self.currentCells[i][j].get(1.0, END).strip())
        with open(self.filename, "w") as csvfile:
            for rw in range(len(self.currentCells)):
                row = ""
                for i in range(len(self.currentCells[0])):
                    x = rw * len(self.currentCells[0])
                    if(i != len(self.currentCells[0]) - 1):
                        row += vals[x + i] + ","
                    else:
                        #row += vals[x + i]
                        row += '"' + vals[x + i] + '"'
                csvfile.write(row + "\n")
        tkinter.messagebox.showinfo("", "Saved!")


if __name__ == "__main__":
    # test
    test01 = False
    test02 = True
    if test01:
        filename = "../Sandbox/ActorsTest01.csv"
        app = T3CsvEditor()
        app.run_app(filename)
    if test02:
        filename = "../Sandbox/Comments.csv"
        app = T3CsvEditor()
        app.run_app(filename)