# Piper OpenVINO

Local Wyoming text-to-speech for Home Assistant Assist using Piper and the
ONNX Runtime OpenVINO execution provider.

## Requirements

- Home Assistant OS on `amd64` Intel hardware.
- Intel integrated graphics exposed as `/dev/dri/renderD128`.
- Internet access to download the selected voice.

## Setup

1. Install the **Piper OpenVINO** app.
2. Choose a voice, leave `openvino_device` set to `GPU`, save, and start the app.
3. Wait for the voice download to finish.
4. Add the discovered Piper OpenVINO service under **Settings > Devices & services**.
5. Select its text-to-speech entity in **Settings > Voice assistants**.

The Wyoming endpoint listens on port `10200`. Discovery works internally. For
manual setup, assign host port `10200` in the app's **Network** panel and connect
the Wyoming integration to the Home Assistant host address and port `10200`.

## Options

| Option | Default | Purpose |
| --- | --- | --- |
| `voice` | `en_US-lessac-medium` | Piper voice model. |
| `openvino_device` | `GPU` | OpenVINO execution device. |
| `speaker` | `0` | Speaker ID for multi-speaker voices. |
| `length_scale` | `1.0` | Speech speed; lower values speak faster. |
| `noise_scale` | `0.667` | Voice variability. |
| `noise_w` | `0.333` | Duration variability. |
| `debug_logging` | `false` | Detailed runtime logging. |
| `update_voices` | `true` | Refresh the voice catalog at startup. |

## Troubleshooting

- Confirm the log lists `OpenVINOExecutionProvider` and the intended GPU device.
- Duplicate discovery normally indicates a second Piper service or an old Wyoming
  config entry.
- For LibriTTS, verify both the voice and speaker ID.

Source, installation button, build status, and update policy are available on
the [repository home page](https://github.com/Wheemer/ha-piper-openvino-app).
