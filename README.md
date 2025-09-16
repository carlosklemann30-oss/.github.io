# Pirâmide Casas Pré-Fabricadas - Website

## 📋 Visão Geral

Este é o site institucional da [**Pirâmide Casas Pré-Fabricadas**](https://www.piramidecasa.com.br/), uma empresa especializada em construção de casas pré-fabricadas localizada em Joinville, Santa Catarina, com 15 anos de experiência no mercado do norte catarinense.

O projeto é um site estático responsivo, otimizado para performance, que apresenta os serviços da empresa, modelos de casas e informações de contato.

## 🚀 Tecnologias Utilizadas

- **HTML5** - Estrutura semântica e acessível
- **CSS3** - Estilização responsiva com design moderno
- **JavaScript** - Funcionalidades interativas e otimizações
- **Python 3.12** - Script de otimização de imagens
- **Docker & Docker Compose** - Containerização e ambiente de desenvolvimento
- **Nginx** - Servidor web para servir localmente e facilitar otimizações da página

## 📁 Estrutura do Projeto

```
piramidecasa-website/
├── index.html              # Página principal do site
├── style.css              # Estilos CSS principais
├── docker-compose.yml     # Configuração Docker Compose
├── Dockerfile            # Imagem Docker para otimização
├── nginx.conf           # Configuração do servidor Nginx
├── optimize_images.py   # Script Python para otimização de imagens
├── requirements.txt     # Dependências Python
├── CNAME               # Configuração de domínio personalizado
├── images/             # Imagens otimizadas
└── original_images/    # Imagens originais não processadas
```

### Funcionalidades Técnicas
- **Lazy Loading**: Carregamento sob demanda de imagens e vídeos
- **Critical CSS**: Estilos críticos inline para renderização rápida
- **Otimização de Imagens**: Múltiplos formatos (AVIF, WebP, JPEG) e resoluções

## 🛠️ Como Executar o Projeto

### Pré-requisitos para desenvolvimento local
- Docker e Docker Compose instalados
- Python 3.12+

### Método 1: Docker Compose (Recomendado)

```bash
# Clonar o repositório
git clone [URL_DO_REPOSITORIO]
cd piramidecasa-website

# Executar o servidor web
docker-compose up web

# Acessar o site em: http://localhost:3012
```

### Método 2: Servidor Local Simples

```bash
# Usando Python (desenvolvimento)
python -m http.server 8000

# Usando Node.js (se disponível)
npx serve .

# Acessar em: http://localhost:8000
```

## 🖼️ Sistema de Otimização de Imagens

O projeto inclui um sistema avançado de otimização de imagens que:

### Funcionalidades
- **Múltiplas Resoluções**: Gera breakpoints responsivos (sm, md, lg, xl, xxl)
- **Múltiplos Formatos**: AVIF, WebP e JPEG para máxima compatibilidade
- **Retina Ready**: Versões @2x para telas de alta densidade
- **Placeholders**: Base64 blur para melhor UX de carregamento
- **Qualidade Customizada**: Configurações específicas por imagem

### Como Usar

```bash
# Otimizar todas as imagens
docker-compose run optimizer

# Otimizar imagens específicas
docker-compose run optimizer original_images/hero-bg.jpg

# Executar localmente
python optimize_images.py original_images/
```

### Configuração de Qualidade

```python
# Em optimize_images.py
CUSTOM_IMAGES_QUALITY = {
    "local-joinville.jpg": {
        "jpeg": 80,
        "webp": 90,
        "avif": 90,  # Qualidade mais alta para imagem importante
    },
}
```

## 🌐 Deployment e Hospedagem

### GitHub Pages
O site está configurado para GitHub Pages com domínio personalizado:
- **Domínio**: www.piramidecasa.com.br
- **CNAME**: Configurado no arquivo `CNAME`
- **HTTPS**: Automaticamente habilitado

### Servidor Próprio com Docker

```bash
# Build da imagem
docker build -t piramidecasa-web .

# Executar em produção
docker run -d -p 80:80 piramidecasa-web
```

### Configuração Nginx
- **Gzip**: Compressão habilitada para todos os assets
- **Cache**: Headers de cache otimizados (1 hora)
- **Performance**: Configurações otimizadas para servir arquivos estáticos

## 📱 Responsividade e Performance

### Breakpoints
- **Mobile**: < 480px
- **Mobile Large**: 480px - 768px
- **Tablet**: 768px - 992px
- **Desktop**: 992px - 1200px
- **Large Desktop**: > 1200px

### Otimizações de Performance
- **Critical CSS**: Estilos essenciais inline no HTML
- **Async CSS**: Carregamento não-bloqueante do CSS principal
- **Image Optimization**: Múltiplos formatos e resoluções
- **Lazy Loading**: Imagens e vídeos carregados sob demanda
- **Minification**: Assets minificados para produção

## 🔧 Desenvolvimento e Manutenção

### Estrutura CSS
```css
/* CSS Crítico (inline no HTML) */
- Reset e base styles
- Header styles
- Hero section styles
- Mobile responsive básico

/* CSS Principal (style.css) */
- Seções específicas (about, models, etc.)
- Responsividade avançada
- Animações e transições
```

### Adicionando Novas Imagens

1. **Adicionar à pasta `original_images/`**
2. **Executar otimização**:
   ```bash
   docker-compose run optimizer

   # ou localmente se preferir
   python optimize_images.py
   ```
3. **Atualizar HTML** com as novas tags `<picture>`
4. **Testar responsividade** em diferentes dispositivos

### Modificando Conteúdo

1. **Textos**: Editar diretamente no `index.html`
2. **Estilos**: Modificar `style.css` ou CSS inline
3. **Imagens**: Seguir processo de otimização acima

**Desenvolvido com ❤️ para Pirâmide Casas Pré-Fabricadas**
*Construindo sonhos há 15 anos em Joinville, Santa Catarina*
