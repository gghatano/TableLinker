FROM node:16.9.1-stretch

ENV APP_ROOT=/app
ENV TZ=Asia/Tokyo

# Prepare App
WORKDIR $APP_ROOT
COPY . $APP_ROOT

# Install modules
RUN --mount=type=cache,target=/usr/local/share/.cache \
  yarn install

# Launch service
WORKDIR $APP_ROOT
ENV PORT=8080
CMD yarn run dev --host 0.0.0.0

