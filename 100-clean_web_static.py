#!/usr/bin/python3
"""
Module Name: 100-clean_web_static.py
Description: Provides Fabric tasks definition
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['54.160.96.3', '100.26.160.56']


def do_pack():
    """
    Compress web_static directory
    """
    os.makedirs("versions", exist_ok=True)
    formatted_date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"web_static_{formatted_date}.tgz"

    archive_path = f"versions/{filename}"

    print("Packing web_static to", archive_path)
    command = "tar -cvzf {} web_static"
    status = local(command.format(archive_path))

    archive_size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path,
                                                    archive_size))

    return archive_path if status.succeeded is True else None


def do_deploy(archive_path):
    """
    Deploy the archived directory to the servers

    Args:
        archive_path (str): The full path of the archived directory
                            to be deployed
    Return:
        True if succeeded, otherwise False
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Copy the compressed file to the remote server
        put(archive_path, "/tmp/")

        # Get `archive_path` without the extension
        compressed_file = os.path.basename(archive_path)
        archive_name = compressed_file.split(".")[0]

        # Make the destination directory
        destination_path = '/data/web_static/releases/'
        run("mkdir -p {}{}/".format(destination_path, archive_name))

        # Uncompress the file on the remote server
        command = "tar -xzf {} -C {}"
        compressed_file = "/tmp/{}".format(compressed_file)
        full_archive_name_dir = "{}{}/".format(destination_path, archive_name)
        run(command.format(compressed_file, full_archive_name_dir))

        # Remove the compressed file from where it was initially copied to
        run("rm {}".format(compressed_file))

        # Move the uncompressed files to the appropriate location for serving
        run("mv {0}web_static/* {0}".format(full_archive_name_dir))

        # Remove `web_static` directory in the `destination_path`
        run("rm -rf {}web_static".format(full_archive_name_dir))

        # Remove precious created symbolic link for testing
        run("rm -rf /data/web_static/current")

        # Create a new the symbolic link, linked to the new version of the code
        target = full_archive_name_dir
        link = '/data/web_static/current'
        run("ln -s {} {}".format(target, link))
    except Exception:
        return False

    print("New version deployed!")
    return True


def deploy():
    """
    Create and deploy the archive to the server
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Delete out-of-date archives

    Args:
        number (str): The number of archive(s) to keep. If zero, one is kept

    Return:
        None
    """
    number = int(number)
    if number < 0:
        return

    number = number if number > 0 else 1
    try:
        # Get all archives in the versions directory
        local_archives = local("ls -t versions", capture=True).split("\n")

        # Delete the unwanted archives
        for archive in local_archives[number:]:
            local(f"rm -r versions/{archive}")

        # Get all archives in `/data/web_static/releases` directory
        remote_archives = run("ls -t /data/web_static/releases").split()
        # Delete the unwanted archives
        for archive in remote_archives[number:]:
            if "web_static_" in archive:
                run(f"rm -r /data/web_static/releases/{archive}")
    except Exception:
        pass
