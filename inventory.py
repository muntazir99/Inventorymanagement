import csv
import os
import streamlit as st

INVENTORY_FILE = "inventory.csv"

from db_config import get_db
def initialize_inventory():
    db = get_db()
    inventory = db['inventory']
    
def initialize_inventory():
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Quantity"])

def get_inventory_items():
    items = []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            items.append(row[0])
    return items

def get_inventory_data():
    inventory_data = []
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                inventory_data.append({
                    "name": row[0],
                    "quantity": int(row[1])
                })
    return inventory_data

def add_item(item_name, quantity):
    # Normalize item name
    normalized_name = item_name.strip().lower()
    inventory_data = get_inventory_data()
    item_found = False

    for item in inventory_data:
        if item['name'].lower() == normalized_name:
            item['quantity'] += quantity
            item_found = True
            break

    if not item_found:
        inventory_data.append({
            "name": item_name.strip(),
            "quantity": quantity
        })

    # Write the updated inventory back to the file
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Quantity"])
        for item in inventory_data:
            writer.writerow([item['name'], item['quantity']])

    st.success(f"{item_name} has been added/updated with quantity {quantity}.")

def update_inventory(item_name, quantity, increase=True):
    rows = []
    item_found = False

    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == item_name:
                current_quantity = int(row[1])
                new_quantity = current_quantity + quantity if increase else current_quantity - quantity
                row[1] = str(new_quantity)
                item_found = True
            rows.append(row)

    if item_found:
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        return True
    return False

def view_inventory():
    inventory_data = get_inventory_data()
    if inventory_data:
        st.table(inventory_data)
    else:
        st.write("No items in inventory.")
