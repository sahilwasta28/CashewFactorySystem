"""
cashew_backup_system.py - AUTOMATIC VERSION
Drops into your project and adds backup to all windows automatically
"""

import os
import datetime
import time
import tempfile
import threading
import tkinter as tk
from tkinter import messagebox
import gc
import shutil
import warnings
import subprocess
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class BackupSystem:
    # Configuration - Edit these values
    DB_HOST = "localhost"
    DB_USER = "Admin"
    DB_PASSWORD = "newpassword123"
    DB_NAME = "cfms"
    GOOGLE_DRIVE_CREDENTIALS = "credentials.json"
    GOOGLE_DRIVE_FOLDER_ID = "17PryBSaH9_M3dJ042A4sv3kru2UD9TBJ"

    # Track if we've already set up automatic backups
    _initialized = False
    _backup_dir = os.path.join(tempfile.gettempdir(), "cashew_backups")

    @classmethod
    def init_system(cls):
        """Initialize backup system (call once at startup)"""
        if not cls._initialized:
            # Create backup directory if it doesn't exist
            os.makedirs(cls._backup_dir, exist_ok=True)
            cls.schedule_automatic_backups()
            cls._patch_tkinter()
            cls._initialized = True

    @classmethod
    def _patch_tkinter(cls):
        """Monkey-patch Tk/Toplevel to auto-add backup button"""
        original_tk_init = tk.Tk.__init__
        original_toplevel_init = tk.Toplevel.__init__

        def patched_tk_init(self, *args, **kwargs):
            original_tk_init(self, *args, **kwargs)
            cls.add_backup_button(self)

        def patched_toplevel_init(self, *args, **kwargs):
            original_toplevel_init(self, *args, **kwargs)
            cls.add_backup_button(self)

        tk.Tk.__init__ = patched_tk_init
        tk.Toplevel.__init__ = patched_toplevel_init

    @classmethod
    def add_backup_button(cls, window):
        """Add backup button with ensured visibility"""
        btn = tk.Button(
            window,
            text="🚨 BACKUP 🚨",
            command=lambda: cls.run_backup(),
            bg="#ff0000",
            fg="white",
            font=("Arial", 10, "bold"),
            borderwidth=3,
            relief="raised"
        )
        btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        btn.lift()

    @classmethod
    def clean_old_drive_backups(cls):
        """Delete old backups from Google Drive, keeping only the latest"""
        if not os.path.exists(cls.GOOGLE_DRIVE_CREDENTIALS):
            return

        try:
            creds = service_account.Credentials.from_service_account_file(
                cls.GOOGLE_DRIVE_CREDENTIALS,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            service = build('drive', 'v3', credentials=creds)

            query = f"name contains 'cashew_backup_' and '{cls.GOOGLE_DRIVE_FOLDER_ID}' in parents"
            results = service.files().list(
                q=query,
                fields="files(id,name,createdTime)"
            ).execute()

            files = results.get('files', [])

            if len(files) > 1:
                files.sort(key=lambda x: x['createdTime'], reverse=True)
                for old_file in files[1:]:
                    try:
                        service.files().delete(fileId=old_file['id']).execute()
                    except Exception:
                        pass
        except Exception:
            pass

    @classmethod
    def safe_file_remove(cls, filepath, max_attempts=5, delay=1, show_message=True):
        """Safely remove a file with retries and forced garbage collection"""
        for attempt in range(max_attempts):
            try:
                # Force release of any file handles
                gc.collect()

                # Try normal deletion first
                try:
                    os.remove(filepath)
                    return True
                except PermissionError:
                    # If normal delete fails, try alternate methods
                    try:
                        # Try forcing deletion by changing permissions
                        os.chmod(filepath, 0o777)
                        os.remove(filepath)
                        return True
                    except:
                        # Final attempt with different method
                        with open(os.devnull, 'w') as devnull:
                            subprocess.call(
                                ['del', '/F', filepath],
                                shell=True,
                                stdout=devnull,
                                stderr=devnull
                            )
                        if not os.path.exists(filepath):
                            return True

                return not os.path.exists(filepath)

            except Exception as e:
                if attempt == max_attempts - 1:
                    if show_message:
                        messagebox.showwarning(
                            "Cleanup Warning",
                            f"Could not delete temporary backup file. Please delete manually: {filepath}\n"
                            f"Error: {str(e)}"
                        )
                    return False
                time.sleep(delay * (attempt + 1))

    @classmethod
    def cleanup_old_local_backups(cls, max_age_minutes=5):
        """Clean up local backup files older than specified minutes"""
        try:
            now = time.time()
            for filename in os.listdir(cls._backup_dir):
                filepath = os.path.join(cls._backup_dir, filename)
                if os.path.isfile(filepath) and filename.startswith("cashew_backup_"):
                    file_age = now - os.path.getmtime(filepath)
                    if file_age > max_age_minutes * 60:
                        cls.safe_file_remove(filepath, show_message=False)
        except Exception:
            pass

    @classmethod
    def run_backup(cls, show_message=True):
        """Main backup method with guaranteed file cleanup"""
        backup_file = None
        conn = None

        try:
            # Clean up old local backups first (now using minutes instead of hours)
            cls.cleanup_old_local_backups()

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(cls._backup_dir, f"cashew_backup_{timestamp}.sql")

            # Connect to MySQL
            import mysql.connector
            conn = mysql.connector.connect(
                host=cls.DB_HOST,
                user=cls.DB_USER,
                password=cls.DB_PASSWORD,
                database=cls.DB_NAME
            )
            cursor = conn.cursor()

            # Use a temporary file first, then rename to final name
            temp_path = backup_file + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as temp_file_handle:
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]

                for table in tables:
                    cursor.execute(f"SHOW CREATE TABLE `{table}`")
                    create_table = cursor.fetchone()[1]
                    temp_file_handle.write(f"{create_table};\n\n")

                    cursor.execute(f"SELECT * FROM `{table}`")
                    rows = cursor.fetchall()
                    if rows:
                        columns = [i[0] for i in cursor.description]
                        temp_file_handle.write(f"INSERT INTO `{table}` ({','.join(columns)}) VALUES\n")
                        for row in rows:
                            values = []
                            for v in row:
                                if v is None:
                                    values.append("NULL")
                                else:
                                    values.append(f"'{str(v).replace("'", "''")}'")
                            temp_file_handle.write(f"({','.join(values)}),\n")
                        temp_file_handle.write(";\n\n")

            # Rename temp file to final name
            os.rename(temp_path, backup_file)

            # Google Drive Upload
            if os.path.exists(cls.GOOGLE_DRIVE_CREDENTIALS):
                try:
                    cls.clean_old_drive_backups()

                    creds = service_account.Credentials.from_service_account_file(
                        cls.GOOGLE_DRIVE_CREDENTIALS,
                        scopes=['https://www.googleapis.com/auth/drive.file']
                    )
                    service = build('drive', 'v3', credentials=creds)

                    file_metadata = {
                        'name': os.path.basename(backup_file),
                        'description': f'Database backup {datetime.datetime.now().isoformat()}'
                    }
                    if cls.GOOGLE_DRIVE_FOLDER_ID:
                        file_metadata['parents'] = [cls.GOOGLE_DRIVE_FOLDER_ID]

                    media = MediaFileUpload(
                        backup_file,
                        mimetype='application/sql',
                        resumable=True
                    )

                    service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                except Exception as e:
                    if show_message:
                        messagebox.showwarning("Warning", f"Google Drive upload skipped: {str(e)}")

            if show_message:
                messagebox.showinfo("Success", "Backup completed successfully!")
            return True

        except Exception as e:
            if show_message:
                messagebox.showerror("Error", f"Backup failed: {str(e)}")
            return False

        finally:
            # Close database connection
            if conn and conn.is_connected():
                conn.close()

            # Clean up files with more aggressive approach
            if backup_file and os.path.exists(backup_file):
                # First try normal cleanup
                if not cls.safe_file_remove(backup_file, show_message=show_message):
                    # If normal cleanup failed, schedule delayed cleanup
                    threading.Timer(
                        10,  # Try again after 10 seconds
                        lambda: cls.safe_file_remove(backup_file, show_message=False)
                    ).start()

            # Also clean up temp file if it exists
            temp_path = backup_file + '.tmp' if backup_file else None
            if temp_path and os.path.exists(temp_path):
                cls.safe_file_remove(temp_path, show_message=False)

    @classmethod
    def schedule_automatic_backups(cls, interval_hours=24):
        """Schedule background backups"""

        def backup_loop():
            while True:
                cls.run_backup(show_message=False)
                time.sleep(interval_hours * 3600)

        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()