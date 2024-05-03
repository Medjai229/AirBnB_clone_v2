#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generate a .tgz archive from the contents of the web_static"""
    time = datetime.now()
    appended_name = time.strftime("%Y%m%d%H%M%S")
    archive = "versions/web_static_" + appended_name + ".tgz"

    local("mkdir -p versions")

    if local("tar -cvzf {} web_static".format(archive)).failed is True:
        return None

    return archive
