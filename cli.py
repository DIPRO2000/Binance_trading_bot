import typer
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.orders import execute_order
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

load_dotenv()
setup_logging()

app = typer.Typer(help="Interactive Binance Futures Testnet Trading CLI Bot")
console = Console()

def run_interactive_wizard():
    
    console.clear()
    console.print(Panel.fit(
        "[bold dynamic_magenta]🚀 Binance Futures Trading Wizard[/bold dynamic_magenta]\n"
        "[dim]Follow the prompts below to safely configure and execute your trade.[/dim]",
        border_style="cyan"
    ))

    console.print("\n[bold cyan][1] Select Crypto Asset Pair[/bold cyan]")
    symbol_choice = Prompt.ask(
        "Enter trading pair symbol or choose common options", 
        choices=["BTCUSDT", "ETHUSDT", "SOLUSDT"], 
        default="BTCUSDT"
    ).upper()

    console.print("\n[bold cyan][2] Select Order Direction[/bold cyan]")
    console.print("[green]BUY[/green]  -> Bet the price goes UP (Long)")
    console.print("[red]SELL[/red] -> Bet the price goes DOWN (Short)")
    side_choice = Prompt.ask("Choose your position side", choices=["BUY", "SELL"]).upper()

    console.print("\n[bold cyan][3] Select Order Execution Type[/bold cyan]")
    console.print("[magenta]MARKET[/magenta]     -> Execute immediately at the best current price")
    console.print("[magenta]LIMIT[/magenta]      -> Wait on the book until the market hits your target price")
    console.print("[magenta]STOP_LIMIT[/magenta] -> Advanced conditional order with a trigger/activation price")
    type_choice = Prompt.ask("Choose order type", choices=["MARKET", "LIMIT", "STOP_LIMIT"]).upper()

    console.print("\n[bold cyan][4] Enter Position Size[/bold cyan]")
    qty_choice = Prompt.ask("How much crypto volume do you want to trade? (e.g., 0.001)")
    try:
        qty_choice = float(qty_choice)
    except ValueError:
        qty_choice = 0.0  

    price_choice = None
    stop_price_choice = None

    if type_choice in ["LIMIT", "STOP_LIMIT"]:
        console.print(f"\n[bold cyan][5] Set Execution Target Price[/bold cyan]")
        p_input = Prompt.ask(f"At what specific asset price should this order execute?")
        try:
            price_choice = float(p_input)
        except ValueError:
            price_choice = 0.0

    if type_choice == "STOP_LIMIT":
        console.print(f"\n[bold cyan][6] Set Stop Activation Trigger Price[/bold cyan]")
        s_input = Prompt.ask("What market activation price triggers this limit order to sit on the books?")
        try:
            stop_price_choice = float(s_input)
        except ValueError:
            stop_price_choice = 0.0

    console.print("\n")
    console.print(Panel(
        f"[bold yellow]⚠️ Confirm Your Trade Setup[/bold yellow]\n\n"
        f"• [bold]Asset Pair:[/bold] {symbol_choice}\n"
        f"• [bold]Direction:[/bold] {side_choice}\n"
        f"• [bold]Order Type:[/bold] {type_choice}\n"
        f"• [bold]Quantity:[/bold] {qty_choice} units\n"
        f"• [bold]Target Price:[/bold] {price_choice if price_choice else 'Market Price'}\n"
        f"• [bold]Trigger Price:[/bold] {stop_price_choice if stop_price_choice else 'None'}",
        title="Pre-Flight Safety Check",
        border_style="yellow"
    ))
    
    confirm = Prompt.ask("Do you want to send this order to the exchange?", choices=["y", "n"], default="n")
    if confirm.lower() != 'y':
        console.print("[bold red]❌ Order canceled by user.[/bold red]")
        return None, None, None, None, None, None

    return symbol_choice, side_choice, type_choice, qty_choice, price_choice, stop_price_choice


@app.command()
def place_order(
    symbol: str = typer.Option(None, "--symbol", "-s", help="Trading pair asset symbol, e.g., BTCUSDT"),
    side: str = typer.Option(None, "--side", "-d", help="Execution direction: BUY or SELL"),
    order_type: str = typer.Option(None, "--order-type", "-t", help="Execution method: MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(None, "--quantity", "-q", help="The volume/amount of asset to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Target entry price (Required for LIMIT and STOP_LIMIT orders)"),
    stop_price: float = typer.Option(None, "--stop-price", "-x", help="Trigger activation threshold price (Required for STOP_LIMIT orders)")
):

    if symbol is None or side is None or order_type is None or quantity is None:
        symbol, side, order_type, quantity, price, stop_price = run_interactive_wizard()
        if symbol is None: 
            return

    try:
        validate_inputs(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as err:
        console.print(f"[bold red]❌ Input Validation Error:[/bold red] {err}")
        return

    console.print(f"[yellow]⏳ Dispatching {order_type} {side} execution layer for {quantity} {symbol}...[/yellow]")
    
    result = execute_order(symbol, side, order_type, quantity, price, stop_price)

    if result["success"]:
        data = result["data"]
        console.print("[bold green]✔ Execution Request Successfully Transmitted to Exchange![/bold green]")
        
        table = Table(title="Order Execution Summary Statement", show_lines=True)
        table.add_column("Key Metric Reference", style="cyan", no_wrap=True)
        table.add_column("Exchange Value Output", style="magenta")
        
        table.add_row("Order Identification Unique ID", str(data.get("orderId")))
        table.add_row("Transaction Target Status", str(data.get("status")))
        table.add_row("Client Context Symbol Pair", str(data.get("symbol")))
        table.add_row("Executed Context Filled Qty", str(data.get("executedQty", "0.0000")))
        table.add_row("Average Filled Processing Price", str(data.get("avgPrice", "N/A")))
        
        if order_type.upper() == "STOP_LIMIT":
            table.add_row("Conditional Trigger Activation Price", str(data.get("stopPrice", stop_price)))
            
        console.print(table)
    else:
        console.print(f"[bold red]❌ Exchange Reject Error Flagged:[/bold red] {result['error']}")

if __name__ == "__main__":
    app()