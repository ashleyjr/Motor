import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201117_grooves/gen.py",'r').read())

name = "Bearing"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

thickness           = 10
pin_rad             = 5.5
pin_torus_rad       = thickness / 8
bearing_npins       = 10
bearing_radius      = 23
rotor_radius        = 17.5
rotor_hole_radius   = 14
house_radius        = 32
house_hole_radius   = 28.5
gap                 = 0.4

# Pin component
level=Part.makeCylinder(2*pin_rad, thickness)

t1=Part.makeTorus(pin_rad, pin_torus_rad)
t2=t1.copy()
t3=t1.copy()
t4=t1.copy()
t5=t1.copy()

level.translate(Base.Vector(0,0,-thickness))
t1=t1.cut(level)

t2.translate(Base.Vector(0,0,4*pin_torus_rad))

t3.translate(Base.Vector(0,0,8*pin_torus_rad))
level.translate(Base.Vector(0,0,2*thickness))
t3=t3.cut(level)

c=Part.makeCylinder(pin_rad, thickness)
t4.translate(Base.Vector(0,0,2*pin_torus_rad))
c=c.cut(t4)
t5.translate(Base.Vector(0,0,6*pin_torus_rad))
c=c.cut(t5)

pin=Part.makeCompound([t1,t2,t3,c])

# Put pins in a circle
for i in range(bearing_npins):
    a=(i*2*math.pi)/bearing_npins
    x=bearing_radius*math.cos(a)
    y=bearing_radius*math.sin(a)

    # Pin
    pin_inst=pin.copy()
    pin_inst.translate(Base.Vector(x,y,0))
    Part.show(pin_inst)


# Rotor
rotor     = Part.makeCylinder(rotor_radius, thickness)
rotor_hole= Part.makeCylinder(rotor_hole_radius,thickness)
rotor     = rotor.cut(rotor_hole)

# Rotor runners
tr=Part.makeTorus(rotor_radius, pin_torus_rad+gap)
rotor=rotor.cut(tr)
tr.translate(Base.Vector(0,0,thickness/2))
rotor=rotor.cut(tr)
tr.translate(Base.Vector(0,0,thickness/2))
rotor=rotor.cut(tr)

t1=Part.makeTorus(rotor_radius, pin_torus_rad-gap)
t1.translate(Base.Vector(0,0,2*pin_torus_rad))

t2=Part.makeTorus(rotor_radius, pin_torus_rad-gap)
t2.translate(Base.Vector(0,0,6*pin_torus_rad))


rotor=Part.makeCompound([rotor,t1,t2])
Part.show(rotor)

# House
house     = Part.makeCylinder(house_radius, thickness)
house_hole= Part.makeCylinder(house_hole_radius,thickness)
house     = house.cut(house_hole)

# House runners
tr=Part.makeTorus(house_hole_radius, pin_torus_rad+gap)
house=house.cut(tr)
tr.translate(Base.Vector(0,0,thickness/2))
house=house.cut(tr)
tr.translate(Base.Vector(0,0,thickness/2))
house=house.cut(tr)

t1=Part.makeTorus(house_hole_radius, pin_torus_rad-gap)
t1.translate(Base.Vector(0,0,2*pin_torus_rad))

t2=Part.makeTorus(house_hole_radius, pin_torus_rad-gap)
t2.translate(Base.Vector(0,0,6*pin_torus_rad))


house=Part.makeCompound([house,t1,t2])

Part.show(house)





#bottom_level.translate(Base.Vector(0,0,-thickness))
#pin=pin.cut(bottom_level)
#top_level=Part.makeCylinder(2*pin_rad, thickness)
#top_level.translate(Base.Vector(0,0,thickness))
#pin=pin.cut(top_level)

#c=Part.makeCylinder(pin_rad, thickness)
#pin=Part.makeCompound([t1,t2,t3,c])
#t1=Part.makeTorus(pin_rad, pin_torus_rad)
#t1.translate(Base.Vector(0,0,3*pin_torus_rad))
#t2=Part.makeTorus(pin_rad, pin_torus_rad)
#t2.translate(Base.Vector(0,0,7*pin_torus_rad))
#pin=pin.cut(t1)
#pin=pin.cut(t2)


#Part.show(pin)

TH    = 10.0    # Thickness
R     = 18      # Radius of bearing

NPins = 10      # Number of pin bearings
RPins = 5.5     # Radius of pins
CPins = 4       # Radius of pin cut out

RT    = 7.8
CT    = 4.6

RTR   = 12.2    # Radius of rotor
RTRH  = 11.2     # Radius of hole in rotor

HOR   = 24.8    # Radius of housing
HORH  = 23.8    # Radius of hole in housing

RRad  = 3.6

# Create a single pin
#pin   = Part.makeCylinder(RPins, TH)
#t_pin = Part.makeTorus(RPins, CT)
#t_pin.translate(Base.Vector(0,0,TH/2))
#pin   = pin.cut(t_pin)
#
## Place the pins in a ring
#for i in range(NPins):
#    a=(i*2*math.pi)/NPins
#    x=R*math.cos(a)
#    y=R*math.sin(a)
#
#    # Pin
#    pin_inst=pin.copy()
#    pin_inst.translate(Base.Vector(x,y,0))
#    Part.show(pin_inst)
#
## Rotor
#rotor     = Part.makeCylinder(RTR, TH)
#rotor_hole= Part.makeCylinder(RTRH,TH)
#rotor     = rotor.cut(rotor_hole)
#Part.show(rotor)
## Rotor Runner
#rotor_r  = Part.makeTorus(RTR-2, CT-0.3)
#rotor_r.translate(Base.Vector(0,0,TH/2))
#rotor_hole= Part.makeCylinder(RTRH,2*TH)
#rotor_hole.translate(Base.Vector(0,0,-TH/2))
#rotor_r  = rotor_r.cut(rotor_hole)
#top   = Part.makeCylinder(2*HOR, TH)
#top.translate(Base.Vector(0,0,TH))
#rotor_r = rotor_r.cut(top)
#bot   = Part.makeCylinder(2*HOR, TH)
#bot.translate(Base.Vector(0,0,-TH))
#rotor_r = rotor_r.cut(bot)
#Part.show(rotor_r)
#
## Housing
#house     = Part.makeCylinder(HOR, TH)
#house_hole= Part.makeCylinder(HORH,TH)
#house     = house.cut(house_hole)
#Part.show(house)
## Housing Runner
#house_r  = Part.makeTorus(HORH+2, CT-0.3)
#house_r.translate(Base.Vector(0,0,TH/2))
#house_r=house_r.cut(top)
#house_r=house_r.cut(bot)
#ringo=Part.makeCylinder(2*HOR, TH)
#ringi=Part.makeCylinder(HOR, TH)
#ring=ringo.cut(ringi)
#house_r=house_r.cut(ring)
#Part.show(house_r)
#
