#! /bin/bash

# Author: Yoseph Alabdulwahab
# Description: 	
#	A tool to encrypt/decrypt a file and securely wipe the unencrypted source file from the drive.
#	This tool was made to encrypt password manager exports so that the original export is retrievable.
#	GPG encryption is used, as well as the wipe linux package.
#
# Usage - ./secure-encrypt.sh [filename <optional>]
# 
# Notes on usage:
#	if filename does not end with .gpg extension then it will attempt to encrypt it. 
#	However if it does end with .gpg extension then it will attempt to decrypt it 

echo "UPDATE: A cross OS python version of this script is availble. Check it out (https://github.com/yoseph1998/secure-encrypt)."

does_package_exist () { 
	package=$1
	if ! which $package >/dev/null; then #gpg is not installed. Install it.
		echo "Dependency $package not installed. Installing..."
		#Find a package manager and install gpg using it
		if which pacman >/dev/null; then
			sudo pacman -S $package
			return 0
		elif which apt-get >/dev/null; then
			sudo apt-get install $package
			return 0
		else
			echo "No supported package manager installed on system. (pacman, apt-get)"
			echo "Please install gpg then run this script again."
			return 1
		fi
	fi
}



#Check if gpg installed correctly and is usable.
#If so select the desired file and encrypt
if does_package_exist gpg; then
	if ! [ -z "$1" ] && [ -e "$1" ]; then #input is given, set to filename
		filename=$1
	else #Ask for a filename
		read -e -p "Enter filepath / filename: " filename
	fi
	if ! [ -e "$filename" ]; then
		echo "The file/filepath you specified does not exist. Please double check that and try again."
		exit 1
	else
		#determine if we are encrypting or decrypting
		if [[ ${filename: -4} == ".gpg" ]]; then #decrypting
			echo ".gpg extension detected. Attempting to decrypt it..."
			gpg -o "${filename::-4}" -d "$filename"
			exit 0 #stop executing script to prevent secure deletion of encrypted input
		else #encrypting
			does_package_exist wipe #Prompt to install (if needed) wipe before we start encrypting
			echo "Encrypting source file ($filename)..."
			gpg -c "$filename"
			if ! [ -e "${filename}.gpg" ]; then
				echo "Could not locate encrypted file. Skipping secure wipe of source file"
				exit 1
			fi
		fi
	fi
fi

#Check if gpg installed correctly and is usable.
#If so select the desired file and encrypt
if does_package_exist wipe; then
	#Warn user if using an SSD
	[[ $(df "$filename") =~ sd[a-z] ]]; #Look for sdX in output of df .
	isRota=$(cat /sys/block/${BASH_REMATCH[0]}/queue/rotational) #Run rotery check. 1 is hdd 0 is ssd
	if [ "$isRota" == 0 ]; then
		echo "WARNING: A secure delete is not possible on a SSD. For more information - https://github.com/yoseph1998/secure-encrypt"
	fi
	echo "Securely deleting source file..."
	wipe "$filename"
else
	echo "Could not securely wipe source file."
	exit 1
fi
