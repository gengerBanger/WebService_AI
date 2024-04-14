FROM python:3.11.4
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]