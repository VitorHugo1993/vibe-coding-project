# Deploy API to Heroku

## Quick Setup:

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create nezasa-api-demo
   ```

4. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

## Your API will be at:
`https://nezasa-api-demo.herokuapp.com`

## Update Streamlit:
```python
API_BASE_URL = "https://nezasa-api-demo.herokuapp.com"
```
