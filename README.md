# AFT File Templates

Create and store file templates.

Uses variables for different configs in each group.


# Installing

Requires: python3, python3-pip

```
git clone https://github.com/Sjc1000/aft
cd aft
pip3 install . --user
```

# Running

## Create a new group

`aft new group_name -f path/to/file/file1.txt other/path/file2.txt`

Create a new group and backup those files.. They will be stored in ~/.aft/templates/group_name/files/path/to/file/file1.txt

You will need to edit these and place $variables$  where you want aft to change settings. You will then place those $variables$ in different configs. (Explained in next step.)

You can use `aft files group_name -f more/things/tobackup.txt`  later on if needed.


## Create a config

use `aft edit group_name config_name`  to create / edit a new config. This is where you place your variables.

This is in yaml format. For example, adding something like


```yaml
background: "#000000"
```

will make a background variable usable when you load different configs, only in group_name though.

You will then need to place $background$  in the files you backed up earlier.


### More variable info


You can make a setup like this.

```yaml
terminal:
    background: "#000000"
```

and you can place $terminal.background$  in your files


## The reload script

Use `aft edit group_name reload`

To edit the reload script. This is a .sh script that will be run every time you change configs.

## The default.yaml

Use `aft edit group_name default`

To load the default settings, aft will check this for variables if it does not find them in the config you attempt to load.

So you can have global settings in here with custom settings in the other configs.


## Load a config

Run `aft load group_name config_name` to load a config. Or run aft with no params to load the UI.


