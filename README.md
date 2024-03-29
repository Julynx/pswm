# pswm
*A simple command line password manager written in Python.*
<br><br>

<h4 align="center">Built to be secure, it encrypts your passwords with a key that only you know.</h4>
<p align="center">  
  <img width="772" src="https://i.imgur.com/IqHqajs.png">
</p>
<br>

<h4 align="center">Its intuitive syntax and its reduced set of commands make it easy to use.</h4>
<p align="center">  
  <img width="772" src="https://i.imgur.com/GPNoxX6.png">
</p>
<br>

<h4 align="center">It looks better than you might expect for a command-line application thanks to prettytable.</h4>
<p align="center">  
  <img width="772" src="https://i.imgur.com/Ie5UCvX.png">
</p>
<br>

## Dependencies
pswm uses [cryptocode](https://pypi.org/project/cryptocode/) & [prettytable](https://pypi.org/project/prettytable/) which can be installed through pip:
```
pip3 install cryptocode prettytable
```
It has been tested with Python 3.8.10, results may vary if other versions are used.
<br><br>

## Installation
The following commands will download the latest version of pswm from this repository 
and install it in your `/usr/bin/` directory:
```
git clone https://github.com/Julynx/pswm
cd pswm
```
```
sudo chmod +x pswm
sudo cp pswm /usr/bin/
```
The program can now be ran from a terminal with the command `pswm`.
<br><br>

## Usage
When running pswm for the first time, you will be prompted to define a master password that will be used to encrypt your other passwords. 

If you forget your master password, pswm will give you the option to reset it after three failed attempts. This would **delete** all your saved passwords since they would be encrypted with your old master password and impossible to decrypt without it. You should store your master password somewhere safe or choose something you will always remember.

After choosing a master password, a password vault will be created as an encrypted file named `pswm` inside `~/.local/share/pswm/`.
You can use any of the following commands to access your password vault:
```
pswm <alias> <user> <password>   - Store a username and a password.
pswm <alias> <user> -g=<length>  - Store a random password for a username.
pswm <alias> -d                  - Delete user and password for an alias.
pswm <alias>                     - Print user and password for an alias.
pswm -a                          - Print all stored users and passwords.
```
<br>

## Importing from CSV
You can use the included python script `from_csv.py` to import passwords from your browser into pswm:

- In Chrome, navigate to `Settings > Autofill > Passwords`. 

- Click on the three dotted menu to the right of *Saved Passwords* and select `Export passwords`.

- You can now execute the script to import all your passwords into pswm with the following command:
```
python3 from_csv.py <file.csv> <master_password>
```
<br>

## License
This software comes **without any warranty** as distributed under the [GNU GPL 2.0 license](https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html).

You should receive a copy of the license with your download of pswm.

