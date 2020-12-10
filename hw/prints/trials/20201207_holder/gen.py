import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201207_holder/gen.py",'r').read())

name = "holder"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)



############################################################
# Base
box_z = 12
box_y = 12
box_x = 21

base=Part.makeBox(box_x,box_y,box_z)
base.translate(Base.Vector(-6,-box_y/2,0))


############################################################
# notch
notch_z = 12
notch_y = 8.4
notch_x = 8

notch=Part.makeBox(notch_x,notch_y,notch_z)
notch.translate(Base.Vector(5,-notch_y/2,0))
base=base.cut(notch)
Part.show(base)


############################################################
# Create a star shaped base by interleaving
# two cicles at different radius

r_in  = 4
r_out = 5
N     = 40
length= 10

ps    = []
for i in range(0,N,2):
    a_out = (i*2*math.pi)/N
    x     = r_out*math.cos(a_out)
    y     = r_out*math.sin(a_out)
    ps.append(Base.Vector(x, y, 0))
    a_in  = ((i+1)*2*math.pi)/N
    x     = r_in*math.cos(a_in)
    y     = r_in*math.sin(a_in)
    ps.append(Base.Vector(x, y, 0))

a_out = (i*2*math.pi)/N
x     = r_out*math.cos(0)
y     = r_out*math.sin(0)
ps.append(Base.Vector(x, y, 0))

star=Part.makePolygon(ps)
star=Part.Face(star)
star=star.extrude(Base.Vector(0,0,length))
star.translate(Base.Vector(0,0,box_z))
Part.show(star)


