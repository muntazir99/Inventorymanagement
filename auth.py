import streamlit as st
import bcrypt
from db_config import get_db


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def create_user(username, password, role="user"):
    db = get_db()
    collection = db["users"]

    # Check if the user already exists
    if collection.find_one({"username": username}):
        st.warning("User already exists!")
        return False

    # Insert new user
    hashed_pw = hash_password(password)
    collection.insert_one({"username": username, "password": hashed_pw, "role": role})
    st.success(f"User '{username}' created successfully!")
    return True


def update_password(username, old_password, new_password):
    db = get_db()
    collection = db["users"]

    # Find the user
    user = collection.find_one({"username": username})
    if not user:
        return False, "User does not exist!"

    # Verify old password
    if not verify_password(old_password, user["password"]):
        return False, "Old password is incorrect!"

    # Update with the new password
    hashed_pw = hash_password(new_password)
    collection.update_one({"username": username}, {"$set": {"password": hashed_pw}})
    return True, "Password updated successfully!"


def authenticate(username, password):
    db = get_db()
    collection = db["users"]

    # Find the user
    user = collection.find_one({"username": username})
    if not user:
        return False, None

    # Verify the password
    if verify_password(password, user["password"]):
        return True, user["role"]
    return False, None


def login():
    # Initialize session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None

    if not st.session_state.authenticated:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            is_authenticated, role = authenticate(username, password)
            if is_authenticated:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.sidebar.success(f"Logged in as: {username}")
            else:
                st.sidebar.error("Invalid username or password")
    
    return st.session_state.authenticated, st.session_state.role

