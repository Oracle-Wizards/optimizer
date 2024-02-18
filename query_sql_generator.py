# query_generator.py
import google.generativeai as genai
import json

from load_model import load_model

def generate_sql_query(input_text):
    model = load_model()
    input_with_context = "Generate an optimized SQL query for: " + input_text + ", in the form [SQL Query]"
    generated_content = model.generate_content(input_with_context)
    sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]
    return sql_query

tables_info = {
    "CUSTOMERS": ["CUSTOMER_ID", "EMAIL_ADDRESS", "FULL_NAME"],
    "STORES": ["STORE_ID", "STORE_NAME", "WEB_ADDRESS", "PHYSICAL_ADDRESS", "LATITUDE", "LONGITUDE", "LOGO", "LOGO_MIME_TYPE", "LOGO_FILENAME", "LOGO_CHARSET", "LOGO_LAST_UPDATED"],
    "PRODUCTS": ["PRODUCT_ID", "PRODUCT_NAME", "UNIT_PRICE", "PRODUCT_DETAILS", "PRODUCT_IMAGE", "IMAGE_MIME_TYPE", "IMAGE_FILENAME", "IMAGE_CHARSET", "IMAGE_LAST_UPDATED"],
    "ORDERS": ["ORDER_ID", "ORDER_TMS", "CUSTOMER_ID", "ORDER_STATUS", "STORE_ID"],
    "SHIPMENTS": ["SHIPMENT_ID", "STORE_ID", "CUSTOMER_ID", "DELIVERY_ADDRESS", "SHIPMENT_STATUS"],
    "ORDER_ITEMS": ["ORDER_ID", "LINE_ITEM_ID", "PRODUCT_ID", "UNIT_PRICE", "QUANTITY", "SHIPMENT_ID"],
    "INVENTORY": ["INVENTORY_ID", "STORE_ID", "PRODUCT_ID", "PRODUCT_INVENTORY"]
}
def extract_optimized_sql_query(text):
    # Load model and generate SQL query based on text input
    model = load_model()  # Supposons que cette fonction charge votre modèle
    
    # Construire le contexte avec les informations sur les tables et leurs colonnes, ainsi que les exemples
def extract_optimized_sql_query(text):
    # Load model
    model = load_model()  # Supposons que cette fonction charge votre modèle
    
    # Initialiser la requête SQL avec une valeur nulle
    sql_query = None
    
    # Tant que la requête SQL n'est pas valide, continuez à générer une nouvelle requête
    input_with_context = (
        "Extract the most optimized SQL query for Oracle database from the following text: " 
        + text 
        + ", in the form [SQL Query]. Notez que les tables de la base de données avec leurs colonnes sont les suivantes : "
        + "CUSTOMERS: CUSTOMER_ID, EMAIL_ADDRESS, FULL_NAME. "
        + "STORES: STORE_ID, STORE_NAME, WEB_ADDRESS, PHYSICAL_ADDRESS, LATITUDE, LONGITUDE, LOGO, LOGO_MIME_TYPE, LOGO_FILENAME, LOGO_CHARSET, LOGO_LAST_UPDATED. "
        + "PRODUCTS: PRODUCT_ID, PRODUCT_NAME, UNIT_PRICE, PRODUCT_DETAILS, PRODUCT_IMAGE, IMAGE_MIME_TYPE, IMAGE_FILENAME, IMAGE_CHARSET, IMAGE_LAST_UPDATED. "
        + "ORDERS: ORDER_ID, ORDER_TMS, CUSTOMER_ID, ORDER_STATUS, STORE_ID. "
        + "SHIPMENTS: SHIPMENT_ID, STORE_ID, CUSTOMER_ID, DELIVERY_ADDRESS, SHIPMENT_STATUS. "
        + "ORDER_ITEMS: ORDER_ID, LINE_ITEM_ID, PRODUCT_ID, UNIT_PRICE, QUANTITY, SHIPMENT_ID. "
        + "INVENTORY: INVENTORY_ID, STORE_ID, PRODUCT_ID, PRODUCT_INVENTORY. "
        + "Exemples : "
        + "INPUT :  SELECT * FROM Orders WHERE ORDER_STATUS = 'Pending'; "
        + "OUTPUT : ```sql SELECT ORDER_ID, CUSTOMER_ID FROM Orders WHERE ORDER_STATUS = 'Complete' INDEX(ORDER_STATUS); ```"
    )
    while not sql_query:

        generated_content = model.generate_content(input_with_context)

        try:
            sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]
        except IndexError:
            pass


    return sql_query
