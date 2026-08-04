import streamlit as st
import requests
import time

#BASE_URL = "http://localhost:8000"
BASE_URL = "https://todoapp-backend-1fm4.onrender.com"

st.set_page_config(
    page_title="Taskflow",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap');

        :root {
            --ink: #1a2332;
            --muted: #5c6b7a;
            --surface: rgba(255, 255, 255, 0.78);
            --surface-solid: #f4f7f5;
            --accent: #0f766e;
            --accent-deep: #0d5c56;
            --accent-soft: #ccfbf1;
            --warn: #c2410c;
            --warn-soft: #ffedd5;
            --ok: #15803d;
            --ok-soft: #dcfce7;
            --line: rgba(26, 35, 50, 0.08);
            --shadow: 0 18px 40px rgba(15, 40, 50, 0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse 80% 50% at 10% -10%, rgba(15, 118, 110, 0.18), transparent 55%),
                radial-gradient(ellipse 60% 40% at 90% 10%, rgba(194, 65, 12, 0.10), transparent 50%),
                linear-gradient(165deg, #e8f0ec 0%, #f7faf8 40%, #eef3f1 100%);
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        h1, h2, h3, .brand-mark {
            font-family: 'Source Serif 4', Georgia, serif !important;
            letter-spacing: -0.02em;
            color: var(--ink) !important;
        }

        .brand-hero {
            text-align: center;
            padding: 2.5rem 1rem 1.5rem;
            animation: riseIn 0.7s ease-out both;
        }

        .brand-mark {
            font-size: 3.2rem;
            font-weight: 700;
            color: var(--accent-deep) !important;
            margin: 0;
            line-height: 1.1;
        }

        .brand-tag {
            margin-top: 0.6rem;
            color: var(--muted);
            font-size: 1.05rem;
            font-weight: 400;
        }

        .auth-shell {
            background: var(--surface);
            backdrop-filter: blur(12px);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 2rem 2.2rem 1.5rem;
            box-shadow: var(--shadow);
            animation: riseIn 0.8s ease-out 0.1s both;
        }

        .page-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 1rem;
            margin-bottom: 0.5rem;
            animation: riseIn 0.5s ease-out both;
        }

        .page-top h1 {
            margin: 0;
            font-size: 2.1rem;
        }

        .page-top .sub {
            color: var(--muted);
            margin-top: 0.25rem;
            font-size: 0.95rem;
        }

        .stat-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.85rem;
            margin: 1.25rem 0 1.5rem;
            animation: riseIn 0.55s ease-out 0.08s both;
        }

        .stat {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            box-shadow: var(--shadow);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }

        .stat:hover {
            transform: translateY(-3px);
            box-shadow: 0 22px 44px rgba(15, 40, 50, 0.12);
        }

        .stat .label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--muted);
            font-weight: 600;
        }

        .stat .value {
            font-family: 'Source Serif 4', Georgia, serif;
            font-size: 1.85rem;
            font-weight: 700;
            color: var(--ink);
            margin-top: 0.2rem;
        }

        .todo-row {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 8px 22px rgba(15, 40, 50, 0.04);
            border-left: 3px solid var(--accent);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            animation: riseIn 0.45s ease-out both;
        }

        .todo-row:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }

        .todo-row.p-high { border-left-color: var(--warn); }
        .todo-row.p-mid { border-left-color: #ca8a04; }
        .todo-row.p-low { border-left-color: var(--ok); }
        .todo-row.done { opacity: 0.72; }

        .todo-title {
            font-weight: 600;
            font-size: 1.05rem;
            color: var(--ink);
            margin: 0 0 0.25rem;
        }

        .todo-desc {
            color: var(--muted);
            font-size: 0.9rem;
            margin: 0 0 0.65rem;
            line-height: 1.45;
        }

        .meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            align-items: center;
        }

        .chip {
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .chip-high { background: var(--warn-soft); color: var(--warn); }
        .chip-mid { background: #fef9c3; color: #a16207; }
        .chip-low { background: var(--ok-soft); color: var(--ok); }
        .chip-done { background: var(--ok-soft); color: var(--ok); }
        .chip-open { background: #e0f2fe; color: #0369a1; }
        .chip-id { background: #f1f5f9; color: var(--muted); }

        .profile-panel {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            box-shadow: var(--shadow);
        }

        .profile-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.85rem 1.5rem;
            margin-bottom: 0.5rem;
        }

        .profile-field .k {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--muted);
            font-weight: 600;
        }

        .profile-field .v {
            font-size: 1.05rem;
            color: var(--ink);
            font-weight: 500;
            margin-top: 0.15rem;
        }

        .empty-state {
            text-align: center;
            padding: 2.5rem 1rem;
            color: var(--muted);
            background: var(--surface);
            border: 1px dashed var(--line);
            border-radius: 16px;
        }

        .section-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
            font-weight: 600;
            margin: 0.5rem 0 0.75rem;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 0.35rem;
            background: transparent;
            border-bottom: 1px solid var(--line);
            padding-bottom: 0.35rem;
        }

        div[data-testid="stTabs"] [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: var(--muted);
            font-weight: 500;
            padding: 0.55rem 1rem;
        }

        div[data-testid="stTabs"] [aria-selected="true"] {
            background: var(--accent-soft) !important;
            color: var(--accent-deep) !important;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
            border: none;
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-deep) 100%);
            color: white;
            box-shadow: 0 8px 18px rgba(15, 118, 110, 0.28);
        }

        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 12px 24px rgba(15, 118, 110, 0.35);
        }

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div {
            border-radius: 10px !important;
            border: 1px solid var(--line) !important;
            background: rgba(255,255,255,0.9) !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15) !important;
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 0.75rem 1rem;
        }

        hr {
            border: none;
            border-top: 1px solid var(--line);
            margin: 1.25rem 0;
        }

        @keyframes riseIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .stat-row { grid-template-columns: 1fr 1fr; }
            .brand-mark { font-size: 2.4rem; }
            .profile-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session_state():
    defaults = {
        "token": None,
        "user_info": None,
        "current_page": "login",
        "user_role": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_headers():
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers


# ── Auth APIs ──────────────────────────────────────────────

def register_user(username, email, password, first_name, last_name, role):
    try:
        data = {
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "role": role,
        }
        response = requests.post(f"{BASE_URL}/auth/", json=data, timeout=30)
        if response.status_code == 201:
            return True, "Account created. Sign in to continue."
        return False, response.json() if response.text else "Registration failed"
    except Exception as e:
        return False, str(e)


def login_user(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={"username": username, "password": password},
            timeout=30,
        )
        if response.status_code == 200:
            return True, response.json()["access_token"]
        return False, "Invalid username or password"
    except Exception as e:
        return False, str(e)


def get_all_users():
    """GET /auth/users — list every registered user (admin view)."""
    try:
        response = requests.get(f"{BASE_URL}/auth/users", timeout=30)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Could not load users: {e}")
        return []


# ── User APIs ──────────────────────────────────────────────

def get_current_user():
    try:
        response = requests.get(f"{BASE_URL}/user/", headers=get_headers(), timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Could not load profile: {e}")
        return None


def update_password(current_password, new_password):
    try:
        data = {"password": current_password, "new_password": new_password}
        response = requests.put(
            f"{BASE_URL}/user/password",
            json=data,
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 204:
            return True, "Password updated."
        detail = response.json().get("detail", "Failed to update password") if response.text else "Failed"
        return False, detail
    except Exception as e:
        return False, str(e)


# ── Todo APIs ──────────────────────────────────────────────

def get_all_todos():
    try:
        response = requests.get(f"{BASE_URL}/todo/", headers=get_headers(), timeout=30)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Could not load todos: {e}")
        return []


def get_todo_by_id(todo_id):
    try:
        response = requests.get(
            f"{BASE_URL}/todo/{todo_id}",
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Could not fetch todo: {e}")
        return None


def create_todo(title, description, priority, completed=False):
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
        }
        response = requests.post(
            f"{BASE_URL}/todo",
            json=data,
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 201:
            return True, "Todo created."
        return False, response.json() if response.text else "Create failed"
    except Exception as e:
        return False, str(e)


def update_todo(todo_id, title, description, priority, completed):
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
        }
        response = requests.put(
            f"{BASE_URL}/todo/{todo_id}/",
            json=data,
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 204:
            return True, "Todo updated."
        return False, "Update failed"
    except Exception as e:
        return False, str(e)


def delete_todo(todo_id):
    try:
        response = requests.delete(
            f"{BASE_URL}/todo/{todo_id}/",
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 204:
            return True, "Todo deleted."
        return False, "Delete failed"
    except Exception as e:
        return False, str(e)


# ── Admin APIs ─────────────────────────────────────────────

def get_admin_todos():
    try:
        response = requests.get(
            f"{BASE_URL}/admin/todos",
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Could not load admin todos: {e}")
        return []


def admin_delete_todo(todo_id):
    try:
        response = requests.delete(
            f"{BASE_URL}/admin/todo/{todo_id}/",
            headers=get_headers(),
            timeout=30,
        )
        if response.status_code == 204:
            return True, "Todo deleted."
        return False, "Delete failed"
    except Exception as e:
        return False, str(e)


# ── Helpers ────────────────────────────────────────────────

def priority_meta(level):
    if level >= 7:
        return "high", "p-high", "High"
    if level >= 4:
        return "mid", "p-mid", "Medium"
    return "low", "p-low", "Low"


def render_stats(todos):
    completed = sum(1 for t in todos if t.get("completed"))
    pending = len(todos) - completed
    high = sum(1 for t in todos if t.get("priority", 0) >= 7)
    st.markdown(
        f"""
        <div class="stat-row">
            <div class="stat"><div class="label">Total</div><div class="value">{len(todos)}</div></div>
            <div class="stat"><div class="label">Done</div><div class="value">{completed}</div></div>
            <div class="stat"><div class="label">Open</div><div class="value">{pending}</div></div>
            <div class="stat"><div class="label">High priority</div><div class="value">{high}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_todo_card(todo, key_prefix="", show_owner=False, on_delete=None):
    level = todo.get("priority", 5)
    chip_cls, row_cls, label = priority_meta(level)
    done = todo.get("completed", False)
    status_chip = "chip-done" if done else "chip-open"
    status_text = "Completed" if done else "Open"
    done_cls = "done" if done else ""
    owner_html = (
        f'<span class="chip chip-id">Owner #{todo.get("owner_id")}</span>'
        if show_owner
        else ""
    )

    st.markdown(
        f"""
        <div class="todo-row {row_cls} {done_cls}">
            <p class="todo-title">{todo.get("title", "")}</p>
            <p class="todo-desc">{todo.get("description", "")}</p>
            <div class="meta">
                <span class="chip chip-{chip_cls}">{label} · {level}</span>
                <span class="chip {status_chip}">{status_text}</span>
                <span class="chip chip-id">#{todo.get("id")}</span>
                {owner_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 1, 6]) if on_delete is None else st.columns([1, 1, 1, 5])
    tid = todo.get("id")

    with cols[0]:
        if st.button("Edit", key=f"{key_prefix}edit_{tid}", use_container_width=True):
            st.session_state[f"edit_todo_{tid}"] = True
            st.rerun()

    with cols[1]:
        if st.button("Delete", key=f"{key_prefix}del_{tid}", use_container_width=True):
            deleter = on_delete or delete_todo
            ok, msg = deleter(tid)
            if ok:
                st.toast(msg)
                time.sleep(0.4)
                st.rerun()
            else:
                st.error(msg)

    if st.session_state.get(f"edit_todo_{tid}", False):
        with st.expander("Edit task", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                new_title = st.text_input(
                    "Title", value=todo.get("title"), key=f"{key_prefix}title_{tid}"
                )
            with c2:
                new_priority = st.slider(
                    "Priority", 1, 9, todo.get("priority", 5), key=f"{key_prefix}pri_{tid}"
                )
            new_desc = st.text_area(
                "Description",
                value=todo.get("description"),
                key=f"{key_prefix}desc_{tid}",
                height=90,
            )
            new_done = st.checkbox(
                "Mark completed",
                value=todo.get("completed", False),
                key=f"{key_prefix}done_{tid}",
            )
            s1, s2 = st.columns(2)
            with s1:
                if st.button("Save", key=f"{key_prefix}save_{tid}", type="primary", use_container_width=True):
                    if new_title and new_desc:
                        ok, msg = update_todo(tid, new_title, new_desc, new_priority, new_done)
                        if ok:
                            st.session_state[f"edit_todo_{tid}"] = False
                            st.toast(msg)
                            time.sleep(0.4)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Title and description are required.")
            with s2:
                if st.button("Cancel", key=f"{key_prefix}cancel_{tid}", use_container_width=True):
                    st.session_state[f"edit_todo_{tid}"] = False
                    st.rerun()


def logout():
    st.session_state.token = None
    st.session_state.user_info = None
    st.session_state.current_page = "login"
    st.session_state.user_role = None
    st.rerun()


def filter_todos(todos, status_filter, priority_filter, search=""):
    filtered = list(todos)
    if status_filter == "Completed":
        filtered = [t for t in filtered if t.get("completed")]
    elif status_filter == "Open":
        filtered = [t for t in filtered if not t.get("completed")]

    if priority_filter == "High (7–9)":
        filtered = [t for t in filtered if t.get("priority", 0) >= 7]
    elif priority_filter == "Medium (4–6)":
        filtered = [t for t in filtered if 4 <= t.get("priority", 0) < 7]
    elif priority_filter == "Low (1–3)":
        filtered = [t for t in filtered if t.get("priority", 0) < 4]

    if search:
        q = search.lower()
        filtered = [
            t
            for t in filtered
            if q in (t.get("title") or "").lower() or q in (t.get("description") or "").lower()
        ]
    return filtered


def render_profile(user, pwd_key_prefix=""):
    st.markdown(
        f"""
        <div class="profile-panel">
            <div class="profile-grid">
                <div class="profile-field"><div class="k">Name</div><div class="v">{user.get('first_name', '')} {user.get('last_name', '')}</div></div>
                <div class="profile-field"><div class="k">Username</div><div class="v">{user.get('username', '')}</div></div>
                <div class="profile-field"><div class="k">Email</div><div class="v">{user.get('email', '')}</div></div>
                <div class="profile-field"><div class="k">Role</div><div class="v">{user.get('role', '')}</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<p class="section-label" style="margin-top:1.5rem">Change password</p>', unsafe_allow_html=True)
    current_pwd = st.text_input(
        "Current password",
        type="password",
        key=f"{pwd_key_prefix}pwd_cur",
        placeholder="Current password",
    )
    new_pwd = st.text_input(
        "New password",
        type="password",
        key=f"{pwd_key_prefix}pwd_new",
        placeholder="At least 6 characters",
    )
    confirm_pwd = st.text_input(
        "Confirm new password",
        type="password",
        key=f"{pwd_key_prefix}pwd_cfm",
        placeholder="Repeat new password",
    )
    if st.button("Update password", type="primary", key=f"{pwd_key_prefix}pwd_btn"):
        if not all([current_pwd, new_pwd, confirm_pwd]):
            st.warning("Fill in all password fields.")
        elif new_pwd != confirm_pwd:
            st.error("New passwords do not match.")
        elif len(new_pwd) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            ok, msg = update_password(current_pwd, new_pwd)
            if ok:
                st.success(msg)
            else:
                st.error(msg)


# ── Pages ──────────────────────────────────────────────────

def login_page():
    st.markdown(
        """
        <div class="brand-hero">
            <h1 class="brand-mark">Taskflow</h1>
            <p class="brand-tag">Plan clearly. Finish what matters!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.35, 1])
    with mid:
        st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Sign in</p>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Your username", label_visibility="collapsed")
        password = st.text_input(
            "Password", type="password", placeholder="Your password", label_visibility="collapsed"
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign in", type="primary", use_container_width=True):
                if username and password:
                    ok, result = login_user(username, password)
                    if ok:
                        st.session_state.token = result
                        user_data = get_current_user()
                        st.session_state.user_info = user_data
                        st.session_state.user_role = user_data.get("role") if user_data else None
                        st.session_state.current_page = (
                            "admin_panel"
                            if st.session_state.user_role == "admin"
                            else "todos"
                        )
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Enter username and password.")
        with c2:
            if st.button("Create account", use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def register_page():
    st.markdown(
        """
        <div class="brand-hero">
            <h1 class="brand-mark">Taskflow</h1>
            <p class="brand-tag">Create your workspace in a minute.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.45, 1])
    with mid:
        st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Register</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First name", placeholder="First name")
            username = st.text_input("Username", placeholder="Username")
            password = st.text_input("Password", type="password", placeholder="Password")
        with c2:
            last_name = st.text_input("Last name", placeholder="Last name")
            email = st.text_input("Email", placeholder="Email")
            confirm_password = st.text_input(
                "Confirm password", type="password", placeholder="Confirm password"
            )
        role = st.selectbox("Role", ["user", "admin"])

        r1, r2 = st.columns(2)
        with r1:
            if st.button("Register", type="primary", use_container_width=True):
                if not all([username, email, first_name, last_name, password, confirm_password]):
                    st.warning("Please fill every field.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    ok, msg = register_user(
                        username, email, password, first_name, last_name, role
                    )
                    if ok:
                        st.success(msg)
                        time.sleep(0.8)
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error(msg)
        with r2:
            if st.button("Back to sign in", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def todos_page():
    user = st.session_state.user_info or {}
    name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "there"

    top_l, top_r = st.columns([5, 1])
    with top_l:
        st.markdown(
            f"""
            <div class="page-top">
                <div>
                    <h1>Your tasks</h1>
                    <p class="sub">Welcome back, {name}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_r:
        st.write("")
        if st.button("Sign out", use_container_width=True):
            logout()

    tabs = st.tabs(["Board", "Find by ID", "New task", "Profile"])

    # ── Board: GET /todo/ · PUT · DELETE ──
    with tabs[0]:
        todos = get_all_todos()
        if todos:
            render_stats(todos)
            f1, f2 = st.columns(2)
            with f1:
                status_filter = st.selectbox("Status", ["All", "Open", "Completed"], key="board_status")
            with f2:
                priority_filter = st.selectbox(
                    "Priority",
                    ["All", "High (7–9)", "Medium (4–6)", "Low (1–3)"],
                    key="board_pri",
                )
            filtered = filter_todos(todos, status_filter, priority_filter)
            st.caption(f"Showing {len(filtered)} of {len(todos)}")
            for todo in filtered:
                render_todo_card(todo, key_prefix="board_")
        else:
            st.markdown(
                '<div class="empty-state"><p>No tasks yet. Create one from the New task tab.</p></div>',
                unsafe_allow_html=True,
            )

    # ── Find: GET /todo/{id} ──
    with tabs[1]:
        st.markdown('<p class="section-label">Lookup</p>', unsafe_allow_html=True)
        s1, s2 = st.columns([4, 1])
        with s1:
            todo_id = st.text_input(
                "Todo ID", placeholder="e.g. 12", label_visibility="collapsed", key="find_id"
            )
        with s2:
            search = st.button("Search", type="primary", use_container_width=True, key="find_btn")

        if search:
            if not todo_id:
                st.warning("Enter a todo ID.")
            else:
                try:
                    todo = get_todo_by_id(int(todo_id))
                    if todo:
                        render_todo_card(todo, key_prefix="find_")
                    else:
                        st.error(f"No todo found with ID {todo_id}.")
                except ValueError:
                    st.error("ID must be a number.")

    # ── Create: POST /todo ──
    with tabs[2]:
        st.markdown('<p class="section-label">New task</p>', unsafe_allow_html=True)
        with st.form("create_todo_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="What needs doing?")
            description = st.text_area("Description", placeholder="Short notes or context", height=110)
            priority = st.slider("Priority", 1, 9, 5, help="1–3 low · 4–6 medium · 7–9 high")
            submitted = st.form_submit_button("Create task", type="primary", use_container_width=True)
            if submitted:
                if title and description:
                    ok, msg = create_todo(title, description, priority)
                    if ok:
                        st.success(msg)
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Title and description are required.")

    # ── Profile: GET /user/ · PUT /user/password ──
    with tabs[3]:
        st.markdown('<p class="section-label">Account</p>', unsafe_allow_html=True)
        if st.button("Refresh profile"):
            st.session_state.user_info = get_current_user()
            st.rerun()
        if st.session_state.user_info:
            render_profile(st.session_state.user_info, pwd_key_prefix="user_")


def admin_panel():
    user = st.session_state.user_info or {}
    name = user.get("first_name") or "Admin"

    top_l, top_r = st.columns([5, 1])
    with top_l:
        st.markdown(
            f"""
            <div class="page-top">
                <div>
                    <h1>Admin</h1>
                    <p class="sub">Signed in as {name}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_r:
        st.write("")
        if st.button("Sign out", use_container_width=True, key="admin_out"):
            logout()

    tabs = st.tabs(["All todos", "Users", "Profile"])

    # ── Admin todos: GET /admin/todos · DELETE /admin/todo/{id}/ ──
    with tabs[0]:
        todos = get_admin_todos()
        if todos:
            render_stats(todos)
            f1, f2, f3 = st.columns(3)
            with f1:
                status_filter = st.selectbox("Status", ["All", "Open", "Completed"], key="adm_status")
            with f2:
                priority_filter = st.selectbox(
                    "Priority",
                    ["All", "High (7–9)", "Medium (4–6)", "Low (1–3)"],
                    key="adm_pri",
                )
            with f3:
                search = st.text_input("Search", placeholder="Title or description", key="adm_search")
            filtered = filter_todos(todos, status_filter, priority_filter, search)
            st.caption(f"Showing {len(filtered)} of {len(todos)}")
            for todo in filtered:
                render_todo_card(
                    todo,
                    key_prefix="admin_",
                    show_owner=True,
                    on_delete=admin_delete_todo,
                )
        else:
            st.markdown(
                '<div class="empty-state"><p>No todos in the system.</p></div>',
                unsafe_allow_html=True,
            )

    # ── Users: GET /auth/users ──
    with tabs[1]:
        st.markdown('<p class="section-label">Registered users</p>', unsafe_allow_html=True)
        users = get_all_users()
        if users:
            st.caption(f"{len(users)} accounts")
            for u in users:
                st.markdown(
                    f"""
                    <div class="todo-row">
                        <p class="todo-title">{u.get('first_name', '')} {u.get('last_name', '')}</p>
                        <p class="todo-desc">{u.get('email', '')}</p>
                        <div class="meta">
                            <span class="chip chip-id">@{u.get('username', '')}</span>
                            <span class="chip chip-open">{u.get('role', 'user')}</span>
                            <span class="chip chip-id">#{u.get('id')}</span>
                            <span class="chip {'chip-done' if u.get('is_active') else 'chip-high'}">
                                {'Active' if u.get('is_active') else 'Inactive'}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="empty-state"><p>No users found.</p></div>',
                unsafe_allow_html=True,
            )

    # ── Profile ──
    with tabs[2]:
        st.markdown('<p class="section-label">Account</p>', unsafe_allow_html=True)
        if st.button("Refresh profile", key="admin_refresh"):
            st.session_state.user_info = get_current_user()
            st.rerun()
        if st.session_state.user_info:
            render_profile(st.session_state.user_info, pwd_key_prefix="admin_")


def main():
    apply_theme()
    init_session_state()

    if st.session_state.token:
        if st.session_state.current_page == "admin_panel":
            admin_panel()
        else:
            todos_page()
    elif st.session_state.current_page == "register":
        register_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
