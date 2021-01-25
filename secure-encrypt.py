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
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "python-gnupg"])
	except:
		print("Cannot run pip. Please try installing python again http://python.org/")
		exit(1)
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
		print("ERROR: Could not open file '"+{filepath}+"'. Make sure you entered the correct file")
		quit(1)

# A method to decrypt a file using the provided password.
#
# filepath -> The path of the file to decrypt
# passwd -> The password to use for decrypting
#
# Output: Will create a file named [filepath]<minus the .gpg extension> containing the decrypted content
def decrypt_file(filepath, passwd):
	#init GnuPG
	gpg = gnupg.GPG()

	try:
		#Decrypt file with gpg decrypt. Will work with any valid gpg encryption scheme
		with open(filepath, 'rb') as file:
			gpg = gnupg.GPG()
			filepath_o = filepath[:-4]
			status = gpg.decrypt_file(file, passphrase=passwd, output=filepath_o)
	except FileNotFoundError:
		print("ERROR: Could not open file '"+{filepath}+"'. Make sure you entered the correct filepath")
		quit(1)

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
def validate_filepath(filepath, quit=False, debug=True):
	if(not isinstance(filepath, str)):
		return False
	elif(not path.exists(filepath)):
		if(debug):
			print("ERROR! File '"+{filepath}+"' does not exist. Please double check and try again")
		if(quit):
			exit(1) #Quit program
		return False
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
	print("\n   Usage:")
	print("      python {"+sys.argv[0]+"} <command> <filepath>")
	print("      or `alias` <command> <filepath>")
	print("\n   Commands:")
	print("      encrypt | -e    # Encrypt file and wipe")
	print("      decrypt | -d    # Decrypt file")
	print("      wipe    | -w       # Wipe\n")


# Wipe file
def wipe(filepath):
	#Validate filepath. Quit if does not exist
	validate_filepath(filepath, quit=True)

	#Give user warning on ssd and non standard filesystems
	print("Secure wiping file {filepath} ...")
	print("    WARNING: This only works on Windows/Linux on standard filesystems using a HDD. \
FILES MAY STILL BE RECOVERABLE ON SSDs.")

	#Wipe
	secure_delete.secure_random_seed_init()
	secure_delete.secure_delete(filepath)

#Encrypt file. Will also wipe it
def encrypt(filepath):
	#Validate filepath. Quit if does not exist
	validate_filepath(filepath, quit=True)

	#Get password
	passwd = get_password(asktwice = True)

	#Encrypt file
	print("Encrypting file '" + filepath + "'")
	status = encrypt_file(filepath, passwd)

	#Check if succeded
	if(status == False):
		print("Could not encrypt. Skipping secure.")
		exit(1) #Quit program

	#Wipe file
	wipe(filepath)

#Decrypt file
def decrypt(filepath):
	#Validate filepath. Quit if does not exist
	validate_filepath(filepath, quit=True)

	#Get password
	passwd = get_password()

	#Decrypt file
	print("Decrypting file '" + filepath + "'")
	decrypt_file(filepath, passwd)

###################################################################################################
## START OF SCRIPT ################################################################################
###################################################################################################

#Make sure gpg is installed
try:
	gnupg.GPG()
except:
	print("ERROR: Could not start GPG")
	print("Please make sure gpg is installed in the default location. For more info: https://gnupg.org/.")
	exit(0)

#Check if minimum arguments is provided
if(len(sys.argv) < 2 or len(sys.argv) > 3):
	print("ERROR: Invalid number of arguments. Please run the script as follows: ")
	print_usage()
	exit(1) #Quit program

arg0 = sys.argv[1]

#See if first arg is a command
if(arg0 == "encrypt" or arg0 == "-e"):
	if(len(sys.argv) != 3):
		print("ERROR: Filepath to encrypt not specified.")
		exit(1) #Quit program
	#Encrypt and Wipe file
	encrypt(sys.argv[2])
elif(arg0 == "decrypt" or arg0 == "-d"):
	if(len(sys.argv) != 3):
		print("ERROR: Filepath to decrypt not specified.")
		exit(1) #Quit program
	#Decrypt file
	decrypt(sys.argv[2])
elif(arg0 == "wipe" or arg0 == "-w"):
	if(len(sys.argv) != 3):
		print("ERROR: Filepath to wipe not specified.")
		exit(1) #Quit program
	#Wipe file
	wipe(sys.argv[2])

#See if first argument is a file
else: #Unknown know command
	print("WARNING: no command supplied. Trying to guess what you mean ...")
	arg0 = sys.argv[1]

	if(validate_filepath(arg0, debug=False)):
		#Decide between encrypting or decrypting
		if(arg0[-4:] == '.gpg'): #Decrypt file
			decrypt(arg0)
		else: #Encrypt said file
			encrypt(arg0)
	else:
		print("\nInvalid usage. Please run script as follows:")
		print("(If you meant to type a filename, then it does not exist)")
		print_usage()
		exit(1)


	

print("Complete.")