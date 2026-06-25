import os
from colorama import Fore, Style, init

init(autoreset = True)

file_path = input('Enter path to project folder: ')

if not os.path.exists(file_path):
	print(Fore.RED + 'Error:' + Style.RESET_ALL + ' The specified path does not exist.')
else:
	print(Fore.GREEN + 'Success:' + Style.RESET_ALL + ' Looking for fucked up UIDs')

