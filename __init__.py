import json, getpass
from ftplib import FTP, FTP_TLS

# FTP
def ftp_file_down(domain, remote_path, local_path, secure=True):
    ftp_files_down(domain, [remote_path], [local_path], secure)

def ftp_file_up(domain, remote_path, local_path, secure=True):
    ftp_files_up(domain, [remote_path], [local_path], secure)

def ftp_files_down(domain, remote_paths, local_paths, secure=True):
    ftp_files(domain, remote_paths, local_paths, 'down', secure)

def ftp_files_up(domain, remote_paths, local_paths, secure=True):
    ftp_files(domain, remote_paths, local_paths, 'up', secure)

def ftp_files(domain, remote_paths, local_paths, direction, secure=True):
    ftp = FTP_TLS(domain) if secure else FTP(domain)
    ftp.login(prompt_usr(), prompt_pw())
    
    if secure:
        ftp.prot_p()
    
    for remote_path, local_path in zip(remote_paths, local_paths):
        if direction.lower() == 'up':
            ftp.storbinary('STOR ' + remote_path, open(local_path, 'rb'))
        elif direction.lower() == 'down':
            ftp.retrbinary('RETR ' + remote_path, open(local_path, 'wb').write)
        else:
            raise Exception('Invalid direction: ' + direction)
    
    ftp.quit()


# JSON
def load_json_file(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)

def save_json_file(obj, path):
    with open(path, 'w') as json_file:
        json.dump(obj, json_file, sort_keys=True, indent=4)


# Interactive Prompts
def prompt(msg, default=None):
    if default:
        msg += " ['" + default + "']"
    return raw_input(msg + ': ') or default

def prompt_bool(msg, default=None):
    if default == True:
        default = 'yes'
    elif default == False:
        default = 'no'
    
    while True:
        response = prompt(msg + ' (yes/no)', default)
        if response:
            break
        else:
            print('Please types \'yes\' or \'no\'')
    
    return response.lower() == 'yes'

def prompt_usr(default=None):
    default = default or getpass.getuser()
    return raw_input("Username ['" + default + "']: ") or default

def prompt_pw():
    return getpass.getpass()