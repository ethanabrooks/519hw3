import random
import pytest
from numpy import *
import numpy.testing as npt
import scipy
import sklearn
from boostedDT import calculate_beta, calculate_error, standardize, votes_per_class, combine, votes, \
    get_bad_predictions

__author__ = 'Ethan'


def test_votes_per_class():
    classes = [1, 5]
    weights = ones(5)
    predictions = matrix([
        [0, 1, 2, 6, 1],
        [1, 1, 1, 5, 2],
        [1, 5, 4, 3, 0]
    ])
    actual = votes_per_class(classes, predictions, weights)
    desired = matrix([
        [2, 0],
        [3, 1],
        [1, 1]
    ])
    npt.assert_almost_equal(actual, desired)


def normalize(weights_pre_norm):
    [weights_pre_norm] = standardize((weights_pre_norm))

    return matrix(weights_pre_norm / weights_pre_norm.sum())


def test_calculate_score():
    epsilon = 2. / 5.
    K = 2
    actual = calculate_beta(epsilon, K)
    desired = 0.202732554054
    npt.assert_almost_equal(actual, desired)

    epsilon = 1. / 8.
    K = 4
    actual = calculate_beta(epsilon, K)
    desired = 1.52226121886171149825029
    npt.assert_almost_equal(actual, desired)


# def test_pre_norm():
#     weights = [5]
#     beta = -1.2
#     y = [-1]
#     h_x = [1]
#     actual = get_pre_norm(weights, beta, y, h_x)
#     desired = matrix(1.5059711)
#     npt.assert_almost_equal(actual, desired)
#
#     weights = [3]
#     beta = -1.2
#     y = [-1]
#     h_x = [0]
#     actual = get_pre_norm(weights, beta, y, h_x)
#     desired = matrix(3)
#     npt.assert_almost_equal(actual, desired)
#
#     weights = [5, 3]
#     beta = -1.2
#     y = [-1, -1]
#     h_x = [1, -1]
#     h_x = get_bad_predictions(h_x, y)
#     actual = get_pre_norm(weights, beta, y, h_x)
#     desired = matrix([1.50597106, 3])
#     npt.assert_almost_equal(actual, desired)


def test_normalize():
    pre_norm = matrix([16.6005846, 0.9035826])
    actual = normalize(pre_norm)
    desired = matrix([0.948379, 0.051621])
    npt.assert_almost_equal(sum(actual), 1)
    npt.assert_almost_equal(actual, desired)

    random.seed(0)
    random_vector = random.rand(1, 5)
    actual = sklearn.preprocessing.normalize(random_vector, axis=1, norm='l1')
    desired = normalize(random_vector)
    npt.assert_almost_equal(actual, desired)


def test_calculate_error():
    weights = [2, .5, .23, 3.1]
    predictions = [1, 1, 1, 1]
    y = [1, -1, 1, 1]
    predictions = get_bad_predictions(predictions, y)
    actual = calculate_error(weights, predictions)
    desired = 0.0857632933104631
    npt.assert_almost_equal(actual, desired)

    weights = [2, .5, .23, 3.1, 5, 5, 5, 5]
    predictions = [1, 1, 1, 1, 1, 1, 1, 1]
    y = [-1, 1, -1, -1, 1, 1, 1, 1]
    predictions = get_bad_predictions(predictions, y)
    actual = calculate_error(weights, predictions)
    desired = 0.206349206349206349206
    npt.assert_almost_equal(actual, desired)


def test_votes():
    weights = ones(5)
    klass = 1
    predictions = matrix([
        [0, 1, 2, 6, 1],
        [1, 1, 1, 5, 2],
        [1, 5, 4, 3, 0]
    ])
    actual = votes(klass, predictions, weights)
    desired = matrix([2, 3, 1]).T
    npt.assert_almost_equal(actual, desired)

    weights = ones(5)
    klass = 5
    predictions = matrix([
        [0, 5, 2, 6, 1],
        [1, 1, 1, 5, 2],
        [1, 5, 4, 3, 0]
    ])
    actual = votes(klass, predictions, weights)
    desired = matrix([1, 1, 1]).T
    npt.assert_almost_equal(actual, desired)

    weights = matrix([1, 2, 1, 2, 0])
    klass = 5
    predictions = matrix([
        [0, 5, 2, 6, 1],
        [1, 1, 5, 2, 2],
        [1, 1, 4, 3, 5]
    ])
    actual = votes(klass, predictions, weights)
    desired = matrix([2, 1, 0]).T
    npt.assert_almost_equal(actual, desired)


def test_get_bad_predictions():
    predictions = [1, 3, 45, 3, 5, 3]
    y = [1, 1, 4, 0, 5, 3]
    actual = get_bad_predictions(predictions, y)
    desired = [0, 1, 1, 1, 0, 0]
    npt.assert_almost_equal(actual, desired)
