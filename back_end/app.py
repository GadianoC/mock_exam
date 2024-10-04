from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from document_processor import process_document
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SERVER_NAME'] = 'localhost:5000'


@app.route('/api/summarize', methods=['POST'])
def summarize_document():
    # generation_config = {

    # }

    genai.configure(api_key=os.getenv('api_key'))
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

    document_file = request.files.get('document')

    if not document_file:
        return jsonify({'error': 'No Document file provided'}), 400
    
    file_bytes = document_file.read()
    file_extention = os.path.splitext(document_file.filename)[1]
    try:
        document_content = process_document(file_bytes, file_extention)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    summary_length = request.form.get('summaryLength', 0.5)
    detail_level = request.form.get('detailLevel', 2)
    
    try:
        summary_length = float(summary_length)
        detail_level = int(detail_level)
    except ValueError:
        return jsonify({'error': 'Invalid summary length or detail level'}), 400
    
    # What is still needed is the code is the details and input needed for the mock exam
    try:
        prompt = f'Summarize the following text and keep summary within {summary_length * 100}% of the original text length. Adjust the level of detail based on the provided detail based on the provided detail level ({detail_level}):\n\n{document_content}'

        response = model.generate_content(prompt)

        summary = response.text.strip()

        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
