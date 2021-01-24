"""
Author: Yoseph Alabdulwahab
Copyright: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

Description:
	This is a python script to encrypt and decrypt files for use as backup. 
	The encryption process also provides ability to securely wipe the plaintext file
	when possible.
"""
import sys, subprocess, getpass
from os import path

#Import packages that may need install.
try:
	import gnupg
except ImportError:
	print('Installing python-gnupg...\n')
	subprocess.check_call([sys.executable, "-m", "pip", "install", "python-gnupg"])
	import gnupg
	print("--------------------------------------------------------------------------------\n")
try:
	from secure_delete import secure_delete
except ImportError:
	print('Installing secure_delete...\n')
	subprocess.check_call([sys.executable, "-m", "pip", "install", "secure_delete"])
	import secure_delete
	print("--------------------------------------------------------------------------------\n")

########################################################################################################
## Encryption and Decryption ###########################################################################
########################################################################################################

# A method to encrypt a file using the provided password
#
# filepath -> The path of the file to encrypt
# passwd -> The password to use for encrypting
#
# Output: Returns true or false based on success. Will print error if failed.
def encrypt_file(filepath, passwd):
	#init GnuPG
	gpg = gnupg.GPG()

	#Open file and encrypt with AES256 and output to {filepath}.gpg
	try:
		with open(filepath, 'rb') as file:
			status = gpg.encrypt_file(file, 
				symmetric='AES256', 
				passphrase=passwd, 
				output=filepath+'.gpg', 
				armor=False, 
				recipients=None)
	except FileNotFoundError:
		print(f"ERROR: Could not open file '{filepath}'. Make sure you entered the correct file")
		return False #Abort function

# A method to decrypt a file using the provided password.
#
# filepath -> The path of the file to decrypt
# passwd -> The password to use for decrypting
#
# Output: Will create a file named [filepath]<minus the .gpg extension> containing the decrypted content
def decrypt_file(filepath, passwd):
	#double check we are decrypting a .gpg file if so prep
	if(not filepath.endswith(".gpg")):
		print(f"ERROR: File '{filepath}' is not a .gpg file.")
		return False
	
	#init GnuPG
	gpg = gnupg.GPG()

	try:
		#Decrypt file with gpg decrypt. Will work with any valid gpg encryption scheme
		with open(filepath, 'rb') as file:
			gpg = gnupg.GPG()
			filepath_o = filepath[:-4]
			status = gpg.decrypt_file(file, passphrase=passwd, output=filepath_o)
	except FileNotFoundError:
		print(f"ERROR: Could not open file '{filepath}'. Make sure you entered the correct filepath")
		return False #Abort function

###################################################################################################
## I/O Methods ####################################################################################
###################################################################################################

# A method to check if a file exists.
#
# filepath -> the file path to validate
#
# Output: 
# 		Return false if filepath is not a string
#		Return true if filepath is valid
#		Print error and Quit program if filepath does not exists
def validate_filepath(filepath):
	filepath = sys.argv[0]
	if(not isinstance(filepath, str)):
		return False
	elif(not path.exists(filepath)):
		print(f"ERROR! File '{filepath}' does not exist. Please double check and try again")
		exit(1) #Quit program
	else:
		return True

# A method to get userpassword from the command line.
# If asktwice is set to true then it will reprompt the
# 	user to re-enter the same password until they match
def get_password(asktwice = False):
	#Ask for a password
	passwd = getpass.getpass(prompt="Enter a password: ")

	#Stark asking for passwd confirmation.
	if(asktwice == False):
		return passwd
	passwd_re = getpass.getpass(prompt="Re-enter the password: ")

	#if passwords do not match, ask to enter again
	while(passwd != passwd_re):
		print("\nPasswords did not match. Please try again.")
		passwd = getpass.getpass(prompt="Enter a password: ")
		passwd_re = getpass.getpass(prompt="Re-enter the password: ")

	#Passwords matched, return passwd
	return passwd


#Print script usage
def print_usage():
	print("\n Usage: ")
	print("    secure-encrypt.py encrypt <filepath>			# Will encrypt said file and wipe it")
	print("    secure-encrypt.py decrypt <filepath>			# Will decrypt said file")
	print("    secure-encrypt.py wipe <filepath>			# Will only wipe said file")

# Wipe file
def wipe(filepath):
	print(f"Secure wiping file {filepath}...")
	print("    WARNING: This only works on Windows/Linux on standard filesystems using a HDD. \
				FILES MAY STILL BE RECOVERABLE ON SSDs.")
	secure_delete.secure_random_seed_init()
	secure_delete.secure_delete(filepath)

#Encrypt file. Will also wipe it
def encrypt(filepath):
	#Get password
	passwd = get_password(asktwice = True)

	#Encrypt file
	print(f"Encrypting file '{filepath}'.")
	status = encrypt_file(filepath, passwd)

	#Check if succeded
	if(status == False):
		print("Could not encrypt. Skipping secure.")
		exit(1) #Quit program

	#Wipe file
	wipe(filepath)

#Decrypt file
def decrypt(filepath):
	#Get password
	passwd = get_password()

	#Decrypt file
	print(f'Decrypting file ')
	decrypt_file(filepath, passwd)

###################################################################################################
## START OF SCRIPT ################################################################################
###################################################################################################

#Guess if we are encrypting or decrypting
if(len(sys.argv) == 2):
	print("WARNING: no command supplied. Trying to guess what you mean ...")
	arg0 = sys.argv[1]

	#Make sure file exists before proceding 
	validate_filepath(arg0)

	#Decide between encrypting or decrypting
	if(arg0[-4:] == '.gpg'): #Decrypt file
		decrypt(arg0)
		exit(0) #Quit program
	else: #Encrypt said file
		encrypt(arg0)
		exit(0)

#Guess if we are encrypting or decrypting
elif(len(sys.argv) == 3):
	#Prepare arguments
	arg0 = sys.argv[1]
	arg1 = sys.argv[2]

	#Determine the argument entered
	if(arg0 == "encrypt"):
		encrypt(arg1)
	elif(arg0 == "decrypt"):
		decrypt(arg1)
	elif(arg0 == "wipe"):
		wipe(arg1)
	else: #Unknown know command
		print(f"ERROR: Unknown command '{arg0}'. Please run the script as follows: ")
		print_usage()

#Invalid number of arguments. Throw error.
else: 
	print("ERROR: Invalid number of arguments. Please run the script as follows: ")
	print_usage()
	exit(1) #Quit program



print("Complete.\n")