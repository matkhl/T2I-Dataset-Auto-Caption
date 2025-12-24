import os
import yaml
import ollama
from PIL import Image
from tqdm import tqdm
import re

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def clean_filename(filename, prefixes):
    name = os.path.splitext(filename)[0]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    # Replace underscores and hyphens with spaces for better readability by LLM
    return name.replace("_", " ").replace("-", " ")

def generate_caption(client, model_name, image_path, filename_hint, config):
    # Construct the prompt
    system_instruction = config['prompts']['system_instruction']
    
    user_message = "Describe this image."
    
    if filename_hint:
        user_message += f"\nContext info: The file is named '{filename_hint}'. Use this context to identify the object if it is ambiguous, but describe what you see visually."

    # Strict enforcement prompt appended to ensure clean output
    enforcement_prompt = "\nIMPORTANT: Output ONLY the raw caption text. Do not add conversational filler like 'Here is the description'."

    final_prompt = f"{user_message} {enforcement_prompt}"

    try:
        response = client.chat(
            model=model_name,
            messages=[
                {
                    'role': 'system',
                    'content': system_instruction
                },
                {
                    'role': 'user',
                    'content': final_prompt,
                    'images': [image_path]
                }
            ],
            options=config['ollama'].get('options', {})
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"\nError processing {image_path}: {e}")
        return None

def main():
    # Load Config
    if not os.path.exists("config.yaml"):
        print("Error: config.yaml not found.")
        return
    
    conf = load_config()
    
    # Setup Paths
    input_dir = conf['paths']['input_folder']
    output_dir = conf['paths']['output_folder']
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup Ollama Client
    client = ollama.Client(host=conf['ollama']['host'])
    
    # Get Images
    valid_exts = tuple(conf['paths']['valid_extensions'])
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_exts)]
    
    print(f"Found {len(images)} images in '{input_dir}'. Starting captioning with model '{conf['ollama']['model']}'...")

    # Processing Loop
    for image_file in tqdm(images, desc="Captioning"):
        input_path = os.path.join(input_dir, image_file)
        
        # Determine output filename (replace image ext with .txt)
        base_name = os.path.splitext(image_file)[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")
        
        # Check context settings
        filename_context = None
        if conf['processing']['use_filename_context']:
            prefixes = conf['processing'].get('filename_strip_prefixes', [])
            filename_context = clean_filename(image_file, prefixes)

        # Generate Caption via LLM
        generated_caption = generate_caption(
            client, 
            conf['ollama']['model'], 
            input_path, 
            filename_context, 
            conf
        )

        if generated_caption:
            # Post-processing: Add trigger word
            trigger = conf['processing']['trigger_word']
            
            final_caption = generated_caption
            
            # Ensure no trailing periods if we are just appending raw text, 
            # though usually standardizing on "Trigger, Caption." is best.
            if trigger:
                final_caption = f"{trigger}, {generated_caption}"
            
            # Write to file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_caption)

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()