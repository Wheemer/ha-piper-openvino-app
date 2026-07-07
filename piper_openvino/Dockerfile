ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:bookworm
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Piper
WORKDIR /usr/src
ARG BUILD_ARCH
ARG WYOMING_PIPER_VERSION=2.2.2
ENV PIP_BREAK_SYSTEM_PACKAGES=1
COPY rootfs /
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
        python3 \
        python3-pip \
    \
    && pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    && pip3 install --no-cache-dir \
        --extra-index-url https://www.piwheels.org/simple \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        "wyoming-piper[zeroconf,zh] @ https://github.com/rhasspy/wyoming-piper/archive/refs/tags/v${WYOMING_PIPER_VERSION}.tar.gz" \
    && pip3 uninstall -y onnxruntime \
    && pip3 install --no-cache-dir \
        onnxruntime-openvino==1.24.1 \
    && python3 /usr/local/bin/patch-piper-openvino.py \
    \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Wheemer" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Wheemer" \
    org.opencontainers.image.licenses="Apache-2.0" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.version="${BUILD_VERSION}"

HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10200 \
        | grep -q "piper" \
        || exit 1
