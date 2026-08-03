import streamlit as st
import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:8000"
#BASE_URL = "https://todoapp-backend-1fm4.onrender.com/"
st.set_page_config(page_title="Todo App", layout="wide", initial_sidebar_state="expanded")

# Custom Theme & Styling
def apply_custom_theme():
    """Apply custom CSS styling to the app"""
    custom_css = """
    <style>
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #FF6B6B;
        --success-color: #51CF66;
        --warning-color: #FFD93D;
        --danger-color: #FF6B6B;
        --dark-bg: #0F1419;
        --light-bg: #F8F9FF;
        --card-bg: #FFFFFF;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #F8F9FF 0%, #E8EBFF 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6C63FF 0%, #5A4FFF 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: #6C63FF;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        background-color: #F0F0F7;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #E8EBFF;
        box-shadow: 0 2px 8px rgba(108, 99, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6C63FF !important;
        color: white !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    .todo-card {
        background: white;
        border-left: 4px solid #6C63FF;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .todo-card:hover {
        box-shadow: 0 4px 16px rgba(108, 99, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .todo-card.high-priority {
        border-left-color: #FF6B6B;
    }
    
    .todo-card.medium-priority {
        border-left-color: #FFD93D;
    }
    
    .todo-card.low-priority {
        border-left-color: #51CF66;
    }
    
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.3);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C63FF 0%, #5A4FFF 100%);
    }
    
    .stTextInput, .stTextArea, .stSelectbox, .stSlider {
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #E8EBFF !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1) !important;
    }
    
    .stTitle {
        color: #6C63FF;
        font-weight: 700;
    }
    
    .stSubheader {
        color: #5A4FFF;
        font-weight: 600;
    }
    
    .todo-title {
        color: #0F1419;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .todo-description {
        color: #5A5A7A;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .todo-meta {
        display: flex;
        gap: 16px;
        font-size: 12px;
        color: #7A7A8A;
        margin-top: 12px;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-high {
        background: #FFE8E8;
        color: #FF6B6B;
    }
    
    .badge-medium {
        background: #FFF9E8;
        color: #FFD93D;
    }
    
    .badge-low {
        background: #E8F8E8;
        color: #51CF66;
    }
    
    .badge-completed {
        background: #E8F8E8;
        color: #51CF66;
    }
    
    .badge-pending {
        background: #FFE8E8;
        color: #FF6B6B;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0F1419;
    }
    
    .success-message {
        background: #E8F8E8;
        border-left: 4px solid #51CF66;
        color: #2A6F2A;
    }
    
    .error-message {
        background: #FFE8E8;
        border-left: 4px solid #FF6B6B;
        color: #8A2A2A;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

apply_custom_theme()

def init_session_state():
    """Initialize session state variables"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

def get_headers():
    """Get headers with authentication token"""
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def register_user(username, email, password, first_name, last_name, role):
    """Register a new user"""
    try:
        data = {
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "role": role
        }
        response = requests.post(f"{BASE_URL}/auth/", json=data)
        if response.status_code == 201:
            return True, "Registration successful! Please login."
        else:
            return False, response.json() if response.text else "Registration failed"
    except Exception as e:
        return False, str(e)

def login_user(username, password):
    """Login user and get token"""
    try:
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        if response.status_code == 200:
            token_data = response.json()
            return True, token_data["access_token"]
        else:
            return False, "Invalid credentials"
    except Exception as e:
        return False, str(e)

def get_current_user():
    """Fetch current user information"""
    try:
        response = requests.get(f"{BASE_URL}/user/", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching user info: {e}")
        return None

def get_all_todos():
    """Fetch all todos for the current user"""
    try:
        response = requests.get(f"{BASE_URL}/todo/", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching todos: {e}")
        return []

def get_todo_by_id(todo_id):
    """Fetch a specific todo by ID"""
    try:
        response = requests.get(f"{BASE_URL}/todo/{todo_id}", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching todo: {e}")
        return None

def create_todo(title, description, priority, completed=False):
    """Create a new todo"""
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed
        }
        response = requests.post(f"{BASE_URL}/todo", json=data, headers=get_headers())
        if response.status_code == 201:
            return True, "Todo created successfully!"
        else:
            return False, response.json() if response.text else "Failed to create todo"
    except Exception as e:
        return False, str(e)

def update_todo(todo_id, title, description, priority, completed):
    """Update a todo"""
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed
        }
        response = requests.put(f"{BASE_URL}/todo/{todo_id}/", json=data, headers=get_headers())
        if response.status_code == 204:
            return True, "Todo updated successfully!"
        else:
            return False, "Failed to update todo"
    except Exception as e:
        return False, str(e)

def delete_todo(todo_id):
    """Delete a todo"""
    try:
        response = requests.delete(f"{BASE_URL}/todo/{todo_id}/", headers=get_headers())
        if response.status_code == 204:
            return True, "Todo deleted successfully!"
        else:
            return False, "Failed to delete todo"
    except Exception as e:
        return False, str(e)

def get_admin_todos():
    """Fetch all todos for admin"""
    try:
        response = requests.get(f"{BASE_URL}/admin/todos", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching todos: {e}")
        return []

def admin_delete_todo(todo_id):
    """Admin delete a todo"""
    try:
        response = requests.delete(f"{BASE_URL}/admin/todo/{todo_id}/", headers=get_headers())
        if response.status_code == 204:
            return True, "Todo deleted successfully!"
        else:
            return False, "Failed to delete todo"
    except Exception as e:
        return False, str(e)

def update_password(current_password, new_password):
    """Update user password"""
    try:
        data = {
            "password": current_password,
            "new_password": new_password
        }
        response = requests.put(f"{BASE_URL}/user/password", json=data, headers=get_headers())
        if response.status_code == 204:
            return True, "Password updated successfully!"
        else:
            return False, "Failed to update password"
    except Exception as e:
        return False, str(e)

def logout():
    """Logout user"""
    st.session_state.token = None
    st.session_state.user_info = None
    st.session_state.current_page = "login"
    st.session_state.user_role = None
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

def login_page():
    """Login page UI with enhanced styling"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center;'><h1 style='color: #6C63FF; font-size: 2.5em;'>🔐 Todo App</h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><p style='color: #7A7A8A; font-size: 1.1em;'>Organize your tasks, boost productivity</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        
        st.markdown("")
        
        col_login, col_register = st.columns(2)
        with col_login:
            if st.button("🔑 Login", use_container_width=True, key="btn_login"):
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.session_state.token = message
                        user_data = get_current_user()
                        st.session_state.user_info = user_data
                        st.session_state.user_role = user_data.get("role") if user_data else None
                        
                        if st.session_state.user_role == "admin":
                            st.session_state.current_page = "admin_panel"
                        else:
                            st.session_state.current_page = "todos"
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {message}")
                else:
                    st.warning("⚠️ Please enter username and password")
        
        with col_register:
            if st.button("📝 Register", use_container_width=True, key="btn_register"):
                st.session_state.current_page = "register"
                st.rerun()

def register_page():
    """Registration page UI with enhanced styling"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center;'><h1 style='color: #6C63FF; font-size: 2.5em;'>📝 Create Account</h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><p style='color: #7A7A8A; font-size: 1em;'>Join us and start organizing your tasks</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        username = st.text_input("👤 Username", placeholder="Choose a username")
        email = st.text_input("📧 Email", placeholder="Enter your email")
        first_name = st.text_input("✍️ First Name", placeholder="Enter first name")
        last_name = st.text_input("✍️ Last Name", placeholder="Enter last name")
        password = st.text_input("🔑 Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Confirm password")
        role = st.selectbox("👑 Role", ["user", "admin"])
        
        st.markdown("")
        
        col_reg, col_back = st.columns(2)
        with col_reg:
            if st.button("✅ Register", use_container_width=True, key="btn_reg"):
                if not all([username, email, first_name, last_name, password, confirm_password]):
                    st.warning("⚠️ Please fill all fields")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    success, message = register_user(username, email, password, first_name, last_name, role)
                    if success:
                        st.success(f"✅ {message}")
                        time.sleep(1)
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ Registration failed: {message}")
        
        with col_back:
            if st.button("🔙 Back to Login", use_container_width=True, key="btn_back"):
                st.session_state.current_page = "login"
                st.rerun()

def todos_page():
    """Todos page UI with enhanced styling"""
    st.title("✅ My Todos")
    
    user = st.session_state.user_info
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"### Welcome, **{user.get('first_name')} {user.get('last_name')}**! 👋")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    tabs = st.tabs(["📋 View All Todos", "🔍 Find Todo by ID", "➕ Create Todo", "👤 My Profile"])
    
    # TAB 1: View All Todos
    with tabs[0]:
        st.subheader("Your Todos")
        todos = get_all_todos()
        
        if todos:
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            completed = sum(1 for t in todos if t.get("completed"))
            pending = len(todos) - completed
            high_priority = sum(1 for t in todos if t.get("priority") >= 7)
            
            with col1:
                st.metric("Total Todos", len(todos))
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("Pending", pending)
            with col4:
                st.metric("High Priority", high_priority)
            
            st.markdown("---")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Completed", "Pending"])
            with col2:
                filter_priority = st.selectbox("Filter by Priority", ["All", "🔴 High (7-9)", "🟡 Medium (4-6)", "🟢 Low (1-3)"])
            
            # Apply filters
            filtered_todos = todos
            if filter_status == "Completed":
                filtered_todos = [t for t in filtered_todos if t.get("completed")]
            elif filter_status == "Pending":
                filtered_todos = [t for t in filtered_todos if not t.get("completed")]
            
            if filter_priority != "All":
                if "High" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if t.get("priority") >= 7]
                elif "Medium" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if 4 <= t.get("priority") < 7]
                elif "Low" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if t.get("priority") < 4]
            
            st.markdown("---")
            
            # Display todos
            for todo in filtered_todos:
                priority_level = todo.get("priority", 5)
                status = "✅ Completed" if todo.get("completed") else "⏳ Pending"
                priority_badge = "🔴" if priority_level >= 7 else "🟡" if priority_level >= 4 else "🟢"
                
                # Determine card class
                priority_class = "high-priority" if priority_level >= 7 else "medium-priority" if priority_level >= 4 else "low-priority"
                
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"<div class='todo-title'>{todo.get('title')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='todo-description'>{todo.get('description')}</div>", unsafe_allow_html=True)
                        
                        badge_priority = f"<span class='badge badge-{'high' if priority_level >= 7 else 'medium' if priority_level >= 4 else 'low'}'>{priority_badge} Level {priority_level}</span>"
                        badge_status = f"<span class='badge badge-{'completed' if todo.get('completed') else 'pending'}'>{status}</span>"
                        st.markdown(f"{badge_priority} &nbsp; {badge_status}", unsafe_allow_html=True)
                        st.caption(f"ID: `{todo.get('id')}`")
                    
                    with col2:
                        if st.button(f"✏️", key=f"edit_{todo.get('id')}", help="Edit this todo"):
                            st.session_state[f"edit_todo_{todo.get('id')}"] = True
                            st.rerun()
                    
                    with col3:
                        if st.button(f"🗑️", key=f"delete_{todo.get('id')}", help="Delete this todo"):
                            success, message = delete_todo(todo.get('id'))
                            if success:
                                st.success(message)
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    # Edit form
                    if st.session_state.get(f"edit_todo_{todo.get('id')}", False):
                        st.markdown("---")
                        st.markdown("**✏️ Edit Todo**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_title = st.text_input("Title", value=todo.get('title'), key=f"title_{todo.get('id')}")
                        with col2:
                            new_priority = st.slider("Priority", 1, 9, todo.get('priority'), key=f"priority_{todo.get('id')}")
                        
                        new_desc = st.text_area("Description", value=todo.get('description'), key=f"desc_{todo.get('id')}", height=80)
                        new_completed = st.checkbox("Mark as Completed", value=todo.get('completed'), key=f"completed_{todo.get('id')}")
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.button("💾 Save Changes", key=f"save_{todo.get('id')}", use_container_width=True):
                                if new_title and new_desc:
                                    success, message = update_todo(todo.get('id'), new_title, new_desc, new_priority, new_completed)
                                    if success:
                                        st.success(message)
                                        st.session_state[f"edit_todo_{todo.get('id')}"] = False
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(message)
                                else:
                                    st.warning("Title and description cannot be empty")
                        with col_cancel:
                            if st.button("❌ Cancel", key=f"cancel_{todo.get('id')}", use_container_width=True):
                                st.session_state[f"edit_todo_{todo.get('id')}"] = False
                                st.rerun()
        else:
            st.info("📭 No todos yet! Create one to get started.")
    
    # TAB 2: Find Todo by ID
    with tabs[1]:
        st.subheader("🔍 Find Todo by ID")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            todo_id = st.text_input("Enter Todo ID", placeholder="e.g., 1, 2, 3...")
        with col2:
            search_clicked = st.button("Search", use_container_width=True)
        
        if search_clicked and todo_id:
            try:
                todo_id_int = int(todo_id)
                todo = get_todo_by_id(todo_id_int)
                
                if todo:
                    priority_level = todo.get("priority", 5)
                    status = "✅ Completed" if todo.get("completed") else "⏳ Pending"
                    priority_badge = "🔴" if priority_level >= 7 else "🟡" if priority_level >= 4 else "🟢"
                    
                    st.success(f"✅ Todo found!")
                    st.markdown("---")
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"<div class='todo-title'>{todo.get('title')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='todo-description'>{todo.get('description')}</div>", unsafe_allow_html=True)
                            
                            badge_priority = f"<span class='badge badge-{'high' if priority_level >= 7 else 'medium' if priority_level >= 4 else 'low'}'>{priority_badge} Level {priority_level}</span>"
                            badge_status = f"<span class='badge badge-{'completed' if todo.get('completed') else 'pending'}'>{status}</span>"
                            st.markdown(f"{badge_priority} &nbsp; {badge_status}", unsafe_allow_html=True)
                            st.caption(f"ID: `{todo.get('id')}`")
                        
                        with col2:
                            if st.button(f"✏️ Edit", key=f"quick_edit_{todo.get('id')}"):
                                st.session_state[f"quick_edit_todo_{todo.get('id')}"] = True
                        
                        if st.session_state.get(f"quick_edit_todo_{todo.get('id')}", False):
                            st.markdown("---")
                            st.markdown("**✏️ Edit Todo**")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                new_title = st.text_input("Title", value=todo.get('title'), key=f"quick_title_{todo.get('id')}")
                            with col2:
                                new_priority = st.slider("Priority", 1, 9, todo.get('priority'), key=f"quick_priority_{todo.get('id')}")
                            
                            new_desc = st.text_area("Description", value=todo.get('description'), key=f"quick_desc_{todo.get('id')}", height=80)
                            new_completed = st.checkbox("Mark as Completed", value=todo.get('completed'), key=f"quick_completed_{todo.get('id')}")
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.button("💾 Save Changes", key=f"quick_save_{todo.get('id')}", use_container_width=True):
                                    if new_title and new_desc:
                                        success, message = update_todo(todo.get('id'), new_title, new_desc, new_priority, new_completed)
                                        if success:
                                            st.success(message)
                                            st.session_state[f"quick_edit_todo_{todo.get('id')}"] = False
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error(message)
                                    else:
                                        st.warning("Title and description cannot be empty")
                            with col_cancel:
                                if st.button("❌ Cancel", key=f"quick_cancel_{todo.get('id')}", use_container_width=True):
                                    st.session_state[f"quick_edit_todo_{todo.get('id')}"] = False
                                    st.rerun()
                else:
                    st.error(f"❌ Todo with ID {todo_id} not found")
            except ValueError:
                st.error("❌ Please enter a valid todo ID (number)")
        elif search_clicked:
            st.warning("⚠️ Please enter a todo ID")
    
    # TAB 3: Create Todo
    with tabs[2]:
        st.subheader("➕ Create a New Todo")
        
        with st.form("create_todo_form"):
            title = st.text_input("📝 Title", placeholder="Enter todo title")
            description = st.text_area("📄 Description", placeholder="Enter todo description", height=120)
            priority = st.slider("⭐ Priority Level", 1, 9, 5, 
                               help="🟢 Low (1-3), 🟡 Medium (4-6), 🔴 High (7-9)")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("➕ Create Todo", use_container_width=True)
            with col2:
                st.form_submit_button("Clear Form", use_container_width=True, on_click=lambda: None)
            
            if submitted:
                if title and description:
                    success, message = create_todo(title, description, priority)
                    if success:
                        st.success("✅ Todo created successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {message}")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    # TAB 4: Profile
    with tabs[3]:
        st.subheader("👤 Your Profile")
        if user:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**👤 Name:** {user.get('first_name')} {user.get('last_name')}")
                st.markdown(f"**@️ Username:** {user.get('username')}")
            with col2:
                st.markdown(f"**📧 Email:** {user.get('email')}")
                st.markdown(f"**👑 Role:** {user.get('role')}")
            
            st.markdown("---")
            st.subheader("🔐 Change Password")
            
            current_pwd = st.text_input("Current Password", type="password", placeholder="Enter current password")
            new_pwd = st.text_input("New Password", type="password", placeholder="Enter new password")
            confirm_pwd = st.text_input("Confirm New Password", type="password", placeholder="Confirm new password")
            
            if st.button("🔐 Update Password", use_container_width=True):
                if current_pwd and new_pwd and confirm_pwd:
                    if new_pwd != confirm_pwd:
                        st.error("❌ New passwords do not match")
                    elif len(new_pwd) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        success, message = update_password(current_pwd, new_pwd)
                        if success:
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill all fields")

def admin_panel():
    """Admin panel UI with enhanced styling"""
    st.title("⚙️ Admin Dashboard")
    
    user = st.session_state.user_info
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"### Welcome, **Admin {user.get('first_name')}**! 👋")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    tabs = st.tabs(["📊 All Todos", "👤 Admin Profile"])
    
    with tabs[0]:
        st.subheader("📊 System Overview")
        todos = get_admin_todos()
        
        if todos:
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            completed = sum(1 for t in todos if t.get("completed"))
            pending = len(todos) - completed
            high_priority = sum(1 for t in todos if t.get("priority") >= 7)
            
            with col1:
                st.metric("Total Todos", len(todos))
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("Pending", pending)
            with col4:
                st.metric("High Priority", high_priority)
            
            st.markdown("---")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Completed", "Pending"])
            with col2:
                filter_priority = st.selectbox("Filter by Priority", ["All", "🔴 High (7-9)", "🟡 Medium (4-6)", "🟢 Low (1-3)"])
            with col3:
                search_term = st.text_input("Search by title", placeholder="Type to search...")
            
            # Apply filters
            filtered_todos = todos
            if filter_status == "Completed":
                filtered_todos = [t for t in filtered_todos if t.get("completed")]
            elif filter_status == "Pending":
                filtered_todos = [t for t in filtered_todos if not t.get("completed")]
            
            if filter_priority != "All":
                if "High" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if t.get("priority") >= 7]
                elif "Medium" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if 4 <= t.get("priority") < 7]
                elif "Low" in filter_priority:
                    filtered_todos = [t for t in filtered_todos if t.get("priority") < 4]
            
            if search_term:
                filtered_todos = [t for t in filtered_todos if search_term.lower() in t.get("title", "").lower()]
            
            st.markdown("---")
            st.markdown(f"**Showing {len(filtered_todos)} of {len(todos)} todos**")
            st.markdown("---")
            
            # Display todos
            for todo in filtered_todos:
                priority_level = todo.get("priority", 5)
                status = "✅ Completed" if todo.get("completed") else "⏳ Pending"
                priority_badge = "🔴" if priority_level >= 7 else "🟡" if priority_level >= 4 else "🟢"
                
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1.5, 0.5])
                    
                    with col1:
                        st.markdown(f"<div class='todo-title'>{todo.get('title')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='todo-description'>{todo.get('description')}</div>", unsafe_allow_html=True)
                        
                        badge_priority = f"<span class='badge badge-{'high' if priority_level >= 7 else 'medium' if priority_level >= 4 else 'low'}'>{priority_badge} Level {priority_level}</span>"
                        badge_status = f"<span class='badge badge-{'completed' if todo.get('completed') else 'pending'}'>{status}</span>"
                        st.markdown(f"{badge_priority} &nbsp; {badge_status}", unsafe_allow_html=True)
                        st.caption(f"ID: `{todo.get('id')}` | Owner ID: `{todo.get('owner_id')}`")
                    
                    with col2:
                        st.caption(f"📅 Created by user {todo.get('owner_id')}")
                    
                    with col3:
                        if st.button(f"🗑️", key=f"admin_delete_{todo.get('id')}", help="Delete this todo"):
                            success, message = admin_delete_todo(todo.get('id'))
                            if success:
                                st.success(message)
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
        else:
            st.info("📭 No todos in the system yet")
    
    with tabs[1]:
        st.subheader("👤 Your Admin Profile")
        if user:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**👤 Name:** {user.get('first_name')} {user.get('last_name')}")
                st.markdown(f"**@️ Username:** {user.get('username')}")
            with col2:
                st.markdown(f"**📧 Email:** {user.get('email')}")
                st.markdown(f"**👑 Role:** {user.get('role')}")
            
            st.markdown("---")
            st.subheader("🔐 Change Password")
            
            current_pwd = st.text_input("Current Password", type="password", placeholder="Enter current password", key="admin_pwd_current")
            new_pwd = st.text_input("New Password", type="password", placeholder="Enter new password", key="admin_pwd_new")
            confirm_pwd = st.text_input("Confirm New Password", type="password", placeholder="Confirm new password", key="admin_pwd_confirm")
            
            if st.button("🔐 Update Password", use_container_width=True):
                if current_pwd and new_pwd and confirm_pwd:
                    if new_pwd != confirm_pwd:
                        st.error("❌ New passwords do not match")
                    elif len(new_pwd) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        success, message = update_password(current_pwd, new_pwd)
                        if success:
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill all fields")

def main():
    """Main app logic"""
    init_session_state()
    
    if st.session_state.token:
        if st.session_state.current_page == "todos":
            todos_page()
        elif st.session_state.current_page == "admin_panel":
            admin_panel()
    else:
        if st.session_state.current_page == "register":
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
