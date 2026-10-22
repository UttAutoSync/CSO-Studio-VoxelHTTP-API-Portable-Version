"""Frozen-friendly launcher for the VoxelHTTP API."""

import os
import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    app_dir = Path(sys.executable).resolve().parent
elif (Path(__file__).resolve().parent / "app" / "src").is_dir():
    app_dir = Path(__file__).resolve().parent
else:
    app_dir = Path(__file__).resolve().parent.parent / "cso-py-voxelhttp-server"

app_source = app_dir / "app" / "src"
if not app_source.is_dir():
    app_source = app_dir / "src"
sys.path.insert(0, str(app_source))

# The API reads voxelhttp.env using a relative path and SQLite also uses a
# relative path, so both resolve beside the executable in the portable folder.
os.chdir(app_dir)

import uvicorn  # noqa: E402


if __name__ == "__main__":
    uvicorn.run(
        "voxelhttp.main:app",
        host="127.0.0.1",
        port=int(os.environ.get("VOXELHTTP_PORT", "8765")),
        reload=False,
        log_level="info",
    )
