import json
import threading
import urllib.request
import logging
import os
import sys
import platform
import shutil
import tempfile
from typing import Optional, Callable
from src.i18n import t

class UpdateManager:
    """Manages version checking and automatic update logic"""
    
    REPO_URL = "https://api.github.com/repos/hslcrb/pixelab/releases/latest"
    
    def __init__(self, current_version: str):
        self.current_version = current_version
        self.latest_version: Optional[str] = None
        self.update_url: Optional[str] = None
        self.download_url: Optional[str] = None
        
    def check_for_updates(self, callback: Callable[[str, str], None]):
        """
        Check for updates in a background thread.
        Calls callback(latest_version, update_url) if a new version is found.
        """
        def _target():
            try:
                # Custom User-Agent is required by GitHub API
                req = urllib.request.Request(
                    self.REPO_URL, 
                    headers={'User-Agent': 'PixeLab-Updater'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    
                    self.latest_version = data.get('tag_name', '').replace('v', '')
                    self.update_url = data.get('html_url')
                    
                    # Detect correct asset for current platform
                    assets = data.get('assets', [])
                    self.download_url = self._get_asset_url(assets)
                    
                    if self._is_newer(self.latest_version, self.current_version):
                        callback(self.latest_version, self.update_url)
                        
            except Exception as e:
                logging.error(f"Failed to check for updates: {e}")

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()

    def _get_asset_url(self, assets) -> Optional[str]:
        """Find the correct asset URL for the current platform"""
        os_name = platform.system().lower() # 'linux', 'windows', 'darwin'
        
        target_name = ""
        if os_name == 'linux':
            target_name = 'pixelab-linux'
        elif os_name == 'windows':
            target_name = 'pixelab-windows.exe'
        elif os_name == 'darwin': # macOS
            target_name = 'pixelab-macos'
            
        for asset in assets:
            if asset.get('name') == target_name:
                return asset.get('browser_download_url')
        return None

    def start_auto_update(self, progress_callback: Callable[[int, str], None], finish_callback: Callable[[bool, str], None]):
        """Start the automatic download and replacement process"""
        if not self.download_url:
            finish_callback(False, "No download URL found for this platform.")
            return

        def _update_thread():
            try:
                # 1. Create temp directory
                temp_dir = tempfile.mkdtemp()
                temp_file = os.path.join(temp_dir, os.path.basename(self.download_url))
                
                # 2. Download with progress
                progress_callback(10, t('downloading').format(p=10))
                
                def _reporthook(blocknum, blocksize, totalsize):
                    readsofar = blocknum * blocksize
                    if totalsize > 0:
                        percent = int(readsofar * 100 / totalsize)
                        # Scale to 10-90%
                        scaled_percent = 10 + int(percent * 0.8)
                        progress_callback(scaled_percent, t('downloading').format(p=percent))
                
                urllib.request.urlretrieve(self.download_url, temp_file, _reporthook)
                
                # 3. Apply Update
                progress_callback(95, t('applying_update'))
                
                # Get current executable path
                if getattr(sys, 'frozen', False):
                    # Running as bundled binary (PyInstaller)
                    current_exe = sys.executable
                else:
                    # Running as script
                    current_exe = os.path.abspath(sys.argv[0])

                # Atomic replacement (as much as possible)
                if os.name == 'nt': # Windows
                    old_exe = current_exe + ".old"
                    if os.path.exists(old_exe):
                        os.remove(old_exe)
                    os.rename(current_exe, old_exe)
                    shutil.move(temp_file, current_exe)
                else: # Linux/macOS
                    shutil.move(temp_file, current_exe)
                    os.chmod(current_exe, 0o755) # Ensure executable
                
                progress_callback(100, t('restarting'))
                finish_callback(True, t('update_complete_restart'))
                
                # 4. Restart Application
                self._restart_app(current_exe)
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                finish_callback(False, t('update_failed').format(e=str(e)))
            finally:
                # Cleanup
                try: shutil.rmtree(temp_dir)
                except: pass

        thread = threading.Thread(target=_update_thread, daemon=True)
        thread.start()

    def _restart_app(self, exe_path):
        """Restart the application"""
        if getattr(sys, 'frozen', False):
            # Bundled executable
            os.execv(exe_path, [exe_path] + sys.argv[1:])
        else:
            # Python script
            os.execv(sys.executable, [sys.executable] + sys.argv)

    def _is_newer(self, latest: str, current: str) -> bool:
        """Simple version comparison"""
        try:
            l_parts = [int(p) for p in latest.split('.')]
            c_parts = [int(p) for p in current.split('.')]
            max_len = max(len(l_parts), len(c_parts))
            l_parts.extend([0] * (max_len - len(l_parts)))
            c_parts.extend([0] * (max_len - len(c_parts)))
            return l_parts > c_parts
        except:
            return latest != current
