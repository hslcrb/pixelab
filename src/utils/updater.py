"""
Update Manager - Check for updates via GitHub API
"""
import json
import threading
import urllib.request
import logging
from typing import Optional, Callable

class UpdateManager:
    """Manages version checking and update logic"""
    
    REPO_URL = "https://api.github.com/repos/hslcrb/pixelab/releases/latest"
    
    def __init__(self, current_version: str):
        self.current_version = current_version
        self.latest_version: Optional[str] = None
        self.update_url: Optional[str] = None
        
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
                    
                    tag_name = data.get('tag_name', '').replace('v', '')
                    self.latest_version = tag_name
                    self.update_url = data.get('html_url')
                    
                    if self._is_newer(tag_name, self.current_version):
                        callback(tag_name, self.update_url)
                        
            except Exception as e:
                logging.error(f"Failed to check for updates: {e}")

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()

    def _is_newer(self, latest: str, current: str) -> bool:
        """Simple version comparison (highly simplified)"""
        try:
            l_parts = [int(p) for p in latest.split('.')]
            c_parts = [int(p) for p in current.split('.')]
            # Extend shorter list with zeros
            max_len = max(len(l_parts), len(c_parts))
            l_parts.extend([0] * (max_len - len(l_parts)))
            c_parts.extend([0] * (max_len - len(c_parts)))
            
            return l_parts > c_parts
        except:
            return latest != current
