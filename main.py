import logging
import os
import posixpath
import stat
from pathlib import Path
from typing import NamedTuple

import paramiko
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class Config(NamedTuple):
    host : str
    username : str
    password : str
    local_base : str
    remote_base : str

    @classmethod
    def load(cls):
        load_dotenv()
        return cls(
            os.getenv("HOST"),
            os.getenv("USERNAME"),
            os.getenv("PASSWORD"),
            os.getenv("LOCAL_BASE"),
            os.getenv("REMOTE_BASE"),
        )

def local_list_files_recursive(folder):
    files = []
    for root, dirs, filenames in os.walk(folder):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files

def remote_list_files_recursive(sftp, remote_path):
    files = []
    for entry in sftp.listdir_attr(remote_path):
        full_path = posixpath.join(remote_path, entry.filename)

        if stat.S_ISDIR(entry.st_mode):
            files.extend(remote_list_files_recursive(sftp, full_path))
        else:
            files.append(full_path)
    return files

def remove_base(files, base):
    files_without_base = []
    for file in files:
        split = file.split(base)
        if 1 < len(split):
            files_without_base.append(split[1])
    return files_without_base

def files_to_delete(local_files, remote_files, config):
    local_files_without_base = remove_base(local_files, config.local_base)
    remote_files_without_base = remove_base(remote_files, config.remote_base)
    files_to_delete = set(local_files_without_base) - set(remote_files_without_base)
    return files_to_delete

def files_to_download(local_files, remote_files, config):
    local_files_without_base = remove_base(local_files, config.local_base)
    remote_files_without_base = remove_base(remote_files, config.remote_base)
    files_to_download = set(remote_files_without_base) - set(local_files_without_base)
    return files_to_download

def remove_empty_folders(config):
    root = Path(config.local_base)
    for p in sorted(root.rglob("*"), reverse=True):
        if p.is_dir():
            try:
                p.rmdir()   # only removes if empty
            except OSError:
                pass

def main():
    config = Config.load()
    local_files = local_list_files_recursive(config.local_base)
    for_deletion = []
    with paramiko.Transport((config.host, 22)) as transport:
        transport.connect(username=config.username, password=config.password)
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            remote_files = remote_list_files_recursive(sftp, config.remote_base)
            files_to_downloadx = files_to_download(local_files, remote_files, config)
            for_deletion = files_to_delete(local_files, remote_files, config)
            for file in files_to_downloadx:
                local_file = config.local_base + file
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                logging.info(f"downloading file: {file}")

                sftp.get(config.remote_base + file, config.local_base + file)
    for file in for_deletion:
        logging.info(f"remove file {config.local_base + file}")
        os.remove(config.local_base + file)
    remove_empty_folders(config)


if __name__ == "__main__":
    main()
