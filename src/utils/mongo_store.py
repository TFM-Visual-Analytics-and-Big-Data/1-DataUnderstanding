import os
from pymongo import MongoClient
from dotenv import load_dotenv
 
def get_mongo_collection():
    """Retorna la colección de MongoDB usando la configuración de entorno."""
    
    [MONGO_URI,MONGO_DB, MONGO_COLLECTION]=load_env_variables() 

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    return collection

def load_env_variables():
    """
    Carga las variables de entorno desde el archivo .env.
    
    Returns:
        dict: Diccionario con las variables de entorno cargadas.
    """
    load_dotenv()  # Carga las variables de entorno desde el archivo .env
    # return {
    #     "MONGO_URI": os.getenv("MONGO_URI"),
    #     "MONGO_DB": os.getenv("MONGO_DB"),
    #     "MONGO_COLLECTION": os.getenv("MONGO_COLLECTION")
    # }
    return [os.getenv("MONGO_URI"), os.getenv("MONGO_DB"), os.getenv("MONGO_COLLECTION")]

def save_dict_to_mongo(data: dict):
    """
    Guarda un diccionario en la colección configurada de MongoDB.
    
    Args:
        data (dict): Diccionario a guardar.
    
    Returns:
        InsertOneResult: Resultado de la operación de inserción.
    """
    try:
        collection = get_mongo_collection()
        result = collection.insert_one(data)    
        return result.acknowledged 
    except Exception as e:
        print(f"Error inserting data: {e}")
        return False 