import os
import logging
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.logging import RichHandler
from rich.markdown import Markdown
from graph.workflow import run_workflow

# Load environment variables
load_dotenv()

# Configure Logging with Rich
logging.basicConfig(
    level=logging.WARNING, # Only show warnings or higher for a clean CLI
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("MAS_LifeAssistant")
console = Console()

def display_reasoning(state: dict):
    """Formats and prints the reasoning steps from the agent state."""
    console.print("\n[bold cyan]─── Reasoning Steps ───[/bold cyan]")
    
    # Intent
    intent = state.get("intent_category") or "Unknown"
    console.print(f"[bold blue]Intent Categorized:[/bold blue] {intent}")
    
    # Memories
    memories = state.get("memories", [])
    if memories:
        console.print("[bold magenta]Found relevant memories:[/bold magenta]")
        for m in memories:
            console.print(f" • {m}")
    else:
        console.print("[dim magenta]No relevant memories found.[/dim magenta]")
        
    # Search
    if state.get("search_needed"):
        query = state.get("search_query")
        console.print(f"[bold yellow]Executed search for:[/bold yellow] {query}")
        if state.get("external_context"):
            console.print(f"[dim grey]Search context snippet: {state['external_context'][:100]}...[/dim grey]")
    
    # Critic
    if not state.get("is_valid"):
        console.print("[bold red]Critic rejected first pass:[/bold red]")
        console.print(f"[italic red]{state.get('critic_feedback')}[/italic red]")
        console.print(f"[dim]Total revisions: {state.get('revision_count', 0)}[/dim]")

    console.print("[bold cyan]───────────────────────[/bold cyan]\n")

def main():
    """Main CLI entry point."""
    console.print(Panel.fit(
        "[bold green]Welcome to MAS Life Assistant[/bold green]\n"
        "[italic]Your personal agentic decision engine[/italic]",
        border_style="bright_blue"
    ))

    user_id = os.getenv("USER_ID", "phoenix_user")
    
    while True:
        try:
            # Get user query
            query = console.input("[bold yellow]Query (type 'exit' to quit): [/bold yellow]")
            
            if query.lower() in ["exit", "quit", "q"]:
                console.print("[bold blue]Goodbye![/bold blue]")
                break
                
            if not query.strip():
                continue

            with console.status("[bold green]Agent is thinking...", spinner="dots"):
                # Run the workflow
                final_state = run_workflow(query, user_id=user_id)

            # Display reasoning
            display_reasoning(final_state)
            
            # Display final decision
            decision = final_state.get("decision", "No decision made.")
            console.print(Panel(
                Markdown(decision),
                title="[bold green]Final Agent Decision[/bold green]",
                expand=False,
                border_style="green"
            ))
            
            # Display insights
            insights = final_state.get("insights", [])
            if insights:
                console.print("[bold cyan]Key Insights Captured:[/bold cyan]")
                for insight in insights:
                    console.print(f" ✓ {insight}")
            
            console.print("\n" + "─" * 40 + "\n")

        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")
            logger.exception("Details:")

if __name__ == "__main__":
    main()
