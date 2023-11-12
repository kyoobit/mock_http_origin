# Use a smaller image
FROM docker.io/library/alpine:latest

# Install the required Python modules
RUN apk add python3 py3-pip
RUN pip install --upgrade tornado

# Add the files used by the app
RUN mkdir /mock_http_origin
COPY app.py /mock_http_origin/app.py
COPY cli.py /mock_http_origin/cli.py
COPY football.svg /mock_http_origin/football.svg
COPY help.txt /mock_http_origin/help.txt

# Set the command to run on start up
ENTRYPOINT ["python3", "/mock_http_origin/cli.py"]
