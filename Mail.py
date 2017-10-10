import numpy as np


class Mail(object):
    # class representing a mail instance
    def __init__(self, line):
        self.target = float(line[0])
        self.output = 0.0
        self.feature_vector = []
        self.content = line[2:]
        self.words = set(self.content.split(" "))
        self.correct_class = False
