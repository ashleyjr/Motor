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

length      = 50
int_rad     = 2
ext_rad     = 2.8
disc_rad    = 5
disc_length = 4

int_shaft=Part.makeCylinder(int_rad,length)
ext_shaft=Part.makeCylinder(ext_rad,length)
shaft=ext_shaft.cut(int_shaft)

disc_top=Part.makeCylinder(disc_rad,disc_length)
disc_top=disc_top.cut(int_shaft)
disc_bot=disc_top.copy()
disc_bot.translate(Base.Vector(0,0,length))

solenoid=Part.makeCompound([disc_bot,shaft,disc_top])

int_shaft=Part.makeCylinder(int_rad,length)
solenoid=solenoid.cut(int_shaft)

Part.show(solenoid)

