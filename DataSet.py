from Mail import *


class DataSet(object):
    # a class representing a data set, which will be loaded from a file

    def __init__(self, file):
        """

        :param file: path to file containing data;
               a row in file is of format: target_value(0 or 1) mail_content
        """

        # correspondence dict between word and mails
        # key - word; value - array of mails containing the word
        self.word_corresp = {}
        self.MAILS = []

        # load the mails into Mail objects, along with their target result
        with open(file, 'r') as f:
            for line in f:
                mail_instance = Mail(line.replace('\n', ''))
                for word in mail_instance.words:
                    if self.word_corresp.has_key(word):
                        self.word_corresp[word].add(mail_instance)
                    else:
                        self.word_corresp[word] = set([mail_instance])
                self.MAILS += [mail_instance]

        # remove the words which appear in fewer than 30 mails
        for word, mails in self.word_corresp.items():
            if len(mails) < 30:
                self.word_corresp.pop(word)

        # a sorted array will help with branch prediction, faster processing
        sorted_words = sorted(self.word_corresp)

        # create feature vectors for mails
        for mail in self.MAILS:
            # multiplying a bool with an int -> int
            # faster than int(bool)
            mail.feature_vector = [(word in mail.words) * 1 for word in sorted_words]
        self.weights_no = len(sorted_words)


    @property
    def mail_instances(self):
        # returns all mail objects in the dataset
        return self.MAILS

    @property
    def words(self):
        # returns the dictonary of mails and their corresponding mails
        return self.word_corresp
