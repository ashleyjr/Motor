import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201123_side/gen.py",'r').read())

name = "Side"

#Create new document
App.setActiveDocument(name)
App.closeDocument(name)
App.newDocument(name)
App.setActiveDocument(name)
App.ActiveDocument=App.getDocument(name)
Gui.ActiveDocument=Gui.getDocument(name)

TH          = 10.0    # Thickness

############################################################
# Star shapes to cut out
star_gap = 0.3
r_out = 5 + star_gap
r_in  = 4 + star_gap
P     = 40
ps    = []
for i in range(0,P,2):
    a_out = (i*2*math.pi)/P
    x = r_out*math.cos(a_out)
    y = r_out*math.sin(a_out)
    ps.append(Base.Vector(x, y, 0))
    a_in= ((i+1)*2*math.pi)/P
    x = r_in*math.cos(a_in)
    y = r_in*math.sin(a_in)
    ps.append(Base.Vector(x, y, 0))
x = r_out*math.cos(0)
y = r_out*math.sin(0)
ps.append(Base.Vector(x, y, 0))
star=Part.makePolygon(ps)
star=Part.Face(star)
star=star.extrude(Base.Vector(0,0,TH))


############################################################
# Create tri plate

tri_rad      = 60
tri_end_rad  = 11
tri_int_rad  = 21

# Create a prong
prong=Part.makeBox(tri_rad-tri_int_rad,2*tri_end_rad,TH)
prong.translate(Base.Vector(tri_int_rad,-tri_end_rad,0))
end=Part.makeCylinder(tri_end_rad, TH)
end.translate(Base.Vector(tri_rad+1,0,0)) # need to overlap to make solid part
prong=prong.cut(end)
end=Part.makeCylinder(tri_end_rad, TH)
end=end.cut(star)
end.translate(Base.Vector(tri_rad,0,0))
prong=Part.makeCompound([prong,end])

# Create 3
prs=[]
for i in [0,120,240]:
    prong_inst=prong.copy()
    prong_inst.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), i)
    prs.append(prong_inst)
tri=Part.makeCompound(prs)


# Centre bearing housing
bearing_rad=25
bearing=Part.makeCylinder(bearing_rad, TH)
tri=Part.makeCompound([tri,bearing])

# Cut out centre bearing
gap=0.4
rball=TH/2
centre_rad=15

cut_t=Part.makeTorus(centre_rad,rball+gap)
cut_t.translate(Base.Vector(0,0,rball))

tri=tri.cut(cut_t)


# Cut out the centre star
tri=tri.cut(star)

Part.show(tri)

############################################################
# Create ball bearings

Nballs=9
for i in range(Nballs):
    ball=Part.makeSphere(rball)
    a=(i*2*math.pi)/Nballs
    x=centre_rad*math.cos(a)
    y=centre_rad*math.sin(a)
    ball.translate(Base.Vector(x,y,TH/2))
    Part.show(ball)








