import click
from master import start_master
from node import start_node


@click.group()
def cli():
    pass


@cli.command()
def version() -> None:
    """Returns version information"""
    click.echo("v0.0.1")


@cli.command()
def master() -> None:
    """Runs the master daemon"""
    click.echo("Hello from master")
    start_master()


@cli.command()
def node() -> None:
    """Runs the node daemon"""
    click.echo("Hello from node")
    start_node()


if __name__ == "__main__":
    cli()
