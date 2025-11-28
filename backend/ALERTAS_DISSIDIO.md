# Sistema de Alertas de Dissídio

## 📋 Visão Geral

O sistema de alertas de dissídio monitora automaticamente o vencimento das convenções coletivas e gera notificações para empresas afetadas quando estão próximas do vencimento ou já vencidas.

## 🔔 Tipos de Alertas

O sistema gera alertas baseados nos dias restantes até o vencimento:

- **VENCIMENTO_PROXIMO_90**: 90 dias antes do vencimento (prioridade baixa)
- **VENCIMENTO_PROXIMO_60**: 60 dias antes do vencimento (prioridade média)
- **VENCIMENTO_PROXIMO_30**: 30 dias antes do vencimento (prioridade alta)
- **VENCIMENTO_URGENTE_15**: 15 dias antes do vencimento (prioridade urgente)
- **VENCIMENTO_URGENTE_7**: 7 dias antes do vencimento (prioridade urgente)
- **VENCIDO**: Convenção já vencida (até 180 dias após vencimento)

## 🚀 Como Funciona

### 1. Verificação Automática

A tarefa `check_dissidio_alerts` verifica diariamente todas as convenções ativas e gera alertas quando necessário.

### 2. Processo de Geração de Alertas

1. **Busca Convenções Ativas**: Encontra todas as convenções com `data_vigencia_fim >= hoje` e status `PROCESSADO`
2. **Calcula Dias Restantes**: Para cada convenção, calcula quantos dias faltam até o vencimento
3. **Gera Alertas**: Cria notificações para empresas associadas baseado nos dias restantes
4. **Verifica Vencidas**: Para convenções vencidas, verifica se há nova negociação em andamento
5. **Evita Duplicatas**: Não cria alertas duplicados se já existe um não lido do mesmo tipo

### 3. Associação com Empresas

Os alertas são gerados para empresas que:
- Estão diretamente associadas à convenção (via `ConvencaoEmpresa`)
- OU têm mesmo CNAE, município e UF da convenção

## 📡 Endpoints da API

### Listar Alertas de Dissídio

```http
GET /api/v1/notifications/dissidio?lida=false
```

**Parâmetros:**
- `lida` (opcional): Filtrar por notificações lidas/não lidas

**Resposta:**
```json
[
  {
    "id": "uuid",
    "tipo": "VENCIMENTO_PROXIMO_30",
    "titulo": "🔔 Convenção vence em 30 dias",
    "mensagem": "A convenção '...' vence em 30 dias (31/12/2024)...",
    "lida": false,
    "convencao_id": "uuid",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Executar Verificação Manualmente

```http
POST /api/v1/collector/check-dissidio-alerts
```

**Resposta:**
```json
{
  "status": "accepted",
  "message": "Verificação de alertas de dissídio iniciada em background."
}
```

## 🛠️ Execução Manual

### Via Script Python

```bash
cd backend
python check_dissidio_alerts.py
```

### Via PowerShell

```powershell
cd backend
.\check_dissidio_alerts.ps1
```

### Via API (com autenticação)

```bash
curl -X POST http://localhost:8000/api/v1/collector/check-dissidio-alerts \
  -H "Authorization: Bearer SEU_TOKEN"
```

## ⚙️ Configuração de Agendamento Automático

### Opção 1: Celery Beat (Recomendado)

Crie um arquivo `celeryconfig.py`:

```python
from celery.schedules import crontab

beat_schedule = {
    'check-dissidio-alerts-daily': {
        'task': 'check_dissidio_alerts',
        'schedule': crontab(hour=8, minute=0),  # Todo dia às 8h
    },
}
```

Execute o Celery Beat:

```bash
celery -A app.tasks.dissidio_alerts.celery_app beat --loglevel=info
```

### Opção 2: Cron Job (Linux/Mac)

Adicione ao crontab:

```bash
0 8 * * * cd /caminho/para/backend && python check_dissidio_alerts.py
```

### Opção 3: Task Scheduler (Windows)

1. Abra o Task Scheduler
2. Crie uma nova tarefa
3. Configure para executar diariamente às 8h
4. Ação: Executar `check_dissidio_alerts.ps1`

## 🎨 Interface do Usuário

### Dashboard

O dashboard exibe:
- Card com contador de alertas de dissídio não lidos
- Seção destacada com os 3 alertas mais urgentes
- Link rápido para página de alertas de dissídio

### Página de Alertas de Dissídio

Acesse em: `/notifications/dissidio`

**Recursos:**
- Lista todos os alertas ordenados por prioridade
- Filtros: Todas / Não lidas
- Cores diferentes por tipo de alerta:
  - 🔴 Vermelho: Urgente (7, 15 dias) e Vencido
  - 🟠 Laranja: 30 dias
  - 🟡 Amarelo: 60 dias
  - 🔵 Azul: 90 dias
- Botão para marcar como lida
- Link direto para a convenção relacionada

## 📊 Estrutura de Dados

### Notification Model

```python
class Notification(Base):
    tipo: str  # VENCIMENTO_PROXIMO_90, VENCIMENTO_URGENTE_7, etc.
    titulo: str  # Título do alerta
    mensagem: str  # Mensagem detalhada
    convencao_id: UUID  # ID da convenção relacionada
    user_id: UUID  # ID do usuário que recebe o alerta
    lida: bool  # Se o alerta foi lido
```

## 🔍 Detecção de Nova Negociação

O sistema verifica se uma convenção vencida já tem uma nova negociação em andamento:

- Busca convenções mais recentes para o mesmo CNAE/município/UF
- Se encontrar, não gera alerta de "vencido" (assumindo que já há renovação)
- Se não encontrar, gera alerta de "vencido" (até 180 dias após vencimento)

## 📝 Mensagens Personalizadas

Cada tipo de alerta tem uma mensagem específica:

- **90 dias**: "Planeje a renovação"
- **60 dias**: "Planeje a renovação"
- **30 dias**: "Considere iniciar o processo de renovação"
- **15 dias**: "Prepare-se para iniciar a negociação"
- **7 dias**: "É necessário iniciar a negociação para renovação"
- **Vencido**: "Verifique se há nova negociação em andamento"

## 🚨 Boas Práticas

1. **Execute diariamente**: Configure o agendamento para rodar uma vez por dia
2. **Horário recomendado**: 8h da manhã (antes do horário comercial)
3. **Monitore logs**: Verifique os logs para garantir que está funcionando
4. **Teste manualmente**: Execute o script manualmente antes de configurar agendamento
5. **Revise alertas**: Periodicamente revise se os alertas estão sendo gerados corretamente

## 🐛 Troubleshooting

### Alertas não estão sendo gerados

1. Verifique se há convenções com `data_vigencia_fim` preenchida
2. Verifique se as convenções têm status `PROCESSADO`
3. Verifique se há empresas associadas às convenções
4. Execute manualmente e verifique os logs

### Alertas duplicados

- O sistema evita duplicatas verificando se já existe alerta não lido do mesmo tipo
- Se ainda assim aparecerem duplicatas, verifique a lógica de verificação

### Alertas não aparecem no frontend

1. Verifique se o endpoint `/notifications/dissidio` está funcionando
2. Verifique se o usuário está autenticado
3. Verifique se há alertas não lidos no banco de dados

## 📚 Arquivos Relacionados

- `backend/app/tasks/dissidio_alerts.py` - Tarefa principal de verificação
- `backend/app/api/v1/endpoints/notifications.py` - Endpoints de notificações
- `backend/app/api/v1/endpoints/collector.py` - Endpoint para execução manual
- `frontend/app/notifications/dissidio/page.tsx` - Página de alertas
- `frontend/app/dashboard/page.tsx` - Dashboard com resumo de alertas

