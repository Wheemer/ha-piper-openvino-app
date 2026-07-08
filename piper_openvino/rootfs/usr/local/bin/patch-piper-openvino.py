#!/usr/bin/env python3
"""Patch piper-tts to select ONNX Runtime OpenVINO provider by environment."""

from __future__ import annotations

from pathlib import Path
import site


OLD = '''        providers: list[Union[str, tuple[str, dict[str, Any]]]]
        if use_cuda:
            providers = [
                (
                    "CUDAExecutionProvider",
                    {"cudnn_conv_algo_search": "HEURISTIC"},
                )
            ]
            _LOGGER.debug("Using CUDA")
        else:
            providers = ["CPUExecutionProvider"]
'''

NEW = '''        providers: list[Union[str, tuple[str, dict[str, Any]]]]
        provider_name = os.environ.get("PIPER_ONNX_PROVIDER", "").strip()
        if provider_name == "OpenVINOExecutionProvider":
            device_type = os.environ.get("PIPER_OPENVINO_DEVICE", "GPU").strip() or "GPU"
            providers = [
                (
                    "OpenVINOExecutionProvider",
                    {"device_type": device_type},
                ),
                "CPUExecutionProvider",
            ]
            _LOGGER.info("Using OpenVINO provider: %s", device_type)
        elif use_cuda:
            providers = [
                (
                    "CUDAExecutionProvider",
                    {"cudnn_conv_algo_search": "HEURISTIC"},
                )
            ]
            _LOGGER.debug("Using CUDA")
        else:
            providers = ["CPUExecutionProvider"]
'''


def main() -> None:
    candidates = []
    for site_dir in site.getsitepackages():
        candidates.append(Path(site_dir) / "piper" / "voice.py")

    for voice_py in candidates:
        if not voice_py.exists():
            continue

        text = voice_py.read_text(encoding="utf-8")
        if "PIPER_ONNX_PROVIDER" in text:
            return

        if "import os" not in text:
            text = text.replace("import json\n", "import json\nimport os\n", 1)

        if OLD not in text:
            raise RuntimeError(f"Provider block not found in {voice_py}")

        voice_py.write_text(text.replace(OLD, NEW), encoding="utf-8")
        return

    raise RuntimeError("Could not find piper/voice.py")


if __name__ == "__main__":
    main()
