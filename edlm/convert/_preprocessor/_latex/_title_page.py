# coding=utf-8
"""
Title page
"""

_HLINE = r'\vspace{-10pt}\noindent\rule{\textwidth}{1pt}\vspace{-10pt}'

# noinspection SpellCheckingInspection
TITLE_PAGE = rf"""
\thispagestyle{{empty}}
\newgeometry{{noheadfoot=true,left=2.5cm,right=2.5cm,top=1.5cm,bottom=1.5cm}}

\begin{{minipage}}[t]{{0.5\textwidth}}
    \textit{{\textbf{{BY ORDER OF THE COMMAND STAFF\\VIRTUAL 57\textsuperscript{{th}} WING}}}} \\
    \begin{{minipage}}[l]{{\textwidth}}
        \vspace*{{1em}}
        $for(title_pictures)$
              \includegraphics[height=2.5cm]{{$title_pictures$}}
        $endfor$
    \end{{minipage}}
\end{{minipage}}
\hfill
\begin{{minipage}}[t]{{0.5\textwidth}}
    \begin{{flushright}}
        \textit{{\textbf{{VIRTUAL 57\textsuperscript{{th}} WING}}}} \\
        \textit{{\textbf{{ $qualifier$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $published_date$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $category$ }}}} \\
        \vspace*{{1em}}
        \textit{{\textbf{{ $title$ }}}}
    \end{{flushright}}
\end{{minipage}}
    
\begin{{center}}
    \textbf{{COMPLIANCE WITH THIS PUBLICATION IS MANDATORY FOR ALL AFFECTED PARTIES}}
\end{{center}}

{_HLINE}

\textbf{{ACCESSIBILITY:}} The most current version of this document is available digitally on the Virtual 
57\textsuperscript{{th}} Wing website at \url{{$link$}}.

\textbf{{RELEASABILITY:}} $if(releasability)$
	$releasability$
$else$
	There are no releasability restriction on this publication.
$endif$

\textbf{{DISCLAIMER:}} This document is modeled from real world USAF publications for non-profit entertainment purposes only, 
to be used within the virtual flying community.  It in no way implies endorsement by any branch of the 
US Armed Services or its constituent organizations and groups. Not for real world use.

{_HLINE}

\begin{{minipage}}[t]{{0.5\textwidth}}
    OPR: $opr$ \\
    Supersedes: $supersedes$
\end{{minipage}}
\hfill
\begin{{minipage}}[t]{{0.5\textwidth}}
    \begin{{flushright}}
        Certified by: \\ $for(certified_by)$ $certified_by$ \\ $endfor$
        Pages: \pageref{{LastPage}}
    \end{{flushright}}
\end{{minipage}}

{_HLINE}

\textit{{\textbf{{$description$}}}}

\textbf{{SUMMARY OF CHANGES}} \\ $for(summary_of_changes)$ - $summary_of_changes$ \\ $endfor$

\vfill
\restoregeometry


"""  # noqa
