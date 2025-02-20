"""
** References:

* Family-wise errors
@article{halperin1988some,
  title={Some implications of an alternative definition of the multiple comparison problem},
  author={Halperin, Max and Lan, KK Gordon and Hamdy, Mohamed I},
  journal={Biometrika},
  volume={75},
  number={4},
  pages={773--778},
  year={1988},
  publisher={Oxford University Press}
}

* Holm
@article{29def780-e117-38f0-8afb-edf384af3fad,
 ISSN = {03036898, 14679469},
 URL = {http://www.jstor.org/stable/4615733},
 abstract = {This paper presents a simple and widely applicable multiple test procedure of the sequentially rejective type, i.e. hypotheses are rejected one at a time until no further rejections can be done. It is shown that the test has a prescribed level of significance protection against error of the first kind for any combination of true hypotheses. The power properties of the test and a number of possible applications are also discussed.},
 author = {Sture Holm},
 journal = {Scandinavian Journal of Statistics},
 number = {2},
 pages = {65--70},
 publisher = {[Board of the Foundation of the Scandinavian Journal of Statistics, Wiley]},
 title = {A Simple Sequentially Rejective Multiple Test Procedure},
 urldate = {2025-02-20},
 volume = {6},
 year = {1979}
}

* Hochberg
@article{hochberg1988sharper,
  title={A sharper Bonferroni procedure for multiple tests of significance},
  author={Hochberg, Yosef},
  journal={Biometrika},
  volume={75},
  number={4},
  pages={800--802},
  year={1988},
  publisher={Oxford University Press}
}

* Benjamini-Hochberg
@article{benjamini1995controlling,
  title={Controlling the false discovery rate: a practical and powerful approach to multiple testing},
  author={Benjamini, Yoav and Hochberg, Yosef},
  journal={Journal of the Royal statistical society: series B (Methodological)},
  volume={57},
  number={1},
  pages={289--300},
  year={1995},
  publisher={Wiley Online Library}
}

"""

def no_correction(pv, alpha=0.05, *, sort=True):
    """ Determine the highest p-value that is still significant without correction. """
    if sort:
        pv = sorted(pv)

    n = len(pv)
    for i, p in enumerate(pv):
        if p > alpha:
            break
    return pv[i-1] if i > 0 else None


def bonferroni(pv, alpha=0.05, *, sort=True):
    """ Determine the highest p-value that is still significant after Bonferroni correction. """
    if sort:
        pv = sorted(pv)

    n = len(pv)
    for i, p in enumerate(pv):
        if p > alpha / n:
            break
    return pv[i-1] if i > 0 else None


def holm(pv, alpha=0.05, *, sort=True):
    """ Determine the highest p-value that is still significant after Holm correction. """
    if sort:
        pv = sorted(pv)

    n = len(pv)
    for i, p in enumerate(pv):
        if p > alpha / (n - i):
            break
    return pv[i-1] if i > 0 else None


def hochberg(pv, alpha=0.05, *, sort=True):
    """ Determine the highest p-value that is still significant after Hochberg correction. """
    if sort:
        pv = sorted(pv)

    n = len(pv)
    for i, p in reversed(list(enumerate(pv))):
        if p <= alpha / (n - i):
            return p
    return None

def benjamini_hochberg(pv, alpha=0.05, *, sort=True):
    """ Determine the highest p-value that is still significant after Benjamini-Hochberg correction. """
    if sort:
        pv = sorted(pv)

    n = len(pv)
    for i, p in reversed(list(enumerate(pv))):
        if p <= alpha * (i + 1) / n:
            return p
    return None

_methods = {
    'None': no_correction,
    'Bonferroni': bonferroni,
    'Holm': holm,
    'Hochberg': hochberg,
    'Benjamini-Hochberg': benjamini_hochberg,
}

def maximal_pvalue(pv, alpha=0.05, *, sort=True):
    """ Print the highest p-value that is still significant after correction. """
    if sort:
        pv = sorted(pv)
        
    print(f'Context: {alpha=}, {len(pv)} p-values')
    for method, fn in _methods.items():
        v = fn(pv, alpha, sort=False)
        n = len([x for x in pv if x <= v])
        print(f'{method:<20}\tp-value={v:.6f}\t{n:>3} significant p-values')


