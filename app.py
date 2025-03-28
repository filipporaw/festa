from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

TEMPLATE_PATH = "ricetta_ssn.png"
FONT_PATH = "arial.ttf"
CSV_PATH = "partecipanti.csv"
POS_NOME = (170, 220)
FONT_SIZE = 36

if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "nome", "accompagnatore"])

@app.route("/genera", methods=["POST"])
def genera_ricetta():
    nome = request.form.get("nome", "Nome Sconosciuto").upper()
    accompagnatore = request.form.get("accompagnatore") == "1"

    if accompagnatore:
        nome += " +1"

    img = Image.open(TEMPLATE_PATH).convert("RGB")
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)
    draw.text(POS_NOME, nome, font=font, fill="red")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), nome, "SI" if accompagnatore else "NO"])

    return send_file(buffer, mimetype='image/png', download_name=f"ricetta_{nome.replace(' ', '_')}.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
