from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import PyPDF2
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyBWR8Zk15zVVWwjZ5J6OE_nK36Z8g2fGXI"
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

@app.route("/")
def index():
    return render_template("diagnostics.html")

@app.route('/premium')
def premium():
    return render_template('premium.html')  # Template for the premium page

@app.route('/upload_report')
def upload_report():
    return render_template('upload_report.html')  # Template for the premium page

@app.route('/cht_q')
def chatbot_query():
    return render_template('chatbot_query.html')

@app.route("/analyze", methods=["POST"])
def analyze_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    pdf_text = extract_text_from_pdf(file_path)
    prompt = ("Analyze this medical report and provide structured information with proper spacing. "
              "Format it as follows:(start after leaving one line spaces)\n\n"
              "**Summary**\n(Summary of the report highlighting abnormalities and risk level)\n\n"
              "**Patient Details**\n(Patient's name <br>, age <br>, gender <br>, and any relevant medical history<br>)\n\n"
              "**Risk Assessment & Alerts**\n(Detect potential health risks and suggest further tests)\n\n"
              "**Prescription Advice**\n(Provide medicines based on the disease mentioned in the report. If not available, suggest general treatment. "
              "Add a disclaimer that this is AI-generated and a doctor should be consulted for proper treatment.)\n\n"
              "Now analyze this report:\n\n" + pdf_text)
    
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    
    # Formatting: Bold for headings and adding two-line spacing before each section
    formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", response.text)  # Bold formatting
    formatted_text = formatted_text.replace("\n\n", "<br><br>")  # Adding two-line spacing
    
    return jsonify({"analysis": formatted_text})

if __name__ == "__main__":
    app.run(debug=True)
