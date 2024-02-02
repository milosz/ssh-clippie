# ssh-clippie

## description

Small utility to check ssh client configuration.

## how it works

Default rules definition using YAML file.

```yaml
ssh-clippie:
  main_directory:
    condition: mandatory
    type: directory
    mode: "700"
    description: SSH client configuration directory
    file_types:
      - private_key
      - public_key
  files:
    - name: known_hosts
      condition: optional
      type: file
      mode: "600"
      description: list of host keys known to the user
    - name: known_hosts2
      condition: not expected
      type: file
      mode: "600"
      description: list of host keys known to the user, backup file
    - name: authorized_keys
      condition: optional
      type: file
      mode: "600"
      description: public keys that can be used to log in as this user
    - name: authorized_keys2
      condition: not expected
      type: file
      mode: "600"
      description: public keys that can be used to log in as this user, backup file
    - name: config
      condition: optional
      type: file
      mode: "600"
      description: user configuration file
    - name: environment
      condition: optional
      type: file
      mode: "600"
      description: additional environment variables
    - name: rc
      condition: optional
      type: file
      mode: "600"
      description: executed when the user logs in
    - name: config.d
      condition: optional
      type: directory
      mode: "700"
      description: configuration snippets
      file_types:
        - ascii_text
    - name: scripts.d
      condition: optional
      type: directory
      mode: "700"
      description: additional scripts
      file_types:
          - executable_script
    - name: agent.sock
      condition: optional
      type: socket
      mode: "600"
      description: SSH agent socket
  types:
    private_key:
      name: OpenSSH private key
      pattern: ".* private key$"
      mode: "600"
    public_key:
      name: OpenSSH public key
      pattern: ".* public key$"
      mode: "600"
    executable_script:
      name: executable script
      pattern: ".*script.*executable.*"
      mode: "700"
    ascii_text:
      name: ascii text file
      pattern: ".*ASCII text.*"
      mode: "600"
```
It will check main directory permissions, specific files, file types, and verify file types inside subdirectories. 
Simple and effective.

## usage

Display help information.

```
$ ssh-clippie 
Usage: ssh-clippie [OPTIONS]

  This script reads permissions definition from YAML file and performs checks
  against user ssh directory

Options:
  --verbose                       Verbose mode
  --quiet                         Quiet mode
  --explain                       Explain mode
  --ssh-directory DIRECTORY       Home directory  [default: /home/milosz/.ssh]
  --permissions-definition-file FILE
                                  Permissions definition YAML file
  --help                          Show this message and exit.
```

Explain rules.

```
$ ssh-clippie --explain
Main directory should have permissions set to 700 and can contain OpenSSH private key, OpenSSH public key.

known_hosts (list of host keys known to the user) file which is optional and should have permissions set to 600
known_hosts2 (list of host keys known to the user, backup file) file which is not expected
authorized_keys (public keys that can be used to log in as this user) file which is optional and should have permissions set to 600
authorized_keys2 (public keys that can be used to log in as this user, backup file) file which is not expected
config (user configuration file) file which is optional and should have permissions set to 600
environment (additional environment variables) file which is optional and should have permissions set to 600
rc (executed when the user logs in) file which is optional and should have permissions set to 600
config.d (configuration snippets) directory which is optional and should have permissions set to 700 and can contain ascii text file.
scripts.d (additional scripts) directory which is optional and should have permissions set to 700 and can contain executable script.
agent.sock (SSH agent socket) socket which is optional and should have permissions set to 600

OpenSSH private key matching file type ".* private key$" should have permissions set to 600.
OpenSSH public key matching file type ".* public key$" should have permissions set to 600.
executable script matching file type ".*script.*executable.*" should have permissions set to 700.
ascii text file matching file type ".*ASCII text.*" should have permissions set to 600.
```

Perform check using quiet mode using exit code to determine success or failure.

```
$ ssh-clippie --quiet
```

```
$ echo $?
0
```

Perform check using verbose mode.

```
$ ssh-clippie --verbose
Checking /home/milosz/.ssh directory

Success
$ echo $?
0
```

```
$ touch ~/.ssh/known_hosts2
$ ssh-clippie --verbose
Checking /home/milosz/.ssh directory

file /home/milosz/.ssh/known_hosts2 should not exist
Failed
$ echo $?
2
```


## development

Install a project in editable mode.

```
$ pip install --editable .
Defaulting to user installation because normal site-packages is not writeable
Obtaining file:///mnt/c/Users/milos/PycharmProjects/ssh-clippie
  Preparing metadata (setup.py) ... done
Requirement already satisfied: click==8.1.7 in /home/milosz/.local/lib/python3.10/site-packages (from ssh-clippie==0.8.3) (8.1.7)
Requirement already satisfied: python-magic==0.4.27 in /home/milosz/.local/lib/python3.10/site-packages (from ssh-clippie==0.8.3) (0.4.27)
Requirement already satisfied: pyyaml==6.0.1 in /home/milosz/.local/lib/python3.10/site-packages (from ssh-clippie==0.8.3) (6.0.1)
Installing collected packages: ssh-clippie
  Running setup.py develop for ssh-clippie
Successfully installed ssh-clippie-0.8.3
```

Execute tests.

```
$ python3 -m unittest --verbose ssh_clippie/tests/test_utils.py
test_check_permissions (tests.test_utils.Test) ... ok
test_display_file_types (tests.test_utils.Test) ... ok
test_exit_application (tests.test_utils.Test) ... ok
test_explain (tests.test_utils.Test) ... ok
test_get_file_type (tests.test_utils.Test) ... ok
test_get_permissions (tests.test_utils.Test) ... ok
test_load_permissions_definition (tests.test_utils.Test) ... ok
test_print_error_message (tests.test_utils.Test) ... ok
test_print_error_message_with_fix (tests.test_utils.Test) ... ok
test_print_header_quiet (tests.test_utils.Test) ... ok
test_print_header_verbose (tests.test_utils.Test) ... ok
test_print_message_quiet (tests.test_utils.Test) ... ok
test_print_message_verbose (tests.test_utils.Test) ... ok
test_set_ssh_directory (tests.test_utils.Test) ... ok
test_set_verbose_mode (tests.test_utils.Test) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.055s

OK
```
