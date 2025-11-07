"""
Run the Streamlit UI client
"""

import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "mcp_client/app.py",
        "--server.port=8501",
        "--server.address=localhost"
    ])

