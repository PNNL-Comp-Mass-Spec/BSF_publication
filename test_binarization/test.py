""" 
1. test a correlation between cosine distance and BSF scores
python benchmark.py --data GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06_1000.npy --num_sets 500 --cutoff 2.5
python benchmark.py --data ProteinMatrix_20x15k.npy --num_sets 500 --cutoff 0.6

2. test a binarization from a continous numeric matrix into a binarized matrix to fit to BSF
python benchmark.py --data GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06_1000.npy --num_sets 500 --cutoff 2.5 --binarizeonly
"""
import sys
import numpy as np
import pandas as pd
import time
from numba import jit

import bsf

import scipy.spatial
import scipy.stats as stats

import matplotlib.pyplot as plt
### if you want to run this script in an interactive mode,
### please comment the following three lines out and run this code.
# import matplotlib as mpl
# mpl.use('Agg')
# plt.ioff() #http://matplotlib.org/faq/usage_faq.html (interactive mode)

import argparse

###############################################################
parser = argparse.ArgumentParser()

parser.add_argument(
    '--data', type=str, default='ProteinMatrix_20x15k.npy',
    help='data file')
parser.add_argument(
    '--num_sets', type=int, default=100,
    help='number of signatures to test')
parser.add_argument(
    '--cutoff', type=float, default=1,
    help='cutoff value')
parser.add_argument(
    '--binarizeonly', action='store_true',
    help='test a binarization only')
FLAGS = parser.parse_args()
###############################################################

@jit
def bool2int(x):
    y = 0
    for i, j in enumerate(x):
        if j:
            y += 1 << i
    return y


def bool2ints(fn, bits, _size):
    newsize = _size * 64
    r = np.zeros(_size, dtype=np.uint64)
    for j in range(_size):
        _end = min((j + 1) * 64, newsize)
        r[j] = fn(bits[j * 64:_end][::-1])  # reverse
    return r


def bool2uint64(fn, boolmat, _size):
    """convert boolean matrix into uint64
    Args:
        boolmat: boolean-type 2d numpy array of [nsignatures, vec_len]
    Results:
        r: [nsignatures, _size]
    """
    nsignatures, vec_len = boolmat.shape
    r = np.zeros((nsignatures, _size), dtype=np.uint64)
    start = time.time()
    for i in range(nsignatures):
        r[i, :] = bool2ints(fn, boolmat[i, :], _size)
    done = time.time()
    elapsed = done - start
    print(fn, elapsed)
    return r


def cal_cosine(mat):
    ''' calculate cosine distances for pairwise comparisons
    '''
    nrows, ncols = mat.shape
    dist = np.zeros((nrows, nrows))
    for i in range(nrows):
        for j in range(i, nrows):
            dist[i,j] = scipy.spatial.distance.cosine(mat[i,:], mat[j,:])
    return dist


def binerize_by_cutoff(mat, cutoff, direction=1):
    '''binerize a matrix by cutoff threshold
    '''
    if direction == 0:  # True if <= cutoff
        bin_mat = mat < cutoff
    else:  # True if >= cutoff
        bin_mat = mat > cutoff
    
    n_sets, n_elements = bin_mat.shape
    
    # 64bit uint
    _size = int(n_elements / 64)
    if n_elements % 64:
        _size += 1
    return bool2uint64(bool2int, bin_mat, _size)


def cal_fisher_exact_test(mat, cutoff):
    ''' calculate fisher exact tests for pairwise binarized vectors
    '''
    nrows, ncols = mat.shape
    dist = np.zeros((nrows, nrows))

    bin_mat = (mat < -cutoff) | (mat > cutoff)

    for i in range(nrows):
        for j in range(i, nrows):
            overlap = np.sum(bin_mat[i, :] & bin_mat[j, :])
            dist[i,j] = fisher_exact(overlap, np.sum(bin_mat[i, :]), np.sum(bin_mat[j, :]), ncols)
    return dist


def fisher_exact(overlap, n_set1, n_set2, n_backgrounds):
    ''' compute a p-value of fisher exact tests
    '''
    a = overlap
    b = n_set1 - a
    c = n_set2 - a
    d = n_backgrounds - n_set1 - c
    oddsratio, pvalue = stats.fisher_exact([[a, b], [c, d]], alternative='greater')
    return pvalue


def get_bsf_scores(mat_up, mat_dn, size, fout="test"):
    """find relevant genesets by filtering via BSF
    """
    bsf.analysis_with_chunk(mat_up, size, 'up.txt', './')
    bsf.analysis_with_chunk(mat_dn, size, 'dn.txt', './')
    with open("bin_{0}_0_0_{0}_{0}_up.txt.bin".format(size), "rb") as f:
        up_scores = np.frombuffer(f.read(), dtype=np.uint32).reshape((mat_up.shape[0], mat_up.shape[0]))
    with open("bin_{0}_0_0_{0}_{0}_dn.txt.bin".format(size), "rb") as f:
        dn_scores = np.frombuffer(f.read(), dtype=np.uint32).reshape((mat_dn.shape[0], mat_dn.shape[0]))
    return up_scores, dn_scores


def plot_cor(mat1, mat2, xlabel, ylabel, out_file='out.pdf'):
    # upper triangular part 
    iu = np.triu_indices(mat1.shape[0], 1)

    plt.close('all')

    fig, ax = plt.subplots()
    ax.scatter(mat1[iu], mat2[iu])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(out_file)


if __name__ == '__main__':
    stime = time.time()
    print('Loading ...')
    _mat = np.load(FLAGS.data)
    n_sets, n_elements = _mat.shape
    print('Done loading: {0} sec'.format(time.time()-stime))
    print('Matrix size: ({0}, {1})'.format(n_sets, n_elements))

    mat = _mat[0:FLAGS.num_sets,:]

    stime = time.time()
    up = binerize_by_cutoff(mat, FLAGS.cutoff, 1)
    dn = binerize_by_cutoff(mat, -FLAGS.cutoff, 0)
    etime = time.time()
    print('Time binerize_by_cutoff:{0} sec'.format(etime-stime))
    print('up %:', np.sum(mat>FLAGS.cutoff)/(mat.shape[0]*mat.shape[0]))
    print('dn %:', np.sum(mat<-FLAGS.cutoff)/(mat.shape[0]*mat.shape[0]))

    if FLAGS.binarizeonly:
        sys.exit()

    cosine_dist = cal_cosine(mat)
    np.save('ProteinMatrix_{0}_cos'.format(FLAGS.num_sets), cosine_dist)
    
    up_scores, dn_scores = get_bsf_scores(up, dn, FLAGS.num_sets)
    np.save('ProteinMatrix_{0}_bsf_up'.format(FLAGS.num_sets), up_scores)
    np.save('ProteinMatrix_{0}_bsf_dn'.format(FLAGS.num_sets), dn_scores)
    
    fisher_p = cal_fisher_exact_test(mat, FLAGS.cutoff)
    np.save('ProteinMatrix_{0}_fisher'.format(FLAGS.num_sets), fisher_p)

    plot_cor(cosine_dist, up_scores+dn_scores, 'Cosine distance','BSF score','cos_bsf_scatter_{0}.pdf'.format(FLAGS.num_sets))
    plot_cor(cosine_dist, fisher_p, 'Cosine distance','Fisher exact (p-value)', 'cos_fisher_scatter_{0}.pdf'.format(FLAGS.num_sets))
    plot_cor(up_scores+dn_scores, fisher_p, 'BSF score','Fisher exact (p-value)', 'bsf_fisher_scatter_{0}.pdf'.format(FLAGS.num_sets))

