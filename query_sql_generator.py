# query_generator.py
import google.generativeai as genai

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
    input_with_context = (
        "Extract the most optimized SQL query for Oracle database from the following text: " 
        + text 
        + ", in the form [SQL Query], Sachat que les tables de la base de donnees et avec leus colonnes sont:"
        + "CUSTOMERS: CUSTOMER_ID, EMAIL_ADDRESS, FULL_NAME. "
        + "STORES: STORE_ID, STORE_NAME, WEB_ADDRESS, PHYSICAL_ADDRESS, LATITUDE, LONGITUDE, LOGO, LOGO_MIME_TYPE, LOGO_FILENAME, LOGO_CHARSET, LOGO_LAST_UPDATED. "
        + "PRODUCTS: PRODUCT_ID, PRODUCT_NAME, UNIT_PRICE, PRODUCT_DETAILS, PRODUCT_IMAGE, IMAGE_MIME_TYPE, IMAGE_FILENAME, IMAGE_CHARSET, IMAGE_LAST_UPDATED. "
        + "ORDERS: ORDER_ID, ORDER_TMS, CUSTOMER_ID, ORDER_STATUS, STORE_ID. "
        + "SHIPMENTS: SHIPMENT_ID, STORE_ID, CUSTOMER_ID, DELIVERY_ADDRESS, SHIPMENT_STATUS. "
        + "ORDER_ITEMS: ORDER_ID, LINE_ITEM_ID, PRODUCT_ID, UNIT_PRICE, QUANTITY, SHIPMENT_ID. "
        + "INVENTORY: INVENTORY_ID, STORE_ID, PRODUCT_ID, PRODUCT_INVENTORY."
    )
    generated_content = model.generate_content(input_with_context)
    
    # Extract and return the generated SQL query
    sql_query = generated_content.text.split('```sql\n')[1].split('\n```')[0]
    return sql_query

   