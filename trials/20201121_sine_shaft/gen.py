import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201121_sine_shaft/gen.py",'r').read())

name = "sine_shaft"

#Create new document
#App.setActiveDocument(name)
#App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)


ss=[]

# The main shaft
length=100
disc_rad=5
A=10
N=500
step=length/N
for i in range(N):
    disc=Part.makeCylinder(disc_rad,step)
    t=(i*2*math.pi)/N
    x=A*math.sin(t)
    disc.translate(Base.Vector(x,0,i*step))
    ss.append(disc)

r_in  = 4
r_out = 5
P     = 40

off_rad  = 2
off1_pos = 7
off2_pos = -7


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
star=Part.makePolygon(ps)
star=Part.Face(star)
star=star.extrude(Base.Vector(0,0,lock_length))
star1=star.copy()
star1.translate(Base.Vector(0,0,-lock_length))
star2=star.copy()
star2.translate(Base.Vector(0,0,length))
ss.append(star1)
ss.append(star2)

shaft=Part.makeCompound(ss)
Part.show(shaft)

