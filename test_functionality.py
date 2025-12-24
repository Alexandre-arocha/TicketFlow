#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🧪 Teste de Funcionalidade do TicketFlow
Valida se todos os módulos e funcionalidades funcionam corretamente
"""

import sys
import os

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("\n" + "="*60)
    print("🧪 TESTE 1: Importar Módulos")
    print("="*60)
    
    try:
        # Projeto foi consolidado em `main.py` — importar a partir de lá
        from main import (
            Ticket,
            PrioridadeEnum,
            StatusEnum,
            GerenciadorDados,
            SistemaTickets,
            InterfaceCLI,
            InterfaceGUI,
        )
        print("✅ Importado de main.py")
        print("\n✅ Todos os módulos foram importados com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")
        return False

def test_ticket_creation():
    """Testa criação de tickets"""
    print("\n" + "="*60)
    print("🧪 TESTE 2: Criar Tickets")
    print("="*60)
    
    try:
        from main import SistemaTickets, PrioridadeEnum
        
        # Usar arquivo temporário para teste
        test_file = "test_tickets.json"
        sistema = SistemaTickets(test_file)
        sistema.definir_usuario("Teste User")
        
        # Criar ticket
        ticket = sistema.criar_ticket(
            titulo="Ticket de Teste",
            descricao="Descrição de teste",
            prioridade=PrioridadeEnum.MEDIA.name,
            categoria="Teste"
        )
        
        print(f"✅ Ticket criado: {ticket.id}")
        
        # Listar
        tickets = sistema.listar_tickets()
        print(f"✅ Total de tickets: {len(tickets)}")
        
        # Limpar arquivo de teste
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar ticket: {e}")
        return False

def test_tkinter():
    """Testa se tkinter está disponível"""
    print("\n" + "="*60)
    print("🧪 TESTE 3: Verificar Tkinter")
    print("="*60)
    
    try:
        import tkinter
        print("✅ tkinter disponível")
        
        # Verificar versão
        version = tkinter.TkVersion
        print(f"✅ Versão Tk: {version}")
        
        return True
    except ImportError:
        print("❌ tkinter não está instalado")
        print("   Dica: Reinstale Python com tkinter incluído")
        return False

def test_json_persistence():
    """Testa persistência em JSON"""
    print("\n" + "="*60)
    print("🧪 TESTE 4: Persistência JSON")
    print("="*60)
    
    try:
        from main import SistemaTickets, PrioridadeEnum, StatusEnum
        
        test_file = "test_persistence.json"
        
        # Criar e salvar
        sistema1 = SistemaTickets(test_file)
        sistema1.definir_usuario("User 1")
        ticket = sistema1.criar_ticket(
            titulo="Teste Persistência",
            descricao="Teste",
            prioridade=PrioridadeEnum.ALTA.name
        )
        ticket_id = ticket.id
        
        print(f"✅ Ticket salvo: {ticket_id}")
        
        # Carregar em nova instância
        sistema2 = SistemaTickets(test_file)
        loaded_ticket = sistema2.gerenciador.obter_ticket(ticket_id)
        
        if loaded_ticket and loaded_ticket.titulo == "Teste Persistência":
            print("✅ Dados recuperados corretamente")
        else:
            raise Exception("Dados não foram recuperados")
        
        # Limpar
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"❌ Erro de persistência: {e}")
        return False

def test_status_operations():
    """Testa operações de status"""
    print("\n" + "="*60)
    print("🧪 TESTE 5: Operações de Status")
    print("="*60)
    
    try:
        from main import SistemaTickets, StatusEnum, PrioridadeEnum
        
        test_file = "test_status.json"
        sistema = SistemaTickets(test_file)
        sistema.definir_usuario("Test User")
        
        # Criar ticket
        ticket = sistema.criar_ticket(
            titulo="Teste Status",
            descricao="Teste",
            prioridade=PrioridadeEnum.MEDIA.name
        )
        
        # Testar diferentes status
        for status in StatusEnum:
            sistema.atualizar_status(ticket.id, status.value)
            print(f"✅ Status alterado para: {status.value}")
        
        # Limpar
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar status: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🎫 TICKETFLOW - TESTE DE FUNCIONALIDADE")
    print("="*60)
    
    results = []
    
    # Executar testes
    results.append(("Importar Módulos", test_imports()))
    results.append(("Criar Tickets", test_ticket_creation()))
    results.append(("Tkinter", test_tkinter()))
    results.append(("Persistência JSON", test_json_persistence()))
    results.append(("Operações de Status", test_status_operations()))
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:30} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ TicketFlow está pronto para uso\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        print("❌ Revise os erros acima\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
