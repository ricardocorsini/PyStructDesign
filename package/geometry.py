import ezdxf


class Geometry:

    def __init__(self):
        pass
        
    def add_retangle(doc, pointFix, height, width, dxfattribs):

        msp = doc.modelspace()

        p1 = pointFix
        p2 = (pointFix[0] + height, pointFix[1])  # Canto inferior direito
        p3 = (pointFix[0] + height, pointFix[1] + width)  # Canto superior direito
        p4 = (pointFix[0], pointFix[1] + width)  # Canto superior esquerdo

        msp.add_line(p1, p2, dxfattribs)
        msp.add_line(p2, p3, dxfattribs)
        msp.add_line(p3, p4, dxfattribs)
        msp.add_line(p4, p1, dxfattribs)


