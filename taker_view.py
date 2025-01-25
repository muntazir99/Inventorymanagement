# import csv
from db_config import get_db
import streamlit as st

# LOG_FILE = "inventory_log.csv"
def view_taker_data():
    db = get_db()
    collection = db["logs"]
    taker_data = {}

    # Corrected projection: Only include specific fields
    logs = collection.find(
        {"taker": {"$exists": True, "$ne": None}},
        {"item_name": 1, "quantity": 1, "project": 1, "taker": 1, "_id": 0}
    )

    # Process logs into the taker_data dictionary
    for log in logs:
        taker = log.get("taker")
        if taker not in taker_data:
            taker_data[taker] = []
        taker_data[taker].append({
            "item": log.get("item_name", "N/A"),
            "quantity": log.get("quantity", 0),
            "project": log.get("project", "N/A")
        })

    # Display the taker data in Streamlit
    if not taker_data:
        st.warning("No data available for takers.")
    else:
        for taker, items in taker_data.items():
            st.subheader(f"Taker: {taker}")
            for item in items:
                st.info(
                    f"Component: {item['item']} | "
                    f"Quantity Allotted: {item['quantity']} | "
                    f"Project: {item['project']}"
                )
            st.markdown("---")

    
    # Open the log file and read the data
    # with open(LOG_FILE, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # Skip header
        
    #     # Iterate through each row in the log file
    #     for row in reader:
    #         if len(row) >= 4:  # Ensure the row has at least 4 columns (Item, Quantity, Project, Taker)
    #             taker = row[3]
    #             if taker:
    #                 if taker not in taker_data:
    #                     taker_data[taker] = []
    #                 taker_data[taker].append({
    #                     "item": row[0],
    #                     "quantity": row[1],
    #                     "project": row[2]
    #                 })

    # # Display the data using Streamlit
    # if not taker_data:
    #     st.warning("No data available for takers.")
    # else:
    #     for taker, items in taker_data.items():
    #         st.subheader(f"Taker: {taker}")
    #         for item in items:
    #             st.info(f"Component: {item['item']} | Quantity Allotted: {item['quantity']} | Project: {item['project']}")
    #         st.markdown("---")
