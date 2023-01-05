import os
import shutil
import subprocess

import version as vn

version = 'v' + vn.Version_Number()

if os.path.isdir('dist/VimeoLikes2Eagle_' + version) : shutil.rmtree('dist/VimeoLikes2Eagle_' + version)
os.mkdir('dist/VimeoLikes2Eagle_' + version)

shutil.copy('vimeolikes_2_eagle.py', 'dist/VimeoLikes2Eagle_' + version + '/vimeolikes_2_eagle.py')
shutil.copy('version.py', 'dist/VimeoLikes2Eagle_' + version + '/version.py')
shutil.copy('apikey.py', 'dist/VimeoLikes2Eagle_' + version + '/apikey.py')

#pyarmor == 7.6.0 pyinstaller == 5.6.2
subprocess.run('pyarmor pack -e "--onefile --exclude numpy --exclude pandas --icon=logo.ico" --clean --name VimeoLikes2Eagle dist/VimeoLikes2Eagle_' + version + '/vimeolikes_2_eagle.py')

shutil.copy('dist/VimeoLikes2Eagle_' + version + '/dist/VimeoLikes2Eagle.exe', 'dist/VimeoLikes2Eagle_' + version + '/VimeoLikes2Eagle.exe')

shutil.rmtree('dist/VimeoLikes2Eagle_' + version + '/dist')
shutil.rmtree('build')
os.remove('dist/VimeoLikes2Eagle_' + version + '/vimeolikes_2_eagle.py')
os.remove('dist/VimeoLikes2Eagle_' + version + '/version.py')
os.remove('dist/VimeoLikes2Eagle_' + version + '/apikey.py')

#with open('Readme.txt', encoding = 'UTF-8') as rm_reader : rm_text = rm_reader.read().replace(r'{version}', version)
#with open('dist/VimeoLikes2Eagle_' + version + '/Readme.txt', 'w', encoding = 'UTF-8') as rm_writer : rm_writer.write(rm_text)

print('\nComplete!')