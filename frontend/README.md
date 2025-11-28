# Frontend - ConvençãoColetiva

## 🚀 Setup

### Pré-requisitos

- Node.js 18+
- npm ou yarn

### Instalação

1. **Instalar dependências:**
```bash
npm install
# ou
yarn install
```

2. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env
# Editar .env com a URL da API
```

3. **Executar em desenvolvimento:**
```bash
npm run dev
# ou
yarn dev
```

A aplicação estará disponível em `http://localhost:3000`

## 📋 Estrutura

```
frontend/
├── app/                    # Next.js App Router
│   ├── login/              # Página de login
│   ├── register/           # Página de registro
│   ├── dashboard/          # Dashboard principal
│   └── ...
├── components/             # Componentes reutilizáveis
├── lib/                    # Utilitários e configurações
├── store/                  # Estado global (Zustand)
└── public/                 # Arquivos estáticos
```

## 🛠️ Tecnologias

- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Zustand** - Gerenciamento de estado
- **React Hook Form** - Formulários
- **Axios** - Cliente HTTP
- **React Hot Toast** - Notificações

## 📱 Páginas Principais

- `/login` - Login
- `/register` - Cadastro
- `/dashboard` - Dashboard principal
- `/companies` - Lista de empresas
- `/companies/new` - Cadastrar empresa
- `/convencoes` - Lista de convenções
- `/convencoes/search` - Busca de convenções
- `/convencoes/[id]` - Detalhes da convenção
- `/notifications` - Notificações

## 🔐 Autenticação

O frontend usa JWT tokens armazenados no localStorage. O token é automaticamente incluído em todas as requisições à API.

## 🎨 Estilização

O projeto usa Tailwind CSS com classes customizadas definidas em `app/globals.css`.

