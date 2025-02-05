import os
import subprocess

import psutil
from dotenv import load_dotenv


class MinecraftServer:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MinecraftServer, cls).__new__(cls)
        return cls._instance

    def __init__(self, jar_path: str = "", memory="2048M"):
        if jar_path == "":
            load_dotenv()
            jar_path = os.getenv("JAR_PATH")
        if not hasattr(self, "proc"):  # Prevent re-initialization in singleton
            self.jar_path = jar_path
            self.memory = memory
            self.proc = None  # Store process reference

    def start_server(self):
        """Starts the Minecraft server"""
        if self.is_running():
            return "Server is already running!"

        self.proc = subprocess.Popen(
            [
                "java",
                f"-Xmx{self.memory}",
                "-Xms1024M",
                "-jar",
                self.jar_path,
                "nogui",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
            cwd=os.path.dirname(self.jar_path),
        )

        return f"Server started with PID {self.proc.pid}"

    def stop_server(self):
        """Stops the Minecraft server"""
        if not self.is_running():
            return "Server is not running!"

        self.proc.terminate()
        self.proc.wait()

        return "Server stopped successfully."

    def is_running(self):
        """Check if the Minecraft server is running"""
        if not self.proc:
            return False
        return self.proc.poll() is None  # None means still running

    def get_server_status(self):
        """Returns CPU & RAM usage of the Minecraft process"""
        if not self.is_running():
            return "Server is not running!"

        try:
            process = psutil.Process(self.proc.pid)
            cpu_usage = process.cpu_percent(interval=1)
            memory_info = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            return f"CPU Usage: {cpu_usage}%, RAM Usage: {memory_info:.2f} MB"
        except psutil.NoSuchProcess:
            return "Process not found."
