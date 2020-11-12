import Part
import math
from FreeCAD import Base

# Run in Freecad
# exec(open("/Users/ashleyr/Desktop/motor/trials/20201112_bearing_gap/gen.py",'r').read())

for g in [0.25, 0.5, 0.75, 1]:

    name = "Bearing"+str(g).replace('.','')

    #Create new document
    App.newDocument(name)
    App.setActiveDocument(name)
    App.ActiveDocument=App.getDocument(name)
    Gui.ActiveDocument=Gui.getDocument(name)

    TH    = 10.0    # Thickness
    NBall = 10      # Number of balls
    RBall = 5.0     # Radius of balls
    GBall = g       # Gap between balls and torus
    R1    = 10.0    # Radius of inner ring hole
    R2    = 15.0    # Radius of inner ring
    R3    = 20.0    # Radious of outer ring

    # Bearings and guide cut
    CBall=((R3-R2)/2)+R2
    T1=Part.makeTorus(CBall,(RBall+GBall))
    T1.translate(Base.Vector(0,0,TH/2))
    for i in range(NBall):
      Ball=Part.makeSphere(RBall)
      Alpha=(i*2*math.pi)/NBall
      BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),TH/2)
      Ball.translate(BV)
      Part.show(Ball)

    # Wheel
    B1=Part.makeCylinder(R1,TH)
    B2=Part.makeCylinder(R2,TH)
    IR=B2.cut(B1)
    InnerRing=IR.cut(T1)
    Part.show(InnerRing)

    # Housing - Custom shape
    B3=Part.makeCylinder(R3,TH)
    ps = []
    ps.append(Base.Vector(-25, -25, 0))
    ps.append(Base.Vector( 25, -25, 0))
    ps.append(Base.Vector( 25,  25, 0))
    ps.append(Base.Vector(-25,  25, 0))
    ps.append(Base.Vector(-25, -25, 0))
    B4=Part.makePolygon(ps)
    B4=Part.Face(B4)
    B4=B4.extrude(Base.Vector(0,0,TH))
    OR=B4.cut(B3)
    OuterRing=OR.cut(T1)
    Part.show(OuterRing)


