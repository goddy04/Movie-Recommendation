# from fpdf import FPDF
# import fitz  # PyMuPDF for extracting text from the PDF
# import os
# import requests  # To make API requests
# import json

# # Function to append text to the PDF file
# def append_to_pdf(text, pdf_filename):
#     # Check if the file exists
#     if os.path.exists(pdf_filename):
#         # First, extract the existing text and append it into the new PDF with the new text
#         existing_text = extract_text_from_pdf(pdf_filename)

#         # Create a new PDF file to store both existing and new content
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)

#         # Write the old content to the PDF
#         pdf.multi_cell(0, 10, existing_text)

#         # Append the new text to the existing content
#         pdf.multi_cell(0, 10, text)

#         # Save the appended content back to the file
#         pdf.output(pdf_filename, 'F')
#     else:
#         # Create new PDF and add the text
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)
#         pdf.multi_cell(0, 10, text)
#         pdf.output(pdf_filename)

# # Function to extract text from the PDF
# def extract_text_from_pdf(pdf_filename):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_filename)
    
#     # Initialize an empty string to store the extracted text
#     extracted_text = ""

#     # Loop through each page and extract the text
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document.load_page(page_num)
#         extracted_text += page.get_text()

#     # Close the PDF file after extraction
#     pdf_document.close()
    
#     return extracted_text

# # Function to call Azure OpenAI GPT-4 model with extracted text
# def call_azure_openai_api(extracted_text, api_key, endpoint_url, deployment_id):
#     headers = {
#         "Content-Type": "application/json",
#         "api-key": api_key
#     }

#     # Payload with prompt for GPT-4
#     payload = {
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Based on the following text, suggest 10 movies:\n{extracted_text}"}
#         ]
#     }

#     response = requests.post(
#         f"{endpoint_url}/openai/deployments/{deployment_id}/chat/completions?api-version=2023-05-15",
#         headers=headers,
#         data=json.dumps(payload)
#     )

#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         raise Exception(f"Error {response.status_code}: {response.text}")

# if __name__ == "__main__":
#     # File name of the PDF to store user input
#     pdf_filename = "user_input.pdf"

#     # Ask for user input
#     user_input = input("Enter your text: ")

#     # Append input to the PDF
#     append_to_pdf(user_input, pdf_filename)

#     print(f"Your input has been appended to {pdf_filename}.")

#     # Automatically extract the text from the PDF
#     extracted_text = extract_text_from_pdf(pdf_filename)

#     print("Extracted Text from PDF:\n", extracted_text)

#     # Azure OpenAI API details (fill in your details here)
#     api_key = "9f0ee660ead84adba48708c174088d84"
#     endpoint_url = "https://miniproject123.openai.azure.com/"  # e.g., https://your-endpoint-name.openai.azure.com
#     deployment_id = "gpt-4"  # This is the deployment name for the GPT-4 model

#     # Call the Azure OpenAI API with the extracted text
#     try:
#         chatgpt_response = call_azure_openai_api(extracted_text, api_key, endpoint_url, deployment_id)
#         print("ChatGPT-4 Response:\n", chatgpt_response)
#     except Exception as e:
#         print(f"Error calling Azure OpenAI API: {e}")


from flask import Flask, request, render_template, redirect, url_for
from fpdf import FPDF
import fitz  # PyMuPDF for extracting text from the PDF
import os
import requests  # To make API requests
import json

app = Flask(__name__)

# Function to append text to the PDF file
def append_to_pdf(text, pdf_filename):
    if os.path.exists(pdf_filename):
        existing_text = extract_text_from_pdf(pdf_filename)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, existing_text)
        pdf.multi_cell(0, 10, text)
        pdf.output(pdf_filename, 'F')
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(pdf_filename)

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_filename):
    pdf_document = fitz.open(pdf_filename)
    extracted_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        extracted_text += page.get_text()
    pdf_document.close()
    return extracted_text

# Function to call Azure OpenAI GPT-4 model with extracted text
def call_azure_openai_api(extracted_text, api_key, endpoint_url, deployment_id):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Based on the following text, suggest 10 movies:\n{extracted_text}"}
        ]
    }
    response = requests.post(
        f"{endpoint_url}/openai/deployments/{deployment_id}/chat/completions?api-version=2023-05-15",
        headers=headers,
        data=json.dumps(payload)
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Define the route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    suggestions = None

    if request.method == 'POST':
        movie_name = request.form['movie']

        # File name of the PDF to store user input
        pdf_filename = "user_input.pdf"

        # Append user input to the PDF
        append_to_pdf(movie_name, pdf_filename)

        # Automatically extract the text from the PDF
        extracted_text = extract_text_from_pdf(pdf_filename)

        # Azure OpenAI API details (use your details here)
        api_key = "9f0ee660ead84adba48708c174088d84"
        endpoint_url = "https://miniproject123.openai.azure.com/"
        deployment_id = "gpt-4"

        # Call the Azure OpenAI API with the extracted text
        try:
            suggestions = call_azure_openai_api(extracted_text, api_key, endpoint_url, deployment_id)
        except Exception as e:
            suggestions = f"Error calling Azure OpenAI API: {e}"

    return render_template('index.html', suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)
