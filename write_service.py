"""
Windows Service wrapper for write.py
This allows the auto-typer to run as a Windows background service.
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import threading
from pathlib import Path

# Import the main typing function from write.py
import write


class WriterService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AutoWriterService"
    _svc_display_name_ = "Auto Writer Background Service"
    _svc_description_ = "Automated text typing service that runs in the background"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.worker_thread = None
        socket.setdefaulttimeout(60)

        # Configuration - modify these paths as needed
        self.script_dir = Path(__file__).parent.resolve()
        self.text_file = self.script_dir / "text.txt"
        self.config_file = self.script_dir / "service_config.txt"

    def SvcStop(self):
        """Called when the service is being stopped"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )

    def SvcDoRun(self):
        """Called when the service is started"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def load_config(self):
        """Load configuration from service_config.txt"""
        config = {
            'delay': 5.0,
            'min_interval': 0.02,
            'max_interval': 0.12,
            'randomize': True,
            'restart_on_completion': True,
            'restart_delay': 10.0
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                key = key.strip()
                                value = value.strip()

                                if key == 'delay':
                                    config['delay'] = float(value)
                                elif key == 'min_interval':
                                    config['min_interval'] = float(value)
                                elif key == 'max_interval':
                                    config['max_interval'] = float(value)
                                elif key == 'randomize':
                                    config['randomize'] = value.lower() in ('true', '1', 'yes')
                                elif key == 'restart_on_completion':
                                    config['restart_on_completion'] = value.lower() in ('true', '1', 'yes')
                                elif key == 'restart_delay':
                                    config['restart_delay'] = float(value)
                                elif key == 'text_file':
                                    self.text_file = Path(value)
            except Exception as e:
                servicemanager.LogErrorMsg(f"Error loading config: {e}")

        return config

    def run_typing_session(self, text, config):
        """Run a single typing session"""
        try:
            write.simulate_typing(
                text=text,
                initial_delay=config['delay'],
                min_interval=config['min_interval'],
                max_interval=config['max_interval'],
                randomize=config['randomize']
            )
            return True
        except Exception as e:
            servicemanager.LogErrorMsg(f"Error during typing session: {e}")
            return False

    def main(self):
        """Main service loop"""
        servicemanager.LogInfoMsg("Auto Writer Service is starting...")

        while self.running:
            try:
                # Load configuration
                config = self.load_config()

                # Load text to type
                if self.text_file.exists():
                    with open(self.text_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                    servicemanager.LogInfoMsg(f"Loaded text from {self.text_file}")
                else:
                    text = write.TEXT
                    servicemanager.LogInfoMsg("Using default text from write.py")

                if not text:
                    servicemanager.LogErrorMsg("No text to type. Waiting 30 seconds...")
                    time.sleep(30)
                    continue

                # Run typing session in a separate thread so we can respond to stop events
                success = self.run_typing_session(text, config)

                if not self.running:
                    break

                # If configured to restart, wait and continue
                if config['restart_on_completion']:
                    restart_delay = config['restart_delay']
                    servicemanager.LogInfoMsg(f"Typing completed. Restarting in {restart_delay} seconds...")

                    # Wait with ability to check stop event
                    for _ in range(int(restart_delay)):
                        if not self.running:
                            break
                        time.sleep(1)
                else:
                    # If not restarting, just wait for stop signal
                    servicemanager.LogInfoMsg("Typing completed. Waiting for new configuration...")
                    while self.running:
                        time.sleep(5)

            except Exception as e:
                servicemanager.LogErrorMsg(f"Unexpected error in service main loop: {e}")
                if self.running:
                    time.sleep(10)  # Wait before retrying

        servicemanager.LogInfoMsg("Auto Writer Service has stopped.")


def install_service():
    """Install the service"""
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WriterService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WriterService)


if __name__ == '__main__':
    install_service()
