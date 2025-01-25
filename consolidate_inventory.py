# import csv
# import os
from db_config import get_db
import streamlit as st

# INVENTORY_FILE = "inventory.csv"

def consolidate_inventory():
    db=get_db()
    collection=db['inventory']
    pipeline = [{
        "$group": {
            "_id": "$name",
            "total_quantity": {"$sum": "$quantity"}
        }
    }]
    consolidated_data = list(collection.aggregate(pipeline))
    collection.delete_many({})  # Clear the inventory collection
    for item in consolidated_data:
        collection.insert_one({"name": item["_id"], "quantity": item["total_quantity"]})
    st.success("Inventory has been consolidated. Duplicate items have been combined.")
    
    # consolidated_data = {}

    # # Read the current inventory data
    # with open(INVENTORY_FILE, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     header = next(reader)  # Skip header
    #     for row in reader:
    #         item_name = row[0].strip().lower()  # Normalize item name
    #         quantity = int(row[1])

    #         # Combine quantities for duplicate items
    #         if item_name in consolidated_data:
    #             consolidated_data[item_name] += quantity
    #         else:
    #             consolidated_data[item_name] = quantity

    # # Write the consolidated data back to the inventory file
    # with open(INVENTORY_FILE, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Item", "Quantity"])  # Write the header back
    #     for item_name, quantity in consolidated_data.items():
    #         writer.writerow([item_name, quantity])

    # st.success("Inventory has been consolidated. Duplicate items have been combined.")
