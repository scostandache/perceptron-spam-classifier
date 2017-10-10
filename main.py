from DataSet import *
from Perceptron import *
from numpy import dot
import cProfile
import random
import multiprocessing as mp


if __name__ == "__main__":
    train_set = DataSet("datasets/spam_train.txt")
    test_set = DataSet("datasets/spam_test.txt")
    validate_set = DataSet("datasets/spam_validation.txt")

    perceptron = Perceptron(train_set, test_set, validate_set)
    perceptron.train(0.7)
    print "test results: ",perceptron.test(),"\n"
    print "validation results: ", perceptron.validate(),"\n"
    perceptron.best_and_worst(15)








