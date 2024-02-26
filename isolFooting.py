import ezdxf
from ezdxf.tools.standards import linetypes
from ezdxf.enums import TextEntityAlignment
from package.geometry import Geometry
from package.config import Settings

class Footing():
    
    footing_list = []
    
    def __init__(self, title, origin, cob, sideX, sideY, h0, h1, df, pX, pY, path):
       
        self.title = title
        self.origin = origin
        self.cob = cob
        self.sideX = sideX
        self.sideY = sideY
        self.h0 = h0
        self.h1 = h1
        self.df = df
        self.pX = pX
        self.pY = pY
        self.path = path

        Footing.footing_list.append(self)

    def __str__(self):
        return self.title
    

    def add_isolFooting(self):

        doc = ezdxf.new()
        msp = doc.modelspace()

        #Text

        doc.styles.new("Title", dxfattribs={"font" : "Arial.ttf"})
        doc.styles.new("Subtitle", dxfattribs={"font" : "Arial.ttf"})

       

        #linetypes

        for name, desc, pattern in Settings.my_line_types:
            if name not in doc.linetypes:
                doc.linetypes.add(
                    name=name,
                    pattern=pattern,
                    description=desc,
                )

        
        #Layers Creation
                
        doc.layers.new(name='STRUCT_FOOTING_0', dxfattribs={'color': 3})
        doc.layers.new(name='STRUCT_FOOTING_1', dxfattribs={'color': 3, 'linetype': 'DASHED_FOOTING'})
        doc.layers.new(name='STRUCT_FOOTING_2', dxfattribs={'color': 3, 'linetype': 'DOTTED'})
        doc.layers.new(name='STRUCT_FOOTING_3', dxfattribs={'color': 5})

        #Insertion of texts in the drawing
        
        msp.add_text(
                    self.title,
                    height=0.1,
                    dxfattribs={"style": "Title", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.40), align=TextEntityAlignment.LEFT)

        msp.add_text(
                    'PLANTA',
                    height=0.05,
                    dxfattribs={"style": "Subtitle", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.30), align=TextEntityAlignment.LEFT)

        msp.add_text(
                    str(round(self.sideX * 100, 0)) + ' x ' + str(round(self.sideY * 100, 0)),
                    height=0.05,
                    dxfattribs={"style": "Subtitle", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.20), align=TextEntityAlignment.LEFT)

        
        #Plant insertion

        Geometry.add_retangle(doc, self.origin, self.sideX, self.sideY, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        Geometry.add_retangle(doc, [self.origin[0] + ((self.sideX - self.pX) / 2), self.origin[1] + ((self.sideY - self.pY) / 2)], self.pX, self.pY, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        

        if self.h0 != self.h1:
            msp.add_line(self.origin, [self.origin[0] + ((self.sideX - self.pX) / 2), self.origin[1] + ((self.sideY - self.pY) / 2)], dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line([self.origin[0], self.origin[1] + self.sideY], [self.origin[0] + ((self.sideX - self.pX) / 2), self.origin[1] + ((self.sideY - self.pY) / 2) + self.pY], dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line([self.origin[0] + self.sideX, self.origin[0]], [self.origin[0] + ((self.sideX - self.pX) / 2) + self.pX, self.origin[1] + ((self.sideY - self.pY) / 2)], dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line([self.origin[0] + self.sideX, self.origin[1] + self.sideY], [self.origin[0] + ((self.sideX - self.pX) / 2) + self.pX, self.origin[1] + ((self.sideY - self.pY) / 2) + self.pY], dxfattribs={'layer': 'STRUCT_FOOTING_0',})

        #reinforcement in plan
            
        flapLength = self.h0 - 2 * self.cob
        
        msp.add_line([self.origin[0] + self.sideX + 0.1, self.origin[1] + self.cob], [self.origin[0] + self.sideX + 0.1 + flapLength, self.origin[1] + self.cob], dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line([self.origin[0] + self.sideX + 0.1, self.origin[1] + self.sideY - self.cob], [self.origin[0] + self.sideX + 0.1 + flapLength, self.origin[1] + self.sideY - self.cob], dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line([self.origin[0] + self.sideX + 0.1 + flapLength, self.origin[1] + self.cob], [self.origin[0] + self.sideX + 0.1 + flapLength, self.origin[1] + self.sideY - self.cob], dxfattribs={'layer': 'STRUCT_FOOTING_3',})   

        msp.add_text(
                    '11 N8 %%C 8.0 c/11 C=149',
                    height=0.05,
                    dxfattribs={"style": "Subtitle", 'color': 3, 'rotation': 90}
        ).set_placement((self.origin[0] + self.sideX + 0.1 + flapLength + 0.025, self.origin[1] + self.sideY / 2), align=TextEntityAlignment.TOP_CENTER)

        msp.add_text(
                    '234',
                    height=0.05,
                    dxfattribs={"style": "Subtitle", 'color': 3, 'rotation': 90}
        ).set_placement((self.origin[0] + self.sideX + 0.1 + flapLength -0.015, self.origin[1] + self.sideY / 2), align=TextEntityAlignment.BOTTOM_CENTER)



        msp.add_line([self.origin[0] + self.cob, self.origin[1] - 0.1], [self.origin[0] + self.cob, self.origin[1] - 0.1 - flapLength], dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line([self.origin[0] + self.sideX - self.cob, self.origin[1] - 0.1], [self.origin[0] + self.sideX - self.cob, self.origin[1] - 0.1 - flapLength], dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line([self.origin[0] + self.cob, self.origin[1] - 0.1 - flapLength], [self.origin[0] + self.sideX - self.cob, self.origin[1] - 0.1 - flapLength], dxfattribs={'layer': 'STRUCT_FOOTING_3',})


        #Foundation cut
            
        msp.add_text(
                    'CORTE',
                    height=0.06,
                    dxfattribs={"style": "Subtitle", 'color': 3}
        ).set_placement((self.origin[0] + self.sideX, self.origin[1] + self.sideY + 0.20), align=TextEntityAlignment.LEFT)
        

        path = './examples/' + self.path + '.dxf'
        doc.saveas(path)

    
    
    def list_footing():
        for footing in Footing.footing_list:
            print(footing)
        
        
#TESTES

#Cria Sapata     title, origin, cob, sideX, sideY, h0,   h1,   df,     pX, pY, path    
sapata1 = Footing('S1', [1, 1], 0.05 ,0.85, 1.10, 0.25, 0.40, 1.75, 0.14, 0.40, 'S1')
sapata2 = Footing('S2', [0, 0], 0.05 ,1.2, 1.2, 0.25, 0.40, 1.75, 0.40, 0.40, 'S2')

#Footing.list_footing()

#desenha sapata
sapata1.add_isolFooting()

