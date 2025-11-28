# Personas e Casos de Uso

## 👥 Personas

### 1. Ana - Gerente de RH

**Perfil Demográfico:**
- Idade: 35-45 anos
- Cargo: Gerente de RH em empresa média (100-500 funcionários)
- Localização: Grande centro urbano
- Experiência: 8-12 anos em RH

**Características:**
- Responsável por garantir conformidade trabalhista
- Lida com múltiplas empresas do grupo
- Precisa estar sempre atualizada sobre novas convenções
- Tem pouco tempo para busca manual
- Valoriza organização e eficiência

**Necessidades:**
- Receber alertas quando novas convenções são publicadas
- Acessar rapidamente convenções aplicáveis às empresas que gerencia
- Comparar cláusulas entre diferentes convenções
- Manter histórico para auditorias

**Frustrações:**
- Perder tempo buscando convenções manualmente
- Descobrir novas convenções tarde demais
- Dificuldade em organizar múltiplas versões
- Falta de centralização das informações

**Objetivos:**
- Manter conformidade trabalhista
- Economizar tempo em tarefas administrativas
- Evitar problemas legais por desconhecimento

---

### 2. Carlos - Advogado Trabalhista

**Perfil Demográfico:**
- Idade: 30-50 anos
- Cargo: Advogado especializado em direito trabalhista
- Localização: Escritório de advocacia em capital
- Experiência: 5-20 anos de experiência

**Características:**
- Atende múltiplos clientes de diferentes setores
- Precisa pesquisar convenções para casos específicos
- Valoriza precisão e completude de informações
- Trabalha sob pressão de prazos
- Precisa comparar diferentes convenções

**Necessidades:**
- Buscar convenções por CNPJ, CNAE ou sindicato
- Encontrar cláusulas específicas rapidamente
- Comparar convenções antigas e recentes
- Acessar histórico completo de publicações
- Exportar dados para análises

**Frustrações:**
- Sites governamentais lentos e difíceis de navegar
- PDFs escaneados difíceis de pesquisar
- Falta de ferramentas de comparação
- Informações desorganizadas

**Objetivos:**
- Encontrar informações precisas rapidamente
- Fornecer análises completas aos clientes
- Economizar tempo em pesquisas

---

### 3. Maria - Analista de Compliance

**Perfil Demográfico:**
- Idade: 28-38 anos
- Cargo: Analista de Compliance em grande empresa (500+ funcionários)
- Localização: Empresa multinacional no Brasil
- Experiência: 3-8 anos em compliance

**Características:**
- Responsável por garantir conformidade regulatória
- Trabalha com múltiplas unidades e filiais
- Precisa documentar tudo para auditorias
- Valoriza rastreabilidade e histórico
- Trabalha com equipes distribuídas

**Necessidades:**
- Monitorar convenções de múltiplas localidades
- Manter histórico completo e organizado
- Receber notificações sobre mudanças
- Compartilhar informações com equipe
- Gerar relatórios de conformidade

**Frustrações:**
- Dificuldade em monitorar múltiplas fontes
- Falta de visibilidade sobre mudanças
- Processo manual propenso a erros
- Dificuldade em comprovar conformidade

**Objetivos:**
- Garantir conformidade em todas as unidades
- Facilitar auditorias com documentação completa
- Reduzir riscos de não conformidade

---

### 4. João - Empresário/CEO de Pequena Empresa

**Perfil Demográfico:**
- Idade: 40-55 anos
- Cargo: CEO/Proprietário de empresa pequena (10-50 funcionários)
- Localização: Cidades médias ou grandes
- Experiência: Empresário com conhecimento básico de RH

**Características:**
- Usa serviços terceirizados de RH ou consultoria
- Precisa entender o que se aplica à sua empresa
- Valoriza simplicidade e clareza
- Tem pouco tempo para tarefas administrativas
- Preocupa-se com custos e conformidade

**Necessidades:**
- Saber quais convenções se aplicam à sua empresa
- Entender o impacto das convenções no negócio
- Receber alertas sobre mudanças importantes
- Acessar informações de forma simples

**Frustrações:**
- Complexidade de sites governamentais
- Dificuldade em entender jargão jurídico
- Falta de tempo para pesquisar
- Medo de não estar em conformidade

**Objetivos:**
- Manter-se em conformidade legal
- Entender obrigações trabalhistas
- Evitar problemas e multas
- Focar no negócio principal

---

## 🎯 Principais Casos de Uso

### UC01: Buscar Convenção por CNPJ

**Ator:** Ana (Gerente de RH)

**Pré-condições:**
- Usuário está autenticado
- CNPJ da empresa está cadastrado

**Fluxo Principal:**
1. Ana acessa o dashboard
2. Ana digita o CNPJ no campo de busca
3. Sistema busca convenções associadas ao CNPJ
4. Sistema exibe lista de convenções encontradas
5. Ana seleciona uma convenção para visualizar detalhes

**Fluxo Alternativo:**
- Se nenhuma convenção for encontrada, sistema informa e sugere busca por CNAE ou município

**Pós-condições:**
- Ana visualiza convenções aplicáveis à empresa

---

### UC02: Receber Notificação de Nova Convenção

**Ator:** Maria (Analista de Compliance)

**Pré-condições:**
- Usuário está autenticado
- Empresas estão cadastradas com CNPJ/CNAE
- Sistema de coleta identificou nova convenção

**Fluxo Principal:**
1. Sistema de coleta identifica nova convenção publicada
2. Sistema verifica se convenção é aplicável às empresas cadastradas
3. Sistema envia notificação (email/push) para usuários relevantes
4. Maria recebe notificação
5. Maria clica na notificação e acessa detalhes da convenção
6. Maria visualiza resumo e cláusulas principais

**Fluxo Alternativo:**
- Se usuário não estiver online, notificação fica pendente até próximo acesso

**Pós-condições:**
- Maria está ciente da nova convenção
- Convenção está disponível no sistema

---

### UC03: Buscar Cláusula por Palavra-chave

**Ator:** Carlos (Advogado Trabalhista)

**Pré-condições:**
- Usuário está autenticado
- Convenções estão indexadas no sistema

**Fluxo Principal:**
1. Carlos acessa a busca avançada
2. Carlos digita palavra-chave (ex: "piso salarial")
3. Sistema busca em todas as convenções indexadas
4. Sistema exibe resultados com contexto da cláusula
5. Carlos seleciona resultado para ver convenção completa
6. Sistema destaca termo buscado no documento

**Fluxo Alternativo:**
- Se nenhum resultado for encontrado, sistema sugere termos similares

**Pós-condições:**
- Carlos visualiza cláusulas relevantes encontradas

---

### UC04: Visualizar Histórico de Convenções

**Ator:** Maria (Analista de Compliance)

**Pré-condições:**
- Usuário está autenticado
- Empresa está cadastrada
- Existem convenções históricas no sistema

**Fluxo Principal:**
1. Maria acessa o dashboard
2. Maria seleciona uma empresa
3. Maria clica em "Histórico de Convenções"
4. Sistema exibe lista cronológica de convenções
5. Maria pode filtrar por período, categoria ou sindicato
6. Maria seleciona convenção antiga para comparar com atual

**Pós-condições:**
- Maria visualiza histórico completo de convenções

---

### UC05: Comparar Convenções

**Ator:** Ana (Gerente de RH)

**Pré-condições:**
- Usuário está autenticado
- Existem pelo menos duas convenções para comparar

**Fluxo Principal:**
1. Ana acessa lista de convenções
2. Ana seleciona duas convenções para comparar
3. Sistema exibe comparação lado a lado
4. Sistema destaca diferenças entre convenções
5. Ana pode exportar comparação em PDF

**Fluxo Alternativo:**
- Se convenções forem de formatos diferentes (HTML vs PDF), sistema converte para formato comparável

**Pós-condições:**
- Ana visualiza diferenças entre convenções

---

### UC06: Cadastrar Empresa para Monitoramento

**Ator:** João (Empresário)

**Pré-condições:**
- Usuário está autenticado
- Conta permite cadastro de empresas

**Fluxo Principal:**
1. João acessa "Minhas Empresas"
2. João clica em "Adicionar Empresa"
3. João preenche CNPJ, CNAE e município
4. Sistema valida informações
5. Sistema busca convenções existentes aplicáveis
6. Sistema ativa monitoramento automático
7. João recebe confirmação e visualiza convenções encontradas

**Fluxo Alternativo:**
- Se CNPJ for inválido, sistema solicita correção
- Se não houver convenções existentes, sistema informa que monitorará novas publicações

**Pós-condições:**
- Empresa está cadastrada e sendo monitorada
- Convenções existentes estão associadas à empresa

---

### UC07: Coletar Convenções Automaticamente

**Ator:** Sistema (Job automatizado)

**Pré-condições:**
- Sistema de coleta está configurado
- Acesso ao Mediador MTE está disponível

**Fluxo Principal:**
1. Job agendado executa busca no Mediador MTE
2. Sistema identifica novas convenções pelos IDs de instrumento coletivo
3. Para cada nova convenção:
   - Sistema extrai metadados (CNPJ, CNAE, município, sindicato)
   - Sistema baixa documento (HTML ou PDF)
   - Sistema extrai texto do documento
   - Sistema armazena no banco de dados
   - Sistema indexa para busca
4. Sistema verifica empresas cadastradas que podem ser afetadas
5. Sistema gera notificações para usuários relevantes

**Fluxo Alternativo:**
- Se documento for PDF escaneado, sistema usa OCR para extrair texto
- Se site estiver indisponível, sistema registra erro e tenta novamente mais tarde

**Pós-condições:**
- Novas convenções estão armazenadas no sistema
- Usuários relevantes foram notificados

---

### UC08: Visualizar Dashboard

**Ator:** Ana (Gerente de RH)

**Pré-condições:**
- Usuário está autenticado
- Empresas estão cadastradas

**Fluxo Principal:**
1. Ana acessa o dashboard após login
2. Sistema exibe:
   - Resumo de empresas cadastradas
   - Convenções recentes aplicáveis
   - Notificações pendentes
   - Estatísticas (total de convenções, últimas atualizações)
3. Ana pode filtrar por empresa ou período
4. Ana clica em convenção para ver detalhes

**Pós-condições:**
- Ana visualiza visão geral do sistema

