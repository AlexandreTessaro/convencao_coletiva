# Índice da Documentação

## 📚 Documentos do Projeto

1. **[Visão do Produto](./01-visao-produto.md)**
   - Nome do produto: **ConvençãoColetiva**
   - Descrição curta e longa
   - Proposta de valor
   - Objetivos do MVP

2. **[Personas e Casos de Uso](./02-personas-casos-uso.md)**
   - 4 personas principais (Ana, Carlos, Maria, João)
   - 8 casos de uso detalhados
   - Fluxos de interação

3. **[Arquitetura do MVP](./03-arquitetura.md)**
   - Visão geral da arquitetura
   - 9 módulos principais
   - Stack tecnológica recomendada
   - Estrutura do banco de dados
   - Escalabilidade futura

4. **[Fluxo de Coleta de Dados](./04-fluxo-coleta.md)**
   - Processo detalhado de coleta
   - Extração de IDs de instrumentos coletivos
   - Processamento de documentos (HTML, PDF digital, PDF escaneado)
   - Armazenamento e indexação
   - Diagramas e exemplos de código

5. **[Riscos e Mitigação](./05-riscos-mitigacao.md)**
   - Análise de riscos legais, técnicos, de negócio e operacionais
   - Estratégias de mitigação
   - Planos de contingência
   - Matriz de riscos

6. **[Backlog Inicial](./06-backlog.md)**
   - 6 épicos principais
   - 28 histórias de usuário detalhadas
   - Priorização do MVP
   - Métricas de sucesso

7. **[Prototipação Textual](./07-prototipacao.md)**
   - 7 telas principais (Login, Dashboard, Cadastro, etc.)
   - Componentes reutilizáveis
   - Responsividade
   - Fluxos de navegação
   - Paleta de cores e acessibilidade

---

## 🚀 Início Rápido

### Para Desenvolvedores
1. Leia a [Arquitetura](./03-arquitetura.md) para entender a estrutura técnica
2. Consulte o [Fluxo de Coleta](./04-fluxo-coleta.md) para implementar o scraper
3. Revise o [Backlog](./06-backlog.md) para entender as funcionalidades

### Para Product Owners
1. Comece pela [Visão do Produto](./01-visao-produto.md)
2. Entenda as [Personas](./02-personas-casos-uso.md) e casos de uso
3. Revise o [Backlog](./06-backlog.md) para planejamento de sprints

### Para Stakeholders
1. Leia a [Visão do Produto](./01-visao-produto.md) para entender o produto
2. Consulte [Riscos e Mitigação](./05-riscos-mitigacao.md) para avaliação
3. Veja a [Prototipação](./07-prototipacao.md) para visualizar a interface

---

## 📋 Resumo Executivo

### O Produto
**ConvençãoColetiva** é uma plataforma SaaS que automatiza a busca, organização e notificação de Convenções Coletivas de Trabalho (CCTs) para empresas e profissionais de RH.

### Principais Funcionalidades
- ✅ Coleta automática de convenções do Mediador MTE
- ✅ Busca por CNPJ, CNAE, município e palavras-chave
- ✅ Notificações de novas convenções aplicáveis
- ✅ Dashboard com visão consolidada
- ✅ Histórico e comparação de convenções

### Tecnologias Principais
- **Backend:** Python (FastAPI) ou Node.js (Express)
- **Frontend:** React/Next.js ou Vue.js/Nuxt.js
- **Banco:** PostgreSQL
- **Scraping:** Scrapy/Selenium ou Puppeteer
- **OCR:** Tesseract

### Próximos Passos
1. Validar termos de uso do Mediador MTE
2. Implementar MVP conforme backlog priorizado
3. Testar coleta de dados em ambiente de desenvolvimento
4. Obter feedback de usuários beta

---

## 📞 Contato e Suporte

Para dúvidas ou sugestões sobre a documentação, consulte o README principal do projeto.

