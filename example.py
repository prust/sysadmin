import os, shutil, sysadmin

class ExError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

try:
    # create test data
    if not os.path.exists('app'):
        os.makedirs('app/ui')
        os.makedirs('app/components')
    with open('app/ui/index.html', 'w') as htmlfile:
        htmlfile.write('<html></html>')
    with open('app/components/component1.py', 'w') as pyfile:
        pyfile.write('import this')
    
    # make a new folder for the update
    update_ver = sysadmin.prompt('Version')
    ver_path = 'v' + update_ver
    if os.path.exists(ver_path):
        raise ExError('Version ' + update_ver + ' already exists!')
    else:
        os.makedirs(ver_path)
    
    # copy UI & Python Components
    shutil.copytree('app/ui', ver_path + '/ui')
    
    if sysadmin.prompt_bool('Include Python components?', True):
        shutil.copytree('app/components', ver_path + '/components')
    
    # Zip
    shutil.make_archive('update-' + update_ver, 'zip', 'app')
    
    # upload to FTP server securely
    if sysadmin.prompt_bool('FTP to dev server?', True):
        local_path = 'update-' + update_ver + '.zip'
        remote_path = 'updates/' + local_path
        sysadmin.ftp_file_up('ftp.mycompany.com', remote_path, local_path)
    
except ExError as ex:
    print ex