import sys
import uuid
import os
import json
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from dataclasses import dataclass, asdict, field

# Models (merged from models.py)
class PrioridadeEnum(Enum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4

    def __str__(self):
        return self.name.replace('_', ' ')


class StatusEnum(Enum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    PAUSADO = "pausado"
    RESOLVIDO = "resolvido"
    FECHADO = "fechado"
    REABERTO = "reaberto"

    def __str__(self):
        return self.value.replace('_', ' ').title()


@dataclass
class HistoricoAlteracao:
    data: str
    usuario: str
    campo: str
    valor_anterior: Optional[str]
    valor_novo: str
    descricao: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Comentario:
    id: str
    data: str
    usuario: str
    conteudo: str
    atualizado_em: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class User:
    username: str
    password_hash: str
    role: str = "user"  # 'admin' or 'user'
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


class UserManager:
    def __init__(self, arquivo_usuarios: str = "users.json"):
        self.arquivo_usuarios = arquivo_usuarios
        self._inicializar_arquivo()
        self.users: Dict[str, User] = self._carregar_usuarios_dict()
        # garantir usuário admin padrão
        if "admin" not in self.users:
            self.create_user("admin", "adim", role="admin")

    def _inicializar_arquivo(self):
        if not os.path.exists(self.arquivo_usuarios):
            with open(self.arquivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump({"users": []}, f, ensure_ascii=False, indent=2)

    def _carregar_usuarios_dict(self) -> Dict[str, User]:
        try:
            with open(self.arquivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            users = {}
            for u in data.get("users", []):
                user = User(username=u.get("username"), password_hash=u.get("password_hash"), role=u.get("role", "user"), created_at=u.get("created_at"))
                users[user.username] = user
            return users
        except Exception:
            return {}

    def _salvar_usuarios(self):
        data = {"users": [u.to_dict() for u in self.users.values()]}
        with open(self.arquivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create_user(self, username: str, password: str, role: str = "user") -> bool:
        username = username.strip()
        if not username or username in self.users:
            return False
        ph = self._hash_password(password)
        user = User(username=username, password_hash=ph, role=role)
        self.users[username] = user
        self._salvar_usuarios()
        return True

    def authenticate(self, username: str, password: str) -> Optional[User]:
        u = self.users.get(username)
        if not u:
            return None
        if u.password_hash == self._hash_password(password):
            return u
        return None

    def list_users(self) -> List[User]:
        return list(self.users.values())


@dataclass
class Ticket:
    id: str
    titulo: str
    descricao: str
    prioridade: str
    status: str = StatusEnum.ABERTO.value
    criado_em: str = field(default_factory=lambda: datetime.now().isoformat())
    atualizado_em: str = field(default_factory=lambda: datetime.now().isoformat())
    criado_por: str = "sistema"
    atribuido_a: Optional[str] = None
    categoria: Optional[str] = None
    historico: List[dict] = field(default_factory=list)
    comentarios: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def from_dict(data: dict):
        return Ticket(
            id=data.get('id'),
            titulo=data.get('titulo'),
            descricao=data.get('descricao'),
            prioridade=data.get('prioridade'),
            status=data.get('status', StatusEnum.ABERTO.value),
            criado_em=data.get('criado_em', datetime.now().isoformat()),
            atualizado_em=data.get('atualizado_em', datetime.now().isoformat()),
            criado_por=data.get('criado_por', 'sistema'),
            atribuido_a=data.get('atribuido_a'),
            categoria=data.get('categoria'),
            historico=data.get('historico', []),
            comentarios=data.get('comentarios', [])
        )


# Data manager (merged from gerenciador_dados.py)
class GerenciadorDados:
    def __init__(self, arquivo_dados: str = "tickets.json"):
        self.arquivo_dados = arquivo_dados
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        if not os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump({"tickets": []}, f, ensure_ascii=False, indent=2)

    def salvar_ticket(self, ticket: Ticket) -> bool:
        try:
            dados = self._carregar_dados()
            indice = None
            for i, t in enumerate(dados["tickets"]):
                if t["id"] == ticket.id:
                    indice = i
                    break
            if indice is not None:
                dados["tickets"][indice] = ticket.to_dict()
            else:
                dados["tickets"].append(ticket.to_dict())
            self._salvar_dados(dados)
            return True
        except Exception as e:
            print(f"Erro ao salvar ticket: {e}")
            return False

    def obter_ticket(self, ticket_id: str) -> Optional[Ticket]:
        try:
            dados = self._carregar_dados()
            for t in dados["tickets"]:
                if t["id"] == ticket_id:
                    return Ticket.from_dict(t)
            return None
        except Exception as e:
            print(f"Erro ao obter ticket: {e}")
            return None

    def obter_todos_tickets(self) -> List[Ticket]:
        try:
            dados = self._carregar_dados()
            return [Ticket.from_dict(t) for t in dados["tickets"]]
        except Exception as e:
            print(f"Erro ao obter tickets: {e}")
            return []

    def obter_tickets_por_status(self, status: str) -> List[Ticket]:
        return [t for t in self.obter_todos_tickets() if t.status == status]

    def obter_tickets_por_prioridade(self, prioridade: str) -> List[Ticket]:
        return [t for t in self.obter_todos_tickets() if t.prioridade == prioridade]

    def obter_tickets_por_usuario(self, usuario: str) -> List[Ticket]:
        return [t for t in self.obter_todos_tickets() if t.atribuido_a == usuario]

    def deletar_ticket(self, ticket_id: str) -> bool:
        try:
            dados = self._carregar_dados()
            dados["tickets"] = [t for t in dados["tickets"] if t["id"] != ticket_id]
            self._salvar_dados(dados)
            return True
        except Exception as e:
            print(f"Erro ao deletar ticket: {e}")
            return False

    def _carregar_dados(self) -> Dict:
        with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _salvar_dados(self, dados: Dict):
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def gerar_relatorio(self) -> Dict:
        tickets = self.obter_todos_tickets()
        return {
            "total_tickets": len(tickets),
            "por_status": self._contar_por_campo(tickets, "status"),
            "por_prioridade": self._contar_por_campo(tickets, "prioridade"),
            "por_usuario": self._contar_por_campo(tickets, "atribuido_a"),
            "tickets_abertos": len(self.obter_tickets_por_status(StatusEnum.ABERTO.value)),
            "tickets_criticos": len(self.obter_tickets_por_prioridade(PrioridadeEnum.CRITICA.name))
        }

    def _contar_por_campo(self, tickets: List[Ticket], campo: str) -> Dict:
        contagem = {}
        for ticket in tickets:
            valor = getattr(ticket, campo, None)
            if valor:
                contagem[valor] = contagem.get(valor, 0) + 1
        return contagem


# Business logic (merged from sistema_tickets.py)
class SistemaTickets:
    def __init__(self, arquivo_dados: str = "tickets.json"):
        self.gerenciador = GerenciadorDados(arquivo_dados)
        self.usuario_atual = "admin"

    def definir_usuario(self, usuario: str):
        self.usuario_atual = usuario

    def criar_ticket(
        self,
        titulo: str,
        descricao: str,
        prioridade: str = PrioridadeEnum.MEDIA.name,
        categoria: Optional[str] = None,
        atribuido_a: Optional[str] = None
    ) -> Ticket:
        ticket_id = str(uuid.uuid4())[:8].upper()
        ticket = Ticket(
            id=ticket_id,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            criado_por=self.usuario_atual,
            atribuido_a=atribuido_a,
            categoria=categoria
        )
        self._adicionar_historico(
            ticket,
            "status",
            None,
            StatusEnum.ABERTO.value,
            f"Ticket criado com título: {titulo}"
        )
        self.gerenciador.salvar_ticket(ticket)
        print(f"✓ Ticket criado com sucesso: {ticket_id}")
        return ticket

    def atualizar_status(self, ticket_id: str, novo_status: str) -> bool:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            print(f"✗ Ticket {ticket_id} não encontrado")
            return False
        status_anterior = ticket.status
        ticket.status = novo_status
        ticket.atualizado_em = datetime.now().isoformat()
        self._adicionar_historico(
            ticket,
            "status",
            status_anterior,
            novo_status,
            f"Status alterado de {status_anterior} para {novo_status}"
        )
        self.gerenciador.salvar_ticket(ticket)
        print(f"✓ Status do ticket {ticket_id} atualizado para: {novo_status}")
        return True

    def atualizar_prioridade(self, ticket_id: str, nova_prioridade: str) -> bool:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            print(f"✗ Ticket {ticket_id} não encontrado")
            return False
        prioridade_anterior = ticket.prioridade
        ticket.prioridade = nova_prioridade
        ticket.atualizado_em = datetime.now().isoformat()
        self._adicionar_historico(
            ticket,
            "prioridade",
            prioridade_anterior,
            nova_prioridade,
            f"Prioridade alterada de {prioridade_anterior} para {nova_prioridade}"
        )
        self.gerenciador.salvar_ticket(ticket)
        print(f"✓ Prioridade do ticket {ticket_id} atualizada para: {nova_prioridade}")
        return True

    def atribuir_ticket(self, ticket_id: str, usuario: str) -> bool:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            print(f"✗ Ticket {ticket_id} não encontrado")
            return False
        usuario_anterior = ticket.atribuido_a or "não atribuído"
        ticket.atribuido_a = usuario
        ticket.atualizado_em = datetime.now().isoformat()
        self._adicionar_historico(
            ticket,
            "atribuido_a",
            usuario_anterior,
            usuario,
            f"Ticket atribuído para {usuario}"
        )
        self.gerenciador.salvar_ticket(ticket)
        print(f"✓ Ticket {ticket_id} atribuído para: {usuario}")
        return True

    def adicionar_comentario(self, ticket_id: str, conteudo: str) -> bool:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            print(f"✗ Ticket {ticket_id} não encontrado")
            return False
        comentario_id = str(uuid.uuid4())[:8]
        comentario = {
            "id": comentario_id,
            "data": datetime.now().isoformat(),
            "usuario": self.usuario_atual,
            "conteudo": conteudo,
            "atualizado_em": None
        }
        ticket.comentarios.append(comentario)
        ticket.atualizado_em = datetime.now().isoformat()
        self._adicionar_historico(
            ticket,
            "comentario",
            None,
            comentario_id,
            f"Comentário adicionado por {self.usuario_atual}"
        )
        self.gerenciador.salvar_ticket(ticket)
        print(f"✓ Comentário adicionado ao ticket {ticket_id}")
        return True

    def obter_historico(self, ticket_id: str) -> List[dict]:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            print(f"✗ Ticket {ticket_id} não encontrado")
            return []
        return ticket.historico

    def visualizar_ticket(self, ticket_id: str) -> Optional[str]:
        ticket = self.gerenciador.obter_ticket(ticket_id)
        if not ticket:
            return f"✗ Ticket {ticket_id} não encontrado"
        info = f"""
╔══════════════════════════════════════════════════════════════╗
║                      DETALHES DO TICKET                      ║
╠══════════════════════════════════════════════════════════════╣
║ ID: {ticket.id}
║ Título: {ticket.titulo}
║ Descrição: {ticket.descricao}
║ Status: {ticket.status}
║ Prioridade: {ticket.prioridade}
║ Categoria: {ticket.categoria or 'N/A'}
║ Criado por: {ticket.criado_por}
║ Criado em: {ticket.criado_em}
║ Atribuído a: {ticket.atribuido_a or 'Não atribuído'}
║ Atualizado em: {ticket.atualizado_em}
╠══════════════════════════════════════════════════════════════╣
║                      COMENTÁRIOS                             ║
╠══════════════════════════════════════════════════════════════╣"""
        if ticket.comentarios:
            for com in ticket.comentarios:
                info += f"\n║ [{com['usuario']}] {com['data']}: {com['conteudo']}"
        else:
            info += "\n║ Nenhum comentário"
        info += """
╠══════════════════════════════════════════════════════════════╣
║                      HISTÓRICO                               ║
╠══════════════════════════════════════════════════════════════╣"""
        if ticket.historico:
            for hist in ticket.historico:
                info += f"\n║ [{hist['data']}] {hist['descricao']}"
        else:
            info += "\n║ Sem histórico"
        info += "\n╚══════════════════════════════════════════════════════════════╝"
        return info

    def listar_tickets(
        self,
        status: Optional[str] = None,
        prioridade: Optional[str] = None,
        usuario: Optional[str] = None
    ) -> List[Ticket]:
        tickets = self.gerenciador.obter_todos_tickets()
        if status:
            tickets = [t for t in tickets if t.status == status]
        if prioridade:
            tickets = [t for t in tickets if t.prioridade == prioridade]
        if usuario:
            tickets = [t for t in tickets if t.atribuido_a == usuario]
        return tickets

    def _adicionar_historico(
        self,
        ticket: Ticket,
        campo: str,
        valor_anterior: Optional[str],
        valor_novo: str,
        descricao: str
    ):
        historico_entrada = {
            "data": datetime.now().isoformat(),
            "usuario": self.usuario_atual,
            "campo": campo,
            "valor_anterior": valor_anterior,
            "valor_novo": valor_novo,
            "descricao": descricao
        }
        ticket.historico.append(historico_entrada)

    def obter_estatisticas(self) -> Dict:
        return self.gerenciador.gerar_relatorio()

    def gerar_relatorio_completo(self) -> str:
        stats = self.obter_estatisticas()
        relatorio = """
╔════════════════════════════════════════════════════════════════════╗
║                   RELATÓRIO DO SISTEMA DE TICKETS                  ║
╠════════════════════════════════════════════════════════════════════╣
║ RESUMO GERAL
╠════════════════════════════════════════════════════════════════════╣"""
        relatorio += f"\n║ Total de Tickets: {stats['total_tickets']}"
        relatorio += f"\n║ Tickets Abertos: {stats['tickets_abertos']}"
        relatorio += f"\n║ Tickets Críticos: {stats['tickets_criticos']}"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        relatorio += "\n║ POR STATUS"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        for status, count in stats['por_status'].items():
            relatorio += f"\n║ {status}: {count}"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        relatorio += "\n║ POR PRIORIDADE"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        for prioridade, count in stats['por_prioridade'].items():
            relatorio += f"\n║ {prioridade}: {count}"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        relatorio += "\n║ POR USUÁRIO"
        relatorio += "\n╠════════════════════════════════════════════════════════════════════╣"
        for usuario, count in stats['por_usuario'].items():
            relatorio += f"\n║ {usuario}: {count}"
        relatorio += "\n╚════════════════════════════════════════════════════════════════════╝"
        return relatorio

# Embedded compact GUI + CLI (merged to reduce file count)
import tkinter as tk
from tkinter import Tk, Frame, Listbox, Scrollbar, Button, Label, Entry, Text, END, Toplevel, StringVar, OptionMenu, messagebox, simpledialog


class InterfaceGUI:
    def __init__(self):
        self.sistema = SistemaTickets()
        self.root = Tk()
        self.root.title("TicketFlow - Gerenciador de Chamados")
        self.root.geometry("1200x650")
        self.root.minsize(800, 540)
        self.bg_color = "#f0f0f0"
        self.sidebar_color = "#2c3e50"
        self.button_color = "#3498db"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.warning_color = "#f39c12"
        self.root.configure(bg=self.bg_color)
        self.usuario_atual = StringVar(value="Usuário")
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        header = Frame(self.root, bg=self.sidebar_color, height=48)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        Label(header, text="🎫 TicketFlow", bg=self.sidebar_color, fg="white", font=("Helvetica", 14, "bold")).pack(side="left", padx=12)
        Label(header, textvariable=self.usuario_atual, bg=self.sidebar_color, fg="white").pack(side="right", padx=12)

        main_content = Frame(self.root, bg=self.bg_color)
        main_content.pack(fill="both", expand=True)

        left_panel = Frame(main_content, bg=self.sidebar_color, width=340)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        user_frame = Frame(left_panel, bg=self.sidebar_color)
        user_frame.pack(fill="x", padx=8, pady=8)
        Label(user_frame, text="Usuário Atual:", bg=self.sidebar_color, fg="white").pack(anchor="w")
        user_entry = Entry(user_frame)
        user_entry.pack(fill="x", pady=4)
        Button(user_frame, text="Definir Usuário", bg=self.success_color, fg="white", command=lambda: self._definir_usuario_campo(user_entry)).pack(fill="x")

        search_frame = Frame(left_panel, bg=self.sidebar_color)
        search_frame.pack(fill="x", padx=8, pady=8)
        Label(search_frame, text="Pesquisar:", bg=self.sidebar_color, fg="white").pack(anchor="w")
        self.search_var = StringVar()
        self.search_var.trace("w", lambda *a: self._filtrar_lista())
        Entry(search_frame, textvariable=self.search_var).pack(fill="x", pady=4)

        Label(left_panel, text="Tickets", bg=self.sidebar_color, fg="white").pack(anchor="w", padx=8, pady=(6, 0))
        list_frame = Frame(left_panel, bg="white")
        list_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.listbox = Listbox(list_frame)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self._visualizar())
        Scrollbar(list_frame, command=self.listbox.yview).pack(side="left", fill="y")

        btn_frame = Frame(left_panel, bg=self.sidebar_color)
        btn_frame.pack(fill="x", padx=8, pady=8)
        Button(btn_frame, text="Novo", command=self._novo_ticket, bg=self.button_color, fg="white").pack(fill="x", pady=2)
        Button(btn_frame, text="Visualizar", command=self._visualizar, bg=self.button_color, fg="white").pack(fill="x", pady=2)
        Button(btn_frame, text="Relatório", command=self._gerar_relatorio, bg=self.button_color, fg="white").pack(fill="x", pady=2)
        Button(btn_frame, text="Atualizar", command=self._refresh_list, bg="#95a5a6", fg="white").pack(fill="x", pady=2)

        right_panel = Frame(main_content, bg="white")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        Label(right_panel, text="Detalhes", bg="white", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.text = Text(right_panel)
        self.text.pack(fill="both", expand=True)
        actions = Frame(right_panel, bg="white")
        actions.pack(fill="x")
        Button(actions, text="Atribuir", command=self._atribuir, bg=self.button_color, fg="white").pack(side="left", padx=4)
        Button(actions, text="Status", command=self._atualizar_status, bg=self.button_color, fg="white").pack(side="left", padx=4)
        Button(actions, text="Prioridade", command=self._atualizar_prioridade, bg=self.warning_color, fg="white").pack(side="left", padx=4)
        Button(actions, text="Comentar", command=self._adicionar_comentario, bg=self.button_color, fg="white").pack(side="left", padx=4)
        Button(actions, text="Deletar", command=self._deletar_ticket, bg=self.danger_color, fg="white").pack(side="left", padx=4)

    def _refresh_list(self, *a):
        tickets = self.sistema.listar_tickets()
        self.listbox.delete(0, END)
        for t in tickets:
            display = f"{t.id} - {t.titulo} [{t.status}] ({t.prioridade})"
            self.listbox.insert(END, display)

    def _get_selected_id(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione um ticket")
            return None
        return self.listbox.get(sel[0]).split(" - ")[0].strip()

    def _novo_ticket(self):
        w = Toplevel(self.root)
        w.title("Novo Ticket")
        Label(w, text="Título").pack()
        titulo = Entry(w, width=60)
        titulo.pack()
        Label(w, text="Descrição").pack()
        desc = Text(w, width=60, height=6)
        desc.pack()
        prio_var = StringVar(value=PrioridadeEnum.MEDIA.name)
        OptionMenu(w, prio_var, *[p.name for p in PrioridadeEnum]).pack()
        Label(w, text="Categoria (opcional)").pack()
        categoria = Entry(w, width=40)
        categoria.pack()
        Label(w, text="Atribuir a (opcional)").pack()
        atrib = Entry(w, width=40)
        atrib.pack()

        def criar():
            t = titulo.get().strip()
            d = desc.get("1.0", END).strip()
            if not t or not d:
                messagebox.showerror("Erro", "Título e descrição são obrigatórios")
                return
            pr = prio_var.get()
            cat = categoria.get().strip() or None
            at = atrib.get().strip() or None
            self.sistema.criar_ticket(titulo=t, descricao=d, prioridade=pr, categoria=cat, atribuido_a=at)
            w.destroy()
            self._refresh_list()

        Button(w, text="Criar", command=criar).pack(pady=6)

    def _visualizar(self, *a):
        tid = self._get_selected_id()
        if not tid:
            return
        info = self.sistema.visualizar_ticket(tid)
        self.text.delete("1.0", END)
        self.text.insert(END, info)

    def _atribuir(self):
        tid = self._get_selected_id()
        if not tid:
            return
        nome = simpledialog.askstring("Atribuir", "Nome do usuário:")
        if nome:
            self.sistema.atribuir_ticket(tid, nome)
            self._refresh_list()

    def _atualizar_status(self):
        tid = self._get_selected_id()
        if not tid:
            return
        choices = [s.value for s in StatusEnum]
        novo = simpledialog.askstring("Status", f"Escolha status: {choices}")
        if novo and novo in choices:
            self.sistema.atualizar_status(tid, novo)
            self._refresh_list()
        else:
            messagebox.showinfo("Info", "Status inválido ou cancelado.")

    def _atualizar_prioridade(self):
        tid = self._get_selected_id()
        if not tid:
            return
        choices = [p.name for p in PrioridadeEnum]
        novo = simpledialog.askstring("Prioridade", f"Escolha prioridade: {choices}")
        if novo and novo in choices:
            self.sistema.atualizar_prioridade(tid, novo)
            self._refresh_list()
        else:
            messagebox.showinfo("Info", "Prioridade inválida ou cancelado.")

    def _adicionar_comentario(self):
        tid = self._get_selected_id()
        if not tid:
            return
        texto = simpledialog.askstring("Comentário", "Comentário:")
        if texto:
            self.sistema.adicionar_comentario(tid, texto)
            self._visualizar()

    def _deletar_ticket(self):
        tid = self._get_selected_id()
        if not tid:
            return
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o ticket {tid}?"):
            self.sistema.deletar_ticket(tid)
            self._refresh_list()
            self.text.delete("1.0", END)
            self.text.insert(END, "Ticket deletado.")

    def _gerar_relatorio(self):
        rel = self.sistema.gerar_relatorio_completo()
        w = Toplevel(self.root)
        w.title("Relatório")
        t = Text(w, width=100, height=30)
        t.pack()
        t.insert(END, rel)

    def _definir_usuario_campo(self, entry_field):
        nome = entry_field.get().strip()
        if nome:
            self.sistema.definir_usuario(nome)
            self.usuario_atual.set(f"👤 {nome}")
            entry_field.delete(0, END)
            messagebox.showinfo("Sucesso", f"Usuário atual: {nome}")

    def run(self):
        self.root.mainloop()


class InterfaceCLI:
    def __init__(self):
        self.sistema = SistemaTickets()
        self.usuario_atual = "admin"

    def exibir_menu_principal(self):
        print("""
╔════════════════════════════════════════════════════════════════╗
║          SISTEMA DE GERENCIAMENTO DE TICKETS                  ║
╠════════════════════════════════════════════════════════════════╣
║  1. Criar novo ticket
║  2. Listar tickets
║  3. Visualizar ticket
║  4. Atualizar status
║  5. Atualizar prioridade
║  6. Atribuir ticket
║  7. Adicionar comentário
║  8. Ver histórico
║  9. Gerar relatório
║  10. Definir usuário
║  0. Sair
╠════════════════════════════════════════════════════════════════╣
""")

    def criar_ticket_interativo(self):
        print("\n--- CRIAR NOVO TICKET ---")
        titulo = input("Título: ").strip()
        if not titulo:
            print("✗ Título não pode estar vazio")
            return
        descricao = input("Descrição: ").strip()
        if not descricao:
            print("✗ Descrição não pode estar vazia")
            return
        print("\nNíveis de Prioridade:")
        for i, p in enumerate(PrioridadeEnum, 1):
            print(f"  {i}. {p.name}")
        try:
            opcao_prioridade = int(input("Escolha a prioridade (1-4): "))
            prioridade = list(PrioridadeEnum)[opcao_prioridade - 1].name
        except (ValueError, IndexError):
            print("✗ Opção inválida. Usando prioridade MÉDIA")
            prioridade = PrioridadeEnum.MEDIA.name
        categoria = input("Categoria (opcional): ").strip() or None
        atribuido_a = input("Atribuir a (opcional): ").strip() or None
        ticket = self.sistema.criar_ticket(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            categoria=categoria,
            atribuido_a=atribuido_a
        )
        print(f"\n✓ Ticket criado: {ticket.id}")

    def listar_tickets_interativo(self):
        print("\n--- LISTAR TICKETS ---")
        print("1. Todos os tickets")
        print("2. Filtrar por status")
        print("3. Filtrar por prioridade")
        print("4. Filtrar por usuário")
        opcao = input("Escolha uma opção: ").strip()
        status_filter = None
        prioridade_filter = None
        usuario_filter = None
        if opcao == "2":
            print("\nStatus disponíveis:")
            for i, s in enumerate(StatusEnum, 1):
                print(f"  {i}. {s.value}")
            try:
                status_filter = list(StatusEnum)[int(input("Escolha o status: ")) - 1].value
            except (ValueError, IndexError):
                print("✗ Opção inválida")
                return
        elif opcao == "3":
            print("\nPrioridades disponíveis:")
            for i, p in enumerate(PrioridadeEnum, 1):
                print(f"  {i}. {p.name}")
            try:
                prioridade_filter = list(PrioridadeEnum)[int(input("Escolha a prioridade: ")) - 1].name
            except (ValueError, IndexError):
                print("✗ Opção inválida")
                return
        elif opcao == "4":
            usuario_filter = input("Nome do usuário: ").strip()
        tickets = self.sistema.listar_tickets(
            status=status_filter,
            prioridade=prioridade_filter,
            usuario=usuario_filter
        )
        if not tickets:
            print("✗ Nenhum ticket encontrado")
            return
        self._exibir_tabela_tickets(tickets)

    def _exibir_tabela_tickets(self, tickets):
        print("\n")
        print(f"{'ID':<10} {'Título':<30} {'Status':<15} {'Prioridade':<10} {'Atribuído':<15}")
        print("─" * 85)
        for ticket in tickets:
            titulo = ticket.titulo[:27] + "..." if len(ticket.titulo) > 30 else ticket.titulo
            atribuido = ticket.atribuido_a if ticket.atribuido_a else "N/A"
            print(f"{ticket.id:<10} {titulo:<30} {ticket.status:<15} {ticket.prioridade:<10} {atribuido:<15}")

    def visualizar_ticket_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        info = self.sistema.visualizar_ticket(ticket_id)
        print(info)

    def atualizar_status_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        print("\nStatus disponíveis:")
        for i, s in enumerate(StatusEnum, 1):
            print(f"  {i}. {s.value}")
        try:
            novo_status = list(StatusEnum)[int(input("Escolha o novo status: ")) - 1].value
            self.sistema.atualizar_status(ticket_id, novo_status)
        except (ValueError, IndexError):
            print("✗ Opção inválida")

    def atualizar_prioridade_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        print("\nPrioridades disponíveis:")
        for i, p in enumerate(PrioridadeEnum, 1):
            print(f"  {i}. {p.name}")
        try:
            nova_prioridade = list(PrioridadeEnum)[int(input("Escolha a nova prioridade: ")) - 1].name
            self.sistema.atualizar_prioridade(ticket_id, nova_prioridade)
        except (ValueError, IndexError):
            print("✗ Opção inválida")

    def atribuir_ticket_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        usuario = input("Nome do usuário: ").strip()
        if usuario:
            self.sistema.atribuir_ticket(ticket_id, usuario)
        else:
            print("✗ Nome do usuário não pode estar vazio")

    def adicionar_comentario_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        conteudo = input("Comentário: ").strip()
        if conteudo:
            self.sistema.adicionar_comentario(ticket_id, conteudo)
        else:
            print("✗ Comentário não pode estar vazio")

    def ver_historico_interativo(self):
        ticket_id = input("ID do ticket: ").strip().upper()
        historico = self.sistema.obter_historico(ticket_id)
        if not historico:
            print("✗ Nenhum histórico encontrado")
            return
        print(f"\n--- HISTÓRICO DO TICKET {ticket_id} ---")
        for entrada in historico:
            print(f"\n[{entrada['data']}]")
            print(f"  Usuário: {entrada['usuario']}")
            print(f"  Campo: {entrada['campo']}")
            print(f"  Valor Anterior: {entrada['valor_anterior']}")
            print(f"  Valor Novo: {entrada['valor_novo']}")
            print(f"  Descrição: {entrada['descricao']}")

    def gerar_relatorio_interativo(self):
        relatorio = self.sistema.gerar_relatorio_completo()
        print(relatorio)

    def definir_usuario_interativo(self):
        novo_usuario = input("Nome do usuário: ").strip()
        if novo_usuario:
            self.sistema.definir_usuario(novo_usuario)
            self.usuario_atual = novo_usuario
            print(f"✓ Usuário alterado para: {novo_usuario}")
        else:
            print("✗ Nome do usuário não pode estar vazio")

    def executar(self):
        print("\n╔════════════════════════════════════════════════════════════════╗")
        print("║    BEM-VINDO AO SISTEMA DE GERENCIAMENTO DE TICKETS          ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        while True:
            self.exibir_menu_principal()
            print(f"Usuário atual: {self.usuario_atual}\n")
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                self.criar_ticket_interativo()
            elif opcao == "2":
                self.listar_tickets_interativo()
            elif opcao == "3":
                self.visualizar_ticket_interativo()
            elif opcao == "4":
                self.atualizar_status_interativo()
            elif opcao == "5":
                self.atualizar_prioridade_interativo()
            elif opcao == "6":
                self.atribuir_ticket_interativo()
            elif opcao == "7":
                self.adicionar_comentario_interativo()
            elif opcao == "8":
                self.ver_historico_interativo()
            elif opcao == "9":
                self.gerar_relatorio_interativo()
            elif opcao == "10":
                self.definir_usuario_interativo()
            elif opcao == "0":
                print("\n✓ Até logo!")
                break
            else:
                print("✗ Opção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar...")


def executar_demo():
    """Executa uma demonstração do sistema"""
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║           DEMONSTRAÇÃO - SISTEMA DE TICKETS                   ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    sistema = SistemaTickets()
    print("📋 Criando tickets de exemplo...\n")
    sistema.definir_usuario("João Silva")
    ticket1 = sistema.criar_ticket(
        titulo="Erro na tela de login",
        descricao="Usuários relatando erro ao fazer login com redes sociais",
        prioridade=PrioridadeEnum.ALTA.name,
        categoria="Bug",
        atribuido_a="Maria Santos"
    )
    sistema.definir_usuario("Pedro Costa")
    ticket2 = sistema.criar_ticket(
        titulo="Implementar autenticação de dois fatores",
        descricao="Adicionar suporte a 2FA na plataforma",
        prioridade=PrioridadeEnum.MEDIA.name,
        categoria="Feature",
        atribuido_a="João Silva"
    )
    sistema.definir_usuario("Admin")
    ticket3 = sistema.criar_ticket(
        titulo="Backup do servidor caiu",
        descricao="Sistema de backup automático parou de funcionar",
        prioridade=PrioridadeEnum.CRITICA.name,
        categoria="Infraestrutura",
        atribuido_a="Carlos Lima"
    )
    print("\n📝 Realizando operações nos tickets...\n")
    sistema.definir_usuario("Maria Santos")
    sistema.atualizar_status(ticket1.id, StatusEnum.EM_ANDAMENTO.value)
    sistema.adicionar_comentario(ticket1.id, "Iniciando investigação do problema")
    sistema.definir_usuario("João Silva")
    sistema.atualizar_status(ticket2.id, StatusEnum.EM_ANDAMENTO.value)
    sistema.definir_usuario("Carlos Lima")
    sistema.atualizar_status(ticket3.id, StatusEnum.EM_ANDAMENTO.value)
    sistema.adicionar_comentario(ticket3.id, "Iniciando reparo urgente")
    sistema.atualizar_status(ticket3.id, StatusEnum.RESOLVIDO.value)
    print("\n\n" + sistema.visualizar_ticket(ticket1.id))
    print("\n" + sistema.gerar_relatorio_completo())
    print("\n✓ Demonstração concluída!")
    print("Para acessar a interface gráfica, reinicie a aplicação!\n")


def launch_public_submit():
    """Abre uma janela simples para o público abrir um chamado (modo limit)
    Não mostra listagens ou controles administrativos: apenas cria um ticket."""
    sistema = SistemaTickets()
    root = Tk()
    root.title("Abrir Chamado - TicketFlow")
    root.geometry("520x420")

    Label(root, text="Abrir Novo Chamado", font=("Helvetica", 14, "bold")).pack(pady=8)

    Label(root, text="Nome (opcional):").pack(anchor="w", padx=12)
    nome_entry = Entry(root)
    nome_entry.pack(fill="x", padx=12, pady=4)

    Label(root, text="Título:").pack(anchor="w", padx=12)
    titulo_entry = Entry(root)
    titulo_entry.pack(fill="x", padx=12, pady=4)

    Label(root, text="Descrição:").pack(anchor="w", padx=12)
    desc_text = Text(root, height=8)
    desc_text.pack(fill="both", padx=12, pady=4, expand=True)

    Label(root, text="Prioridade:").pack(anchor="w", padx=12)
    prio_var = StringVar(value=PrioridadeEnum.MEDIA.name)
    OptionMenu(root, prio_var, *[p.name for p in PrioridadeEnum]).pack(padx=12, pady=4)

    Label(root, text="Categoria (opcional):").pack(anchor="w", padx=12)
    cat_entry = Entry(root)
    cat_entry.pack(fill="x", padx=12, pady=4)

    def enviar():
        titulo = titulo_entry.get().strip()
        descricao = desc_text.get("1.0", END).strip()
        if not titulo or not descricao:
            messagebox.showerror("Erro", "Título e descrição são obrigatórios")
            return
        nome = nome_entry.get().strip() or None
        prioridade = prio_var.get()
        categoria = cat_entry.get().strip() or None
        if nome:
            sistema.definir_usuario(nome)
        sistema.criar_ticket(titulo=titulo, descricao=descricao, prioridade=prioridade, categoria=categoria)
        messagebox.showinfo("Sucesso", "Chamado enviado com sucesso. Obrigado!")
        root.destroy()

    Button(root, text="Enviar Chamado", bg="#27ae60", fg="white", command=enviar).pack(pady=10)
    root.mainloop()


def launch_admin_view():
    """Atalho para abrir a interface administrativa completa (mesma InterfaceGUI)."""
    app = InterfaceGUI()
    app.run()


def menu_principal():
    """Menu principal com opções para usuário"""
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                    TICKETFLOW - MENU PRINCIPAL                 ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    print("Bem-vindo ao TicketFlow - Sistema de Gerenciamento de Chamados!\n")
    print("1. 🎫 Abrir Interface Gráfica (RECOMENDADO)")
    print("2. 💻 Usar Interface de Linha de Comando (CLI)")
    print("3. 📋 Executar Demonstração")
    print("4. ❌ Sair\n")
    
    while True:
        try:
            opcao = input("Escolha uma opção (1-4): ").strip()
            if opcao == "1":
                print("\n🚀 Iniciando interface gráfica...\n")
                app = InterfaceGUI()
                app.run()
                break
            elif opcao == "2":
                print("\n💻 Iniciando interface CLI...\n")
                interface_cli = InterfaceCLI()
                interface_cli.executar()
                break
            elif opcao == "3":
                executar_demo()
                break
            elif opcao == "4":
                print("\n👋 Até logo!")
                sys.exit(0)
            else:
                print("❌ Opção inválida! Tente novamente.")
        except KeyboardInterrupt:
            print("\n\n👋 Aplicação encerrada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            executar_demo()
        elif len(sys.argv) > 1 and sys.argv[1] == "--cli":
            interface_cli = InterfaceCLI()
            interface_cli.executar()
        else:
            menu_principal()
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        sys.exit(1)
    
