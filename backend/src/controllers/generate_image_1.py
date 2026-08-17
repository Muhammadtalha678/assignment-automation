import os
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import json
import base64
import uuid
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
    if os.name == "nt":
    # # Background Chrome instances clear tracking
        try:
            os.system("taskkill /f /im chrome.exe")
            await asyncio.sleep(1)
        except:
            pass
         

    async with async_playwright() as playwright:
        auth_file = "auth_state.json"
        if os.path.exists(auth_file):
            print("Loading authentication state from cookies file...")
            browser = await playwright.chromium.launch(
                headless=True, # 3. FIXED: Must be True for Cloud
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(storage_state=auth_file)
        else:
            print("No auth_state.json found. Falling back to local Windows Profile...")
            user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")

            print("Launching natural browser context with Profile 4...")
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                channel="chrome",
                args=[
                    # f"--profile-directory=Profile 4", 
                    f"--profile-directory=Profile 1", 
                    "--no-first-run",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
        
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
       
        for (idx, question) in enumerate(questions, start=1):
                    prompt = question.get("diagram_prompt")
        
                    print("Google Gemini open ho raha hai...")
                    await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
                    await asyncio.sleep(6)
                   
                    # Export state dynamically if running locally so you can use it on the cloud later
                    if not os.path.exists(auth_file) and os.name == 'nt':
                       await context.storage_state(path=auth_file)
                       print("Generated auth_state.json! Upload this to your cloud service.")




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
