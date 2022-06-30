import sys
import os
from enum import Enum
from colorama import Fore, Style

informational = """
   - I M P O R T A N T -

1) You must have pswm installed in your '/usr/bin/' directory.

2) Your csv file must be formatted as below,
   which is the default for Chrome, Brave and other browsers:

   <name>,<url>,<username>,<password>

3) This script also needs to modify 'pswm' by replacing the line:

   crypt_key = getpass.getpass("[pswm] Master password: ")

   with:

   crypt_key = input("[pswm] Master password: ")

   It will be reverted back to normal when the insertion is finished.
   This is set to happen automatically but may fail in some cases.

   If you already did it manually, press 'M' in the following prompt.
   Otherwise, select 'A'.
"""

pswm_install = "/usr/bin/pswm"
old_l = 'crypt_key = getpass.getpass("[pswm] Master password: ")'
new_l = 'crypt_key = input("[pswm] Master password: ")'


class Field(Enum):
    NAME = 0
    URL = 1
    USER = 2
    PASS = 3


class Mode(Enum):
    MANUAL = ["M", "m"]
    AUTO = ["A", "a"]
    QUIT = ["Q", "q"]


def replace(filename, old_line, new_line):
    """
    Replaces old_line with new_line in filename.

    Args:
        filename (str): Name of the file to perform the replacement on.
        old_line (str): Text to replace.
        new_line (str): Text to replace with.
    """
    wlines = []
    with open(filename, "r") as readfile:
        lines = readfile.readlines()
        for line in lines:
            if old_line in line:
                line = line.replace(old_line, new_line)
            wlines.append(line)

    with open(filename, "w") as writefile:
        writefile.writelines(wlines)


def restore(filename, old_line, new_line):
    """
    Replaces new_line with old_line in filename.

    Args:
        filename (str): Name of the file to perform the replacement on.
        old_line (str): Text to replace with.
        new_line (str): Text to replace.
    """
    wlines = []
    with open(filename, "r") as readfile:
        lines = readfile.readlines()
        for line in lines:
            if new_line in line:
                line = line.replace(new_line, old_line)
            wlines.append(line)

    with open(filename, "w") as writefile:
        writefile.writelines(wlines)


def simplify(name):
    """
    Gets rid of leading strings like 'www.'
    and trailing strings like '.com'.

    Args:
        name (str): Url to simplify.

    Returns:
        str: Simplified url.
    """
    if name.startswith("www."):
        ename = name.replace("www.", "")
    else:
        ename = name

    words = ename.split(".")
    ename = words[len(words) - 2]

    return ename


def check_format(line):
    """
    Checks if the line is correctly formatted.

    Args:
        line (str): Line to be checked.

    Returns:
        Boolean: True if the line is correctly formatted, False otherwise.
    """
    if len(line.split(",")) != 4 or line.startswith("name"):
        print("")
        print(Fore.RED + "Skipping invalid line:")
        print(line, end="")
        print(Style.RESET_ALL)
        return False
    return True


if __name__ == '__main__':

    # Read command line arguments
    if len(sys.argv) != 3:
        print("Usage: from_csv.py <csv_file> <master_password>")
        exit(1)
    master_password = sys.argv[2]
    filename = sys.argv[1]

    # Informational prompt
    print(informational)
    choice = input("([A]uto / [M]anual / [Q]uit) Enter your choice: ")
    if choice in Mode.QUIT.value:
        print("\nAborted.\n")
        exit(0)

    # Automatic replacement
    if choice not in Mode.MANUAL.value:
        replace(pswm_install, old_line=old_l, new_line=new_l)

    # Import each password in the csv file
    with open(filename, 'r') as file:

        for line in file:

            if not check_format(line):
                continue

            words = line.split(',')

            name = simplify(words[Field.NAME.value])
            url = words[Field.URL.value]
            user = words[Field.USER.value]
            passw = words[Field.PASS.value]

            command = 'echo ' + master_password \
                + ' | pswm ' + name + ' ' + user + ' ' + passw
            os.system(command)

    # Automatic restoration
    if choice not in Mode.MANUAL.value:
        restore(pswm_install, old_line=old_l, new_line=new_l)

    # Print success message
    print(Fore.GREEN + "\n- SUCCESS -\n")
