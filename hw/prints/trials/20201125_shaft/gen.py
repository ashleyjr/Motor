import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201125_shaft/gen.py",'r').read())

name = "shaft"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)


ss=[]

# The main shaft
length=100
shaft_rad=5
shaft=Part.makeCylinder(disc_rad,length)
ss.append(shaft)

# Create a star shaped base by interleaving
# two cicles at different radius
r_in  = 4
r_out = 5
P     = 40
lock_length=9
ps    = []
for i in range(0,P,2):
    a_out = (i*2*math.pi)/P
    x     = r_out*math.cos(a_out)
    y     = r_out*math.sin(a_out)
    ps.append(Base.Vector(x, y, 0))
    a_in  = ((i+1)*2*math.pi)/P
    x     = r_in*math.cos(a_in)
    y     = r_in*math.sin(a_in)
    ps.append(Base.Vector(x, y, 0))
a_out = (i*2*math.pi)/N
x     = r_out*math.cos(0)
y     = r_out*math.sin(0)
ps.append(Base.Vector(x, y, 0))
star=Part.makePolygon(ps)
star=Part.Face(star)
star=star.extrude(Base.Vector(0,0,lock_length))
star1=star.copy()
star1.translate(Base.Vector(0,0,-lock_length))
star2=star.copy()
star2.translate(Base.Vector(0,0,length))
ss.append(star1)
ss.append(star2)


# Make
rise_length=length+(2*lock_length)+2
rise_rad=4
rise=Part.makeCylinder(rise_rad,rise_length)
rise.translate(Base.Vector(0,0,-(lock_length+1)))
ss.append(rise)




shaft=Part.makeCompound(ss)
Part.show(shaft)

