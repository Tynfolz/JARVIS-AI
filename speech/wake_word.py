import subprocess


class WakeWord:

    def __init__(self):

        self.process = subprocess.Popen(
            [
                "rustpotter-cli",
                "spot",
                r"D:\jarvis\models\rustpotter\jarvis-default.rpw",
                "-t",
                "0.65",
                "-m",
                "5",
                "-e"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        print("🟢 Rustpotter READY")


    def listen(self):

        line = self.process.stdout.readline()
        print(repr(line))

        if "Wakeword detection" in line:

            print("🔥 JARVIS")

            return True

        return False
# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------