import os
import re

def fix_datetime_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if datetime or timedelta is used but not imported
                needs_datetime = 'datetime.' in content or 'datetime(' in content or 'datetime.now()' in content
                needs_timedelta = 'timedelta(' in content
                
                has_datetime_import = re.search(r'from datetime import.*datetime', content) or 'import datetime' in content
                has_timedelta_import = re.search(r'from datetime import.*timedelta', content)
                
                if (needs_datetime and not has_datetime_import) or (needs_timedelta and not has_timedelta_import):
                    print(f"Fixing imports in {path}")
                    # Prepare import line
                    imports = []
                    if needs_datetime and not has_datetime_import:
                        imports.append("datetime")
                    if needs_timedelta and not has_timedelta_import:
                        imports.append("timedelta")
                    
                    import_line = f"from datetime import {', '.join(imports)}\n"
                    
                    # Add to the top of the file
                    new_content = import_line + content
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_datetime_imports('.')
