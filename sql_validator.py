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


def sql_validator1(input_text):
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
    
def sql_validator(input_text):
    # Vérifier la présence d'un point-virgule unique
    mot_a_rechercher = ';'
    nb_repetitions = input_text.lower().count(mot_a_rechercher.lower())
    if nb_repetitions != 1:
        return {"status": "error", "message": "Invalid query"}

    # Vérifier la présence du mot-clé SELECT, INSERT, UPDATE ou DELETE
    if "SELECT" not in input_text.upper() and "INSERT" not in input_text.upper() \
        and "UPDATE" not in input_text.upper() and "DELETE" not in input_text.upper():
        return {"status": "error", "message": "Query must contain a SELECT, INSERT, UPDATE, or DELETE statement"}

    # Vérifier que la partie entre SELECT et FROM n'est pas vide
    if "SELECT" in input_text.upper() and "FROM" in input_text.upper():
        select_from_part = input_text.upper().split("SELECT")[1].split("FROM")[0].strip()
        if not select_from_part:
            return {"status": "error", "message": "SELECT statement must contain columns between SELECT and FROM"}

    # Vérifier que la partie entre FROM et ; n'est pas vide
    if "FROM" in input_text.upper() and ";" in input_text:
        from_end_part = input_text.upper().split("FROM")[1].split(";")[0].strip()
        if not from_end_part:
            return {"status": "error", "message": "Missing condition after FROM clause"}

    # Vérifier la syntaxe de la requête UPDATE
    if "UPDATE" in input_text.upper():
        if "SET" not in input_text.upper() or "WHERE" not in input_text.upper():
            return {"status": "error", "message": "UPDATE statement must contain SET and WHERE clauses"}

    # Vérifier la syntaxe de la requête INSERT
    if "INSERT" in input_text.upper():
        if "VALUES" not in input_text.upper():
            return {"status": "error", "message": "INSERT statement must contain a VALUES clause"}

    # Vérifier la syntaxe de la requête DELETE
    if "DELETE" in input_text.upper():
        if "FROM" not in input_text.upper() or "WHERE" not in input_text.upper():
            return {"status": "error", "message": "DELETE statement must contain FROM and WHERE clauses"}

    # Vérifier la syntaxe de la requête INSERT INTO et VALUES
    if "INSERT" in input_text.upper() and "INTO" in input_text.upper():
        if "VALUES" not in input_text.upper():
            return {"status": "error", "message": "INSERT statement must contain a VALUES clause"}

    # Vérifier la syntaxe de la requête DELETE FROM et WHERE
    if "DELETE" in input_text.upper() and "FROM" in input_text.upper():
        if "WHERE" not in input_text.upper():
            return {"status": "error", "message": "DELETE statement must contain a WHERE clause"}

    # Valider la requête SQL en utilisant le modèle
    return analyze_sql_query(input_text)
