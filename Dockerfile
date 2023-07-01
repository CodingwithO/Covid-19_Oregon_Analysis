# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Sets the application directory
WORKDIR /app

# Copies the rest of the application
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r COVID19_Dash_app/requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "/app/COVID19_Dash_app/app.py"]
