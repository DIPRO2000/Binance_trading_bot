import typer
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.orders import execute_order
from rich.console import Console
from rich.table import Table

# Initialize core configurations
load_dotenv()
setup_logging()

app = typer.Typer(help="Interactive Binance Futures Testnet Trading CLI Bot")
console = Console()

@app.command()
def place_order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair asset symbol, e.g., BTCUSDT"),
    side: str = typer.Option(..., "--side", "-d", help="Execution direction: BUY or SELL"),
    order_type: str = typer.Option(..., "--order-type", "-t", help="Execution method: MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="The volume/amount of asset to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Target entry price (Required for LIMIT and STOP_LIMIT orders)"),
    stop_price: float = typer.Option(None, "--stop-price", "-x", help="Trigger activation threshold price (Required for STOP_LIMIT orders)")
):
    """
    Validates and executes algorithmic crypto orders via terminal flags.
    """
    # 1. Input Constraints Validation
    try:
        validate_inputs(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as err:
        console.print(f"[bold red]❌ Input Validation Error:[/bold red] {err}")
        return

    # 2. Inform User of Initialization State
    console.print(f"[yellow]⏳ Dispatching {order_type} {side} execution layer for {quantity} {symbol}...[/yellow]")
    
    # 3. Fire Pipeline Execution
    result = execute_order(symbol, side, order_type, quantity, price, stop_price)

    # 4. Handle Visual Responses
    if result["success"]:
        data = result["data"]
        console.print("[bold green]✔ Execution Request Successfully Transmitted to Exchange![/bold green]")
        
        # Render clean data table layout for user review
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