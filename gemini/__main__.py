import click


@click.group()
def cli():
    pass


@click.command()
def version() -> None:
    """Returns version information"""
    click.echo("v0.0.1")


@click.command()
def node() -> None:
    """Runs the node daemon"""
    click.echo("Hello from node")


if __name__ == "__main__":
    cli.add_command(version)
    cli.add_command(node)
    cli()
