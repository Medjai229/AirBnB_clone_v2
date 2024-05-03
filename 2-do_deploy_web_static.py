#!/usr/bin/python3
"""
Fabric script that create and distribute an archive to a web server
"""
from datetime import datetime
from fabric.api import local, put, run, env
from os.path import exists
env.hosts = ['35.174.184.65', '100.25.137.244']


def do_pack():
    """Generate a .tgz archive from the contents of the web_static"""
    time = datetime.now()
    appended_name = time.strftime("%Y%m%d%H%M%S")
    archive = "versions/web_static_" + appended_name + ".tgz"

    local("mkdir -p versions")

    if local("tar -cvzf {} web_static".format(archive)).failed is True:
        return None

    return archive


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if exists(archive_path) is False:
        return False

    full_name = archive_path.split("/")[1]
    file_name = archive_path.split("/")[1],split(".")[0]

    if put(archive_path, "/tmp/{}".format(
           full_name)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(
           file_name)).succeeded is False:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(
           file_name)).succeeded is False:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
           full_name, file_name)).succeeded is False:
        return False

    if run("rm /tmp/{}".format(full_name)).failed is True:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(file_name, file_name)
           ).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(file_name)).failed is True:
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(file_name)).succeeded is False:
        return False

    return True
