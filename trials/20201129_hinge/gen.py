import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201129_hinge/gen.py",'r').read())

name = "hinge"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)



# Shaft holder
shaft_ext_rad = 7
shaft_int_rad = 5.6
shaft_len     = 14
shaft_ext=Part.makeCylinder(shaft_ext_rad,shaft_len)
shaft_int=Part.makeCylinder(shaft_int_rad,shaft_len)
shaft=shaft_ext.cut(shaft_int)

# Shaft holder cut
shaft_cut_rad = 6
shaft_cut=Part.makeCylinder(shaft_cut_rad,2*shaft_ext_rad)
shaft_cut.rotate(Base.Vector(0, 0, 0),Base.Vector(1,0, 0), 90)
shaft_cut.translate(Base.Vector(-shaft_ext_rad,shaft_ext_rad,shaft_len/2))
shaft=shaft.cut(shaft_cut)


# Shaft holder fins
sfins_cut_len = shaft_len / 5
sfins_cut_x   = 9.6
sfins_y       = 9
sfins_x       = 11
sfins=Part.makeBox(sfins_x,sfins_y,shaft_len)
sfins.translate(Base.Vector(shaft_int_rad,-(sfins_y/2),0))
sfins_cut=Part.makeBox(sfins_x,sfins_y,sfins_cut_len)
sfins_cut.translate(Base.Vector(shaft_int_rad+sfins_x-sfins_cut_x,-(sfins_y/2),sfins_cut_len))
sfins=sfins.cut(sfins_cut)
sfins_cut.translate(Base.Vector(0,0,2*sfins_cut_len))
sfins=sfins.cut(sfins_cut)


# Pin
pin_rad = 2
pin_pos = 11.4
pin=Part.makeCylinder(pin_rad,shaft_len)
pin.translate(Base.Vector(pin_pos,0,0))

# Piston holder fins
pfins_cut_len = 3.6
pfins_cut_x   = 10
pfins_y       = 8
pfins_x       = 10
pfins_pos_x   = 7.4
pfins_rad     = 2.4
ppins_pos_x   = pin_pos
pfins=Part.makeBox(pfins_x,pfins_y,shaft_len)
pfins.translate(Base.Vector(pfins_pos_x,-(pfins_y/2),0))

pfins_cut=Part.makeBox(pfins_cut_x,pfins_y,pfins_cut_len)
pfins_cut.translate(Base.Vector(pfins_pos_x,-(pfins_y/2),0))

pfins_cut_1=pfins_cut.copy()
pfins_cut_1.translate(Base.Vector(0,0,-0.3))
pfins=pfins.cut(pfins_cut_1)

pfins_cut_2=pfins_cut.copy()
pfins_cut_2.translate(Base.Vector(0,0,(shaft_len/2)-(pfins_cut_len/2)))
pfins=pfins.cut(pfins_cut_2)

pfins_cut_3=pfins_cut.copy()
pfins_cut_3.translate(Base.Vector(0,0,shaft_len-pfins_cut_len+0.3))
pfins=pfins.cut(pfins_cut_3)

ppin=Part.makeCylinder(pfins_rad,shaft_len)
ppin.translate(Base.Vector(ppins_pos_x,0,0))
pfins=pfins.cut(ppin)

# Cut half curcle
phalf_ext=Part.makeCylinder((pfins_y/2)+5,shaft_len)
phalf_int=Part.makeCylinder(pfins_y/2,shaft_len)
phalf=phalf_ext.cut(phalf_int)

phalf_cut=Part.makeBox(pfins_y,pfins_y,shaft_len)
phalf_cut.translate(Base.Vector(0,-pfins_y/2,0))
phalf=phalf.cut(phalf_cut)

shalf=phalf.copy()
shalf.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)

phalf.translate(Base.Vector(ppins_pos_x,0,0))
pfins=pfins.cut(phalf)

shalf.translate(Base.Vector(ppins_pos_x,0,0))
sfins=sfins.cut(shalf)

# Piston holder
piston_ext_rad = 7
piston_int_rad = 1.9
piston_len     = 10
piston_base_len = 2
piston_gap = 1.5
piston_ext=Part.makeCylinder(piston_ext_rad,piston_len)
piston_int=Part.makeCylinder(piston_int_rad,piston_len)
piston=piston_ext.cut(piston_int)
piston.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
piston.translate(Base.Vector(pfins_x+pfins_pos_x-piston_gap,0,shaft_len/2))
piston_base=Part.makeCylinder(piston_ext_rad,piston_base_len)
piston_base.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
piston_base.translate(Base.Vector(pfins_x+pfins_pos_x-piston_gap,0,shaft_len/2))





hinge=Part.makeCompound([shaft,sfins,pin,pfins,piston,piston_base])
Part.show(hinge)

