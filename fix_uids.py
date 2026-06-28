import os
import time
import re
from datetime import datetime
from colorama import Fore, Style, init

# /mnt/storagedrive/Game Dev/GodotGames/my-summer-at-sapphos-bathhouse

init(autoreset = True)

total = 0
pattern = r'uid://[A-Za-z0-9]+'
bad_uid_count = 0
uid_fix_count = 0

file_path = input('Enter path to project folder: ')
file_path = '/mnt/storagedrive/Game Dev/GodotGames/my-summer-at-sapphos-bathhouse'

if not os.path.exists(file_path):
	print(Fore.RED + 'Error:' + Style.RESET_ALL + ' The specified path does not exist.')
else:
	print(Fore.GREEN + 'Success:' + Style.RESET_ALL + ' Looking for fucked up UIDs')

files_with_uids = []
uids_to_fix = []
log_lines = []
#good_uids = {}

log_lines.append(f'Starting UID scan and fix on {datetime.now()} ...')
log_lines.append(f'Scanning {file_path} for .import files...')

processed_count = 0
#############################################################################
#------ Walk through all files in the directory and its subdirectories -----#
#############################################################################
for root, dirs, files in os.walk(file_path):
	total = len(files)
	if total > 0:
		pass
		#log_lines.append(f"Found {total} total files...")
	#print(f"\nScanning {len(files)} files in {file_path}")

###################################################
#------ Find all import files and their UIDs -----#
###################################################
	for i, file in enumerate(files, start=1):
		if file.endswith('.import'):
			#files_with_uids.append(os.path.join(root, file))
			temp_file_path = os.path.join(root, file)
			temp_save_path = '' #<------- used to find instances in other files where there may be a different UID
			temp_uid = ''		#<------- good UID
			with open(temp_file_path, 'r') as file_open:
				for line in file_open:
					if 'save_to_file/fallback_path' in line and 'slice' not in line:
						temp_save_path = line.split(' ')[1].strip().replace('"', '').replace(',', '')
					if 'save_to_file/path' in line:
						match = re.search(pattern, line)
						if match:
							temp_uid = match.group(0)
			if temp_save_path != '' and temp_uid != '':
				#good_uids[temp_save_path] = temp_uid
				log_lines.append(f'\n------ {temp_uid} - {temp_save_path}')

#############################################################################################################
#-------- Walk through all files again to find instances of temp_save_path and check for different UID -----#
#############################################################################################################
				for root2, dirs2, files2 in os.walk(file_path):
					for file2 in files2:
						if file2.endswith('.tscn'):
							file_check_bool = False
							with open(os.path.join(root2, file2), 'r', encoding='utf-8') as file_check:
								log_lines.append(f'checking: {os.path.join(root2, file2)} for bad UID')
								for line in file_check:
									if temp_save_path in line and temp_uid not in line:
										#print(f'found door cube in: ' + os.path.join(root, file))
										log_lines.append(f'Found bad UID for {temp_save_path}')
										log_lines.append(f'------ Good UID: {temp_uid} Bad UID: {line}')
										bad_uid_count += 1
										file_check_bool = True
										break
							if file_check_bool:
								#print(os.path.join(root, file))
								output_file = []
								with open(os.path.join(root2, file2), 'r') as file_open:
									log_lines.append(f'	Fixing: {os.path.join(root2, file2)}')
									for line in file_open:
										if temp_save_path in line:
											temp = line.split(' ')
											line_out = []
											for item in temp:
												if item.startswith('uid='):
													#print(re.sub(pattern, f'uid://{good_uids[key].replace('uid://', '')}', item))
													log_lines.append(f'Replaced {item} with {temp_uid}')
													uid_fix_count += 1
													line_out.append(re.sub(pattern, f'uid://{temp_uid.replace('uid://', '')}', item))
												else:
													line_out.append(item)
											output_file.append(' '.join(line_out))
										else:
											output_file.append(line)
								log_lines.append('Writing to ' + os.path.join(root2, file2))
								try:
									with open(f'uid_fix_log_{datetime.now().strftime("%Y%m%d")}.log', 'w') as log_writer:
										for log_line in log_lines:
											log_writer.write(log_line + '\n')
								except Exception as e:
									print(Fore.RED + 'Error' + Style.RESET_ALL + ' writing log file: ' + str(e))
								#----- WRITE OUT FIXED FILE -------------------------------#
								with open(os.path.join(root2, file2), 'w') as write_out:
									write_out.writelines(output_file)
								#print('Done writing out ' + os.path.join(root, file))
		
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

print(f'{bad_uid_count} total bad UIDs found')
print(f'{uid_fix_count} UIDs fixed')
print('All files processed')
"""
for key in good_uids:
	print(key + ' : ' + str(good_uids[key]))
	if 'SapphosMansionBedroomDoorR_Cube_126.res' in key:
		print(key + ' : ' + str(good_uids[key]))
		for root, dirs, files in os.walk(file_path):
			for file in files:
				if file.endswith('.tscn'):
					file_check_bool = False
					with open(os.path.join(root, file), 'r') as file_check:
						for line in file_check:
							if 'SapphosMansionBedroomDoorR_Cube_126.res' in line:
								print(f'found door cube in: ' + os.path.join(root, file))
								file_check_bool = True
								break
					if file_check_bool:
						#print(os.path.join(root, file))
						output_file = []
						with open(os.path.join(root, file), 'r') as file_open:
							for line in file_open:
								if key in line:
									temp = line.split(' ')
									line_out = []
									for item in temp:
										if item.startswith('uid='):
											print(re.sub(pattern, f'uid://{good_uids[key].replace('uid://', '')}', item))
											line_out.append(re.sub(pattern, f'uid://{good_uids[key].replace('uid://', '')}', item))
										else:
											line_out.append(item)
									output_file.append(' '.join(line_out).strip())
								else:
									output_file.append(line.strip())
						
						with open(os.path.join(root, file), 'w') as write_out:
							for line in output_file:
								write_out.write(line + '\n')
						print('Done writing out ' + os.path.join(root, file)) """

