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


# AES key must be either 16, 24 or 32 bytes long
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

# create tcp/ip socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# fix host address and port number
host = socket.gethostname()
port = 8091

# bind to the port
server.bind((host, port))

# we will listen to 5 allies we can add more allie if we want
server.listen(5)

# etablish connection
client, address = server.accept()
print bcolors.YELLOW + 'connection from' +str(address) + bcolors.ENDC

# fix the algorithme and the hash that we will use to communicate
client.send(bcolors.YELLOW +"we will use AES and Sha2 for our key here !!")
print "we will use AES and Sha2 for our key here !!" + bcolors.ENDC

# wait for confirmation ...
print bcolors.YELLOW +"waiting for confirmation ..."+ bcolors.ENDC
rep= client.recv(1024)
print bcolors.GREEN + rep + bcolors.ENDC

# we will ask a privat question here !!
que= raw_input(bcolors.BLUE +"ask a privat question to your allies Sir :"+ bcolors.ENDC)
client.send(encrypt(que,key))

# send the hashed question
client.send(sha2(que))

# send a number between 3000 and 4000
b=False
while b == False:
	NA = int(raw_input(bcolors.BLUE +"write a number between 3000 and 4000 Sir :"+ bcolors.ENDC))
	if (3000 < NA < 4000):
		b=True
 		NA = str(NA)
	elif NA < 3000:
		print bcolors.BBLUE +"you are under 3000 Sir"+ bcolors.ENDC
        else:
		print bcolors.BBLUE +"you are writing a big number Sir !!"+ bcolors.ENDC

client.send(NA)

# waiting for confirmation with NB and the answer
print bcolors.YELLOW +"waiting for answer ..."+ bcolors.ENDC

nb = client.recv(1024)

ans = client.recv(1024)

# decrypt answer and wait for confirmation
like = decrypted(ans,key)
print like

# only humain can do this !! verifie the answer
reject = raw_input("This is the right answer y/n ")
reject=reject.upper()

if reject != 'Y' :
	client.close()
	print bcolors.RED +"access has benn denied :)"+ bcolors.ENDC
else : 
	client.send("   every think is okay, we are here for order Sir !!")
	print bcolors.YELLOW +"waiting for orders ..."+bcolors.ENDC
	# verification has been end we can now communicate
	while True:
	    data = client.recv(1024)
	    # if data is empty no need to continue
	    if not data:
	        break
  	    # else we listen to order from our allies 
	    print "Crypted message : " + str(data)
	    order = decrypted(data, key).upper()
	    print "reiceved : " + order
	    # we will aswer with a crypted message better then repeating the same answer in each order like "Yes Sir !!" for exemple because that can defeat our key
	    client.send(data)
client.close()
print bcolors.MOVE +"END OF COMMUNICATION, GOOD LUCK FOR WAR MAY GOD PROTECT YOU !!" +bcolors.ENDC
