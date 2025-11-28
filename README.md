# ConvençãoColetiva - MVP

## 📋 Sobre o Projeto

Plataforma para busca, armazenamento e disponibilização de Convenções Coletivas de Trabalho (CCTs) para empresas e usuários.

## 🎯 Objetivo

Criar uma plataforma que permita:
- Buscar convenções coletivas automaticamente em fontes públicas (principalmente o Mediador MTE)
- Organizar, armazenar e exibir as convenções para os usuários
- Notificar empresas quando novas convenções forem publicadas

## 📚 Documentação

- [Visão do Produto](./docs/01-visao-produto.md) - Nome, descrição e proposta de valor
- [Personas e Casos de Uso](./docs/02-personas-casos-uso.md) - Perfis de usuários e principais fluxos
- [Arquitetura](./docs/03-arquitetura.md) - Arquitetura do MVP e módulos
- [Fluxo de Coleta](./docs/04-fluxo-coleta.md) - Processo de coleta e extração de dados
- [Riscos e Mitigação](./docs/05-riscos-mitigacao.md) - Análise de riscos e estratégias
- [Backlog](./docs/06-backlog.md) - Épicos e histórias de usuário
- [Prototipação](./docs/07-prototipacao.md) - Interface textual da aplicação

## 🚀 Tecnologias

- **Backend**: Python 3.9+ com FastAPI
- **Frontend**: Next.js 14 com React e TypeScript
- **Banco de Dados**: PostgreSQL 14+
- **Scraping**: Selenium/BeautifulSoup
- **Extração de PDF**: PyPDF2, pdfplumber, Tesseract OCR
- **Queue**: Celery com Redis
- **Autenticação**: JWT

## ⚖️ Requisitos Legais

- Validar legalidade do acesso ao Mediador MTE
- Verificar termos de uso
- Evitar scraping agressivo
- Manter dados públicos apenas
- Conformidade com LGPD

## 📁 Estrutura do Projeto

```
convencao_coletiva/
├── docs/              # Documentação do projeto
├── backend/           # Backend FastAPI
├── frontend/          # Frontend Next.js
├── docker-compose.yml # Configuração Docker
├── SETUP.md           # Guia de instalação
└── README.md          # Este arquivo
```

## 🚀 Início Rápido

1. **Setup inicial:**
   ```bash
   # Iniciar PostgreSQL e Redis
   docker-compose up -d
   
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Editar .env
   alembic upgrade head
   python run.py
   
   # Frontend (em outro terminal)
   cd frontend
   npm install
   cp .env.example .env
   # Editar .env
   npm run dev
   ```

2. **Acessar:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/api/docs

Consulte [SETUP.md](./SETUP.md) para instruções detalhadas.

