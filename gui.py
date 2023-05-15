import tkinter as tk

class TitleScreen():
    def __init__(self):
        self.window = tk.Tk()
        self.title = tk.Label(text = "Tanks!",
                              fg = "green",
                              bg = "saddle brown",
                              width = 20,
                              heigh = 5,
                              font = 20)
        self.buttons = [tk.Button(self.window, text = "Player vs AI", command = lambda:self.pva()),
                        tk.Button(self.window, text = "Player vs Player", command = lambda:self.pvp()),
                        tk.Button(self.window, text = "2 Players vs AI", command = lambda:self.twopva()),
                        tk.Button(self.window, text = "Quit", command = lambda:self.endgame())]
        self.mode = None
        self.pack()
        self.display()


    def pack(self):
        self.title.pack()
        for i in self.buttons:
            i.pack()
    
    def pvp(self):
        print('pvp')
        self.mode = 1
        self.kill()
    
    def pva(self):
        print('pva')
        self.mode = 2
        self.kill()

    def twopva(self):
        print('2pva')
        self.mode = 3
        self.kill()

    def endgame(self):
        print('end')
        self.mode = 4
        self.kill()

    def display(self):
        self.window.mainloop()
    
    def kill(self):
        self.window.destroy()

# window = tk.Tk()
# window.title("Tanks!")
# # window.geometry("520x500")
# greeting = tk.Label(text="Tanks!",
#                     fg="green",
#                     bg="saddle brown",
#                     width=20,
#                     height=5,
#                     font=20)
# pva = tk.Button(window, text="Player vs AI", command=callback)
# pvp = tk.Button(window, text="Player vs Player", command=callback)
# ppva = tk.Button(window, text="2 Player vs AI", command=callback)
# greeting.pack()
# pva.pack()
# pvp.pack()
# ppva.pack()
# window.mainloop()