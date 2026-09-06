from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

TARGET_DIR = "/sdcard/Download" if os.path.exists("/sdcard/Download") else "/tmp"

@app.route('/api/scan', methods=['GET'])
def scan_storage():
    total_size = 0
    file_count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp) and not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    file_count += 1
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    size_in_mb = round(total_size / (1024 * 1024), 2)
    return jsonify({
        "status": "success",
        "cache_path": TARGET_DIR,
        "reclaimable_space_mb": size_in_mb,
        "file_count": file_count
    })

@app.route('/api/clean', methods=['POST'])
def clean_storage():
    deleted_files = 0
    freed_bytes = 0
    
    # Example clean routine: Removes .tmp and .apk installer files in Downloads
    try:
        for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
            for f in filenames:
                if f.endswith('.tmp') or f.endswith('.log'):
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        freed_bytes += os.path.getsize(fp)
                        os.remove(fp)
                        deleted_files += 1
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    freed_mb = round(freed_bytes / (1024 * 1024), 2)
    return jsonify({
        "status": "success",
        "freed_space_mb": freed_mb,
        "deleted_count": deleted_files
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

