import sys
import asyncio

# ESTO SIEMPRE PRIMERO PARA WINDOWS
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import json
import os
import aiohttp
import aiofiles
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import FileResponse  
from contextlib import asynccontextmanager
import dotenv
# --- CONFIGURACIÓN ---
CACHE_DIR = "cache_images"

os.makedirs(CACHE_DIR, exist_ok=True)

 

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" significa: "Deja entrar a todo el mundo"
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)
# --- UTILIDADES DE RED --- 

async def fetch(url, session, params=None):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        return {"error": response.status}

async def download_and_cache_image(uid: str, url: str, session: aiohttp.ClientSession):
    filepath = os.path.join(CACHE_DIR, f"{uid}.jpg")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return True # Cache hit

    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(filepath, mode='wb') as f:
                    await f.write(await resp.read())
                return True
    except Exception:
        pass
    return False

async def ig_request_paginated(user_id, target, session):
    is_followers = (target == "followers")
    hash_id = "c76146de99bb02f6415203be841dd25a" if is_followers else "d04b0a864b4b54837c0d870b0e77e076"
    edge_key = "edge_followed_by" if is_followers else "edge_follow"
    
    variables = {"id": user_id, "first": 50}
    params = {"query_hash": hash_id}
    
    collected_users = {}
    has_next = True
    
    while has_next:
        params["variables"] = json.dumps(variables)
        try:
            data = await fetch("https://www.instagram.com/graphql/query/", session, params=params)
            if "error" in data: break
            
            user_data = data.get("data", {}).get("user", {}).get(edge_key, {})
            edges = user_data.get("edges", [])
            
            for node in edges:
                n = node["node"]
                collected_users[n["username"]] = {
                    "id": n["id"],
                    "pfp": n["profile_pic_url"],
                    "username": n["username"]
                }
            
            page_info = user_data.get("page_info", {})
            if page_info.get("has_next_page"):
                variables["after"] = page_info["end_cursor"]
            else:
                has_next = False
        except Exception as e:
            print(f"Error scraping: {e}")
            break
            
    return collected_users

async def get_user_id(username, session:aiohttp.ClientSession):
    headers = {'X-IG-App-ID': '936619743392459'}
    try:
        async with session.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/', 
            params={'username': username}, 
            headers=headers
        ) as api:
            if api.status != 200:
                 return await api.text()
            data = await api.json()
            return data.get("data", {}).get("user", {}).get("id")
    except:
        return None

# --- ENDPOINTS ---

@app.get("/consulta")
async def consulta_usuario(user: str = Query(..., description="usuario de instagram"),
                           sessId: str = Query(
                               
                               os.getenv("OBSIGE_SESS"), description="usuario de instagram")):
      # Crear sesión única
    timeout = aiohttp.ClientTimeout(total=60)
    http_session = aiohttp.ClientSession(timeout=timeout,cookies={"sessionid":sessId})
    if not http_session:
        raise HTTPException(status_code=500, detail="Servidor no inicializado correctamente")
    
    uid = await get_user_id(user, http_session)
    if not uid:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    task_followers = ig_request_paginated(uid,"followers", http_session)
    task_following = ig_request_paginated(uid, "following", http_session)
    
    followers_dict, following_dict = await asyncio.gather(task_followers, task_following)
    
    # Calcular conjuntos
    set_followers = set(followers_dict.keys())
    set_following = set(following_dict.keys())
    
    mutual_keys = set_followers & set_following
    nomutual_keys = set_following - set_followers
    
    mutuals = {k: followers_dict[k] for k in mutual_keys}
    nomutuals = {k: following_dict[k] for k in nomutual_keys}
    
    # Descargar imágenes
    all_users = list(mutuals.values()) + list(nomutuals.values())
    sem = asyncio.Semaphore(50)
    
    async def bounded_download(u):
        async with sem:
            await download_and_cache_image(u["id"], u["pfp"], http_session)

    await asyncio.gather(*[bounded_download(u) for u in all_users])
    await http_session.close()
    return {
        "user": user,
        "stats": {"mutual_count": len(mutuals), "nomutual_count": len(nomutuals)},
        "mutuals": mutuals,
        "nomutuals": nomutuals
    }

@app.get("/imagen")
async def get_imagen(uid: str):
    filepath = os.path.join(CACHE_DIR, f"{uid}.jpg")
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})
    return Response(content="no encontrada", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)