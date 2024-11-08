# Use the Python 3.10 slim image as the base image
FROM python:3.10-slim

# Set the working directory within the container to be /src
WORKDIR /src

# Copy the necessary files and folders into the container
COPY ./requirements.txt /src
COPY ./app /src

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5001 for the app
EXPOSE 5001

# Run the app
CMD ["python3", "app.py"]