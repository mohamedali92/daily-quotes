FROM python:3.6
COPY tests/test-requirements.txt /
RUN pip install -r /test-requirements.txt
COPY . /app
WORKDIR /app
CMD ["bash"]