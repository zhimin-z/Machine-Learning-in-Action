import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
try:
    from sklearn.model_selection import GridSearchCV, train_test_split
except:
    from sklearn.grid_search import GridSearchCV
    from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris


def plot_cross_val_selection():
    iris = load_iris()
    X_trainval, X_test, y_trainval, y_test = train_test_split(iris.data,
                                                              iris.target,
                                                              random_state=0)

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],
                  'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}
    grid_search = GridSearchCV(SVC(), param_grid, cv=5)
    grid_search.fit(X_trainval, y_trainval)
    scores = grid_search.grid_scores_[15:]

    best = np.argmax([x.mean_validation_score for x in scores])
    plt.figure(figsize=(10, 3))
    plt.xlim(-1, len(scores))
    plt.ylim(0, 1.1)
    for i, score in enumerate(scores):
        marker_cv, = plt.plot([i] * 5, score.cv_validation_scores, '^', c='gray', markersize=5, alpha=.5)
        marker_mean, = plt.plot(i, score.mean_validation_score, 'v', c='none', alpha=1, markersize=10)
        if i == best:
            marker_best, = plt.plot(i, score.mean_validation_score, 'o', c='red', fillstyle="none", alpha=1, markersize=20, markeredgewidth=3)

    plt.xticks(range(len(scores)), [str(score.parameters).strip("{}").replace("'", "") for score in scores], rotation=90);
    plt.ylabel("validation accuracy")
    plt.xlabel("parameter settings")
    plt.legend([marker_cv, marker_mean, marker_best], ["cv accuracy", "mean accuracy", "best parameter setting"], loc=(1.05, .4))


def plot_grid_search_overview():
    plt.figure(figsize=(10, 3))
    axes = plt.gca()
    axes.yaxis.set_visible(False)
    axes.xaxis.set_visible(False)
    axes.set_frame_on(False)
    #axes.invert_yaxis()
    def draw(ax, text, start, target=None):
        if target is not None:
            patchB = target.get_bbox_patch()
            end = target.get_position()
        else:
            end = start
            patchB = None
        annotation = ax.annotate(text, end, start, xycoords='axes pixels', textcoords='axes pixels', size=20,
                    arrowprops=dict(arrowstyle="-|>", fc="w", ec="k", patchB=patchB,
                                   connectionstyle="arc3,rad=0.0"),
                    bbox=dict(boxstyle="round", fc="w"), horizontalalignment="center", verticalalignment="center")
        plt.draw()
        return annotation

    step = 100
    grr = 400

    final_evaluation = draw(axes, "final evaluation", (5 * step, grr - 3 * step))
    retrained_model = draw(axes, "retrained model", (3 * step, grr - 3 * step), final_evaluation)
    best_parameters = draw(axes, "best parameters", (.5 * step, grr - 3 * step), retrained_model)
    cross_validation = draw(axes, "cross validation", (.5 * step, grr - 2 * step), best_parameters)
    parameters = draw(axes, "parameter grid", (0.0, grr - 0), cross_validation)
    training_data = draw(axes, "training data", (2 * step, grr - step), cross_validation)
    draw(axes, "training data", (2 * step, grr - step), retrained_model)
    test_data = draw(axes, "test data", (5 * step, grr - step), final_evaluation)
    draw(axes, "data set", (3.5 * step, grr - 0.0), training_data)
    data_set = draw(axes, "data set", (3.5 * step, grr - 0.0), test_data)
    plt.ylim(0, 1)
    plt.xlim(0, 1.5)
