#!/usr/bin/env python3

"""
@file     pswm
@date     04/05/2023
@version  1.5
@change   1.5: Code linting
@license  GNU General Public License v2.0
@url      github.com/Julynx/pswm
@author   Julio Cabria
"""


import sys
import os
import random
import string
from contextlib import suppress
import getpass
import cryptocode
from prettytable import PrettyTable, SINGLE_BORDER


def _get_xdg_path(env: str,
                  app: str,
                  default: str,
                  create: bool = False) -> str:
    """
    Returns the value of the env environment variable with
    the app folder and file appended to it. (See example below)

    Example: Return value equals to
             "XDG_CONFIG_HOME/app/app"
             or
             "default/app/app" if XDG_CONFIG_HOME is not set

    Args:
        env (str): Name of the environment variable.
        app (str): Name of the app to be used for the folder and the file.
        default (str): Default value to use for the path if env
        is not set.
        create (bool): Wether to create the config file or not.
        Defaults to False. Dirs are always created if they don't exist.

    Returns:
        str: Path to the app folder and file or fallback value.
    """

    # 1. Read the XDG_config environment variable
    if env in os.environ and os.path.exists(os.environ[env]):
        config = os.environ[env]
    else:
        # Expand the default path
        config = os.path.expanduser(default)

    config = config[:-1] if config.endswith("/") else config

    # 2. Create the app folder if it doesn't exist
    config += f"/{app}"
    os.makedirs(config, exist_ok=True)

    # 3. Add the config file name to the path
    config += f"/{app}"
    if not os.path.exists(config) and create:
        with open(config, "w") as file:
            file.write("")

    return config


def get_xdg_data_path(app: str, create: bool = False) -> str:
    """
    Returns the value of the XDG_DATA_HOME environment variable with
    the app folder and file appended to it. (See example below)

    Example: Return value equals to
            "XDG_DATA_HOME/app/app"
            or
            "default/app/app" if XDG_DATA_HOME is not set

    Args:
        app (str): Name of the app to be used for the folder and the file.
        create (bool, optional): Wether to create the config file or not.
        Defaults to False. Dirs are always created if they don't exist.

    Returns:
        str: path to the app folder and file or fallback value.
    """
    return _get_xdg_path(env="XDG_DATA_HOME",
                         app=app,
                         default="~/.local/share",
                         create=create)


def args(positional=None):
    """
    Simple argument parser.

    Example:
    $: program joe 1234 -keep -host=127.0.0.1

    dictionary = args(["username", "password"])

    >> username:    joe
    >> password:    1234
    >> -keep:       True
    >> -host:       127.0.0.1

    Args:
        positional (str): A list of strings for the positional arguments.

    Returns:
        dict: A dictionary containing the argument names and their values.
    """
    positional = [] if positional is None else positional
    args_dict = {}

    # Store positional arguments
    tail = len(positional)
    for i, pos_arg in enumerate(positional):
        with suppress(IndexError):
            if str(sys.argv[i+1]).startswith("-"):
                tail = i
                break
            value = sys.argv[i+1]
            args_dict[pos_arg] = value

    # Store flags
    for i in range(tail+1, len(sys.argv)):
        try:
            value = str(sys.argv[i]).split("=")[1]
        except IndexError:
            value = True
        args_dict[str(sys.argv[i]).split("=", maxsplit=1)[0]] = value

    return args_dict


def print_pass_vault(pass_vault, alias=None):
    """
    Function to print the password vault using prettyTable.

    Args:
        pass_vault (dict): A dictionary of aliases associated to usernames
        and passwords.
        alias (str, optional): The alias to print.
        If None, all aliases are printed. Defaults to None.
    """
    if len(pass_vault) == 0:
        print("The password vault is empty.")
        return

    table = PrettyTable()
    if alias is not None:
        if alias in pass_vault:
            row = []
            row.append(alias)
            row.extend(pass_vault[alias])
            table.add_row(row)
        else:
            print("No password for " + alias + " was found.")
            return
    else:
        for stored_alias in sorted(pass_vault, key=lambda x: x[0].lower()):
            row = []
            row.append(stored_alias)
            row.extend(pass_vault[stored_alias])
            table.add_row(row)

    table.field_names = ["Alias", "Username", "Password"]
    table.align = "l"
    table.set_style(SINGLE_BORDER)
    print(table)


def register():
    """
    This function asks the user for a master password for the creation of a
    password vault.

    Returns:
        str, list: The master password and a list of lines containing the
        aliases, users and passwords for the password vault.
    """
    crypt_key = ""
    while len(crypt_key) < MIN_PASS_LENGTH or len(crypt_key) > MAX_PASS_LENGTH:
        try:
            crypt_key = getpass.getpass("[pswm] Create a master password (" +
                                        str(MIN_PASS_LENGTH) + "-" +
                                        str(MAX_PASS_LENGTH) +
                                        " chars): ")
        except KeyboardInterrupt:
            print("\n")
            return False, ""

    crypt_key_verify = ""
    while crypt_key_verify != crypt_key:
        try:
            crypt_key_verify = getpass.getpass("[pswm] Confirm your "
                                               "master password: ")
        except KeyboardInterrupt:
            print("\n")
            return False, ""

    print("Password vault ~/.pswm created.")
    lines = []
    lines.append("pswm\t" + getpass.getuser() + "\t" + crypt_key)
    return crypt_key, lines


def login():
    """
    This function decrypts and reads the password vault.

    Returns:
        str, list: The master password and a list of lines containing the
        aliases and passwords decrypted from the password vault.
    """
    for _ in range(3):

        try:
            crypt_key = getpass.getpass("[pswm] Master password: ")
        except KeyboardInterrupt:
            print("\n")
            return False, ""

        lines = encrypted_file_to_lines(PASS_VAULT_FILE, crypt_key)
        if not lines:
            print("Sorry, try again.")
        else:
            return crypt_key, lines

    print("\nYou have failed to enter the master password 3 times.")
    return reset_master_password()


def manage_master_password():
    """
    Manager function for the master password. Asks the user for the master
    password if there is already a password vault. If not, it creates a new
    password vault associated to a new master password. Can also reset the
    master password after 3 failed attempts.

    Returns:
        str, list: The master password and a list of lines containing the
        aliases and passwords decrypted from the password vault.
    """
    if not (os.path.isfile(PASS_VAULT_FILE)
            and os.path.getsize(PASS_VAULT_FILE) > 0):
        return register()
    return login()


def reset_master_password():
    """
    Function to reset the master password.

    Returns:
        str, list: The master password and a list of lines containing the
        aliases and passwords decrypted from the password vault.
    """
    print("Resetting your master password will delete your password vault.")
    try:
        text = input(
            "[pswm] Do you want to reset your master password? (y/n): ")
    except KeyboardInterrupt:
        print("\nPassword reset aborted.")
        return False, ""

    if text == "y":
        if os.path.isfile(PASS_VAULT_FILE):
            os.remove(PASS_VAULT_FILE)
            print("Password vault ~/.pswm deleted.\n")
        return manage_master_password()

    print("Password reset aborted.")
    return False, ""


def lines_to_pass_vault(lines):
    """
    Splits each line of a list of lines into two parts. Then inserts the second
    part into the dictionary indexed by the first part.

    Args:
        lines(list): A list of lines.

    Returns:
        dict: A dictionary containing the aliases, usernames and passwords.
    """
    pass_vault = {}
    for line in lines:
        line = line.rstrip()
        try:
            alias, username, password = line.split('\t')
            pass_vault[alias] = [username, password]
        except ValueError:
            pass

    return pass_vault


def pass_vault_to_lines(pass_vault):
    """
    For each key in the dictionary, it inserts a string into a list containing
    the key and the values separated by a tab.

    Args:
        pass_vault(dict): A dictionary aliases associated to usernames
        and passwords.

    Returns:
        list: A list of lines each formatted as key\tvalue[0]\tvalue[1].
    """
    lines = ['\t'.join([alias, pass_vault[alias][0], pass_vault[alias][1]])
             for alias
             in pass_vault]

    return lines


def encrypted_file_to_lines(file_name, master_password):
    """
    This function opens and decrypts the password vault.

    Args:
        file_name (str): The name of the file containing the password vault.
        master_password (str): The master password to use to decrypt the
        password vault.

    Returns:
        list: A list of lines containing the decrypted passwords.
    """
    if not os.path.isfile(file_name):
        return ""

    with open(file_name, 'r') as file:
        encrypted_text = file.read()

    decrypted_text = cryptocode.decrypt(encrypted_text, master_password)
    if decrypted_text is False:
        return False

    decrypted_lines = decrypted_text.splitlines()
    return decrypted_lines


def lines_to_encrypted_file(lines, file_name, master_password):
    """
    This function encrypts and stores the password vault.

    Args:
        lines (list): A list of lines containing the aliases and passwords.
        file_name (str): The name of the file to store the password vault.
        master_password (str): The master password to use to encrypt the
        password vault.
    """
    decrypted_text = '\n'.join(lines)
    encrypted_text = cryptocode.encrypt(decrypted_text, master_password)

    with open(file_name, 'w') as file:
        file.write(encrypted_text)


def generate_password(length):
    """
    This function generates a random password of length passed as argument.

    Args:
        length (int): The length of the random password to be generated.

    Returns:
        str: A string containing the random password.
    """
    characters = string.ascii_letters + string.digits + '%+,-./:=@^_{}~'
    return ''.join(random.choice(characters) for _ in range(length))


####################
# GLOBAL VARIABLES #
####################

HELP_MSG = '''
  pswm <alias> <user> <password>   - Store a username and a password.
  pswm <alias> <user> -g=<length>  - Store a random password for a username.
  pswm <alias> -d                  - Delete user and password for an alias.
  pswm <alias>                     - Print user and password for an alias.
  pswm -a                          - Print all stored users and passwords.
'''
MIN_PASS_LENGTH = 4
DEFAULT_PASS_LENGTH = 16
MAX_PASS_LENGTH = 32
PASS_VAULT_FILE = get_xdg_data_path("pswm")


def main():
    """
    Main function.
    """
    crypt_key, lines = manage_master_password()
    if not crypt_key:
        return

    pass_vault = lines_to_pass_vault(lines)
    arg = args(["site", "username", "password"])

    if ("password" in arg or "-g" in arg or "-d" in arg) \
            and (str(arg.get("site", "")) == "pswm"):
        print("You cannot change or delete the master password.")

    elif arg.keys() == {"site", "username", "password"}:
        pass_vault[arg["site"]] = [
            arg["username"], arg["password"]]
        print("Added username and password for " + arg["site"] + ".")

    elif arg.keys() == {"site", "username", "-g"}:
        try:
            length = int(arg["-g"])
            if length <= 4:
                raise ValueError
        except ValueError:
            length = DEFAULT_PASS_LENGTH
        pass_vault[arg["site"]] = [
            arg["username"], generate_password(length)]
        print_pass_vault(pass_vault, arg["site"])

    elif arg.keys() == {"site", "-d"}:
        try:
            del pass_vault[arg["site"]]
            print("Deleted username and password for " + arg["site"] + ".")
        except KeyError:
            print("No password found for " + arg["site"] + ".")

    elif arg.keys() == {"site"}:
        print_pass_vault(pass_vault, arg["site"])

    elif arg.keys() == {"-a"}:
        print_pass_vault(pass_vault)

    else:
        print(HELP_MSG)

    lines = pass_vault_to_lines(pass_vault)
    lines_to_encrypted_file(lines, PASS_VAULT_FILE, crypt_key)


if __name__ == "__main__":
    main()
