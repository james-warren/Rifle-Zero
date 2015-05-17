### This is a learning exercise in Python. The idea is that, with a photo of
### a rifle target/archery tgt/dartboard etc. you could click on
### the bullseye & shot impact points and get an automatic calculation
### of the mean point of impact (MPI).
### You could then zero your rifle/adjust aim to correct
### for any discrepancy between MPI and bull

### JLW 2014

import sys

from tkinter import *

import numpy as np

root = Tk()

root.title("Rifle Zero")
root.geometry("1000x600")

################ FRAMES###################

f1 = Frame(root, background = "red",width = 700, height = 600) #only red to test if bits poking out
f1.grid(row = 0, column = 0, sticky = N) # main frame with canvas and picture

f2 = Frame(root, background = "grey", width = 300, height = 600)
f2.grid(row = 0, column = 1, sticky = N) #"sidebar" frame

f3 = Frame(f2, background = "green", width = 300, height = 300)
f3.grid(row = 0, column = 0, rowspan = 1, columnspan = 3) # Cursor D-pad frame within sidebar




       
######CANVAS BITS#############

# New frame to handle mouse-clicks
c = Canvas(f1, background='white', width=700, height=500)  

filename = input("Please enter filepath for target.gif \n >")

photo = PhotoImage(file = filename)


c.create_image (10,10, image = photo, anchor = NW)

c.focus_set() #apparently need this before key presses can be bound?
c.grid(row = 0 , column =0, sticky = N)

infolabel = Label(f1, text = "Left click = assign shot, d = delete shot \n "
                  "Right click = assign bullseye, b = delete bullseye\n "
                  "m = toggle M.P.I.")
infolabel.grid(row = 1, column =0)

############GLOBAL VARS##################

shot_lst=[] # array holding shot objects (x and y are in object itself)
global i
i=0

global M

global bull_exists
bull_exists = 0

global mpi_exists
mpi_exists = 0

global cursor_exists
cursor_exists = 0

global r # scaling cursor radius
r = 10

global d_for_scale_lbl
d_for_scale_lbl = IntVar()
d_for_scale_lbl.set(1)

global adj_x_cm #mpi adjustment to hit bull, x direction
adj_x_cm = IntVar()
adj_x_cm.set(0)

global adj_y_cm #mpi adjustment to hit bull, y direction
adj_y_cm = IntVar()
adj_y_cm.set(0)


######
class Shot:

    shot_count = 0
  
    def __init__(self, n, sx, sy): # n is shot number, sx, sy shot coords.
        Shot.shot_count += 1
        self.n = Shot.shot_count
        self.sx = sx
        self.sy = sy
        self.co = c.create_oval(sx-4, sy-4, sx+4, sy+4, fill="green")
        
        print ( "Shot count", Shot.shot_count)
        print(type(self.co))

    def __del__(self):
        Shot.shot_count -=1
        c.delete(self.co)  
        

######## CLASSES ################################################
        
class Bull:
    
    global bull_exists

    def __init__(self, sx, sy): # as for Shot,
        print ("instantiating bull")
        global bull_exists
        bull_exists = 1
        print ("bull exists", bull_exists)
        self.sx = sx
        print("self.sx", self.sx)
        self.sy = sy
        print("self.sy", self.sy)
        self.co = c.create_oval(sx-4, sy-4, sx+4, sy+4, fill="red")

    def __del__(self): # careful, if B isn't made global in drawbull then when
                       #  drawbull has finished, B is redundant which
                       # calls __del__ automatically!!!!! bull inst then del!!
                       # look into alternatives to __del__ method?
        print("deleting bull")
        global bull_exists
        bull_exists = 0
        c.delete(self.co)

class MPI: ###Mean Point of Impact

    global mpi_exists
    global M
    global B
    global adj_x_cm
    global adj_y_cm
    global d_for_scale_lbl
    

    def __init__(self, mx, my):
        print ("instantiating MPI")
        global mpi_exists
        mpi_exists = 1
        print ("MPI exist", mpi_exists)
        self.mx = mx
        print("self.mx", self.mx)
        self.my = my
        print("self.my", self.my)
        self.co = c.create_oval(mx-5, my-5, mx+5, my+5, fill="blue")
        self.xhair = c.create_line(mx-15, my, mx+15, my, fill="blue")
        self.yhair = c.create_line(mx, my-15, mx, my+15, fill="blue")

        if (bull_exists == True):   #calculate adjustment needed to MPI to hit bull
            adjustment_x_pix = ((B.sx)-self.mx)
            adjustment_y_pix = (self.my-(B.sy))
            print ("adjust x",adjustment_x_pix, "adjust y", adjustment_y_pix) 
            global adj_x_cm
            adj_x_cm.set("%.2f" %(adjustment_x_pix/d_for_scale_lbl.get()) )
            global adj_y_cm
            adj_y_cm.set("%.2f" %(adjustment_y_pix/d_for_scale_lbl.get()) )

    def __del__(self): 
        print("deleting MPI")
        global mpi_exists
        mpi_exists = 0
        c.delete(self.co, self.xhair, self.yhair)

        

        
################################## END OF CLASSES######################################

############### METHODS FOR SHOTS #############
def drawpoint (event):
    global i
    print ("mouse coords", event.x, event.y) 
    shot_lst.append(Shot(i+1, event.x, event.y))
   
    print ("CLASS obj number", shot_lst[i].n, "x", shot_lst[i].sx, "y", shot_lst[i].sy) 
    i = i+ 1


def delpoint (event):
    global i

    if((len(shot_lst))>0):
        del shot_lst[i-1]  # prints last value to screen and removes it from list
        print("deleting point", i)
                   
        i = i-1

    else:
        print ("There are no points to delete")

###### METHODS FOR BULL #######################
def drawbull (event):

    global bull_exists
    global B
    
    if (bull_exists == 0):
        print ("bull coords", event.x, event.y) 
        B = Bull(event.x, event.y)
        print("B", type(B))
   
        print ("CLASS bull exists", bull_exists, "x", B.sx, "y", B.sy)

    else:
        print ("Bull already exists")

def delbull (event):
    global bull_exists
    global B
    
    if(bull_exists ==1):
        print("B",B)
        del B
        print("method: deleting bull")
        print("Bull exists =", bull_exists)

    else:
        print ("There is no bull to delete")
        
####### METHOD FOR MPI CALC#####
def mpi_toggle(self):
    global mpi_exists
    global M

    if (mpi_exists == 0):
        print ("calculating MPI")
         
        i = 0   #local incrementor
        X = []
        Y = []

        while i<len(shot_lst):
            print ("x",(shot_lst[i].sx), "y",(shot_lst[i].sy))
            X.append(shot_lst[i].sx)
            Y.append(shot_lst[i].sy)
            
            i += 1

        print ("number of X points", len(X),
               "number of Y points", len(Y))
        print ("MPI X", np.mean(X), "Y", np.mean(Y))
        
        global M
        M = MPI(np.mean(X), np.mean(Y))

    else:
        print("destroying MPI")
        #global M statement not needed again, already declared global above
        X = [0]
        Y = [0]
        del M

#################SCALED CURSOR (reticle)################################
################# Added to program after other functions
################# Need to tidy up arrangement of code - separate files?

class Cursor:
    
    global cursor_exists
    global r
    global d_for_scale_lbl

    def __init__(self, sx, sy,sr): # as for Shot,
        #print ("instantiating cursor")
        global cursor_exists
        cursor_exists = 1
        #print ("cursor exists", cursor_exists)
        self.sx = sx
        #print("self.sx", self.sx)
        self.sy = sy
        #print("self.sy", self.sy)
        self.r = sr    # need sr as local name of param that has been passed
        global r       # updates global r to circle size
        r = self.r
        self.co = c.create_oval(sx-r, sy-r, sx+r, sy+r, outline="red")

        global d_for_scale_lbl # diameter = 2r which is IntVar for lbl_curs_diam textvariable,
         # this will display in GUI
        d_for_scale_lbl.set(2*r)

    def __del__(self): # As for Bull: careful, if isn't made global in drawbull then when
                       #  drawbull has finished,  is redundant which
                       # calls __del__ automatically!!!!! bull inst then del!!
                       # look into alternatives to __del__ method?
        #print("deleting cursor")
        global cursor_exists
        cursor_exists = 0
        c.delete(self.co)


#############

def drawcurs ():

    global cursor_exists
    global C

    curs_dflt_x = 300  #default dimensions
    curs_dflt_y = 300
    if (cursor_exists == 0):
        #print ("cursor coords", curs_dflt_x , curs_dflt_y , r) 
        C = Cursor(curs_dflt_x, curs_dflt_y, r)
        #print("C", type(C))
   
        #print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("Cursor already exists")

def delcurs ():
    global cursor_exists
    global C
    
    if(cursor_exists ==1):
        #print("C",C)
        del C
        #print("method: deleting cursor")
        #print("Cursor exists =", cursor_exists)

    else:
        print ("There is no cursor to delete")

def cursup ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
        #print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x, y-5, r)
        #print("Cursor moving up")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
       # print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def cursdown ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
       # print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x, y+5, r)
       # print("Cursor moving down")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
       # print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def cursleft ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
    #   print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x-5, y, r)
    #   print("Cursor moving left")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
       #  print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def cursright ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
      #  print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x+5, y, r)
      #  print("Cursor moving right")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
      #  print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def cursgrow ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
       #  print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x, y, r+5)
       # print("Cursor growing")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
       # print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def cursshrink ():
    global cursor_exists
    global C
    
    if (cursor_exists == 1):
       # print ("moving cursor, initial coords", C.sx, C.sy, C.r)
        x = C.sx
        y = C.sy
        r = C.r
        C = Cursor(x, y, r-5)
       # print("Cursor shrinking")

        cursor_exists = 1
        # need this since moving creates new C, deletes old meaning cursor exists goes to 0
   
       # print ("CLASS cursor exists", cursor_exists, "x", C.sx, "y", C.sy)

    else:
        print ("No cursor exists")

def checkr (event):
    #global r # don't need global declaration here, as you're not altering value.
    print (r)   


############### D-pad type buttons in f3 ###### should redo these as inst of a Button class?#####
    
lbl_curs_ctrl = Label(master = f3, text = "Scale Cursor Control", bg = "green",)
lbl_curs_ctrl.grid(row = 0, column = 1, columnspan = 3, sticky = N)
    
btn_up = Button(master = f3, text = "Up", height=3, width=6, activebackground="red",
                repeatdelay=500, repeatinterval = 25, command= cursup )
btn_up.grid(row=1, column=2)

btn_down = Button(master = f3, text = "Down", height=3, width=6, activebackground="red",
                  repeatdelay=500, repeatinterval = 25, command= cursdown)
btn_down.grid(row=4, column=2)

btn_left = Button(master = f3, text = "Left", height=3, width=6, activebackground="red",
                  repeatdelay=500, repeatinterval = 25, command= cursleft)
btn_left.grid(row=2, rowspan=2, column=1)

btn_right = Button(master =f3, text = "Right", height=3, width=6, activebackground="red",
                   repeatdelay=500, repeatinterval = 25, command= cursright)
btn_right.grid(row=2, rowspan=2, column=3)

btn_grow = Button(master = f3, text = "+", height=1, width=6, command = cursgrow)
btn_grow.grid(row=2, column=2)

btn_shrink = Button(master = f3, text = "-", height=1, width=6, command = cursshrink)
btn_shrink.grid(row=3, column=2)

btn_curs_on = Button(master = f3, text = "Curs On", height=1, width=6, command = drawcurs)
btn_curs_on.grid(row=1, column=1)

btn_curs_off = Button(master = f3, text = "Curs Off", height=1, width=6, command = delcurs)
btn_curs_off.grid(row=1, column=3)

lbl_curs_scale = Label(master = f3, text = "Curs Scale", bg = "white")
lbl_curs_scale.grid(row = 5, column = 1, sticky = E)

lbl_curs_diam = Label(master = f3, textvariable = d_for_scale_lbl, bg = "white", width = 10, height =1)
lbl_curs_diam.grid(row = 5, column = 2)

lbl_curs_units = Label(master = f3, text = "pixels/cm", bg = "white")
lbl_curs_units.grid(row = 5, column = 3, sticky = W)

###### LABELS FOR ADJUSTMENT OF MPI (shot correction)##################
### *** needs formatting

lbl_adjx_name = Label(master = f2, text = "Adjust x = ", bg = "white")
lbl_adjx_name.grid(row = 2, column = 0, sticky = E)

lbl_adjx_value = Label(master = f2, textvariable = adj_x_cm, bg = "white")
lbl_adjx_value.grid(row = 2, column = 1)

lbl_adjx_scale = Label(master = f2, text = "cm", bg = "white")
lbl_adjx_scale.grid(row = 2, column = 2, sticky = W)

lbl_adjy_name = Label(master = f2, text = "Adjust y = ", bg = "white")
lbl_adjy_name.grid(row = 3, column = 0, sticky = E)

lbl_adjy_value = Label(master = f2, textvariable = adj_y_cm, bg = "white")
lbl_adjy_value.grid(row = 3, column = 1)

lbl_adjy_scale = Label(master = f2, text = "cm", bg = "white")
lbl_adjy_scale.grid(row = 3, column = 2, sticky = W)
           
###BINDINGS FOR KEYS/MOUSE

c.bind('<Button-1>', drawpoint) 

c.bind('<d>', delpoint)

c.bind('<Button-3>', drawbull)

c.bind('<b>', delbull)

c.bind('<m>', mpi_toggle)

################### reticle bindings ###########
################### obsolete now GUI controls implemented

#c.bind('<s>', drawcurs)
#c.bind('<q>', delcurs)

#c.bind('<Up>', cursup)
#c.bind('<Down>', cursdown)
#c.bind('<Left>', cursleft)
#c.bind('<Right>', cursright)
#c.bind('<l>', cursgrow)
#c.bind('<k>', cursshrink)

c.bind('<r>', checkr)

                                
    
root.mainloop()
