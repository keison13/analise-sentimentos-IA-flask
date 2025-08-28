import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from flask import Flask, request, render_template, session, Response, send_file
from transformers import pipeline
from datetime import timedelta
from io import BytesIO
import io
from reportlab.pdfgen import canvas
import csv

app = Flask(__name__)
app.secret_key = "chave-secreta-para-sessao"
app.permanent_session_lifetime = timedelta(minutes=30)


classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    framework="pt"
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        text = request.form["user_input"]
        raw_result = classifier(text)[0]

        stars = raw_result["label"]
        score = raw_result["score"]

        if "1" in stars or "2" in stars:
            label_pt = "Negativo"
            explanation = "O texto expressa um sentimento negativo, como insatisfação, tristeza ou rejeição."
            color = "red"
            suggestion = "Considere revisar seu conteúdo para torná-lo mais positivo."
        elif "3" in stars:
            label_pt = "Neutro"
            explanation = "O texto expressa um sentimento neutro ou equilibrado, sem emoções fortes."
            color = "white"
            suggestion = "O texto está equilibrado. Nenhuma ação necessária."
        else:
            label_pt = "Positivo"
            explanation = "O texto expressa um sentimento positivo, como alegria, satisfação ou aprovação."
            color = "green"
            suggestion = "Continue assim! O texto transmite emoções positivas."

        result = {
            "text": text,
            "label": label_pt,
            "score": score,
            "explanation": explanation,
            "color": color,
            "suggestion": suggestion
        }

        history = session.get("history", [])
        history.insert(0, {
            "texto": text,
            "sentimento": label_pt,
            "confiança": f"{score*100:.2f}%"
        })
        session["history"] = history[:5]

    return render_template("index.html", result=result, history=session.get("history", []))

@app.route("/export/csv")
def export_csv():
    output = io.StringIO()
    
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["Texto", "Sentimento", "Confiança"])
    
    for item in session.get("history", []):
        writer.writerow([item["texto"], item["sentimento"], item["confiança"]])

    bom = '\ufeff'
    response = Response(bom + output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=analises.csv"
    return response


@app.route("/export/pdf")
def export_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Histórico de Análises de Sentimento")

    y = 770
    for item in session.get("history", []):
        p.drawString(50, y, f"Texto: {item['texto'][:40]}...")
        y -= 20
        p.drawString(50, y, f"Sentimento: {item['sentimento']} | Confiança: {item['confiança']}")
        y -= 30

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="analises.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)


