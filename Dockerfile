FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir streamlit yfinance pandas plotly numpy requests

# Copy the application
COPY . /app/

# Configure Streamlit
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# Expose the port that Streamlit will run on
EXPOSE 5000

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]