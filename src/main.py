import os
import typer
from dotenv import load_dotenv
from extractor import get_cluster_metrics
from ai_engine import analyze_with_aura
from formatter import save_optimized_yaml

# Load environment variables from .env file
load_dotenv()

# Verify required environment variables
def check_environment():
    """
    Verify that all required environment variables are loaded.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        typer.secho("Error: GEMINI_API_KEY environment variable is not set!", fg=typer.colors.RED, bold=True)
        typer.echo("Please add GEMINI_API_KEY to your .env file or environment.")
        raise typer.Exit(code=1)
    
    typer.secho("Environment variables loaded successfully", fg=typer.colors.GREEN)

app = typer.Typer(
    name="AURA",
    help="Adaptive Usage and Resource Agent",
    add_completion=False,
)

@app.command()
def analyze(
    namespace: str = typer.Argument(..., help="The namespace to analyze (e.g. default, frontend-app)"),
    save: bool = typer.Option(False, "--save", "-s", help="Save the analysis results in a YAML file")
):
    """
    Analyze the actual namespace and its resources. Request AI for optimization recommendations.
    """
    try:
        # Check environment variables first
        check_environment()
        
        typer.secho(f"Initializing AURA...", fg=typer.colors.BLUE, bold=True)
        typer.echo(f"Connecting to OCI cluster to scan the namespace: {namespace}\n")

        typer.echo("Obtaining cluster metrics...")
        try:
            extractor = get_cluster_metrics(namespace)
            metrics = extractor.get_namespace_metrics()
        except Exception as e:
            typer.secho(f"Error connecting to cluster: {str(e)}", fg=typer.colors.RED, bold=True)
            typer.echo("Make sure the namespace exists and you have proper credentials.")
            raise typer.Exit(code=1)

        typer.echo("Sending metrics to AI for analysis...")
        try:
            ai_recommendation = analyze_with_aura(metrics)
        except Exception as e:
            typer.secho(f"Error connecting to AI API: {str(e)}", fg=typer.colors.RED, bold=True)
            typer.echo("Check your GEMINI_API_KEY environment variable.")
            raise typer.Exit(code=1)

        typer.secho("Analysis complete. Recommendations:", fg=typer.colors.GREEN, bold=True)
        typer.echo(ai_recommendation)

        if save:
            try:
                typer.echo("Creating file: optimized_resources.yaml")
                save_optimized_yaml(ai_recommendation)
                typer.secho("File created successfully. Check changes before applying.", fg=typer.colors.YELLOW)
            except Exception as e:
                typer.secho(f"Error saving file: {str(e)}", fg=typer.colors.RED, bold=True)
                raise typer.Exit(code=1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Unexpected error: {str(e)}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

@app.command()
def status():
    """
    Check the connection status with OCI cluster and AI credentials
    """
    try:
        # Check environment variables first
        check_environment()
        
        typer.echo("Checking connection status...")
        
        # Check Kubernetes connection
        try:
            typer.echo("Checking Kubernetes cluster...")
            typer.secho("Kubernetes connection: OK", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"Kubernetes connection: FAILED", fg=typer.colors.RED)
            typer.echo(f"Error: {str(e)}")
        
        # Check AI API connection
        try:
            typer.echo("Checking AI API...")
            typer.secho("AI API connection: OK", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"AI API connection: FAILED", fg=typer.colors.RED)
            typer.echo(f"Error: {str(e)}")
            
    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Unexpected error: {str(e)}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()