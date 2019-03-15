#/bin/python

# import bibl of socket, hashage, cryptage en AES
import socket
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES

# we add some color to make chat clear
class bcolors:
    MOVE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BBLUE = '\033[1m'
    UNDERLINE = '\033[4m'

key=raw_input(bcolors.MOVE +"AES key must be either 16, 24 or 32 bytes long : "+ bcolors.ENDC)

# creat hashed key on hexidegest def
def sha2(message):	
	sha256 = SHA256.new()
	sha256.update(message)
	hex_hash_sha256 = sha256.hexdigest()
	return hex_hash_sha256

#encrypt
def encrypt(message, key):
	cipher_aes = AES.new(key.encode(), AES.MODE_CFB, key)
	encrypted_aes = cipher_aes.encrypt(message.encode())
	return encrypted_aes

#decrypted
def decrypted(message, key):
	dec_cipher_aes = AES.new(key.encode(), AES.MODE_CFB, key)
	decrypted_aes = dec_cipher_aes.decrypt(message)
	return decrypted_aes

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# fix host address and port number
host = '127.0.1.1'
port = 8091

# waiting for connection
print(bcolors.YELLOW + 'connecting to server...'+ bcolors.ENDC)
client.connect((host, port))

# connection has been etablished
print bcolors.YELLOW + 'connected'+ bcolors.ENDC

# ask for communication
msg = client.recv(1024)
print bcolors.YELLOW + msg + bcolors.ENDC
choi=raw_input("would you accept to communicate y/n ")
choi=choi.upper()
if choi != 'Y' :
	client.close()
else :
	# confirm
	client.send(bcolors.GREEN +"Confirmed" + bcolors.ENDC)
	
	# receive the question
	que_c = client.recv(1024)

	# receive the hashed question
	que_h = client.recv(1024)

	# receive the number
	na = client.recv(1024)

	# decrypt the question
	que = decrypted(que_c, key)	

	#hash the question for verification	
	verif=sha2(que)
	
	# verification of the identity of the allie
	if verif != que_h  :
		client.close()
		print bcolors.RED + "we are not connecting to the right server !!, fake identity be careful Sir !!!" + bcolors.ENDC
	else :
		# send a number between 4000 and 5000
		b=False
		while b == False:
			NB= int(raw_input(bcolors.BLUE +"write a number between 4000 and 5000 Sir :"+bcolors.ENDC))
			if (4000 < NB < 5000):
				b=True
				NB = str(NB)
			elif NB < 4000:
				print bcolors.BBLUE+"you are under 4000 Sir"+bcolors.ENDC
        		else:
				print bcolors.BBLUE+"you are writing a big number :o !!"+bcolors.ENDC
		client.send(NB)
		# answer the question		
		print bcolors.YELLOW + que + bcolors.ENDC
		ans = str(raw_input(bcolors.BLUE + "answer : " + bcolors.ENDC))
		an = encrypt(ans,key)		
		
		# send crypted answer, NB and NA
		client.send(an)

		# server verified we can transfer our crypted message or file
		message = raw_input("write your message or print q to quit :")

		# if the client would communicate he can else he left the canal with 'q'
		while message != 'q':
			client.send(encrypt(message, key))
			data = client.recv(1024)
			print "Order has been received " + str(data)
			message = raw_input("write your message or print q to quit :")
client.close()
print bcolors.MOVE +"END OF COMMUNICATION"+bcolors.ENDC
