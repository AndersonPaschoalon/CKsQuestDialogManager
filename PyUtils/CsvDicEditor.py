import csv
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
import tkinter as tk
from PyUtils.ScreenInfo import ScreenInfo
from PyUtils.ScrollFrame import ScrollFrame


class CsvDicEditor(tk.Frame):

    cellList = []
    currentCells = []
    currentCell = None

    def __init__(self, master=None, height=650):
        # print("CsvDicEditor2")
        (width, height) = ScreenInfo.golden_display_pair(height)
        tk.Frame.__init__(self, master, width=width, height=height)
        self.pack_propagate(0)
        self.scroll_frame = ScrollFrame(self)  # add a new scrollable frame.
        self.scroll_frame.pack(side="top", fill="both", expand=True)
        # self.scroll_frame.pack(side="bottom", expand=True)
        self.grid()
        self.filename = ""

    def run_app(self, filename=""):
        # print("CsvDicEditor2.run_app()")
        self.filename = filename
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Save Values", command=self.saveCells)
        menubar.add_command(label="Exit", command=self.quit)
        self.master.title("CsvDic Editor [" + filename + "]")
        self.master.config(menu=menubar)
        default_font = tkinter.font.nametofont("TkTextFont")
        default_font.configure(family="Helvetica")
        self.option_add("*Font", default_font)
        if filename != "" and filename != None:
            # print("Opening file " + filename)
            self.loadCells(filename)
        else:
            # print("No filename was provided.")
            self.createDefaultWidgets()
        # ???????????
        # self.pack(side="top", fill="both", expand=True)
        self.mainloop()

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        print("focus_right")
        widget = event.widget.focus_get()
        position = widget.index(tk.INSERT)
        widget.icursor(position + 1)
        return "break"

    def focus_left(self, event):
        print("focus_left")
        widget = event.widget.focus_get()
        position = widget.index(tk.INSERT)
        widget.icursor(position - 1)
        return "break"

    def focus_up(self, event):
        print("focus_up")
        widget = event.widget.focus_get()
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if i < 0:
                        i = len(self.currentCells)
                    self.currentCells[i-1][j].focus()
        return "break"

    def focus_down(self, event):
        widget = event.widget.focus_get()
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if i >= len(self.currentCells) - 1:
                        i = -1
                    self.currentCells[i+1][j].focus()
        return "break"

    def saveFile(self, event):
        # print("CsvDicEditor2.saveFile()")
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
                # create cell and place it into a grid
                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
                sv.set("")
                tmp = tk.Entry(self.scroll_frame.viewPort, textvariable=sv, width=15)
                tmp.grid(padx=0, pady=0, column=j, row=i)
                # create binding keys
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-s>", self.saveFile)
                # update current pointers
                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)
        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
        self.currentCell = self.currentCells[0][0]

    def removeCells(self):
        while len(self.cellList) > 0:
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
                # print("col:" + str(col))
                # print("row:" + str(row))
        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])
        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print("row(i,j)=<" + str(rows[i][j]) + ">")
                ary[i][j] = rows[i][j]
        self.removeCells()
        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if len(ary[i][j]) >= mx:
                    mx = len(ary[i][j])
        w = mx
        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])
        [width_1, width_2] = CsvDicEditor.calc_cols_width(15, 9999, ary)
        # print("==> " + str([width_1, width_2]))
        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                # create cell and place it into the grid
                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
                # disable editing on the first column
                if j == 0:
                    tmp = tk.Entry(self.scroll_frame.viewPort, textvariable=sv, width=width_1)
                    tmp.configure(state='disabled')
                else:
                    tmp = tk.Entry(self.scroll_frame.viewPort, textvariable=sv, width=width_2)
                tmp.grid(padx=0, pady=0, column=j, row=i)
                sv.set(str(ary[i][j]))
                # binding keys
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-s>", self.saveFile)
                # update pointers
                loadCells[i][j] = tmp
                tmp.focus_force()
                self.cellList.append(tmp)
        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]

    def saveCells(self):
        vals = []
        for i in range(len(self.currentCells)):
            row = []
            for j in range(len(self.currentCells[0])):
                row.append(self.currentCells[i][j].get().strip())
            vals.append(row)
        # print("------------------")
        # print(vals)
        with open(self.filename, "w") as csvfile:
            for curr_row in vals:
                row = ""
                for i in range(len(curr_row)):
                    if i == 0:
                        row += curr_row[i] + ","
                    elif i < len(curr_row) - 1:
                        row += '"' + curr_row[i] + '"' + ","
                    else:
                        row += '"' + curr_row[i] + '"'
                csvfile.write(row + "\n")
        tkinter.messagebox.showinfo("", "Saved!")

    @staticmethod
    def calc_cols_width(min_width, max_width, data_matrix):
        """
        Calculate the max number of characters of each columns.
        :param min_width:
        :param max_width:
        :param data_matrix:
        :return:
        """
        max_len1 = 0
        max_len2 = 0
        try:
            curr_len = 0
            for item in data_matrix:
                curr_len = len(item[0])
                if curr_len > max_len1:
                    max_len1 = curr_len
        except:
            # print("error calculating max_len1")
            max_len1 = min_width
        try:
            curr_len = 0
            for item in data_matrix:
                curr_len = len(item[1])
                if curr_len > max_len2:
                    max_len2 = curr_len
        except:
            # print("error calculating max_len2")
            max_len2 = min_width
        width_1 = 0
        if max_len1 < min_width:
            width_1 = min_width
        elif max_len1 > max_width:
            width_1 = max_width
        else:
            width_1 = max_len1
        width_2 = 0
        if max_len2 < min_width:
            width_2 = min_width
        elif max_len1 > max_width:
            width_2 = max_width
        else:
            width_2 = max_len2
        print([width_1, width_2])
        return [width_1, width_2]



def callback(sv):
    print(sv.get())

if __name__ == "__main__":
    # test
    filename = "Actors2.csv"
    app = CsvDicEditor()
    app.run_app(filename)


