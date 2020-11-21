import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201121_hoop/gen.py",'r').read())

name = "hoop"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)



stick_length = 20
stick_width  = 4
r_in  = 5.5
r_out = 7
thick = 3


ss=[]
ss.append(Base.Vector(stick_width/2,  0, 0))
ss.append(Base.Vector(stick_width/2,  stick_length, 0))
ss.append(Base.Vector(-stick_width/2, stick_length, 0))
ss.append(Base.Vector(-stick_width/2, 0, 0))
ss.append(Base.Vector(stick_width/2,  0, 0))
stick=Part.makePolygon(ss)
stick=Part.Face(stick)
stick=stick.extrude(Base.Vector(0,0,thick))

ring_i=Part.makeCylinder(r_in, thick)
ring_o=Part.makeCylinder(r_out,thick)
ring=ring_o.cut(ring_i)
stick=stick.cut(ring_i)

Part.show(ring)
Part.show(stick)

