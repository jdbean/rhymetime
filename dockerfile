FROM python:3.5-slim-stretch
RUN pip install -U pip
COPY ./ /app
WORKDIR /app
RUN pip install -r ./requirements.txt
EXPOSE 5000
ENV FLASK_APP rhymetime
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
