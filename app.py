import streamlit as st
import sqlite3
import json
import datetime
import uuid
import hashlib
from typing import Dict, List, Optional, Any
import pandas as pd
import io
import csv
import os
import base64

# Database imports
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="API Credential Management",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Set white background for the entire app */
    .main .block-container {
        background-color: white;
    }
    
    /* Customize Streamlit buttons to be red */
    .stButton > button {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
        border-radius: 0.25rem !important;
        padding: 0.25rem 1rem !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
    }
    
    /* Primary buttons (more prominent red) */
    .stButton > button[kind="primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
    }
    
    /* Force all primary buttons to be red */
    button[kind="primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
    }
    
    /* Override Streamlit's default primary button colors */
    .stButton button[kind="primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
        box-shadow: none !important;
    }
    
    .stButton button[kind="primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
    }
    
    /* Additional override for form primary buttons */
    .stForm button[kind="primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
    }
    
    .stForm button[kind="primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
    }
    
    /* Ultra-specific targeting for Streamlit primary buttons */
    div[data-testid="stButton"] button[kind="primary"],
    .stButton[kind="primary"] button,
    .stForm .stButton button[kind="primary"],
    .element-container .stButton button[kind="primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
        background: #dc3545 !important;
    }
    
    div[data-testid="stButton"] button[kind="primary"]:hover,
    .stButton[kind="primary"] button:hover,
    .stForm .stButton button[kind="primary"]:hover,
    .element-container .stButton button[kind="primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
        background: #c82333 !important;
    }
    
    /* Nuclear option - target by data attributes */
    button[data-testid="baseButton-primary"] {
        background-color: #dc3545 !important;
        border-color: #dc3545 !important;
        color: white !important;
        background: #dc3545 !important;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        background-color: #c82333 !important;
        border-color: #bd2130 !important;
        color: white !important;
        background: #c82333 !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: #6c757d !important;
        border-color: #6c757d !important;
        color: white !important;
    }
    
    /* Form submit buttons */
    .stForm .stButton > button {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
    }
    
    .stForm .stButton > button:hover {
        background-color: #c82333 !important;
        color: white !important;
    }
    
    /* Ensure all form buttons have the same red styling */
    .stForm button[type="submit"] {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
    }
    
    .stForm button[type="submit"]:hover {
        background-color: #c82333 !important;
        color: white !important;
        border-color: #bd2130 !important;
    }
    
    /* Override any secondary button styling in forms */
    .stForm .stButton > button[kind="secondary"] {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
    }
    
    .stForm .stButton > button[kind="secondary"]:hover {
        background-color: #c82333 !important;
        color: white !important;
        border-color: #bd2130 !important;
    }
    
    /* Ensure all button text is white */
    button {
        color: white !important;
    }
    
    /* Override any button text colors */
    .stButton button, .stForm button {
        color: white !important;
    }
    
    /* Logo container - moved to top left */
    .logo-container {
        position: fixed;
        top: 10px;
        left: 20px;
        z-index: 999;
        background-color: white;
        padding: 8px 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .logo-image {
        height: 32px;
        width: auto;
        max-width: 120px;
    }
    
    .logo-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #dc3545;
        margin: 0;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #dc3545;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #dc3545;
        padding-bottom: 1rem;
        background-color: white;
    }
    
    /* Role badge styling */
    .role-badge {
        background-color: #f8d7da;
        color: #dc3545;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 1rem;
        border: 1px solid #f5c6cb;
    }
    
    /* Credential card styling */
    .credential-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    
    /* Success message styling */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    /* Error message styling */
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    /* Warning message styling */
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    /* Override Streamlit's default theme colors */
    .stSelectbox > div > div {
        background-color: white;
    }
    
    .stTextInput > div > div > input {
        background-color: white;
        color: black !important;
    }
    
    /* Ensure all input text is black and readable */
    .stTextInput input {
        color: black !important;
    }
    
    .stTextInput > label {
        color: black !important;
    }
    
    /* Text area inputs */
    .stTextArea > div > div > textarea {
        background-color: white;
        color: black !important;
    }
    
    .stTextArea textarea {
        color: black !important;
    }
    
    /* Selectbox text */
    .stSelectbox > div > div > div {
        color: black !important;
    }
    
    /* Selectbox dropdown arrow */
    .stSelectbox svg {
        fill: black !important;
        color: black !important;
    }
    
    /* Selectbox button arrow */
    .stSelectbox button svg {
        fill: black !important;
        stroke: black !important;
    }
    
    /* Ensure all form input text is black */
    .stForm input, .stForm textarea, .stForm select {
        color: black !important;
    }
    
    /* Customize placeholder text color */
    .stTextInput input::placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input::-webkit-input-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input::-moz-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input:-ms-input-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    /* Placeholder styling for all input types */
    input::placeholder,
    textarea::placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    input::-webkit-input-placeholder,
    textarea::-webkit-input-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    input::-moz-placeholder,
    textarea::-moz-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    input:-ms-input-placeholder,
    textarea:-ms-input-placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    /* Style disabled input fields to match placeholder color but keep white background */
    .stTextInput input[disabled] {
        color: #666666 !important;
        background-color: white !important;
    }
    
    .stTextInput input[disabled="true"] {
        color: #666666 !important;
        background-color: white !important;
    }
    
    /* Override any disabled input styling */
    input[disabled], input[disabled="true"] {
        color: #666666 !important;
        background-color: white !important;
    }
    
    /* Make sure the main content area has white background */
    .stApp {
        background-color: white;
    }
    
    /* Customize expander headers */
    .streamlit-expanderHeader {
        background-color: white !important;
        color: black !important;
    }
    
    /* Expander header hover state */
    .streamlit-expanderHeader:hover {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Expander header selected/active state */
    .streamlit-expanderHeader[aria-expanded="true"] {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background-color: white !important;
        color: black !important;
    }
    
    /* Ensure expander text is always black */
    .streamlit-expanderHeader h3,
    .streamlit-expanderHeader div,
    .streamlit-expanderHeader span {
        color: black !important;
    }
    
    /* Expander button styling */
    .streamlit-expanderHeader button {
        background-color: transparent !important;
        color: black !important;
        border: none !important;
    }
    
    /* Expander icon styling */
    .streamlit-expanderHeader .streamlit-expanderIcon {
        color: black !important;
    }
    
    /* Additional expander states */
    .streamlit-expanderHeader[data-testid="streamlit-expanderHeader"] {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Focus state for accessibility */
    .streamlit-expanderHeader:focus {
        background-color: #dc3545 !important;
        color: white !important;
        outline: 2px solid #dc3545 !important;
    }
    
    /* More specific targeting for expander headers */
    .streamlit-expanderHeader:hover,
    .streamlit-expanderHeader[aria-expanded="true"],
    .streamlit-expanderHeader[data-testid="streamlit-expanderHeader"]:hover,
    .streamlit-expanderHeader[data-testid="streamlit-expanderHeader"][aria-expanded="true"] {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Target the actual expander button */
    .streamlit-expanderHeader button:hover {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Override any Streamlit default styling */
    div[data-testid="streamlit-expanderHeader"] {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    div[data-testid="streamlit-expanderHeader"]:hover {
        background-color: #c82333 !important;
        color: white !important;
    }
    
    
    /* Customize entire sidebar with darker red background */
    .stSidebar {
        background-color: #dc3545 !important;
    }
    
    .stSidebar .css-1d391kg {
        background-color: #dc3545 !important;
    }
    
    /* Sidebar container styling */
    .stSidebar .block-container {
        background-color: #dc3545 !important;
    }
    
    /* Ensure all sidebar content has darker red background */
    .stSidebar .element-container {
        background-color: #dc3545 !important;
    }
    
    /* Sidebar form elements */
    .stSidebar .stSelectbox {
        background-color: #dc3545 !important;
    }
    
    .stSidebar .stSelectbox > div > div {
        background-color: white !important;
        color: black !important;
    }
    
    .stSidebar .stInfo {
        background-color: #dc3545 !important;
    }
    
    /* Sidebar text elements */
    .stSidebar .stMarkdown {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    .stSidebar .stText {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Sidebar headings */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: white !important;
        background-color: #dc3545 !important;
    }
    
    /* Sidebar paragraphs and divs */
    .stSidebar p, .stSidebar div, .stSidebar span {
        color: white !important;
        background-color: #dc3545 !important;
    }
    
    /* Sidebar labels */
    .stSidebar label {
        color: white !important;
        background-color: #dc3545 !important;
    }
    
    /* Override any sidebar background colors */
    .stSidebar .stApp {
        background-color: #dc3545 !important;
    }
    
    /* Sidebar main container */
    .stSidebar > div {
        background-color: #dc3545 !important;
    }
    
    /* Sidebar expandable sections */
    .stSidebar .streamlit-expanderHeader {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    .stSidebar .streamlit-expanderContent {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    /* Additional white background overrides */
    .stApp > header {
        background-color: white;
    }
    
    .stApp > div {
        background-color: white;
    }
    
    /* Ensure dataframes have white background */
    .stDataFrame {
        background-color: white;
    }
    
    /* Customize tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
    }
    
    /* Customize form elements */
    .stForm {
        background-color: white;
    }
    
    /* Ensure all containers have white background */
    .block-container {
        background-color: white !important;
    }
    
    /* Customize selectbox and input backgrounds */
    .stSelectbox > label {
        background-color: white;
    }
    
    .stTextInput > label {
        background-color: white;
    }
    
    /* Make all text black */
    .stApp {
        color: black !important;
    }
    
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: black !important;
    }
    
    .stApp p, .stApp div, .stApp span {
        color: black !important;
    }
    
    /* Ensure Streamlit elements have black text */
    .stMarkdown {
        color: black !important;
    }
    
    .stText {
        color: black !important;
    }
    
    /* Override any default text colors */
    .element-container {
        color: black !important;
    }
    
    /* Ensure table headers and content are black */
    .stDataFrame th, .stDataFrame td {
        color: black !important;
    }
    
    /* Ensure sidebar text is black */
    .stSidebar {
        color: black !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: black !important;
    }
    
    /* Ensure form labels and text are black */
    .stForm label {
        color: black !important;
    }
    
    /* Ensure tab text is black */
    .stTabs [data-baseweb="tab"] {
        color: black !important;
    }
    
    /* Override any inherited colors */
    .main .block-container {
        color: black !important;
    }
    
    /* Ensure expander content is black */
    .streamlit-expanderContent {
        color: black !important;
    }
    
    /* Fix JSON display box styling */
    .stJson {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
        border-radius: 0.25rem !important;
        padding: 1rem !important;
    }
    
    /* JSON content styling */
    .stJson pre {
        background-color: white !important;
        color: black !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* JSON syntax highlighting fix */
    .stJson .token.string {
        color: #0066cc !important;
    }
    
    .stJson .token.number {
        color: #0066cc !important;
    }
    
    .stJson .token.boolean {
        color: #0066cc !important;
    }
    
    .stJson .token.null {
        color: #666 !important;
    }
    
    /* Ensure all JSON elements have proper contrast */
    .stJson * {
        color: black !important;
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Database setup and initialization
class DatabaseManager:
    def __init__(self, db_path: str = "credentials.db", use_postgres: bool = False, postgres_url: str = None):
        self.db_path = db_path
        self.use_postgres = use_postgres
        self.postgres_url = postgres_url
        self.engine = None
        
        if use_postgres and SQLALCHEMY_AVAILABLE and postgres_url:
            try:
                self.engine = create_engine(postgres_url)
                self.init_postgres_database()
            except Exception as e:
                st.warning(f"Failed to connect to PostgreSQL: {e}. Falling back to SQLite.")
                self.use_postgres = False
                self.init_database()
        else:
            self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create credentials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier TEXT NOT NULL,
                environment TEXT NOT NULL,
                auth_type TEXT NOT NULL,
                data TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                allow_self_rotation BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Create audit_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cred_id INTEGER,
                action TEXT NOT NULL,
                actor TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (cred_id) REFERENCES credentials (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Seed sample data if tables are empty
        self._seed_sample_data()
    
    def init_postgres_database(self):
        """Initialize PostgreSQL database with required tables"""
        try:
            with self.engine.connect() as conn:
                # Create credentials table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS credentials (
                        id SERIAL PRIMARY KEY,
                        supplier TEXT NOT NULL,
                        environment TEXT NOT NULL,
                        auth_type TEXT NOT NULL,
                        data TEXT NOT NULL,
                        created_by TEXT NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL,
                        allow_self_rotation BOOLEAN DEFAULT FALSE
                    )
                """))
                
                # Create audit_logs table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id SERIAL PRIMARY KEY,
                        cred_id INTEGER,
                        action TEXT NOT NULL,
                        actor TEXT NOT NULL,
                        details TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        FOREIGN KEY (cred_id) REFERENCES credentials (id)
                    )
                """))
                
                conn.commit()
            
            # Seed sample data if tables are empty
            self._seed_postgres_sample_data()
            
        except Exception as e:
            st.error(f"Error initializing PostgreSQL database: {e}")
            raise
    
    def _seed_sample_data(self):
        """Seed the database with sample credentials if empty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if credentials table is empty
        cursor.execute("SELECT COUNT(*) FROM credentials")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_credentials = [
                {
                    "supplier": "Sabre",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "sabre_prod_key_9x8y7z6"}),
                    "created_by": "alice@nezasa.com",
                    "allow_self_rotation": True
                },
                {
                    "supplier": "Amadeus",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "amadeus_api_a1b2c3d4e5"}),
                    "created_by": "bob@nezasa.com",
                    "allow_self_rotation": False
                },
                {
                    "supplier": "Google Maps",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "AIzaSyD_GoogleMapsKey123"}),
                    "created_by": "alice@nezasa.com",
                    "allow_self_rotation": False
                },
                {
                    "supplier": "Stripe",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "sk_live_stripe_secret_key"}),
                    "created_by": "carol@nezasa.com",
                    "allow_self_rotation": True
                },
                {
                    "supplier": "Payyo",
                    "environment": "sandbox",
                    "auth_type": "username_password",
                    "data": json.dumps({"username": "payyo_sandbox", "password": "payyo_2024_test"}),
                    "created_by": "bob@nezasa.com",
                    "allow_self_rotation": False
                },
                {
                    "supplier": "Viator",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "viator_prod_key_v1a2t3"}),
                    "created_by": "alice@nezasa.com",
                    "allow_self_rotation": True
                },
                {
                    "supplier": "Musement",
                    "environment": "production",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "musement_api_m9u8s7"}),
                    "created_by": "carol@nezasa.com",
                    "allow_self_rotation": False
                },
                {
                    "supplier": "G Adventures",
                    "environment": "production",
                    "auth_type": "username_password",
                    "data": json.dumps({"username": "gadventures_api", "password": "ga_secure_2024"}),
                    "created_by": "bob@nezasa.com",
                    "allow_self_rotation": True
                },
                {
                    "supplier": "OTS Globe",
                    "environment": "staging",
                    "auth_type": "api_key",
                    "data": json.dumps({"api_key": "ots_staging_key_o1t2s3"}),
                    "created_by": "alice@nezasa.com",
                    "allow_self_rotation": False
                },
                {
                    "supplier": "TUI",
                    "environment": "production",
                    "auth_type": "username_password",
                    "data": json.dumps({"username": "tui_prod_user", "password": "tui_password_2024"}),
                    "created_by": "carol@nezasa.com",
                    "allow_self_rotation": True
                }
            ]
            
            now = datetime.datetime.now().isoformat()
            
            for i, cred in enumerate(sample_credentials):
                cursor.execute("""
                    INSERT INTO credentials (supplier, environment, auth_type, data, created_by, created_at, updated_at, allow_self_rotation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cred["supplier"],
                    cred["environment"],
                    cred["auth_type"],
                    cred["data"],
                    cred["created_by"],
                    now,
                    now,
                    cred["allow_self_rotation"]
                ))
                
                # Log the creation
                cred_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    cred_id,
                    "create",
                    cred["created_by"],
                    f"Created credential for {cred['supplier']} ({cred['environment']})",
                    now
                ))
                
                # Add additional audit log examples for variety
                if i == 0:  # Sabre - add update log
                    cursor.execute("""
                        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cred_id,
                        "update",
                        "bob@nezasa.com",
                        f"Updated authentication data for {cred['supplier']}",
                        now
                    ))
                elif i == 1:  # Amadeus - add rotation log
                    cursor.execute("""
                        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cred_id,
                        "rotate",
                        "alice@nezasa.com",
                        f"Rotated API key for {cred['supplier']}",
                        now
                    ))
                elif i == 3:  # Stripe - add view log
                    cursor.execute("""
                        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cred_id,
                        "view",
                        "carol@nezasa.com",
                        f"Viewed credential details for {cred['supplier']}",
                        now
                    ))
                elif i == 5:  # Viator - add rotation log
                    cursor.execute("""
                        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cred_id,
                        "rotate",
                        "bob@nezasa.com",
                        f"Rotated API key for {cred['supplier']}",
                        now
                    ))
                elif i == 7:  # G Adventures - add update log
                    cursor.execute("""
                        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cred_id,
                        "update",
                        "carol@nezasa.com",
                        f"Updated password for {cred['supplier']}",
                        now
                    ))
            
                conn.commit()
            
            conn.close()
    
    def _seed_postgres_sample_data(self):
        """Seed PostgreSQL database with sample credentials if empty"""
        try:
            with self.engine.connect() as conn:
                # Check if credentials table is empty
                result = conn.execute(text("SELECT COUNT(*) FROM credentials"))
                count = result.scalar()
                
                if count == 0:
                    sample_credentials = [
                        {
                            "supplier": "Sabre",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "sabre_prod_key_9x8y7z6"}),
                            "created_by": "alice@nezasa.com",
                            "allow_self_rotation": True
                        },
                        {
                            "supplier": "Amadeus",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "amadeus_api_a1b2c3d4e5"}),
                            "created_by": "bob@nezasa.com",
                            "allow_self_rotation": False
                        },
                        {
                            "supplier": "Google Maps",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "AIzaSyD_GoogleMapsKey123"}),
                            "created_by": "alice@nezasa.com",
                            "allow_self_rotation": False
                        },
                        {
                            "supplier": "Stripe",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "sk_live_stripe_secret_key"}),
                            "created_by": "carol@nezasa.com",
                            "allow_self_rotation": True
                        },
                        {
                            "supplier": "Payyo",
                            "environment": "sandbox",
                            "auth_type": "username_password",
                            "data": json.dumps({"username": "payyo_sandbox", "password": "payyo_2024_test"}),
                            "created_by": "bob@nezasa.com",
                            "allow_self_rotation": False
                        },
                        {
                            "supplier": "Viator",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "viator_prod_key_v1a2t3"}),
                            "created_by": "alice@nezasa.com",
                            "allow_self_rotation": True
                        },
                        {
                            "supplier": "Musement",
                            "environment": "production",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "musement_api_m9u8s7"}),
                            "created_by": "carol@nezasa.com",
                            "allow_self_rotation": False
                        },
                        {
                            "supplier": "G Adventures",
                            "environment": "production",
                            "auth_type": "username_password",
                            "data": json.dumps({"username": "gadventures_api", "password": "ga_secure_2024"}),
                            "created_by": "bob@nezasa.com",
                            "allow_self_rotation": True
                        },
                        {
                            "supplier": "OTS Globe",
                            "environment": "staging",
                            "auth_type": "api_key",
                            "data": json.dumps({"api_key": "ots_staging_key_o1t2s3"}),
                            "created_by": "alice@nezasa.com",
                            "allow_self_rotation": False
                        },
                        {
                            "supplier": "TUI",
                            "environment": "production",
                            "auth_type": "username_password",
                            "data": json.dumps({"username": "tui_prod_user", "password": "tui_password_2024"}),
                            "created_by": "carol@nezasa.com",
                            "allow_self_rotation": True
                        }
                    ]
                    
                    now = datetime.datetime.now()
                    
                    for i, cred in enumerate(sample_credentials):
                        # Insert credential
                        conn.execute(text("""
                            INSERT INTO credentials (supplier, environment, auth_type, data, created_by, created_at, updated_at, allow_self_rotation)
                            VALUES (:supplier, :environment, :auth_type, :data, :created_by, :created_at, :updated_at, :allow_self_rotation)
                        """), {
                            "supplier": cred["supplier"],
                            "environment": cred["environment"],
                            "auth_type": cred["auth_type"],
                            "data": cred["data"],
                            "created_by": cred["created_by"],
                            "created_at": now,
                            "updated_at": now,
                            "allow_self_rotation": cred["allow_self_rotation"]
                        })
                        
                        # Log the creation
                        conn.execute(text("""
                            INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                            VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                        """), {
                            "action": "create",
                            "actor": cred["created_by"],
                            "details": f"Created credential for {cred['supplier']} ({cred['environment']})",
                            "timestamp": now
                        })
                        
                        # Add additional audit log examples for variety
                        if i == 0:  # Sabre - add update log
                            conn.execute(text("""
                                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                                VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                            """), {
                                "action": "update",
                                "actor": "bob@nezasa.com",
                                "details": f"Updated authentication data for {cred['supplier']}",
                                "timestamp": now
                            })
                        elif i == 1:  # Amadeus - add rotation log
                            conn.execute(text("""
                                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                                VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                            """), {
                                "action": "rotate",
                                "actor": "alice@nezasa.com",
                                "details": f"Rotated API key for {cred['supplier']}",
                                "timestamp": now
                            })
                        elif i == 3:  # Stripe - add view log
                            conn.execute(text("""
                                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                                VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                            """), {
                                "action": "view",
                                "actor": "carol@nezasa.com",
                                "details": f"Viewed credential details for {cred['supplier']}",
                                "timestamp": now
                            })
                        elif i == 5:  # Viator - add rotation log
                            conn.execute(text("""
                                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                                VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                            """), {
                                "action": "rotate",
                                "actor": "bob@nezasa.com",
                                "details": f"Rotated API key for {cred['supplier']}",
                                "timestamp": now
                            })
                        elif i == 7:  # G Adventures - add update log
                            conn.execute(text("""
                                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                                VALUES (LASTVAL(), :action, :actor, :details, :timestamp)
                            """), {
                                "action": "update",
                                "actor": "carol@nezasa.com",
                                "details": f"Updated password for {cred['supplier']}",
                                "timestamp": now
                            })
                    
                    conn.commit()
                    
        except Exception as e:
            st.error(f"Error seeding PostgreSQL database: {e}")
            raise

# Initialize database
try:
    from database_config import get_database_config
    config = get_database_config()
    
    if config["use_postgres"]:
        db = DatabaseManager(
            use_postgres=True,
            postgres_url=config["postgres_url"]
        )
        # st.success("🔗 Connected to PostgreSQL database")  # Commented out to remove banner
    else:
        db = DatabaseManager(db_path=config["sqlite_path"])
        # st.info("💾 Using SQLite database (data will persist)")  # Commented out to remove banner
        
except ImportError:
    # Fallback to default SQLite if config file not found
    db = DatabaseManager()
    # st.info("💾 Using SQLite database (default)")  # Commented out to remove banner

# Role-based access control
class RBACManager:
    ROLES = {
        "admin": {
            "can_create": True,
            "can_update": True,
            "can_rotate": True,
            "can_view_unmasked": True,
            "can_view_audit": True,
            "description": "Full access to all operations"
        },
        "devops": {
            "can_create": False,
            "can_update": True,
            "can_rotate": False,
            "can_view_unmasked": True,
            "can_view_audit": True,
            "description": "Can update credentials and view audit logs"
        },
        "cs": {
            "can_create": False,
            "can_update": False,
            "can_rotate": False,
            "can_view_unmasked": False,
            "can_view_audit": False,
            "description": "Can only view masked credentials"
        },
        "partner": {
            "can_create": False,
            "can_update": False,
            "can_rotate": "conditional",  # Only if allow_self_rotation is True
            "can_view_unmasked": False,
            "can_view_audit": False,
            "description": "Limited access, can rotate if allowed"
        }
    }
    
    @classmethod
    def has_permission(cls, role: str, action: str, credential_data: Optional[Dict] = None) -> bool:
        """Check if a role has permission for a specific action"""
        if role not in cls.ROLES:
            return False
        
        role_permissions = cls.ROLES[role]
        
        if action == "create":
            return role_permissions["can_create"]
        elif action == "update":
            return role_permissions["can_update"]
        elif action == "rotate":
            if role_permissions["can_rotate"] == "conditional":
                return credential_data and credential_data.get("allow_self_rotation", False)
            return role_permissions["can_rotate"]
        elif action == "view_unmasked":
            return role_permissions["can_view_unmasked"]
        elif action == "view_audit":
            return role_permissions["can_view_audit"]
        
        return False

# Credential management functions
class CredentialManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_all_credentials(self) -> List[Dict]:
        """Retrieve all credentials from the database"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, supplier, environment, auth_type, data, created_by, 
                   created_at, updated_at, allow_self_rotation
            FROM credentials
            ORDER BY updated_at DESC
        """)
        
        credentials = []
        for row in cursor.fetchall():
            credentials.append({
                "id": row[0],
                "supplier": row[1],
                "environment": row[2],
                "auth_type": row[3],
                "data": json.loads(row[4]),
                "created_by": row[5],
                "created_at": row[6],
                "updated_at": row[7],
                "allow_self_rotation": bool(row[8])
            })
        
        conn.close()
        return credentials
    
    def get_credential_by_id(self, cred_id: int) -> Optional[Dict]:
        """Retrieve a specific credential by ID"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, supplier, environment, auth_type, data, created_by, 
                   created_at, updated_at, allow_self_rotation
            FROM credentials
            WHERE id = ?
        """, (cred_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "supplier": row[1],
                "environment": row[2],
                "auth_type": row[3],
                "data": json.loads(row[4]),
                "created_by": row[5],
                "created_at": row[6],
                "updated_at": row[7],
                "allow_self_rotation": bool(row[8])
            }
        return None
    
    def create_credential(self, supplier: str, environment: str, auth_type: str, 
                         data: Dict, created_by: str) -> bool:
        """Create a new credential"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            now = datetime.datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO credentials (supplier, environment, auth_type, data, created_by, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (supplier, environment, auth_type, json.dumps(data), created_by, now, now))
            
            cred_id = cursor.lastrowid
            
            # Log the creation
            cursor.execute("""
                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (cred_id, "create", created_by, f"Created credential for {supplier} ({environment})", now))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error creating credential: {str(e)}")
            return False
    
    def update_credential(self, cred_id: int, auth_type: str, data: Dict, updated_by: str) -> bool:
        """Update an existing credential"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            now = datetime.datetime.now().isoformat()
            
            cursor.execute("""
                UPDATE credentials 
                SET auth_type = ?, data = ?, updated_at = ?
                WHERE id = ?
            """, (auth_type, json.dumps(data), now, cred_id))
            
            # Log the update
            cursor.execute("""
                INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (cred_id, "update", updated_by, f"Updated credential data for ID {cred_id}", now))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error updating credential: {str(e)}")
            return False
    
    def rotate_credential(self, cred_id: int, rotated_by: str) -> bool:
        """Rotate a credential by generating new secret values"""
        try:
            credential = self.get_credential_by_id(cred_id)
            if not credential:
                return False
            
            # Generate new secret based on auth_type
            new_data = {}
            timestamp = datetime.datetime.now().strftime("%Y%m%d")
            
            if credential["auth_type"] == "api_key":
                new_data["api_key"] = f"ak_{credential['environment']}_{timestamp}_{str(uuid.uuid4())[:8]}"
            elif credential["auth_type"] == "username_password":
                new_data["username"] = credential["data"].get("username", "user")
                new_data["password"] = f"pass_{timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Update the credential
            success = self.update_credential(cred_id, credential["auth_type"], new_data, rotated_by)
            
            if success:
                # Log the rotation specifically
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (cred_id, "rotate", rotated_by, f"Rotated credential secrets for {credential['supplier']}", datetime.datetime.now().isoformat()))
                
                conn.commit()
                conn.close()
            
            return success
        except Exception as e:
            st.error(f"Error rotating credential: {str(e)}")
            return False
    
    def get_audit_logs(self, cred_id: Optional[int] = None) -> List[Dict]:
        """Retrieve audit logs, optionally filtered by credential ID"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        if cred_id:
            cursor.execute("""
                SELECT al.id, al.cred_id, al.action, al.actor, al.details, al.timestamp,
                       c.supplier
                FROM audit_logs al
                LEFT JOIN credentials c ON al.cred_id = c.id
                WHERE al.cred_id = ?
                ORDER BY al.timestamp DESC
            """, (cred_id,))
        else:
            cursor.execute("""
                SELECT al.id, al.cred_id, al.action, al.actor, al.details, al.timestamp,
                       c.supplier
                FROM audit_logs al
                LEFT JOIN credentials c ON al.cred_id = c.id
                ORDER BY al.timestamp DESC
            """)
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "id": row[0],
                "cred_id": row[1],
                "action": row[2],
                "actor": row[3],
                "details": row[4],
                "timestamp": row[5],
                "supplier": row[6] if row[6] else "System"
            })
        
        conn.close()
        return logs

# Initialize credential manager
cred_manager = CredentialManager(db)

# Utility functions
def load_logo_image():
    """Load the Nezasa logo image if it exists"""
    logo_paths = ["nezasa_logo.png", "nezasa_logo.jpg", "nezasa_logo.svg", "logo.png", "logo.jpg"]
    
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    image_data = f.read()
                    base64_image = base64.b64encode(image_data).decode()
                    
                    if logo_path.endswith('.svg'):
                        return f"data:image/svg+xml;base64,{base64_image}"
                    elif logo_path.endswith('.png'):
                        return f"data:image/png;base64,{base64_image}"
                    elif logo_path.endswith('.jpg'):
                        return f"data:image/jpeg;base64,{base64_image}"
            except Exception as e:
                print(f"Error loading logo: {e}")
                continue
    
    return None

def mask_secret_data(data: Dict, auth_type: str) -> Dict:
    """Mask secret data for non-admin users"""
    masked_data = {}
    
    if auth_type == "api_key":
        api_key = data.get("api_key", "")
        masked_data["api_key"] = "*****" + api_key[-4:] if len(api_key) > 4 else "*****"
    elif auth_type == "username_password":
        username = data.get("username", "")
        password = data.get("password", "")
        masked_data["username"] = username  # Username can be shown
        masked_data["password"] = "*****" + password[-4:] if len(password) > 4 else "*****"
    
    return masked_data

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.datetime.fromisoformat(timestamp_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

# Streamlit UI
def main():
    # Add Nezasa logo above the page title
    logo_data = load_logo_image()
    
    # Create a container for the logo and title
    if logo_data:
        # Display actual logo image
        st.markdown(f"""
        <div style="text-align: left; margin-bottom: 1rem;">
            <img src="{logo_data}" style="height: 80px; width: auto; max-width: 250px;" alt="Nezasa Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback to text logo
        st.markdown("""
        <div style="text-align: left; margin-bottom: 1rem;">
            <div style="color: #dc3545; font-weight: bold; font-size: 2.8rem;">NEZASA</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🔐 API Credential Management</h1>', unsafe_allow_html=True)
    
    # Role selector in sidebar
    st.sidebar.title("🔑 Role Management")
    selected_role = st.sidebar.selectbox(
        "Select Role:",
        ["admin", "devops", "cs", "partner"],
        help="Choose a role to simulate different access levels"
    )
    
    # Display role info
    role_info = RBACManager.ROLES[selected_role]
    st.sidebar.markdown(f'<span class="role-badge">{selected_role.upper()}</span>', unsafe_allow_html=True)
    st.sidebar.info(f"**{selected_role.title()}**: {role_info['description']}")
    
    # Store role in session state
    st.session_state.current_role = selected_role
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Create Credential", "📋 Audit Logs"])
    
    with tab1:
        dashboard_tab()
    
    with tab2:
        create_credential_tab()
    
    with tab3:
        audit_logs_tab()

def dashboard_tab():
    """Dashboard tab with credential table and management actions"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("📊 Credential Dashboard")
    with col2:
        if st.button("🔄 Refresh Data", help="Refresh to see changes from API requests"):
            st.rerun()
    
    # Show success messages if any actions were completed
    for key, value in st.session_state.items():
        if key.startswith("rotate_success_") and value:
            cred_id = key.replace("rotate_success_", "")
            st.success(f"✅ Credential {cred_id} rotated successfully!")
            st.session_state[key] = False  # Clear the flag
        elif key.startswith("update_success_") and value:
            cred_id = key.replace("update_success_", "")
            st.success(f"✅ Credential {cred_id} updated successfully!")
            st.session_state[key] = False  # Clear the flag
    
    # Get all credentials
    credentials = cred_manager.get_all_credentials()
    
    if not credentials:
        st.info("No credentials found. Create your first credential using the 'Create Credential' tab.")
        return
    
    # Display credentials in a table
    st.subheader(f"Found {len(credentials)} credentials")
    
    # Create a dataframe for display
    display_data = []
    for cred in credentials:
        # Mask data for non-admin users
        if RBACManager.has_permission(st.session_state.current_role, "view_unmasked"):
            display_data_dict = cred["data"]
        else:
            display_data_dict = mask_secret_data(cred["data"], cred["auth_type"])
        
        display_data.append({
            "ID": cred["id"],
            "Supplier": cred["supplier"],
            "Environment": cred["environment"],
            "Auth Type": cred["auth_type"],
            "Data": json.dumps(display_data_dict, indent=2),
            "Created By": cred["created_by"],
            "Updated At": format_timestamp(cred["updated_at"]),
            "Actions": cred["id"]  # Store ID for action buttons
        })
    
    df = pd.DataFrame(display_data)
    
    # Display the table
    st.dataframe(
        df.drop("Actions", axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # Action buttons for each credential
    st.subheader("🔧 Credential Actions")
    
    cols = st.columns(min(len(credentials), 3))
    for i, cred in enumerate(credentials):
        with cols[i % 3]:
            with st.expander(f"🔐 {cred['supplier']} ({cred['environment']})", expanded=False):
                st.write(f"**ID:** {cred['id']}")
                st.write(f"**Created:** {format_timestamp(cred['created_at'])}")
                
                # View button (always available)
                if st.button(f"👁️ View Details", key=f"view_{cred['id']}"):
                    view_credential_details(cred)
                
                # Update button (admin, devops)
                if RBACManager.has_permission(st.session_state.current_role, "update"):
                    if st.button(f"✏️ Update", key=f"update_{cred['id']}"):
                        st.session_state[f"show_update_form_{cred['id']}"] = True
                
                # Rotate button (admin, partner if allowed)
                can_rotate = RBACManager.has_permission(
                    st.session_state.current_role, 
                    "rotate", 
                    cred
                )
                if can_rotate:
                    if st.button(f"🔄 Rotate", key=f"rotate_{cred['id']}"):
                        if cred_manager.rotate_credential(cred['id'], f"{st.session_state.current_role}@demo.com"):
                            st.session_state[f"rotate_success_{cred['id']}"] = True
                            st.success(f"✅ Credential {cred['id']} rotated successfully!")
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Failed to rotate credential")
                elif st.session_state.current_role == "partner":
                    st.warning("🔒 Rotation not allowed for this credential")
                
                # Show update form if requested
                if st.session_state.get(f"show_update_form_{cred['id']}", False):
                    show_update_form(cred)

def view_credential_details(credential: Dict):
    """Display detailed credential information"""
    st.info("🔍 **Credential Details**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**ID:** {credential['id']}")
        st.write(f"**Supplier:** {credential['supplier']}")
        st.write(f"**Environment:** {credential['environment']}")
        st.write(f"**Auth Type:** {credential['auth_type']}")
    
    with col2:
        st.write(f"**Created By:** {credential['created_by']}")
        st.write(f"**Created At:** {format_timestamp(credential['created_at'])}")
        st.write(f"**Updated At:** {format_timestamp(credential['updated_at'])}")
        st.write(f"**Self-Rotation:** {'✅ Yes' if credential['allow_self_rotation'] else '❌ No'}")
    
    st.write("**Data:**")
    if RBACManager.has_permission(st.session_state.current_role, "view_unmasked"):
        st.json(credential["data"])
    else:
        masked_data = mask_secret_data(credential["data"], credential["auth_type"])
        st.json(masked_data)
        st.warning("🔒 Data is masked for your role. Admin users can view unmasked data.")

def show_update_form(credential: Dict):
    """Show form to update credential"""
    st.info(f"✏️ **Update Credential {credential['id']}**")
    
    with st.form(f"update_form_{credential['id']}"):
        new_auth_type = st.selectbox(
            "Auth Type:",
            ["api_key", "username_password"],
            index=0 if credential["auth_type"] == "api_key" else 1,
            key=f"auth_type_{credential['id']}"
        )
        
        new_data = {}
        
        if new_auth_type == "api_key":
            api_key = st.text_input(
                "API Key:",
                value=credential["data"].get("api_key", ""),
                key=f"api_key_{credential['id']}"
            )
            new_data = {"api_key": api_key}
        
        elif new_auth_type == "username_password":
            username = st.text_input(
                "Username:",
                value=credential["data"].get("username", ""),
                key=f"username_{credential['id']}"
            )
            password = st.text_input(
                "Password:",
                value=credential["data"].get("password", ""),
                type="password",
                key=f"password_{credential['id']}"
            )
            new_data = {"username": username, "password": password}
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            submit_update = st.form_submit_button("💾 Update Credential")
        
        with col2:
            cancel_update = st.form_submit_button("❌ Cancel")
        
        if submit_update:
            if not any(new_data.values()):
                st.error("❌ Please fill in all required fields")
            else:
                if cred_manager.update_credential(
                    credential["id"], 
                    new_auth_type, 
                    new_data, 
                    f"{st.session_state.current_role}@demo.com"
                ):
                    st.session_state[f"update_success_{credential['id']}"] = True
                    st.success("✅ Credential updated successfully!")
                    st.session_state[f"show_update_form_{credential['id']}"] = False
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Failed to update credential")
        
        if cancel_update:
            st.session_state[f"show_update_form_{credential['id']}"] = False
            st.rerun()

def create_credential_tab():
    """Create new credential tab"""
    st.header("➕ Create New Credential")
    
    # Clear any existing success flags (no persistent messages)
    if st.session_state.get('show_creation_success', False):
        st.session_state.show_creation_success = False
    
    # Check permissions
    if not RBACManager.has_permission(st.session_state.current_role, "create"):
        st.error("🚫 **Access Denied**: Only admin users can create credentials.")
        st.info("Current role permissions:")
        role_info = RBACManager.ROLES[st.session_state.current_role]
        for perm, value in role_info.items():
            if not perm.startswith("can_"):
                continue
            status = "✅" if value else "❌"
            st.write(f"{status} {perm.replace('_', ' ').title()}")
        return
    
    
    st.subheader("📝 Credential Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        supplier = st.text_input(
            "Supplier Name:",
            placeholder="e.g., Expedia, Booking.com",
            help="Name of the API supplier",
            key="create_supplier"
        )
        environment = st.selectbox(
            "Environment:",
            ["production", "sandbox", "staging", "development"],
            help="Target environment for the credential",
            key="create_environment"
        )
    
    with col2:
        auth_type = st.selectbox(
            "Authentication Type:",
            ["api_key", "username_password"],
            help="Type of authentication required",
            key="create_auth_type"
        )
        created_by = st.text_input(
            "Created By:",
            value=f"{st.session_state.current_role}@demo.com",
            disabled=True,
            help="User creating the credential"
        )
    
    st.subheader("🔑 Authentication Data")
    
    credential_data = {}
    
    if auth_type == "api_key":
        api_key = st.text_input(
            "API Key:",
            placeholder="Enter the API key",
            help="The API key provided by the supplier",
            key="create_api_key"
        )
        if api_key:
            credential_data = {"api_key": api_key}
    
    elif auth_type == "username_password":
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input(
                "Username:",
                placeholder="Enter username",
                help="Username for authentication",
                key="create_username"
            )
        with col2:
            password = st.text_input(
                "Password:",
                placeholder="Enter password",
                type="password",
                help="Password for authentication",
                key="create_password"
            )
        if username and password:
            credential_data = {"username": username, "password": password}
    
    with st.form("create_credential_form"):
        
        st.subheader("⚙️ Additional Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            allow_self_rotation = st.checkbox(
                "Allow Partner Self-Rotation",
                value=False,
                help="Allow partner role to rotate this credential"
            )
        
        with col2:
            # Placeholder for alignment
            st.write("")  # Empty space to align with checkbox
        
        # Aligned buttons
        st.subheader("🎯 Actions")
        
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            # Preview button
            if st.form_submit_button("👁️ Preview Credential", type="primary"):
                if supplier and environment and credential_data:
                    st.success("✅ **Credential Preview**")
                    
                    preview_data = {
                        "ID": "New",
                        "Supplier": supplier,
                        "Environment": environment,
                        "Auth Type": auth_type,
                        "Data": json.dumps(credential_data, indent=2),
                        "Created By": created_by,
                        "Allow Self-Rotation": allow_self_rotation
                    }
                    
                    for key, value in preview_data.items():
                        st.write(f"**{key}:** {value}")
                else:
                    st.warning("⚠️ Please fill in all required fields to see preview")
        
        with button_col2:
            # Submit button
            if st.form_submit_button("🚀 Create Credential", type="primary"):
                # Validation
                if not supplier:
                    st.error("❌ Supplier name is required")
                elif not environment:
                    st.error("❌ Environment is required")
                elif not credential_data:
                    st.error("❌ Authentication data is required")
                else:
                    # Create the credential
                    if cred_manager.create_credential(supplier, environment, auth_type, credential_data, created_by):
                        st.success("🎉 **Credential created successfully!**")
                        # Add a small delay to keep success message visible longer
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Failed to create credential. Please check the logs for details.")
    

def audit_logs_tab():
    """Audit logs tab"""
    st.header("📋 Audit Trail")
    
    # Check permissions
    if not RBACManager.has_permission(st.session_state.current_role, "view_audit"):
        st.error("🚫 **Access Denied**: You don't have permission to view audit logs.")
        st.info("Only admin and devops roles can view audit logs.")
        return
    
    # Filter options
    st.subheader("🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_supplier = st.selectbox(
            "Filter by Supplier:",
            ["All"] + list(set([cred["supplier"] for cred in cred_manager.get_all_credentials()])),
            help="Filter logs by supplier"
        )
    
    with col2:
        filter_action = st.selectbox(
            "Filter by Action:",
            ["All", "create", "update", "rotate"],
            help="Filter logs by action type"
        )
    
    with col3:
        filter_actor = st.selectbox(
            "Filter by Actor:",
            ["All"] + list(set([log["actor"] for log in cred_manager.get_audit_logs()])),
            help="Filter logs by actor (user who performed the action)"
        )
    
    # Get audit logs
    all_logs = cred_manager.get_audit_logs()
    
    # Apply filters
    filtered_logs = all_logs
    
    if filter_supplier != "All":
        filtered_logs = [log for log in filtered_logs if log["supplier"] == filter_supplier]
    
    if filter_action != "All":
        filtered_logs = [log for log in filtered_logs if log["action"] == filter_action]
    
    if filter_actor != "All":
        filtered_logs = [log for log in filtered_logs if log["actor"] == filter_actor]
    
    # Display results
    st.subheader(f"📊 Found {len(filtered_logs)} audit log entries")
    
    if not filtered_logs:
        st.info("No audit logs found matching your filters.")
        return
    
    # Create dataframe for display
    log_data = []
    for log in filtered_logs:
        log_data.append({
            "ID": log["id"],
            "Credential ID": log["cred_id"] if log["cred_id"] else "N/A",
            "Supplier": log["supplier"],
            "Action": log["action"].title(),
            "Actor": log["actor"],
            "Details": log["details"],
            "Timestamp": format_timestamp(log["timestamp"])
        })
    
    df_logs = pd.DataFrame(log_data)
    
    # Display the table
    st.dataframe(
        df_logs,
        use_container_width=True,
        hide_index=True
    )
    
    # Export functionality
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as CSV"):
            csv_buffer = io.StringIO()
            df_logs.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"audit_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Export Summary"):
            # Create summary statistics
            summary_data = {
                "Total Actions": len(filtered_logs),
                "Actions by Type": df_logs["Action"].value_counts().to_dict(),
                "Actions by Actor": df_logs["Actor"].value_counts().to_dict(),
                "Actions by Supplier": df_logs["Supplier"].value_counts().to_dict()
            }
            
            st.json(summary_data)

def api_monitor_tab():
    """API Monitor tab showing live API requests and database view"""
    st.header("🔍 API Monitor & Database View")
    
    st.info("💡 **Demo Tip:** Run API requests in another terminal and watch them appear here in real-time!")
    
    # Add auto-refresh toggle
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### 📡 Live API Request Log")
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=False, help="Automatically refresh every 2 seconds")
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Auto-refresh logic
    if auto_refresh:
        import time
        time.sleep(2)
        st.rerun()
    
    # Read API request log file
    log_file_path = "api_requests.log"
    
    # Check if file exists and show appropriate message
    if not os.path.exists(log_file_path):
        st.warning("⚠️ API log file not found. The API server needs to be running to generate logs.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📍 Current Directory:**")
            st.code(os.getcwd())
        
        with col2:
            st.markdown("**📂 Log File Expected:**")
            st.code(log_file_path)
        
        st.markdown("""
        **To start the API server:**
        
        ```bash
        # Option 1: Direct Python
        python3 api.py
        
        # Option 2: Using uvicorn
        python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
        
        # Option 3: Background (keeps running)
        nohup python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 > api_server.log 2>&1 &
        ```
        
        **Then make a test request:**
        ```bash
        curl -X GET http://localhost:8000/api/v1/credentials \\
          -H "X-API-Key: admin_key_123"
        ```
        
        **Or open interactive docs:**
        http://localhost:8000/api/docs
        """)
    else:
        try:
            with open(log_file_path, "r") as f:
                log_lines = f.readlines()
                
            # Get last 50 lines
            recent_logs = log_lines[-50:] if len(log_lines) > 50 else log_lines
            
            if recent_logs:
                # Display in a nice format with line count
                st.success(f"✅ API server is active! Showing last {len(recent_logs)} log entries.")
                log_text = "".join(recent_logs)
                st.code(log_text, language="log")
            else:
                st.info("📭 Log file exists but is empty. Make some API requests to see them here!")
                st.markdown("""
                **Quick test request:**
                ```bash
                curl -X GET http://localhost:8000/api/v1/credentials \\
                  -H "X-API-Key: admin_key_123"
                ```
                """)
        except Exception as e:
            st.error(f"❌ Error reading log file: {str(e)}")
            st.code(f"File path: {os.path.abspath(log_file_path)}")
    
    st.markdown("---")
    
    # Database View Section
    st.markdown("### 🗄️ Database View")
    
    # Create tabs for different database views
    db_tab1, db_tab2, db_tab3 = st.tabs(["📋 Credentials Table", "📝 Audit Logs Table", "📊 Database Stats"])
    
    with db_tab1:
        st.subheader("Credentials Table (Raw Data)")
        
        # Get all credentials directly from database
        credentials = cred_manager.get_all_credentials()
        
        if credentials:
            # Create dataframe with all fields
            db_data = []
            for cred in credentials:
                # cred["data"] is already a dict, just format it nicely
                data_str = json.dumps(cred["data"], indent=2) if isinstance(cred["data"], dict) else str(cred["data"])
                
                db_data.append({
                    "ID": cred["id"],
                    "Supplier": cred["supplier"],
                    "Environment": cred["environment"],
                    "Auth Type": cred["auth_type"],
                    "Data (JSON)": data_str,
                    "Created By": cred["created_by"],
                    "Created At": cred["created_at"],
                    "Updated At": cred["updated_at"],
                    "Allow Self Rotation": cred["allow_self_rotation"]
                })
            
            df = pd.DataFrame(db_data)
            
            # Display row count
            st.metric("Total Credentials", len(credentials))
            
            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Export option
            if st.button("📥 Export Credentials to CSV"):
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"credentials_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No credentials in database yet.")
    
    with db_tab2:
        st.subheader("Audit Logs Table (Raw Data)")
        
        # Get all audit logs
        logs = cred_manager.get_audit_logs()
        
        if logs:
            # Create dataframe
            log_data = []
            for log in logs:
                # Get supplier name from credential
                cred = next((c for c in credentials if c["id"] == log["cred_id"]), None)
                supplier = cred["supplier"] if cred else f"ID:{log['cred_id']}"
                
                log_data.append({
                    "Log ID": log["id"],
                    "Credential ID": log["cred_id"],
                    "Supplier": supplier,
                    "Action": log["action"],
                    "Actor": log["actor"],
                    "Details": log["details"],
                    "Timestamp": log["timestamp"]
                })
            
            df_logs = pd.DataFrame(log_data)
            
            # Display row count
            st.metric("Total Audit Entries", len(logs))
            
            # Display table
            st.dataframe(
                df_logs,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Export option
            if st.button("📥 Export Audit Logs to CSV"):
                csv_buffer = io.StringIO()
                df_logs.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"audit_logs_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No audit logs in database yet.")
    
    with db_tab3:
        st.subheader("Database Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Credentials", len(credentials))
            st.metric("Total Audit Logs", len(logs) if logs else 0)
        
        with col2:
            if credentials:
                # Count by environment
                env_counts = {}
                for cred in credentials:
                    env = cred["environment"]
                    env_counts[env] = env_counts.get(env, 0) + 1
                
                st.markdown("**By Environment:**")
                for env, count in env_counts.items():
                    st.write(f"- {env}: {count}")
        
        with col3:
            if credentials:
                # Count by auth type
                auth_counts = {}
                for cred in credentials:
                    auth = cred["auth_type"]
                    auth_counts[auth] = auth_counts.get(auth, 0) + 1
                
                st.markdown("**By Auth Type:**")
                for auth, count in auth_counts.items():
                    st.write(f"- {auth}: {count}")
        
        # Action statistics
        if logs:
            st.markdown("---")
            st.markdown("**Actions Over Time:**")
            
            action_counts = {}
            for log in logs:
                action = log["action"]
                action_counts[action] = action_counts.get(action, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Action Types:**")
                for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"- {action}: {count}")
            
            with col2:
                # Most active actors
                actor_counts = {}
                for log in logs:
                    actor = log["actor"]
                    actor_counts[actor] = actor_counts.get(actor, 0) + 1
                
                st.markdown("**Most Active Users:**")
                for actor, count in sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    st.write(f"- {actor}: {count} actions")
    
    # SQL Query Runner (for advanced demo)
    st.markdown("---")
    st.markdown("### 🔧 Advanced: SQL Query Runner")
    
    with st.expander("Run Custom SQL Query (Read-Only)"):
        st.warning("⚠️ This is for demo purposes only. Only SELECT queries are allowed.")
        
        query = st.text_area(
            "SQL Query:",
            value="SELECT * FROM credentials LIMIT 10;",
            help="Enter a SELECT query to run against the database"
        )
        
        if st.button("▶️ Run Query"):
            if query.strip().upper().startswith("SELECT"):
                try:
                    import sqlite3
                    conn = sqlite3.connect("credentials.db")
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    cursor.execute(query)
                    results = cursor.fetchall()
                    conn.close()
                    
                    if results:
                        # Convert to dataframe
                        result_data = [dict(row) for row in results]
                        df_results = pd.DataFrame(result_data)
                        
                        st.success(f"✅ Query executed successfully. {len(results)} rows returned.")
                        st.dataframe(df_results, use_container_width=True, hide_index=True)
                    else:
                        st.info("Query executed successfully but returned no results.")
                        
                except Exception as e:
                    st.error(f"❌ Error executing query: {str(e)}")
            else:
                st.error("❌ Only SELECT queries are allowed for safety reasons.")

# Run the app
if __name__ == "__main__":
    main()
