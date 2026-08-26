ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Piper
WORKDIR /usr/src
ARG BUILD_ARCH
ARG WYOMING_PIPER_VERSION=2.4.2
ARG INTEL_COMPUTE_RUNTIME_VERSION=24.35.30872.36
ARG INTEL_LEVEL_ZERO_VERSION=1.5.30872.36
ARG INTEL_IGC_VERSION=1.0.17537.24
ARG INTEL_GMMLIB_VERSION=22.5.0
ENV PIP_BREAK_SYSTEM_PACKAGES=1
COPY rootfs /
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        netcat-traditional \
        ocl-icd-libopencl1 \
        python3 \
        python3-pip \
    && mkdir -p /tmp/intel-legacy \
    && cd /tmp/intel-legacy \
    && curl -fLO --retry 5 --retry-delay 2 --connect-timeout 20 --max-time 300 "https://github.com/intel/intel-graphics-compiler/releases/download/igc-${INTEL_IGC_VERSION}/intel-igc-core_${INTEL_IGC_VERSION}_amd64.deb" \
    && curl -fLO --retry 5 --retry-delay 2 --connect-timeout 20 --max-time 300 "https://github.com/intel/intel-graphics-compiler/releases/download/igc-${INTEL_IGC_VERSION}/intel-igc-opencl_${INTEL_IGC_VERSION}_amd64.deb" \
    && curl -fLO --retry 5 --retry-delay 2 --connect-timeout 20 --max-time 300 "https://github.com/intel/compute-runtime/releases/download/${INTEL_COMPUTE_RUNTIME_VERSION}/intel-level-zero-gpu-legacy1_${INTEL_LEVEL_ZERO_VERSION}_amd64.deb" \
    && curl -fLO --retry 5 --retry-delay 2 --connect-timeout 20 --max-time 300 "https://github.com/intel/compute-runtime/releases/download/${INTEL_COMPUTE_RUNTIME_VERSION}/intel-opencl-icd-legacy1_${INTEL_COMPUTE_RUNTIME_VERSION}_amd64.deb" \
    && curl -fLO --retry 5 --retry-delay 2 --connect-timeout 20 --max-time 300 "https://github.com/intel/compute-runtime/releases/download/${INTEL_COMPUTE_RUNTIME_VERSION}/libigdgmm12_${INTEL_GMMLIB_VERSION}_amd64.deb" \
    && printf '%s  %s\n' \
        '40dfbd15ab62de036a00824b304a2aa1fa2d81ad60ef83da09cfe3c5a80c429f' "intel-level-zero-gpu-legacy1_${INTEL_LEVEL_ZERO_VERSION}_amd64.deb" \
        'bbe71e4f414259e06a10cde72c29a2bd78d41b2bb2f6f8463b1806797fe66e85' "intel-opencl-icd-legacy1_${INTEL_COMPUTE_RUNTIME_VERSION}_amd64.deb" \
        'cc29d14df83cff1b3c6a66baa39257f0211b168ab43a99c2dc62a3734431bc23' "libigdgmm12_${INTEL_GMMLIB_VERSION}_amd64.deb" \
        | sha256sum -c - \
    && apt-get install -y --no-install-recommends ./*.deb \
    && cd /usr/src \
    \
    && pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    && pip3 install --no-cache-dir \
        --extra-index-url https://www.piwheels.org/simple \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        "wyoming-piper[zeroconf,zh] @ https://github.com/OHF-Voice/wyoming-piper/archive/refs/tags/v${WYOMING_PIPER_VERSION}.tar.gz" \
    && pip3 uninstall -y onnxruntime \
    && pip3 install --no-cache-dir \
        "numpy<3" \
        onnxruntime-openvino==1.24.1 \
    && python3 /usr/local/bin/patch-piper-openvino.py \
    \
    && rm -rf /tmp/intel-legacy /var/lib/apt/lists/*

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
