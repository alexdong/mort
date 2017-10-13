# pragma: no cover

import json

import click

from mort import controller
from mort.driver import download_latest_target_list
from mort.file_utils import get_git_hash
from mort.local_conf import TARGETS, PATHS, TARGET_LIST_FILE_PATH


@click.group()
@click.option('--targets', default=json.dumps(TARGETS))
@click.option('--paths', default=json.dumps(PATHS))
@click.option('--git-hash', default=get_git_hash())
@click.pass_context
def cli(ctx, targets, paths, git_hash):
    ctx.obj = {"targets": json.loads(targets), "paths": json.loads(paths), "git_hash": git_hash}


@cli.command()
@click.pass_obj
def capture(ctx):
    controller.capture(ctx.obj['paths'], ctx.obj['urls'], ctx.obj['git_hash'])


@cli.command()
@click.pass_obj
@click.argument('ref-git-hash')
def compare(ctx, ref_git_hash):
    controller.compare(ctx.obj['paths'], ctx.obj['urls'], ctx.obj['git_hash'], ref_git_hash)


@cli.command()
@click.option('--save-as', default=TARGET_LIST_FILE_PATH)
def update(save_as):
    print("Downloading the latest device and OS support list from BrowserStack ...")
    download_latest_target_list(save_as)
