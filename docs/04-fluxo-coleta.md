# Fluxo de Coleta de Dados

## 🔍 Visão Geral

O processo de coleta de dados envolve monitorar o Mediador MTE, identificar novas convenções, extrair informações e armazenar no sistema.

---

## 📋 Processo Detalhado

### Etapa 1: Identificação de Novas Convenções

#### 1.1 Acesso ao Mediador MTE

**URL Base:** `https://mediador.trabalho.gov.br/` (exemplo - validar URL real)

**Estratégias de Busca:**

**Opção A: Monitoramento de Novas Publicações**
- Acessar página de "Últimas Publicações" ou similar
- Verificar periodicamente (ex: a cada 6 horas)
- Comparar com IDs já coletados no banco

**Opção B: Busca Sistemática**
- Executar buscas por diferentes critérios:
  - Por município (todos os municípios brasileiros)
  - Por CNAE (principais códigos CNAE)
  - Por período (últimos 30 dias, por exemplo)
- Combinar resultados e remover duplicatas

**Opção C: Busca por ID Incremental**
- Se IDs seguem padrão sequencial, tentar IDs incrementais
- Validar se ID existe antes de processar

#### 1.2 Extração do ID do Instrumento Coletivo

**Localização do ID:**
- Geralmente presente na URL: `/mediador/instrumento/{ID}`
- Ou em campo específico na página HTML
- Pode estar em formato numérico ou alfanumérico

**Exemplo de URL:**
```
https://mediador.trabalho.gov.br/instrumento/12345678
```

**Código de Exemplo (Python/Scrapy):**
```python
def parse_instrumento_id(self, response):
    # Extrair ID da URL
    url = response.url
    instrumento_id = url.split('/')[-1]
    
    # Ou extrair de campo específico na página
    instrumento_id = response.css('span#instrumento-id::text').get()
    
    return instrumento_id
```

---

### Etapa 2: Coleta de Metadados

#### 2.1 Acessar Página de Detalhes

Para cada ID identificado, acessar a página de detalhes da convenção.

**Estrutura Esperada da Página:**
- Título da convenção
- Data de publicação
- Período de vigência
- Sindicatos envolvidos (empregador e trabalhador)
- Município/UF
- CNAE relacionado
- Link para documento (HTML ou PDF)

#### 2.2 Extração de Metadados

**Campos a Extrair:**

| Campo | Localização | Exemplo |
|-------|-------------|---------|
| Título | `<h1>` ou campo específico | "CCT - Comércio Varejista" |
| Data Publicação | Campo de data | "15/03/2024" |
| Vigência Início | Campo de data | "01/04/2024" |
| Vigência Fim | Campo de data | "31/03/2025" |
| Sindicato Empregador | Campo específico | "Sindicato do Comércio" |
| Sindicato Trabalhador | Campo específico | "Sindicato dos Empregados" |
| Município | Campo de localização | "São Paulo" |
| UF | Campo de localização | "SP" |
| CNAE | Campo específico | "4711-3/00" |
| Link Documento | Link de download | URL do PDF/HTML |

**Código de Exemplo (Scrapy):**
```python
def parse_convencao_detalhes(self, response):
    convencao = {
        'instrumento_id': self.extract_instrumento_id(response),
        'titulo': response.css('h1.titulo::text').get(),
        'data_publicacao': self.parse_date(
            response.css('span.data-publicacao::text').get()
        ),
        'vigencia_inicio': self.parse_date(
            response.css('span.vigencia-inicio::text').get()
        ),
        'vigencia_fim': self.parse_date(
            response.css('span.vigencia-fim::text').get()
        ),
        'sindicato_empregador': response.css(
            'div.sindicato-empregador::text'
        ).get(),
        'sindicato_trabalhador': response.css(
            'div.sindicato-trabalhador::text'
        ).get(),
        'municipio': response.css('span.municipio::text').get(),
        'uf': response.css('span.uf::text').get(),
        'cnae': response.css('span.cnae::text').get(),
        'documento_url': response.css('a.download-documento::attr(href)').get(),
    }
    
    # Validar campos obrigatórios
    if convencao['instrumento_id'] and convencao['documento_url']:
        yield convencao
```

---

### Etapa 3: Download do Documento

#### 3.1 Identificar Tipo de Documento

**Tipos Possíveis:**
1. **HTML**: Página web com conteúdo da convenção
2. **PDF Digital**: PDF gerado digitalmente (texto selecionável)
3. **PDF Escaneado**: PDF de documento físico escaneado (imagem)

**Como Identificar:**
- Verificar extensão do arquivo (.html, .pdf)
- Para PDFs, tentar extrair texto:
  - Se sucesso → PDF Digital
  - Se falha → PDF Escaneado (precisa OCR)

#### 3.2 Download

**Estratégia:**
- Usar biblioteca HTTP (requests, axios) para download
- Salvar em storage temporário primeiro
- Validar integridade do arquivo
- Mover para storage permanente após processamento

**Código de Exemplo (Python):**
```python
import requests
from pathlib import Path

def download_documento(url, instrumento_id):
    """Baixa documento e retorna caminho local"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Determinar extensão
    content_type = response.headers.get('content-type', '')
    if 'pdf' in content_type:
        ext = '.pdf'
    elif 'html' in content_type:
        ext = '.html'
    else:
        ext = '.pdf'  # default
    
    # Salvar arquivo
    filename = f"{instrumento_id}{ext}"
    filepath = Path(f"/tmp/{filename}")
    filepath.write_bytes(response.content)
    
    return filepath, ext
```

---

### Etapa 4: Extração de Texto

#### 4.1 HTML

**Processo:**
- Usar BeautifulSoup ou Cheerio para parsear HTML
- Extrair conteúdo do body ou container principal
- Remover tags e manter apenas texto
- Limpar espaços em branco excessivos

**Código de Exemplo (Python):**
```python
from bs4 import BeautifulSoup

def extract_text_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remover scripts e styles
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Extrair texto
    text = soup.get_text()
    
    # Limpar espaços
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text
```

#### 4.2 PDF Digital

**Processo:**
- Usar biblioteca de extração de PDF (PyPDF2, pdfplumber)
- Extrair texto página por página
- Concatenar todo o texto
- Manter estrutura básica (quebras de linha)

**Código de Exemplo (Python):**
```python
import PyPDF2

def extract_text_from_pdf_digital(filepath):
    text = ""
    with open(filepath, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text
```

#### 4.3 PDF Escaneado (OCR)

**Processo:**
1. Converter PDF em imagens (uma por página)
2. Aplicar OCR em cada imagem usando Tesseract
3. Concatenar texto extraído
4. Pode ser lento para documentos grandes

**Código de Exemplo (Python):**
```python
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extract_text_from_pdf_escaneado(filepath):
    # Converter PDF em imagens
    images = convert_from_path(filepath, dpi=300)
    
    text = ""
    for image in images:
        # Aplicar OCR
        page_text = pytesseract.image_to_string(
            image, 
            lang='por'  # Português
        )
        text += page_text + "\n"
    
    return text
```

#### 4.4 Detecção Automática de Tipo

**Fluxo:**
```python
def extract_text_from_document(filepath, file_ext):
    if file_ext == '.html':
        return extract_text_from_html(filepath)
    
    elif file_ext == '.pdf':
        # Tentar extrair como PDF digital primeiro
        try:
            text = extract_text_from_pdf_digital(filepath)
            # Se extraiu pouco texto, pode ser escaneado
            if len(text.strip()) < 100:
                raise ValueError("Pouco texto extraído")
            return text
        except:
            # Tentar OCR
            return extract_text_from_pdf_escaneado(filepath)
    
    else:
        raise ValueError(f"Formato não suportado: {file_ext}")
```

---

### Etapa 5: Armazenamento

#### 5.1 Validação e Deduplicação

**Antes de armazenar:**
- Verificar se convenção já existe (por `instrumento_id`)
- Validar campos obrigatórios
- Normalizar dados (datas, CNPJ, CNAE)

**Código de Exemplo:**
```python
def validar_e_armazenar(convencao, texto_extraido):
    # Verificar se já existe
    existing = db.query(Convencao).filter_by(
        instrumento_id=convencao['instrumento_id']
    ).first()
    
    if existing:
        # Atualizar se necessário
        if existing.updated_at < convencao['data_publicacao']:
            update_convencao(existing, convencao, texto_extraido)
        return existing
    
    # Validar campos
    if not convencao.get('instrumento_id'):
        raise ValueError("ID do instrumento obrigatório")
    
    # Normalizar dados
    convencao['cnpj'] = normalizar_cnpj(convencao.get('cnpj'))
    convencao['cnae'] = normalizar_cnae(convencao.get('cnae'))
    
    # Criar registro
    nova_convencao = criar_convencao(convencao, texto_extraido)
    return nova_convencao
```

#### 5.2 Armazenamento no Banco

**Estrutura:**
1. Inserir registro na tabela `convencoes`
2. Armazenar documento original no storage
3. Armazenar texto extraído no banco (ou storage, dependendo do tamanho)
4. Criar índices para busca

**Código de Exemplo:**
```python
def criar_convencao(convencao_data, texto_extraido, documento_path):
    # Upload do documento para storage
    documento_url = upload_to_storage(documento_path)
    
    # Criar registro
    convencao = Convencao(
        instrumento_id=convencao_data['instrumento_id'],
        titulo=convencao_data['titulo'],
        data_publicacao=convencao_data['data_publicacao'],
        vigencia_inicio=convencao_data['vigencia_inicio'],
        vigencia_fim=convencao_data['vigencia_fim'],
        sindicato_empregador=convencao_data['sindicato_empregador'],
        sindicato_trabalhador=convencao_data['sindicato_trabalhador'],
        municipio=convencao_data['municipio'],
        uf=convencao_data['uf'],
        cnae=convencao_data['cnae'],
        documento_url=documento_url,
        documento_path=documento_path,
        texto_extraido=texto_extraido[:1000000],  # Limitar tamanho
        formato_documento=detectar_formato(documento_path),
        status='PROCESSADO'
    )
    
    db.session.add(convencao)
    db.session.commit()
    
    # Indexar para busca
    indexar_para_busca(convencao)
    
    return convencao
```

#### 5.3 Associação com Empresas

**Após armazenar convenção:**
- Buscar empresas cadastradas que podem ser afetadas
- Critérios de matching:
  - CNPJ exato
  - CNAE correspondente
  - Município correspondente
- Criar associações na tabela `convencoes_empresas`

**Código de Exemplo:**
```python
def associar_convencao_empresas(convencao):
    # Buscar empresas por CNAE
    empresas_cnae = db.query(Company).filter_by(
        cnae=convencao.cnae
    ).all()
    
    # Buscar empresas por município
    empresas_municipio = db.query(Company).filter_by(
        municipio=convencao.municipio,
        uf=convencao.uf
    ).all()
    
    # Combinar e remover duplicatas
    empresas = set(empresas_cnae + empresas_municipio)
    
    # Criar associações
    for empresa in empresas:
        score = calcular_relevancia(convencao, empresa)
        associacao = ConvencaoEmpresa(
            convencao_id=convencao.id,
            company_id=empresa.id,
            relevancia_score=score
        )
        db.session.add(associacao)
    
    db.session.commit()
    
    # Gerar notificações
    gerar_notificacoes(convencao, empresas)
```

---

## 🔄 Fluxo Completo (Diagrama)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Job Agendado (Cron/Scheduler)                           │
│    Executa a cada 6 horas                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Scraper: Acessa Mediador MTE                            │
│    - Busca novas publicações                                │
│    - Extrai lista de IDs de instrumentos                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Para cada ID novo:                                       │
│    - Acessa página de detalhes                              │
│    - Extrai metadados                                       │
│    - Baixa documento                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Processador de Documentos:                              │
│    - Identifica tipo (HTML/PDF Digital/PDF Escaneado)       │
│    - Extrai texto                                           │
│    - Aplica OCR se necessário                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Validação e Armazenamento:                               │
│    - Valida dados                                           │
│    - Verifica duplicatas                                    │
│    - Armazena no banco                                      │
│    - Upload para storage                                    │
│    - Indexa para busca                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Associação e Notificações:                               │
│    - Associa convenção a empresas relevantes               │
│    - Gera notificações para usuários                       │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuração e Agendamento

### Agendamento de Jobs

**Opções:**
- **Cron Job** (Linux/Mac)
- **Task Scheduler** (Windows)
- **Celery Beat** (Python)
- **node-cron** (Node.js)
- **Cloud Scheduler** (GCP) ou **EventBridge** (AWS)

**Frequência Recomendada:**
- Inicial: A cada 6 horas
- Após estabilização: A cada 12 horas ou diário

### Rate Limiting

**Importante:** Respeitar limites do servidor
- Delay entre requisições: 2-5 segundos
- User-Agent rotativo
- Headers apropriados
- Tratamento de erros (429, 503)

---

## 🛡️ Tratamento de Erros

### Cenários de Erro

1. **Site Indisponível**
   - Retry com backoff exponencial
   - Registrar erro e tentar novamente mais tarde

2. **Documento Não Encontrado**
   - Registrar e pular
   - Tentar novamente em próxima execução

3. **OCR Falhou**
   - Marcar como "ERRO_OCR"
   - Permitir processamento manual posterior

4. **Dados Inválidos**
   - Validar antes de armazenar
   - Registrar warning
   - Continuar processamento

### Logging

Registrar todos os eventos:
- Convenções coletadas
- Erros encontrados
- Tempo de processamento
- Estatísticas (total processado, sucessos, falhas)

