import os
import time
from colorama import Fore, Style, init

# /mnt/storagedrive/Game Dev/GodotGames/my-summer-at-sapphos-bathhouse

init(autoreset = True)

total = 0

file_path = input('Enter path to project folder: ')

if not os.path.exists(file_path):
	print(Fore.RED + 'Error:' + Style.RESET_ALL + ' The specified path does not exist.')
else:
	print(Fore.GREEN + 'Success:' + Style.RESET_ALL + ' Looking for fucked up UIDs')

files_with_uids = []
uids_to_fix = []
good_uids = {}

processed_count = 0
for root, dirs, files in os.walk(file_path):
	total = len(files)
	#print(f"\nScanning {len(files)} files in {file_path}")
	for i, file in enumerate(files, start=1):
		if file.endswith('.import'):
			files_with_uids.append(file)
		
		width = 40
		progress = i / total
		filled = int(progress * width)
		bar = Fore.LIGHTYELLOW_EX + '#' * filled + Fore.LIGHTBLACK_EX + '-' * (width - filled)
		if i == total:
			print(f"\r[{bar}] {Fore.LIGHTGREEN_EX}{i}/{total}{Style.RESET_ALL} files ({progress:.1%})", end="", flush=True)
		else:
			print(f"\r[{bar}] {Fore.LIGHTRED_EX}{i}/{Fore.LIGHTGREEN_EX}{total}{Style.RESET_ALL} files ({progress:.1%})", end="", flush=True)
		time.sleep(0.01)
	if total > 0:
		processed_count += 1
		print(f'\nProcessed{processed_count}')

print('All files processed')