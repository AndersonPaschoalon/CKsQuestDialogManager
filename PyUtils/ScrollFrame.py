import tkinter as tk
import platform


class ScrollFrame(tk.Frame):
    """
    Scrollable Frame Class
    """
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        # place canvas on self
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        # place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")
        # y scroll -- place a scrollbar on self
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # x scroll -- place a scrollbar on self
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        # attach scrollbar action to scroll of canvas
        self.canvas.configure(xscrollcommand=self.hsb.set)

        # pack bar
        # pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # pack scrollbar to right of self
        self.hsb.pack(side="bottom", fill="x")

        # pack canvas to left of self and expand to fil
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4),
                                                       window=self.viewPort,
                                                       anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)
        # bind an event whenever the size of the canvas frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)

        # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Enter>', self.onEnter)
        # unbind wheel events when the cursorl leaves the control
        self.viewPort.bind('<Leave>', self.onLeave)

        # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(
            None)

    def onFrameConfigure(self, event):
        """
        Reset the scroll region to encompass the inner frame
        :param event:
        :return: void
        """
        # whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))

    def onCanvasConfigure(self, event):
        """
        Reset the canvas window to encompass inner frame when required.
        *Note*: the last implementation was misconfiguring the interface, removing the implementation fixed it!
        :param event:
        :return:
        """
        # **old implementation**
        # canvas_width = event.width
        # self.canvas.itemconfig(self.canvas_window,
        # width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.
        pass

    def onMouseWheel(self, event):
        """
        Cross platform scroll wheel event.
        :param event:
        :return:
        """
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def onEnter(self, event):
        """
        Bind wheel events when the cursor enters the control.
        :param event:
        :return:
        """
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        """
        unbind wheel events when the cursor leaves the control
        :param event:
        :return:
        """
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

