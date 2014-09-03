from tkinter import *
from tkinter import ttk
from display import PixelDisplay, FillColor
from search import Search, SearchMode
from navigation import  NavigationNode, NavigationState

#When the user presses run this method is called. 
#The input entered in the textbox is retrieved, and split into tuples.
#These tuples are used to construct the state, navigationNode.
#A best, depth or breadth first search is run based on what
#radiobutton is active in the GUI.
def calculate(*args):
    try:
        text = data_entry.get("1.0", "end")
        arr = text.split()
        if len(arr) <3:
            raise Exception("Input not correct, to few tuples")
        for i in range(len(arr)):
        	#TODO: Not to happy about space after commas. (10, 10)
        	arr[i] = eval(arr[i])

        dim = arr.pop(0)
        start = arr.pop(0)
        end = arr.pop(0)

    except ValueError:
        pass
    s = Search( navigation_map )
    state = NavigationState( start, end, dim, arr )
    navigation_map.setModel(state)
    navigation_map.start()
    initalNode = NavigationNode( state, start[0], start[1] )
    result = s.search( initalNode, SearchMode(v.get()) )
    navigation_map.stop()

root = Tk()
root.title("A* navigation")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


data_entry = Text(mainframe, width=25, height=15)
data_entry.grid(column=1, row=0, columnspan=3, sticky=(W, E))

v = IntVar()
v.set(SearchMode.BEST.value)

best = Radiobutton(mainframe, text="Best", variable=v, value=SearchMode.BEST.value)
best.grid(column=1, row=2, sticky=(W, E))
depth = Radiobutton(mainframe, text="Depth", variable=v, value=SearchMode.DEPTH.value)
depth.grid(column=2, row=2, sticky=(W, E))
breadth = Radiobutton(mainframe, text="Breadth", variable=v, value=SearchMode.BREADTH.value)
breadth.grid(column=3, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Run", command=calculate).grid(column=1, row=3, sticky=W)

navigation_map = PixelDisplay(mainframe)
navigation_map.grid(column=0, row=0, sticky=E)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

data_entry.focus()
#root.bind('<Return>', calculate)

root.mainloop()