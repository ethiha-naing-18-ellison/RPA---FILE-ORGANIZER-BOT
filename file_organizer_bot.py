#!/usr/bin/env python3
"""
File Organizer Bot
A Python script to organize files in a user-selected folder by file type.

The script uses a GUI folder picker and organizes files into categorized subfolders
while keeping the script itself safe in its original location.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from collections import defaultdict


class FileOrganizerBot:
    """Main File Organizer Bot class"""
    
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
        self.selected_folder = ""
        self.organized_files_path = ""
    
    def get_folder_from_user(self):
        """Show GUI folder selection dialog"""
        print("🤖 File Organizer Bot")
        print("=" * 50)
        print("Opening folder selection dialog...")
        
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        
        # Show folder selection dialog
        folder_path = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=os.path.expanduser("~")
        )
        
        root.destroy()
        
        if not folder_path:
            print("❌ No folder selected. Exiting...")
            return None
        
        return folder_path
    
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
            print(f"📁 Created organized folder: {organized_path}")
        else:
            print(f"📁 Using existing organized folder: {organized_path}")
        
        print("=" * 50)
        print(f"🎯 ORGANIZED FILES WILL BE STORED IN:")
        print(f"📍 {organized_path}")
        print("=" * 50)
        
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
                print(f"📝 Renamed '{original_filename}' to '{new_name}' (duplicate found)")
                return str(new_path)
            
            counter += 1
    
    def organize_files(self, folder_path):
        """Main function to organize files in the selected folder"""
        self.selected_folder = folder_path
        print(f"\n📂 Organizing folder: {folder_path}")
        
        # Create organized files structure
        organized_path = self.create_organized_folders(folder_path)
        self.organized_files_path = organized_path
        
        # Get all files in the selected folder (not subfolders)
        try:
            all_items = os.listdir(folder_path)
        except PermissionError:
            print("❌ Permission denied. Cannot access the selected folder.")
            return False
        
        # Filter to only include files (not directories)
        files = [item for item in all_items 
                if os.path.isfile(os.path.join(folder_path, item))]
        
        if not files:
            print("📭 No files found in the selected folder.")
            return True
        
        print(f"📊 Found {len(files)} files to organize...")
        
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
                    print(f"📁 Created category: {category}")
                
                # Prepare target path
                target_path = os.path.join(category_path, filename)
                
                # Handle duplicates
                target_path = self.get_unique_filename(target_path, filename)
                
                # Move the file
                shutil.move(file_path, target_path)
                
                # Update statistics
                self.stats[category] += 1
                self.total_files_moved += 1
                
                print(f"✅ Moved '{filename}' → {category}/")
                
            except Exception as e:
                print(f"❌ Failed to move '{filename}': {str(e)}")
        
        return True
    
    def print_summary(self):
        """Print organization summary"""
        print("\n" + "=" * 60)
        print("📊 ORGANIZATION SUMMARY")
        print("=" * 60)
        print(f"📂 Selected folder: {self.selected_folder}")
        print(f"📁 Organized files location: {self.organized_files_path}")
        print("=" * 60)
        print(f"📈 Total files moved: {self.total_files_moved}")
        
        if self.stats:
            print("\n📋 Files organized by category:")
            for category, count in sorted(self.stats.items()):
                print(f"   • {category}: {count} files")
        
        print("\n🎉 Organization completed successfully!")
        print("✨ All files have been moved to their respective subfolders.")
        print("=" * 60)
    
    def run(self):
        """Main execution method"""
        try:
            # Get folder from user
            folder_path = self.get_folder_from_user()
            if not folder_path:
                return
            
            # Validate folder exists
            if not os.path.exists(folder_path):
                print(f"❌ Selected folder does not exist: {folder_path}")
                return
            
            # Organize files
            success = self.organize_files(folder_path)
            
            if success:
                # Print summary
                self.print_summary()
                
                # Show completion dialog
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo(
                    "File Organizer Bot", 
                    f"✅ Successfully organized {self.total_files_moved} files!\n\n"
                    f"Check the 'Organized_Files' folder in:\n{folder_path}"
                )
                root.destroy()
            
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            
            # Show error dialog
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("File Organizer Bot", f"Error: {str(e)}")
                root.destroy()
            except:
                pass


def main():
    """Main function"""
    print("🤖 File Organizer Bot - Starting...")
    
    # Check if tkinter is available
    try:
        import tkinter
        print("✅ GUI components loaded successfully")
    except ImportError:
        print("❌ tkinter not available. GUI mode requires tkinter.")
        print("Please install tkinter or use a Python distribution that includes it.")
        return
    
    # Create and run the organizer
    organizer = FileOrganizerBot()
    organizer.run()
    
    print("\n👋 File Organizer Bot - Finished")


if __name__ == "__main__":
    main()