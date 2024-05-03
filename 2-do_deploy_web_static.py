#!/usr/bin/python3
"""
Fabric script that create and distribute an archive to a web server
"""
from fabric.api import put, run, env
from os.path import exists
env.hosts = ['35.174.184.65', '100.25.137.244']


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if exists(archive_path) is False:
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
