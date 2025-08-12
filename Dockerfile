# 1. Base Image: Use a slim, official Python image for a smaller footprint.
FROM python:3.11-slim

# 2. Set Environment Variables:
# - Prevents Python from writing.pyc files to disk.
# - Prevents Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set Working Directory:
WORKDIR /app

# 4. Install Dependencies:
# - Copy only the requirements file first to leverage Docker cache.
# - This layer is only rebuilt when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy Application Code:
# - Copy the application source code into the container.
# - This layer is rebuilt on every code change.
COPY ./src ./src

# 6. Expose Port:
# - Inform Docker that the container listens on port 8080.
# - Cloud Run will automatically use the PORT environment variable.
EXPOSE 8080

# 7. Run the Application:
# - Use the exec form for graceful shutdowns.
# - The web server listens on 0.0.0.0 to be accessible from outside the container.
# - The port is dynamically set by the PORT environment variable provided by Cloud Run.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]