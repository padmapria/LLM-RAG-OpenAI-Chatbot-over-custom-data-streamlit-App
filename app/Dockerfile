# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
	
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the index_documents.py script first and then start the Streamlit application
CMD sh -c "python index_documents.py && streamlit run rag.py --server.port=8501 --server.address=0.0.0.0"
