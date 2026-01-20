# obsige

app web (nextjs + shadcn/ui) hecho por pgbito, para ver quién te sigue y quién no en instagram.  
interfaz clean, tarjetas redondeadas y checklist para marcar mutuals / no mutuals.

---

**⚠️ seguridad y transparencia ante todo**

esta app **no guarda, almacena ni comparte credenciales de instagram**.  
el `sessId` que se usa proviene de tu propia sesión de instagram y **solo sirve para permitir que la app consulte tus listas de seguidores y seguidos**.  
no se almacena en servidores ni bases de datos, solo queda guardado en tu navegador (localStorage).

> ⚠️ **importante sobre el sessId:**
>
> - el `sessId` puede **vencer o dejar de funcionar** por varias razones:
>   - si el usuario a consultar tiene **demasiados seguidores o seguidos**, instagram puede limitar temporalmente las solicitudes.
>   - si hacés **muchas consultas seguidas** con el mismo `sessId`, instagram puede **ratelimitar o desactivar temporalmente tu sesión** por detectar actividad automatizada.
>   - los `sessId` expiran naturalmente después de unos días o si cerrás sesión en instagram.
> - un `sessId` **no da acceso a tus mensajes, publicaciones, ni datos privados**, solo permite obtener información pública del perfil (seguidores, seguidos y biografía).
> - la app **no ejecuta acciones en tu cuenta**, solo consulta información visible públicamente.

---

## features

- buscar usuario: consulta el servidor de Instagram para conseguir seguidores (si no pones sessid tu cuenta debe de ser publica)
- mostrar `mutuals` y `nomutuals`

- pantalla de configuración para guardar `sessId` (si no se pone, se usa el default del servidor)

---

---

## credenciales

### cómo obtener el `sessId` (mini tutorial con cookieeditor)

1. abrí chrome (o firefox) y entrá a instagram.com y logueate con tu cuenta.
2. instalá la extensión **CookieEditor** (o cualquier editor de cookies).
3. abrí la extensión mientras estás en `https://www.instagram.com`.
4. buscá la cookie llamada `sessionid`.
5. el valor de esa cookie es tu `sessId`. copiálo.
   - ejemplo: `abcd1234efgh...`
6. pegalo en la app: menú `configuración` -> campo `sessId` -> guardar.
7. ahora la app hará las consultas usando ese sessId (si tu endpoint lo requiere).

> nota de seguridad: no compartas tu `sessionid` públicamente.

---

## instalación (local)

requisitos: node >= 18, npm

```bash
git clone https://github.com/tuusuario/insta-consulta.git
cd insta-consulta
npm install
npm run dev
# abrir http://localhost:3000
```
