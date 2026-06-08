import os
from dotenv import load_dotenv, set_key
from rich.prompt import Prompt
from rich.console import Console

console = Console()

#Used for first-time setup and configuration of .env credentials if not already present. 
def ensure_env_configured():

    env_path = ".env"
    
    load_dotenv(env_path)
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        console.print("\n[bold yellow]⚠️ First-Time Configuration Detected[/bold yellow]")
        console.print("[dim]Your Binance Futures Testnet credentials are missing. Let's configure them now.[/dim]\n")
        
        input_key = Prompt.ask("[bold cyan]Enter your BINANCE_API_KEY[/bold cyan]")
        input_secret = Prompt.ask("[bold cyan]Enter your BINANCE_API_SECRET[/bold cyan]")
        
        if not input_key.strip() or not input_secret.strip():
            console.print("[bold red]❌ Keys cannot be empty. Initialization aborted.[/bold red]")
            raise SystemExit
            
        set_key(env_path, "BINANCE_API_KEY", input_key.strip())
        set_key(env_path, "BINANCE_API_SECRET", input_secret.strip())
        
        load_dotenv(env_path)
        console.print("[bold green]✔ Credentials saved successfully to .env! Proceeding...[/bold green]\n")