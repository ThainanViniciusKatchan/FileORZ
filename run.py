from ui.index import on_app


if __name__ == "__main__":
    try:
        on_app()
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar o aplicativo: {e}")
    finally:
        print("Aplicativo encerrado.")
