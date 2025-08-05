#!/usr/bin/env python3
"""
File Organizer Core Logic
Extracted from File Organizer Bot for Flask web interface integration.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


class FileOrganizer:
    """Core File Organizer class for web interface"""
    
    def __init__(self):
        # Define file categories and their extensions
        self.categories = {
            # Document files
            'PDFs': ['.pdf'],
            'Word': ['.doc', '.docx', '.docm', '.dot', '.dotx', '.dotm', '.rtf'],
            'Excel': ['.xls', '.xlsx', '.xlsm', '.xlsb', '.xlt', '.xltx', '.xltm', '.csv'],
            'PowerPoint': ['.ppt', '.pptx', '.pptm', '.pot', '.potx', '.potm', '.pps', '.ppsx', '.ppsm'],
            'Text': ['.txt', '.md', '.rtf', '.log', '.readme'],
            
            # Media files
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.dng', '.heic', '.heif'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg', '.m2v', '.divx', '.asf', '.rm', '.rmvb', '.vob', '.ts', '.mts', '.m2ts'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff', '.au', '.ra', '.midi', '.mid', '.ac3', '.dts'],
            
            # Archives & Compressed
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', '.tar.bz2', '.tar.xz', '.cab', '.ace', '.arj', '.lzh', '.sit', '.sitx', '.sea'],
            
            # Executables & Installers
            'Executables': ['.exe', '.msi', '.msu', '.deb', '.rpm', '.dmg', '.pkg', '.app', '.appx', '.msix', '.apk', '.ipa', '.run', '.bin', '.com', '.bat', '.cmd', '.sh', '.ps1'],
            
            # Programming & Development
            'Code': ['.py', '.js', '.html', '.htm', '.css', '.php', '.java', '.cpp', '.c', '.h', '.cs', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.pl', '.lua', '.r', '.m', '.sql'],
            'Web': ['.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.js', '.css', '.scss', '.sass', '.less', '.vue', '.jsx', '.tsx', '.json', '.xml', '.yaml', '.yml'],
            'Data': ['.json', '.xml', '.yaml', '.yml', '.csv', '.tsv', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.dbf', '.sav', '.dta'],
            
            # Design & Graphics
            'Design': ['.psd', '.ai', '.eps', '.indd', '.sketch', '.fig', '.xd', '.cdr', '.dwg', '.dxf', '.step', '.iges', '.stl', '.obj', '.fbx', '.blend', '.max', '.ma', '.mb'],
            
            # System & Configuration
            'System': ['.dll', '.sys', '.drv', '.ocx', '.cpl', '.scr', '.vxd', '.inf', '.reg', '.ini', '.cfg', '.conf', '.config', '.properties', '.plist'],
            
            # Fonts
            'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.pfb', '.pfm', '.afm', '.bdf', '.pcf'],
            
            # Ebooks
            'Ebooks': ['.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lit', '.lrf', '.pdb', '.pml', '.rb', '.tcr'],
            
            # Disk Images & Virtual
            'DiskImages': ['.iso', '.img', '.bin', '.nrg', '.mdf', '.cue', '.ccd', '.sub', '.vcd', '.vhd', '.vhdx', '.vmdk', '.vdi', '.qcow2'],
            
            # Backup & Temporary
            'Backup': ['.bak', '.backup', '.old', '.tmp', '.temp', '.swp', '.swo', '.cache', '.dat', '.dmp'],
            
            # Certificates & Security
            'Certificates': ['.crt', '.cer', '.pem', '.key', '.p12', '.pfx', '.jks', '.keystore', '.pub', '.sig'],
            
            # CAD & Engineering
            'CAD': ['.dwg', '.dxf', '.step', '.stp', '.iges', '.igs', '.catpart', '.catproduct', '.prt', '.asm', '.sldprt', '.sldasm', '.slddrw'],
            
            # 3D Models
            '3D_Models': ['.obj', '.fbx', '.dae', '.3ds', '.blend', '.max', '.ma', '.mb', '.stl', '.ply', '.x3d', '.gltf', '.glb'],
            
            # Email & Communication
            'Email': ['.msg', '.eml', '.mbox', '.pst', '.ost', '.dbx', '.mbx', '.emlx'],
            
            # Calendar & Contacts
            'Calendar': ['.ics', '.ical', '.vcs', '.vcf', '.ldif']
        }
        
        # Statistics tracking
        self.stats = defaultdict(int)
        self.total_files_moved = 0
        self.organized_files_path = ""
        self.errors = []
    
    def get_file_category(self, file_extension):
        """Determine which category a file belongs to based on its extension"""
        file_ext = file_extension.lower()
        
        for category, extensions in self.categories.items():
            if file_ext in extensions:
                return category
        
        return 'Others'  # Default category for unmatched files
    
    def create_organized_folders(self, base_path):
        """Create the Organized_Files directory and category subfolders"""
        organized_path = os.path.join(base_path, "Organized_Files")
        
        # Create main organized folder if it doesn't exist
        if not os.path.exists(organized_path):
            os.makedirs(organized_path)
        
        return organized_path
    
    def get_unique_filename(self, target_path, original_filename):
        """Generate a unique filename if file already exists"""
        if not os.path.exists(target_path):
            return target_path
        
        # Extract filename parts
        file_path = Path(target_path)
        name_without_ext = file_path.stem
        extension = file_path.suffix
        parent_dir = file_path.parent
        
        # Find unique name with counter
        counter = 1
        while True:
            new_name = f"{name_without_ext}({counter}){extension}"
            new_path = parent_dir / new_name
            
            if not os.path.exists(new_path):
                return str(new_path)
            
            counter += 1
    
    def organize_files_in_folder(self, folder_path):
        """
        Main function to organize files in the specified folder
        Returns a dictionary with results and statistics
        """
        # Reset stats for this run
        self.stats = defaultdict(int)
        self.total_files_moved = 0
        self.errors = []
        
        # Validate folder path
        if not os.path.exists(folder_path):
            return {
                'success': False,
                'error': f"Folder does not exist: {folder_path}",
                'stats': {},
                'total_files': 0,
                'organized_path': '',
                'errors': []
            }
        
        if not os.path.isdir(folder_path):
            return {
                'success': False,
                'error': f"Path is not a directory: {folder_path}",
                'stats': {},
                'total_files': 0,
                'organized_path': '',
                'errors': []
            }
        
        # Create organized files structure
        try:
            organized_path = self.create_organized_folders(folder_path)
            self.organized_files_path = organized_path
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to create organized folder: {str(e)}",
                'stats': {},
                'total_files': 0,
                'organized_path': '',
                'errors': []
            }
        
        # Get all files in the selected folder (not subfolders)
        try:
            all_items = os.listdir(folder_path)
        except PermissionError:
            return {
                'success': False,
                'error': "Permission denied. Cannot access the selected folder.",
                'stats': {},
                'total_files': 0,
                'organized_path': '',
                'errors': []
            }
        
        # Filter to only include files (not directories)
        files = [item for item in all_items 
                if os.path.isfile(os.path.join(folder_path, item))]
        
        if not files:
            return {
                'success': True,
                'message': "No files found in the selected folder.",
                'stats': {},
                'total_files': 0,
                'organized_path': organized_path,
                'errors': []
            }
        
        # Process each file
        for filename in files:
            # Skip if file is already in Organized_Files or is a system file
            if filename.startswith('.') or filename == 'Organized_Files':
                continue
            
            file_path = os.path.join(folder_path, filename)
            file_extension = Path(filename).suffix
            
            try:
                # Determine category
                category = self.get_file_category(file_extension)
                
                # Create category folder if it doesn't exist
                category_path = os.path.join(organized_path, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                
                # Prepare target path
                target_path = os.path.join(category_path, filename)
                
                # Handle duplicates
                target_path = self.get_unique_filename(target_path, filename)
                
                # Move the file
                shutil.move(file_path, target_path)
                
                # Update statistics
                self.stats[category] += 1
                self.total_files_moved += 1
                
            except Exception as e:
                error_msg = f"Failed to move '{filename}': {str(e)}"
                self.errors.append(error_msg)
        
        return {
            'success': True,
            'message': f"Successfully organized {self.total_files_moved} files!",
            'stats': dict(self.stats),
            'total_files': self.total_files_moved,
            'organized_path': organized_path,
            'errors': self.errors
        }


def organize_files_in_folder(folder_path):
    """
    Convenience function to organize files in a folder
    Returns a dictionary with results and statistics
    """
    organizer = FileOrganizer()
    return organizer.organize_files_in_folder(folder_path)


if __name__ == "__main__":
    # Test the organizer
    test_path = input("Enter folder path to organize: ")
    result = organize_files_in_folder(test_path)
    
    if result['success']:
        print(f"✅ {result['message']}")
        print(f"📁 Organized files location: {result['organized_path']}")
        if result['stats']:
            print("\n📋 Files by category:")
            for category, count in result['stats'].items():
                print(f"   • {category}: {count} files")
        if result['errors']:
            print("\n❌ Errors occurred:")
            for error in result['errors']:
                print(f"   • {error}")
    else:
        print(f"❌ Error: {result['error']}")