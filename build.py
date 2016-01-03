#!/usr/bin/env python
# coding=utf-8


import os
import argparse
import json
import yaml
import codecs
from logbook import Logger
from os.path import exists

logging = Logger(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))
CWD_DIR = os.getcwd()
parser = argparse.ArgumentParser()


class OSType:

    WIN, LINUX, MACOSX, UNKNOWN = range(4)

    def __init__(self):
        pass

    @staticmethod
    def get_type():
        import platform
        system_name = platform.system()
        if system_name.lower() == 'windows':
            return OSType.WIN
        elif system_name.lower() == 'linux':
            return OSType.LINUX
        elif system_name.lower() == 'darwin':
            return OSType.MACOSX
        else:
            return OSType.UNKNOWN


def run_process(cmd_str, cwd=None):
    """
    run command
    cmd_str unicode string.
    """

    if OSType.WIN == OSType.get_type():
        cmd_str = cmd_str.encode('gbk')
    elif OSType.LINUX == OSType.get_type():
        cmd_str = cmd_str.encode('utf-8')
    elif OSType.MACOSX == OSType.get_type():
        cmd_str = cmd_str.encode('utf-8')
    else:
        raise RuntimeError("your os is not support.")

    logging.info('cmd: %s' % cmd_str)

    import subprocess
    close_fds = False if OSType.WIN == OSType.get_type() else True
    p = subprocess.Popen(cmd_str, shell=True, close_fds=close_fds, cwd=cwd)
    p.wait()
    return p.returncode


def _save_text_to_file(context, target_file):
    target_dir = os.path.dirname(target_file)
    if not exists(target_dir):
        os.makedirs(target_dir)

    with codecs.open(target_file, 'w', 'UTF-8') as target_handle:
        target_handle.write(context)


def yaml2json(yaml_file):
    if not os.path.isfile(yaml_file):
        logging.error('configure file is not file.')
        exit(-1)
    result_json_file = '%s.json' % os.path.abspath(yaml_file)
    config_yaml = yaml.load(open(yaml_file))
    config_json = json.dumps(config_yaml, indent=4, sort_keys=True)

    _save_text_to_file(config_json, result_json_file)
    return result_json_file


class Packer:

    def __init__(self):
        pass

    def build(self, build_file, var_file):
        if build_file is None or not exists(build_file):
            parser.print_help()
            return -1
        cmd_strs = ['packer', 'build']
        if var_file is not None and exists(var_file):
            cmd_strs.append(u'-var-file=%s' % yaml2json(var_file))

        cmd_strs.append(yaml2json(build_file))
        logging.info('packer build...')

        return run_process(' '.join(cmd_strs))


def main():
    parser.add_argument('-v', dest='var_file',
                        help='variable file. packer -var-file argument')
    parser.add_argument('-f', dest='build_file',
                        help='build file, packer build configure file.')

    args = parser.parse_args()

    if args.build_file is None:
        parser.print_help()
        exit(-1)

    packer = Packer()
    exit(packer.build(args.build_file, args.var_file))

if __name__ == '__main__':
    main()
