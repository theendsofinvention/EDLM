# coding=utf-8



from .aliases import process_aliases
from .images import process_images
from .._context import Context


def process_markdown(ctx: Context):

    ctx.debug(f'processing markdown file: {ctx.index_file}')
    ctx.markdown_text = ctx.index_file.read_text(encoding='utf8')
    process_aliases(ctx)
    process_images(ctx)
