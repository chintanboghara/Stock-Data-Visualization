FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . /app/

# Configure Streamlit settings
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# Expose the port that Streamlit will run on
EXPOSE 5000

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]