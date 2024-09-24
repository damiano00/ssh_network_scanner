import tkinter as tk
from tkinter import messagebox
import paramiko
import subprocess
import threading
import time
import sys
import platform

class SSHScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Scanner")
        self.root.geometry("400x300")

        # Create GUI components
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.pack()

        self.server_label = tk.Label(root, text="Server IP:")
        self.server_label.pack()

        self.server_entry = tk.Entry(root)
        self.server_entry.pack()

        self.connect_button = tk.Button(root, text="Connect and Scan", command=self.start_scan)
        self.connect_button.pack()

        self.time_label = tk.Label(root, text="Time Elapsed: 0 seconds")
        self.time_label.pack()

        self.output_text = tk.Text(root, wrap='word', height=10)
        self.output_text.pack(expand=True, fill='both')

        # Close and minimize buttons
        self.close_button = tk.Button(root, text="Close", command=root.quit)
        self.close_button.pack(side=tk.LEFT)

        self.minimize_button = tk.Button(root, text="Minimize", command=root.iconify)
        self.minimize_button.pack(side=tk.RIGHT)

    def check_linux(self):
        """Check if the operating system is Linux."""
        return platform.system() == "Linux"

    def check_nmap_installed(self):
        """Check if Nmap is installed."""
        try:
            subprocess.run(["nmap", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def install_nmap(self):
        """Install Nmap using apt."""
        try:
            messagebox.showinfo("Updating apt", "Updating apt...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            messagebox.showinfo("Upgrading apt", "Upgrading apt...")
            subprocess.run(["sudo", "apt", "upgrade"], check=True)
            messagebox.showinfo("Installing Nmap", "Nmap is not installed. Installing now...")
            subprocess.run(["sudo", "apt", "install", "-y", "nmap"], check=True)
            messagebox.showinfo("Installation Complete", "Nmap has been installed successfully.")
        except Exception as e:
            messagebox.showerror("Installation Error", str(e))
            sys.exit(1)

    def start_scan(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        server_ip = self.server_entry.get()

        if not username or not password or not server_ip:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        # Start the SSH connection and scanning in a separate thread
        threading.Thread(target=self.scan_network, args=(username, password, server_ip)).start()

    def scan_network(self, username, password, server_ip):
        try:
            # Connect to the server via SSH
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_ip, username=username, password=password)


            '''
            TODO: add these features, to fix
            # Check if Nmap is installed, if not, install it
            if not client.check_nmap_installed():
                self.install_nmap()

            # Check if the script is running on Linux
            if not self.check_linux():
                messagebox.showerror("Unsupported OS", "This script can only be run on Linux.")
                sys.exit(1)
            '''

            # Start the nmap scan command
            command = "sudo nmap -sn -PR -PA21,22,80,443 -oA gateway_scan 192.168.1.1/24"
            stdin, stdout, stderr = client.exec_command(command)

            # Update time elapsed in the GUI
            start_time = time.time()
            while not stdout.channel.exit_status_ready():
                elapsed_time = int(time.time() - start_time)
                self.update_time_label(elapsed_time)
                time.sleep(1)

            # Get the output
            output = stdout.read().decode()
            client.close()

            # Show output in the GUI
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, output)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_time_label(self, elapsed_time):
        self.time_label.config(text=f"Time Elapsed: {elapsed_time} seconds")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHScannerApp(root)
    root.mainloop()
