# 🔒 Kali Security Setup

<div align="center">

![Kali Linux](https://img.shields.io/badge/Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Hardening-red?style=for-the-badge&logo=shield&logoColor=white)

**Automated security configuration and privacy hardening for Kali Linux**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security-configurations) • [License](#-license)

</div>

---

## 📋 Overview

Kali Security Setup is a comprehensive Python script that automates security hardening, privacy configurations, and essential application installation for Kali Linux. Perfect for penetration testers, security researchers, and privacy-conscious users who want a secure and optimized Kali Linux environment.

## ✨ Features

### 🛡️ Security Hardening

**MAC Address Randomization**
- Automatic random MAC address on every boot
- WiFi and Ethernet support
- NetworkManager integration
- Prevents device tracking and fingerprinting

**Volatile Logs (RAM-based)**
- System logs stored in RAM instead of disk
- Logs cleared automatically on shutdown/reboot
- Enhanced privacy - no persistent log traces
- Protects against forensic analysis

**Lid Switch Security**
- Automatic poweroff when laptop lid closes
- Works on battery and AC power
- Prevents unauthorized access
- Quick emergency shutdown capability

**Advanced Firewall (UFW)**
- Default deny all incoming connections
- ICMP/ping blocking (stealth mode)
- Outgoing connections allowed
- Protection against port scanning
- Network reconnaissance prevention

### 🎨 Customization

**Login Wallpaper Configuration**
- Custom login screen background
- Simple file path input
- Automatic backup of original
- Supports JPG, PNG, BMP, GIF formats

### 📦 Application Installer

**Privacy & Security Apps:**
- **Brave Browser** - Privacy-focused web browser with built-in ad blocking
- **Mullvad VPN** - Anonymous VPN with no logging policy
- **Proton VPN** - Secure VPN from Swiss privacy experts
- **Tor Browser** - Anonymous browsing through Tor network

**Communication:**
- **Discord** - Secure team communication
- **Telegram** - Encrypted messaging platform
- **ProtonMail Bridge** - End-to-end encrypted email client

**Development & Testing:**
- **VirtualBox** - Virtual machine management
- **Genymotion** - Android emulator for mobile testing

**Batch Installation** - Install all applications with one command

### 🧹 Deep System Cleaner

**Comprehensive cleanup tool that removes:**
- APT package cache (archives, lists)
- Orphaned packages and unused dependencies
- Residual configuration files
- System logs (journald + legacy logs)
- Temporary files (/tmp, /var/tmp)
- Thumbnail cache (all users)
- User trash bins (all users)
- Browser cache (Firefox, Chrome, Chromium)
- DNS cache (systemd-resolved, nscd, NetworkManager)
- Python bytecode cache (__pycache__, *.pyc)
- Bash/Zsh command history (optional)

**Benefits:**
- Frees up significant disk space
- Removes tracking artifacts
- Clears browsing history traces
- Enhances system privacy
- Improves system performance

### ⚡ System Updates

- Automated package list refresh
- Full system upgrade (apt upgrade + full-upgrade)
- Automatic cleanup of unused packages
- Progress indicators for long operations
- Error handling with detailed feedback

### 🎯 One-Click Configuration

**Configure All** - Apply all security settings at once:
- Random MAC address
- Volatile logs
- Lid switch poweroff
- Firewall with ICMP blocking
- Optional wallpaper customization

## 🚀 Installation

### Prerequisites

- Kali Linux (latest version recommended)
- Python 3.8 or higher
- Root/sudo privileges
- Internet connection

### Quick Start

```bash
# Clone the repository
git clone https://github.com/sofiaelena777/kali-security-setup.git
cd kali-security-setup

# Make executable
chmod +x kali_setup.py

# Run with root privileges
sudo python3 kali_setup.py
```

## 📖 Usage

### Interactive Menu

Run the script and choose from the interactive menu:

```bash
sudo python3 kali_setup.py
```

### Menu Options

```
1. Update System                      - Full system upgrade
2. Configure Random MAC Address       - Privacy enhancement
3. Configure RAM Logs (volatile)      - No persistent logs
4. Configure Lid Switch (Poweroff)    - Emergency shutdown
5. Configure Firewall (UFW + ICMP)    - Network protection
6. Configure Login Wallpaper          - Visual customization
7. Install Essential Applications     - Batch app installer
8. Deep System Clean                  - Privacy & space cleanup
9. Configure ALL at once              - One-click hardening
0. Exit                               - Quit script
```

## 🔒 Security Configurations

### MAC Address Randomization

**What it does:**
- Generates random MAC address on every boot
- Prevents tracking across networks
- Enhances anonymity on public WiFi

**Configuration file:** `/etc/NetworkManager/conf.d/00-macrandomize.conf`

**Verify:**
```bash
ip link show | grep ether
```

### Volatile Logs

**What it does:**
- Stores system logs in RAM (/run/log/journal)
- Logs disappear on reboot
- No persistent log files on disk

**Configuration file:** `/etc/systemd/journald.conf`

**Verify:**
```bash
journalctl --disk-usage
ls /run/log/journal
```

### Lid Switch Poweroff

**What it does:**
- System powers off when lid closes
- Works on battery and AC power
- Prevents unauthorized access

**Configuration file:** `/etc/systemd/logind.conf`

**Verify:**
```bash
systemctl show -p HandleLidSwitch
```

### Firewall + ICMP Blocking

**What it does:**
- Blocks all incoming connections
- Blocks ICMP (ping) requests
- Allows outgoing connections
- Makes system "invisible" to scanners

**Verify:**
```bash
sudo ufw status verbose
sysctl net.ipv4.icmp_echo_ignore_all
```

## 🧹 Deep Clean Details

### Disk Space Recovery

The deep clean typically frees:
- **100MB - 2GB** from APT cache
- **50MB - 500MB** from logs
- **100MB - 1GB** from browser cache
- **50MB - 300MB** from thumbnails
- **Variable** from trash bins and temp files

### Privacy Enhancement

Removes tracking artifacts:
- Web browsing history cache
- DNS query cache
- Command history (optional)
- Temporary session files
- Application usage logs

## 📦 Installed Applications

### Privacy Tools

**Brave Browser**
- Built-in ad/tracker blocking
- HTTPS Everywhere
- Fingerprinting protection
- Fast and lightweight

**Mullvad VPN**
- Anonymous account creation
- WireGuard protocol
- No logging policy
- Open source client

**Proton VPN**
- Secure Core architecture
- Swiss jurisdiction
- Kill switch feature
- Free tier available

**Tor Browser**
- Onion routing
- Maximum anonymity
- Pre-configured security
- Access to .onion sites

### Communication

**Discord** - Team collaboration and communication

**Telegram** - Encrypted messaging with secret chats

**ProtonMail Bridge** - End-to-end encrypted email

### Development

**VirtualBox** - Full virtualization with extension pack

**Genymotion** - Professional Android emulator

## 🛠️ Technical Details

### System Requirements
- Kali Linux 2020.1 or newer
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space
- Internet connection for updates/installs

### Dependencies
All dependencies are built into Python 3.8+:
- `subprocess` - Command execution
- `pathlib` - File system operations
- `threading` - Progress indicators
- `shutil` - File operations

### File Modifications

**Backup files created:**
- `/etc/systemd/journald.conf.bak`
- `/etc/systemd/logind.conf.bak`
- `/usr/share/desktop-base/kali-theme/login/background.bak`

**Configuration files modified:**
- `/etc/NetworkManager/conf.d/00-macrandomize.conf`
- `/etc/systemd/journald.conf`
- `/etc/systemd/logind.conf`
- `/etc/sysctl.conf`

## ⚠️ Important Notes

### Security Considerations

- **MAC Randomization**: May cause issues with MAC filtering on networks
- **Volatile Logs**: Debugging system issues becomes harder without persistent logs
- **Lid Switch**: Ensure you save work before closing lid
- **Firewall**: Some applications may require manual port opening

### Reversibility

Most configurations can be reverted:
```bash
# Restore original configs from backups
sudo cp /etc/systemd/journald.conf.bak /etc/systemd/journald.conf
sudo cp /etc/systemd/logind.conf.bak /etc/systemd/logind.conf

# Disable MAC randomization
sudo rm /etc/NetworkManager/conf.d/00-macrandomize.conf

# Disable firewall
sudo ufw disable
```

## 🐛 Troubleshooting

### "Permission denied" errors
```bash
# Ensure script is run with sudo
sudo python3 kali_setup.py
```

### NetworkManager not restarting
```bash
# Manually restart NetworkManager
sudo systemctl restart NetworkManager
```

### Firewall blocking needed services
```bash
# Allow specific port (example: SSH)
sudo ufw allow 22/tcp

# Check current rules
sudo ufw status numbered
```

### Applications not installing
```bash
# Update package lists first
sudo apt update

# Check internet connection
ping -c 3 8.8.8.8
```

## 📊 Comparison

| Feature | Before Setup | After Setup |
|---------|--------------|-------------|
| MAC Address | Static, trackable | Random per boot |
| System Logs | Persistent on disk | Volatile (RAM only) |
| Lid Action | Suspend/Sleep | Poweroff (secure) |
| Firewall | Inactive/Basic | Active + ICMP blocking |
| ICMP Response | Responds to ping | Stealth mode |
| Cache/Temp | Accumulates | Clean on demand |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional security configurations
- More application installers
- Automated security auditing
- Performance optimizations

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2024 sofiaelena777

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ⚠️ Disclaimer

This tool is provided for educational and legitimate security hardening purposes. Users are responsible for:
- Understanding each security configuration
- Ensuring compatibility with their network policies
- Backing up important data before use
- Complying with local laws and regulations

**The author is not responsible for any misuse or damages resulting from using this software.**

## 👤 Author

**sofiaelena777**

- GitHub: [@sofiaelena777](https://github.com/sofiaelena777)

## 🙏 Acknowledgments

- Kali Linux development team
- Open source security community
- NetworkManager and systemd developers
- Privacy-focused application developers

---

<div align="center">

**🔒 Secure by Default | 🕵️ Privacy First | ⚡ Easy to Use**

Made with ❤️ by sofiaelena777

</div>
