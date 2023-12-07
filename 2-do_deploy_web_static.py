#!/usr/bin/python3
"""
Module Name: 2-do_deploy_web_static.py
Description: Provides Fabric tasks definition
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.user = "ubuntu"
env.hosts = ['54.197.78.222', '18.210.16.208']
env.key_filename = '~/.ssh/school'


def get_filename():
    """
    Get the filename format
    """
    formatted_date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"web_static_{formatted_date}.tgz"

    return filename


def do_pack():
    """
    Compress web_static directory
    """
    os.makedirs("versions", exist_ok=True)
    filename = get_filename()
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
    """
    if not os.path.exists(archive_path):
        return False
    # Copy the compressed file to the remote server
    status = put(archive_path, "/tmp/")
    if status.failed is True:
        return False

    # Get `archive_path` without the extension
    compressed_file = archive_path.split("/")[1]
    archive_name = compressed_file.split(".")[0]

    # Make the destination directory
    destination_path = '/data/web_static/releases/'
    status = run("mkdir -p {}{}/".format(destination_path, archive_name))
    if status.failed is True:
        return False

    # Uncompress the file on the remote server
    command = "tar -xzf {} -C {}"
    compressed_file = "/tmp/{}".format(compressed_file)
    archive_name_with_path = "{}{}/".format(destination_path, archive_name)
    status = run(command.format(compressed_file, archive_name_with_path))
    if status.failed is True:
        return False

    # Remove the compressed file from where it was initially copied to
    status = run("rm {}".format(compressed_file))
    if status.failed is True:
        return False

    # Move the uncompressed files to the appropriate location for serving
    status = run("mv {}web_static/* {}".format(archive_name_with_path,
                                               archive_name_with_path))
    if status.failed is True:
        return False

    # Remove `web_static` directory in the `destination_path`
    status = run("rm -rf {}/web_static".format(archive_name_with_path))
    if status.failed is True:
        return False

    # Remove precious created symbolic link for testing
    status = run("rm -rf /data/web_static/current")
    if status.failed is True:
        return False

    # Create a new the symbolic link, linked to the new version of your code
    target = archive_name_with_path
    link = '/data/web_static/current'
    status = run("sudo ln -s {} {}".format(target, link))
    if status.succeeded is True:
        print("New version deployed!")
        return True
    else:
        return False
