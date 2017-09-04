FROM python:3.6-alpine
LABEL maintainer="Ivan Tyshchenko <iv.tihon@gmail.com>"
RUN /usr/local/bin/python3 -m pip install flask && \
  mkdir -p /opt/singleclickuvnc/{static,templates}
ADD __main__.py /opt/singleclickuvnc/__main__.py
COPY ./static/ /opt/singleclickuvnc/static/
COPY ./templates/ /opt/singleclickuvnc/templates/
ENV IDSETTER ""
ENV REPEATER ""
ENV DISTR ""
EXPOSE 5000
CMD ["/usr/local/bin/python3", "/opt/singleclickuvnc"]
