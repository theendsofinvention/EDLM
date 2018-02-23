# coding=utf-8
"""
Latex abstract
"""

_parbox = r'\parbox[t]{10cm}'
_color = r'\color{gray}'
_changes = r'$for(summary_of_changes)$ $summary_of_changes$ \vspace{2mm} \\ $endfor$'
_applies = r'$for(applies)$ \textbf{$applies$} \\ $endfor$'
_spacing = r'\null'

# noinspection SpellCheckingInspection
ABSTRACT = rf"""
$if(applies)$
    \thispagestyle{{empty}}
    \null
    \vfill
    \begin{{minipage}}{{\textwidth}}
        \begin{{center}}
            \begin{{tabular}}{{ r l }}

                {{{_color}APPLIES TO:}}
                & {_parbox}{{{_applies}}} \\

                {_spacing} \\

                $if(type)$
                {{{_color}TYPE:}}
                & {_parbox}{{\textbf{{$type$}}}} \\

                {_spacing} \\
                $endif$

                $if(version)$
                {{{_color}VERSION:}}
                & {_parbox}{{$version$}} \\

                {_spacing} \\
                $endif$

                $if(audience)$
                {{{_color}INTENDED AUDIENCE:}}
                & {_parbox}{{$audience$}} \\

                {_spacing} \\
                $endif$

                $if(status)$
                {{{_color}STATUS:}}
                & {_parbox}{{$status$}} \\

                {_spacing} \\
                $endif$

                $if(published_date)$
                {{{_color}PUBLISHED DATE:}}
                & {_parbox}{{$published_date$}} \\

                {_spacing} \\
                $endif$

                $if(responsible)$
                {{{_color}DOCUMENT RESPONSIBLE:}}
                & {_parbox}{{$responsible$}} \\

                {_spacing} \\
                $endif$

                $if(summary_of_changes)$
                {{{_color}SUMMARY OF CHANGES:}}
                & {_parbox}{{{_changes}}} \\

                {_spacing} \\
                $endif$

            \end{{tabular}}
        \end{{center}}
    \end{{minipage}}
    \vfill
$endif$
"""
