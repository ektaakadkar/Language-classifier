import pickle
import sys


""" This file predicts the language class for Decision tree and Adaboost algorithms. The algorithm is selected as per 
the input pickle file. 
predict_adaboost method : to predict Adaboost algorithm output 
predict_decisiontree method : to predict decision tree output
The output prints the language class 'en' or 'dt' to which the given input line belongs.
"""

class Node:
    __slots__ = 'value', 'true' , 'false','parent'

    def __init__(self,value,true=None,false=None,parent = None):
        self.value = value
        self.true = true
        self.false = false
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_link(self,node):
        if self.true == node:
            return 'True'
        elif self.false == node:
            return 'False'

class Tree:
    __slots__ = 'node','link'

    def __init__(self,node,node_true,node_false):
        self.node = node
        node.true = node_true
        node.false = node_false
        node_true.parent = node
        node_false.parent = node


""" Prediction for Adaboost : The input line belongs to class for which the respective weight is greater. The weight 
is obtained from the hypothesis_weight array given in the input pickle file.
Prediction for Decision Tree : The input line belongs to class stated in the leaf node by traversing the decision 
tree according to the given set of attributes.
"""


class prediction:
    __slots__ = 'attributes_list','class_list','root_node'
    def __init__(self,root_node):
        self.attributes_list = []
        self.class_list = []
        self.root_node = root_node

    def predict_adaboost(self):
        for y in range (len(self.attributes_list)):
            hypothesis = self.root_node[0]
            hypothesis_weight = self.root_node[1]
            total_english_weight = 0
            total_dutch_weight = 0
            for x in range(len(hypothesis)):
                hypothesis_attribute = hypothesis[x]
                hypothesis_attribute_weight = hypothesis_weight[x]
                real_attribute = self.attributes_list[y][hypothesis_attribute]
                if real_attribute == 'True':
                    total_english_weight = total_english_weight + hypothesis_attribute_weight
                elif real_attribute == 'False':
                    total_dutch_weight = total_dutch_weight + hypothesis_attribute_weight
            if (total_english_weight > total_dutch_weight ):
                print('en')
            elif (total_dutch_weight > total_english_weight):
                print('nl')
        # print(final_class)

    def predict_decisiontree(self,line,root_node):
            if (root_node.value == 'en' or root_node.value == 'nl'):
                ret = root_node.value
                self.class_list.append(ret)
                return
            else:
                link = self.attributes_list[line][root_node.value]
                if link == 'True':
                    self.predict_decisiontree(line,root_node.true)
                else:
                    self.predict_decisiontree(line,root_node.false)

    def contain_hyphen(self, array):
        booleanvalue = 'False'
        for x in array:
            if x.__contains__("-"):
                booleanvalue = 'True'
                break
        return booleanvalue

    def containenglishwords(self, array):
        booleanvalue = 'False'
        list = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yourself', 'he', 'him', 'his',
                'himself', 'she', 'her', 'herself', 'it', 'itself', 'they', 'them', 'their', 'themselves', 'what',
                'which', 'who', 'whom', ' this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
                'being', 'been',
                'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
                'or', 'because', 'as', 'until', 'while', 'of', 'at', 'for', 'with', 'after', 'below', 'from', 'there',
                'so', 'than',
                'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now']
        for x in array:
            if len(x) > 0 and list.__contains__(x):
                booleanvalue = 'True'
                break
        return booleanvalue

    def frequency_words(self, array):
        booleanvalue = 'True'
        counter = 0
        for x in array:
            if len(x) > 12:
                counter = counter + 1
            if counter > 1:
                booleanvalue = 'False'
                break
        return booleanvalue

    def apostrophe(self, array):
        booleanvalue = 'False'
        for x in array:
            if x.__contains__("'"):
                booleanvalue = 'True'
                break
        return booleanvalue

    def containIJ(self, array):
        booleanvalue = 'True'
        counter = 0
        list = ['aan', 'af', 'al', 'alles', 'als', 'altijd', 'andere', 'ben', 'bij', 'daar', 'dan', 'dat', 'der',
                'deze',
                'die', 'dit', 'doch', 'doen', 'door', 'dus', 'een', 'eens', 'en', 'er', 'ge', 'geen', 'geweest', 'haar',
                'heb', 'hebben', 'heeft', 'hem', 'hier', 'hij', 'hoe', 'hun', 'iemand', 'iets', 'ik',
                'ja', 'je',
                'kan', 'kon', 'kunnen', 'maar', 'me', 'meer', 'men', 'met', 'mij', 'mijn', 'moet', 'na', 'naar', 'niet',
                'niets',
                'nog', 'nu', 'om', 'omdat', 'ons', 'ook', 'op', 'reeds', 'te', 'tegen', 'toch', 'toen',
                'tot',
                'u', 'uit', 'uw', 'van', 'veel', 'voor', 'waren', 'wat', 'wel', 'werd', 'wezen', 'wie', 'wij', 'wil',
                'worden',
                'zal', 'ze', 'zei', 'zelf', 'zich', 'zij', 'zijn', 'zo', 'zonder', 'zou', 'ij']
        for x in array:
            if list.__contains__(x):
                booleanvalue = 'False'
                break
        return booleanvalue

    def ratio(self, array):
        booleanvalue = 'True'
        total_char = 0
        for x in array:
            total_char = total_char + len(x)
        ratio = total_char / (len(array))
        # print(array)
        if ratio > 6:
            booleanvalue = 'False'
        return booleanvalue

    def containhetde(self, array):
        booleanvalue = 'True'
        for x in array:
            if x == 'het' or x == 'de':
                booleanvalue = 'False'
        return booleanvalue

    def containz(self, array):
        booleanvalue = 'True'
        counter = 0
        for x in array:
            if x.__contains__("z"):
                counter = counter + 1
            if (counter > 0):
                booleanvalue = 'False'
                break
        return booleanvalue

    def englishpronouns(self, array):
        booleanvalue = 'False'
        list = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'who', 'me', 'him', 'her', 'it', 'us', 'you',
                'them', 'whom',
                'mine', 'yours', 'his', 'hers', 'ours', 'theirs', 'this', 'that', 'these', 'those']
        for x in array:
            if list.__contains__(x):
                booleanvalue = 'True'
                break
        return booleanvalue

    def dutchpronouns(self, array):
        booleanvalue = 'True'
        list = ['ik', 'jij', 'je', 'u', 'hij', 'zij', 'ze', 'wij', 'zij', 'mij', 'jou', 'uw', 'hem', 'haar', 'ons',
                'hen'
                'mijn', 'jouw', 'uw', 'zijn', 'haar', 'onze', 'hun', 'van mij', 'van jou', 'van u', 'van hem',
                'van haar', 'van ons', 'van hun']
        for x in array:
            if list.__contains__(x):
                booleanvalue = 'False'
                break
        return booleanvalue

    def initialize_class(self):
        file = open(sys.argv[2], encoding='utf8')
        line = file.readline()
        line = line.replace("\n", '')
        while line:
            attribute_array = []
            line = line.replace("\n", '')
            individual_char = line.split(" ")
            attribute1 = self.contain_hyphen(individual_char)
            attribute2 = self.containenglishwords(individual_char)
            attribute3 = self.frequency_words(individual_char)
            attribute4 = self.apostrophe(individual_char)
            attribute5 = self.containIJ(individual_char)
            attribute6 = self.ratio(individual_char)
            attribute7 = self.containhetde(individual_char)
            attribute8 = self.containz(individual_char)
            attribute9 = self.englishpronouns(individual_char)
            attribute10 = self.dutchpronouns(individual_char)
            attribute_array.append(attribute1)
            attribute_array.append(attribute2)
            attribute_array.append(attribute3)
            attribute_array.append(attribute4)
            attribute_array.append(attribute5)
            attribute_array.append(attribute6)
            attribute_array.append(attribute7)
            attribute_array.append(attribute8)
            attribute_array.append(attribute9)
            attribute_array.append(attribute10)
            self.attributes_list.append(attribute_array)
            line = file.readline()

if __name__ == '__main__':
    dbfile = open(sys.argv[1], 'rb')
    root_node = pickle.load(dbfile)
    # print(root_node)
    flag = root_node[0]
    if (flag == 0):
        root_node = root_node[1]
        object = prediction(root_node)
        object.initialize_class()
        final_list = []
        for line in range (len(object.attributes_list)):
            getclass = object.predict_decisiontree(line,root_node)
        for x in object.class_list:
            print(x)
        # print(object.class_list)
    elif (flag == 1):
        node = []
        node_list = root_node[1]
        node.append(node_list)
        node_list = root_node[2]
        node.append(node_list)
        object = prediction(node)
        object.initialize_class()
        object.predict_adaboost()