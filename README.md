# secure-encrypt
A tool that encrypts a file and securely deletes the source file, or decrypts a file encrypted with gpg semmytric encryption. It's dependencies are gpg and wipe.

**###Usage:**
1. download the secure-encrypt.sh file
2. Run it with `./secure-encrypt.sh [filename < optional >]`
3. If you did not enter a file name you will then be asked to enter the filename. If the file is in the same directory you can just enter its name, however if it is in a different directory, please provide the full directory.
4. You will then be prompted to enter a password either to encrypt or decrypt. If the file ends with .gpg it will decrypt, otherwise it will encrypt
5. And your done.

**###Create Alias:**
1. Move the file to a desired location. I placed mine inside my home directory.
2. run the following command alias `secenc="~/secure-encrypt.sh"`
3. Now you can following the steps under usgae, except instead of needing to be in the same directory and typing `./secure-encrypt.sh` you can istead type `secenc`
