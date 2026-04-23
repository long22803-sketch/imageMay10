from flask import Flask, request, send_file
import io, zipfile
from PIL import Image, ImageFilter

app = Flask(__name__)

@app.route("/")
def home():
    return "Image Tool Running"

@app.route("/process", methods=["POST"])
def process():
    files = request.files.getlist("images")
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as z:
        for f in files:
            img = Image.open(f).convert("RGB")

            canvas = Image.new("RGB", (2000,2000), (245,245,245))
            x = (2000 - img.width)//2
            y = (2000 - img.height)//2
            canvas.paste(img,(x,y))

            out = io.BytesIO()
            canvas.save(out, format="PNG")
            z.writestr(f.filename, out.getvalue())

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True)

if __name__ == "__main__":
    app.run()
