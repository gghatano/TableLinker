FROM ubuntu:16.04

ENV APP_ROOT=/app
ENV TZ=Asia/Tokyo

RUN apt-get update -qq \
    && apt-get install -y \
        nginx \
        apache2 \
        libapache2-mod-wsgi \
        libpq5 \
        git-core \
        wget
#        postgresql

RUN wget http://packaging.ckan.org/python-ckan_2.8-xenial_amd64.deb && dpkg -i python-ckan_2.8-xenial_amd64.deb

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_CONFIG /etc/ckan/default
ENV CKAN_STORAGE_PATH=/var/lib/ckan

ENV CONFIG="${CKAN_CONFIG}/default/production.ini"
ADD ./production.ini $CONFIG
ADD ./who.ini $CONFIG

ADD ./ckan-entrypoint.sh /ckan-entrypoint.sh
RUN chmod +x /ckan-entrypoint.sh

EXPOSE 5000

CMD ["/ckan-entrypoint.sh", "ckan", "serve"]