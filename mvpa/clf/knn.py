#emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""PyMVPA: k-Nearest-Neighbour classification"""

import numpy as N

from mvpa.misc import verbose

try:
    import psyco
    psyco.profile()
except:
    verbose(5, "Psyco online compilation is not enabled in knn")


class kNN:
    """ k-nearest-neighbour classification.
    """
    def __init__(self, k=2):
        """
        Parameters:
          k:       number of nearest neighbours to be used for voting
        """
        self.__k = k
        self.__votingfx = self.getWeightedVote
        self.__data = None


    def __repr__(self):
        """ String summary over the object
        """
        return """kNN:
 k (# of nearest neighbors): %d
 votingfx: TODO
 data: %s""" % (self.__k, `self.__data`)


    def train( self, data ):
        """ Train the classifier.

        For kNN it is degenerate -- just stores the data.
        """
        self.__data = data


    def predict(self, data):
        """ Predict the class labels for the provided data.

        Returns a list of class labels (one for each data sample).
        """
        # make sure we're talking about arrays
        data = N.array( data )

        if not data.ndim == 2:
            raise ValueError, "Data array must be two-dimensional."

        if not data.shape[1] == self.__data.nfeatures:
            raise ValueError, "Length of data samples (features) does " \
                              "not match the classifier."

        # predicted class labels will go here
        predicted = []

        # for all test pattern
        for p in data:
            # calc the euclidean distance of the pattern vector to all
            # patterns in the training data
            dists = N.sqrt(
                        N.sum(
                            N.abs( self.__data.samples - p )**2, axis=1
                            )
                        )
            # get the k nearest neighbours from the sorted list of distances
            knn = dists.argsort()[:self.__k]

            # finally get the class label
            predicted.append( self.__votingfx(knn) )

        return predicted


    def getMajorityVote(self, knn_ids):
        """TODO docstring
        """
        # create dictionary with an item for each condition
        votes = dict( zip ( self.__data.uniquelabels,
                            [0 for i in self.__data.uniquelabels ] ) )

        # add 1 to a certain condition per NN
        for nn in knn_ids:
            votes[self.__data.labels[nn]] += 1

        # find the condition with most votes
        best_cond = None
        most_votes = None
        for cond, vote in votes.iteritems():
            if best_cond is None or vote > most_votes:
                best_cond = cond
                most_votes = vote

        return best_cond


    def getWeightedVote(self, knn_ids):
        """TODO docstring
        """

        # create dictionary with an item for each condition
        votes = dict( zip ( self.__data.uniquelabels,
                            [0 for i in self.__data.uniquelabels ] ) )
        weights = dict( zip ( self.__data.uniquelabels,
                    [ 1 - ( float( self.__data.labels.tolist().count(i) ) \
                      / len(self.__data.labels) )
                        for i in self.__data.uniquelabels ] ) )

        for nn in knn_ids:
            votes[self.__data.labels[nn]] += weights[self.__data.labels[nn]]

        # find the condition with most votes
        best_cond = None
        most_votes = None
        for cond, vote in votes.iteritems():
            if best_cond is None or vote > most_votes:
                best_cond = cond
                most_votes = vote

        return best_cond
