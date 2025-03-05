# IGWR (Image Generation With Reflection)

A powerful image generation tool that uses DALL-E 3 with prompt enhancement through LLM reflection to create high-quality, detailed images.

## Features

- **Prompt Enhancement**: Uses advanced LLMs (GPT-4.5, Claude, etc.) to improve image generation prompts
- **Multiple Model Support**: Compatible with various LLMs for prompt enhancement
- **High-Quality Image Generation**: Leverages DALL-E 3 for image creation
- **Flexible Output Options**: Customizable image size and quality settings
- **Local Image Saving**: Automatically saves generated images with meaningful filenames
- **Comprehensive Logging**: Tracks all generations with detailed metadata
- **Command-Line Interface**: Easy-to-use CLI with multiple configuration options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/IGWR.git
cd IGWR
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
AVALAI_API_KEY=your_api_key_here
BASE_URL=your_base_url_here
```

## Usage

Basic usage:
```bash
python image_generation.py --prompt "your prompt here"
```

Advanced usage:
```bash
python image_generation.py \
    --prompt "your prompt here" \
    --size 1792x1024 \
    --quality hd \
    --n 2 \
    --use-reflection \
    --show-improved-prompt \
    --model gpt-4 \
    --output-dir "my_images" \
    --log-file "my_logs.jsonl"
```

### Command Line Arguments

- `--prompt`: The image generation prompt (required)
- `--size`: Image size (1024x1024, 1792x1024, 1024x1792)
- `--quality`: Image quality (standard, hd)
- `--n`: Number of images to generate (1-10)
- `--output-dir`: Directory to save generated images
- `--use-reflection`: Enable prompt enhancement
- `--show-improved-prompt`: Display the enhanced prompt
- `--model`: LLM model for prompt enhancement
- `--log-file`: File to save generation logs

## Example Results

Here are some example results showing the effectiveness of prompt enhancement:

**Original Prompt:**
```
First-person view of a mythical French world—enchanted castles, floating gardens, and mystical creatures, blending fantasy with French folklore.
```

**GPT 4.5 Preview(model_name = gpt-4.5-preview)**
![Mythical French World](generated_images\gpt-4.5-preview.png)

**GPT 4.5 Preview(model_name = gpt-4.5-preview-2025-02-27)**
![Mythical French World](generated_images\gpt-4.5-preview-2025-02-27.png)

**Claude 3.7 Sonnet(model_name = anthropic.claude-3-7-sonnet-20250219-v1:0)**
![Mythical French World](generated_images\anthropic.claude-3-7-sonnet-20250219-v1.png)

**Claude 3.7 Sonnet(model_name = anthropic.claude-3-5-sonnet-20241022-v2:0)**
![Mythical French World](generated_images\anthropic.claude-3-5-sonnet-20241022-v2.png)

**Llama 3.3 70B(model_name = meta.llama3-3-70b-instruct-v1)**
![Mythical French World](generated_images\meta.llama3-3-70b-instruct-v1.png)

**Mistral Large(model_name = mistral.mistral-large-2407-v1)**
![Mythical French World](generated_images\mistral.mistral-large-2407-v1.png)


## Logging

The tool maintains detailed logs of all generations in JSONL format, including:
- Timestamp
- Original and enhanced prompts
- Model used
- Generation parameters
- Execution time
- Image URLs and local paths
- Any errors encountered

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

