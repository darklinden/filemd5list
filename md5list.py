#!/usr/bin/env python

import json
import os
import hashlib
import sys
import time
import shutil

def file_is_ok(file_path, timestamp):
    if file_path.find("files.txt") != -1 or file_path.find("update.txt") != -1:
        return False

    fi = os.stat(file_path)
    if fi.st_mtime != timestamp:
        print(file_path + " is new")
    return True
    # filename, file_extension = os.path.splitext(file_path)
    # if file_extension != "":
    #     return True
    # else:
    #     return False


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def __main__():
    # param
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("using md5list [src] [timestamp] to make md5 list")
        return

    file_name = "files.txt"
    folder_path = sys.argv[1]
    if len(sys.argv) > 2:
        timestamp = int(sys.argv[2])
    else:
        timestamp = int(time.time())

    print("path: " + folder_path + " time: " + str(timestamp))

    if os.path.isdir(folder_path):
        assets_dict = {}
        for root, dirs, files in os.walk(folder_path):
            sub_files = os.listdir(root)
            for fn in sub_files:
                file_path = root + "/" + fn
                if os.path.isfile(file_path):
                    if not file_is_ok(file_path, timestamp):
                        # print('skip ' + file_path)
                        continue

                    if len(root) > len(folder_path):
                        key_path = os.path.join(root[len(folder_path):], fn)
                    else:
                        key_path = fn

                    obj_dict = {}
                    obj_dict["len"] = os.path.getsize(file_path)
                    obj_dict["md5"] = md5(file_path)
                    obj_dict["timestamp"] = timestamp
                    assets_dict[key_path] = obj_dict

                    os.utime(file_path,(timestamp, timestamp))


        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            file_old = open(file_path, mode='rb')
            json_old = json.loads(file_old.read())
            json_new = json_old
            file_old.close()
        else:
            json_new = {}

        json_new["assets"] = assets_dict
        json_des = json.dumps(json_new, sort_keys=True, indent=4)

        file_new = open(file_path + '-tmp', mode='wb')
        file_new.write(json_des)
        file_new.close()

        if os.path.isfile(file_path):
            os.remove(file_path)
        shutil.move(file_path + '-tmp', file_path)

        print("Done")
    else:
        print("src is not folder")

__main__()
