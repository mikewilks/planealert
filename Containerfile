FROM python:latest
RUN pip install --upgrade pip
RUN pip install apprise requests
ADD ./planealert.py /app/planealert.py
CMD ["python", "/app/planealert.py","/input"]
