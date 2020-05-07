import pickle
import sys
import pandas
import math
""" Decision Tree and Adaboost algrithm are built to classify the given input file into Dutch and English language
line by line. This is the training code. There are 10 attributes on which the algorithms are trained. 
Command line arguments : train.py input_file output_file type_of_algorithm
Here, input_file : The file which will contain the training data
      output_file : For Decision tree - pickle file where the tree is stored.
                    For Adaboost algorithm - pickle file where array consisting of hypothesis and hypothesis weight 
                    is stored.
      type_of_algorithm : For Decision tree : input is "dt"
                          For Adaboost algorithm : input is "ada" 
The decision tree algorithm uses array-list to store the input data.
Adaboost algorithm uses pandas dataframe to store the input data. 
"""

class Node:

    __slots__ = 'value', 'true', 'false', 'parent'

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

    __slots__ = 'node', 'link'

    def __init__(self,node,node_true,node_false):
        self.node = node
        node.true = node_true
        node.false = node_false
        node_true.parent = node
        node_false.parent = node


""" The decision tree and adaboost algorithm are built using 10 attributes. The attributes have two values : 'True' and 
'False'. The attribute with highest information gain is selected as that current node value. The information gain is 
calculated on the basis of entropy. The parent nodes of the current attribute node are stored in dictionary called as
'nodes' which are used to give constraints while calculating the true and false count further used to calculate the 
entropy.
first_level method is used to find the root node.
second_level_true is used to find the true node for the current parent node.
second_level_false is used to find the false node for the current parent node. 
parameters : 'attributes_list' : array list containing the attribute values either 'True' or 'False'.
             'class_list' : array list containing the class 'en' or 'nl' for the particular line.
             'root_attribute' : root node of the decision tree
"""


class Decision_Tree_Build:

    __slots__ = 'attributes_list','class_list','root_attribute'

    def __init__(self):
        self.attributes_list = []
        self.class_list = []

    def calculate_maximum_number(self, array):
        index_of_maximum_number = 0
        maximum_number = array[0]
        for index in range(1, len(array)):
            if maximum_number < array[index]:
                maximum_number = array[index]
                index_of_maximum_number = index
        return index_of_maximum_number

    def calculate_entropy(self, first_number, second_number):
        if (first_number == 0 or second_number == 0):
            return 0
        total_sum = first_number + second_number
        first_term = first_number / total_sum
        second_term = second_number / total_sum
        entropy = - (first_term * math.log(first_term, 2)) - (second_term * math.log(second_term, 2))
        return entropy

    def second_level_true(self,node,flag2):
        information_gain_list = []
        nodes = {}
        main_en = 0
        main_nl = 0
        true_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        true_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        copy_node = node
        parent = copy_node.get_parent()
        counter = 0
        while parent is not None:
            link_boolean = parent.get_link(copy_node)
            nodes[parent.value] = link_boolean
            counter =counter + 1
            temp_parent = parent.get_parent()
            copy_node = parent
            parent = temp_parent
        for line in range(len(self.attributes_list)):
            flag = 0
            if len(nodes) == 0:
                if (self.attributes_list[line][self.root_attribute.value]) == 'True':
                    flag = 1
            else:
                list_of_nodes = nodes.keys()
                for x in list_of_nodes:
                    if self.attributes_list[line][x] == nodes.get(x) and self.attributes_list[line][node.value] == 'True':
                        flag = 1
                    else:
                        flag = 0
                        break
            if flag == 1:
                for x in range(len(self.attributes_list[line])):
                    if self.attributes_list[line][x] == 'True' and self.class_list[line] == 'en':
                        true_count_en[x] = true_count_en[x] + 1
                    elif self.attributes_list[line][x] == 'True' and self.class_list[line] == 'nl':
                        true_count_nl[x] = true_count_nl[x] + 1
                    elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'en':
                        false_count_en[x] = false_count_en[x] + 1
                    elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'nl':
                        false_count_nl[x] = false_count_nl[x] + 1
                if self.class_list[line] == 'en':
                    main_en = main_en + 1
                elif self.class_list[line] == 'nl':
                    main_nl = main_nl + 1
            else:
                continue
        if (main_en == 0):
            get_node = Node('nl')
            return get_node
        if (main_nl == 0):
            get_node = Node('en')
            return get_node
        if flag2 == 1:
            if main_en > main_nl:
                node = Node('en')
                return node
            else:
                node = Node('nl')
                return node
        total = main_en + main_nl
        main_entropy = self.calculate_entropy(main_en, main_nl)
        for y in range(len(true_count_nl)):
            if len(nodes) == 0:
                if [self.root_attribute.value] == y:
                    information_gain_list.append(0)
                    continue
            else:
                list_of_nodes = nodes.keys()
                if y in list_of_nodes:
                    information_gain_list.append(0)
                    continue
            total_count_true = true_count_en[y] + true_count_nl[y]
            total_count_false = false_count_en[y] + false_count_nl[y]
            entropy_true = self.calculate_entropy(true_count_en[y], true_count_nl[y])
            first_term = (total_count_true / total) * entropy_true
            entropy_false = self.calculate_entropy(false_count_en[y], false_count_nl[y])
            second_term = (total_count_false / total) * entropy_false
            total_entropy = first_term + second_term
            information_gain = main_entropy - total_entropy
            information_gain_list.append(information_gain)
        maximum_index = self.calculate_maximum_number(information_gain_list)
        get_node = Node(maximum_index)
        return get_node

    def second_level_false(self,node,flagg):
        information_gain_list = []
        nodes = {}
        main_en = 0
        main_nl = 0
        true_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        true_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp_node = node
        parent = temp_node.get_parent()
        counter = 0
        while parent is not None:
            link_boolean = parent.get_link(temp_node)
            nodes[parent.value] = link_boolean
            counter = counter + 1
            temp_parent = parent.get_parent()
            temp_node = parent
            parent = temp_parent
        for line in range(len(self.attributes_list)):
            flag = 0
            if len(nodes) == 0:
                if (self.attributes_list[line][self.root_attribute.value]) == 'False':
                    flag = 1
            else:
                list_of_nodes = nodes.keys()
                for x in list_of_nodes:
                    if self.attributes_list[line][x] == nodes.get(x) and self.attributes_list[line][node.value] == 'False':
                        flag = 1
                    else:
                        flag = 0
                        break
            if flag == 1:
                for x in range(len(self.attributes_list[line])):
                    if self.attributes_list[line][x] == 'True' and self.class_list[line] == 'en':
                        true_count_en[x] = true_count_en[x] + 1
                    elif self.attributes_list[line][x] == 'True' and self.class_list[line] == 'nl':
                        true_count_nl[x] = true_count_nl[x] + 1
                    elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'en':
                        false_count_en[x] = false_count_en[x] + 1
                    elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'nl':
                        false_count_nl[x] = false_count_nl[x] + 1
                if self.class_list[line] == 'en':
                    main_a = main_a + 1
                elif self.class_list[line] == 'nl':
                    main_b = main_b + 1
            else:
                continue
        if (main_en == 0):
            get_node = Node('nl')
            return get_node
        if (main_nl == 0):
            get_node = Node('en')
            return get_node
        if flagg == 1:
            if main_en > main_nl:
                n = Node('en')
            else:
                n = Node('nl')
            return n
        total = main_en + main_nl
        main_entropy = self.calculate_entropy(main_en, main_nl)
        for y in range(len(true_count_nl)):
            total_count_true = true_count_en[y] + true_count_nl[y]
            total_count_false = false_count_en[y] + false_count_nl[y]
            entropy_true = self.calculate_entropy(true_count_en[y], true_count_nl[y])
            first_term = (total_count_true / total) * entropy_true
            entropy_false = self.calculate_entropy(false_count_en[y], false_count_nl[y])
            second_term = (total_count_false / total) * entropy_false
            total_entropy = first_term + second_term
            information_gain = main_entropy - total_entropy
            information_gain_list.append(information_gain)
        maximum_index = self.calculate_maximum_number(information_gain_list)
        get_node = Node(maximum_index)
        return get_node

    def first_level(self):
        information_gain_list = []
        main_en = 0
        main_nl = 0
        true_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        true_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_nl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        false_count_en = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for line in range (len(self.attributes_list)):
            for x in range(len(self.attributes_list[line])):
                if self.attributes_list[line][x] == 'True' and self.class_list[line] == 'en':
                    true_count_en[x] = true_count_en[x] + 1
                elif self.attributes_list[line][x] == 'True' and self.class_list[line] == 'nl':
                    true_count_nl[x] = true_count_nl[x] + 1
                elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'en':
                    false_count_en[x] = false_count_en[x] + 1
                elif self.attributes_list[line][x] == 'False' and self.class_list[line] == 'nl':
                    false_count_nl[x] = false_count_nl[x] + 1
            if self.class_list[line] == 'en':
                main_en = main_en + 1
            elif self.class_list[line] == 'nl':
                main_nl = main_nl + 1
        if (main_en == 0):
            get_node = Node('nl')
            return get_node
        if (main_nl == 0):
            get_node = Node('en')
            return get_node
        total = main_en + main_nl
        main_entropy = self.calculate_entropy(main_en, main_nl)
        for y in range(len(true_count_nl)):
            total_count_true = true_count_en[y] + true_count_nl[y]
            total_count_false = false_count_en[y] + false_count_nl[y]
            entropy_true = self.calculate_entropy(true_count_en[y], true_count_nl[y])
            first_term = (total_count_true / total) * entropy_true
            entropy_false = self.calculate_entropy(false_count_en[y], false_count_nl[y])
            second_term = (total_count_false / total) * entropy_false
            total_entropy = first_term + second_term
            information_gain = main_entropy - total_entropy
            information_gain_list.append(information_gain)
        maximum_index = self.calculate_maximum_number(information_gain_list)
        object_node = Node(maximum_index)
        self.root_attribute = object_node
        return self.root_attribute

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
        file = open(sys.argv[1], encoding='utf8')
        line = file.readline()
        line = line.replace("\n", '')
        while line:
            attribute_array= []
            line = line.replace("\n", '')
            individual_char = line.split(" ")
            get_class = individual_char[0].split('|')
            self.class_list.append(get_class[0])
            individual_char.append(get_class[1])
            attribute_array.append(self.contain_hyphen(individual_char[1:]))
            attribute_array.append(self.containenglishwords(individual_char[1:]))
            attribute_array.append(self.frequency_words(individual_char[1:]))
            attribute_array.append(self.apostrophe(individual_char[1:]))
            attribute_array.append(self.containIJ(individual_char[1:]))
            attribute_array.append(self.ratio(individual_char[1:]))
            attribute_array.append(self.containhetde(individual_char[1:]))
            attribute_array.append(self.containz(individual_char[1:]))
            attribute_array.append(self.englishpronouns(individual_char[1:]))
            attribute_array.append(self.dutchpronouns(individual_char[1:]))
            self.attributes_list.append(attribute_array)
            line = file.readline()


"""The main aim of Adaboost algorithm is to increase the examples which are wrongly classified. This is achieved by 
decreasing the weights for the examples which are correctly classified. Thus, the weights for the examples which are 
incorrectly classifies become greater than the correctly classified ones. This weight is used instead of count while 
calculating the entropy. The attribute with highest information gain becomes the respective stump. 
"""


class Decision_Stump:

    __slots__ = 'dataframe'

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def calculate_maximum_number(self, array):
        index_of_maximum_number = 0
        maximum_number = array[0]
        for index in range(1, len(array)):
            if maximum_number < array[index]:
                maximum_number = array[index]
                index_of_maximum_number = index
        return index_of_maximum_number

    def calculate_entropy(self, first_number, second_number):
        if (first_number == 0 or second_number == 0):
            return 0
        total_sum = first_number + second_number
        first_term = first_number / total_sum
        second_term = second_number / total_sum
        entropy = - (first_term * math.log(first_term, 2)) - (second_term * math.log(second_term, 2))
        return entropy

    def decide_rootnode(self,number_of_attributes):
        information_gain_list = []
        true_count_en = []
        true_count_nl = []
        false_count_en = []
        false_count_nl = []
        attribute = ['attribute1', 'attribute2', 'attribute3', 'attribute4', 'attribute5', 'attribute6', 'attribute7',
                     'attribute9', 'attribute8', 'attribute10']
        for index in range(number_of_attributes):
            true_count_en.append(self.dataframe[(self.dataframe[attribute[index]] == 'True') &
                                                  (self.dataframe['class'] == 'en')].loc[:,'weight'].sum())
            true_count_nl.append(self.dataframe[(self.dataframe[attribute[index]] == 'True') &
                                                  (self.dataframe['class'] == 'nl')].loc[:,'weight'].sum())
            false_count_en.append(self.dataframe[(self.dataframe[attribute[index]] == 'False') &
                                                   (self.dataframe['class'] == 'en')].loc[:,'weight'].sum())
            false_count_nl.append(self.dataframe[(self.dataframe[attribute[index]] == 'False') &
                                                   (self.dataframe['class'] == 'nl')].loc[:,'weight'].sum())
        total_count_en = self.dataframe[(self.dataframe['class'] == 'en')].loc[:,'weight'].sum()
        total_count_nl = self.dataframe[(self.dataframe['class'] == 'nl')].loc[:,'weight'].sum()
        total_count = total_count_en + total_count_nl
        class_entropy = self.calculate_entropy(total_count_en, total_count_nl)
        for y in range(len(true_count_nl)):
            total_count_true = true_count_en[y] + true_count_nl[y]
            total_count_false = false_count_en[y] + false_count_nl[y]
            entropy_true = self.calculate_entropy(true_count_en[y], true_count_nl[y])
            first_term = (total_count_true / total_count) * entropy_true
            entropy_false = self.calculate_entropy(false_count_en[y], false_count_nl[y])
            second_term = (total_count_false / total_count) * entropy_false
            attribute_entropy = first_term + second_term
            information_gain = class_entropy - attribute_entropy
            information_gain_list.append(information_gain)
        maximum_index = self.calculate_maximum_number(information_gain_list)
        return maximum_index

class Adaboost:

    __slots__ = 'dataframe', 'hypothesis', 'hypothesis_weight'

    def __init__(self,dataframe):

        self.dataframe = dataframe
        self.hypothesis = []
        self.hypothesis_weight = []

    def main_algorithm(self,number_of_lines):

        attribute = ['attribute1', 'attribute2', 'attribute3', 'attribute4', 'attribute5', 'attribute6', 'attribute7',
                     'attribute8', 'attribute9', 'attribute10']
        for k in range (11):
            object_of_decision_stump = Decision_Stump(self.dataframe)
            rootnode = object_of_decision_stump.decide_rootnode(10)
            self.hypothesis.append(rootnode)
            error = 0
            for index in range (number_of_lines):
                if self.dataframe.loc[index,'class'] == 'en':
                    class_attribute_value = 'True'
                else:
                    class_attribute_value = 'False'
                if not(self.dataframe.loc[index,attribute[rootnode]] == class_attribute_value):
                    weight_value = self.dataframe.loc[index, 'weight']
                    error = error + weight_value
            for index in range (number_of_lines):
                if self.dataframe.loc[index,'class'] == 'en':
                    class_attribute_value = 'True'
                else:
                    class_attribute_value = 'False'
                if self.dataframe.loc[index,attribute[rootnode]] == class_attribute_value:
                    self.dataframe.loc[index, 'weight'] = ((self.dataframe.loc[index,'weight'] * error) / (1 - error))
            total_weight = self.dataframe.loc[:,'weight'].sum()
            for index in range (number_of_lines):
                self.dataframe.loc[index,'weight'] = (self.dataframe.loc[index,'weight'] / total_weight)
            hypothesis_weight = math.log((1 - error) / error)
            self.hypothesis_weight.append(hypothesis_weight)
        return self.hypothesis, self.hypothesis_weight

class LoadData:

    __slots__ = 'dataframe'

    def __init__(self, dataframe):
         self.dataframe = dataframe

    def contain_hyphen(self, array):
        booleanvalue = 'False'
        for word in array:
            if word.__contains__("-"):
                booleanvalue = 'True'
                break
        return booleanvalue

    def contain_english_words(self, array):
        booleanvalue = 'False'
        list_of_frequent_english_words = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
                'yourself', 'he', 'him', 'his', 'himself', 'she', 'her', 'herself', 'it', 'itself', 'they', 'them',
                'their', 'themselves', 'what', 'which', 'who', 'whom', ' this', 'that', 'these', 'those', 'am', 'is',
                'are', 'was', 'were', 'be', 'being', 'been', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                'for', 'with', 'after', 'below', 'from', 'there', 'so', 'than', 'too', 'very', 'can', 'will',
                'just', 'don', 'should', 'now']
        for word in array:
            if len(word) > 0 and list_of_frequent_english_words.__contains__(word):
                booleanvalue = 'True'
                break
        return booleanvalue

    def frequency_of_long_words(self, array):
        booleanvalue = 'True'
        counter = 0
        for word in array:
            if len(word) > 12:
                counter = counter + 1
            if counter > 1:
                booleanvalue = 'False'
                break
        return booleanvalue

    def apostrophe(self, array):
        booleanvalue = 'False'
        for word in array:
            if word.__contains__("'"):
                booleanvalue = 'True'
                break
        return booleanvalue

    def contain_dutch_words(self, array):
        booleanvalue = 'True'
        list = ['aan', 'af', 'al', 'alles', 'als', 'altijd', 'andere', 'ben', 'bij', 'daar', 'dan', 'dat', 'der',
                'deze']
        for word in array:
            if list.__contains__(word):
                booleanvalue = 'False'
                break
        return booleanvalue

    def average_length(self, array):
        booleanvalue = 'True'
        total_length = 0
        for x in array:
            total_length = total_length + len(x)
        average_length = total_length / (len(array))
        if average_length > 6:
            booleanvalue = 'False'
        return booleanvalue

    def contain_het_de(self,array):
        booleanvalue = 'True'
        for word in array:
            if word == 'het' or word == 'de':
                booleanvalue = 'False'
        return booleanvalue

    def contain_z(self,array):
        booleanvalue = 'True'
        counter = 0
        for word in array:
            if word. __contains__("z"):
                counter = counter + 1
            if (counter > 0):
                booleanvalue = 'False'
                break
        return booleanvalue

    def english_pronouns(self,array):
        booleanvalue = 'False'
        list_of_pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'who', 'me', 'him', 'her', 'it', 'us', 'you', 'them', 'whom',
            'mine', 'yours', 'his', 'hers', 'ours', 'theirs', 'this', 'that', 'these', 'those' ]
        for word in array:
            if list_of_pronouns.__contains__(word):
                booleanvalue = 'True'
                break
        return booleanvalue

    def dutch_pronouns(self,array):
        booleanvalue = 'True'
        list_of_pronouns = ['ik', 'jij', 'je', 'u', 'hij', 'zij', 'ze', 'wij', 'zij', 'mij', 'jou', 'uw', 'hem','haar','ons','hen'
                'mijn', 'jouw', 'uw', 'zijn', 'haar', 'onze', 'hun', 'van mij', 'van jou', 'van u', 'van hem', 'van haar','van ons', 'van hun']
        for word in array :
            if list_of_pronouns.__contains__(word):
                booleanvalue = 'False'
                break
        return booleanvalue

    def readFile(self):
        file = open(sys.argv[1], encoding='utf8')
        line = file.readline()
        line = line.replace("\n", '')
        number_of_samples = 0
        while line and len(line)>1:
            number_of_samples = number_of_samples + 1
            line = line.replace("\n", '')
            array_words = line.split(" ")
            get_class = array_words[0].split('|')
            array_words.append(get_class[1])
            attribute1 = self.contain_hyphen(array_words[1:])
            attribute2 = self.contain_english_words(array_words[1:])
            attribute3 = self.frequency_of_long_words(array_words[1:])
            attribute4 = self.apostrophe(array_words[1:])
            attribute5 = self.contain_dutch_words(array_words[1:])
            attribute6 = self.average_length(array_words[1:])
            attribute7 = self.contain_het_de(array_words[1:])
            attribute8 = self.contain_z(array_words[1:])
            attribute9 = self.english_pronouns(array_words[1:])
            attribute10 = self.dutch_pronouns(array_words[1:])
            dictionary = {'attribute1': [attribute1], 'attribute2': [attribute2], 'attribute3': [attribute3],
                          'attribute4': [attribute4], 'attribute5': [attribute5], 'attribute6': [attribute6],
                          'attribute7': [attribute7], 'attribute8': [attribute8], 'attribute9': [attribute9],
                          'attribute10': [attribute10], 'class': [get_class[0]]}
            dataframe_to_be_appended = pandas.DataFrame(dictionary)
            self.dataframe = self.dataframe.append(dataframe_to_be_appended,ignore_index=True)
            line = file.readline()
        weight = 1 / number_of_samples
        weightarray = []
        for number in range (number_of_samples):
            weightarray.append(weight)
        self.dataframe['weight'] = weightarray
        return number_of_samples


""" Decision tree is implemented using dynamic programming. The attributes are dropped for the respective subtrees. 
When all the attributes are used or if the 'en' or 'nl' class is found then that respective branch of decision tree 
terminates. The 'flagcheck' is used to check the terminating condition of the decision tree.
"""


if __name__ == '__main__':
    algodecider = sys.argv[3]
    if (algodecider == "ada"):
        dataframe = pandas.DataFrame()
        object_loaddata = LoadData(dataframe)
        line = object_loaddata.readFile()
        object_adaboost = Adaboost(object_loaddata.dataframe)
        hypothesis, hypothesis_weight = object_adaboost.main_algorithm(line)
        pickle_list = []
        flag = 1
        pickle_list.append(flag)
        pickle_list.append(hypothesis)
        pickle_list.append(hypothesis_weight)
        dbfile = open(sys.argv[2], 'ab')
        pickle.dump(pickle_list, dbfile)
        dbfile.close()
    elif (algodecider == "dt"):
        main_object = Decision_Tree_Build()
        Decision_Tree_Build.initialize_class(main_object)
        root_node = Decision_Tree_Build.first_level(main_object)
        counter = 0
        counter1 = 1
        array_program = []
        array_program.append(root_node)
        flag = 0
        attribute_append = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        attribute_append.remove(root_node.value)
        attributemainarray = []
        attributemainarray.append(attribute_append)
        check = len(attributemainarray)
        flagcheck = 0
        while (flagcheck == 0):
            counter = counter + 1
            leaf_nodes_count = 0
            leaf_node = 0
            loop_counter = math.pow(2, (counter))
            check = 1
            while (leaf_node < loop_counter):
                main_node = array_program[leaf_nodes_count]
                leaf_nodes_count = leaf_nodes_count + 1
                if (main_node == None or main_node.value == 'en' or main_node.value == 'nl'):
                    continue
                second_node = Decision_Tree_Build.second_level_true(main_object, main_node, flag)
                third_node = Decision_Tree_Build.second_level_false(main_object, main_node, flag)
                check = check + 1
                arrayremove2 = []
                arrayremove1 = []
                for x in attributemainarray[check - 2]:
                    arrayremove1.append(x)
                try:
                    if (not (second_node.value == 'en' or second_node.value == 'nl' or arrayremove1 == [])):
                        arrayremove1.remove(second_node.value)
                        attributemainarray.append(arrayremove1)
                    else:
                        attributemainarray.append([])
                except:
                    second_node = Decision_Tree_Build.second_level_true(main_object, main_node, 1)
                    attributemainarray.append([])
                for x in attributemainarray[check - 2]:
                    arrayremove2.append(x)
                try:
                    if (not (third_node.value == 'en' or third_node.value == 'nl' or arrayremove2 == [])):
                        arrayremove2.remove(third_node.value)
                        attributemainarray.append(arrayremove2)
                    else:
                        attributemainarray.append([])
                except:
                    third_node = Decision_Tree_Build.second_level_false(main_object, main_node, 1)
                    attributemainarray.append([])
                object_graph2 = Tree(main_node, second_node, third_node)
                array_program.append(second_node)
                array_program.append(third_node)
                leaf_node = leaf_node + 2
            flagcheck = 1
            math_remove = math.pow(2, (counter - 1))
            for x in range(int(math_remove)):
                array_program.pop(0)
                attributemainarray.pop(0)
            for x in attributemainarray:
                if x != []:
                    flagcheck = 0
        counter2 = 0
        for x in array_program:
            if not (x.value == 'en' or x.value == 'nl'):
                parent_node = x.parent
                link = parent_node.get_link(x)
                if link == 'True':
                    second_node = Decision_Tree_Build.second_level_true(main_object, parent_node, 1)
                    Tree(parent_node, second_node, parent_node.false)
                elif link == 'False':
                    second_node = Decision_Tree_Build.second_level_false(main_object, parent_node, 1)
                    Tree(parent_node, parent_node.true, second_node)
                    array_program[counter2] = second_node
            counter2 = counter2 + 1
        dbfile = open(sys.argv[2], 'ab')
        picklelist = []
        picklelist.append(0)
        picklelist.append(root_node)
        pickle.dump(picklelist, dbfile)
        dbfile.close()