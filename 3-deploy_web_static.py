#!/usr/bin/python3
"""Fabric script that distributes archive web servers using do_deploy:"""

from fabric.api import *
import os
from datetime import datetime


env.hosts = ['54.82.173.246', '18.234.80.21']


def do_pack():
    """generate a .tgz archive from contents of web_static folder"""

    local('mkdir -p versions/')

    Current = datetime.now()
    Time = ""
    Time += "{}{}{}".format(Current.year, Current.month, Current.day)
    Time += "{}{}{}".format(Current.hour, Current.minute, Current.second)

    file_name = "versions/web_static_{}.tgz".format(Time)

    local('tar -cvzf {} web_static/'.format(file_name))
    return file_name


def do_deploy(archive_path):
    """Deploys a web_static into an IP after being called by deploy"""

    if os.path.exists(archive_path):

        put(archive_path, '/tmp/')

        archive_name = archive_path.split('/')[-1]
        archive = archive_name.split('.')[0]
        folder_name = '/data/web_static/releases/{}'.format(archive)

        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, folder_name))

        run('rm /tmp/{}'.format(archive_name))

        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))

        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    else:
        return False


def deploy():
    """distributes an archive to your web servers, using do_deploy"""

    Path = do_pack()
    print(Path)

    if Path:
        return do_deploy(Path)
    else:
        return False

    deploy()
