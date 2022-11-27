% Additional warnings for deprecated things
\RequirePackage[l2tabu, orthodox]{nag}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{gropro}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Optional 'english' language option
\newcommand{\InitGroProLanguage}{\PassOptionsToPackage{english,ngerman}{babel}}
\DeclareOption{english}{\renewcommand{\InitGroProLanguage}{\PassOptionsToPackage{english}{babel}}}

\ProcessOptions
\InitGroProLanguage

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% report format with MATSE styling
\LoadClass[a4paper, 12pt]{report}
\renewcommand{\thesection}{\arabic{section}}
\usepackage[a4paper, left=2cm, right=3.2cm, top=3.9cm, bottom=2.8cm]{geometry}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Enable post-90s text processing
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Typesetting
\usepackage{babel}
\usepackage{parskip}
\usepackage{microtype}
\usepackage{csquotes}
\usepackage{booktabs}
\usepackage{listings}
\usepackage[font=small,labelfont=bf]{caption}

\usepackage{lmodern} % upgrade default font
\usepackage[sc]{mathpazo} % pretty font for text

% \usepackage{fontspec}
% \setmainfont{Verdana}

\usepackage[scaled=0.85]{beramono}

\usepackage{lstautogobble}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Colors
\RequirePackage[svgnames, table]{xcolor}

\definecolor{fhprimary}{RGB}{1, 169, 159}
\definecolor{fhsecondary}{RGB}{1, 148, 138}
\definecolor{fhtertiary}{RGB}{0, 111, 104}
\definecolor{fhquaternary}{RGB}{0, 74, 68}
\definecolor{fhsilver}{RGB}{168, 169, 172}

\definecolor{codered}{rgb}{0.788, 0.102, 0.35}
\definecolor{codegreen}{rgb}{0.137, 0.471, 0.255}
\definecolor{codeblue}{rgb}{0, 0.333, 0.749}
\definecolor{codeorange}{rgb}{0.996, 0.541, 0.094}
\definecolor{codegrey}{rgb}{0.627, 0.647, 0.663}
\definecolor{codepurple}{HTML}{C42043}
\definecolor{backcolour}{HTML}{F2F2F2}
\definecolor{bookColor}{cmyk}{0,0,0,0.90}  
\definecolor{orange}{RGB}{230,159,0}
\definecolor{skyblue}{RGB}{86,180,233}
\definecolor{bluishgreen}{RGB}{0,158,115}
\definecolor{vermillion}{RGB}{213,94,0}
\definecolor{reddishpurple}{RGB}{204,121,167}
\definecolor{matse}{RGB}{11,102,168}
\definecolor{fhmint}{RGB}{0,177,172}
\definecolor{fhblue}{RGB}{0,141,208}
\definecolor{fhred}{RGB}{168,46,104}
\definecolor{fhpurple}{RGB}{147,81,159}
\definecolor{fhyellow}{RGB}{249,248,113}
\definecolor{bg}{rgb}{0.95,0.95,0.95}

\lstset{upquote=true}

% better highlighting
\makeatletter
\newenvironment{btHighlight}[1][]
{\begingroup\tikzset{bt@Highlight@par/.style={#1}}\begin{lrbox}{\@tempboxa}}
{\end{lrbox}\bt@HL@box[bt@Highlight@par]{\@tempboxa}\endgroup}

\newcommand\btHL[1][]{%
  \begin{btHighlight}[#1]\bgroup\aftergroup\bt@HL@endenv%
}
\def\bt@HL@endenv{%
  \end{btHighlight}%   
  \egroup
}
\newcommand{\bt@HL@box}[2][]{%
  \tikz[#1]{%
    \pgfpathrectangle{\pgfpoint{1pt}{0pt}}{\pgfpoint{\wd #2}{\ht #2}}%
    \pgfusepath{use as bounding box}%
    \node[anchor=base west, fill=orange!30,outer sep=0pt,inner xsep=1pt, inner ysep=0pt, rounded corners=3pt, minimum height=\ht\strutbox+1pt,#1]{\raisebox{1pt}{\strut}\strut\usebox{#2}};
  }%
}
\makeatother

\lstdefinestyle{MatseInputStyle}{
    backgroundcolor=\color{backcolour}, 
    basicstyle=\footnotesize\ttfamily,
    keywordstyle=\bfseries\color{codeblue},  
    stringstyle=\color{codered},
    commentstyle=\color{codegrey},
    %keywordstyle=\color{codeblue},
    %stringstyle=\color{codered},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false, %
    autogobble=true,
    % SQL specific
    % language=mysql,
    % deletekeywords={IDENTITY},
    % deletekeywords={[2]INT},
    % morekeywords={clustered},
    % show small line numbers
    numbers=left,
    numberstyle=\tiny\color{codegrey},
    numbersep=10pt,
    stepnumber=1,
    framesep=5pt,
    xleftmargin=10pt,
    framexleftmargin=0pt,
    %frame=ltb,
    frame=l,
    framerule=0pt,
}
\lstset{style=MatseInputStyle}

\makeatletter
\linespread{1.05} % more spacing

\usepackage[shortlabels]{enumitem}
\setlist{nosep}
\makeatother

\makeatletter
% Re-enable paragraph spacing in minipages;
% we choose something smaller than what is used outside of minipages.
\newcommand{\@minipagerestore}{\setlength{\parskip}{0.8\medskipamount}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Utilities
\usepackage{blindtext}
\usepackage{footnote}
\usepackage{pdfpages}
\usepackage{enumitem}
\usepackage{adjustbox}
\usepackage{mdframed}
\usepackage{float}

% Show most recent revision number and date in date field
\makeatletter
\date{\small \IfLanguageName{ngerman}{Letzte Änderung:}{Last Change:} \filename@parse{\jobname}\IfFileExists{\filename@base.last-change}{\input{\filename@base.last-change}}{\today}}
\makeatother

% escaping underscores
\makeatletter
\DeclareRobustCommand*{\escapeus}[1]{%
  \begingroup\@activeus\scantokens{#1\endinput}\endgroup}
\begingroup\lccode`\~=`\_\relax
   \lowercase{\endgroup\def\@activeus{\catcode`\_=\active \let~\_}}
\makeatother



%\subject{\normalfont{}\texttt{\href{https://matse.paddel.xyz/spicker}{https://matse.paddel.xyz/spicker}}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Math & Symbols
\usepackage{mathtools}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{stmaryrd}
\usepackage{braket}
\usepackage{cool}
\usepackage{siunitx}
\usepackage{venndiagram}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Diagrams
\usepackage{tikz}
\usetikzlibrary{chains,scopes,matrix,shapes,snakes,positioning}
\usepackage{tikzscale}
\usepackage{pgfplots, pgfplotstable}
\usepgfplotslibrary{fillbetween}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Links and Metadata
\usepackage{tcolorbox}
\usepackage{nameref}

\usepackage[]{imakeidx}
\usepackage[
  colorlinks,
  citecolor = matse,
  linkcolor = matse,
  urlcolor = matse
]{hyperref}
\usepackage{bookmark}

\makeatletter
\AtBeginDocument{
  \hypersetup{
    pdftitle = {\@title},
    pdfauthor = {\@author}
  }
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Context
%\usepackage[]{imakeidx}
\usepackage{iflang}

\usepackage{etoolbox}
\usepackage{tikzpagenodes}

\makeatletter

\let\@azubiid\@empty
\let\@programmingLanguage\@empty
\let\@affiliation\@empty
\def\@matselogo{\includegraphics[height=20mm]{matse-logo.png}}
\def\@logo{\includegraphics[height=15mm]{logo.jpg}}

\newcommand{\azubiid}[1]{\gdef\@azubiid{#1}}
\newcommand{\programmingLanguage}[1]{\gdef\@programmingLanguage{#1}}
\newcommand{\affiliation}[1]{\gdef\@affiliation{#1}}

\newenvironment{alwayssingle}{%
       \@restonecolfalse
       \if@twocolumn\@restonecoltrue\onecolumn
       \else\if@openright\cleardoublepage\else\clearpage\fi
       \fi}%
       {\if@restonecol\twocolumn
       \else\newpage\thispagestyle{plain}\fi
}

% \newcommand\AtPageUpperRight[1]{\AtPageUpperLeft{%
% \makebox[\paperwidth][r]{#1}}}

\renewcommand\maketitle{%
\begin{alwayssingle}
  \thispagestyle{empty}
  % FH-Logo  
%   \begin{tikzpicture}[
%     remember picture,
%     overlay,
%     %shift={(current page.north east)}
%     ]
%       \node[
%         anchor=north east,
%         xshift=0.15cm,
%         yshift=-1cm,
%         ]
%         at (current page.north east) 
%         {\includegraphics[height=4.84cm]{../fh-aachen.jpg}};
%   \end{tikzpicture}
  %
  % Deckblatt
    \begin{center}
        {\large\IfLanguageName{ngerman}{Dokumentation der Abschlussprüfung im Ausbildungsberuf \enquote{Mathematisch-Technische*r Softwareentwickler*in},\\Prüfungsbereich: \enquote{Entwicklung eines Softwaresystems}}{Documentation of the Final Examination in the Occupation of \enquote{Mathematical-Technical Software Developer},\\Examination Area: \enquote{Development of a Software System}}\par}
        {\Huge\bfseries\@title\par}
        \vspace*{2cm}
        % \vspace*{8ex}
        {\Large\bfseries\@author\ifx\@azubiid\@empty\else\ (\@azubiid)\par}
        {\ifx\@affiliation\@empty\else\large\vspace*{1ex}\par\@affiliation\par\fi}
        {\ifx\@programmingLanguage\@empty\else\large\vspace*{1ex}\par\IfLanguageName{ngerman}{Programmiersprache:}{Programming Language:} \@programmingLanguage\par\fi}
        {\vspace*{20mm}\par$\vcenter{\hbox{\@matselogo}}$\ifx\@affiliation\@empty\else\hspace{15mm}$\vcenter{\hbox{\@logo}}$\par\vspace*{20mm}\fi}
        \vfill
        %
        \vspace*{2ex}
        {\today}
    \end{center}
\null\vfill

\newpage 
\thispagestyle{empty}

\begin{center}
  {\Large\bfseries Eidesstattliche Erklärung \par}
\end{center}
\vspace*{4ex}

Hiermit versichere ich, dass das vorliegende Prüfprodukt zum Thema 

\vspace*{2ex}

\begin{center}
  {\large\@title\par}
\end{center}

\vspace*{2ex}


von mir selbstständig erstellt wurde.
Die als Arbeitshilfe genutzten Unterlagen sind in der Arbeit vollständig aufgeführt. 
Ich versichere, dass der vorgelegte Ausdruck mit dem Inhalt der von mir erstellten digitalen Version identisch ist.
Weder ganz noch in Teilen wurde die Arbeit bereits als Prüfungsleitung vorgelegt. 
Mir ist bewusst, dass jedes Zuwiederhandeln als Täuschungsversuch zu gelten hat, der die Anerkennung des Prüfprodukts als Prüfungsleistung ausschließt.

\vspace*{4ex}

Name: \@author

Aachen, den \today

\vspace*{10ex}
% \begin{center}
  { % Signatures short format
  \begin{tabular}{@{}p{3in}@{}}
      \hrulefill \\
      Unterschrift der/des Auszubildenden
  \end{tabular}
  }
% \end{center}
\null\vfill
\end{alwayssingle}
}
\endinput

\AtEndDocument{
  \makeatletter
  \makeatother
}