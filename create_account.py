from main import UserManager
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, messagebox

um = UserManager()

def launch_register():
    root = Tk()
    root.title("Criar Conta - TicketFlow")
    root.geometry("420x220")

    Label(root, text="Criar Nova Conta", font=("Helvetica", 14, "bold")).pack(pady=8)
    Label(root, text="Usuário:").pack(anchor='w', padx=12)
    user_entry = Entry(root)
    user_entry.pack(fill='x', padx=12, pady=4)

    Label(root, text="Senha:").pack(anchor='w', padx=12)
    pass_entry = Entry(root, show='*')
    pass_entry.pack(fill='x', padx=12, pady=4)

    def criar():
        u = user_entry.get().strip()
        p = pass_entry.get().strip()
        if not u or not p:
            messagebox.showerror("Erro", "Usuário e senha são obrigatórios")
            return
        ok = um.create_user(u, p, role='user')
        if ok:
            messagebox.showinfo("Sucesso", "Conta criada com sucesso")
            root.destroy()
        else:
            messagebox.showerror("Erro", "Usuário já existe ou nome inválido")

    Button(root, text="Criar Conta", command=criar, bg="#27ae60", fg="white").pack(pady=10)
    root.mainloop()

if __name__ == '__main__':
    launch_register()
