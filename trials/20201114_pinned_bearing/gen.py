import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201114_pinned_bearing/gen.py",'r').read())

name = "Bearing"

#Create new document
#App.setActiveDocument(name)
#App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

TH    = 10.0    # Thickness

NPins = 18      # Number of pin bearings
RPins = 2       # Radius of pins
RBall = 3.0     # Radius of balls
R     = 17.5    # Radius of bearing arrangement

RTR   = 15.2    # Radius of rotor
RTRH  = 13      # Radius of hole in rotor

HOR   = 22      # Radius of housing
HORH  = 19.8    # Radius of hole in housing

# Pin bearings and guide cut out
guide=Part.makeTorus(R,(RBall+GBall))
guide.translate(Base.Vector(0,0,TH/2))
for i in range(NPins):
    a=(i*2*math.pi)/NPins
    x=R*math.cos(a)
    y=R*math.sin(a)
    # Pins
    pin=Part.makeCylinder(RPins,TH)
    pin.translate(Base.Vector(x,y,0))
    Part.show(pin)
    # Balls
    ball=Part.makeSphere(RBall)
    ball.translate(Base.Vector(x,y,(TH/2)))
    Part.show(ball)

# Rotor
rotor     = Part.makeCylinder(RTR, TH)
rotor_hole= Part.makeCylinder(RTRH,TH)
rotor     = rotor.cut(rotor_hole)
rotor     = rotor.cut(guide)
Part.show(rotor)

# Housing
house     = Part.makeCylinder(HOR, TH)
house_hole= Part.makeCylinder(HORH,TH)
house     = house.cut(house_hole)
house     = house.cut(guide)
Part.show(house)

