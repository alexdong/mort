import click

from mort.driver import download_latest_target_list
from mort.local_conf import TARGETS
from mort.target_matcher import matches


@click.group()
@click.option('--target_filter')
@click.option('--url_filter')
@click.pass_context
def cli(ctx, target_filter, url_filter):
    ctx.obj = {"target_filter": target_filter, "urls": url_filter}


@cli.command()
@click.pass_obj
def show(ctx_obj):
    print([target for target in TARGETS if matches(ctx_obj['target_filter'], target)])


@cli.command()
def update():
    print("Downloading the latest device and OS support list from BrowserStack ...")
    download_latest_target_list("./targets.json")
