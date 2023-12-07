#!/usr/bin/python3
"""
Module Name: 2-do_deploy_web_static.py
Description: Provides Fabric tasks definition
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['54.197.78.222', '18.210.16.208']


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
    if put(archive_path, "/tmp/").failed:
        return False

    # Get `archive_path` without the extension
    compressed_file = archive_path.split("/")[1]
    archive_name = compressed_file.split(".")[0]

    # Make the destination directory
    destination_path = '/data/web_static/releases/'
    if run("mkdir -p {}{}/".format(destination_path, archive_name)).failed:
        return False

    # Uncompress the file on the remote server
    command = "tar -xzf {} -C {}"
    compressed_file = "/tmp/{}".format(compressed_file)
    full_archive_name_dir = "{}{}/".format(destination_path, archive_name)
    if run(command.format(compressed_file, full_archive_name_dir)).failed:
        return False

    # Remove the compressed file from where it was initially copied to
    if run("rm {}".format(compressed_file)).failed:
        return False

    # Move the uncompressed files to the appropriate location for serving
    if run("mv {0}web_static/* {0}".format(full_archive_name_dir)).failed:
        return False

    # Remove `web_static` directory in the `destination_path`
    if run("rm -rf {}web_static".format(full_archive_name_dir)).failed:
        return False

    # Remove precious created symbolic link for testing
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a new the symbolic link, linked to the new version of your code
    target = full_archive_name_dir
    link = '/data/web_static/current'
    if run("ln -s {} {}".format(target, link)).failed:
        return False

    print("New version deployed!")
    return True
