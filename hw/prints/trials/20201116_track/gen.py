import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201115_hourglass_cups/gen.py",'r').read())

name = "Bearing"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

TH    = 10.0    # Thickness

NPins = 10      # Number of pin bearings
RPins = 3.2     # Radius of pins
HPins = 2       # Radius of pin hollow
RBall = 5.0     # Radius of balls
GTorus= 0.4
R     = 17.5    # Radius of bearing arrangement

RTR   = 13.9    # Radius of rotor
RTRH  = 10      # Radius of hole in rotor

HOR   = 25      # Radius of housing
HORH  = 21.1    # Radius of hole in housing

# Pin bearings and guide cut out
guide_top_o    = Part.makeCylinder(HORH+1.9,2.4)
guide_top_i    = Part.makeCylinder(RTR-1.9,2.4)
guide_top      = guide_top_o.cut(guide_top_i)
guide_top.translate(Base.Vector(0,0,TH-2.4))

guide_bottom_o = Part.makeCylinder(HORH+1.9,2.4)
guide_bottom_i = Part.makeCylinder(RTR-1.9,2.4)
guide_bottom   = guide_bottom_o.cut(guide_bottom_i)
guide_bottom.translate(Base.Vector(0,0,0))

for i in range(NPins):
    a=(i*2*math.pi)/NPins
    x=R*math.cos(a)
    y=R*math.sin(a)

    # Plate 1
    ball1=Part.makeCylinder(RBall, 2)
    ball1.translate(Base.Vector(x,y,0))
    Part.show(ball1)

    # Plate 2
    ball2=Part.makeCylinder(RBall, 2)
    ball2.translate(Base.Vector(x,y,TH-2))
    Part.show(ball2)

    # Pin
    pin=Part.makeCylinder(RPins, TH)
    pin.translate(Base.Vector(x,y,0))
    Part.show(pin)



# Rotor
rotor     = Part.makeCylinder(RTR, TH)
rotor_hole= Part.makeCylinder(RTRH,TH)
rotor     = rotor.cut(rotor_hole)
rotor     = rotor.cut(guide_top)
rotor     = rotor.cut(guide_bottom)
Part.show(rotor)

# Housing
house     = Part.makeCylinder(HOR, TH)
house_hole= Part.makeCylinder(HORH,TH)
house     = house.cut(house_hole)
house     = house.cut(guide_top)
house     = house.cut(guide_bottom)
Part.show(house)

