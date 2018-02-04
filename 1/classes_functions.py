import random

class aString:
	def __init__(self):
		self.vec = ''
		self.size = 0

	def insert(self, x):
		self.vec.append(x)
		self.size += 1

	def delete(self, x):
		del self.vec[x]
		self.size -= 1

class aList:
	def __init__(self):
		self.vec = []
		self.size = 0

	def insert(self, x):
		self.vec.append(x)
		self.size += 1

	def delete(self, x):
		del self.vec[x]
		self.size -= 1

class Node:
	def __init__(self, freq, symb = None, left = None, right = None):
        	self.freq = freq
        	self.symb = symb
        	self.l = left
        	self.r = right

class BinHeap:
	def __init__(self):
        	self.heapList = [Node(0)]
        	self.currentSize = 0

	def percUp(self,i):
		while i // 2 > 0:
	      		if self.heapList[i].freq < self.heapList[i // 2].freq:
	         		tmp = self.heapList[i // 2]
	         		self.heapList[i // 2] = self.heapList[i]
	         		self.heapList[i] = tmp
	      		i = i // 2

	def insert(self,k):
	    	self.heapList.append(k)
	    	self.currentSize = self.currentSize + 1
	    	self.percUp(self.currentSize)

	def percDown(self,i):
    		while (i * 2) <= self.currentSize:
        		mc = self.minChild(i)
        		if self.heapList[i].freq > self.heapList[mc].freq:
            			tmp = self.heapList[i]
            			self.heapList[i] = self.heapList[mc]
            			self.heapList[mc] = tmp
        		i = mc

	def minChild(self,i):
	    	if i * 2 + 1 > self.currentSize:
	        	return i * 2
	    	else:
	        	if self.heapList[i*2].freq < self.heapList[i*2+1].freq:
	        		return i * 2
	        	else:
	        		return i * 2 + 1

	def delMin(self):
	    	retval = self.heapList[1]
	    	self.heapList[1] = self.heapList[self.currentSize]
	    	self.currentSize = self.currentSize - 1
	    	self.heapList.pop() #del self.heapList[self.currentSize]
	    	self.percDown(1)
	    	return retval

def is_number(s):
    	try:
        	complex(s) # for int, long, float and complex
    	except ValueError:
        	return False
    	return True

def GenerateCode(root, code = '', symbols = {}):
    if root.symb != None:
        symbols[root.symb] = code
        #print(root.symb, code)
    else:
        GenerateCode(root.l, code + '0', symbols) # + is maybe not the most efficient!!!
        GenerateCode(root.r, code + '1', symbols)
    return symbols

def Decode(root, InString, OutString = ''):
    while(InString != ''):
        OutString, InString = RunTree(root, InString, OutString)
    print('Decoded string:', OutString)

def RunTree(root, InString, OutString):
    while(root.symb == None):
        if(int(InString[0]) == 0):
            root = root.l
        elif(int(InString[0]) == 1):
            root = root.r
        InString = InString[1:]
    OutString += str(root.symb)
    return OutString, InString

def HuffmanCode(Symbols, Freqs):
	HuffTree = BinHeap()
	i = 0
	for simb in Symbols:
		HuffTree.insert(Node(Freqs[i], simb))
		i += 1

#	for x in HuffTree.heapList:
#		print(x.freq)

	while(HuffTree.currentSize > 1):
		small1 = HuffTree.delMin()
		small2 = HuffTree.delMin()

		HuffTree.insert(Node(small1.freq + small2.freq, None, small1, small2))

	root = HuffTree.heapList[1]
	Code = GenerateCode(root)

	print('Symbols and generated Huffman prefixes:')
	for word in Code:
		print(word,':',Code[word])

def RandTree(symbols):
	while(symbols.size > 1):
		i = round(random.random() * (symbols.size - 1))
		aux1 = symbols.vec[i]
		symbols.delete(i)
		i = round(random.random() * (symbols.size - 1))
		aux2 = symbols.vec[i]
		symbols.delete(i)

		symbols.insert(Node(None, None, aux1, aux2))

	return symbols.vec[0]
