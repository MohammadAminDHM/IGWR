from openai import OpenAI
from prompt_engineering.reflection import enhance_prompt
from prompt_engineering import system_prompts
from dotenv import load_dotenv
import os
import argparse
import requests
from datetime import datetime
from pathlib import Path
import sys
import json
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate images using DALL-E 3')
    parser.add_argument('--prompt', type=str, required=True, help='The prompt for image generation')
    parser.add_argument('--size', type=str, default='1024x1024', choices=['1024x1024', '1792x1024', '1024x1792'], 
                        help='Size of the generated image')
    parser.add_argument('--quality', type=str, default='standard', choices=['standard', 'hd'],
                        help='Quality of the generated image')
    parser.add_argument('--n', type=int, default=1, help='Number of images to generate (1-10)')
    parser.add_argument('--output-dir', type=str, default='generated_images',
                        help='Directory to save the generated images')
    parser.add_argument('--use-reflection', action='store_true',
                        help='Use reflection to improve the prompt')
    parser.add_argument('--show-improved-prompt', action='store_true',
                        help='Show the improved prompt before generating image')
    parser.add_argument('--model', type=str, default='gpt-4',
                        help='Model to use for prompt enhancement')
    parser.add_argument('--log-file', type=str, default='generation_logs.jsonl',
                        help='File to save generation logs')
    return parser.parse_args()

def save_log(log_data, log_file):
    """Save log entry to a JSONL file"""
    log_path = Path(log_file)
    
    # Create directory if it doesn't exist
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Append log entry
    with open(log_path, 'a', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False)
        f.write('\n')

def save_image(url, output_dir, index, prompt):
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename using timestamp and prompt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean prompt for filename (keep only alphanumeric and spaces, limit length)
    clean_prompt = "".join(c for c in prompt if c.isalnum() or c.isspace())[:30]
    filename = f"{timestamp}_{clean_prompt}_{index}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Download and save the image
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Image {index} saved to: {filepath}")
        return filepath
    else:
        print(f"Failed to download image {index}")
        return None

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["AVALAI_API_KEY", "BASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease make sure these variables are set in your .env file")
        sys.exit(1)

def main():
    # Load environment variables
    load_dotenv()
    
    # Check environment variables before proceeding
    check_environment()
    
    args = parse_arguments()
    start_time = time.time()
    
    # Initialize log data
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "original_prompt": args.prompt,
        "model": args.model,
        "size": args.size,
        "quality": args.quality,
        "n_images": args.n,
        "use_reflection": args.use_reflection,
        "generated_images": []
    }

    final_prompt = args.prompt

    if args.use_reflection:
        try:
            final_prompt = enhance_prompt(args.prompt,
                                        args.model,
                                        system_prompts.SYSTEM_PROMPT_IMAGE_1)
            log_data["improved_prompt"] = final_prompt
            
            if args.show_improved_prompt:
                print(f"Original prompt: {args.prompt}")
                print(f"Improved prompt: {final_prompt}")
        except Exception as e:
            print(f"Error during prompt enhancement: {str(e)}")
            print("Proceeding with original prompt...")
            final_prompt = args.prompt
            log_data["prompt_enhancement_error"] = str(e)

    try:
        client = OpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("AVALAI_API_KEY")
        )

        response = client.images.generate(
            model="dall-e-3",
            prompt=final_prompt,
            size=args.size,
            quality=args.quality,
            n=args.n
        )

        for i, image_data in enumerate(response.data):
            print(f"Image {i+1} URL: {image_data.url}")
            image_path = save_image(image_data.url,
                                  args.output_dir,
                                  i+1,
                                  final_prompt)
            
            if image_path:
                log_data["generated_images"].append({
                    "index": i + 1,
                    "url": image_data.url,
                    "local_path": str(image_path)
                })
                    
    except Exception as e:
        error_msg = str(e)
        print(f"Error during image generation: {error_msg}")
        log_data["generation_error"] = error_msg
        sys.exit(1)
    finally:
        # Add execution time
        log_data["execution_time_seconds"] = round(time.time() - start_time, 2)
        
        # Save log
        save_log(log_data, args.log_file)
        
        # Print summary
        print("\nGeneration Summary:")
        print(f"Time taken: {log_data['execution_time_seconds']} seconds")
        print(f"Original prompt: {args.prompt}")
        if args.use_reflection:
            print(f"Final prompt: {final_prompt}")
        print(f"Images generated: {len(log_data['generated_images'])}")
        print(f"Log saved to: {args.log_file}")

if __name__ == "__main__":
    main()