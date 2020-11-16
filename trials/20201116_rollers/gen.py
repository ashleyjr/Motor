import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201116_rollers/gen.py",'r').read())

name = "Bearing"

#Create new document
#App.setActiveDocument(name)
#App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

TH    = 10.0    # Thickness
R     = 18      # Radius of bearing

NPins = 10      # Number of pin bearings
RPins = 5.4     # Radius of pins
CPins = 4       # Radius of pin cut out

RT    = 8
CT    = 6

RTR   = 12.2    # Radius of rotor
RTRH  = 11.2     # Radius of hole in rotor

HOR   = 24.8    # Radius of housing
HORH  = 23.8    # Radius of hole in housing

RRad  = 3.6

# Create a single pin
pin   = Part.makeCylinder(RPins, TH)
t_pin = Part.makeTorus(RT, CT)
t_pin.translate(Base.Vector(0,0,TH/2))
pin   = pin.cut(t_pin)

# Place the pins in a ring
for i in range(NPins):
    a=(i*2*math.pi)/NPins
    x=R*math.cos(a)
    y=R*math.sin(a)

    # Pin
    pin_inst=pin.copy()
    pin_inst.translate(Base.Vector(x,y,0))
    Part.show(pin_inst)

# Rotor
rotor     = Part.makeCylinder(RTR, TH)
rotor_hole= Part.makeCylinder(RTRH,TH)
rotor     = rotor.cut(rotor_hole)
Part.show(rotor)
# Rotor Runner
rotor_r  = Part.makeTorus(RTR-2.2, CT-0.4)
rotor_r.translate(Base.Vector(0,0,TH/2))
rotor_hole= Part.makeCylinder(RTRH,2*TH)
rotor_hole.translate(Base.Vector(0,0,-TH/2))
rotor_r  = rotor_r.cut(rotor_hole)
top   = Part.makeCylinder(2*HOR, TH)
top.translate(Base.Vector(0,0,TH))
rotor_r = rotor_r.cut(top)
bot   = Part.makeCylinder(2*HOR, TH)
bot.translate(Base.Vector(0,0,-TH))
rotor_r = rotor_r.cut(bot)
Part.show(rotor_r)

# Housing
house     = Part.makeCylinder(HOR, TH)
house_hole= Part.makeCylinder(HORH,TH)
house     = house.cut(house_hole)
Part.show(house)
# Housing Runner
house_r  = Part.makeTorus(HORH+2.2, CT-0.4)
house_r.translate(Base.Vector(0,0,TH/2))
house_r=house_r.cut(top)
house_r=house_r.cut(bot)
ringo=Part.makeCylinder(2*HOR, TH)
ringi=Part.makeCylinder(HOR, TH)
ring=ringo.cut(ringi)
house_r=house_r.cut(ring)
Part.show(house_r)

