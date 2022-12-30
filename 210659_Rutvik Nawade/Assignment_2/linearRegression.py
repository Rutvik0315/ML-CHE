import numpy as np
import matplotlib.pyplot as plt


def h(theta, X):
    return np.dot(theta, np.transpose(X))


def costFun(theta, X_train, Y_train):
    totalcost = 0
    m= Y_train.shape[0]
    for i in range(Y_train.shape[0]):
        totalcost += (Y_train[i]-np.dot(X_train[i],theta))**2

    totalcost = totalcost/(2*m)
    return totalcost


def diffcostFun(theta, X_train, Y_train):
    m = Y_train.shape[0]
    diff = np.matmul(np.transpose(X_train), (np.matmul(X_train, theta) - Y_train)) / m
    return diff


def fitGD(X_train, Y_train, alpha, lamb_in, ToR, iterations, theta_in):
    J_history = np.zeros(iterations)
    # p_history = np.zeros(1)
    theta = theta_in
    m = X_train.shape[0]
    print(m)
    n = len(theta)
    print(theta)
   # X_train = np.concatenate([np.ones(m).reshape(m, 1), X_train], axis=1)
    # reg_dj_dtheta = np.zeros(n)

    if ToR == 1:
        for i in range(iterations):
            reg_cost = 0.0
            reg_dj_dtheta = np.zeros(n)
            for j in range(n):
                reg_cost += np.absolute(theta[j])
                reg_dj_dtheta[j] += lamb_in / (2 * m)

            reg_cost = (reg_cost * lamb_in) / (2 * m)
            dj_dtheta = np.add(diffcostFun(theta, X_train, Y_train), reg_dj_dtheta)
            theta = theta - alpha * dj_dtheta
            J_history[i] = (costFun(theta, X_train, Y_train) + reg_cost)

    if ToR == 2:
        for i in range(iterations):
            reg_cost = 0
            reg_dj_dtheta = np.zeros((n,))
            for j in range(n):
                reg_cost += (theta[j] ** 2)
                reg_dj_dtheta[j] += (lamb_in / m) * theta[j]

            reg_cost = (reg_cost * lamb_in) / (2 * m)
            dj_dtheta = np.add(diffcostFun(theta, X_train, Y_train), reg_dj_dtheta)
            theta = theta - alpha * dj_dtheta
            # print(theta)
            J_history[i] = (costFun(theta, X_train, Y_train) + reg_cost)

    if ToR == 3:
        for i in range(iterations):
            reg_cost = 0
            reg_dj_dtheta = np.zeros((n,))
            for j in range(n):
                reg_cost += 0.5 * (theta[j] ** 2) + 0.5 * np.absolute(theta[j])
                reg_dj_dtheta[j] += 0.5 * (lamb_in / m) * theta[j] + 0.5 * lamb_in / (2 * m)

            reg_cost = (reg_cost * lamb_in) / (2 * m)
            dj_dtheta = np.add(diffcostFun(theta, X_train, Y_train), reg_dj_dtheta)
            theta = theta - alpha * dj_dtheta
            J_history[i] = (costFun(theta, X_train, Y_train) + reg_cost)

    plt.plot(J_history)
    plt.show()
    return theta


def wm(X_train, tau, x):
    m = X_train.shape[0]
    w = np.mat(np.eye(m))

    for i in range(m):
        xi = X_train[i]
        d = (-2 * tau * tau)
        w[i, i] = np.exp(np.dot((xi - x), (xi - x).T) / d)

    return w


def locallyWeighted(y,X_train, Y_train, tau):
    x=y
    x_ = np.array([1, x])
    w = wm(X_train, tau, x_)
    theta = np.linalg.pinv(X_train.T * (w * X_train)) * (X_train.T * (w * Y_train))
    y = np.dot(x_, theta)

    return float(y[0][0])


def fitNormal(X_train, Y_train):
    return np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X_train), X_train)), np.transpose(X_train)), Y_train)


"""
X_train1 = np.array([[2.5, 4.7, 5.2, 7.3, 9.5, 11.5]])
Y_train1 = np.array([[5.21, 7.70, 8.30, 11, 14.5, 15]])
X_train1 = np.transpose(X_train1)
m = X_train1.shape[0]
X_train1 = np.concatenate([np.ones(m).reshape(m, 1), X_train1], axis=1)
Y_train1 = np.transpose(Y_train1)
print(X_train1)
# print(locallyWeighted(X_train,Y_train,5,0.5))
theta_in1 = np.ones(X_train1.shape[1])
print(theta_in1)print(fitGD(X_train1, Y_train1, 0.01, 5, 3, 5000, theta_in1))
"""