#! /bin/bash

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
	read -e -p "Enter filepath / filename: " filename
	if ! [ -e $filename ]; then
		echo "The file/filepath you specified does not exist. Please double check that and try again."
	else
		echo "Encrypting source file..."
		gpg -c $filename
		if ! [ -e "${filename}.gpg" ]; then
			echo "Could not locate encrypted file. Skipping secure wipe of source file"
			exit 1
		fi
	fi
fi

#Check if gpg installed correctly and is usable.
#If so select the desired file and encrypt
if does_package_exist wipe; then
	echo "Securely deleting source file..."
	wipe $filename
else
	echo "Could not securely wipe source file."
	exit 1
fi