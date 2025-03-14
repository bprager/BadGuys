# BadGuys

Several Python scripts to monitor and defend against unauthorized access attempts on Linux systems.

## Components

- `add2blacklist.sh` - Adds an IP address to the Linux kernel's blacklist.
- `attack_monitor.py` - Curses-based monitoring tool for recent attack attempts.
- `block_bad_guys.py` - Automatically blocks IP addresses with excessive failed attempts.
- `collectAttack.py` - Parses kernel logs for recent `iptables` deny records and persists them.
- `collect-attacks-py.service` - Runs `collectAttack.py` as a systemd service.
- `whoAttacksMe.py` - Lists recent attackers for quick reference.
- `update_logrotate.sh` - Sets up and updates logrotate configurations for logs generated by these tools.

## Installation and Setup

Follow these steps to set up the repository after cloning.

### 1. Clone the Repository

```bash
git clone [repository-url] ~/Projects/BadGuys/
```

### 2. Configure Log Rotation

Make sure logs are rotated and maintained properly.

- Make the script executable:

```bash
chmod +x ~/Projects/BadGuys/update_logrotate.sh
```

- Run the script as root:

```bash
sudo ~/Projects/BadGuys/update_logrotate.sh
```

### 3. Set Up the Systemd Service

Install and manage the service that collects attack data:

- Copy service file:

```bash
sudo cp ~/Projects/BadGuys/collect-attacks-py.service /etc/systemd/system/
```

- Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable collect-attacks-py.service
sudo systemctl start collect-attacks-py.service
```

- Check the service status:

```bash
sudo systemctl status collect-attacks-py.service
```

### 4. Automate Logrotate Updates via Git Hook

Automatically update logrotate configurations upon committing changes:

- Create or edit the Git hook:

```bash
nano ~/Projects/BadGuys/.git/hooks/post-commit
```

- Add the following content:

```bash
#!/bin/sh
sudo ~/Projects/BadGuys/update_logrotate.sh
```

- Make the hook executable:

```bash
chmod +x ~/Projects/BadGuys/.git/hooks/post-commit
```

## Troubleshooting

- Check service logs for issues:

```bash
sudo journalctl -u collect-attacks-py.service
```

- Debug logrotate configuration:

```bash
sudo logrotate --debug /etc/logrotate.d/bad_guys_logs
```

## Security Best Practices

- Directory `/home/bernd/bin/` should have permissions set to `755`.
- Configuration files in `/etc/logrotate.d/` should have permissions set to `644` and ownership as `root:root`.

Following these steps ensures consistent, secure, and reliable operation across multiple systems.


