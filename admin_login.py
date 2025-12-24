from main import UserManager, launch_admin_view

def run_cli_login():
    um = UserManager()
    print("== Login de Administrador ==")
    user = input("Usuário: ").strip()
    pwd = input("Senha: ").strip()
    u = um.authenticate(user, pwd)
    if not u:
        print("Credenciais inválidas")
        return
    if u.role != 'admin':
        print("Acesso negado: usuário não é administrador")
        return
    print("Login bem-sucedido. Abrindo painel administrativo...")
    launch_admin_view()

if __name__ == '__main__':
    run_cli_login()
