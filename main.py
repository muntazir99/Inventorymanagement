import streamlit as st
from inventory import get_inventory_items, get_inventory_data, add_item, update_inventory, view_inventory
from consolidate_inventory import consolidate_inventory
from log_manager import log_allotment, log_return, view_log
from taker_view import view_taker_data
from auth import login, create_user, update_password

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None

# Streamlit App Title
st.title("Aaruush Inventory")

# Authentication
if st.session_state.authenticated:
    st.sidebar.title("Actions")
    st.sidebar.success(f"Logged in as: {st.session_state.role.capitalize()}")

    # Admin and user-specific options
    admin_options = [
        "View Inventory Dashboard",
        "View Inventory List",
        "Add Item",
        "Allot Item",
        "Return Item",
        "View Log",
        "View Taker Data",
        "Consolidate Inventory",
        "Add User",
        "Update Password",
    ]
    user_options = [
        "View Inventory Dashboard",
        "View Inventory List",
        "View Taker Data",
        "Update Password",
    ]

    # Show options based on user role
    option = st.sidebar.selectbox(
        "Choose an action", admin_options if st.session_state.role == "admin" else user_options
    )

    # Fetch inventory items
    inventory_items = get_inventory_items()

    if option == "View Inventory Dashboard":
        st.header("Components in Inventory")
        inventory_data = get_inventory_data()
        if not inventory_data:
            st.warning("No items found in the inventory.")
        else:
            cols = st.columns(3)
            for idx, item in enumerate(inventory_data):
                col = cols[idx % 3]
                with col:
                    st.subheader(item["name"].capitalize())
                    st.info(f"Quantity: {item['quantity']}")

    elif option == "View Inventory List":
        st.header("Current Inventory")
        view_inventory()

    elif option == "Add Item" and st.session_state.role == "admin":
        st.header("Add a New Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        if st.button("Add Item"):
            add_item(item_name, quantity)
            st.success(f"Added {item_name} with quantity {quantity} to the inventory.")

    elif option == "Allot Item" and st.session_state.role == "admin":
        st.header("Allot an Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity to Allot", min_value=1, step=1)
        project = st.text_input("Project Name")
        taker = st.text_input("Taker's Name")
        head = st.text_input("Head's Name")
        if st.button("Allot Item"):
            if update_inventory(item_name, quantity, increase=False):
                log_allotment(item_name, quantity, project, taker, head)
                st.success(f"Allotted {quantity} of {item_name} to {taker} for project {project}.")
            else:
                st.error(f"Failed to allot {quantity} of {item_name}. Item may not exist or insufficient quantity.")

    elif option == "Return Item" and st.session_state.role == "admin":
        st.header("Return an Item")
        item_name = st.selectbox("Select Item", inventory_items)
        quantity_returned = st.number_input("Quantity to Return", min_value=1, step=1)
        taker = st.text_input("Taker's Name")
        if st.button("Return Item"):
            if update_inventory(item_name, quantity_returned, increase=True):
                log_return(item_name, quantity_returned, taker)
                st.success(f"Returned {quantity_returned} of {item_name} from {taker} back to inventory.")
            else:
                st.error(f"Failed to return {quantity_returned} of {item_name}.")

    elif option == "View Log" and st.session_state.role == "admin":
        st.header("Inventory Log")
        view_log()

    elif option == "View Taker Data":
        st.header("Takers and Their Allotted Components")
        view_taker_data()

    elif option == "Consolidate Inventory" and st.session_state.role == "admin":
        st.header("Consolidate Inventory")
        st.write("Combine duplicate items in the inventory by summing their quantities.")
        if st.button("Consolidate Now"):
            consolidate_inventory()
            st.success("Inventory consolidated successfully.")

    elif option == "Add User" and st.session_state.role == "admin":
        st.header("Add New User")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Select Role", ["admin", "user"])
        if st.button("Create User"):
            create_user(new_username, new_password, new_role)

    elif option == "Update Password":
        st.header("Update Password")
        username = st.text_input("Username")
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            success, message = update_password(username, old_password, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

    if st.sidebar.button("Logout"):
        for key in ['authenticated', 'role']:
            st.session_state.pop(key, None)
        st.success("Logged out successfully!")
        st.rerun()

else:
    is_authenticated, role = login()
    if is_authenticated:
        st.session_state.authenticated = True
        st.session_state.role = role
        st.rerun()
