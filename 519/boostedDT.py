"""
    TEMPLATE FOR MACHINE LEARNING HOMEWORK
    AUTHOR Eric Eaton, Vishnu Purushothaman Sreenivasan
"""
import numpy as np
import numpy.testing as npt
from numpy.ma import log
from sklearn import tree
from sklearn.preprocessing import normalize


def standardize(args, new_type=np.asmatrix):
    # convert args to matrices
    args = [new_type(arg) for arg in args]
    if new_type == np.asmatrix:
        for i, arg in enumerate(args):
            n, d = arg.shape
            # convert column vectors to row vectors
            if n > 1 and d == 1:
                args[i] = arg.T
    if new_type == np.asarray:
        for i, arg in enumerate(args):
            # convert column vectors to row vectors
            if len(arg.shape) == 2:
                if 1 in arg.shape:
                    args[i] = arg.flatten()
    return args


def get_bad_predictions(predictions, y):
    """
    :return: indicator matrix (each value = 1 if prediction is wrong else 0)
    from the SAMME paper: I( c_i != T(m)(x_i) )
    """
    predictions, y = standardize((predictions, y))

    bad_predictions = np.matrix(np.ones(y.size))
    bad_predictions[predictions == y] = 0
    return bad_predictions


def calculate_beta(error, num_classes):
    return .5 * (log((1 - error) / error) + log(num_classes - 1))


def calculate_error(weights, bad_predictions):
    weights, bad_predictions = standardize(
        (weights, bad_predictions), new_type=np.asarray
    )
    return np.dot(weights, bad_predictions)  # / weights.sum() <= this is always == 1 right?


def get_new_weights(bad_predictions, weights, beta):
    weights, bad_predictions = standardize((weights, bad_predictions))

    pre_norm_weights = np.multiply(weights, np.exp(beta * bad_predictions))
    return normalize(pre_norm_weights, axis=1, norm='l1').flatten()


class BoostedDT:
    def __init__(self, numBoostingIters=100, maxTreeDepth=3):
        """
        Constructor
        """
        self.numBoostingIters = numBoostingIters
        self.maxTreeDepth = maxTreeDepth


    def fit(self, X, y):
        """
        Trains the model
        Arguments:
            X is a n-by-d numpy array
            y is an n-dimensional numpy array
        """
        # TODO
        weights = normalize(np.ones(len(y)), axis=1, norm='l1').flatten()  # 1/n, ..., 1/n
        self.classes = np.unique(np.asarray(y))
        self.betas, self.models = [], []

        for _ in range(self.numBoostingIters):
            npt.assert_almost_equal(weights.sum(), 1.)  # sum(weights) == 1

            # train classifier
            clf = tree.DecisionTreeClassifier(max_depth=self.maxTreeDepth)
            trained_model = clf.fit(X, y, weights)

            bad_predictions = get_bad_predictions(trained_model.predict(X), y)

            error = calculate_error(weights, bad_predictions)
            assert error < (self.classes.size - 1.) / self.classes.size
            beta = calculate_beta(error, self.classes.size)

            self.betas.append(beta)
            self.models.append(trained_model)

            weights = get_new_weights(bad_predictions, weights, beta)

    def predict(self, X):
        """
        Used the model to predict values for each instance in X
        Arguments:
            X is a n-by-d numpy array
        Returns:
            an n-dimensional numpy array of the predictions
        """
        # TODO
        predictions = [h.predict(X) for h in self.models]
        return combine(self.classes, predictions, self.betas)


def combine(classes, predictions, betas):
    predictions, betas = standardize([predictions, betas])

    predictions = predictions.T
    votes_per = votes_per_class(classes, predictions, betas)
    indices = votes_per.argmax(axis=1)
    return classes[indices]


def votes_per_class(classes, predictions, betas):
    predictions, betas = standardize([predictions, betas])

    votes_per = [votes(c, predictions, betas) for c in classes]
    return np.hstack(votes_per)


def votes(klass, predictions, betas):
    predictions, betas = standardize([predictions, betas])

    indicators = np.matrix(np.zeros(predictions.shape))
    indicators[predictions == klass] = 1
    return indicators * betas.T