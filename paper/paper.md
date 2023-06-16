---
title: 'BoxKit: A Python library to manage analysis of block-structured simulation datasets'
tags:
  - Python
  - block structured datasets
  - simulation analysis
  - machine learning
  - performance optimization
authors:
  - name: Akash Dhruv
    orcid: 0000-0003-4997-321X
    affiliation: 1
affiliations:
 - name: Argonne National Laboratory, USA
   index: 1
date: 15 June 2023
bibliography: paper.bib
---

# Summary

BoxKit is a library that provides building blocks to parallelize and 
scale data science, high performance computing, and machine learning
applications for block-structured datasets. Spatial data from
simulations and experiments can be accessed and managed using tools
available in this library when working with more data analysis oriented
packages like SciKit, FlowNet, and OpticalFlow


# Statement of need

Details about why there is software addresses references like
[@DUBEY2022], [@DHRUV2023], and [@HASSAN2023] 

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
