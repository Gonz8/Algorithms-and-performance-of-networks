from classes_functions import aList, RandTree, GenerateCode, Decode, Node

f = open('test2.txt',"r")
Symbols = aList()
for word in f.read().split():
	Symbols.insert(Node(None,word))
f.closed

root = RandTree(Symbols) #Creates random tree with the symbols and outputs its root
Code = GenerateCode(root) #Outupts the dictionary cointaing the code for the symbols in the tree leaves

print('Symbols and generated prefixes:')
for word in Code: #Prints the code contain in the dictionary
	print(word,':',Code[word])

bi_string = input('Write a binary string to be decoded: ') #Waits for user to type a binary string
Decode(root, bi_string)
