# Premiumize FTP Sync

A lightweight Python script to synchronize files from your [Premiumize.me](https://www.premiumize.me) cloud storage to a local home server using SFTP.

The script performs a one-way sync from the remote Premiumize SFTP server to your local directory. It automatically downloads new files, deletes local files that are no longer present on the remote server, and cleans up empty directories.

## Features

- **One-Way Sync**: Keeps your local directory perfectly in sync with your Premiumize cloud.
- **Automatic Downloads**: Detects and downloads new files from the remote SFTP server.
- **Automatic Cleanup**: Deletes local files that have been removed from your Premiumize cloud.
- **Empty Folder Removal**: Recursively cleans up empty local directories after synchronization.
- **Logging**: Provides clear, timestamped logs of all sync activities.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## Installation

### Using `uv` (Recommended)

If you have `uv` installed, you can run the project directly or set up a virtual environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/premiumize-ftp-sync.git
cd premiumize-ftp-sync

# Install dependencies and create virtual environment
uv sync
```

### Using `pip`

Alternatively, you can use standard Python tools:

```bash
# Clone the repository
git clone https://github.com/yourusername/premiumize-ftp-sync.git
cd premiumize-ftp-sync

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r pyproject.toml
```

## Configuration

The script is configured using environment variables. Create a `.env` file in the root directory of the project:

```env
HOST=sftp.premiumize.me
USERNAME=your_premiumize_customer_id
PASSWORD=your_premiumize_pin_or_password
LOCAL_BASE=/path/to/your/local/sync/directory/
REMOTE_BASE=/folder-to-sync
```

### Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| `HOST` | The SFTP host address for Premiumize. | `sftp.premiumize.me` |
| `USERNAME` | Your Premiumize customer ID or username. | `123456789` |
| `PASSWORD` | Your Premiumize API PIN or password. | `your_secret_pin` |
| `LOCAL_BASE` | The absolute path to the local directory where files should be synced. **Must not end with a slash.** | `/mnt/storage/downloads` |
| `REMOTE_BASE` | The remote directory path on Premiumize to sync from. **Must not end with a slash.** | `/` or `/folder_name` |

## Usage

To run the synchronization script:

### Using `uv`

```bash
uv run main.py
```

### Using standard Python

```bash
python main.py
```

## Automation (Cron Job)

To keep your files synced automatically, you can set up a cron job on your home server.

For example, to run the sync every hour:

```cron
0 * * * * /path/to/premiumize-ftp-sync/.venv/bin/python /path/to/premiumize-ftp-sync/main.py >> /path/to/premiumize-ftp-sync/sync.log 2>&1
```

## How It Works

1. **Load Configuration**: Loads environment variables from the `.env` file using `dotenv`.
2. **Scan Local & Remote**: Recursively lists all files in the local `LOCAL_BASE` and remote `REMOTE_BASE` directories.
3. **Compare Files**:
   - Identifies files present on remote but missing locally (queued for download).
   - Identifies files present locally but missing on remote (queued for deletion).
4. **Download**: Downloads new files via SFTP and creates any necessary local subdirectories.
5. **Delete**: Deletes local files that are no longer on the remote server.
6. **Clean Up**: Recursively removes any empty local directories.

## License

[MIT License](LICENSE)
