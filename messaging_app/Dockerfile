# Use the base Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY Requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# Copy the project code into the container
COPY . .

# Expose the port Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
