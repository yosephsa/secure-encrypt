# secure-encrypt
A tool that encrypts a file and securely deletes the source file, or decrypts a file encrypted with gpg semmytric encryption. It's dependencies are gpg and wipe.

To use the tool download the secure-encrypt.sh and run it in one of the following two ways.
1. ./secure-encrypt.sh [filename < optional >]
2. If you did not enter a file name you will then be asked to enter the filename. If the file is in the same directory you can just enter its name, however if it is in a different directory, please provide the full directory.
3. You will then be prompted to enter a password either to encrypt or decrypt. If the file ends with .gpg it will decrypt, otherwise it will encrypt
4. And your done.
