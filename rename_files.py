import os
import shutil

# Backup the original base.html
shutil.copy('app/templates/base.html', 'app/templates/base_original.html')
print("Original base.html backed up to base_original.html")

# Replace base.html with the new version
shutil.copy('app/templates/base_new.html', 'app/templates/base.html')
print("New base.html installed successfully")

print("Navigation redesign complete!")