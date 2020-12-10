import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201205_flywheel/gen.py",'r').read())

name = "flywheel"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

# Main wheel
wheel_depth   = 8
ext_wheel_rad = 35
int_wheel_rad = 25
wheel_offset  = 2.5

ext_wheel=Part.makeCylinder(ext_wheel_rad, wheel_depth)
int_wheel=Part.makeCylinder(int_wheel_rad, wheel_depth)
wheel=ext_wheel.cut(int_wheel)
wheel.translate(Base.Vector(0,0,-wheel_offset))

# Prongs
prong_width=12
prong_depth=3
x=Part.makeBox(2*int_wheel_rad,prong_width,prong_depth)
x.translate(Base.Vector(-int_wheel_rad,-(prong_width/2),0))
wheel=Part.makeCompound([wheel,x])

y=Part.makeBox(2*int_wheel_rad,prong_width,prong_depth)
y.translate(Base.Vector(-int_wheel_rad,-(prong_width/2),0))
y.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
wheel=Part.makeCompound([wheel,y])

# Main wheel
stick_depth = 5
stick_rad   = 8

stick=Part.makeCylinder(stick_rad, stick_depth)
stick.translate(Base.Vector(0,0,prong_depth))
wheel=Part.makeCompound([wheel,stick])

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
star=star.extrude(Base.Vector(0,0,stick_depth+prong_depth))


# Cut out star
wheel=wheel.cut(star)

Part.show(wheel)

