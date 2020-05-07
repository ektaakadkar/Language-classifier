# Language-classifier
 Language classifier using ‘Decision Tree’ and ‘Adaboost algorithm’ to classify the given set of lines into Dutch and English. Accuracy : 98 %  

Description of the decision tree learning, how you came up with the best parameters and your own testing results - 
The decision tree learning algorithm is based on the information gain of each attribute. The attribute having the highest information gain is selected as the root node. This process is iterated till all the attributes within the tree are used. That means the tree root value consists of the attribute. Then the respective tree will not have that attribute in it’s nodes. The entire decision tree is saved in the bi-directional graph structure (tree). The most powerful attribute is selected as the root node and in the later levels of the tree the attributes having the highest information gain excluding the parent node attributes is selected. The leaf nodes of the tree consists of classes ‘en’ and ‘nl’. Here, ‘en’ represents English language and ‘nl’ represents Dutch language. 

Description of the boosting, how many trees turned out to be useful, and your own testing -  
The attributes which are more powerful were only selected by the Adaboost algorithm. The hypothesis weight of the powerful attribute was also more compared to other attribute hypothesis weight. Out of the total attributes, the attributes which are more powerful were repeatedly chosen. From my attribute list, attributes such as “frequent dutch words”, “frequent english words”, “whether it contains ‘het’ or ‘de’ “ were selected repeatedly. The error rate for each hypothesis decreases as we proceed. The examples which are wrongly classified are allocated more weight and this weight is taken into consideration while calculating entropy. The attribute having highest information gain will be selected. As the wrongly classified examples have more weight they are taken more into consideration as per the algorithm.   

Description of your features and how you chose them – 
For English I have taken the attribute value as ‘True’ and for Dutch I have taken the attribute value as ‘False’. 
I have selected 10 features in total which was the given least requirement. 
The features selected are as follows: 
1. Hyphen : 
The hyphen which is used between the words is found more often in English language than the Dutch language. So, if the line contains a hyphen then it is classified as English. Thus, if the input line contains hyphen then the function returns ‘True’ otherwise it returns ‘False’. 
2. Frequent english words : 
 I have made a list of English words which are found often. This list consists of words such as after, before, etc… So, if the line contains the words given in the list then it is classified as English. Thus, if the input line contains words given in the list then the function returns ‘True’ otherwise it returns ‘False’. 
3. Length of words: 
The length of dutch words is more than the english words. Thus, if the length of any one word in the input line is greater than 12 then it is classified as dutch and so returns ‘False’. 
4. Apostrophe : 
English language contains more apostrophes than the Dutch language. Thus if the line contains an apostrophe then it is classified as English and returns ‘True’. 
5. Frequent dutch words : 
I have made a list of Dutch words which are found often. So, if the line contains the words given in the list then it is classified as Dutch. Thus, if the input line contains words given in the list then the function returns ‘False’ otherwise it returns ‘True’. 
6. Average word length : 
As stated earlier, Dutch words have larger length than English words. So, if the average word length of the given sentence is greater than 6 then it is classified as Dutch and it returns ‘True’. 
7. Contains ‘het’ or ‘de’ : 
Even if I have a list of more frequent dutch words, the words ‘het’ and ‘de’ were much more frequently occuring. So I thought that this would be a powerful attribute to classify the Dutch language. Hence, I made a separate attribute for these words. So, if the input contains the two words then it will return ‘False’ otherwise it returns ‘True’. 
8. English pronouns : 
The pronouns would make a powerful set of attributes. So a list of pronouns used in English was made separately and this list was used to check the input. If the input contains a word from the given list then it returns ‘True’ otherwise it returns ‘False’.  
9. Dutch pronouns : 
A list of pronouns used in Dutch  was made separately and this list was used to check the input. If the input contains a word from the given list then it returns ‘False’ otherwise it returns ‘True’ 
10.Letter z: 
The input in Dutch has more z letters than the input in English. Thus, if the input contains more than 1 z letter then it is classified as Dutch and returns ‘False’ otherwise it returns ‘True’. 
