import ezdxf
from ezdxf.tools.standards import linetypes
from ezdxf.enums import TextEntityAlignment
from package.config import Settings
import numpy as np

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

        doc.styles.new("Title_01", dxfattribs={"font" : "Arial.ttf"})
        doc.styles.new("Subtitle_01", dxfattribs={"font" : "Arial.ttf"})


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
        doc.layers.new(name='STRUCT_FOOTING_1', dxfattribs={'color': 3, 'linetype': 'DASHED'})
        doc.layers.new(name='STRUCT_FOOTING_2', dxfattribs={'color': 3, 'linetype': 'DOTTED'})
        doc.layers.new(name='STRUCT_FOOTING_3', dxfattribs={'color': 5})

        #Insertion of texts in the drawing
        
        msp.add_text(
                    self.title,
                    height=0.1,
                    dxfattribs={"style": "Title_01", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.40), align=TextEntityAlignment.LEFT)

        msp.add_text(
                    'PLANTA',
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.30), align=TextEntityAlignment.LEFT)

        msp.add_text(
                    str(round(self.sideX * 100, 0)) + ' x ' + str(round(self.sideY * 100, 0)),
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3}
        ).set_placement((self.origin[0], self.origin[1] + self.sideY + 0.20), align=TextEntityAlignment.LEFT)

        
        #Plant insertion
        
        #Fotting Points

        bottomLeftPoint_plant = np.array(self.origin)
        bottomRightPoint_plant = bottomLeftPoint_plant + np.array([self.sideX, 0])
        topRightPoint_plant = bottomRightPoint_plant + np.array([0, self.sideY])
        topLeftPoint_plant = topRightPoint_plant + np.array([-self.sideX, 0])
     
        msp.add_line(bottomLeftPoint_plant, bottomRightPoint_plant, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(bottomRightPoint_plant, topRightPoint_plant, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(topRightPoint_plant, topLeftPoint_plant, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(topLeftPoint_plant, bottomLeftPoint_plant, dxfattribs={'layer': 'STRUCT_FOOTING_0',})

        #Pillar Points

        bottomLeftPoint_plant_pillar = bottomLeftPoint_plant + np.array([(self.sideX / 2) - (self.pX / 2), (self.sideY / 2) - (self.pY / 2)])
        bottomRightPoint_plant_pillar = bottomLeftPoint_plant_pillar + np.array([self.pX, 0])
        topRightPoint_plant_pillar = bottomRightPoint_plant_pillar + np.array([0, self.pY])
        topLeftPoint_plant_pillar = topRightPoint_plant_pillar + np.array([- self.pX, 0])

        msp.add_line(bottomLeftPoint_plant_pillar, bottomRightPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(bottomRightPoint_plant_pillar, topRightPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(topRightPoint_plant_pillar, topLeftPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(topLeftPoint_plant_pillar, bottomLeftPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        
        #Chamfer

        if self.h0 != self.h1:
            msp.add_line(bottomLeftPoint_plant, bottomLeftPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line(bottomRightPoint_plant, bottomRightPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line(topRightPoint_plant, topRightPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
            msp.add_line(topLeftPoint_plant, topLeftPoint_plant_pillar, dxfattribs={'layer': 'STRUCT_FOOTING_0',})


        #reinforcement in plan
            
        flapLength = self.h0 - 2 * self.cob

        pointOneBottom_reinforced_90 = bottomRightPoint_plant + np.array([0.1, self.cob])
        pointTwoBottom_reinforced_90 = pointOneBottom_reinforced_90 + np.array([flapLength, 0])
        pointOneTop_reinforced_90 = pointOneBottom_reinforced_90 + np.array([0, self.sideY - 2 * self.cob])
        pointTwoTop_reinforced_90 = pointOneTop_reinforced_90 + np.array([flapLength, 0])
        
        msp.add_line(pointOneBottom_reinforced_90, pointTwoBottom_reinforced_90, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointTwoBottom_reinforced_90, pointTwoTop_reinforced_90, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointTwoTop_reinforced_90, pointOneTop_reinforced_90, dxfattribs={'layer': 'STRUCT_FOOTING_3',})   

        msp.add_text(
                    '11 N8 %%C 8.0 c/11 C=149',
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3, 'rotation': 90}
        ).set_placement((self.origin[0] + self.sideX + 0.1 + flapLength + 0.025, self.origin[1] + self.sideY / 2), align=TextEntityAlignment.TOP_CENTER)

        msp.add_text(
                    '234',
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3, 'rotation': 90}
        ).set_placement((self.origin[0] + self.sideX + 0.1 + flapLength -0.015, self.origin[1] + self.sideY / 2), align=TextEntityAlignment.BOTTOM_CENTER)


        pointOneTop_reinforced_0 = bottomLeftPoint_plant + np.array([self.cob, - 0.1])
        pointTwoTop_reinforced_0 = pointOneTop_reinforced_0 + np.array([self.sideX - 2 * self.cob, 0])
        pointOneBottom_reinforced_0 = pointOneTop_reinforced_0 + np.array([0, - flapLength])
        pointTwoBottom_reinforced_0 = pointTwoTop_reinforced_0 + np.array([0, - flapLength])

        msp.add_line(pointOneTop_reinforced_0, pointOneBottom_reinforced_0, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointTwoTop_reinforced_0, pointTwoBottom_reinforced_0, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointOneBottom_reinforced_0, pointTwoBottom_reinforced_0, dxfattribs={'layer': 'STRUCT_FOOTING_3',})

        msp.add_text(
                    '11 N8 %%C 8.0 c/11 C=149',
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3, 'rotation': 0}
        ).set_placement((bottomLeftPoint_plant[0] + (self.sideX / 2), pointOneBottom_reinforced_0[1] - 0.025), align=TextEntityAlignment.TOP_CENTER)

        msp.add_text(
                    '234',
                    height=0.05,
                    dxfattribs={"style": "Subtitle_01", 'color': 3, 'rotation': 0}
        ).set_placement((bottomLeftPoint_plant[0] + (self.sideX / 2), pointOneBottom_reinforced_0[1] + 0.015), align=TextEntityAlignment.BOTTOM_CENTER)


        #Foundation cut
            
        msp.add_text(
                    'CORTE',
                    height=0.06,
                    dxfattribs={"style": "Subtitle_01", 'color': 3}
        ).set_placement((topRightPoint_plant[0] + 2 * self.h0, topRightPoint_plant[1] + 0.2), align=TextEntityAlignment.LEFT)
        
        dottedLineTop_one = pointTwoTop_reinforced_90 + np.array([self.h0, self.cob])
        dottedLineTop_two = dottedLineTop_one + np.array([2 * self.h0 + self.sideX, 0])
        dottedLineBottom_one = dottedLineTop_one + np.array([0, - self.df])
        dottedLineBottom_two = dottedLineTop_two + np.array([0, - self.df])

        msp.add_line(dottedLineTop_one, dottedLineTop_two, dxfattribs={'layer': 'STRUCT_FOOTING_2',})
        msp.add_line(dottedLineBottom_one, dottedLineBottom_two, dxfattribs={'layer': 'STRUCT_FOOTING_2',})

        cutBottomPoint_one = dottedLineBottom_one + np.array([self.h0, 0])
        cutBottomPoint_two = cutBottomPoint_one + np.array([self.sideX, 0])
        cutTopPoint_one = cutBottomPoint_one + np.array([0, self.h0])
        cutTopPoint_two = cutBottomPoint_two + np.array([0, self.h0])
        
        cutPillarPoint_one = dottedLineTop_one + np.array([self.h0 + (self.sideX / 2) - (self.pX / 2), 0])
        cutPillarPoint_two = cutPillarPoint_one + np.array([self.pX, 0]) 

        cutH1Point_one = cutPillarPoint_one + np.array([0, - self.df + self.h1])
        cutH1Point_two = cutPillarPoint_two + np.array([0, - self.df + self.h1])

        msp.add_line(cutPillarPoint_one, cutPillarPoint_two, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutPillarPoint_one, cutH1Point_one, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutPillarPoint_two, cutH1Point_two, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutH1Point_one, cutTopPoint_one, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutH1Point_two, cutTopPoint_two, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutTopPoint_two, cutBottomPoint_two, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutTopPoint_one, cutBottomPoint_one, dxfattribs={'layer': 'STRUCT_FOOTING_0',})
        msp.add_line(cutBottomPoint_one, cutBottomPoint_two, dxfattribs={'layer': 'STRUCT_FOOTING_0',})

        #reinforcement in cut

        pointOneTop_reinforced_cut = cutBottomPoint_one + np.array([self.cob, self.cob + flapLength])
        pointTwoTop_reinforced_cut = pointOneTop_reinforced_cut + np.array([self.sideX - 2 * self.cob, 0])
        pointOneBottom_reinforced_cut = pointOneTop_reinforced_cut + np.array([0, - flapLength])
        pointTwoBottom_reinforced_cut = pointTwoTop_reinforced_cut + np.array([0, - flapLength])

        msp.add_line(pointOneTop_reinforced_cut, pointOneBottom_reinforced_cut, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointTwoTop_reinforced_cut, pointTwoBottom_reinforced_cut, dxfattribs={'layer': 'STRUCT_FOOTING_3',})
        msp.add_line(pointOneBottom_reinforced_cut, pointTwoBottom_reinforced_cut, dxfattribs={'layer': 'STRUCT_FOOTING_3',})



        path = './examples/' + self.path + '.dxf'
        doc.saveas(path)

    


    
    def list_footing():
        for footing in Footing.footing_list:
            print(footing)

    def volume(self):

        if self.h0 == self.h1:
            bottomVol = self.sideX * self.sideY * self.h0
            pillarVol = (self.df - self.h0) * self.pX * self.pY
            totalVol = bottomVol + pillarVol
        else:
            straightPartVol = self.sideX * self.sideY * self.h0 #Straigth Part Volume

            sB = self.sideX * self.sideY #larger base area
            sb = self.pX * self.pY #smaller base area
            heightPyrTrunk = self.h1 - self.h0 #height of pyramid trunk
            pyramidTrunk = (heightPyrTrunk / 3) * (sB + ((sB * sb) ** (1 / 2)) + sb)
            
            bottomVol = straightPartVol + pyramidTrunk
            pillarVol = (self.df - self.h1) * self.pX * self.pY
            totalVol = bottomVol + pillarVol

        return [round(bottomVol, 2), round(pillarVol, 2), round(totalVol, 2)]
    
    def formwork(self):

        side = 2 * (self.sideX * self.h0) + 2 * (self.sideY * self.h0)

        return side
        

        
#Testes e métodos desenvolvidos - roteiro para README.MD futuro.

#Cria Sapata      title, origin, cob, sideX, sideY, h0,   h1,   df,    pX, pY, path    
#Medidas em metro. 
sapata1 = Footing('S1', [1, 1], 0.05 ,0.85, 1.10, 0.25, 0.40, 1.75, 0.14, 0.40, 'S1')
sapata2 = Footing('S2', [0, 0], 0.05 ,1.8, 2.20,  0.25, 0.45, 1.50, 0.30, 0.60, 'S2')
sapata3 = Footing('S3', [0, 0], 0.045 ,2.15, 2.30,  0.30, 0.60, 2.20, 0.35, 0.50, 'S3')

#Lista todas as sapatas já criadas.
#Footing.list_footing() 

#Desenha a sapata
#sapata2.add_isolFooting() 

#Fornece uma lista [Volume da parte inferior (reta ou com chanfro), volume da parte do pilar, volume total]
print(sapata3.volume())

#Fornece o valor das fôrmas por m2. As fôrmas contabilizam somente a parte lateral. 
print(sapata3.formwork())

