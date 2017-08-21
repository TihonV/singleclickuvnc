FROM python:3.6-alpine

RUN /usr/local/bin/python3 -m pip install flask && \
  mkdir -p /opt/singleclickuvnc
ADD __main__.py /opt/singleclickuvnc/__main__.py
# TODO: ADD ENV VARS
CMD ["/usr/local/bin/python3", "/opt/singleclickuvnc"]
