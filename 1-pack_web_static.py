#!/usr/bin/python3
"""
Module Name: 1-pack_web_static.py
Description: Provides definition of `do_pack` function
"""
import os
from datetime import datetime
from fabric.api import env, local


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
