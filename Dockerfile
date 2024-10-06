# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any necessary packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 5000

# Create a flag file with the desired content
RUN echo 'BBJ{1t5_5tr0ng_bl4ckl1st_15nt_1t?}' > flag.txt

# Command to run the Flask app
CMD ["python", "app.py"]
