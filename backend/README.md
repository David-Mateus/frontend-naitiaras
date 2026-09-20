# Backend da Nai Tiaras

O backend usa apenas Python 3 e SQLite. Ele pode rodar junto deste repositório ou em uma pasta irmã durante o desenvolvimento.

```bash
python3 backend/server.py
```

O frontend Vite deve ser executado em outro terminal:

```bash
cd frontend-naitiaras
npm run dev
```

Credenciais de desenvolvimento padrão:

- E-mail: `admin@naitiaras.com`
- Senha: `troque-esta-senha`

Antes de publicar, defina `NAI_ADMIN_EMAIL`, `NAI_ADMIN_PASSWORD`, `NAI_ALLOWED_ORIGINS` e `NAI_COOKIE_SECURE=1` no ambiente. Consulte `../DEPLOYMENT.md` para o cenário com frontend na Vercel e API hospedada separadamente.

## Chatbot com Groq

O site já possui um widget de atendimento conectado à rota `/api/chat`. Sem chave, ele usa respostas locais baseadas no catálogo e nas regras da loja. Para ativar respostas com IA, configure:

```bash
export GROQ_API_KEY="sua-chave-da-groq"
export GROQ_MODEL="llama-3.3-70b-versatile"
python3 backend/server.py
```

A chave fica somente no backend e nunca é enviada ao navegador.
