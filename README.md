# Piper for Intel OpenVINO
### GPU-accelerated local text-to-speech for Home Assistant Assist

[![Home Assistant App](https://img.shields.io/badge/HOME%20ASSISTANT-APP-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white&labelColor=555555)](https://www.home-assistant.io/apps/)
[![AMD64](https://img.shields.io/badge/AMD64-SUPPORTED-22C55E?style=for-the-badge&labelColor=555555)](https://github.com/Wheemer/ha-piper-openvino-app)
[![Latest release](https://img.shields.io/github/v/release/Wheemer/ha-piper-openvino-app?style=for-the-badge&logo=github&logoColor=white&label=RELEASE&labelColor=555555&color=22C55E)](https://github.com/Wheemer/ha-piper-openvino-app/releases/latest)
[![Publish](https://img.shields.io/github/actions/workflow/status/Wheemer/ha-piper-openvino-app/publish.yml?style=for-the-badge&label=BUILD&labelColor=555555)](https://github.com/Wheemer/ha-piper-openvino-app/actions/workflows/publish.yml)

Piper for Intel OpenVINO provides private, local text-to-speech through the Wyoming
protocol. It is based on [`wyoming-piper`](https://github.com/rhasspy/wyoming-piper)
and replaces its CPU ONNX runtime with the OpenVINO execution provider for Intel
integrated graphics.

The app exposes Wyoming on port `10200`. Text and generated speech stay on the
Home Assistant machine.

## Requirements

- Home Assistant OS with Apps support.
- An `amd64` Intel processor with an integrated GPU.
- A working `/dev/dri/renderD128` render device on the Home Assistant host.
- Internet access to download voice files.

## Installation

[![Add app repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fha-piper-openvino-app)

1. Select the button above, or open **Settings > Apps > App store > Repositories**.
2. Add `https://github.com/Wheemer/ha-piper-openvino-app`.
3. Install **Piper for Intel OpenVINO** from the app store.
4. Open **Configuration**, choose a voice, and leave **OpenVINO device** set to `GPU`.
5. Start the app and wait for the selected voice to download.

## Connect Home Assistant

The app advertises itself through Wyoming discovery. Open **Settings > Devices &
services** and add the discovered **Piper for Intel OpenVINO** service. If discovery is
unavailable, assign host port `10200` on the app's **Network** panel and add the
Wyoming integration using the Home Assistant host address and port `10200`.

Then open **Settings > Voice assistants**, edit the desired Assist pipeline, and
select the new Piper text-to-speech entity and voice.

## Configuration

| Option | Default | Purpose |
| --- | --- | --- |
| `voice` | `en_US-lessac-medium` | Piper voice model. |
| `openvino_device` | `GPU` | OpenVINO device: `GPU`, `CPU`, or `AUTO`. |
| `speaker` | `0` | Speaker ID for multi-speaker voices such as LibriTTS. |
| `length_scale` | `1.0` | Speech speed; lower values speak faster. |
| `noise_scale` | `0.667` | Voice variability. |
| `noise_w` | `0.333` | Phoneme duration variability. |
| `debug_logging` | `false` | Detailed Piper and OpenVINO logs. |
| `update_voices` | `true` | Refresh the upstream voice catalog at startup. |

Downloaded voice models are stored in the app's shared voice location and are
excluded from app backups where the file pattern applies.

## Troubleshooting

- Confirm the app log lists `OpenVINOExecutionProvider` and the intended GPU device.
- A second discovered Piper usually means another Piper service is still running or
  its old Wyoming config entry remains in Home Assistant.
- If speech works but sounds wrong, verify both the voice and speaker ID; LibriTTS
  voices contain many distinct speakers.
- Assign host port `10200` only when manual Wyoming configuration or LAN access is
  required. Discovery does not require a public host port.

## Updates

GitHub checks `wyoming-piper`, `onnxruntime-openvino`, base images, and workflow
actions every week. Proposed updates are built on a GitHub-hosted runner and opened
as pull requests. Merging a reviewed update publishes a new GHCR image; installing
that update in Home Assistant remains manual.

## Development

The prebuilt image is published as
`ghcr.io/wheemer/amd64-app-piper-openvino:<version>`.

The OpenVINO compatibility patch lives in
`piper_openvino/rootfs/usr/local/bin/patch-piper-openvino.py`. Keep the version in
`piper_openvino/config.yaml` matched to the image tag.

## Upstream

- [Home Assistant Piper app](https://github.com/home-assistant/addons/tree/master/piper)
- [Wyoming Piper](https://github.com/rhasspy/wyoming-piper)
- [ONNX Runtime OpenVINO](https://pypi.org/project/onnxruntime-openvino/)
