import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201201_crank_plate/gen.py",'r').read())

name = "crank_plate"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

ss=[]

length = 30
width  = 14
depth  = 3

############################################################
# Star shapes to cut out
star_gap = 0.4
r_out = 5 + star_gap
r_in  = 4 + star_gap
P     = 40
ps    = []
for i in range(0,P,2):
    a_out = (i*2*math.pi)/P
    x = r_out*math.cos(a_out)
    y = r_out*math.sin(a_out)
    ps.append(Base.Vector(x, y, 0))
    a_in= ((i+1)*2*math.pi)/P
    x = r_in*math.cos(a_in)
    y = r_in*math.sin(a_in)
    ps.append(Base.Vector(x, y, 0))
x = r_out*math.cos(0)
y = r_out*math.sin(0)
ps.append(Base.Vector(x, y, 0))
star=Part.makePolygon(ps)
star=Part.Face(star)
star=star.extrude(Base.Vector(0,0,depth))

############################################################
# Half circle for ends

int_rad = width/2
ext_rad = length
i=Part.makeCylinder(int_rad, depth)
e=Part.makeCylinder(ext_rad, depth)
h=e.cut(i)
b=Part.makeBox(2*length,2*length,depth)
b.translate(Base.Vector(0,-length,0))
h=h.cut(b)

############################################################
# Plate

plate  = Part.makeBox(length, width, depth)

star1=star.copy()
star1.translate(Base.Vector(7,7,0))
plate=plate.cut(star1)

star2=star.copy()
star2.translate(Base.Vector(23,7,0))
plate=plate.cut(star2)

h1=h.copy()
h1.translate(Base.Vector(width/2,width/2,0))
plate=plate.cut(h1)

h2=h.copy()
h2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
h2.translate(Base.Vector(length-(width/2),width/2,0))
plate=plate.cut(h2)

Part.show(plate)

