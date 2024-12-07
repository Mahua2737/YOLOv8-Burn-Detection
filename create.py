import os

# Define the folder structure
folders = [
    "flask_app/static/uploads",
    "flask_app/static/results",
    "flask_app/templates",
]

# Create the folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create placeholder files
open("flask_app/app.py", "w").close()  # Main Flask application script
open("flask_app/templates/index.html", "w").close()  # HTML template file

print("Folder structure created successfully!")
