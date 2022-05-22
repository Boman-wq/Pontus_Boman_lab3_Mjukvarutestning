import binascii
import hashlib

# Simple encryption / decryption algorithm 
# encrypts or decrypts with XOR depending on what inBuffer is sent in

def main():

    # Input
	#infile = input("Input file name to Decode or Encode: ")
	#outfile = input("Output file name: ")
	#bEncrypt = int(input("1=encrypt, 0=decrypt: "))

	# bEncrypt = 1 => encrypt
	infile1 = "c:/tmp/test.txt"
	outfile1 = "c:/tmp/test1.enc"
	encode(infile1, outfile1, bEncrypt = 1)

	# bEncrypt = 0 => decrypt
	infile2 = "c:/tmp/test1.enc"
	outfile2 = "c:/tmp/test2.txt"
	encode(infile2, outfile2, bEncrypt = 0)

	# check hash input vs. output

	with open(infile1, mode='rb') as file1:
		before = file1.read()
		with open(outfile2, mode='rb') as file2:
			after = file2.read()

			hash_object1 = hashlib.md5(before)
			hash_object2 = hashlib.md5(after)
			print("Are the files equal after XOR encryption? " + 
				str(hash_object1.hexdigest() == hash_object2.hexdigest()))


# perform high level work
def encode(infile, outfile, bEncrypt):
	
	# encryption key, must be 20 chars
	key = "abcdefghijklmnopqrst"
	inBuffer = []

	# read input file from storage into inBuffer
	with open(infile, mode='rb') as file:
		char = file.read(1)
		while char:
			inBuffer.append(char.hex())
			char = file.read(1)
		file.close()

	# encrypt or decrypt (bEncrypt) inBuffer into outBuffer
	outBuffer = decrypt(key, inBuffer, len(inBuffer), bEncrypt)

	# write outBuffer to file on storage
	# https://www.delftstack.com/howto/python/how-to-convert-int-to-bytes-in-python-2-and-python-3/
	with open(outfile, mode='wb') as file:
		for decChar in outBuffer:
			file.write(bytes([decChar]))
		file.close()


# perform low level work
def decrypt(key, inBuffer, length, bEncrypt):
	# size of the en/de-cryption key buffer
	KEY_BUF = 20
	outBuffer = []
	KeyA = 0
	
	for n in range(0, KEY_BUF):
		KeyA ^= ord(key[n])
			
	nKeyPos = KeyA % KEY_BUF
	
	for n in range(0, length):
		# Get lost high-values that got removed when writing the char
		XORval = format(ord(key[nKeyPos]) * KeyA, 'x')
		XORval = XORval[:-2]
		trueEnc = XORval + inBuffer[n]
		
		# Inverse the XOR
		decVal = int(trueEnc, 16) ^ (ord(key[nKeyPos]) * KeyA)
		outBuffer.append(decVal)
		
		# print("%s ^ %s = %s" % (int(trueEnc, 16), (ord(key[nKeyPos]) * KeyA), decVal))
		
		# Get the next KeyA and pos
		# KeyA och nKeyPos beräknas alltid på den krypterade bufferten
		if(bEncrypt == 1):
			#KeyA = (KeyA + int(outBuffer[n], 16)) % 256
			#nKeyPos = int(outBuffer[n], 16) % KEY_BUF
			KeyA = KeyA + outBuffer[n]
			nKeyPos = outBuffer[n] % KEY_BUF
		else:
			KeyA = (KeyA + int(inBuffer[n], 16)) % 256
			nKeyPos = int(inBuffer[n], 16) % KEY_BUF

	return outBuffer
	

if __name__ == "__main__":
    main()

