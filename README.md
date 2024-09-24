
# SSH Network Scanner

This repository contains a basic Python-based application that uses Tkinter for the graphical user interface (GUI) and Paramiko for SSH connections. The tool allows users to connect to a remote server via SSH, execute network scanning commands (such as nmap), and view the results directly within the app.
## Deployment

To deploy this project on Linux run

```bash
    sudo apt update
    sudo apt upgrade
    git clone https://github.com/damiano00/ssh_network_scanner.git
    cd <your-repository-directory>
    python3 -m venv venv
    pip3 install paramiko
```

If you want to get the .exe file run

```bash
    pip install pyinstaller
    pyinstaller --onefile hosts.py
```
## Author

- [@damiano00](https://www.github.com/damiano00)
