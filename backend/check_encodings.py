import os

def check_encoding(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.yaml', '.json', '.env')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError as e:
                    print(f"ENCODING ERROR in {path}: {e}")

if __name__ == "__main__":
    check_encoding('.')
