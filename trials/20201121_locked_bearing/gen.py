import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201121_locked_bearing/gen.py",'r').read())

name = "locked_bearing"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)


gap   = 0.1
r     = 7
r_in  = 4 + gap
r_out = 5 + gap
P     = 40

# Create a star shaped base by interleaving
# two cicles at different radius
lock_length=10
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
lock=Part.makePolygon(ps)
lock=Part.Face(lock)
lock=lock.extrude(Base.Vector(0,0,lock_length))
holder=Part.makeCylinder(r,lock_length)
holder=holder.cut(lock)
Part.show(holder)

