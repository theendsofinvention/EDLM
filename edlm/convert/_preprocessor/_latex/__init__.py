# coding=utf-8
"""
Processes Latex template
"""
import pprint
from pathlib import Path

import elib
from jinja2 import BaseLoader, Environment, TemplateNotFound

from edlm.convert._context import Context
from edlm.convert._preprocessor._latex._abstract import ABSTRACT
from edlm.convert._preprocessor._latex._empty_page import EMPTY_PAGE
from edlm.convert._preprocessor._latex._title_page import TITLE_PAGE


def _get_template_source(ctx: Context) -> Path:
    if ctx.template_source:
        return ctx.template_source

    raise ValueError('ctx.template_source is undefined')


class TexTemplateLoader(BaseLoader):
    """
    Loads the template for Jinja2
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    def get_source(self, environment, template):
        # noinspection SpellCheckingInspection
        """
        Get the template source, filename and reload helper for a template.
        It's passed the environment and template name and has to return a
        tuple in the form ``(source, filename, uptodate)`` or raise a
        `TemplateNotFound` error if it can't locate the template.

        The source part of the returned tuple must be the source of the
        template as unicode string or a ASCII bytestring.  The filename should
        be the name of the file on the filesystem if it was loaded from there,
        otherwise `None`.  The filename is used by python for the tracebacks
        if no loader extension is used.

        The last item in the tuple is the `uptodate` function.  If auto
        reloading is enabled it's always called to check if the template
        changed.  No arguments are passed so the function must store the
        old state somewhere (for example in a closure).  If it returns `False`
        the template will be reloaded.
        """
        self.ctx.debug(f'environment: {pprint.pformat(environment)}')
        self.ctx.debug(f'template: {template}')
        if not self.ctx.template_source.exists():
            raise TemplateNotFound(str(self.ctx.template_source))
        source = self.ctx.template_source.read_text(encoding='utf8')
        # "False" here means always reload the template
        return source, self.ctx.template_source.absolute(), False


def _get_jinja_env(ctx: Context):
    return Environment(  # nosec
        block_start_string=r'\BLOCK{',
        block_end_string=r'}',
        variable_start_string=r'\VAR{',
        variable_end_string=r'}',
        comment_start_string=r'\#{',
        comment_end_string=r'}',
        line_statement_prefix=r'%%',
        line_comment_prefix=r'%#',
        trim_blocks=True,
        autoescape=False,
        loader=TexTemplateLoader(ctx)
    )


def process_latex(ctx: Context):
    """
    Processes the Tex template

    Adds path the media folders
    """
    ctx.debug(f'processing Tex template file: {ctx.template_source}')

    try:
        elib.path.ensure_file(ctx.template_source)
    except FileNotFoundError:
        ctx.error(f'LaTeX template not found: "{ctx.template_source}"')
        raise

    jinja_env = _get_jinja_env(ctx)

    _media_folders_raw = [folder.absolute() for folder in ctx.media_folders]
    _media_folders_sanitized = [str(folder).replace('\\', '/') for folder in _media_folders_raw]
    media_folders = ''.join(f'{{{folder}/}}' for folder in _media_folders_sanitized)
    ctx.debug(f'adding media folders to template: {media_folders}')
    empty_page = EMPTY_PAGE  # pylint: disable=possibly-unused-variable
    # abstract = ABSTRACT  # pylint: disable=possibly-unused-variable
    title_page = TITLE_PAGE  # pylint: disable=possibly-unused-variable
    template_source = _get_template_source(ctx)
    try:
        template = jinja_env.get_template(template_source.name)
        ctx.template_file.write_text(template.render(**locals()), encoding='utf8')
    except TemplateNotFound:
        ctx.error(f'template not found: {template_source.absolute()}')
        raise
