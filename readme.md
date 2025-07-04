# Projeto: Plataforma Web AgroAxis

## 1. Resumo

A plataforma AgroAxis é um sistema de gestão agropecuária (SaaS) projetado para otimizar a tomada de decisão em fazendas de pecuária leiteira. A aplicação web servirá como a ferramenta central para a consultoria AgroAxis, permitindo o lançamento de dados, acompanhamento de indicadores e a geração de relatórios estratégicos para os produtores rurais clientes.

O sistema será acessível via navegador em desktops e dispositivos móveis (design responsivo), com foco em uma **experiência de usuário intuitiva e visualmente agradável, inspirada no Material Design**.

## 2. Tecnologia Proposta

*   **Backend:** Python (Django).
    *   *Django é altamente recomendado por já vir com um painel de administração robusto, sistema de autenticação e ORM, o que acelera o desenvolvimento de sistemas de gestão como este.*
*   **Frontend:** HTML5, CSS3, JavaScript (com **MDBootstrap** para Material Design).
    *   *O uso de MDBootstrap garante a responsividade da aplicação e uma estética moderna, alinhada aos princípios do Material Design, otimizando a UI/UX.*
*   **Banco de Dados:** PostgreSQL (robusto, confiável e bem integrado com Python/Django).
*   **Hospedagem:** Serviços de nuvem como Heroku, DigitalOcean, ou AWS.

## 3. Estrutura e Perfis de Usuário

O sistema terá dois níveis de acesso principais para garantir a privacidade e a correta gestão dos dados.

### Perfil 1: Administrador (Consultor Master - Você)

O Administrador tem controle total sobre a plataforma.

*   **Funcionalidades:**
    *   Fazer login em seu painel de controle geral.
    *   **Cadastrar, editar e desativar/ativar contas de Produtores Rurais** através de uma interface dedicada.
    *   Visualizar uma lista de todos os seus clientes (produtores), com um indicador de "saúde" (verde/amarelo/vermelho) aprimorado com base em dados reais.
    *   **Acessar o painel individual de QUALQUER produtor** (funcionalidade "Logar como") para visualizar, lançar ou editar dados em nome dele.
    *   **Acessar e filtrar dados de Rebanho, Qualidade do Leite e Financeiro por produtor.**
    *   Gerar relatórios comparativos entre fazendas (de forma anônima) para benchmarking (futuro).
    *   Receber notificações sobre todos os clientes (ex: alertas de CCS alta).

### Perfil 2: Produtor Rural (Cliente)

O Produtor tem acesso restrito apenas aos dados de sua própria fazenda.

*   **Funcionalidades:**
    *   Fazer login com seu próprio usuário e senha (criado pelo Administrador).
    *   Visualizar o dashboard com os principais indicadores **da sua propriedade**, incluindo gráficos interativos populados com dados reais.
    *   Lançar novos dados (ex: inseminações, despesas, resultados de leite, eventos sanitários) **apenas para sua própria fazenda**.
    *   Visualizar históricos e gráficos **apenas dos seus dados**.
    *   Gerar e baixar relatórios da sua fazenda.

## 4. Módulos e Funcionalidades Principais

### Módulo 1: Dashboard Principal

É a primeira tela após o login. O conteúdo se adapta ao perfil do usuário.

*   **Visão do Produtor:**
    *   Card com a média de CCS/CBT do último mês.
    *   Card com o resumo financeiro (Receita x Despesa) do mês corrente.
    *   Card de Alertas (Ex: "3 vacas com mais de 90 dias pós-parto e vazias", "Vaca 101 com CCS alta há 2 meses") - **Alertas dinâmicos baseados em dados reais.**
    *   **Gráficos interativos:** Produção de leite dos últimos 30 dias, evolução de CCS/CBT, fluxo de caixa mensal - **Gráficos populados com dados reais.**
*   **Visão do Administrador:**
    *   Cards de resumo com total de produtores, ativos e inativos.
    *   Lista de fazendas clientes com um indicador de "saúde" (verde/amarelo/vermelho) aprimorado.
    *   Feed de atividades recentes de todos os clientes (futuro).
    *   Links rápidos para acessar o painel de cada produtor (via "Logar como").

### Módulo 2: Gestão de Rebanho

O coração operacional da fazenda.

*   `Cadastro de Animais`:
    *   Campos: Brinco (ID único), Nome, Data de Nascimento, Raça, Status (em lactação, seca, novilha, bezerra), Foto (futuro).
    *   **CRUD completo** (Criar, Ler, Atualizar, Deletar).
    *   **Filtros e Paginação** - **Admin pode filtrar por produtor; Produtor vê apenas seus animais.**
    *   **Admin pode selecionar o produtor ao cadastrar/editar animais.**
*   `Ficha Individual do Animal`:
    *   Uma tela com todo o histórico do animal: produções, eventos reprodutivos, sanitários, ocorrências.
    *   **Admin pode ver qualquer animal; Produtor vê apenas seus animais.**
*   `Controle Reprodutivo`:
    *   **Lançamento e visualização** de cio, cobertura/inseminação, diagnóstico de gestação (DG), previsão de parto e data do parto.
    *   **Admin pode adicionar/editar eventos para qualquer animal; Produtor apenas para seus animais.**
*   `Controle Sanitário`:
    *   **Lançamento e visualização** de registro de vacinas, medicamentos e tratamentos com data e carência.
    *   **Admin pode adicionar/editar eventos para qualquer animal; Produtor apenas para seus animais.**

### Módulo 3: Qualidade do Leite (Seu Nicho Principal)

*   `Lançamento de Resultados`:
    *   Área para lançar manualmente os dados mensais de CCS e CBT por animal, ou do tanque, incluindo volume de produção.
    *   **CRUD completo**.
    *   **Filtros e Paginação** - **Admin pode filtrar por produtor; Produtor vê apenas seus registros.**
    *   **Admin pode selecionar o produtor ao cadastrar/editar registros.**
    *   **(Evolução Futura):** Importação de planilhas CSV enviadas pelo laticínio.
*   `Análise Gráfica`:
    *   Gráfico da evolução de CCS/CBT do tanque ao longo do tempo.
    *   Gráfico comparativo da CCS dos animais individualmente.
*   `Ranking de Vacas-Problema`:
    *   Lista ordenada das vacas com maior CCS para facilitar a tomada de decisão (tratar, secar, descartar).

### Módulo 4: Gestão Financeira (Seu Outro Nicho)

*   `Lançamento Simplificado`:
    *   Formulário para registrar Receitas (venda de leite, venda de animais) e Despesas (alimentação, sanidade, mão de obra, etc.). Cada lançamento deve ser categorizado.
    *   **CRUD completo**.
    *   **Filtros e Paginação** - **Admin pode filtrar por produtor; Produtor vê apenas suas transações.**
    *   **Admin pode selecionar o produtor ao cadastrar/editar transações.**
*   `Relatório de Custo de Produção`:
    *   O sistema calcula automaticamente o **custo por litro de leite** com base nos dados lançados, o principal indicador que você vende.
*   `Fluxo de Caixa`:
    *   Demonstrativo simples de entradas e saídas por período, com gráfico mensal.

### Módulo 5: Análises (Novo)

*   **Dashboard de Análises:**
    *   Visão consolidada de gráficos de produção de leite, CCS/CBT e fluxo de caixa.
    *   **Admin pode selecionar o produtor para visualizar as análises.**
    *   **Produtor vê apenas suas próprias análises.**

### Módulo 6: Configurações e Utilitários

*   `Página de Configurações`:
    *   Permite ao usuário editar seu próprio perfil (senha, e-mail).
    *   Links para gerenciamento de categorias financeiras (via admin).
*   `Itens Úteis`:
    *   Página com links para calculadoras, modelos e recursos externos relevantes para a gestão da fazenda.

## 5. Próximos Passos e Evolução (Roadmap)

A abordagem é construir o **MVP (Mínimo Produto Viável)** e, em seguida, agregar valor iterativamente.

### Fase 1: MVP Essencial (Concluído)

*   Sistema de login para os 2 perfis (Admin e Produtor).
*   O Admin pode criar, editar e ativar/desativar contas de Produtor.
*   **Módulo de Qualidade do Leite completo:** Lançamento, visualização, filtros, paginação e gráficos - **Refatorado para vincular dados a produtores.**
*   **Módulo de Gestão de Rebanho (Cadastro de Animais):** Lançamento, visualização, filtros, paginação - **Refatorado para vincular dados a produtores.**
*   **Controle Reprodutivo e Sanitário:** Lançamento e visualização de eventos - **Refatorado para vincular dados a produtores.**
*   **Módulo Financeiro:** Lançamento de transações, visualização, filtros, paginação e relatórios básicos (custo de produção, fluxo de caixa) - **Refatorado para vincular dados a produtores.**
*   **Dashboards:** Dashboard do produtor com gráficos (populados com dados reais) e alertas dinâmicos, dashboard do administrador com lista de produtores (indicador de saúde aprimorado) e "Logar como".
*   **Novo Módulo de Análises:** Dashboard de análises com gráficos de produção de leite, CCS/CBT e fluxo de caixa, com filtro por produtor para admin.
*   **UI/UX:** Integração inicial do MDBootstrap para um visual Material Design e aprimoramentos gerais de interface.
*   **Feedback ao Usuário:** Mensagens de sucesso/erro.
*   **Segurança:** Configuração de `SECRET_KEY` via variável de ambiente.
*   **Organização de Código:** Scripts movidos para comandos de gerenciamento do Django.

### Fase 2: Agregando Valor (Próximas Prioridades)

*   **Aprimoramento da Ficha Individual do Animal:** Adicionar mais detalhes e visualizações de dados (ex: gráficos de produção individual).
*   **Relatórios Financeiros Avançados:** Análise de rentabilidade por animal/lote, orçamento.
*   **Notificações Inteligentes:** Alertas configuráveis (e-mail, SMS, WhatsApp).
*   **Otimização de Performance:** Garantir que o sistema seja rápido e responsivo com grandes volumes de dados.

### Fase 3: Inovação e Expansão (Ideias Futuras - Inspirado em líderes de mercado como Rumina)

*   **Análise Preditiva (AI/ML):** Previsão de produção, detecção precoce de doenças, otimização reprodutiva.
*   **Integrações (APIs):** Conexão com laboratórios, laticínios, sensores IoT (coleiras, medidores de leite).
*   **Aplicativo Web Progressivo (PWA):** Funcionalidades offline para lançamentos em campo.
*   **Módulo de Nutrição:** Controle de estoque de insumos e formulação de dietas.
*   **Gestão de Pastagens:** Registro e análise de áreas.
*   **Benchmarking Avançado:** Comparação anônima de indicadores entre fazendas.
*   **Ferramentas de Colaboração:** Acesso para consultores externos.
*   **Gamificação:** Elementos para engajar o usuário.
