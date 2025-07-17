# NVIDIA Power Limiter
A GUI for setting NVIDIA GPU Power Limits on Linux using `nvidia-smi` commands.  

## Features
- **Power Limit Control**: Set GPU power limits from 0-1000W
- **Persistence Mode**: Option to make power limit changes permanent
- **Real-time Status**: Check current vs default power limits

## Requirements
- Linux system with **systemd**
- NVIDIA GPU with drivers installed
- `nvidia-smi` command available
- Python 3 with tkinter
- sudo rights

## Usage
##### Run-Option 1:
cd into repo directory:  
```bash
	sudo python3 nvidia_power_limiter.py
```
##### Run-Option 2:
Use the provided launcher script from within repo directory:  
```bash
	./run.sh
```
##### Run-Option 3:
Use the .desktop link via launcher _(see Install/Setup)_
#### Settings:
- `Set Power Limit` with **🔲 unckecked** "Make permanent" checkbox will **only affect the running session**.
- `Set Power Limit` with **☑️ checked** "Make permanent" checkbox will also **persist on reboot**.

## Install/Setup
- sudo copy `nvidia-persistence.service` to `/etc/systemd/system/nvidia-persistence.service` and make it executable:
  ```bash
	sudo chmod +x /etc/systemd/system/nvidia-persistence.service
  ```
  - Enable, start and check the service:
  ```bash
    sudo systemctl enable nvidia-persistence.service
    sudo systemctl start nvidia-persistence.service
    sudo systemctl status nvidia-persistence.service
  ```
- sudo copy `set_gpu_power_limit.sh` to `/usr/local/bin/set_gpu_power_limit.sh` and make it executable:
```bash
	sudo chmod +x /usr/local/bin/set_gpu_power_limit.sh
```
- Make `run.sh` executable:
  ```bash
	chmod +x run.sh
  ```
- _(Optional)_ Edit the path and copy `nvidia-power-limiter.desktop` to `~/.local/share/applications/nvidia-power-limiter.desktop` file for launcher integration.

## Screenshot
![NVIDIA Power Limiter Interface](2025-07-06-1751808507.png "NVIDIA Power Limiter Interface")
