#===================================================================================
# Description:
# 	This is a python script to encrypt and decrypt files for use as backup. 
# 	The encryption process also provides ability to securely wipe the plaintext file
# 	when possible.
# 
# Author: Yoseph Alabdulwahab
# 
# Copyright: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
#===================================================================================
import sys, subprocess

#Import packages that may need install.
try:
	import gnupg
except ImportError:
	subprocess.check_call([sys.executable, "-m", "pip", "install", "python-gnupg"])
	import gnupg
	print("\n")

def encrypt_file(filepath, passwd):
	#Open file and encrypt
	try:
		with open(filepath, 'r') as file:
			gpg = gnupg.GPG()
			#Encrypt file with AES256 and output to {filepath}.gpg
			status = gpg.encrypt(file, symmetric='AES256', passphrase=passwd, armor=False, encrypt=False, output=filepath+'.gpg')
	except FileNotFoundError:
		print(f"ERROR: Could not open file '{filepath}'. Make sure you entered the correct file")
		return False #Abort function

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
			filepath_o = filepath[:-4]+".out"
			status = gpg.decrypt_file(file, passphrase=passwd, output=filepath_o)
			print(status.stderr)
	except FileNotFoundError:
		print(f"ERROR: Could not open one or more files ('{filepath}', '{filepath_o}'). Make sure you entered the correct file")
		return False #Abort function


encrypt_file("ignore.testfile.text", "test")
decrypt_file("ignore.testfile.text.gpg", "test")



