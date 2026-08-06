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
                "--no-first-run",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        for (idx,question) in enumerate(questions,start=1):
            prompt = question.get("diagram_prompt")

            print("Google AI Studio open ho raha hai...")
            await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
            await asyncio.sleep(6)

            print("Locating chat text field area...")
            chat_box = page.locator("div[contenteditable='true'], div[aria-label*='Prompt'],textarea").first
            await chat_box.click()
            await asyncio.sleep(1)

            print("Typing prompt string...")
            # Thoda sa delay badha rahe hain taaki human rhythm lage
            await page.keyboard.type(prompt, delay=35) 
            await asyncio.sleep(2)
        
            print("Submitting prompt query...")
            # submit button dhndo
            submit_btn = page.locator("button[aria-label*='Send'], button.send-button, mat-icon:has-text('send')").first
            if await submit_btn.count() > 0 and await submit_btn.is_visible():
                print("Visible Run button mil gaya! Simulating human mouse cursor move...")
                # Direct click karne ki jagah mouse ko button par hover karwayein (anti-bot bypass karne ke liye)
                await submit_btn.hover()
                await asyncio.sleep(1)
                # Human click behavior invoke karein
                await submit_btn.click()
            else:
                await page.keyboard.press("Enter")
            
            print("Generation initiated. Monitoring DOM execution layout (40 seconds wait)...")
            await asyncio.sleep(40)
            
            # Generated image target structure catch karna
            image_node = page.locator(
                "mat-card img[src*='googleusercontent'],"
                "div.conversation-container img[src*='googleusercontent'],"
                "img[alt*='Generated Image'],"
                "message-content img").last
            
            if await image_node.count() > 0:
                print("Successfully verified generated image element on canvas window!")
                file_path = os.path.abspath(os.path.join(output_dir, f"temp_{idx}.png"))
                
                # Direct target clear snapshot capture
                await page.locator("body").click(position={"x":5,"y":5})
                await asyncio.sleep(0.5)
                await image_node.screenshot(path=file_path)
                print(f"\n[SUCCESS] Original High-Res Asset Saved via Playwright: {file_path}")
                image_map[idx] = file_path
            else:
                print("\n[INFO] Saving broader chat canvas window layout...")
                file_path = os.path.abspath(os.path.join(output_dir, f"fallback_canvas_{idx}.png"))
                await page.screenshot(path=file_path)
                print(f"[SUCCESS] Viewport screen extracted to: {file_path}")
                
        await context.close()
        print(image_map)
        return image_map 
