# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /code
ENV PYTHONHASHSEED=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./main.py /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]