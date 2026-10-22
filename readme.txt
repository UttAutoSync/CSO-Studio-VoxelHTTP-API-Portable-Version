# CSO VoxelHTTP API Portable Version

## Quick Start
1. Extract the entire ZIP archive.
2. Double-click `start.bat` (Start Server.bat).
3. Wait for the API documentation page to open in your browser: http://127.0.0.1:8765/docs

There is no need to install Python or Poetry separately. The folder already includes the runtime environment, API, and CSNZ voxel metadata database.

Keep the entire folder structure intact. Do not move individual files out of their original locations.

## Game Connection
The server listens only on `127.0.0.1` (localhost), making it suitable for game clients running on the same computer.

In the game's `HTTPIPList` configuration, use the following settings:

- `IP=http://127.0.0.1`
- `Ports=8765`

VXL/VMG resource URLs can remain pointed at their original cloud URLs.

## Shutting Down the Server
Press `Ctrl+C` in the **CSO VoxelHTTP API** window.

## Database
The package includes `voxelhttp_metadata_distilled.sqlite.db`.

The server uses `voxelhttp.env` and the database file located in the same directory.