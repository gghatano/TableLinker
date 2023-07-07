# Build Vue App
FROM node:16.9.1 as build
ENV APP_ROOT=/app
WORKDIR $APP_ROOT
ADD ./app/package.json $APP_ROOT
ADD ./app/yarn.lock $APP_ROOT
RUN yarn install
ADD ./app $APP_ROOT
RUN yarn build

# Build Django Static File.
FROM python:3.7.5 as django_static
ENV APP_ROOT=/app
RUN pip install poetry
WORKDIR $APP_ROOT
COPY ./api/poetry.lock $APP_ROOT
COPY ./api/pyproject.toml $APP_ROOT
RUN poetry config virtualenvs.create false
RUN poetry install
COPY ./api $APP_ROOT
WORKDIR $APP_ROOT/tablelinker
RUN python manage.py collectstatic --noinput
RUN ls static

# Build Nginx 
FROM nginx:1.11.3
ENV APP_ROOT=/app
WORKDIR $APP_ROOT
RUN mkdir -p /app/public/static/
COPY --from=django_static /app/tablelinker/static/ /app/public/static/
COPY --from=build /app/dist /app/public/
RUN rm -f /etc/nginx/nginx.conf
ADD containers/nginx/nginx.conf /etc/nginx/nginx.conf
CMD /usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf