import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
# from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

# Azure Key Vault Configuration
# key_vault_url = os.getenv("KEY_VAULT_URL")
# credential = DefaultAzureCredential()
# secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# Retrieve MongoDB Atlas connection string from Azure Key Vault
# mongo_db_url = secret_client.get_secret("MongoDBAtlasConnectionString").value
mongo_db_url = "mongodb+srv://root:root@cluster0.ztxtvvm.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Atlas Configuration
client = AsyncIOMotorClient(mongo_db_url)
db = client["flightReservationSystem"]


def load_db():
    return db






















# import os
#
# from dotenv import load_dotenv
# from motor.motor_asyncio import AsyncIOMotorClient
# # from azure.identity import DefaultAzureCredential
# # from azure.keyvault.secrets import SecretClient
#
# load_dotenv()
#
# # Azure Key Vault Configuration
# # key_vault_url = os.getenv("KEY_VAULT_URL")
# # credential = DefaultAzureCredential()
# # secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
#
# # Retrieve MongoDB Atlas connection string from Azure Key Vault
# # mongo_db_url = secret_client.get_secret("MongoDBAtlasConnectionString").value
# mongo_db_url = "mongodb+srv://root:root@cluster0.ztxtvvm.mongodb.net/?retryWrites=true&w=majority"
#
# # MongoDB Atlas Configuration
# client = AsyncIOMotorClient(mongo_db_url)
# db = client["flightReservationSystem"]
#
#
# def load_db():
#     return db
