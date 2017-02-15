#!/usr/bin/env python3


import curses
import os
import shutil
import argparse
import sys
import random

import yaml
import urwid

from aft.ui import UI
from aft._template import restore_template


DEBUG = False
VERSION = '0.1.8'
DOT = os.path.expanduser('~/.aft/')


def deprint(text):
    """Prints text if it is in debug mode. Skips otherwise.
    
    :text: The text to print.
    :returns: None

    """
    if DEBUG:
        print( text )
    return None


def create_default():
    """Creates the defualt files and folder if they don't already exist
    """
    deprint('Checking for / Creating default directories and files.')
    folders = [DOT, '{}templates/'.format(DOT)]
    for folder in folders:
        if not os.path.exists(folder):
            deprint('Making: {}'.format(folder))
            os.mkdir(folder)
    return None


def create_group(group, files=[]):
    """Creates a group of configs, backs up files if they are passed in.
    
    :group: The group to create.
    :files: The files to backup into group/files/
    :returns: None

    """
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
    """Backups the files you specify. Optionally backs them up by force.

    :group: The name of the group to backup to.
    :files: A list of files to backup.
    :force: True if you want to force the backup, False otherwise.
    :returns: None

    """
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
    """Iterates through the directories and makes them if they don't exist.
    The same as mkdir -p
    
    :directory: The fullpath to make.
    :returns: None

    """
    split = directory.split('/')
    for index, item in enumerate(split):
        path = '/'.join(split[:index])
        if path == '':
            continue
        if not os.path.exists(path):
            os.mkdir(path)
    return None


def create_template(group, name):
    """Create a template config under a group name.
    
    :group: The group to create it under.
    :name: The name of the config.
    :returns: None

    """
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


def main():
    create_default()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', default=None, nargs='?')
    parser.add_argument('group', nargs='?')
    parser.add_argument('config', nargs='?')
    parser.add_argument('-f', '--files', nargs='*')
    args = parser.parse_args()

    if args.command is None:
        # Load up the UI

        ui = UI()
        ui.run()
        return None

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
