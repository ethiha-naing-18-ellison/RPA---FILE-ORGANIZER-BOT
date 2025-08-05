#!/usr/bin/env python3
"""
Flask Web Interface for File Organizer Bot
A web-based interface to organize files in folders by type.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
from organizer import organize_files_in_folder

app = Flask(__name__)
app.secret_key = 'file_organizer_secret_key_2024'  # For flash messages

@app.route('/')
def index():
    """Display the main form for folder path input"""
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    """Process the folder organization request"""
    folder_path = request.form.get('folder_path', '').strip()
    
    # Debug: Show what we received
    print(f"📥 Received folder path: '{folder_path}'")
    
    # Basic validation
    if not folder_path:
        flash('Please enter a folder path.', 'error')
        return redirect(url_for('index'))
    
    # Normalize the path (but be more careful about it)
    try:
        # Store original path for comparison
        original_path = folder_path
        folder_path = os.path.abspath(folder_path)
        print(f"📍 Original path: {original_path}")
        print(f"📍 Normalized path: {folder_path}")
    except Exception as e:
        print(f"❌ Path normalization failed: {str(e)}")
        flash(f'Invalid folder path: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    # Debug: Print the path being processed
    print(f"🔍 Processing folder path: {folder_path}")
    print(f"📁 Path exists: {os.path.exists(folder_path)}")
    print(f"📂 Is directory: {os.path.isdir(folder_path)}")
    
    # Call the organizer function
    try:
        result = organize_files_in_folder(folder_path)
        
        if result['success']:
            return render_template('result.html', 
                                 success=True,
                                 folder_path=folder_path,
                                 organized_path=result['organized_path'],
                                 total_files=result['total_files'],
                                 stats=result['stats'],
                                 errors=result['errors'],
                                 message=result['message'])
        else:
            # Provide more helpful error messages
            error_msg = result["error"]
            if "does not exist" in error_msg:
                # Extract the path from the error for better guidance
                path_match = re.search(r'Folder does not exist: (.+)', error_msg)
                if path_match:
                    invalid_path = path_match.group(1)
                    
                    # Provide suggestions for common path issues
                    suggestions = []
                    if "YourName" in invalid_path or "username" in invalid_path.lower():
                        suggestions.append("Replace 'YourName' with your actual Windows username")
                        # Try to suggest actual username from system
                        actual_user = os.environ.get('USERNAME', os.environ.get('USER', 'User'))
                        corrected_path = invalid_path.replace('YourName', actual_user)
                        suggestions.append(f"Try: {corrected_path}")
                    
                    if suggestions:
                        suggestion_text = ". " + ". ".join(suggestions)
                        error_msg = f"Folder path not found: {invalid_path}{suggestion_text}"
                    else:
                        error_msg = f"Folder path not found: {invalid_path}. Please verify the path exists and try again"
            
            flash(error_msg, 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        # More detailed error handling
        error_message = str(e)
        
        # Check for common error patterns and provide helpful guidance
        if "cannot access local variable" in error_message:
            error_message = "Internal error occurred. Please try again or contact support."
        elif "Permission denied" in error_message:
            error_message = "Permission denied. Please check folder permissions and try again."
        elif "No such file or directory" in error_message:
            error_message = "Folder path not found. Please verify the path exists and is accessible."
        else:
            error_message = f"Unexpected error occurred: {error_message}"
        
        flash(error_message, 'error')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page with information about the File Organizer Bot"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"Created templates directory: {templates_dir}")
    
    # Get port from environment (Render.com sets this) or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    print("🤖 File Organizer Bot - Web Interface")
    print("=" * 50)
    print("🌐 Starting Flask server...")
    print(f"📍 Access the web interface at: http://localhost:{port}")
    print("🔧 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the Flask app (0.0.0.0 allows external connections for Render.com)
    app.run(host='0.0.0.0', port=port, debug=True)