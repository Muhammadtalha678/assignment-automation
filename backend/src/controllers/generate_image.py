import requests
import urllib.parse

def generate_image(image_desc: str, save_path: str) -> bool:
    try:
        # Prompt Optimization: Unnecessary text/clutter ko avoid karne ke liye keywords add kiye gaye hain
        clean_desc = image_desc.replace("\n", " ").strip()
        enhanced_prompt = (
            f"Minimalist technical diagram, sharp 2d vector infographic illustrating: {clean_desc}. "
            f"Clean layout, bold geometric shapes, clear flowchart boxes, white background, high resolution 4k, professional UI diagram style, no unreadable small text"
        )
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # High resolution endpoint (1280x720 aspect ratio for crisp Word insert)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed=42"
        
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Image generation failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error generating image for prompt '{image_desc}': {e}")
        return False