#!/usr/bin/env python3


import curses
import os
import shutil
import argparse
import sys
import random

import yaml


DEBUG = False
VERSION = '0.1.8'
DOT = os.path.expanduser('~/.aft/')


def deprint(text):
    if DEBUG:
        print( text )
    return None


def create_default():
    deprint('Checking for / Creating default directories and files.')
    folders = [DOT, '{}templates/'.format(DOT)]
    for folder in folders:
        if not os.path.exists(folder):
            deprint('Making: {}'.format(folder))
            os.mkdir(folder)
    return None


def create_group(group, files=[]):
    print('Creating group: {}'.format(group))
    path = '{}templates/{}/'.format(DOT, group)
    if os.path.exists(path):
        deprint('That already exists!')
    else:
        os.mkdir(path)
        os.mkdir('{}files/'.format(path))
        with open('{}reload.sh'.format(path), 'w') as f:
            f.write('# Reload script for {}'.format(group))
        with open('{}default.yaml'.format(path), 'w') as f:
            f.write('# Default variables.')
    create_group_backup(group, files)
    return None


def create_group_backup(group, files=[], force=False):
    print('Creating backup for: {}'.format(group))
    if files is None:
        print('No files added.')
        return None
    for directory in files:
        fullpath = os.path.expanduser(directory)
        if not fullpath.startswith('/'):
            fullpath = '/' + fullpath
        backup = os.path.expanduser('~/.aft/templates/{}/files{}'.format(group,
                 fullpath))
        print(backup)
        mkdir_recursive(backup)
        if os.path.exists(backup) and not force:
            continue
        shutil.copy(fullpath, backup)
    return None


def mkdir_recursive(directory):
    split = directory.split('/')
    for index, item in enumerate(split):
        path = '/'.join(split[:index])
        if path == '':
            continue
        if not os.path.exists(path):
            os.mkdir(path)
    return None


def create_template(group, name):
    print('Creating template: {} {}'.format(group, name))
    path = '{}templates/{}/{}.yaml'.format(DOT, group, name)
    deprint('Checking for: {}'.format(path))
    if not os.path.exists(path):
        deprint('Creating: {}'.format(path))
        with open(path, 'w') as f:
            f.write('# Write your variables here.\n')
    else:
        print('Already exists.')
    return None


def restore_template(group, name):
    yaml_path = '{}templates/{}/{}.yaml'.format(DOT, group, name)
    deprint('Loading config: {}'.format(yaml_path))

    with open(yaml_path, 'r') as f:
        yaml_conf = yaml.load(f.read())

    if yaml_conf is None:
        print('No config found for {}/{}'.format(group, name))
        return None
    
    with open('{}templates/{}/default.yaml'.format(DOT, group, name)) as f:
        default_conf = yaml.load(f.read())

    yaml_conf = flatten(yaml_conf)

    if default_conf is not None:
        default_conf = flatten(default_conf)

    # walk through the directory loading and changing the files.

    for root, paths, files in os.walk('{}templates/{}/files'.format(DOT, group)):
        if files == []:
            continue
        _, realpath = root.split('{}templates/{}/files'.format(DOT, group))
        backpath = root
        for name in files:
            file_real = os.path.join(realpath, name)
            file_back = os.path.join(backpath, name)
            if not os.path.exists(file_real):
                continue

            with open(file_back, 'r') as f:
                data = f.read()

            if default_conf is not None:
                for variable in default_conf:
                    if variable in yaml_conf:
                        continue
                    data = data.replace('${}$'.format(variable),
                           str(default_conf[variable]))
            
            for variable in yaml_conf:
                data = data.replace('${}$'.format(variable),
                       str(yaml_conf[variable]))
            if os.path.exists(file_real):
                os.remove(file_real)
            with open(file_real, 'w') as f:
                f.write(data)

    os.system('bash {}templates/{}/reload.sh'.format(DOT, group))
    return None


def flatten(iterable, key='', seperator='.'):
    items = []
    for index, value in iterable.items():
        new_key = key + seperator + index if key else index
        if isinstance(value, dict):
            items.extend(flatten(value, new_key, seperator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def main():
    create_default()

    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('group', nargs='?')
    parser.add_argument('config', nargs='?')
    parser.add_argument('-f', '--files', nargs='*')
    args = parser.parse_args()

    if args.command == 'load':
        if args.config == '$':
            files = os.listdir('{}templates/{}'.format(DOT, args.group))
            files = [x.replace('.yaml', '') for x in files if x.endswith('.yaml')]
            config = random.choice(files)
        else:
            config = args.config
        restore_template(args.group, config)
    if args.command == 'new':
        # Check if the group exists.
        create_group(args.group, args.files)
        create_template(args.group, args.config)
    if args.command == 'files':
        create_group_backup(args.group, args.files, True)
    if args.command == 'edit':
        editor = os.environ['EDITOR']
        ext = '.sh' if args.config == 'reload' else '.yaml'
        os.system('{} {}templates/{}/{}{}'.format(editor, DOT, args.group,
                  args.config, ext))
    if args.command == 'list' and args.group is not None:
        print('Listing files: ')
        files = os.listdir('{}templates/{}/'.format(DOT, args.group))
        files = [x for x in sorted(files) if '.' in x]
        for name in files:
            print('\t- {}'.format(name))
    return None


if __name__ == "__main__":
    main()
