import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201202_top_shaft/gen.py",'r').read())

name = "top_shaft"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)



############################################################
# Solenoid bucket
sb_length     = 30
sb_ext_rad    = 10
sb_int_rad    = 9
sb_base_depth = 1
sb_hole_rad   = 1.5
sb_hole_pairs = 8
sb_hole_z     = 5
sb_bot_rad    = 7

sb_ext=Part.makeCylinder(sb_ext_rad, sb_length)
sb_int=Part.makeCylinder(sb_int_rad, sb_length-sb_base_depth)
sb_int.translate(Base.Vector(0,0,sb_base_depth))
sb=sb_ext.cut(sb_int)

holes=Part.makeCylinder(sb_hole_rad, (sb_ext_rad*2))
holes.translate(Base.Vector(0,0,(-sb_ext_rad)))
holes.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)

holes.translate(Base.Vector(0,0,sb_base_depth))
for i in range(int(sb_length/sb_hole_z)):
    holes.translate(Base.Vector(0,0,sb_hole_z))
    for j in range(sb_hole_pairs):
        sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), (180*j)/sb_hole_pairs)
        sb = sb.cut(holes)


sb_bot=Part.makeCylinder(sb_bot_rad, sb_base_depth)
sb=sb.cut(sb_bot)

############################################################
# Two baskets

sb_sep = 40

sb_l=sb.copy()
sb_r=sb.copy()
sb_r.translate(Base.Vector(sb_sep,0,0))


Part.show(sb_l)
Part.show(sb_r)

############################################################
# Bridge between

br_depth  = 15
br_length = sb_sep - (sb_int_rad*2)
br_width  = 5
br_rad    = br_length / 2
br_arch_z = 12

bridge= Part.makeBox(br_length, br_width, br_depth)
bridge.translate(Base.Vector(sb_int_rad,-(br_width/2),sb_length-br_depth))

arch=Part.makeCylinder(br_rad, br_width)
arch.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
arch.translate(Base.Vector(sb_sep/2,(br_width/2),br_arch_z))
bridge=bridge.cut(arch)
Part.show(bridge)

############################################################
# Left end

l_depth  = 15
l_length = 20
l_width  = 5
l_rad    = 30
l_arch_z = -5
l_centre = -30
left= Part.makeBox(l_length, l_width, l_depth)
left.translate(Base.Vector(-sb_int_rad-l_length,-(br_width/2),sb_length-l_depth))

l_arch=Part.makeCylinder(l_rad, l_width)
l_arch.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
l_arch.translate(Base.Vector(l_centre,(br_width/2),l_arch_z))
left=left.cut(l_arch)


Part.show(left)


############################################################
# Right end

r_depth  = 15
r_length = 20
r_width  = 5
r_rad    = 30
r_arch_z = -5
r_centre = 70

right= Part.makeBox(r_length, r_width, r_depth)
right.translate(Base.Vector(sb_sep+sb_int_rad,-(br_width/2),sb_length-r_depth))

r_arch=Part.makeCylinder(r_rad, r_width)
r_arch.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
r_arch.translate(Base.Vector(r_centre,(br_width/2),r_arch_z))
right=right.cut(r_arch)

Part.show(right)





