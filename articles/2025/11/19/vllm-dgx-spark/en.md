---
title: Install vLLM on DGX Spark
date: 2025-11-19
tags: install, vLLM, DGX spark, python
thumbnail: mistral-vllm.png
abstract: Step‑by‑step guide to download, compile and run vLLM on an NVIDIA DGX‑Spark system (CUDA 13.0, Python 3.12). 
language: en
---

# Let's install VLLM on the DGX spark
As of 2025/11/19 installing vllm on the spark is not straightforward ! Our goal today is to have a **fully functional vLLM installation** that can serve a `7‑B Mistral` model on a `DGX‑Spark` node. 

# 1. Install the required system packages 
vLLM needs a recent C++ tool‑chain and CMake so that Triton and the flash‑infer JIT can be compiled.

```bash
sudo apt install cmake build-essential ninja-build python3-dev
```

    cmake – generates the makefiles for Triton.  
    build-essential – provides gcc, g++ and make.  
    ninja-build – a fast backend that Triton prefers.  
    python3-dev – header files needed when building Python extensions.

# 2. Create a clean Python environment
We use uv (a fast, modern replacement for pip/venv) to keep the environment reproducible.
```bash
# Install uv if you don’t have it yet
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtualenv with Python 3.12 (the default on DGX‑Spark)
uv venv --python 3.12
source .venv/bin/activate
```

# 3. Install the Python dependencies that are not on PyPI

## 3.1 PyTorch (CUDA 13.0)
The official PyTorch wheel for CUDA 13.0 lives on the PyTorch custom index:
```bash
uv pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu130
``` 
The `cu130` suffix = CUDA 13.0.

## 3.2 Triton and XGrammar (required by vLLM)
```bash
uv pip install xgrammar triton
```

## 3.3 FlashInfer nightly builds
FlashInfer is the low‑level kernel library that vLLM uses for fast KV‑cache updates.
Because the DGX‑Spark CUDA version is newer than the most recent stable release, we pull the nightly wheels directly from the FlashInfer site.
```bash
# Core FlashInfer runtime (no extra deps)
uv pip install flashinfer-python \
    --prerelease=allow \
    --index-url https://flashinfer.ai/whl/nightly/ \
    --no-deps

# Pre‑compiled cubin files for the current CUDA version
uv pip install flashinfer-cubin \
    --index-url https://flashinfer.ai/whl/nightly/

# JIT cache helper (specific to cu130)
uv pip install flashinfer-jit-cache \
    --prerelease=allow \
    --index-url https://flashinfer.ai/whl/nightly/cu130
```

### Why --no-deps?
The nightly wheel already bundles its own Torch dependency, which would otherwise try to reinstall an older version and break the cu130 build.

# 4. Build vllm from source

## 4.1 Clone the repository
Get vllm sources.

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
```

## 4.2 Tell vLLM to reuse the Torch you already installed
The helper script `use_existing_torch.py` patches the requirements/*.txt files so that the build system does not download a different Torch wheel.
```bash
python use_existing_torch.py
```
## 4.3 Remove the (now‑installed) FlashInfer line

The `requirements/cuda.txt` file still contains a `flashinfer` entry that would try to pull the stable release from PyPI. We delete it with sed.
```bash
sed -i "/flashinfer/d" requirements/cuda.txt
```

## 4.4 Install the build‑time dependencies
```bash
uv pip install -r requirements/build.txt
```
## 4.5 Compile vLLM

The compile step can take about 60 minutes on a fresh DGX‑Spark node because it builds Triton kernels for every GPU architecture you expose.

```bash
# Export the architecture list that matches the Spark GPUs.
# 12.1a is the “ampere” compute capability used on Spark (12.1a == 12.1+)
export TORCH_CUDA_ARCH_LIST=12.1a

# Tell Triton where the CUDA PTXAS binary lives
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas

# Required for the token‑encoding submodule
export TIKTOKEN_ENCODINGS_BASE=$PWD/tiktoken_encodings

# Install vLLM in editable mode (no isolation so it can see the already‑installed Torch)
uv pip install --no-build-isolation -e . -v --pre

# Optional: install the audio extra (needed for Whisper, SpeechT5, …)
uv pip install --no-build-isolation -e .[audio] -v --pre
```

## 5. Download the token‑encoding files (GPT‑OSS models)
vLLM needs the tiktoken encoder files for the OpenAI‑compatible models.

```bash
cd ..
mkdir -p tiktoken_encodings
wget -O tiktoken_encodings/o200k_base.tiktoken "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken"
wget -O tiktoken_encodings/cl100k_base.tiktoken "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
```

# 6. Run a quick inference test
Create a file called `offline_inference.py` inside the vllm folder (or anywhere on your `$PYTHONPATH`).

```python
from vllm import LLM, SamplingParams

# Sample prompts.
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)


def main():
    # Create an LLM.
    llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3")
    # Generate texts from the prompts.
    # The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    outputs = llm.generate(prompts, sampling_params)
    # Print the outputs.
    print("\nGenerated Outputs:\n" + "-" * 60)
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt:    {prompt!r}")
        print(f"Output:    {generated_text!r}")
        print("-" * 60)


if __name__ == "__main__":
    main()

```
Activate the virtual environment `source .venv/bin/activate`
Run the script : `python vllm/offline_inference.py`
You should see:
[![Vllm output](mistral-vllm.png)](mistral-vllm.png)

# References
- vLLM thread on Nvidia forum : [https://forums.developer.nvidia.com/t/run-vllm-in-spark/348862/70](https://forums.developer.nvidia.com/t/run-vllm-in-spark/348862/70)
- full script, all commands in one file : [![Install script](install_vllm_script.txt)](install_vllm_script.txt)