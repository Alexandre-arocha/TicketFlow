
# 🎫 TicketFlow - Sistema de Gerenciamento de Tickets

**Versão 2.0** | ✅ Pronto para Produção | 🎯 Interface Moderna

Um sistema completo e profissional para gerenciar tickets de chamados com interface gráfica moderna, rastreabilidade completa, controle de prioridade e histórico detalhado.

---

## 🌟 Destaques Principais

- ✨ **Interface Gráfica Moderna** - GUI intuitiva com tkinter
- 💻 **Interface CLI** - Linha de comando para usuários avançados
- 🎨 **Temas Personalizáveis** - Múltiplos temas inclusos
- 🔍 **Busca e Filtros Avançados** - Encontre tickets rapidamente
- 📊 **Relatórios Completos** - Analise seus dados
- 💾 **Persistência JSON** - Dados salvos automaticamente
- ✅ **Totalmente Funcional** - Testado e pronto para uso real

---

## 🚀 Início Rápido

### 1. Abrir a Interface Gráfica
```bash
python main.py
# Escolha opção 1: Interface Gráfica
```

### 2. Ou abrir direto
```bash
python run_gui.py
```

### 3. Interface CLI
```bash
python run_cli.py
```

---

## 📦 Funcionalidades Completas

### 🎯 Gerenciamento de Tickets
- ✅ Criar tickets com título, descrição, prioridade e categoria
- ✅ Visualizar detalhes completos
- ✅ Atualizar status em tempo real
- ✅ Gerenciar prioridades (Baixa, Média, Alta, Crítica)
- ✅ Atribuir responsáveis
- ✅ Deletar tickets
- ✅ Adicionar comentários

### 📊 Estados e Prioridades
**Estados:**
- 🔴 Aberto
- 🟡 Em Andamento
- ⏸️ Pausado
- ✅ Resolvido
- ⬛ Fechado
- 🔄 Reaberto

**Prioridades:**
- 🔥 CRÍTICA (Urgente)
- ⚠️ ALTA (Importante)
- 📌 MÉDIA (Normal)
- 💤 BAIXA (Baixa)

### 📈 Recursos Avançados
- 🔍 Pesquisa em tempo real
- 🎯 Filtros por status/prioridade
- 📋 Relatórios detalhados
- 📝 Histórico completo de alterações
- 💬 Comentários com rastreamento
- 👤 Controle de usuários
- 📅 Timestamps automáticos
- 🔄 Ordenação inteligente

---

## 📁 Estrutura do Projeto

```
TicketFlow/
├── main.py                    # Menu principal com 4 opções
├── run_gui.py                # Inicializador direto da GUI
├── run_cli.py                # Inicializador direto da CLI
├── interface_gui.py          # Interface gráfica (NOVO - v2.0)
├── interface_cli.py          # Interface CLI
├── sistema_tickets.py        # Lógica central
├── models.py                 # Modelos de dados
├── gerenciador_dados.py      # Persistência JSON
├── config.py                 # Temas e configurações (NOVO)
├── test_functionality.py     # Testes (NOVO)
├── tickets.json              # Base de dados
├── GUIA_USUARIO.md          # Guia completo de uso (NOVO)
├── DOCUMENTACAO.md          # Documentação técnica (NOVO)
├── README.md                # Este arquivo (ATUALIZADO)
└── LICENSE                  # Licença MIT
```

---

## 🖥️ Interface Gráfica (NOVO em v2.0)

### Layout Intuitivo
```
┌───────────────────────────────────────────────────────────────┐
│   🎫 TicketFlow - Sistema de Gerenciamento de Chamados       │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┬──────────────────────────────┐
│    PAINEL ESQUERDO              │   PAINEL DE DETALHES         │
│                                 │                              │
│ 👤 Usuário Atual: [_________]   │ ┌──────────────────────────┐ │
│                                 │ │ Detalhes do Ticket       │ │
│ 🔍 Pesquisar: [_________]       │ │ ID: ABC12345             │ │
│                                 │ │ Título: ...              │ │
│ 🎯 Status: [Todos ▼]            │ │ Status: ✅ Resolvido     │ │
│ ⭐ Prioridade: [Todos ▼]        │ │ Prioridade: 🔥 CRÍTICA   │ │
│                                 │ │                          │ │
│ 📋 Tickets:                     │ │ [✏️][🎯][⭐][💬][🗑️]   │
│ ┌──────────────────────────────┐│ └──────────────────────────┘ │
│ │ ID123 | ✅ Título  | 📌 MED  ││                              │
│ │ ID124 | 🟡 Título  | 🔥 CRIT ││                              │
│ │ ID125 | 🔴 Título  | ⚠️ ALTA ││                              │
│ └──────────────────────────────┘│                              │
│                                 │                              │
│ [➕][👁️][📋][🔄]              │                              │
└─────────────────────────────────┴──────────────────────────────┘
```

### Recursos da GUI
- 🖱️ Duplo clique para visualizar
- 🔄 Atualização em tempo real
- 🎨 Temas personalizáveis
- 📱 Design responsivo
- ⌨️ Atalhos intuitivos
- 🎯 Ordenação automática

---

## 💻 Exemplos de Uso

### Criar um Novo Ticket
```
1. Clique em [➕ Novo Ticket]
2. Preencha: Título, Descrição, Prioridade
3. Clique em [✅ Criar Ticket]
```

### Filtrar Tickets
```
1. Selecione um Status
2. Selecione uma Prioridade
3. Digite na Pesquisa
4. Lista atualiza automaticamente
```

### Gerar Relatório
```
1. Clique em [📋 Relatório]
2. Janela com estatísticas é aberta
3. Copie ou analise os dados
```

---

## 📊 Dados de Exemplo

### Estrutura de um Ticket
```json
{
  "id": "ABC12345",
  "titulo": "Erro na tela de login",
  "descricao": "Usuários relatando erro ao fazer login",
  "prioridade": "ALTA",
  "status": "em_andamento",
  "criado_por": "João Silva",
  "atribuido_a": "Maria Santos",
  "categoria": "Bug",
  "criado_em": "2025-12-24T10:30:15",
  "atualizado_em": "2025-12-24T11:45:30",
  "comentarios": [...],
  "historico": [...]
}
```

---

## 🎨 Temas Disponíveis

No arquivo `config.py`, mude:
```python
THEME_ACTIVE = "THEME_DEFAULT"  # Escolha um:
```

- `THEME_DEFAULT` - Moderno (padrão) ⭐
- `THEME_DARK` - Escuro
- `THEME_LIGHT` - Claro
- `THEME_CORPORATE` - Corporativo
- `THEME_MINIMAL` - Minimalista
- `THEME_NEON` - Neon (Gamer)
- `THEME_SOLARIZED` - Solarized (Dev)

---

## 🔧 Configuração Avançada

### Personalizar Interface
Edite `config.py`:
```python
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
AUTO_REFRESH_SECONDS = 0
CONFIRM_DELETE = True
```

### Backup Automático
```python
AUTO_BACKUP = True
BACKUP_COUNT = 5
```

---

## 🧪 Testes

Execute testes para verificar tudo funciona:
```bash
python test_functionality.py
```

Resultado esperado:
```
✅ Importar Módulos - PASSOU
✅ Criar Tickets - PASSOU
✅ Tkinter - PASSOU
✅ Persistência JSON - PASSOU
✅ Operações de Status - PASSOU
🎉 TODOS OS TESTES PASSARAM!
```

---

## 📚 Documentação

- **[GUIA_USUARIO.md](GUIA_USUARIO.md)** - Guia completo do usuário
- **[DOCUMENTACAO.md](DOCUMENTACAO.md)** - Documentação técnica
- **[config.py](config.py)** - Configurações e temas
- **[test_functionality.py](test_functionality.py)** - Testes

---

## 🐛 Troubleshooting

### Interface não abre
```bash
pip install --upgrade tkinter
```

### Arquivo não encontrado
```bash
# Arquivo tickets.json é criado automaticamente
# Se precisar resetar:
echo {"tickets": []} > tickets.json
```

### Permissão negada
```bash
# Windows: Clique direito → Propriedades → Segurança
# Linux/Mac: chmod 755 .
```

---

## 🎯 Roadmap Futuro

- [ ] Suporte a múltiplos usuários/autenticação
- [ ] Banco de dados (SQLite/PostgreSQL)
- [ ] API REST
- [ ] Aplicativo Mobile
- [ ] Notificações
- [ ] Exportação (PDF, Excel)
- [ ] Temas mais personalizáveis

---

## 📜 Licença

Este projeto está sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Informações da Versão

| Item | Valor |
|------|-------|
| **Versão** | 2.0 |
| **Status** | ✅ Produção |
| **Python** | 3.8+ |
| **Tkinter** | 8.6+ |
| **Última Atualização** | 24/12/2025 |
| **Autor** | TicketFlow Team |

---

## 🎓 Para Desenvolvedores

Para entender a arquitetura e contribuir:
1. Leia [DOCUMENTACAO.md](DOCUMENTACAO.md)
2. Explore `sistema_tickets.py` para lógica
3. Modifique `interface_gui.py` para UI
4. Execute testes: `python test_functionality.py`

---

## 💡 Dicas de Uso

✅ **Sempre defina seu usuário** antes de criar tickets  
✅ **Use filtros** para encontrar tickets mais rápido  
✅ **Adicione comentários** para rastrear discussões  
✅ **Gere relatórios** regularmente  
✅ **Faça backup** periodicamente  

---

## 🎉 Começar Agora!

```bash
python main.py
# Escolha opção 1 para Interface Gráfica
```

**Bem-vindo ao TicketFlow! 🎫**


```bash
python main.py
```

#### Demonstração
```bash
python main.py --demo
```
