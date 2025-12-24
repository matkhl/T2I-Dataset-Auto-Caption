# T2I Dataset Auto-Caption

A lightweight, configurable Python utility to automatically caption image datasets using local Multimodal LLMs (via [Ollama](https://ollama.com/)). 

Designed for **LoRA/Fine-tuning workflows**, this tool runs locally on your hardware (privacy-focused) and leverages image filenames to provide context, ensuring accurate and consistent captions for specific domains like game assets, pixel art, or specialized textures.

## ✨ Features

* **Local Inference:** Runs entirely offline using Ollama (no API costs, total privacy).
* **Context-Aware:** Feeds cleaned filenames to the LLM to help identify ambiguous objects (e.g., distinguishing specific game items based on file names).
* **Highly Configurable:** Control prompts, model parameters, and output paths via a simple YAML file.
* **Trigger Word Support:** Automatically prepend trigger words (e.g., `factorio icon`) to all captions.
* **Vision Model Support:** Compatible with any vision-capable model on Ollama (e.g., `llama3.2-vision`, `llava`, `minicpm-v`).

## 🛠️ Prerequisites

* **Python 3.10+**
* **[Ollama](https://ollama.com/)** installed and running.
* **Hardware:** NVIDIA GPU (RTX 3060+ recommended) for reasonable inference speeds.

## 🚀 Quick Start

### 1. Installation

Clone the repository and set up a virtual environment:

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Model Setup

Pull a vision-capable model using Ollama.

```bash
# Recommended for balance of speed/accuracy:
ollama pull llama3.2-vision
```

*Note: Ensure the model you choose supports image inputs (vision).*

### 3. Configuration

Create a `config.yaml` file in the root directory. You can copy the example below and adjust it to your needs.

#### Example: Game Asset Captioning

This configuration is optimized for a dataset of Factorio icons where files are named like `conv_advanced-circuit.png`.

```yaml
ollama:
  host: "http://localhost:11434"
  model: "llama3.2-vision"  # Must match the model you pulled
  options:
    temperature: 0.2        # Low temperature = more factual/consistent

paths:
  input_folder: "input"
  output_folder: "output"
  valid_extensions: [".png", ".jpg", ".jpeg", ".webp"]

processing:
  trigger_word: "factorio icon"  # Prepended to every caption
  use_filename_context: true     # Helps the LLM identify the object
  filename_strip_prefixes:       # Clean filenames before sending to LLM
    - "conv_"                    # "conv_accumulator" -> "accumulator"

prompts:
  system_instruction: >
    Describe the main object in the image clearly and concisely.
    Focus on visual details like colors, shapes, and materials.
    Do not use flowery language.
```

### 4. Usage

Place your images in the `input/` folder and run:

```bash
python auto_caption.py
```

The tool will generate corresponding `.txt` files in the `output/` folder.

---

## 📂 Directory Structure

```text
.
├── input/               # Drop your source images here
├── output/              # Generated text files appear here
├── auto_caption.py      # Main script
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md
```

## 🔧 Troubleshooting

* **`ConnectionRefusedError`**: Ensure Ollama is running in the background (`ollama serve`).
* **`Response Error`**: Verify the `model` key in `config.yaml` matches the output of `ollama list`.
* **Performance**: Vision models are heavy. If inference is slow, check your GPU usage.

## 📜 License

[MIT](https://www.google.com/search?q=LICENSE)