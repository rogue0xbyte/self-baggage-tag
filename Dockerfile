# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (if needed, you can modify this)
# ENV MONGO_URI=<your_mongo_uri>
# ENV SECRET_KEY=<your_secret_key>

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
