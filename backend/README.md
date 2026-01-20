# obsig-backend

**⚠️ seguridad ante todo**  
este backend **no guarda credenciales, contraseñas ni cookies de los usuarios**.  
el `sessId` solo se usa temporalmente **para realizar la consulta a instagram** en nombre del usuario.  
no se almacena en archivos, bases de datos ni logs.  
el servidor **solo guarda imágenes de perfil públicas** en cache para optimizar la carga.  
ningún dato privado del usuario se conserva ni se reenvía.

---

api en **fastapi + aiohttp** para consultar seguidores / seguidos de instagram, calcular quién te sigue y quién no, y servir imágenes cacheadas.

---

## features

- endpoint `/consulta` para obtener:
  - cantidad de mutuals y no mutuals
  - listas completas de cada grupo
- endpoint `/imagen` para servir fotos de perfil desde cache
- descarga y cache local de imágenes en `cache_images/`
- cors abierto (`allow_origins=["*"]`) para conexión directa desde cualquier frontend
- compatible con windows / linux (usa `asyncio.WindowsSelectorEventLoopPolicy()` si es win)
- usa sessionid de instagram (`sessId`) para consultas autenticadas
- **no guarda ni registra ninguna información sensible**

---

## instalación local

requisitos:

- python 3.10+
- pip
- cuenta de instagram válida (para el sessionid)

```bash
git clone https://github.com/tuusuario/insta-consulta-backend.git
cd insta-consulta-backend
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en windows
pip install -r requirements.txt
```

si no tenés `requirements.txt`, crealo con:

```bash
fastapi
uvicorn
aiohttp
aiofiles
python-dotenv
```

---

## variables de entorno

crear un archivo `.env` en la raíz con:

```
OBSIGE_SESS=tu_sessionid_por_defecto
```

> este `sessId` sirve solo como valor por defecto si no se pasa en la query.  
> no se guarda ni se usa fuera del proceso de consulta.

---

## uso

### iniciar el servidor

```bash
python main.py
```

o con uvicorn directamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

el backend quedará corriendo en `http://localhost:8000`

---

## endpoints

### `/consulta`

**parámetros:**

- `user`: nombre de usuario de instagram (ej: `pgbito`)
- `sessId`: opcional, sessionid válido (si no, usa `OBSIGE_SESS` del .env)

**ejemplo:**

```
GET /consulta?user=pgbito&sessId=abcd1234...
```

**respuesta:**

```json
{
  "user": "pgbito",
  "stats": {
    "mutual_count": 10,
    "nomutual_count": 5
  },
  "mutuals": {
    "usuario1": { "id": "1", "pfp": "...", "username": "usuario1" }
  },
  "nomutuals": {
    "usuario2": { "id": "2", "pfp": "...", "username": "usuario2" }
  }
}
```

---

### `/imagen`

devuelve la imagen cacheada para un `userId`.

**ejemplo:**

```
GET /imagen?uid=123456
```

responde con la imagen jpeg si existe, o `404` si no está.

---

## cómo obtener el `sessId`

1. iniciá sesión en [instagram.com](https://www.instagram.com)
2. instalá la extensión **CookieEditor**
3. abríla mientras estás en instagram
4. buscá la cookie llamada `sessionid`
5. copiá su valor (será algo como `abcd1234efgh...`)
6. podés usarlo directamente en la query `sessId` o colocarlo en el `.env`

> nota: el sessionid expira después de algunas peticiones; si `/consulta` devuelve 404, el sessId está vencido.

---

## estructura del proyecto

```
main.py               # backend principal
cache_images/         # carpeta donde se guardan las fotos
.env                  # contiene OBSIGE_SESS (default sessionid)
```

---

## deploy rápido

### con uvicorn + systemd (linux)

```bash
pip install fastapi uvicorn aiohttp aiofiles python-dotenv
uvicorn main:app --host 0.0.0.0 --port 8000
```

### o docker (opcional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn aiohttp aiofiles python-dotenv
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## conexión con el frontend

el frontend (hecho en nextjs + shadcn/ui) consulta:

```
https://tu-dominio.com/consulta?user=USUARIO&sessId=SESSIONID
https://tu-dominio.com/imagen?userId=ID
```

asegurate de que el dominio del frontend esté autorizado en `allow_origins` del cors si restringís el acceso.

---

## licencia

open source • libre  
hecho con 💖 por **pgbito**
