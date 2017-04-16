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

    def parseExp(self, exp):
        expressions = exp.split('\n')
        index = 0;

        while index < len(expressions):
            exp = expressions[index]
            if self.matchFunction(exp) == False:
                if self.checkForLoop(exp, expressions[(index + 1) % len(expressions)], expressions[(index + 2) % len(expressions)]) == False:
                    return False
                index += 3
            else:
                index += 1

    def checkForLoop(self, exp, statement, end):
        forRegex = "^for X=?[0-9]+ to [0-9]+ do"
        forWithVarRegex = "^for var = ?[0-9]+ to [0-9]+ do"

        if bool(re.compile(forRegex).match(exp)) and end == "end":
            values = self.getForValues(exp, False)
            index = int(values[1])
            while index < int(values[3]):
                if self.matchFunction(statement) == False:
                    return False
                index += 1
        else:
            return False



    def getForValues(self, exp, withVar):
        res = exp.split(' ')

        if withVar == False:
            res[1] = res[1][2:]
        else:
            res[1] = res[1][6:]
        return res

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

    def pen_up(self):
        self.isDrawing = False

    def put(self, xpos, ypos, angle):
        self.x = xpos
        self.y = ypos
        self.angle = angle
        self.pen_down()

    def move_forward(self):
        self.x += math.cos(math.radians(self.angle))
        self.y += math.sin(math.radians(self.angle))
        if self.isDrawing:
            self.draw_dot()

    def move_backward(self):
        self.x -= math.cos(math.radians(self.angle))
        self.y -= math.sin(math.radians(self.angle))

    def move(self, steps, angle):
        self.turncw(angle)
        for x in range(0, steps):
            self.move_forward()

    def turncw(self, angle):
        self.set_angle(self.angle + angle)

    def turnccw(self, angle):
        self.set_angle(self.angle - angle)
