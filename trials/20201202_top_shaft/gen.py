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
sb_ext_rad    = 8.5
sb_int_rad    = 6.4
sb_base_depth = 2
sb_hole_rad   = 1.5
sb_hole_pairs = 4
sb_hole_z     = 2.9
sb_bot_rad    = 5.5

sb_ext=Part.makeCylinder(sb_ext_rad, sb_length)
sb_int=Part.makeCylinder(sb_int_rad, sb_length-sb_base_depth)
sb_int.translate(Base.Vector(0,0,sb_base_depth))
sb=sb_ext.cut(sb_int)

holes=Part.makeCylinder(sb_hole_rad, (sb_ext_rad*2))
holes.translate(Base.Vector(0,0,(-sb_ext_rad)))
holes.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)

holes.translate(Base.Vector(0,0,0.6))
for i in range(4):
    holes.translate(Base.Vector(0,0,sb_hole_z))
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),-20)
    sb = sb.cut(holes)
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),40)
    sb = sb.cut(holes)
    holes.translate(Base.Vector(0,0,sb_hole_z))
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),-20)
    sb = sb.cut(holes)
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),-40)
    sb = sb.cut(holes)
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),80)
    sb = sb.cut(holes)
    sb.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1),-40)


sb_bot=Part.makeCylinder(sb_bot_rad, sb_base_depth)
sb=sb.cut(sb_bot)

############################################################
# Two baskets

sb_sep = 48

sb_l=sb.copy()
sb_r=sb.copy()
sb_r.translate(Base.Vector(sb_sep,0,0))


Part.show(sb_l)
Part.show(sb_r)

############################################################
# Bridge between

br_depth  = 20
br_length = sb_sep - (sb_int_rad*2)
br_width  = 8
br_rad    = br_length / 2
br_arch_z = 5

bridge= Part.makeBox(br_length, br_width, br_depth)
bridge.translate(Base.Vector(sb_int_rad,-(br_width/2),sb_length-br_depth))

arch=Part.makeCylinder(br_rad, br_width)
arch.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
arch.translate(Base.Vector(sb_sep/2,(br_width/2),br_arch_z))
bridge=bridge.cut(arch)
Part.show(bridge)

############################################################
# Left end

l_depth  = 20
l_length = 20
l_width  = 8
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

r_depth  = 20
r_length = 20
r_width  = 8
r_rad    = 30
r_arch_z = -5
r_centre = 78

right= Part.makeBox(r_length, r_width, r_depth)
right.translate(Base.Vector(sb_sep+sb_int_rad,-(br_width/2),sb_length-r_depth))

r_arch=Part.makeCylinder(r_rad, r_width)
r_arch.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
r_arch.translate(Base.Vector(r_centre,(br_width/2),r_arch_z))
right=right.cut(r_arch)

Part.show(right)


############################################################
# Top holders


holder_x = 20
holder_y = 3
holder_z = 2

holder_ext_cut=Part.makeCylinder(2*sb_ext_rad, 2*sb_length)
holder_int_cut=Part.makeCylinder(sb_ext_rad, 2*sb_length)
holder_cut = holder_ext_cut.cut(holder_int_cut)


right_back= Part.makeBox(holder_x, holder_y, holder_z)
right_back.translate(Base.Vector(-holder_x/2,5.5,sb_length-holder_z))
right_back = right_back.cut(holder_cut)
Part.show(right_back)

right_front= Part.makeBox(holder_x, holder_y, holder_z)
right_front.translate(Base.Vector(-holder_x/2,-8.5,sb_length-holder_z))
right_front = right_front.cut(holder_cut)
Part.show(right_front)

holder_cut.translate(Base.Vector(sb_sep,0,0))

left_back= Part.makeBox(holder_x, holder_y, holder_z)
left_back.translate(Base.Vector(sb_sep+(-holder_x/2),5.5,sb_length-holder_z))
left_back = left_back.cut(holder_cut)
Part.show(left_back)


left_front= Part.makeBox(holder_x, holder_y, holder_z)
left_front.translate(Base.Vector(sb_sep+(-holder_x/2),-8.5,sb_length-holder_z))
left_front = left_front.cut(holder_cut)
Part.show(left_front)


