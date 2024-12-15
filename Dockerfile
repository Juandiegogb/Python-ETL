FROM python:3
WORKDIR /etl
COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . .

CMD [ "python", "./src/elt.py" ]
