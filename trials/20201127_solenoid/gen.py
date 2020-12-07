import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201127_solenoid/gen.py",'r').read())

name = "solenoid"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

length      = 22
int_rad     = 2
ext_rad     = 2.8
disc_rad    = 6
disc_length = 4

int_shaft=Part.makeCylinder(int_rad,length)
ext_shaft=Part.makeCylinder(ext_rad,length)
shaft=ext_shaft.cut(int_shaft)
shaft.translate(Base.Vector(0,0,1))


disc_top=Part.makeCylinder(disc_rad,disc_length)
disc_top=disc_top.cut(int_shaft)
disc_bot=disc_top.copy()
disc_bot.translate(Base.Vector(0,0,length))


solenoid=Part.makeCompound([disc_bot,shaft,disc_top])

# Cut internal
int_shaft=Part.makeCylinder(int_rad,length)
solenoid=solenoid.cut(int_shaft)

# Cut fillet for discs
t_rad = disc_rad - ext_rad
fillet=Part.makeTorus(disc_rad,t_rad)

fillet.translate(Base.Vector(0,0,disc_length))
solenoid=solenoid.cut(fillet)

fillet.translate(Base.Vector(0,0,length-disc_length))
solenoid=solenoid.cut(fillet)

# Cut slots
slot_width=1
slot_offset=4
slot=Part.makeBox(disc_rad,slot_width,length)
slot.translate(Base.Vector(slot_offset,-slot_width/2,0))
for i in [20,340,160,200]:
    slot_inst=slot.copy()
    slot_inst.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), i)
    solenoid=solenoid.cut(slot_inst)

# Drill grip
grip_length = 8
grip_width  = 6
grip = Part.makeBox(grip_width,grip_width,grip_length)
grip.translate(Base.Vector(-grip_width/2,-grip_width/2,0))
grip=grip.cut(int_shaft)
grip.translate(Base.Vector(0,0,length+disc_length))
solenoid=Part.makeCompound([solenoid,grip])

# Cut edges
edge_size = disc_rad * 2
edge = Part.makeBox(edge_size,edge_size,edge_size)
edge.translate(Base.Vector(3,-edge_size/2,length))
solenoid=solenoid.cut(edge)
edge.translate(Base.Vector(-6-edge_size,0,0))
solenoid=solenoid.cut(edge)



Part.show(solenoid)

