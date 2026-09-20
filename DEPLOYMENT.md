# Publicação híbrida: Vercel + backend próprio

O frontend pode continuar na Vercel e a API pode rodar em um computador ou servidor controlado pela loja. O navegador acessa a API pela variável `VITE_API_URL`.

## Frontend na Vercel

1. Importe o repositório no projeto existente da Vercel.
2. Mantenha o diretório raiz como a raiz deste repositório.
3. Adicione a variável de ambiente `VITE_API_URL` com a URL HTTPS pública da API, por exemplo `https://api.naitiaras.com.br`.
4. Faça um novo deploy. A variável é incorporada ao frontend durante o build.

Para desenvolvimento local, não defina `VITE_API_URL`: o Vite usa o proxy `/api` para `http://127.0.0.1:8000`.

## Backend

O backend não depende de pacotes externos:

```bash
cp backend/.env.example backend/.env
# edite as credenciais, origens e a chave Groq
set -a; . backend/.env; set +a
python3 backend/server.py
```

Use HTTPS na frente da API. Para um teste temporário, um túnel como Cloudflare Tunnel pode expor `http://127.0.0.1:8000`; para operação contínua, prefira um túnel nomeado ou um servidor com domínio próprio.

Exemplo de túnel temporário:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Depois, cadastre a URL HTTPS gerada em `NAI_ALLOWED_ORIGINS` e em `VITE_API_URL`, refaça o deploy da Vercel e reinicie o backend.

## Dados e segurança

- O SQLite é criado em `backend/naitiaras.db` e não deve ser versionado.
- Defina uma senha administrativa forte antes de expor a API.
- Use `NAI_COOKIE_SECURE=1` quando a API estiver acessível por HTTPS.
- Inclua no `NAI_ALLOWED_ORIGINS` somente os domínios do frontend autorizados.
- Faça backup do arquivo `backend/naitiaras.db` regularmente.
