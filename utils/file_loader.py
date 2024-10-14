import json

def load_json_file(file_path, default=None, is_list=False):
    try:
        with open(file_path, 'r') as f:
            if is_list:
                return [line.strip() for line in f.readlines() if line.strip()]
            else:
                return json.load(f)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return default if default is not None else []
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from {file_path}: {str(e)}")
        return default if default is not None else []
    except Exception as e:
        print(f"Failed to load {file_path}: {str(e)}")
        return default if default is not None else []