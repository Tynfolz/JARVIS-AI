import subprocess
import threading


class RustpotterWake:

    def __init__(self):
        self.models = [
            "models/rustpotter/jarvis-default.rpw",
            "models/rustpotter/jarvis-community-1.rpw",
            "models/rustpotter/jarvis-community-2.rpw",
            "models/rustpotter/jarvis-community-3.rpw",
            "models/rustpotter/jarvis-community-4.rpw",
            "models/rustpotter/jarvis-community-5.rpw",
        ]

        self.triggered = False


    def start(self):

        cmd = [
            "rustpotter-cli",
            "spot",
            *self.models,
            "-t",
            "0.6"
        ]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )


        threading.Thread(
            target=self.read_output,
            daemon=True
        ).start()


    def read_output(self):

        for line in self.process.stdout:

            print(line.strip())

            if "Wakeword detection" in line:

                self.triggered = True

                print("🔥 JARVIS ACTIVATED")


    def is_triggered(self):

        if self.triggered:
            self.triggered = False
            return True

        return False

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------