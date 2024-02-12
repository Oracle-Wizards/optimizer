import google.generativeai as genai
from load_model import load_model
import re

def analyze_sql_query(input_text):
    model = load_model()
    input_with_context = f"Can you analyze the following SQL query and tell me if it's valid or not : '{input_text}' ?"
    generated_content = model.generate_content(input_with_context)
    response = generated_content.text
    if  "invalid" in response or "is not valid" in response:
        return {"status": "error", "message": "Invalid query"}
    elif "is valid" in response:
        return {"status": "success", "message": "Query is valid"}
    else:
        return {"status": "error", "message": "Unexpected model response"}


def sql_validator(input_text):
    mot_a_rechercher = ';'
    nb_repetitions = input_text.lower().count(mot_a_rechercher.lower())
    if nb_repetitions == 1:
        sql_keyword_regex = r'\b(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE|USE|ALTER\s+DATABASE|CREATE\s+DATABASE|DROP\s+DATABASE|GRANT|REVOKE|BEGIN\s+TRANSACTION|COMMIT|ROLLBACK|CREATE\s+INDEX|DROP\s+INDEX|SHOW|DESCRIBE|DESC)\b'
        matches = re.findall(sql_keyword_regex, input_text, re.IGNORECASE)
        if matches:
            if matches[0].lower() == "select":
                if input_text.lower().count("select".lower()) ==1:
                    mot_a_rechercher = 'from'
                    nb_repetitions = input_text.lower().count(mot_a_rechercher.lower())
                    if nb_repetitions == 1:
                        analyze_sql_query(input_text)
                    else:
                        return {"status": "error", "message": "Invalid query"}
                else:
                    return {"status": "error", "message": "Invalid query"}                 
            else:    
                analyze_sql_query(input_text)

        else :
            return {"status": "error", "message": "Invalid query"}
    else :
        return {"status": "error", "message": "Invalid query"}