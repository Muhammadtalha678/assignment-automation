import json

from fastapi import APIRouter,Request,Depends,BackgroundTasks
from src.models.pydantic_model import data as ChatDataModal
from src.controllers.chat_controller import chat_controller
from src.lib.upload_image_dependency_funct import upload_images_and_get_chat_data
import time
router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(request:Request,backgroundTask:BackgroundTasks,chatData:ChatDataModal = Depends(upload_images_and_get_chat_data)):
    agent_config = request.app.state.agent_config
    # print(chatData)
    # ab hm yhn sy cookies ki file bnayn gy hr user ki uuid sy

    auth_filename = f"{chatData.user_uuid}_auth_state.json"
    cleaned_cookies = []

    if chatData.injected_cookies:
        now = int(time.time())

        for cookie in chatData.injected_cookies:
            name = str(cookie.get("name", "")).strip()
            value = cookie.get("value")

            if not name or value is None:
                continue

            raw_domain = str(cookie.get("domain", "")).strip()
            if not raw_domain:
                continue

            # Remove leading dots first
            host = raw_domain.lstrip(".")

            # ---------------------------------------------------------
            # __Host-* cookies have special RFC requirements:
            #   Secure = true
            #   Path = /
            #   Domain must be host-only (NO leading dot)
            # ---------------------------------------------------------
            is_host_cookie = name.startswith("__Host-")

            if is_host_cookie:
                domain = host
                path = "/"
                secure = True
            else:
                # Normal domain cookie
                domain = f".{host}"
                path = str(cookie.get("path") or "/").strip()

                secure = bool(cookie.get("secure", False))

            # ---------------------------------------------------------
            # SameSite
            # ---------------------------------------------------------
            same_site = str(
                cookie.get("sameSite", "Lax")
            ).strip().capitalize()

            if same_site not in {"Lax", "Strict", "None"}:
                same_site = "Lax"

            # SameSite=None requires Secure
            if same_site == "None":
                secure = True

            # __Host-* must also be Secure
            if is_host_cookie:
                secure = True

            # ---------------------------------------------------------
            # Expiry
            # ---------------------------------------------------------
            raw_expires = cookie.get("expires")

            try:
                if raw_expires is None:
                    expires = -1
                else:
                    expires = int(float(raw_expires))

                    # Chromium accepts -1 for session cookies.
                    # Don't arbitrarily rewrite valid future expiries.
                    if expires != -1 and expires <= now:
                        expires = -1

            except (ValueError, TypeError, OverflowError):
                expires = -1

            playwright_cookie = {
                "name": name,
                "value": str(value),
                "domain": domain,
                "path": path,
                "expires": expires,
                "httpOnly": bool(cookie.get("httpOnly", False)),
                "secure": secure,
                "sameSite": same_site,
            }

            cleaned_cookies.append(playwright_cookie)

    playwright_final_state = {
        "cookies": cleaned_cookies,
        "origins": [
            {
                "origin": "https://google.com",
                "localStorage": [
                    {
                        "name": "BARD_EMBED_CHAT_STORAGE_KEY_V2",
                        "value": "...",
                    },
                    {
                        "name": "brd_dctG",
                        "value": "true",
                    },
                    {
                        "name": "GqGm3b",
                        "value": "true",
                    },
                ],
            }
        ],
    }

    with open(auth_filename, "w", encoding="utf-8") as active_vault:
        json.dump(playwright_final_state, active_vault, indent=2)
    
     # 👈 File temporary write ho gayi!
    return await chat_controller(agent_config=agent_config,chat_data=chatData, backgroundTask=backgroundTask,cookies_path=auth_filename)
    # return "Cookies File Generate Successfully"
