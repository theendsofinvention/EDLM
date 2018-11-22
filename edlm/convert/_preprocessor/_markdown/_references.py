# coding=utf-8
"""
Processes references in the Markdown text
"""

from edlm.convert._context import Context

REFS_TEMPLATE = r"""
\newpage
# References
{}
"""


class Reference:
    """
    Represents a reference in the document
    """

    def __init__(self, raw_ref: str, abbrev: str) -> None:
        self._abbrev = abbrev
        self._raw_ref = raw_ref
        try:
            self._name = raw_ref.split(',')[0].lstrip().rstrip()
            self._link = raw_ref.split(',')[1].lstrip().rstrip()
        except IndexError:
            raise ValueError(f'reference badly formatted in "settings.yml": {abbrev}\n')

    @property
    def abbrev(self) -> str:
        """
        Returns: reference's abbreviation
        """
        return self._abbrev

    @property
    def name(self) -> str:
        """
        Returns: reference's name
        """
        return self._name

    @property
    def link(self) -> str:
        """
        Returns: reference's link
        """
        return self._link

    def to_latex(self) -> str:
        """
        Returns: convert reference to Latex text
        """
        return f'\\href{{{self.link}}}{{{self.name}}}'

    def to_markdown(self) -> str:
        """
        Returns: convert reference to Markdown text
        """
        return f'[{self.name}]({self.link})'

    def __hash__(self):
        return hash(self.abbrev)

    def __repr__(self) -> str:
        return self.name


def process_references(ctx: Context):
    """
    Processes references in the Markdown text

    Args:
        ctx: Context
    """
    ctx.latex_refs = list()
    for abbrev, raw_ref in ctx.settings.references.items():
        if abbrev in ctx.markdown_text:
            ref = Reference(raw_ref, abbrev)
            ctx.latex_refs.append(ref.to_latex())
            ctx.markdown_text = ctx.markdown_text.replace(abbrev, ref.to_markdown())
            ctx.debug(f'used reference: {abbrev}')
    ctx.latex_refs = sorted(ctx.latex_refs)
