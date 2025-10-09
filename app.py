import streamlit as st

# Set page config
st.set_page_config(
    page_title="Hello World App",
    page_icon="👋",
    layout="centered"
)

# Main content
st.title("👋 Hello World!")
st.markdown("Welcome to your first Streamlit app!")

# Add some interactive elements
st.header("Interactive Demo")
name = st.text_input("What's your name?", placeholder="Enter your name here")

if name:
    st.success(f"Hello, {name}! 👋")
else:
    st.info("Please enter your name above to see a personalized greeting!")

# Add some additional content
st.header("About This App")
st.markdown("""
This is a simple Streamlit application that demonstrates:
- Basic Streamlit components
- User input handling
- Dynamic content updates
- Clean, modern UI

**Enjoy exploring Streamlit!** 🚀
""")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("This is your first Streamlit app!")
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")

