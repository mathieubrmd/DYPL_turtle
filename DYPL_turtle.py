# coding=utf-8
'''
DYPL_turtle.py - Parse a turtle code string and draw it with setPixel from Application class
Mathieu Bourmaud - 19941124-P335
Martin Porres - 19940926-P170
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

            # Match function compares the exp to the regex of the 8 functions
            if self.matchFunction(exp) == False:
                # Getting the return value, it can be either the position of the end statement or a False
                returnValue = self.checkForLoop(expressions, index)

                # Just checking if an error has append in the checkForLoop method
                if returnValue == False:
                    return False

                # Change the position of the loop so we don't evaluate the end statements or whatever
                index = returnValue + 1
            else:
                index += 1

    # Return the position of the end statement or False
    # Get the values of the for string and executes the statements
    def checkForLoop(self, expressions, index):
        # The position of the end statement
        endPos = self.getEndPos(expressions, index)

        # The for values X and To
        values = self.getForValues(expressions[index])

        # Something wrong happened
        if values == None:
            return False

        # Loop and executes statements
        x = int(values[0])
        while x != int(values[1]):
            # Loop between the for and the end statement so it executes all the statements between both instructions
            # y = the position of the next instruction after the for
            y = index + 1
            while y != endPos:
                exp = self.setValueInInstrution(expressions[y], values[2], x)
                if self.matchFunction(exp) == False:
                    return False
                y += 1
            x += 1
        return endPos

    # Set the value X or var or whatever in the string
    def setValueInInstrution(self, exp, var, val):
        # replace the x or v or var inside the instruction
        # we don't want the v of move for example to be replaced in the case that the var name is v
        # so the goal is to change the values inside the parenthesis
        exps = exp.split('(')
        exps[1] = exps[1].replace(var, str(val))
        exp = exps[0] + '(' + exps[1]
        return exp

    # Get the position of the end statement
    def getEndPos(self, expressions, index):
        while expressions[index] != "end":
            index += 1
        return index


    # Get the values of the for loop
    def getForValues(self, exp):
        res = exp.split(' ')
        values = [0, 0, 0]

        # The equal char : it means that it's the format X=NUMBER and not var = NUMBER
        try:
            if res[1][1] == "=":
                values[0] = res[1][2:]
                values[1] = res[3]
                values[2] = res[1][:1]
            else:
                values[0] = res[3]
                values[1] = res[5]
                values[2] = res[1]
            return values
        except:
            print("Error, the loop: " + exp + " is not valid.")
            return None

    def matchFunction(self, exp):
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

        try:
            eval("self.{0}".format(exp.strip()))
            return True
        except:
            print("Error, the expression: " + exp.strip() + " is either not valid or is a for loop.")
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
