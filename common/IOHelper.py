#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from shutil import copy


def WriteContentAndSave(file_path, content, mode='a'):
    fp = None

    try:
        CreateFolder(file_path)
        fp = open(file_path, mode)
        os.chmod(file_path, 0o666)
        fp.write(content)
    except Exception as e:
        print 'Exception: ' + str(e)
    finally:
        if fp is not None:
            fp.close()


def WriteLinesAndSave(file_path, lines, mode='a'):

    fp = None
    try:
        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        fp = open(file_path, mode)
        fp.writelines(lines)
    except Exception as e:
        print 'Exception: ' + str(e)
    finally:
        if fp is not None:
            fp.close()


def ReadContent(file_path):

    content = ""
    file_object = None

    try:
        file_object = open(file_path)
        content = file_object.read()
    finally:
        if file_object is not None:
            file_object.close()

    return content


def ReadLines(file_path):
    lines = []
    file_object = None

    try:
        file_object = open(file_path)
        lines = file_object.readlines()
    finally:
        if file_object is not None:
            file_object.close()

    return lines


def copy_file(source_file_path, des_file_path):
    try:
        folder = os.path.dirname(des_file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
            os.chmod(folder, 0777)

        if not os.path.exists(des_file_path):
            copy(source_file_path, des_file_path)
            os.chmod(des_file_path, 0o777)

    except Exception as e:
        print 'Exception: ' + str(e)


def DeleteFile(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print 'Exception: ' + str(e)


def CreateFolder(file_path):
    try:
        original_umask = os.umask(0)
        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.chmod(folder, 0o777)
    except Exception as e:
        print 'Exception: ' + str(e)
    finally:
        os.umask(original_umask)


def is_exist(file_path):
    return os.path.exists(file_path)


def find_path(file_folder, file_name):

    file_list = os.listdir(file_folder)
    for dir_info in file_list:
        file_path = os.path.join(file_folder, dir_info)
        if not os.path.isdir(file_path) and dir_info.find(file_name) > -1:
            return file_path

    return None
