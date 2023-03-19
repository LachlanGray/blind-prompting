FROM python:latest

# COPY main.py /app/main.py
COPY blind_prompt /blind_prompt

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

CMD ["tail", "-f", "/dev/null"]
