# coding=utf-8
"""
Title page
"""

_HLINE = r'\noindent\rule{\textwidth}{1pt}'

# noinspection SpellCheckingInspection
TITLE_PAGE = rf"""
\thispagestyle{{empty}}

\begin{{minipage}}[t]{{0.4\textwidth}}
    \textit{{\textbf{{BY ORDER OF THE COMMAND STAFF VIRTUAL 57\textsuperscript{{th}} WING}}}}
\end{{minipage}}
\hfill
\begin{{minipage}}[t]{{0.4\textwidth}}
    \begin{{flushright}}
        \textit{{\textbf{{VIRTUAL 57\textsuperscript{{th}} WING}}}} \\
        \textit{{\textbf{{ $qualifier_long$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $published_date$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $category$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $title$ }}}}
    \end{{flushright}}
\end{{minipage}}

$if(title_pictures)$
        \begin{{figure}}[h]
            \begin{{minipage}}[c]{{\linewidth}}
                $for(title_pictures)$
                      \includegraphics[height=2cm]{{$title_pictures$}}
                $endfor$
            \end{{minipage}}
        \end{{figure}}
    $endif$
    
\vfill
    
\begin{{center}}
    \textbf{{COMPLIANCE WITH THIS PUBLICATION IS MANDATORY FOR ALL AFFECTED PARTIES}}
\end{{center}}

{_HLINE}

\textbf{{ACCESSIBILITY:}} The most current version of this document is available digitally on the Virtual 
57\textsuperscript{{th}} Wing website at \url{{$link$}}.

\textbf{{DISCLAIMER:}} This document is modeled from real world USAF publications for non-profit entertainment purposes only, 
to be used within the virtual flying community.  It in no way implies endorsement by any branch of the 
US Armed Services or its constituent organizations and groups. Not for real world use.

{_HLINE}

\begin{{minipage}}[t]{{0.4\textwidth}}
    \textbf{{OPR:}} $opr$ \\
    \textbf{{Supersedes:}} \\ $for(supersedes)$ - $supersedes$ \\ $endfor$
\end{{minipage}}
\hfill
\begin{{minipage}}[t]{{0.4\textwidth}}
    \begin{{flushright}}
        \textbf{{Certified by:}} \\ $for(certified_by)$ $certified_by$ \\ $endfor$
    \end{{flushright}}
\end{{minipage}}

{_HLINE}

\textit{{\textbf{{$description$}}}}

{_HLINE}

\textbf{{SUMMARY OF CHANGES}} \\ $for(summary_of_changes)$ - $summary_of_changes$ \\ $endfor$

\vfill


"""  # noqa
