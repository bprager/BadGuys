# BadGuys
Several Python scripts to keep bad guys out

## Components


- `add2blacklist.sh` - Bash script to add an ip address to an IP set in the Linux kernel for blacklisting
- `attack_monitor.py` - Curses based Python script to monitor recent presumed attacks
- `block_bad_guys.py` - Script to check an attack database for actors who tried more than 1,000 times and adds them to the ip blacklist
- `collectAttack.py` - Script reading a kern.log lease file and persists the recen 1000 iptables deny records (assumes that the records are not older than 12 months)
- `collect-attacks-py.service` - Runs `collectAttack.py` as service
- `whoAttacksMe.py` - Helper script to list attackers
- `update_logrotate.sh` - This script copies the logrotate configuration from the repository to `/etc/logrotate.d/` and sets the correct permissions. It needs to be run with root privileges.

## Git Hook Setup

This setup involves using a Git `post-commit` hook to automatically trigger the `update_logrotate.sh` script whenever changes are committed to the repository. 
This ensures that logrotate configurations are always up-to-date on the system with the correct (restricted) file permission to run.

### Installation Steps

1. **Clone the Repository:**

`git clone [repository-url] ~/Projects/BadGuys/`

1. **Install the Service**

1.1. Copy the Service File 

Copy the collect-attacks-py.service file to the /etc/systemd/system/ directory to make it available to systemd. 
This requires root privileges:

`sudo cp ~/Projects/BadGuys/collect-attacks-py.service /etc/systemd/system/`

1.1. Reload Systemd: 

Reload the systemd manager configuration to recognize the new service:

`sudo systemctl daemon-reload`

1.1. Enable the Service: 

Enable the service to start at boot:

`sudo systemctl enable collect-attacks-py.service`

1.1. Start the Service: 

Start the service immediately without rebooting:

`sudo systemctl start collect-attacks-py.service`

1.1. Check the Service Status: 

Verify that the service is running properly:

`sudo systemctl status collect-attacks-py.service`

1.1. Troubleshooting (Optional)

If the service fails to start, check the logs for errors:

`sudo journalctl -u collect-attacks-py.service`

1. **Make this Script Executable:**

`chmod +x update_logrotate.sh`
Ensure that the `update_logrotate.sh` script is executable


1. **Set Up the Post-Commit Hook:**
- Navigate to the `.git/hooks/` directory inside your local repository.
- Create or edit the `post-commit` file:
  ```
  vi .git/hooks/post-commit
  ```
- Add the following lines to `post-commit`:
  ```bash
  #!/bin/sh
  ~/Projects/BadGuys/update_logrotate.sh
  ```
- Make the `post-commit` hook executable:
  ```
  chmod +x .git/hooks/post-commit
  ```


### Note

- Ensure you have the necessary permissions to execute scripts and write to `/etc/logrotate.d/` on your system.
- The `update_logrotate.sh` script must be run as root, so consider this when setting up automated processes.

## Conclusion

By following these steps, you can automate the process of updating logrotate configurations across multiple instances when the repository is cloned and used on other machines. Ensure that all security practices are followed, especially when scripts involve root privileges.

