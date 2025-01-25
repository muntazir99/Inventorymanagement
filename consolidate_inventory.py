import csv
import os
import streamlit as st

INVENTORY_FILE = "inventory.csv"

def consolidate_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return

    # Dictionary to store item names and their total quantities
    consolidated_data = {}

    # Read the current inventory data
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        for row in reader:
            item_name = row[0].strip().lower()  # Normalize item name
            quantity = int(row[1])

            # Combine quantities for duplicate items
            if item_name in consolidated_data:
                consolidated_data[item_name] += quantity
            else:
                consolidated_data[item_name] = quantity

    # Write the consolidated data back to the inventory file
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Quantity"])  # Write the header back
        for item_name, quantity in consolidated_data.items():
            writer.writerow([item_name, quantity])

    st.success("Inventory has been consolidated. Duplicate items have been combined.")
