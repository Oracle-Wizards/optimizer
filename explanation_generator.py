import google.generativeai as genai

from load_model import load_model

def generate_explanation(sql_query):
    model = load_model()
    generated_text = "Provide a brief explanation for: " + sql_query
    explanation_content = model.generate_content(generated_text)
    explanation = explanation_content.text
    return explanation
