# import csv
# import os
import streamlit as st

# INVENTORY_FILE = "inventory.csv"

from db_config import get_db

def initialize_inventory():
    db = get_db()
    inventory = db['inventory']

# def initialize_inventory():
#     if not os.path.exists(INVENTORY_FILE):
#         with open(INVENTORY_FILE, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Item", "Quantity"])

def get_inventory_items():
    db = get_db()
    collection = db['inventory']
    items = collection.find({}, {"_id": 0, "name": 1})
    return [item['name'] for item in items]

    # items = []
    # with open(INVENTORY_FILE, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # Skip header
    #     for row in reader:
    #         items.append(row[0])
    # return items

def get_inventory_data():
    db = get_db()
    collection = db['inventory']
    get_inventory_data = list(collection.find({}, {"_id": 0}))
    return get_inventory_data

    # inventory_data = []
    # if os.path.exists(INVENTORY_FILE):
    #     with open(INVENTORY_FILE, mode='r', newline='') as file:
    #         reader = csv.reader(file)
    #         next(reader)  # Skip header
    #         for row in reader:
    #             inventory_data.append({
    #                 "name": row[0],
    #                 "quantity": int(row[1])
    #             })
    # return inventory_data

def add_item(item_name, quantity):
    db = get_db()
    collection = db['inventory']
    normalized_name=item_name.strip().lower()
    collection.update_one(
        {"name": normalized_name},
        {"$inc": {"quantity": quantity}},
        upsert=True)
    st.success(f"{item_name} has been added/updated with quantity {quantity}.")
    # # Normalize item name
    # normalized_name = item_name.strip().lower()
    # inventory_data = get_inventory_data()
    # item_found = False

    # for item in inventory_data:
    #     if item['name'].lower() == normalized_name:
    #         item['quantity'] += quantity
    #         item_found = True
    #         break

    # if not item_found:
    #     inventory_data.append({
    #         "name": item_name.strip(),
    #         "quantity": quantity
    #     })

    # # Write the updated inventory back to the file
    # with open(INVENTORY_FILE, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Item", "Quantity"])
    #     for item in inventory_data:
    #         writer.writerow([item['name'], item['quantity']])

    # st.success(f"{item_name} has been added/updated with quantity {quantity}.")

def update_inventory(item_name, quantity, increase=True):
    db = get_db()
    collection = db['inventory']
    normalized_name = item_name.strip().lower()

    item=collection.find_one({"name": normalized_name})
    if item:
        new_quantity = item['quantity'] + quantity if increase else item['quantity'] - quantity
        if new_quantity<0:
            st.error("Cannot decrease quantity below zero for {item_name}.")
            return False
        collection.update_one(
            {"name": normalized_name},
            {"$set": {"quantity": new_quantity}}
        )
        st.success(f"{item_name} has been updated with new quantity {new_quantity}.")
        return True
    else:
        st.error(f"{item_name} not found in inventory.")
        return False
    
    # rows = []
    # item_found = False

    # with open(INVENTORY_FILE, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     header = next(reader)
    #     for row in reader:
    #         if row[0] == item_name:
    #             current_quantity = int(row[1])
    #             new_quantity = current_quantity + quantity if increase else current_quantity - quantity
    #             row[1] = str(new_quantity)
    #             item_found = True
    #         rows.append(row)

    # if item_found:
    #     with open(INVENTORY_FILE, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(header)
    #         writer.writerows(rows)
    #     return True
    # return False

def view_inventory():
    inventory_data = get_inventory_data()
    if inventory_data:
        st.table(inventory_data)
    else:
        st.write("No items in inventory.")


    # inventory_data = get_inventory_data()
    # if inventory_data:
    #     st.table(inventory_data)
    # else:
    #     st.write("No items in inventory.")
