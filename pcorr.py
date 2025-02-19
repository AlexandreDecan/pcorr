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


def maximal_pvalue(pv, alpha=0.05, *, sort=True):
    """ Print the highest p-value that is still significant after correction. """
    if sort:
        pv = sorted(pv)

    methods = {
        'None': no_correction,
        'Bonferroni': bonferroni,
        'Holm': holm,
        'Hochberg': hochberg,
        'Benjamini-Hochberg': benjamini_hochberg,
    }
    print(f'Context: {alpha=}, {len(pv)} p-values')

    for method, fn in methods.items():
        v = fn(pv, alpha, sort=False)
        n = len([x for x in pv if x <= v])
        print(f'{method:<20}\tp-value={v:.6f}\t{n:>3} significant p-values')


