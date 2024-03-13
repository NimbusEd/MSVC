# Base python package
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy the dependencies
COPY req.txt req.txt

# Install the dependencies
RUN pip install -r req.txt

COPY . .

# Executable commands
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]