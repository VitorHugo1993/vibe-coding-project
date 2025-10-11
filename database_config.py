# Database Configuration
# Choose your database backend and configure connection settings

# Database Backend Options:
# 1. SQLite (default, local file)
# 2. PostgreSQL (recommended for production)

# ===========================================
# CONFIGURATION OPTIONS
# ===========================================

# Database Type: "sqlite" or "postgresql"
DATABASE_TYPE = "sqlite"

# SQLite Configuration (for local development)
SQLITE_DB_PATH = "credentials.db"

# PostgreSQL Configuration (for production/demo)
POSTGRESQL_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "nezasa_credentials",
    "username": "your_username",
    "password": "your_password"
}

# Alternative: PostgreSQL URL (if you have a connection string)
# POSTGRESQL_URL = "postgresql://username:password@localhost:5432/nezasa_credentials"

# ===========================================
# SETUP INSTRUCTIONS
# ===========================================

"""
SQLite Setup (Default - No setup required):
- Uses local credentials.db file
- Data persists between commits (now configured in .gitignore)
- Perfect for demos and development

PostgreSQL Setup (Recommended for production):
1. Install PostgreSQL on your system
2. Create a database: createdb nezasa_credentials
3. Update the POSTGRESQL_CONFIG above with your credentials
4. Change DATABASE_TYPE to "postgresql"
5. Install dependencies: pip install psycopg2-binary sqlalchemy

Cloud Database Options:
- AWS RDS PostgreSQL
- Google Cloud SQL
- Azure Database for PostgreSQL
- Supabase (free tier available)
- Railway (free tier available)
- Render (free tier available)

Example Supabase setup:
1. Create account at supabase.com
2. Create new project
3. Get connection string from Settings > Database
4. Use as POSTGRESQL_URL = "postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"
"""

def get_database_config():
    """Get database configuration based on settings"""
    if DATABASE_TYPE.lower() == "postgresql":
        # Use URL if provided, otherwise construct from config
        if 'POSTGRESQL_URL' in globals():
            return {
                "use_postgres": True,
                "postgres_url": globals()['POSTGRESQL_URL']
            }
        else:
            # Construct URL from config
            config = POSTGRESQL_CONFIG
            url = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            return {
                "use_postgres": True,
                "postgres_url": url
            }
    else:
        return {
            "use_postgres": False,
            "sqlite_path": SQLITE_DB_PATH
        }
