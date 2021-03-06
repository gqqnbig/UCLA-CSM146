"""
Author      : Yi-Chieh Wu, Sriram Sankararaman
Description : Titanic
"""

# Use only the provided packages!
import math
import csv
from util import *
from collections import Counter

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn import metrics

######################################################################
# classes
######################################################################

class Classifier(object) :
    """
    Classifier interface.
    """
    
    def fit(self, X, y):
        raise NotImplementedError()
        
    def predict(self, X):
        raise NotImplementedError()


class MajorityVoteClassifier(Classifier) :
    
    def __init__(self) :
        """
        A classifier that always predicts the majority class.
        
        Attributes
        --------------------
            prediction_ -- majority class
        """
        self.prediction_ = None
    
    def fit(self, X, y) :
        """
        Build a majority vote classifier from the training set (X, y).
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes
        
        Returns
        --------------------
            self -- an instance of self
        """
        majority_val = Counter(y).most_common(1)[0][0]
        self.prediction_ = majority_val
        return self
    
    def predict(self, X) :
        """
        Predict class values.
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
        
        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.prediction_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")
        
        n,d = X.shape
        y = [self.prediction_] * n 
        return y


class RandomClassifier(Classifier) :
    
    def __init__(self) :
        """
        A classifier that predicts according to the distribution of the classes.
        
        Attributes
        --------------------
            probabilities_ -- class distribution dict (key = class, val = probability of class)
        """
        self.probabilities_ = None
    
    def fit(self, X, y) :
        """
        Build a random classifier from the training set (X, y).
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes
        
        Returns
        --------------------
            self -- an instance of self
        """
        
        ### ========== TODO : START ========== ###
        # part b: set self.probabilities_ according to the training set
        cur_dist = Counter(y)
        self.probabilities_ = (float(cur_dist[0.0])/(float(cur_dist[0.0])+float(cur_dist[1.0])))
        ### ========== TODO : END ========== ###
        
        return self
    
    def predict(self, X, seed=1234) :
        """
        Predict class values.
        
        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            seed -- integer, random seed
        
        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.probabilities_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")
        np.random.seed(seed)
        
        ### ========== TODO : START ========== ###
        # part b: predict the class for each test example
        # hint: use np.random.choice (be careful of the parameters)
        y = np.random.choice(2, X.shape[0],p=[self.probabilities_, 1-self.probabilities_])    
        ### ========== TODO : END ========== ###
        
        return y


######################################################################
# functions
######################################################################
def plot_histograms(X, y, Xnames, yname) :
    n,d = X.shape  # n = number of examples, d =  number of features
    fig = plt.figure(figsize=(20,15))
    nrow = 3; ncol = 3
    for i in range(d) :
        fig.add_subplot (3,3,i)  
        data, bins, align, labels = plot_histogram(X[:,i], y, Xname=Xnames[i], yname=yname, show = False)
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xnames[i])
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')
 
    plt.savefig ('histograms.pdf')


def plot_histogram(X, y, Xname, yname, show = True) :
    """
    Plots histogram of values in X grouped by y.
    
    Parameters
    --------------------
        X     -- numpy array of shape (n,d), feature values
        y     -- numpy array of shape (n,), target classes
        Xname -- string, name of feature
        yname -- string, name of target
    """
    
    # set up data for plotting
    targets = sorted(set(y))
    data = []; labels = []
    for target in targets :
        features = [X[i] for i in range(len(y)) if y[i] == target]
        data.append(features)
        labels.append('%s = %s' % (yname, target))
    
    # set up histogram bins
    features = set(X)
    nfeatures = len(features)
    test_range = list(range(int(math.floor(min(features))), int(math.ceil(max(features)))+1))
    if nfeatures < 10 and sorted(features) == test_range:
        bins = test_range + [test_range[-1] + 1] # add last bin
        align = 'left'
    else :
        bins = 10
        align = 'mid'
    
    # plot
    if show == True:
        plt.figure()
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xname)
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')
        plt.show()

    return data, bins, align, labels


def error(clf, X, y, ntrials=100, test_size=0.2) :
    """
    Computes the classifier error over a random split of the data,
    averaged over ntrials runs.
    
    Parameters
    --------------------
        clf         -- classifier
        X           -- numpy array of shape (n,d), features values
        y           -- numpy array of shape (n,), target classes
        ntrials     -- integer, number of trials
    
    Returns
    --------------------
        train_error -- float, training error
        test_error  -- float, test error
    """
    
    ### ========== TODO : START ========== ###
    # compute cross-validation error over ntrials
    # hint: use train_test_split (be careful of the parameters)
    train_error = 0
    test_error = 0
    
    for i in range(0, ntrials):
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=test_size,random_state=i)
        clf.fit(X_train, y_train)                       # fit training data using the classifier
        y_train_pred = clf.predict(X_train)               # take the classifier and run it on the training data
        y_test_pred = clf.predict(X_test)
        train_error += 1 - metrics.accuracy_score(y_train, y_train_pred, normalize=True)
        test_error += 1 - metrics.accuracy_score(y_test, y_test_pred, normalize=True)
    
    train_error = train_error/ntrials
    test_error = test_error/ntrials
    ### ========== TODO : END ========== ###
    
    return train_error, test_error

def error_partial(clf, X, y, ntrials=100, test_size=0.2, partial_amt=10) :
    """
    Computes the classifier error over a random split of the data,
    averaged over ntrials runs.
    
    Parameters
    --------------------
        clf         -- classifier
        X           -- numpy array of shape (n,d), features values
        y           -- numpy array of shape (n,), target classes
        ntrials     -- integer, number of trials
        partial_amt -- integer, what percentage of the training data to use (1=10%)
        
    Returns
    --------------------
        train_error -- float, training error
        test_error  -- float, test error
    """
    
    ### ========== TODO : START ========== ###
    # compute cross-validation error over ntrials
    # hint: use train_test_split (be careful of the parameters)
    partial_amt = partial_amt/10.0
    train_error = 0
    test_error = 0
    
    for i in range(0, ntrials):
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=test_size,random_state=i)
        X_train = X_train[:int(len(X_train)*partial_amt)]
        y_train = y_train[:int(len(y_train)*partial_amt)]
        clf.fit(X_train, y_train)                       # fit training data using the classifier
        y_train_pred = clf.predict(X_train)             # take the classifier and run it on the training data
        y_test_pred = clf.predict(X_test)
        train_error += 1 - metrics.accuracy_score(y_train, y_train_pred, normalize=True)
        test_error += 1 - metrics.accuracy_score(y_test, y_test_pred, normalize=True)
    train_error = train_error/ntrials
    test_error = test_error/ntrials
    ### ========== TODO : END ========== ###
    
    return train_error, test_error

def write_predictions(y_pred, filename, yname=None) :
    """Write out predictions to csv file."""
    out = open(filename, 'wb')
    f = csv.writer(out)
    if yname :
        f.writerow([yname])
    f.writerows(list(zip(y_pred)))
    out.close()


######################################################################
# main
######################################################################

def main():
    # load Titanic dataset
    titanic = load_data("titanic_train.csv", header=1, predict_col=0)
    X = titanic.X; Xnames = titanic.Xnames
    y = titanic.y; yname = titanic.yname
    n,d = X.shape  # n = number of examples, d =  number of features
    
    
    #========================================
    # part a: plot histograms of each feature
    # print('Plotting...')
    # for i in range(d) :
        # plot_histogram(X[:,i], y, Xname=Xnames[i], yname=yname)

       
    #========================================
    # train Majority Vote classifier on data
    print('Classifying using Majority Vote...')
    majVoteClf = MajorityVoteClassifier() # create MajorityVote classifier, which includes all model parameters
    majVoteClf.fit(X, y)                  # fit training data using the classifier
    y_pred = majVoteClf.predict(X)        # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)
    
    
    
    ### ========== TODO : START ========== ###
    # part b: evaluate training error of Random classifier
    print('Classifying using Random...')
    ranClf = RandomClassifier() # create Randomclassifier classifier, which includes all model parameters
    ranClf.fit(X, y)            # fit training data using the classifier
    y_pred = ranClf.predict(X)  # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part c: evaluate training error of Decision Tree classifier
    # use criterion of "entropy" for Information gain 
    print('Classifying using Decision Tree...')
    decTrClf = DecisionTreeClassifier(criterion="entropy") # create DecisionTreeClassifier classifier, which includes all model parameters
    decTrClf.fit(X, y)                                     # fit training data using the classifier
    y_pred = decTrClf.predict(X)                           # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)
    ### ========== TODO : END ========== ###

    

    # note: uncomment out the following lines to output the Decision Tree graph
    """
    # save the classifier -- requires GraphViz and pydot
    import StringIO, pydot, pydotplus
    from sklearn import tree
    dot_data = StringIO.StringIO()
    tree.export_graphviz(decTrClf, out_file=dot_data,
                         feature_names=Xnames)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf("dtree.pdf") 
    """




    ### ========== TODO : START ========== ###
    # part d: evaluate training error of k-Nearest Neighbors classifier
    # use k = 3, 5, 7 for n_neighbors 
    print('Classifying using k-Nearest Neighbors...')
    nN3Clf = KNeighborsClassifier(n_neighbors=3) # create KNeighborsClassifier classifier, which includes all model parameters
    nN3Clf.fit(X, y)                             # fit training data using the classifier
    y_pred = nN3Clf.predict(X)                   # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error for 3-Nearest Neighbors...: %.3f' % train_error)
    
    nN5Clf = KNeighborsClassifier(n_neighbors=5) # create KNeighborsClassifier classifier, which includes all model parameters
    nN5Clf.fit(X, y)                             # fit training data using the classifier
    y_pred = nN5Clf.predict(X)                   # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error for 5-Nearest Neighbors...: %.3f' % train_error)
    
    nN7Clf = KNeighborsClassifier(n_neighbors=7) # create KNeighborsClassifier classifier, which includes all model parameters
    nN7Clf.fit(X, y)                             # fit training data using the classifier
    y_pred = nN7Clf.predict(X)                   # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error for 7-Nearest Neighbors...: %.3f' % train_error)
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part e: use cross-validation to compute average training and test error of classifiers
    print('Investigating various classifiers...')

    clfErr = error(majVoteClf, X, y)
    print('    For Majority Vote classifier:')
    print('\t-- training error: %.3f' % clfErr[0])
    print('\t-- testing error: %.3f' % clfErr[1])
    
    clfErr = error(ranClf, X, y)
    print('    For Random classifier:')
    print('\t-- training error: %.3f' % clfErr[0])
    print('\t-- testing error: %.3f' % clfErr[1])
    
    clfErr = error(decTrClf, X, y)
    print('    For Decision Tree classifier:')
    print('\t-- training error: %.3f' % clfErr[0])
    print('\t-- testing error: %.3f' % clfErr[1])
    
    clfErr = error(nN5Clf, X, y)
    print('    For 5-Nearest Neighbors classifier:')
    print('\t-- training error: %.3f' % clfErr[0])
    print('\t-- testing error: %.3f' % clfErr[1])
    ### ========== TODO : END ========== ###



    ### ========== TODO : START ========== ###
    # part f: use 10-fold cross-validation to find the best value of k for k-Nearest Neighbors classifier
    print('Finding the best k for K-Nearest-Neighbors classifier...')
    for i in range(1,50,2):
        curKNNClf = KNeighborsClassifier(n_neighbors=i)
        scores = cross_val_score(curKNNClf, X, y, cv=10)
        print('\t-- training error for %g-Nearest Neighbors...: %.3f' % (i, 1-np.mean(scores)))
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part g: investigate decision tree classifier with various depths
    print('Investigating depths...')
    for i in range(1,21):
        curDecTreeClf = DecisionTreeClassifier(criterion="entropy",max_depth=i)
        clfErr = error(curDecTreeClf, X, y)
        print('\t-- error for %g-depth decision tree... --training error: %.3f & --testing error: %.3f' % (i, clfErr[0], clfErr[1]))
    ### ========== TODO : END ========== ###
    
    
    
    ### ========== TODO : START ========== ###
    # part h: investigate Decision Tree and k-Nearest Neighbors classifier with various training set sizes
    print('Investigating training set sizes...')
    decTreeClf = DecisionTreeClassifier(max_depth=6)
    kNNClf = KNeighborsClassifier(n_neighbors=7)
    
    for i in range(1, 11, 1):
        decTreeErr = error_partial(decTreeClf, X, y, 100, 0.1, i)    
        kNNErr = error_partial(kNNClf, X, y, 100, 0.1, i)    
        print('    Using %g%% of training data...' % (i*10))
        print('\t-- error for decision tree...       --training error: %.3f & --testing error: %.3f' % (decTreeErr[0], decTreeErr[1]))
        print('\t-- error for K-Nearest Neighbors... --training error: %.3f & --testing error: %.3f' % (kNNErr[0], kNNErr[1]))
    ### ========== TODO : END ========== ###
    
       
    print('Done')


if __name__ == "__main__":
    main()
