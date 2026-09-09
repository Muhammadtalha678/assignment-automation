import os
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
async def save_login_state(auth_file:str):
    async with async_playwright() as playwright:
        # Hum ek temporary folder banayenge sirf login karne ke liye
        user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\ChromeTempLogin")
        
        # Google ko chakma dene ke liye stealth settings ke sath browser launch karein
        login_context  = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="chrome",
            # Yeh args robot hone ka nishan (navigator.webdriver) khatam kar dete hain
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run"
            ],
            # Fake user agent taake Google normal browser samjhe
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        login_page = await login_context.new_page()
        # await Stealth().apply_stealth_async(login_page)
        # Google Login page par jayen
        await login_page.goto("https://accounts.google.com")
        
        print("\n[🔑 ACTION REQUIRED]: Khule hue browser mein apna Google account login karein!")
        print("Aapke paas login aur 2FA karne ke liye 90 seconds hain...\n")
            
        
        # 90 seconds tak wait karein taake aap aaram se login kar sakein
        await login_page.wait_for_timeout(90000) 
        
        # Login hone ke baad aapka session save ho jayega
        await login_context.storage_state(path=auth_file)
        print("\n[SUCCESS]: Aapka login session 'auth_state.json' mein save ho gaya hai!\n")
        
        await login_context.close()

# # Run karein
# asyncio.run(save_login_state())














# import os
# import asyncio
# from playwright.async_api import async_playwright

# async def save_login_state():
#     async with async_playwright() as playwright:
#         # Hum ek temporary folder banayenge sirf login karne ke liye
#         user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\ChromeTempLogin")
        
#         # Google ko chakma dene ke liye stealth settings ke sath browser launch karein
#         context = await playwright.chromium.launch_persistent_context(
#             user_data_dir=user_data_dir,
#             headless=False,
#             channel="chrome",
#             # Yeh args robot hone ka nishan (navigator.webdriver) khatam kar dete hain
#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--no-first-run"
#             ],
#             # Fake user agent taake Google normal browser samjhe
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         )
        
#         page = await context.new_page()
        
#         # Google Login page par jayen
#         await page.goto("https://accounts.google.com")
        
#         print("\n[ALERT]: Ab bina error ke login page khulega. Jaldi se login aur 2FA karein!")
#         print("Aapke paas login karne ke liye 90 seconds hain...\n")
        
#         # 90 seconds tak wait karein taake aap aaram se login kar sakein
#         await page.wait_for_timeout(90000) 
        
#         # Login hone ke baad aapka session save ho jayega
#         await context.storage_state(path="auth_state.json")
#         print("\n[SUCCESS]: Aapka login session 'auth_state.json' mein save ho gaya hai!\n")
        
#         await context.close()

# Run karein
# asyncio.run(save_login_state())
