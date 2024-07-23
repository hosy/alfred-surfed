import json
import os
import subprocess
import sys

# Path to surfed-cli
cli_path = "/Applications/Surfed.app/Contents/MacOS/surfed-cli.app/Contents/MacOS/surfed-cli"

def check_cli_path():
    if not os.path.exists(cli_path):
        print(json.dumps({"items": [{"title": "Surfed App not found", "subtitle": "Please install Surfed before using this workflow.", "valid": False}]}))
        sys.exit(1)

def fetch_urls(query):
    if len(query) > 2:
        check_cli_path()
        apikey = os.getenv("SURFED_API_KEY", "")
        command = f'{cli_path} "{query}" -j -a -l 50'
        if apikey:
            command += f' --key {apikey}'
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                shell=True  # This allows the command string to be interpreted correctly
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(json.dumps({"items": [{"title": "Error", "subtitle": str(e), "valid": False}]}))
            sys.exit(1)
    return {"urls": [], "collections": [], "tags": []}

def format_for_alfred(data):
    items = []
    for collection in data.get("collections", []):
        items.append({
            "title": collection["title"],
            "subtitle": collection["url"],
            "arg": collection["url"],
            "icon": {"path": "collection-icon.png"}
        })
    for tag in data.get("tags", []):
        items.append({
            "title": tag["title"],
            "subtitle": tag["url"],
            "arg": tag["url"],
            "icon": {"path": "tag-icon.png"}
        })
    for url in data.get("urls", []):
        items.append({
            "title": url.get("title", url["url"]),
            "subtitle": url["url"],
            "arg": url["url"],
            "icon": {"path": url["imagePath"]}
        })
    return {"items": items}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    data = fetch_urls(query)
    output = format_for_alfred(data)
    print(json.dumps(output))