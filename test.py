import subprocess

while True:
    output = subprocess.run(
        ["system_profiler", "SPUSBDataType"], capture_output=True
    ).stdout.decode()

    if "G000WM0602110684" in output:
        # Run the script
        print("present")
    else:
        print("not present")
