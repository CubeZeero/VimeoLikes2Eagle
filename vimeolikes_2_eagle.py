# -*- coding: utf-8 -*-

import vimeo
import apikey
import time
from termcolor import colored, cprint
import colorama
import os
from tqdm import tqdm
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import sys
import time
import random
import requests
from InquirerPy import prompt
import base64
from io import BytesIO
import version

colorama.init()

def cprint_info(text):
    print(colored(' INFO ', 'white', 'on_light_green'), text)
    return

def cprint_info_tree(text, on_tree = True):
    if on_tree : print(' └─' + colored(' ! ', 'white', 'on_green'), text)
    if not on_tree : print('   ' + colored(' ! ', 'white', 'on_green'), text)
    return

def cprint_error(text):
    print(colored(' ERROR ', 'white', 'on_light_red'), text)
    return

def cprint_error_tree(text, on_tree = True):
    if on_tree : print(' └─' + colored(' ! ', 'white', 'on_red'), text)
    if not on_tree : print('   ' + colored(' ! ', 'white', 'on_red'), text)
    return

def cprint_question(text):
    print(colored(' ? ', 'white', 'on_light_green'), text)
    return

os.system('title VimeoLikes2Eagle v' + version.Version_Number())

title_figlet = '''
 ___ ___ __                        _____   __ __                 ______ _______               __        
|   |   |__|.--------.-----.-----.|     |_|__|  |--.-----.-----.|__    |    ___|.---.-.-----.|  |.-----.
|   |   |  ||        |  -__|  _  ||       |  |    <|  -__|__ --||    __|    ___||  _  |  _  ||  ||  -__|
 \_____/|__||__|__|__|_____|_____||_______|__|__|__|_____|_____||______|_______||___._|___  ||__||_____|
                                                                                      |_____|           
'''

cprint(title_figlet, 'cyan')
cprint('Tool to send all Vimeo likes to Eagle library!\n', 'cyan')
cprint('v'+ version.Version_Number(), 'cyan')
cprint('Developed by Cube', 'green')
cprint('https://github.com/CubeZeero/VimeoLikes2Eagle\n', 'green')

server_keep_running = True
authorization_server_port = 17856
authorization_code = ''

eagle_server_port_ex = 41593
eagle_server_port_no = 41595

try:
    chk_boot = requests.get('http://localhost:' + str(eagle_server_port_no) + '/api/application/info', timeout = 1)

except requests.exceptions.Timeout:
    cprint_error('Eagle is not running.')
    cprint_error_tree('Please start Eagle and then run it.')
    cprint_error_tree('Shuts down after 3 seconds.', on_tree = False)
    time.sleep(3)
    sys.exit()

# Created a function to select a folder, but the API did not provide a function to specify a folder :-C 
# I will comment out this function in case the API is added.
'''

eagle_folder_list_data = requests.get('http://localhost:' + str(41595) + '/api/folder/list')
eagle_folder_list_dict = eagle_folder_list_data.json()

eagle_folder_list_name = []
eagle_folder_list_id = []

cprint_info('Please select a save folder')

for _folder_name in eagle_folder_list_dict['data']:
    eagle_folder_list_name.append(_folder_name['name'])
    eagle_folder_list_id.append(_folder_name['id'])

eagle_list_questions = [
    {
        'type': 'list',
        'message': 'Select folder:',
        'qmark': '?',
        'choices': eagle_folder_list_name,
        'default': eagle_folder_list_name[0]
    },
]

select_folder_name = prompt(questions = eagle_list_questions)[0]

children_data = eagle_folder_list_dict['data'][int(eagle_folder_list_name.index(select_folder_name))]['children']
print()

while True:
    if not children_data : break

    eagle_folder_list_name = []
    eagle_folder_list_id = []

    for _folder_name in children_data:
        eagle_folder_list_name.append(_folder_name['name'])
        eagle_folder_list_id.append(_folder_name['id'])    
    
    select_folder_name_tmp = '- Use ' + select_folder_name + ' -'
    eagle_folder_list_name.append(select_folder_name_tmp)

    cprint_info('Sub-folders exist. Please select a save folder')
    cprint_info_tree('Selecting ' + colored(select_folder_name_tmp, 'green') + ' uses the previous parent hierarchy.')

    eagle_list_questions = [
        {
            'type': 'list',
            'message': 'Select folder:',
            'qmark': '?',
            'choices': eagle_folder_list_name,
            'default': eagle_folder_list_name[0]
        },
    ]

    select_folder_name = prompt(questions = eagle_list_questions)[0]
    print()

    if select_folder_name_tmp == select_folder_name : break

    if not children_data[int(eagle_folder_list_name.index(select_folder_name))]['children'] : break
    children_data = children_data[int(eagle_folder_list_name.index(select_folder_name))]['children']

'''

vimeoapi = vimeo.VimeoClient(key = apikey.CLIENT_ID(), secret = apikey.CLIENT_SECRET())
vimeo_authorization_url = vimeoapi.auth_url(['public', 'private'], 'http://localhost:' + str(authorization_server_port) + '/', state = random.randint(0,10000))

webbrowser.open(vimeo_authorization_url)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        global authorization_code
        global server_keep_running

        parsed_path = urlparse(self.path)
       
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<script>window.close();</script>')

        server_keep_running = False
        authorization_code = str(parse_qs(parsed_path.query)['code'][0])
    
    def log_message(self, format: str, *args) -> None:
        pass

server = HTTPServer(('localhost', authorization_server_port), MyHTTPRequestHandler)

cprint_info('Please allow access to the application through your browser.')

while server_keep_running:
    server.handle_request()

try:
    token, user, scope = vimeoapi.exchange_code(authorization_code, 'http://localhost:' + str(authorization_server_port) + '/')

except vimeo.auth.GrantFailed:
    cprint_error('Authorization Error')
    cprint_error_tree('Shuts down after 3 seconds.')
    time.sleep(3)
    sys.exit()

likes_list_url = []
likes_list_uri = []
likes_list_name = []
likes_list_picurl = []
likes_list_duration = []

unix_ts = int(time.time())

likes_data_raw = vimeoapi.get('/me/likes?page=1', params = {'fields': 'name,uri,first,last,pictures,link'})
likes_data_dict = likes_data_raw.json()
likes_data = likes_data_dict['data']

total = int(likes_data_dict['total'])
likes_lastpage_num = int(str(likes_data_dict['paging']['last']).replace('&fields=name%2Curi%2Cfirst%2Clast%2Cpictures%2Clink','').replace('/me/likes?page=',''))

cprint_info('Total like videos: ' + colored(str(total), 'green'))
cprint_info('Total like pages: ' + colored(str(likes_lastpage_num), 'green'))
cprint_info('Get all likes data. plz wait...')
cprint_info_tree('Depending on the number of pages, this may take some time.')

for cnt in tqdm(range(1, likes_lastpage_num + 1), leave = False):

    likes_data_raw = vimeoapi.get('/me/likes?page=' + str(cnt), params = {'fields': 'name,uri,first,last,pictures,duration,link'})
    likes_data_dict = likes_data_raw.json()
    likes_data = likes_data_dict['data']

    for likes_ in likes_data:
        likes_list_url.append(str(likes_['link']))
        likes_list_uri.append(str(likes_['uri']))
        likes_list_name.append(str(likes_['name']))
        likes_list_duration.append(str(likes_['duration']))

    for likes_cnt in range(len(likes_data)):
        likes_list_picurl.append(str(likes_data[int(likes_cnt)]['pictures']['base_link']) + '_960x540?r=pad')

    time.sleep(1)

cprint_info('Save all like videos. plz wait...')
cprint_info_tree('Depending on the number of likes, this may take some time.')

skip_num = 0
test_list = []

for tqdm_num, _likes_url, _likes_uri, _likes_name, _likes_picurl, _likes_duration in zip(tqdm(range(len(likes_list_url)), leave = False), likes_list_url, likes_list_uri, likes_list_name, likes_list_picurl, likes_list_duration):

    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    pic_data = requests.get(_likes_picurl)
    imagedata = base64.b64encode(BytesIO(pic_data.content).getvalue()).decode("ascii")
    imagedata = 'data:image/jpeg;base64,' + imagedata
    
    eagle_addVideo_params = {
        'version': '2.7.4',
        'type': 'save-url',
        'title': _likes_name,
        'url': _likes_url,
        'width': 960,
        'height': 540,
        'medium': 'vimeo',
        'videoID': _likes_uri.replace('/videos/', '').replace('/users/114704987/likes/', ''),
        'videoDuration': int(_likes_duration),
        'base64': imagedata
    }

    res = requests.post('http://localhost:' + str(eagle_server_port_ex) + '/', data = eagle_addVideo_params, headers = headers)

    time.sleep(1)

cprint_info('Complete!')
cprint_info_tree('Shuts down after 3 seconds.', on_tree = False)
time.sleep(3)
sys.exit()
