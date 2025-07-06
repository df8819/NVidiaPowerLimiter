import tkinter as tk
from tkinter import messagebox
import subprocess
import os


class NVidiaPowerLimiter:
    def __init__(self, root):
        self.root = root
        self.root.title("NVIDIA Power Limiter")
        self.root.geometry("700x860")
        # self.root.resizable(False, False)

        # Configure style
        self.root.configure(bg='#f0f0f0')

        # Main frame
        main_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(main_frame, text="NVIDIA GPU Power Limiter",
                               font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))

        # Power limit frame
        power_frame = tk.LabelFrame(main_frame, text="Power Limit Settings",
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=15, pady=15)
        power_frame.pack(fill=tk.X, pady=(0, 20))

        # Slider frame
        slider_frame = tk.Frame(power_frame, bg='#f0f0f0')
        slider_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(slider_frame, text="Power Limit (Watts):",
                 font=('Arial', 10), bg='#f0f0f0').pack(anchor=tk.W)

        # Power slider
        self.power_var = tk.IntVar(value=300)
        self.power_slider = tk.Scale(slider_frame, from_=0, to=1000,
                                     orient=tk.HORIZONTAL, variable=self.power_var,
                                     length=400, bg='#f0f0f0',
                                     command=self.update_entry_from_slider)
        self.power_slider.pack(fill=tk.X, pady=(5, 10))

        # Input field frame
        input_frame = tk.Frame(power_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(input_frame, text="Or enter value directly:",
                 font=('Arial', 10), bg='#f0f0f0').pack(anchor=tk.W)

        entry_frame = tk.Frame(input_frame, bg='#f0f0f0')
        entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.power_entry = tk.Entry(entry_frame, font=('Arial', 12), width=10)
        self.power_entry.pack(side=tk.LEFT)
        self.power_entry.bind('<KeyRelease>', self.update_slider_from_entry)

        tk.Label(entry_frame, text="Watts", font=('Arial', 10),
                 bg='#f0f0f0').pack(side=tk.LEFT, padx=(5, 0))

        # Update entry with initial slider value
        self.power_entry.insert(0, str(self.power_var.get()))

        # Permanent checkbox
        self.permanent_var = tk.BooleanVar()
        self.permanent_check = tk.Checkbutton(power_frame, text="Make permanent",
                                              variable=self.permanent_var,
                                              font=('Arial', 10), bg='#f0f0f0')
        self.permanent_check.pack(anchor=tk.W, pady=(0, 10))

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 20))

        # Set power limit button
        self.set_button = tk.Button(button_frame, text="Set Power Limit",
                                    command=self.set_power_limit,
                                    font=('Arial', 12, 'bold'),
                                    bg='#4CAF50', fg='white',
                                    padx=20, pady=10)
        self.set_button.pack(side=tk.LEFT, padx=(0, 10))

        # Check active limit button
        self.check_button = tk.Button(button_frame, text="Check Active Limit",
                                      command=self.check_active_limit,
                                      font=('Arial', 12, 'bold'),
                                      bg='#2196F3', fg='white',
                                      padx=20, pady=10)
        self.check_button.pack(side=tk.LEFT)

        # Center the button frame
        button_frame.pack_configure(anchor=tk.CENTER)

        # Status frame
        status_frame = tk.LabelFrame(main_frame, text="Status",
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=15, pady=15)
        status_frame.pack(fill=tk.BOTH, expand=True)

        # Status text area
        self.status_text = tk.Text(status_frame, height=8, width=70,
                                   font=('Courier', 10), bg='white',
                                   state=tk.DISABLED, wrap=tk.WORD)

        # Scrollbar for status text
        scrollbar = tk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)

        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial status
        self.log_status("NVIDIA Power Limiter initialized.")

        # Check sudo privileges at startup
        self.root.after(100, self.startup_checks)

    def check_sudo_privileges(self):
        """Check if the application has sudo privileges"""
        try:
            # Test sudo access by running a harmless command
            result = subprocess.run(['sudo', '-n', 'true'],
                                    capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def request_sudo_privileges(self):
        """Request sudo privileges from user"""
        try:
            # This will prompt for password if needed
            result = subprocess.run(['sudo', 'true'], timeout=30)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def startup_checks(self):
        """Check if running with root privileges"""
        import os

        if os.geteuid() != 0:
            self.log_status("ERROR: This application must be run with sudo privileges.")
            messagebox.showerror("Sudo Required",
                                 "This application requires root privileges to modify GPU power limits.\n\n"
                                 "Please run the application with:\n\n"
                                 "sudo python3 nvidia_power_limiter.py\n\n"
                                 "The application will now exit.")
            self.root.quit()
            return

        self.log_status("✓ Running with root privileges.")
        self.log_status("Ready to set power limits.")

        # Now check active limits
        self.check_active_limit()

    def update_entry_from_slider(self, value):
        """Update entry field when slider changes"""
        self.power_entry.delete(0, tk.END)
        self.power_entry.insert(0, value)

    def update_slider_from_entry(self, event):
        """Update slider when entry field changes"""
        try:
            value = int(self.power_entry.get())
            if 0 <= value <= 1000:
                self.power_var.set(value)
        except ValueError:
            pass  # Ignore invalid input

    def log_status(self, message):
        """Add message to status text area"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def run_nvidia_smi_command(self, command):
        """Execute nvidia-smi command and return output"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                    text=True, timeout=10)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def check_nvidia_smi_available(self):
        """Check if nvidia-smi is available"""
        returncode, stdout, stderr = self.run_nvidia_smi_command("nvidia-smi --version")
        return returncode == 0

    def get_gpu_count(self):
        """Get number of available GPUs"""
        returncode, stdout, stderr = self.run_nvidia_smi_command("nvidia-smi -L")
        if returncode == 0:
            return len([line for line in stdout.split('\n') if line.startswith('GPU')])
        return 0

    def set_power_limit(self):
        """Set power limit for GPU(s)"""
        try:
            power_limit = int(self.power_entry.get())
            if not (0 <= power_limit <= 1000):
                messagebox.showerror("Error", "Power limit must be between 0 and 1000 watts")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        # Check if nvidia-smi is available
        if not self.check_nvidia_smi_available():
            self.log_status("ERROR: nvidia-smi not found. Please install NVIDIA drivers.")
            messagebox.showerror("Error", "nvidia-smi not found. Please install NVIDIA drivers.")
            return

        # Get GPU count
        gpu_count = self.get_gpu_count()
        if gpu_count == 0:
            self.log_status("ERROR: No NVIDIA GPUs detected.")
            messagebox.showerror("Error", "No NVIDIA GPUs detected.")
            return

        self.log_status(f"Setting power limit to {power_limit}W for {gpu_count} GPU(s)...")

        success_count = 0
        for gpu_id in range(gpu_count):
            gpu_success = True

            # If permanent is checked, first enable persistence mode
            if self.permanent_var.get():
                pm_command = f"nvidia-smi -i {gpu_id} -pm 1"
                self.log_status(f"DEBUG: Executing persistence command: {pm_command}")

                returncode, stdout, stderr = self.run_nvidia_smi_command(pm_command)
                self.log_status(f"DEBUG: Persistence mode - Return code: {returncode}")
                if stderr.strip():
                    self.log_status(f"DEBUG: Persistence mode - STDERR: {stderr.strip()}")

                if returncode != 0:
                    self.log_status(f"✗ GPU {gpu_id}: Failed to enable persistence mode")
                    self.log_status(f"  Error: {stderr.strip()}")
                    gpu_success = False

            # Set power limit command
            pl_command = f"nvidia-smi -i {gpu_id} -pl {power_limit}"
            self.log_status(f"DEBUG: Executing power limit command: {pl_command}")

            returncode, stdout, stderr = self.run_nvidia_smi_command(pl_command)
            self.log_status(f"DEBUG: Power limit - Return code: {returncode}")
            if stdout.strip():
                self.log_status(f"DEBUG: Power limit - STDOUT: {stdout.strip()}")
            if stderr.strip():
                self.log_status(f"DEBUG: Power limit - STDERR: {stderr.strip()}")

            if returncode == 0 and gpu_success:
                success_count += 1
                persistence_text = " with persistence mode" if self.permanent_var.get() else ""
                self.log_status(f"✓ GPU {gpu_id}: Power limit set to {power_limit}W{persistence_text}")
            else:
                self.log_status(f"✗ GPU {gpu_id}: Failed to set power limit")
                if stderr.strip():
                    self.log_status(f"  Error: {stderr.strip()}")

        if success_count == gpu_count:
            permanent_text = " (permanent)" if self.permanent_var.get() else " (temporary)"
            self.log_status(f"SUCCESS: Power limit set to {power_limit}W for all GPUs{permanent_text}")
            self.log_status("-" * 50)
            messagebox.showinfo("Success", f"Power limit set to {power_limit}W for all GPUs{permanent_text}")
        elif success_count > 0:
            self.log_status(f"PARTIAL SUCCESS: Power limit set for {success_count}/{gpu_count} GPUs")
            messagebox.showwarning("Partial Success", f"Power limit set for {success_count}/{gpu_count} GPUs")
        else:
            self.log_status("FAILED: Could not set power limit for any GPU")
            messagebox.showerror("Error", "Failed to set power limit. Check the debug output above.")

    def check_active_limit(self):
        """Check current power limit settings"""
        if not self.check_nvidia_smi_available():
            self.log_status("ERROR: nvidia-smi not found.")
            messagebox.showerror("Error", "nvidia-smi not found. Please install NVIDIA drivers.")
            return

        # Query power limits
        command = "nvidia-smi --query-gpu=index,name,power.limit,power.default_limit --format=csv,noheader,nounits"
        returncode, stdout, stderr = self.run_nvidia_smi_command(command)

        if returncode != 0:
            self.log_status("ERROR: Failed to query GPU power limits")
            self.log_status(f"Error: {stderr.strip()}")
            messagebox.showerror("Error", "Failed to query GPU power limits")
            return

        self.log_status("Current GPU Power Limits:")
        self.log_status("-" * 50)

        lines = stdout.strip().split('\n')
        has_limits = False

        for line in lines:
            if line.strip():
                parts = [part.strip() for part in line.split(',')]
                if len(parts) >= 4:
                    gpu_id, gpu_name, current_limit, default_limit = parts[0], parts[1], parts[2], parts[3]

                    # Check if current limit differs from default
                    try:
                        current_val = float(current_limit)
                        default_val = float(default_limit)

                        if abs(current_val - default_val) > 1:  # Allow for small floating point differences
                            has_limits = True
                            self.log_status(f"GPU {gpu_id} ({gpu_name}):")
                            self.log_status(f"  Current Limit: {current_limit}W")
                            self.log_status(f"  Default Limit: {default_limit}W")
                            self.log_status("-" * 50)
                        else:
                            self.log_status(f"GPU {gpu_id} ({gpu_name}): No custom limit set ({current_limit}W)")
                    except ValueError:
                        self.log_status(f"GPU {gpu_id} ({gpu_name}): Unable to parse limits")

        if not has_limits:
            self.log_status("No custom power limits are currently active.")


def main():
    # Check if running on Linux
    if os.name != 'posix':
        print("Warning: This application is designed for Linux environments.")

    root = tk.Tk()
    app = NVidiaPowerLimiter(root)
    root.mainloop()


if __name__ == "__main__":
    main()