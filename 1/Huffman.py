from classes_functions import is_number, HuffmanCode
import sys

f = open(str(sys.argv[1]),"r") #To run this script with 'test.txt' text file one should write 'python Huffman.py test.txt'
Symbols = []
Freqs = []
for word in f.read().split():
	if is_number(word):
		Freqs.append(float(word)) # WHAT IF NUMBERS ARE SYMBOLS!!!
	else:
		Symbols.append(word)
f.closed
#print(Symbols)
#print(Freqs)

HuffmanCode(Symbols, Freqs)
#Codes = HuffmanCodee(Symbols, Freqs)
