# use this Dockerfile to create a local Ubuntu 20.04 image that is
# suitable for use with https://github.com/nektos/act, as suggested
# in https://github.com/nektos/act/issues/418#issuecomment-727261137
#
# Build:
# docker build -f ubuntu-20.04-local.dockerfile -t ubuntu-builder .
#
# Use:
# act -P ubuntu-20.04=ubuntu-builder
#

FROM ubuntu:20.04

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*


# TODO: consider adding python files into /opt/hostedtoolcache/Python/3.7.9/x64
