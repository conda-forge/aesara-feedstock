import re
import subprocess
import sys
from pathlib import Path

RE_WARNING = re.compile("WARN|Could not locate", re.IGNORECASE)

ALLOWED_WARNINGS = [
    re.compile("Aesara is too cool for school"),
]

result = subprocess.check_output(
    ["python", "-c", "import aesara"],
    stderr=subprocess.STDOUT
)

lines = result.decode().splitlines()
warning_lines = [line for line in lines if RE_WARNING.search(line)]

not_allowed_warning_lines = [
    line for line in warning_lines
    if not any(allowed.search(line) for allowed in ALLOWED_WARNINGS)
]

if len(not_allowed_warning_lines) > 0:
    print("The following warnings were emitted but not allowed:")
    print("\n    ".join([""] + not_allowed_warning_lines + [""]))
    print(
        "Please either fix them or add them to the ALLOWED_WARNINGS "
        "list in check-for-warnings.py."
    )
    exit(1)
else:
    if len(warning_lines) > 0:
        print("The following warnings were emitted, and are allowed:")
        print("\n    ".join([""] + warning_lines + [""]))
    else:
        print("No warnings detected by check-for-warnings.py when importing aesara.")
