# query_generator.py
import google.generativeai as genai

from load_model import load_model

def generate_sql_query(input_text):
    model = load_model()
    input_with_context = "Generate an optimized SQL query for: " + input_text + ", in the form [SQL Query]"
    generated_content = model.generate_content(input_with_context)
    sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]
    return sql_query


def extract_optimized_sql_query(text):
   
    model = load_model()
    input_with_context = "Extract the most optimized SQL query from the following text: " + text + ", in the form [SQL Query]"
    generated_content = model.generate_content(input_with_context)
    return generated_content.text.split('```sql\n')[1].split('\n```')[0]
