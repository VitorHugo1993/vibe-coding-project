# 🗄️ Database Setup Guide

This guide explains how to set up persistent database storage for your Nezasa Credential Management System.

## 🚀 Quick Fix (Already Applied)

✅ **Your data will now persist!** I've updated the `.gitignore` to allow `credentials.db` to be committed to Git.

## 📊 Database Options

### 1. **SQLite (Default - Already Working)**
- ✅ **Current setup**: Uses `credentials.db` file
- ✅ **Data persists**: Your data will no longer be deleted on commits
- ✅ **No setup required**: Works out of the box
- ✅ **Perfect for demos**: Reliable and simple

### 2. **PostgreSQL (Recommended for Production)**

#### **Local PostgreSQL Setup:**
```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database
createdb nezasa_credentials

# Install Python dependencies
pip install psycopg2-binary sqlalchemy
```

#### **Configure PostgreSQL:**
1. Edit `database_config.py`
2. Change `DATABASE_TYPE = "postgresql"`
3. Update `POSTGRESQL_CONFIG` with your credentials:
```python
POSTGRESQL_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "nezasa_credentials",
    "username": "your_username",
    "password": "your_password"
}
```

### 3. **Cloud Database Options (Free Tiers Available)**

#### **Supabase (Recommended)**
1. Go to [supabase.com](https://supabase.com)
2. Create free account and new project
3. Copy connection string from Settings > Database
4. Update `database_config.py`:
```python
DATABASE_TYPE = "postgresql"
POSTGRESQL_URL = "postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"
```

#### **Railway**
1. Go to [railway.app](https://railway.app)
2. Create PostgreSQL database
3. Copy connection string
4. Update configuration

#### **Render**
1. Go to [render.com](https://render.com)
2. Create PostgreSQL database
3. Copy connection string
4. Update configuration

## 🔧 Configuration Files

### `database_config.py`
```python
# Database Type: "sqlite" or "postgresql"
DATABASE_TYPE = "sqlite"

# For PostgreSQL
POSTGRESQL_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "nezasa_credentials",
    "username": "your_username",
    "password": "your_password"
}
```

### `.gitignore` (Updated)
```
# Allow our credentials database for demo purposes
!credentials.db
```

## 🎯 Current Status

✅ **Your SQLite database will now persist between commits**
✅ **No data loss when you commit changes**
✅ **Ready for your product demo**

## 🚀 Next Steps

1. **For Demo**: Keep using SQLite (already working)
2. **For Production**: Consider PostgreSQL or cloud database
3. **For Team**: Use cloud database for shared access

## 📝 Troubleshooting

### Issue: "Database not found"
**Solution**: The app will automatically create the database on first run

### Issue: "Permission denied"
**Solution**: Ensure write permissions in your project directory

### Issue: PostgreSQL connection fails
**Solution**: Check credentials and ensure PostgreSQL is running

## 🎉 Benefits

- ✅ **Data Persistence**: No more losing data on commits
- ✅ **Multiple Backends**: SQLite for dev, PostgreSQL for production
- ✅ **Easy Migration**: Switch between databases easily
- ✅ **Cloud Ready**: Support for cloud databases
- ✅ **Demo Ready**: Perfect for your product interview

Your credential management system now has robust database storage! 🚀
