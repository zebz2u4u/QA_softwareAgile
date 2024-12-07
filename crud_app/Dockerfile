# Use Python 3.10.12 image based on .... as the base image
FROM python:3.10.12-slim-bullseye

# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONBUFFERED=1

# Define an environment variable for the web service's port, commonly used in cloud services
ENV PORT=8080

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /app

# Copy the entire current directory contents into the container at /app
COPY . /app/

# Upgrade pip to ensure we have the latest version for i7vnstalling dependencies
RUN pip install --upgrade pip

# RUN pip install psycopg2-binary

# Install dependencies from the requirements.txt file to ensure Python environment is ready
RUN pip install -r requirements.txt

# Set the command to run web service using Gunicorn, binding it to 0.0.0.0 and the PORT environment variable
CMD ["gunicorn"  , "--bind", "0.0.0.0:8080", "crud_app.wsgi:application"]


# Inform Docker that the container listens on the specified network port at runtime
EXPOSE 8080