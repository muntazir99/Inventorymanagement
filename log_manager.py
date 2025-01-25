# import csv
# import os  # Add this import statement
from datetime import datetime
import streamlit as st
from db_config import get_db

# LOG_FILE = "inventory_log.csv"

def initialize_log():
    pass

def log_allotment(item_name, quantity, project, taker, head):
    db=get_db()
    collection=db['logs']
    log_entry = {
        "item_name": item_name,
        "quantity": quantity,
        "project": project,
        "taker": taker,
        "head": head,
        "date_alloted": datetime.now(),
        "date_returned": None
    }
    collection.insert_one(log_entry)
    st.success(f"{quantity} units of {item_name} have been allotted to {taker} for project {project}.")

    # with open(LOG_FILE, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([item_name, quantity, project, taker, head, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ""])

def log_return(item_name, quantity, taker):
    db=get_db()
    collection=db['logs']
    log_entry={
        "item_name": item_name,
        "quantity": quantity,
        "project": None,
        "taker": taker,
        "head": None,
        "date_alloted": None,
        "date_returned": datetime.now()
    }
    collection.insert_one(log_entry)
    st.success(f"{quantity} units of {item_name} have been returned by {taker}.")
    # with open(LOG_FILE, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([item_name, quantity, "", taker, "", "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def view_log():
    db=get_db()
    collection=db['logs']
    logs=list(collection.find({},{"_id":0}))
    if logs:
        st.table(logs)
    else:
        st.write("No log data available.")

    # log_data = []
    # with open(LOG_FILE, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     header = next(reader)  # Read the header
    #     for row in reader:
    #         log_data.append(row)
    
    # if log_data:
    #     st.table([header] + log_data)  # Display as a table including the header
    # else:
    #     st.write("No log data available.")
