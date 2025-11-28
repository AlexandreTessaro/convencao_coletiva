# Arquitetura do MVP

## 🏗️ Visão Geral da Arquitetura

A arquitetura do MVP segue um padrão de **microserviços simplificado** com separação clara entre frontend, backend e serviços de coleta de dados.

```
┌─────────────────┐
│   Frontend      │  (React/Next.js)
│   (Web App)     │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼─────────────────────────────────┐
│         Backend API                      │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │   REST API   │  │  WebSocket API  │  │
│  │  (Express/   │  │  (Notificações) │  │
│  │   FastAPI)   │  │                 │  │
│  └──────┬───────┘  └─────────────────┘  │
└─────────┼────────────────────────────────┘
          │
┌─────────▼────────────────────────────────┐
│      Banco de Dados                      │
│      PostgreSQL                          │
│  ┌──────────┐  ┌──────────────────┐    │
│  │  Dados   │  │  Full-Text       │    │
│  │  Relacionais│  │  Search (pg_trgm) │    │
│  └──────────┘  └──────────────────┘    │
└──────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────┐
│   Serviço de Coleta                      │
│   (Worker/Job Scheduler)                 │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │   Scraper    │  │  PDF Processor  │  │
│  │  (Puppeteer/ │  │  (PyPDF2/Tika)  │  │
│  │   Scrapy)    │  │  + OCR (Tesseract)│ │
│  └──────────────┘  └─────────────────┘  │
└──────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────┐
│   Armazenamento de Arquivos              │
│   (S3/MinIO ou Local Storage)            │
└──────────────────────────────────────────┘
```

---

## 📦 Módulos do Sistema

### 1. Módulo de Autenticação e Autorização

**Responsabilidades:**
- Gerenciar usuários e autenticação
- Controle de acesso baseado em roles
- Sessões e tokens JWT

**Tecnologias Sugeridas:**
- Backend: JWT para autenticação
- Frontend: Context API ou Redux para estado de autenticação

**Endpoints Principais:**
- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/auth/logout`
- `GET /api/auth/me`

---

### 2. Módulo de Gestão de Empresas

**Responsabilidades:**
- Cadastro e gerenciamento de empresas
- Associação de empresas a usuários
- Validação de CNPJ e CNAE

**Tecnologias Sugeridas:**
- Validação de CNPJ: Biblioteca específica da linguagem
- Validação de CNAE: Base de dados de códigos CNAE

**Endpoints Principais:**
- `GET /api/companies` - Listar empresas do usuário
- `POST /api/companies` - Cadastrar nova empresa
- `GET /api/companies/:id` - Detalhes da empresa
- `PUT /api/companies/:id` - Atualizar empresa
- `DELETE /api/companies/:id` - Remover empresa

**Modelo de Dados:**
```sql
companies (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  cnpj VARCHAR(14) UNIQUE NOT NULL,
  razao_social VARCHAR(255),
  cnae VARCHAR(7),
  municipio VARCHAR(100),
  uf VARCHAR(2),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

### 3. Módulo de Coleta de Dados (Scraper)

**Responsabilidades:**
- Monitorar o Mediador MTE
- Extrair IDs de instrumentos coletivos
- Baixar documentos (HTML, PDF)
- Extrair metadados (CNPJ, CNAE, município, sindicato)

**Tecnologias Sugeridas:**
- **Python**: Scrapy ou Selenium/Playwright para scraping
- **Node.js**: Puppeteer ou Playwright
- Rate limiting e retry logic
- User-Agent rotativo

**Componentes:**
- **Crawler**: Navega pelas páginas do Mediador
- **Parser**: Extrai dados das páginas HTML
- **Downloader**: Baixa PDFs e documentos
- **Metadata Extractor**: Extrai informações estruturadas

**Fluxo:**
1. Acessa página de busca do Mediador
2. Executa buscas por diferentes critérios (ou monitora novas publicações)
3. Extrai lista de IDs de instrumentos coletivos
4. Para cada ID, acessa página de detalhes
5. Extrai metadados e URL do documento
6. Baixa documento
7. Armazena no sistema

---

### 4. Módulo de Processamento de Documentos

**Responsabilidades:**
- Extrair texto de PDFs digitais
- OCR para PDFs escaneados
- Extrair texto de HTML
- Indexar conteúdo para busca

**Tecnologias Sugeridas:**
- **PDF Digital**: PyPDF2, pdfplumber (Python) ou pdf-parse (Node.js)
- **PDF Escaneado**: Tesseract OCR + pdf2image
- **HTML**: BeautifulSoup ou Cheerio
- **Indexação**: PostgreSQL Full-Text Search (pg_trgm) ou Elasticsearch

**Componentes:**
- **PDF Parser**: Extrai texto de PDFs digitais
- **OCR Engine**: Converte imagens em texto
- **Text Extractor**: Extrai texto de HTML
- **Indexer**: Indexa conteúdo para busca full-text

---

### 5. Módulo de Armazenamento de Convenções

**Responsabilidades:**
- Armazenar metadados das convenções
- Armazenar documentos originais
- Armazenar texto extraído
- Manter histórico de versões

**Tecnologias Sugeridas:**
- **Banco de Dados**: PostgreSQL
- **Armazenamento de Arquivos**: AWS S3, MinIO ou sistema de arquivos local

**Modelo de Dados:**
```sql
convencoes (
  id UUID PRIMARY KEY,
  instrumento_id VARCHAR(50) UNIQUE NOT NULL, -- ID do Mediador
  titulo VARCHAR(500),
  tipo VARCHAR(50), -- CCT, ACT, etc.
  data_publicacao DATE,
  data_vigencia_inicio DATE,
  data_vigencia_fim DATE,
  sindicato_empregador VARCHAR(255),
  sindicato_trabalhador VARCHAR(255),
  municipio VARCHAR(100),
  uf VARCHAR(2),
  cnae VARCHAR(7),
  documento_url TEXT, -- URL do documento original
  documento_path TEXT, -- Caminho do arquivo armazenado
  texto_extraido TEXT, -- Texto completo extraído
  formato_documento VARCHAR(20), -- HTML, PDF_DIGITAL, PDF_ESCANEADO
  status VARCHAR(20), -- PROCESSANDO, PROCESSADO, ERRO
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

convencoes_empresas (
  id UUID PRIMARY KEY,
  convencao_id UUID REFERENCES convencoes(id),
  company_id UUID REFERENCES companies(id),
  relevancia_score DECIMAL, -- Score de relevância
  created_at TIMESTAMP
)

convencoes_metadados (
  id UUID PRIMARY KEY,
  convencao_id UUID REFERENCES convencoes(id),
  chave VARCHAR(100),
  valor TEXT,
  created_at TIMESTAMP
)
```

---

### 6. Módulo de Busca

**Responsabilidades:**
- Busca por CNPJ, CNAE, município, sindicato
- Busca full-text por palavras-chave
- Filtros avançados
- Ranking de resultados

**Tecnologias Sugeridas:**
- PostgreSQL Full-Text Search (pg_trgm para similaridade)
- Índices GIN para busca rápida
- Elasticsearch (opcional, para escala futura)

**Endpoints Principais:**
- `GET /api/convencoes/search?q=...` - Busca geral
- `GET /api/convencoes/search?cnpj=...` - Busca por CNPJ
- `GET /api/convencoes/search?cnae=...` - Busca por CNAE
- `GET /api/convencoes/search?keyword=...` - Busca por palavra-chave
- `GET /api/convencoes/search?municipio=...` - Busca por município

**Índices Sugeridos:**
```sql
CREATE INDEX idx_convencoes_cnpj ON convencoes_metadados(convencao_id) WHERE chave = 'cnpj';
CREATE INDEX idx_convencoes_cnae ON convencoes(cnae);
CREATE INDEX idx_convencoes_municipio ON convencoes(municipio, uf);
CREATE INDEX idx_convencoes_texto ON convencoes USING gin(to_tsvector('portuguese', texto_extraido));
```

---

### 7. Módulo de Notificações

**Responsabilidades:**
- Identificar novas convenções aplicáveis
- Enviar notificações para usuários
- Gerenciar preferências de notificação
- Histórico de notificações

**Tecnologias Sugeridas:**
- **Email**: SendGrid, AWS SES ou SMTP
- **Push Notifications**: WebSockets ou Server-Sent Events
- **Queue**: Bull (Node.js) ou Celery (Python) para processamento assíncrono

**Componentes:**
- **Notification Service**: Lógica de envio de notificações
- **Matching Engine**: Identifica convenções aplicáveis
- **Preference Manager**: Gerencia preferências do usuário

**Endpoints Principais:**
- `GET /api/notifications` - Listar notificações
- `PUT /api/notifications/:id/read` - Marcar como lida
- `GET /api/notifications/preferences` - Obter preferências
- `PUT /api/notifications/preferences` - Atualizar preferências

**Modelo de Dados:**
```sql
notifications (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  convencao_id UUID REFERENCES convencoes(id),
  tipo VARCHAR(50), -- NOVA_CONVENCAO, ATUALIZACAO, etc.
  titulo VARCHAR(255),
  mensagem TEXT,
  lida BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
)

notification_preferences (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  email_enabled BOOLEAN DEFAULT TRUE,
  push_enabled BOOLEAN DEFAULT TRUE,
  frequencia VARCHAR(20), -- IMEDIATO, DIARIO, SEMANAL
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

### 8. Módulo de Dashboard

**Responsabilidades:**
- Exibir resumo de empresas e convenções
- Estatísticas e métricas
- Lista de convenções recentes
- Visualização de convenções

**Endpoints Principais:**
- `GET /api/dashboard/stats` - Estatísticas gerais
- `GET /api/dashboard/recent` - Convenções recentes
- `GET /api/dashboard/companies/:id` - Dashboard por empresa

---

### 9. Módulo de Comparação (Futuro)

**Responsabilidades:**
- Comparar duas ou mais convenções
- Destacar diferenças
- Gerar relatórios de comparação

**Tecnologias Sugeridas:**
- Difflib (Python) ou similar para comparação de texto
- Algoritmos de similaridade (Levenshtein, Jaccard)

---

## 🔄 Fluxo de Dados Principal

### Coleta de Dados
```
Mediador MTE → Scraper → Parser → Downloader → PDF Processor → Database
                                                      ↓
                                              File Storage
```

### Busca e Visualização
```
User → Frontend → API → Database → Full-Text Search → Results → Frontend
```

### Notificações
```
New Convention → Matching Engine → Notification Service → Email/Push → User
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

1. **users** - Usuários do sistema
2. **companies** - Empresas cadastradas
3. **convencoes** - Convenções coletivas
4. **convencoes_empresas** - Relação entre convenções e empresas
5. **convencoes_metadados** - Metadados adicionais
6. **notifications** - Notificações
7. **notification_preferences** - Preferências de notificação
8. **documentos** - Armazenamento de documentos (opcional, pode usar storage externo)

---

## 🔧 Stack Tecnológica Recomendada

### Backend
- **Linguagem**: Python (FastAPI) ou Node.js (Express/NestJS)
- **Banco de Dados**: PostgreSQL 14+
- **ORM**: SQLAlchemy (Python) ou Prisma/TypeORM (Node.js)
- **Queue**: Celery (Python) ou Bull (Node.js)
- **Cache**: Redis (opcional)

### Frontend
- **Framework**: React com Next.js ou Vue.js com Nuxt.js
- **Estado**: Redux Toolkit ou Zustand
- **UI**: Material-UI, Ant Design ou Tailwind CSS
- **Charts**: Chart.js ou Recharts

### Scraping
- **Python**: Scrapy + Selenium/Playwright
- **Node.js**: Puppeteer ou Playwright
- **Rate Limiting**: Respeitar delays entre requisições

### Processamento de Documentos
- **PDF**: PyPDF2, pdfplumber (Python) ou pdf-parse (Node.js)
- **OCR**: Tesseract OCR
- **HTML**: BeautifulSoup (Python) ou Cheerio (Node.js)

### Infraestrutura
- **Containerização**: Docker
- **Orquestração**: Docker Compose (MVP)
- **Storage**: MinIO (local) ou AWS S3 (produção)
- **Deploy**: Heroku, Railway, ou AWS

---

## 📊 Escalabilidade Futura

### Fase 1 (MVP)
- Monolito modular
- Banco único PostgreSQL
- Storage local ou S3 básico

### Fase 2 (Crescimento)
- Separação de serviços (API, Scraper, Processor)
- Cache Redis
- Elasticsearch para busca avançada
- CDN para documentos

### Fase 3 (Escala)
- Microserviços completos
- Load balancer
- Replicação de banco
- Processamento distribuído

