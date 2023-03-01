FROM python:3.7

# Expose port you want your app on
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
