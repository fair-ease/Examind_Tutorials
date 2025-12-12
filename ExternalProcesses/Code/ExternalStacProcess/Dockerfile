FROM python:3.9-slim

# Install requests to handle HTTP and JSON
RUN pip install requests

# Add the script to the container
ADD stac_downloader.py /stac_downloader.py

# Set the entrypoint
ENTRYPOINT ["python", "/stac_downloader.py"]
