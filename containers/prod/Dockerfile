#FROM ubuntu:18.04
#
#ENV TZ=Asia/Tokyo
#
#RUN apt-get update -qq \
#    && apt-get install -y \
#        build-essential \
#        curl unzip\
#        python3.7 python3-pip python-pip  \
#        libpq-dev \
#        software-properties-common python3.7-dev autoconf libtool libboost-all-dev libsqlite3-dev
#
##ENV DEBIAN_FRONTEND=noninteractive
#RUN add-apt-repository -y ppa:ondrej/php \
#    && apt-get install -y php5.6 php5.6-sqlite php5.6-zip libmecab-dev
#
#RUN ln -f -s /usr/bin/python3.7 /usr/bin/python
#
## Install Dams
#ENV DAMS_DIR=/opt/dams DAMS_VER=dams-4.3.4
#RUN mkdir -p $DAMS_DIR && cd $DAMS_DIR \
#    && curl -O http://newspat.csis.u-tokyo.ac.jp/download/${DAMS_VER}.tgz && tar zxvf ${DAMS_VER}.tgz \
#    && (cd ${DAMS_VER} \
#        && ./configure --prefix=/usr/local \
#        && make \
#        && make install \
#        && make dic \
#        && make install-dic)
#
### INSTALL geonlp
#ENV GEONLP_INSTALL_DIR=/opt/geonlp
#ENV GEONLP_DIR=$HOME/geonlp_dic
#ENV GEONLP_BRANCH=master
#ENV GEONLP_REPO=https://codeload.github.com/t-sagara/geonlp-software/zip/$GEONLP_BRANCH
#RUN mkdir -p ${GEONLP_INSTALL_DIR} && cd ${GEONLP_INSTALL_DIR} \
#    && curl -o $GEONLP_BRANCH.zip $GEONLP_REPO && unzip ${GEONLP_BRANCH}.zip \
#    && ( cd geonlp-software-${GEONLP_BRANCH} \
#        && sh ./autotools.sh && ./configure --prefix=/usr/local \
#        && make && make install \
#        && ( cd geonlp-dic-util \
#            && php geonlp-dic-util.php add geonlp/japan_pref geonlp/japan_city geonlp/japan_station \
#            && php geonlp-dic-util.php compile \
#            && echo yes | php geonlp-dic-util.php install) \
#        && ( cd python-extension/pygeonlp && python setup.py install) \
#       )
#ENV LD_LIBRARY_PATH=/usr/local/lib

FROM python:3.7.5

ENV APP_ROOT=/app
ENV TZ=Asia/Tokyo

# Install Poetry
RUN pip install poetry

# SETUP for app
WORKDIR $APP_ROOT

COPY ./api/poetry.lock $APP_ROOT
COPY ./api/pyproject.toml $APP_ROOT
RUN poetry config virtualenvs.create false
RUN poetry install

RUN mkdir -p /run/gunicorn

# SETUP app
COPY ./api .

## Download jageocoder
# RUN curl https://www.info-proto.com/static/jusho.zip --output jusho.zip
COPY ./jusho.zip .

## Install jageocoder
RUN python ./install_jageocoder.py
RUN rm jusho.zip

WORKDIR $APP_ROOT/tablelinker

CMD poetry run gunicorn --pid /run/gunicorn/pid --bind 0.0.0.0:8000 --timeout 300 --workers 3 --threads 1 config.wsgi:application

