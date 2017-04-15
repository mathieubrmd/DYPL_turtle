# coding=utf-8
'''
DYPL_turtle.py - Parse a turtsle code string and draw it with setPixel from Application class
Mathieu Bourmaud - 19941124-P335
Martin Porrès - 19940926-P170
'''

import re
import math

class DYPL_turtle:
    def __init__(self, application):
        self.application = application
        self.isDrawing = False
        self.x = 0
        self.y = 0
        self.angle = 0
        # quand TkTurtle crée un DYPL_turle, il lui passe la class Application en paramètre pour qu'on puisse avoir
        # accès à setPixel() via un application.setPixel(x, Y).


    # Quand on clique sur le bouton Run de la GUI, la fonction parseExp est appelée avec le code turtle passé
    # en paramètre sous forme de string

    # Les boutons Previous et Next de la GUI servent à executer les differentes parties du fichier turtle_code_file
    def parseExp(self, exp):
        # Permet de récup dans un tableau la différente série d'instruction
        expressions = exp.split('\n')

        # Il faut ensuite la parse pour savoir laquelle c'est
        print(expressions)

        # Il y a donc les 8 expressions + la possibilité d'avoir la boucle for (cas a part qu'on checkera a la fin)
        for exp in expressions:
            print("EXP:" + exp)
            # Methode qui va check les regex et les expressions et qui va call automatiquement la méthode associé
            # Return False si ça couille
            if self.matchFunction(exp) == False:
                # Quand ça chie. Faut voir ce qu'on doit faire, là actuellement ça continue le prog mais suffit de return pr que ça stop
                print("NIQUEZ VOS MERES")


    # Match avec les regex et call la fonction direct via la String :awesome:
    def matchFunction(self, exp):
        putRegex = "^put\(?[0-9]+. ,?[0-9]+. ,?[0-9]+\)"
        moveRegex = "^move\(?[0-9]+. ,?[0-9]+\)"
        turnCWRegex = "^turn cw\(?[0-9]+\)"
        turnCCWRegex = "^turn ccw\(?[0-9]+\)"

        if exp == "pen down":
            self.pen_down()
            return True

        if exp == "pen up":
            self.pen_up()
            return True

        if exp == "move forward":
            self.move_forward()
            return True

        if exp == "move backward":
            self.move_backward()
            return True

        if (bool(re.compile(putRegex).match(exp)) or
            bool(re.compile(moveRegex).match(exp)) or
            bool(re.compile(turnCWRegex).match(exp)) or
            bool(re.compile(turnCCWRegex).match(exp))):
            exp = exp.replace(' ', '')
            eval("self.{0}".format(exp))
            return True
        return False

    def set_angle(self, angle):
        if (angle < 0):
            self.angle = 360 - (angle % 360)
        else:
            self.angle = angle % 360

    def draw_dot(self):
        self.application.setPixel(int(self.x), int(self.y))

    def pen_down(self):
        self.isDrawing = True
        self.draw_dot()
        print("PEN DOWN")

    def pen_up(self):
        self.isDrawing = False
        print("PEN UP")

    def put(self, xpos, ypos, angle):
        self.x = xpos
        self.y = ypos
        self.angle = angle
        self.pen_down()
        print("PUT " + str(xpos) + " " + str(ypos) + " " + str(angle))

    def move_forward(self):
        self.x += math.cos(math.radians(self.angle))
        self.y += math.sin(math.radians(self.angle))
        if self.isDrawing:
            self.draw_dot()
        print("MOVE FORWARD")

    def move_backward(self):
        self.x -= math.cos(math.radians(self.angle))
        self.y -= math.sin(math.radians(self.angle))
        print("MOVE BACKWARD")

    def move(self, steps, angle):
        self.turncw(angle)
        for x in range(0, steps):
            self.move_forward()
        print("MOVE " + str(steps) + " " +  str(angle))

    def turncw(self, angle):
        self.set_angle(self.angle + angle)
        print("TURN CLOCKWISE " +  str(angle))

    def turnccw(self, angle):
        self.set_angle(self.angle - angle)
        print("TURN COUNTER CLOCKWISE " +  str(angle))