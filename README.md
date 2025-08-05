# 🤖 File Organizer Bot

A simple Python script that helps you organize any folder on your computer by automatically sorting files into categorized subfolders.

## ✨ What it does

1. **Shows a folder picker** - Select any folder on your computer
2. **Scans for files** - Finds all files in that folder (ignores subfolders)
3. **Creates organized structure** - Makes an `Organized_Files` folder with category subfolders
4. **Moves files automatically** - Sorts files by type into appropriate folders
5. **Handles duplicates** - Renames files if they already exist (e.g., `file(1).pdf`)
6. **Shows summary** - Displays what was organized

## 📂 File Categories

| Category | File Types |
|----------|------------|
| **PDFs** | `.pdf` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif` |
| **Excel** | `.xls`, `.xlsx` |
| **Word** | `.doc`, `.docx` |
| **PowerPoint** | `.ppt`, `.pptx` |
| **Text** | `.txt` |
| **Others** | All other file types |

## 🚀 How to Use

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Running the Script

1. **Double-click** the `file_organizer_bot.py` file, or
2. **Command line**: `python file_organizer_bot.py`

### What happens:
1. A folder selection dialog appears
2. Choose the folder you want to organize
3. The script automatically organizes all files
4. A summary shows what was moved
5. A success dialog confirms completion

## 📁 Example

**Before organizing:**
```
Downloads/
├── document.pdf
├── photo.jpg
├── spreadsheet.xlsx
├── presentation.pptx
├── notes.txt
└── music.mp3
```

**After organizing:**
```
Downloads/
├── Organized_Files/
│   ├── PDFs/
│   │   └── document.pdf
│   ├── Images/
│   │   └── photo.jpg
│   ├── Excel/
│   │   └── spreadsheet.xlsx
│   ├── PowerPoint/
│   │   └── presentation.pptx
│   ├── Text/
│   │   └── notes.txt
│   └── Others/
│       └── music.mp3
```

## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_organizer.py
```

This creates sample files and tests the organization process.

## ⚠️ Important Notes

- **Safe operation**: The script only moves files, never deletes them
- **Self-protection**: The script stays in its own folder and won't organize itself
- **No subfolders**: Only processes files in the root of the selected folder
- **Duplicate handling**: Files with same names get numbered (e.g., `file(1).pdf`)
- **Permission required**: You need write access to the folder you're organizing

## 🛠️ Troubleshooting

**"tkinter not available"**
- Install tkinter: `pip install tk` or use a Python distribution that includes it

**"Permission denied"**
- Run as administrator (Windows) or with `sudo` (Mac/Linux)
- Make sure you have write permissions to the target folder

**Script doesn't start**
- Make sure Python 3.6+ is installed
- Try running from command line: `python file_organizer_bot.py`

## 🔧 Customization

To add new file categories, edit the `categories` dictionary in the `FileOrganizerBot` class:

```python
self.categories = {
    'PDFs': ['.pdf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    # Add your custom category
    'Videos': ['.mp4', '.avi', '.mkv'],
    # ... other categories
}
```

---

**Happy organizing! 🎉**