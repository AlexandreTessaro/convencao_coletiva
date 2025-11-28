# Busca em Tempo Real do Mediador MTE

## 🎯 Funcionalidade

A aplicação agora suporta busca de convenções coletivas diretamente do site do Mediador MTE em tempo real, sem precisar armazenar os dados no banco primeiro.

## 📡 Endpoints Disponíveis

### 1. Busca em Tempo Real (`/api/v1/mediador/search-live`)

Busca convenções diretamente do site do Mediador MTE sem consultar o banco local.

**Parâmetros:**
- `municipio` (opcional): Nome do município
- `uf` (opcional): Sigla do estado (ex: SP, RJ)
- `cnae` (opcional): Código CNAE
- `cnpj` (opcional): CNPJ da empresa
- `limit` (padrão: 20): Limite de resultados (1-100)

**Exemplo:**
```bash
GET /api/v1/mediador/search-live?municipio=São Paulo&uf=SP&limit=10
```

**Resposta:**
```json
{
  "total": 10,
  "results": [
    {
      "instrumento_id": "12345678",
      "titulo": "Convenção Coletiva de Trabalho...",
      "data_publicacao": "2024-01-15",
      "municipio": "São Paulo",
      "uf": "SP",
      "cnae": "62015",
      "fonte": "mediador_mte"
    }
  ],
  "source": "mediador_mte_live"
}
```

### 2. Busca Híbrida (`/api/v1/mediador/search-hybrid`)

Combina resultados do banco local com busca em tempo real do Mediador MTE.

**Parâmetros:**
- Todos os parâmetros da busca local (`q`, `municipio`, `uf`, `cnae`, `cnpj`, `keyword`)
- `page` (padrão: 1): Número da página
- `page_size` (padrão: 20): Tamanho da página
- `use_live` (padrão: false): Se `true`, inclui resultados em tempo real

**Exemplo:**
```bash
GET /api/v1/mediador/search-hybrid?municipio=São Paulo&use_live=true&page=1&page_size=20
```

## 🖥️ Interface do Usuário

Na página de busca (`/convencoes/search`), você pode escolher entre três modos:

1. **Banco Local**: Busca apenas nos dados já coletados e armazenados
2. **Mediador MTE (Tempo Real)**: Busca diretamente do site do Mediador MTE
3. **Híbrido**: Combina resultados do banco local + busca em tempo real

## ⚙️ Como Funciona

### Processo de Busca em Tempo Real

1. **Requisição HTTP**: Faz uma requisição para o site do Mediador MTE
2. **Parse HTML**: Extrai informações das páginas HTML usando BeautifulSoup
3. **Múltiplas Estratégias**: Tenta diferentes seletores CSS para encontrar dados
4. **Retorno**: Retorna os dados formatados em JSON

### Limitações

- **Estrutura do Site**: O scraper precisa ser ajustado se a estrutura HTML do site mudar
- **Rate Limiting**: O site pode limitar requisições muito frequentes
- **Autenticação**: Algumas áreas podem requerer login
- **Performance**: Busca em tempo real é mais lenta que busca no banco local

## 🔧 Configuração

A URL base do Mediador MTE está configurada em `backend/app/core/config.py`:

```python
MEDIADOR_API_URL: str = "https://www3.mte.gov.br/sistemas/mediador"
```

Você pode alterar isso no arquivo `.env`:

```env
MEDIADOR_API_URL=https://www3.mte.gov.br/sistemas/mediador
```

## 📝 Notas Importantes

1. **Legalidade**: Certifique-se de que o scraping está de acordo com os termos de uso do site
2. **Respeito**: O código inclui delays entre requisições para não sobrecarregar o servidor
3. **Manutenção**: Se o site mudar sua estrutura, será necessário ajustar os seletores CSS
4. **Fallback**: Se a busca em tempo real falhar, você ainda pode usar os dados do banco local

## 🐛 Troubleshooting

### Nenhum resultado encontrado

- Verifique se o site está acessível
- Verifique os logs do backend para ver erros específicos
- Ajuste os seletores CSS em `backend/app/services/mediador_api.py`

### Erro de timeout

- O site pode estar lento ou indisponível
- Aumente o timeout nas configurações
- Tente novamente mais tarde

### Dados incompletos

- Alguns campos podem não estar disponíveis no site
- O scraper tenta extrair o máximo possível, mas pode não conseguir todos os campos

## 🚀 Melhorias Futuras

- Cache de resultados em tempo real
- Suporte a autenticação se necessário
- Melhor tratamento de erros
- Suporte a mais filtros de busca
- Webhooks para notificações de novas convenções

