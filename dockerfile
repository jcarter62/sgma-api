FROM python:latest
#
RUN mkdir /app
WORKDIR /app
#
copy ./requirements.txt /app/requirements.txt
#
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-compile -r requirements.txt

COPY . /app
# RUN chmod +x /app/start.sh
#
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400"]
ENTRYPOINT ["bash"]




