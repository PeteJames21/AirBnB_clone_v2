#!/usr/bin/python3
"""
Defines fabric tasks for deploying the AirBnB_clone_V2 project to
the remote servers.
"""
from fabric import task
from fabric import ThreadingGroup as Group
import os
from datetime import datetime

hosts = ["web1", "web2"]


@task
def do_pack(c):
    """Compress the pwd into an archive in the versions/ dir"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    dt = datetime.now()
    archive_name = f"web_static_{dt.year}{dt.month}{dt.day}{dt.hour}"\
                   f"{dt.minute}{dt.second}.tgz"
    print(f"[Creating archive: {archive_name}]")
    # Files to be excluded from the archive
    excludes = "--exclude=versions --exclude=.git --exclude=.gitignore"
    # Compress all files in the pwd to the versions/ dir.
    result = c.run(f"tar {excludes} -czvf versions/{archive_name} .")
    if not result.ok:
        return False
    print("[Archive created successfully]")

    return "versions/" + archive_name  # Return relative pathname of archive


@task
def do_deploy(c, archive_path):
    """Deploy an archive to web servers."""
    if not os.path.isfile(archive_path):
        print("Archive does not exist")
        return False

    print("[connecting...]")
    filename = os.path.basename(archive_path)
    group = Group(*hosts, user="ubuntu")
    # Upload archive to the /tmp/ dir of remote hosts
    results = group.put(archive_path, remote=f"/tmp/{filename}")
    if results.failed:
        print("Could not push archive to remote servers")
        return False

    print("[uncompressing archive]")
    # Uncompress the archive [remote]
    # Destination filename is same as archive_path but without the extension
    fout = os.path.basename(archive_path).split(".tgz")[0]
    fout = "/data/web_static/releases/" + fout
    group.run(f"rm -rf {fout}")  # Delete the dir if it already exists
    group.run(f"mkdir -p {fout}")
    result = group.run(f"tar -xzvf /tmp/{filename} -C {fout}")
    # Delete the archive
    group.run(f"rm /tmp/{filename}")
    if results.failed:
        print("extraction failed")
        return False

    print("[creating symlink ...]")
    # Delete the symlink from the server
    group.run(f"rm -f /data/web_static/current")
    # Create a new symlink based on the extracted archive
    results = group.run(f"ln -s {fout}/web_static /data/web_static/current")

    if results.failed:
        print("Symlink creation failed")
        return False

    print("[Deployment successful]")

    return True


@task
def deploy(c):
    """Create an archive and deploy it to the web servers."""
    archive_name = do_pack(c)
    return do_deploy(c, archive_name)


@task
def do_clean(c, number=0):
    """
    Delete out-of-date archives from the local host.

    If number is 0 or 1, keep only the most recent version. If 2, keep the
    most recent and the second most recent versions, etc. NOTE: the versions/
    directory is not pushed to the remote hosts by the deployment tasks, thus
    this task only modifies the filesystem of the local host.

    :param number: The number of the most recent archives to keep.
    """
    # Get list of relative pathnnames of archives.
    archives = [f"versions/{fname}" for fname in os.listdir("versions")]
    # Sort archives based on modification times (oldest to newest)
    archives = sorted(archives, reverse=False, key=lambda f: os.stat(f)[-1])

    # Keep the specified number of archives. Delete the rest.
    number = 1 if number == 0 else number
    for _ in range(number):
        archives.pop()
    for fname in archives:
        os.remove(fname)
