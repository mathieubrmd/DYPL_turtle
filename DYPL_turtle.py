# coding=utf-8
'''
DYPL_turtle.py - Parse a turtle code string and draw it with setPixel from Application class
Mathieu Bourmaud - 19941124-P335
Martin Porrès - 19940926-P170
'''


class DYPL_turtle:
    def __init__(self, application):
        self.data = application
        # quand TkTurtle crée un DYPL_turle, il lui passe la class Application en paramètre pour qu'on puisse avoir
        # accès à setPixel() via un application.setPixel(x, Y).

    def parseExp(self, exp):
        print("Exp: " + exp)
        # Quand on clique sur le bouton Run de la GUI, la fonction parseExp est appelée avec le code turtle passé
        # en paramètre sous forme de string

        # Les boutons Previous et Next de la GUI servent à executer les differentes parties du fichier turtle_code_file
