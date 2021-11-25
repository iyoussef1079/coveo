from typing import Literal
from game_interface import Answer, GameMessage, Question, TotemAnswer
import json
from math import sqrt


class Solver:
    def __init__(self):
        """
        This method should be use to initialize some variables you will need throughout the challenge.
        """
        self.i_debout = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.i_couche = [(0, 0), (1, 0), (2, 0), (3, 0)]
        self.l_debout = [(1, 0), (0, 0), (0, 1), (0, 2)]
        self.l_couche = [(0, 0), (0, 1), (1, 1), (2, 1)]
        self.l_renverse = [(2, 0), (2, 1), (1, 1), (1, 0)]
        self.j_couche = [(0, 1), (0, 0), (1, 0), (2, 0)]
        self.j_debout = [(0, 0), (1,0), (1, 1), (1, 2)]
        self.j_renverse = [(0, 0), (0, 1), (0, 2), (1, 2)]
        self.t_couche = [(0, 0), (1, 0), (2, 0), (1, 1)]
        self.t_debout = [(0, 0), (0, 1), (0, 2), (1, 1)]  # 2 orientations possibles
        self.t_renverse = [(0, 1), (1, 1), (2, 1), (1, 0)]
        self.s_debout = [(0, 1), (0, 2), (1, 1), (1, 0)]
        self.s_couche = [(0, 0), (1, 0), (1, 1), (2, 1)]
        self.z_couche = [(0, 1), (1, 1), (1, 0), (2, 0)]
        self.z_debout = [(0, 0), (0, 1), (1, 1), (1, 2)]
        self.o = [(0, 0), (1, 0), (1, 1), (0, 1)]

        

    def get_answer(self, game_message: GameMessage) -> Answer:
        """
        Here is where the magic happens, for now the answer is a single 'I'. I bet you can do better ;)
        """
        totems = []
        posX_init = 0
        posY_init = 0
        myCubeList = []
        pieceForCube = {"I":0, "J":0, "L":0, "O":0}
        otherShape = {"T":0, "Z":0, "S":0}
        questions = game_message.payload 
        print("Received Question:", questions)
        shapeList = questions.totems
        for shape in shapeList:
            if shape.shape == "I":
                pieceForCube["I"] += 1
            elif shape.shape == "J":
                pieceForCube["J"] += 1
            elif shape.shape == "L":
                pieceForCube["L"] += 1
            elif shape.shape == "T":
                otherShape["T"] += 1
            elif shape.shape == "S":
                otherShape["S"] += 1
            elif shape.shape == "Z":
                otherShape["Z"] += 1
            elif shape.shape == "O":
                pieceForCube["O"] += 1
            
        ## construire des carrés tant que c'est possible
        while(pieceForCube["I"] > 0 and pieceForCube["J"] > 0 and pieceForCube["L"] > 0 and pieceForCube["O"] > 0):
            i_perso = []
            o_perso = []
            l_perso = []
            j_perso = []
            monCarreOrigine = []
            for x, y in self.i_couche:
                i_perso.append((x, y + 3))
                
            for x, y in self.o:
                o_perso.append((x + 1, y + 1))
                
            for x, y in self.j_debout:
                j_perso.append((x + 2, y))
                
            for x, y in self.l_debout:
                l_perso.append((x , y))
                
            monCarreOrigine.append(("I", i_perso))
            monCarreOrigine.append(("O",o_perso))
            monCarreOrigine.append(("J",j_perso))
            monCarreOrigine.append(("L",l_perso))
            pieceForCube["I"] -= 1
            pieceForCube["O"] -= 1
            pieceForCube["J"] -= 1
            pieceForCube["L"] -= 1
            myCubeList.append(monCarreOrigine)
            

            ## MyCubeList = [carreOrigine, carreOrigine, carreOrigine..... ]
            ## carreOrigine = [("I", coord), ("J", coord),....]
        cote =  sqrt(len(myCubeList)) // 1
            
        for carre in myCubeList:
            indice = 0
            for piece in carre:
                if piece[0] == "I":
                    coord = []
                    for x, y in piece[1]:
                        coord.append((x + posX_init, y + posY_init ))
                    totems.append(TotemAnswer(shape="I", coordinates=coord))
                elif piece[0] == "J":
                    coord = [] # coordonées avec translation
                    for x, y in piece[1]:
                        coord.append((x + posX_init, y + posY_init ))
                    totems.append(TotemAnswer(shape="J", coordinates=coord))    
                elif piece[0] == "L":
                    coord = [] # coordonées avec translation
                    for x, y in piece[1]:
                        coord.append((x + posX_init, y + posY_init ))
                    totems.append(TotemAnswer(shape="L", coordinates=coord))
                elif piece[0] == "O":
                    coord = [] # coordonées avec translation
                    for x, y in piece[1]:
                        coord.append((x + posX_init, y + posY_init ))
                    totems.append(TotemAnswer(shape="O", coordinates=coord))
            indice += 1
            if indice % cote == 0:
                posX_init += 4
                posY_init = 0
            else:
                posY_init += 4


            
        if len(myCubeList) > 0:            
            posY_init = 0
            posX_init += 4
        for i in range(pieceForCube["I"]):
            coord = []
            for x, y in self.i_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="I", coordinates=coord))
            posY_init += 1
        for i in range(pieceForCube["O"]):
            coord = []
            for x, y in self.o:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="O", coordinates=coord))
            posY_init += 2
        for i in range(pieceForCube["J"]):
            coord = []
            for x, y in self.j_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="J", coordinates=coord))
            posY_init += 2
        for i in range(pieceForCube["L"]):
            coord = []
            for x, y in self.l_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="L", coordinates=coord))
            posY_init += 2
        for i in range(otherShape["T"]):
            coord = []
            for x, y in self.t_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="T", coordinates=coord))
            posY_init += 2
        for i in range(otherShape["S"]):
            coord = []
            for x, y in self.s_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="S", coordinates=coord))
            posY_init += 2
        for i in range(otherShape["Z"]):
            coord = []
            for x, y in self.z_couche:
                coord.append((x + posX_init, y + posY_init))
            totems.append(TotemAnswer(shape="Z", coordinates=coord))
            posY_init += 2

        answer = Answer(totems)
        print("Sending Answer:", answer)
        return answer
