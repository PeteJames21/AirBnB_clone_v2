#!/usr/bin/python3
"""
Defines fabric tasks for deploying the AirBnB_clone_V2 project to
the remote servers.
"""
from fabric import task
import os
from datetime import datetime


@task
def do_pack(c):
    """Compress the pwd into an archive in the versions/ dir"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    dt = datetime.now()
    archive_name = f"web_static_{dt.year}{dt.month}{dt.day}{dt.hour}"\
                   f"{dt.minute}{dt.second}.tgz"
    # Files to be excluded from the archive
    excludes = "--exclude=versions --exclude=.git --exclude=.gitignore"
    # Compress all files in the pwd to the versions/ dir.
    result = c.run(f"tar {excludes} -czvf versions/{archive_name} .")
    return result.ok
