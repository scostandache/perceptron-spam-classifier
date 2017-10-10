from Mail import *
import random
import numpy as np
import math

def work(foo):
    return foo.work()


class Perceptron(object):
    # class to represent the perceptron

    def __init__(self, train_set, test_set, validate_set):
        """
        
        :param train_set: training set
        """
        self.TRAINER = train_set
        self.TESTER = test_set
        self.VALIDATOR = validate_set
        self.WEIGHTS = [random.uniform(-3.0/math.sqrt(self.TRAINER.weights_no),
                                       3.0/math.sqrt(self.TRAINER.weights_no))
                                    for _ in xrange(self.TRAINER.weights_no)]

    def train(self, eta):
        """
        the perceptron training method,
        
        :param eta: the learning rate 
        :return: 
        """

        def sigmoid(t):
            return 1.0 / (1.0 + math.exp(-t))

        learning_rate = eta

        perceptron_trained = False

        correct_instances = 0
        while (perceptron_trained == False):
            correctly_classified = 0
            for mail in self.TRAINER.MAILS:

                mail.output = sigmoid(np.dot(self.WEIGHTS, mail.feature_vector))

                for idx, weight in enumerate(self.WEIGHTS):
                    self.WEIGHTS[idx] = self.WEIGHTS[idx] + \
                                        learning_rate * (mail.target - mail.output) * mail.feature_vector[idx]

                if abs(mail.target - mail.output) <= 0.05:
                    mail.correct_class = True
                    correctly_classified += 1

            print correctly_classified
            wrongly_classified = len(self.TRAINER.MAILS) - correctly_classified

            if learning_rate > 0.03:
                learning_rate -= 0.01
            print learning_rate

            if (wrongly_classified < 5):
                perceptron_trained = True
                correct_instances = correctly_classified

        # we know that the output is close enough to target
        # so we can set the output = target, to have discrete values
        for mail in self.TRAINER.MAILS:
            mail.output = mail.target

        with open('results/weights.txt', 'w+') as f:
            for weight in self.WEIGHTS:
                f.write(str(weight)+'\n')

        print (100.0 * correct_instances) / 4000.0

    def test(self):

        sorted_words = sorted(self.TRAINER.word_corresp)
        # create feature vectors for mails
        for mail in self.TESTER.MAILS:
            # bool * int = int
            # faster than int(bool)
            mail.feature_vector = [(word in mail.words) * 1 for word in sorted_words]
        self.weights_no = len(sorted_words)

        correctly_classified = 0

        def sigmoid(t):
            return 1.0 / (1.0 + math.exp(-t))

        for mail in self.TESTER.MAILS:
            mail.output = sigmoid(np.dot(self.WEIGHTS, mail.feature_vector))
            if abs(mail.target - mail.output) <= 0.1:
                correctly_classified += 1
        print correctly_classified

        return (100.0 * correctly_classified) / 1000.0

    def validate(self):

        sorted_words = sorted(self.TRAINER.word_corresp)
        # create feature vectors for mails
        for mail in self.VALIDATOR.MAILS:
            # multiplying a bool with an int -> int
            # faster than int(bool)
            mail.feature_vector = [(word in mail.words) * 1 for word in sorted_words]
        self.weights_no = len(sorted_words)

        correctly_classified = 0

        def sigmoid(t):
            return 1.0 / (1.0 + math.exp(-t))

        for mail in self.VALIDATOR.MAILS:
            mail.output = sigmoid(np.dot(self.WEIGHTS, mail.feature_vector))
            if abs(mail.target - mail.output) <= 0.1:
                correctly_classified += 1

        print correctly_classified

        return (100.0 * correctly_classified) / 1000.0

    def best_and_worst(self, n):

        class Word(object):
            pass

        sorted_words = sorted(self.TRAINER.word_corresp)
        WORDS = []
        for word, weight in zip(sorted_words, self.WEIGHTS):
            word_instance = Word()
            word_instance.value = word
            word_instance.weight = weight
            WORDS.append(word_instance)

        WORDS = sorted(WORDS, key=lambda x: x.weight, reverse=True)

        with open ('results/words.txt','w+') as f:


            f.write("most influencing words: \n")
            for word in WORDS[:n]:
                f.write(word.value +'\n')

            f.write("\n")

            f.write("most unuseful words: \n")

            for word in WORDS[-n:]:
                f.write(word.value + '\n')
