FROM python:3.7

# Expose port you want your app on
WORKDIR /app

COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8501 

CMD ["streamlit", "run", "app.py"]
