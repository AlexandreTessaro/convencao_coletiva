# Como Coletar Dados de Convenções do Mediador MTE

Este guia explica como coletar dados de convenções coletivas do site oficial do Ministério do Trabalho (Mediador MTE) e popular o banco de dados.

## 📋 Pré-requisitos

1. **Banco de dados configurado** - PostgreSQL rodando e migrações executadas
2. **Ambiente virtual ativado** - Com todas as dependências instaladas
3. **Arquivo `.env` configurado** - Com as variáveis necessárias

## 🚀 Métodos de Coleta

### Método 1: Via Script Python (Recomendado)

Execute o script diretamente no terminal:

```powershell
# No diretório backend
cd backend

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar coleta (sem limite)
python collect_convencoes.py

# Ou limitar a 10 convenções para teste
python collect_convencoes.py 10
```

Ou use o script PowerShell:

```powershell
# Coletar todas as convenções
.\collect_convencoes.ps1

# Coletar apenas 10 convenções
.\collect_convencoes.ps1 10
```

### Método 2: Via API Endpoint

Faça uma requisição POST para o endpoint:

```bash
# Com autenticação (substitua TOKEN pelo seu token JWT)
curl -X POST "http://localhost:8000/api/v1/collector/collect?limit=10" \
  -H "Authorization: Bearer TOKEN"
```

Ou via frontend/Postman:
- **URL**: `POST http://localhost:8000/api/v1/collector/collect`
- **Query Params**: `limit=10` (opcional)
- **Headers**: `Authorization: Bearer <seu_token>`

### Método 3: Via Celery (Coleta Automática)

Se você tiver Celery e Redis configurados:

```python
from app.tasks.collector import collect_convencoes_task

# Executar tarefa
result = collect_convencoes_task.delay()
```

## 🔧 Configuração do Scraper

O scraper está configurado em `backend/app/core/config.py` e usa as seguintes variáveis do `.env`:

```env
MEDIADOR_BASE_URL=https://mediador.trabalho.gov.br
SCRAPER_DELAY_SECONDS=3
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

## 📝 Como Funciona

1. **Extração de IDs**: O scraper tenta encontrar IDs de instrumentos coletivos usando múltiplas estratégias:
   - Busca em APIs JSON (se disponível)
   - Web scraping com Selenium (para conteúdo dinâmico)
   - Parsing HTML simples com BeautifulSoup

2. **Coleta de Metadados**: Para cada ID encontrado:
   - Acessa a página de detalhes
   - Extrai informações como título, datas, sindicatos, localização, CNAE
   - Tenta baixar o documento PDF/HTML

3. **Processamento de Documentos**: 
   - Extrai texto de PDFs digitais
   - Usa OCR para PDFs escaneados (requer Tesseract)
   - Processa documentos HTML

4. **Associação com Empresas**: 
   - Associa convenções às empresas cadastradas baseado em:
     - CNAE correspondente
     - Município e UF correspondentes

5. **Geração de Notificações**: 
   - Cria notificações para usuários cujas empresas são afetadas

## ⚠️ Observações Importantes

### Limitações do Site Oficial

O site do Mediador MTE pode ter:
- Proteção contra scraping (CAPTCHA, rate limiting)
- Estrutura HTML que muda frequentemente
- Requer autenticação em alguns casos
- Limites de requisições por IP

### Ajustes Necessários

Você pode precisar ajustar os seletores CSS em `backend/app/services/scraper.py` baseado na estrutura real do site:

```python
# Exemplo de ajuste de seletores
metadados = {
    'titulo': self._extract_text(soup, 'h1.titulo'),  # Ajustar seletor aqui
    # ...
}
```

### Verificação Manual

Antes de executar a coleta em massa, teste manualmente:

1. Acesse: https://mediador.trabalho.gov.br
2. Verifique a estrutura HTML da página
3. Ajuste os seletores no código se necessário
4. Teste com `limit=1` primeiro

## 🐛 Troubleshooting

### Erro: "No instrumento IDs found"
- Verifique se o site está acessível
- Ajuste os seletores CSS no código
- Verifique se precisa de autenticação

### Erro: "Selenium WebDriver not found"
- Instale o ChromeDriver: https://chromedriver.chromium.org/
- Ou instale via: `pip install webdriver-manager`

### Erro: "Tesseract not found" (para OCR)
- Instale Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- Configure o caminho no `.env`: `TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe`

### Dados incompletos
- Verifique os logs para ver quais campos falharam
- Ajuste os seletores CSS para campos específicos
- Alguns campos podem não estar disponíveis no site

## 📊 Monitoramento

Os logs mostram o progresso da coleta:

```
INFO: Starting convenções collection...
INFO: Found 50 instrumento IDs to process
INFO: Extracting metadata for 12345678...
INFO: Successfully processed 12345678
INFO: Collection complete. 10 new convenções added, 0 errors
```

## 🔄 Atualização Periódica

Para manter os dados atualizados, você pode:

1. **Agendar com Cron (Linux/Mac)**:
```bash
# Executar diariamente às 2h da manhã
0 2 * * * cd /path/to/backend && python collect_convencoes.py
```

2. **Agendar com Task Scheduler (Windows)**:
- Criar tarefa agendada que executa `collect_convencoes.ps1`

3. **Usar Celery Beat**:
```python
# Em celeryconfig.py
beat_schedule = {
    'collect-convencoes': {
        'task': 'collect_convencoes',
        'schedule': crontab(hour=2, minute=0),  # Diariamente às 2h
    },
}
```

## 📚 Referências

- Portal Mediador: https://mediador.trabalho.gov.br
- Documentação FastAPI: https://fastapi.tiangolo.com
- Documentação Selenium: https://selenium-python.readthedocs.io

