# secure-encrypt
A python tool to simplify the encryption and secure wiping of plaintext files as well as decrypting encrypted files.

#### Supported OS:
This tool is designed to run on Windows and Linux. It should also work on macOS, however it has not been tested.

#### Dependencies:
This script requires the following packages/programs to be installed: *pip* and *gpg*. If these packages are not installed this tool may not work properly.

#### Warning:
Due to the way SSDs are designed, a proper secure wipe on an SSD **is not possible**. For more information about the topic of SSDs and secure deletion here is an informative paper. https://www.cs.auckland.ac.nz/~pgut001/pubs/secure_del.html. Under the *Even Further Epilogue* is an explanation to why a secure wipe is not possible* on an SSD.

#### Usage:
1. Download the secure-encrypt.py file
2. Run it with `python secure-encrypt.py [filename]`
3. You will then be prompted to enter a password either to encrypt or decrypt. If the file ends with .gpg it will decrypt, otherwise it will encrypt
4. And your done.
5. If you do not enter a file name you will be shown the help page of the script, showing you the different ways you can use this script.


#### Create Alias (on linux):
1. Move the file to a desired location. I placed mine inside my home directory.
2. run the following command `alias secenc="python ~/secure-encrypt.py"`
3. Now you can following the steps under usgae, except instead of needing to be in the same directory and typing `python secure-encrypt.py` you can istead type `secenc ...`

---

If you find any issues or have any suggestions on how this can be improved. Please feel free to let me know by making a new issue on the github issues page https://github.com/yoseph1998/secure-encrypt/issues and I'll gladly take a look at it.

Hope this helps someone 👍
