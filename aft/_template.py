#!/usr/bin/env python3


import os
import yaml

DOT = os.path.expanduser('~/.aft/')


def restore_template(group, name):
    """Restores a config to the proper directories and fills the placeholder
    variables.
    
    :group: The name of the group.
    :name: The name of the config.
    :returns: None

    """
    yaml_path = '{}templates/{}/{}.yaml'.format(DOT, group, name)

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
