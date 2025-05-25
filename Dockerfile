# Use the official Python base image
FROM python:3.10-slim

# Copy requirements first
COPY requirements.txt .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy application code into container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

#disable usage telemetry and browser auto-launch
ENV STREAMLIT_TELEMETRY_DISABLED=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]