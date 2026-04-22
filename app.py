from flask import Flask, request, jsonify, send_file
from flasgger import Swagger
from s3_service import S3Service
import io

app = Flask(__name__)
swagger = Swagger(app)

s3 = S3Service()

@app.route("/")
def home():
    return "S3 API Running"

@app.route("/upload", methods=["POST"])
def upload():
    """
    Upload File
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Upload successful
    """
    file = request.files["file"]

    success = s3.upload_file(file)
    if success:
        return jsonify({"message": "Upload successful"})
    return jsonify({"error": "Upload failed"}), 500

@app.route("/download", methods=["GET"])
def download():
    """
    Download File
    ---
    parameters:
      - name: filename
        in: query
        type: string
        required: true
    responses:
      200:
        description: File download
    """
    filename = request.args.get("filename")

    obj = s3.download_file(filename)
    if obj:
        return send_file(io.BytesIO(obj["Body"].read()), download_name=filename)
    return jsonify({"error": "Download failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
