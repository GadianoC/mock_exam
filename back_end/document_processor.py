import io
import docx
import pdfplumber

def process_document(file_bytes, file_extention):
    if file_extention.lower() == '.pdf':
        return process_pdf(file_bytes)
    elif file_extention.lower() == '.docx':
        return process_word(file_bytes)
    elif file_extention() == '.txt':
        return process_text(file_bytes)
    else:
        raise ValueError('unsupported file extention {}'.format(file_extention))

def process_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ''
        for page in pdf.pages:
            page_text += page.extract_text() 
            if page_text:
                text += page_text + '\n'
    return text.strip()

def process_word(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text.strip()

def process_text(file_bytes):
    return file_bytes.decode('utf-8').strip()