import base64
import uuid
import os
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
    


# def generate_google_image_sdk(api_key, idx, prompt):
#     # Client initialize karen
#     client = genai.Client(api_key=api_key)
    
#     # Image generate karne ki request
#     response = client.models.generate_content(
#         model="gemini-3.1-flash-image",
#         contents=prompt,
#         config=GenerateContentConfig(
#             response_modalities=[Modality.TEXT, Modality.IMAGE],
#         ),
#     )
    
#     # Diagram/Folder ka path check ya create karen
#     output_dir = "diagram"  # Aapka folder name
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Response se raw bytes nikal kar file mein save karen
#     for part in response.candidates[0].content.parts:
#         if part.inline_data:
#             # File ka mukammal path
#             file_path = os.path.join(output_dir, f"generated_image_{idx}.png")
            
#             # 'wb' (write binary) mode use karke bina PIL ke save karen
#             with open(file_path, "wb") as fp:
#                 fp.write(part.inline_data.data)
                
#             print(f"Image kamyabi se '{file_path}' mein save ho gayi hai!")




# import os
# import time
# from playwright.sync_api import sync_playwright

# def generate_image_via_web(prompt, idx):
#     output_dir = "diagram"
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Pehle se chalte hue kisi bhi background conflict ko khatam karne ke liye force kill command (Optional but safe)
#     try:
#         os.system("taskkill /f /im chrome.exe")
#         time.sleep(1)
#     except:
#         pass

#     with sync_playwright() as p:
#         print("Aapki Chrome Profile 4 ko directly automation ke sath open kiya ja raha hai...")
        
#         # Sahi user data path aur profile configuration
#         user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
        
#         try:
#             # Playwright khud aapki Profile 4 ke sath Chrome launch karega bina network ports ke pange ke
#             context = p.chromium.launch_persistent_context(
#                 user_data_dir=user_data_dir,
#                 headless=False,           # Browser aapko chalta hua dikhega
#                 channel="chrome",          # Aapka original installed Chrome hi chalega
#                 args=[
#                     "--profile-directory=Profile 4",  # Exact aapki target profile
#                     "--no-first-run"
#                 ]
#             )
#         except Exception as e:
#             print(f"\n[ERROR] Browser open nahi ho saka. Error detail: {e}")
#             print("Tip: Yaqeen banayein ke aapka normal Chrome browser mukammal band ho pehle.")
#             return

#         # Naya page open karna
#         page = context.new_page()
        
#         print("Google AI Studio open ho raha hai...")
#         page.goto("https://aistudio.google.com/prompts/new_chat", wait_until="networkidle")
#         time.sleep(5)  # Page load hone ka stable waqt
        
#         print("Prompt enter kiya ja raha hai...")
#         # AI Studio text area selector handle karna
#         textarea = page.locator("textarea, div[contenteditable='true']").first
#         textarea.click()
#         textarea.fill(prompt)
        
#         print("Run button par click ho raha hai...")
#         textarea.press("Enter")
        
#         print("Image generate ho rahi hai... 25 seconds intizar karen...")
#         time.sleep(25) 
        
#         print("Generated image ko 'diagram' folder mein save kiya ja raha hai...")
#         image_element = page.locator("ms-activity-output img, .image-output img, img[src*='blob']").first
        
#         if image_element.count() > 0:
#             file_path = os.path.abspath(os.path.join(output_dir, f"generated_image_{idx}.png"))
#             image_element.screenshot(path=file_path)
#             print(f"\n[SUCCESS] Image kamyabi se save ho gayi: {file_path}")
#         else:
#             print("\n[WARNING] Image element screen par nahi mila. Browser check karein ke image bani hai ya nahi.")
            
#         # Pura browser context clean tareeqe se close hoga
#         context.close()

# # --- Execution ---
# prompt = (
#     "A clean, minimal, 2D vector educational comparative infographic on a solid white background "
#     "illustrating key generational shifts in learners. Left Column labeled 'Previous Generations'; "
#     "Right Column labeled 'Current Generation'. Dark text, vibrant accent colors, high clarity."
# )

# generate_image_via_web(prompt, idx=1)
import os
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import json
async def generate_image_via_advanced_web(json_data_str:str):
    # print(prompt)
    if isinstance(json_data_str, str):
        data = json.loads(json_data_str)
    else:
        data = json_data_str

    output_dir = "diagrams"
    os.makedirs(output_dir, exist_ok=True)

    questions = data.get("questions",[])
    image_map = {}
    # # Background Chrome instances clear tracking
    try:
        os.system("taskkill /f /im chrome.exe")
        await asyncio.sleep(1)
    except:
        pass

    async with async_playwright() as playwright:
        user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
        
        print("Launching natural browser context with Profile 4...")
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="chrome",
            args=[
                f"--profile-directory=Profile 4", 
                # f"--profile-directory=Profile 1", 
                "--no-first-run",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        # for (idx,question) in enumerate(questions,start=1):
        #     prompt = question.get("diagram_prompt")

        #     print("Google AI Studio open ho raha hai...")
        #     await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
        #     await asyncio.sleep(6)

        #     print("Locating chat text field area...")
        #     chat_box = page.locator("div[contenteditable='true'], div[aria-label*='Prompt'],textarea").first
        #     await chat_box.click()
        #     await asyncio.sleep(1)

        #     # # OPTIONAL: Safe reset configuration for Temporary Chats if needed
        #     # # Uses force=True to bypass the aria-disabled restriction enforced by the UI
        #     # try:
        #     #     clear_btn = page.locator("button[aria-label*='New chat'], button[data-test-clear='outside']").first
        #     #     if await clear_btn.count() > 0:
        #     #         print("Forcing chat state refreshment...")
        #     #         await clear_btn.click(force=True)
        #     #         await asyncio.sleep(2)
        #     # except Exception as e:
        #     #     print(f"[INFO] Skipped interface clearing sequence: {e}")

        #     # print("Locating exact prompt field...")
        #     # prompt_box = page.locator("div[contenteditable='true'], text-area-element div, textarea").first
        #     # await prompt_box.scroll_into_view_if_needed()
        #     # await prompt_box.click()
        #     # await asyncio.sleep(1)
        
        #     print("Typing prompt string...")
        #     # Thoda sa delay badha rahe hain taaki human rhythm lage
        #     await page.keyboard.type(prompt, delay=35) 
        #     await asyncio.sleep(2)
        
        #     # print("Executing Run sequence (Simulating Human Action)...")
            
        #     # # 1. Sab se pehle exact 'Run' button dhoondhein
        #     # # Google AI Studio ka asli submit button aksar 'Run' text ya 'Ctrl+Enter' tooltip ke sath hota hai
        #     # run_button = page.locator("button:has-text('Run'), button[aria-label*='Run'], button:has-text('Ctrl')").first
        
        #     print("Submitting prompt query...")
        #     # submit button dhndo
        #     submit_btn = page.locator("button[aria-label*='Send'], button.send-button, mat-icon:has-text('send')").first
        #     if await submit_btn.count() > 0 and await submit_btn.is_visible():
        #         print("Visible Run button mil gaya! Simulating human mouse cursor move...")
        #         # Direct click karne ki jagah mouse ko button par hover karwayein (anti-bot bypass karne ke liye)
        #         await submit_btn.hover()
        #         await asyncio.sleep(1)
        #         # Human click behavior invoke karein
        #         await submit_btn.click()
        #     else:
        #         # print("Direct button control nahi mila. Executing Safe Sequential Keystrokes...")
        #         # Agar button na mile toh Ctrl+Enter ko achanak dabane ki jagah button states ke mutabiq chalayein
        #         # await page.keyboard.down("Control")
        #         # await asyncio.sleep(0.5)  # 500ms ka gap taaki bot behavior na lage
        #         await page.keyboard.press("Enter")
        #         # await asyncio.sleep(0.2)
        #         # await page.keyboard.up("Control")
            
        #     print("Generation initiated. Monitoring DOM execution layout (40 seconds wait)...")
        #     await asyncio.sleep(40)
            
        #     # Generated image target structure catch karna
        #     image_node = page.locator(
        #         "mat-card img[src*='googleusercontent'],"
        #         "div.conversation-container img[src*='googleusercontent'],"
        #         "img[alt*='Generated Image'],"
        #         "message-content img").last
            
        #     if await image_node.count() > 0:
        #         print("Successfully verified generated image element on canvas window!")
        #         file_path = os.path.abspath(os.path.join(output_dir, f"temp_{uuid.uuid4()}_{idx}.png"))
                
        #         # Direct target clear snapshot capture
        #         await page.locator("body").click(position={"x":5,"y":5})
        #         await asyncio.sleep(0.5)
        #         await image_node.screenshot(path=file_path)
        #         print(f"\n[SUCCESS] Original High-Res Asset Saved via Playwright: {file_path}")
        #         image_map[idx] = file_path
        #     else:
        #         print("\n[INFO] Saving broader chat canvas window layout...")
        #         file_path = os.path.abspath(os.path.join(output_dir, f"fallback_canvas_{uuid.uuid4()}_{idx}.png"))
        #         await page.screenshot(path=file_path)
        #         print(f"[SUCCESS] Viewport screen extracted to: {file_path}")
        #         image_map[idx] = file_path

        for (idx, question) in enumerate(questions, start=1):
                    prompt = question.get("diagram_prompt")
        
                    print("Google Gemini open ho raha hai...")
                    await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
                    await asyncio.sleep(6)
        
                    print("Locating chat text field area...")
                    chat_box = page.locator("div[contenteditable='true'], div[aria-label*='Prompt'],textarea").first
                    await chat_box.click()
                    await asyncio.sleep(1)
                
                    print("Typing prompt string...")
                    await page.keyboard.type(prompt, delay=35) 
                    await asyncio.sleep(2)
                
                    print("Submitting prompt query...")
                    submit_btn = page.locator("button[aria-label*='Send'], button.send-button, mat-icon:has-text('send')").first
                    if await submit_btn.count() > 0 and await submit_btn.is_visible():
                        print("Visible Run button mil gaya! Simulating human mouse cursor move...")
                        await submit_btn.hover()
                        await asyncio.sleep(1)
                        await submit_btn.click()
                    else:
                        await page.keyboard.press("Enter")
                    
                    print("Generation initiated. Monitoring DOM execution layout (40 seconds wait)...")
                    await asyncio.sleep(40)
                    
                    # Locate the generated high-res image component
                    image_node = page.locator(
                        "mat-card img[src*='googleusercontent'],"
                        "div.conversation-container img[src*='googleusercontent'],"
                        "img[alt*='Generated Image'],"
                        "message-content img"
                    ).last
                    
                    if await image_node.count() > 0:
                        print("Image element detected! Extracting HD raw bytes via canvas pipeline...")
                        
                        # Fetching element reference directly into browser context execution scope
                        element_handle = await image_node.element_handle()
                        
                        # Bypassing the 403 network barrier by pulling raw cross-origin binary definitions using JavaScript
                        base64_data = await page.evaluate("""
                            async (img) => {
                                return new Promise((resolve) => {
                                    if (!img.complete) {
                                        img.onload = () => convert();
                                    } else {
                                        convert();
                                    }
                                    function convert() {
                                        try {
                                            const canvas = document.createElement('canvas');
                                            canvas.width = img.naturalWidth;
                                            canvas.height = img.naturalHeight;
                                            const ctx = canvas.getContext('2d');
                                            ctx.drawImage(img, 0, 0);
                                            resolve(canvas.toDataURL('image/png'));
                                        } catch (e) {
                                            resolve(null);
                                        }
                                    }
                                });
                            }
                        """, element_handle)
        
                        if base64_data and "base64," in base64_data:
                            file_path = os.path.abspath(os.path.join(output_dir, f"hdimage_{uuid.uuid4()}_{idx}.png"))
                            try:
                                # Strip headers and parse the original binary stream cleanly
                                img_bytes = base64.b64decode(base64_data.split("base64,")[1])
                                with open(file_path, "wb") as img_file:
                                    img_file.write(img_bytes)
                                
                                print(f"[SUCCESS] High-Res Original HD Image Saved (No Borders/Perfect Zoom): {file_path}")
                                image_map[idx] = file_path
                                continue  # Skip screenshot step completely as file was correctly caught
                            except Exception as parse_error:
                                print(f"[WARNING] Local data parsing failed: {parse_error}")
        
                        # B-PLAN: Precise element isolation crop if base64 export fails
                        print("[INFO] Canvas retrieval failed. Running strict localized layout isolate screenshot...")
                        file_path = os.path.abspath(os.path.join(output_dir, f"temp_{uuid.uuid4()}_{idx}.png"))
                        await image_node.screenshot(path=file_path)
                        print(f"[SUCCESS] Isolate bounding screenshot saved: {file_path}")
                        image_map[idx] = file_path
                    else:
                        print("\n[INFO] Saving broader chat canvas window layout...")
                        file_path = os.path.abspath(os.path.join(output_dir, f"fallback_canvas_{uuid.uuid4()}_{idx}.png"))
                        await page.screenshot(path=file_path)
                        print(f"[SUCCESS] Viewport screen extracted to: {file_path}")
                        image_map[idx] = file_path
                        
                 
        await context.close()
        print(image_map)
        return image_map 
