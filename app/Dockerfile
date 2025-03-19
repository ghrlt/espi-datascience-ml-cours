# Use an official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code
COPY . .

# Default command: keep the container running (useful for debugging)
# CMD ["tail", "-f", "/dev/null"]

# run the API
CMD ["python3", "src/api.py"]
