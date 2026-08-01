# Imagens do site

Coloque os arquivos reais nesta pasta (`public/assets/`) com exatamente estes nomes —
o código já está referenciando esses caminhos:

| Arquivo esperado | Onde é usado | Sugestão de conteúdo |
|---|---|---|
| `logo.png` | Header e Footer | A logo "Nai Tiaras & Laços" que você enviou ✅ já adicionada |
| `produto-1.jpeg` | Seção Produtos (card 1) | Foto das faixinhas coloridas com laço de crochê ✅ já adicionada |
| `produto-2.jpeg` | Seção Produtos (card 2) | Foto do kit de laços vermelho/laranja ✅ já adicionada |
| `produto-3.jpeg` | Seção Produtos (card 3) | Foto do kit de laços azul/pink tie-dye ✅ já adicionada |
| `produto-4.jpeg` | Seção Produtos (card 4) e também usada em Sobre Nós (temporário) | Foto da tiara de corações e borboleta ✅ já adicionada |
| `produto-5.jpeg` | Seção Produtos (card 5) | ⚠️ ainda não enviada — foto do laço duplo de renda branca |
| `produto-6.jpeg` | Seção Produtos (card 6) | ⚠️ ainda não enviada — foto da tiara com flor bordada |
| `sobre.jpg` | Seção Sobre Nós | ⚠️ ainda não enviada — adicione uma foto de contexto (ateliê, produção etc.) e troque o caminho em `About.jsx` de volta para `/assets/sobre.jpg` |

> Atenção: os nomes de arquivo (extensão inclusive) precisam bater exatamente com o que está no código.
> Se salvar como `.jpeg` mas o código apontar para `.jpg` (ou vice-versa), a imagem não aparece.

Até você adicionar os arquivos reais, o site funciona normalmente — só aparecem
ícones de imagem quebrada nesses espaços. Basta arrastar as fotos para esta pasta
com os nomes acima que elas aparecem automaticamente, sem precisar mexer no código.

Se preferir usar outros nomes de arquivo, ajuste os caminhos em:
- `src/data/content.js` (produtos)
- `src/components/Header.jsx`, `src/components/Footer.jsx` (logo)
- `src/components/About.jsx` (imagem da seção Sobre Nós)
