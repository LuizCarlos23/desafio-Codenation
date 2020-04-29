from requests import get, post
from json import dumps, loads
from hashlib import sha1

alphabetBase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
token = "7da8c6c71e3fa26b6854b51bab52f1baabecf97d"
urlGet = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token="+token
urlPost = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token="+token

#--------------------Functions---------------------

# Function to generate the encrypted alphabet
def generateEncryptedAlphabet(position):
	newAlphabet = alphabetBase.copy()
	for i in range(0, position+1):
		letter = newAlphabet.pop()
		newAlphabet.insert(0, letter)
	return newAlphabet

# Function to decipher the menssage
def decipherString(position, msg):
	newAlphabet = generateEncryptedAlphabet(position)
	decipheredString = ""
	for letter in msg:
		if (letter.isnumeric()):
			decipheredString += letter
		elif (letter == '.'):
			decipheredString += letter
		elif (letter in alphabetBase):
			decipheredString += alphabetBase[newAlphabet.index(letter)]
		else:
			decipheredString += " "
	return decipheredString

def makeSha1(string, encoding="utf-8"):
	return sha1(string.encode(encoding)).hexdigest()

#---------------------End--------------------------

response_api = get(urlGet)
dataJson = loads(response_api.text)
# Fule created with api data
with open("answer.json", "w") as file:
	file.write(dumps(dataJson))

encryptedString = dataJson["cifrado"]
position = dataJson["numero_casas"]
decipheredString = decipherString(25-position, encryptedString)
#decipheredString = decipherString(24, encryptedString)
cryptographicSummary = makeSha1(decipheredString)

dataJson["decifrado"] = decipheredString
dataJson["resumo_criptografico"] = cryptographicSummary

# Updated with new data
with open("answer.json", "w") as file:
	file.write(dumps(dataJson))

fileJson = {"answer": open("answer.json", "rb")}	
result = post(urlPost, files=fileJson)
print(result)