# pylint: disable=C0103,C0111,W0614,W0401,C0200,C0325
import tkinter
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
from tkinter import *
import csv

##
# This is an implementation based on the original implementation @ https://github.com/ssebs/csveditor.git
# 2022 Anderson Paschoalon
##

class CsvDicEditor(Frame):

    cellList = []
    currentCells = []
    currentCell = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createDefaultWidgets()
        self.filename = ""
        self.label_key = "Key"
        self.label_value = "Value"

    def run_app(self, filename="", label_key="Key", label_value="Value"):
        self.filename = filename
        self.label_value = label_value
        self.label_key = label_key
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_command(label="Save Values", command=self.saveCells)
        menubar.add_command(label="Exit", command=self.quit)
        self.master.title("CsvDic Editor [" + filename + "]")
        self.master.config(menu=menubar)
        default_font = tkinter.font.nametofont("TkTextFont")
        default_font.configure(family="Helvetica")
        self.option_add("*Font", default_font)
        self.loadCells(filename)
        self.mainloop()

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
                    if( i >= len(self.currentCells) - 1):
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
        self.sizeX = 4
        self.sizeY = 6
        self.defaultCells = []
        for i in range(self.sizeY):
            self.defaultCells.append([])
            for j in range(self.sizeX):
                self.defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
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
                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)
        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
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
        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])
        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print rows[i][j]
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
                tmp = Text(self, width=w, height=1)
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
                self.cellList.append(tmp)
                tmp.grid(padx=0, pady=0, column=j, row=i)
        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]

    def loadCells_bkp(self, filename):
        #filename = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
        #                                        filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
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
        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])
        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print rows[i][j]
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
                tmp = Text(self, width=w, height=1)
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
    filename = "../Sandbox/ActorsTest01.csv"
    app = CsvDicEditor()
    app.run_app(filename)

