# NVIDIA Power Limiter

A simple GUI app for setting NVIDIA GPU power limits on Linux using `nvidia-smi` commands.  

## Features

- **Power Limit Control**: Set GPU power limits from 0-1000W
- **Persistence Mode**: Option to make power limit changes permanent
- **Real-time Status**: Check current vs default power limits

## Requirements

- Linux system with **systemd**
- NVIDIA GPU with drivers installed
- `nvidia-smi` command available
- Python 3 with tkinter
- Root/sudo privileges

## Usage

- Run with sudo privileges:  
```bash
sudo python3 nvidia_power_limiter.py
```
- Or use the provided launcher script (change paths):  
```bash
./run.sh
```
- `Set Power Limit` with **unckecked** "Make permanent" checkbox will only affect the running session.
- `Set Power Limit` with **checked** "Make permanent" checkbox will also persist on reboot.

## Setup

- Copy `nvidia-persistence.service` to `/etc/systemd/system/` and make it executable:  
  `sudo chmod +x /etc/systemd/system/nvidia-persistence.service`
- Enable and start the service:  
  ```bash
  sudo systemctl enable nvidia-persistence.service
  sudo systemctl start nvidia-persistence.service
  ```
- Copy `set_gpu_power_limit.sh` to `/usr/local/bin/` and make it executable:  
  `sudo chmod +x /usr/local/bin/set_gpu_power_limit.sh`
- Edit `run.sh` to update the hardcoded paths for your system, then make it executable:  
  `chmod +x run.sh`
- (Optional) Edit or install the `.desktop` file for GUI launcher integration

## Screenshot
![NVIDIA Power Limiter Interface](2025-07-06-1751808507.png)
