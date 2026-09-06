from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Enable CORS so your GitHub Pages frontend can send requests to localhost
CORS(app)

@app.route('/api/scan', methods=['GET'])
def scan_storage():
    # Targets user-accessible storage or temp paths
    target_dir = "/sdcard/Download" if os.path.exists("/sdcard/Download") else "/tmp"
    
    total_size = 0
    file_count = 0

    try:
        for dirpath, dirnames, filenames in os.walk(target_dir):
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
        "cache_path": target_dir,
        "reclaimable_space_mb": size_in_mb,
        "file_count": file_count
    })

if __name__ == '__main__':
    # Listens on port 5000 locally
    app.run(host='127.0.0.1', port=5000, debug=True)
