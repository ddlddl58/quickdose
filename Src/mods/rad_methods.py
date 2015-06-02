__author__ = 'radek hofman'

import math
import numpy
import matplotlib.pyplot as plt


def get_lambda(thalf):
    """
    calculates radioactive decay constant from decay half-life
    """

    return math.log(2.)/thalf


def decay(t1, t2, lamb):
    """
    calculates radioactive decay

    t1, t2 - time in second since the end of chain reaction
    lamb - radioactive decay constant
    """

    return (math.exp(-lamb*t1) - math.exp(-lamb*t2))/(lamb*(t2-t1))


def decay_2(t1, t2, lamb1, lamb2, branch12):
    """
    calculates decay of species A1 into species A2 which also decays with lambda2 into a stable isotope

    t1, t2 - time in second since the end of chain reaction
    lamb1, lamb2 - radioactive decay constants of A1 and A2, respectively
    branch12 - branching ratio of decay A1 to A2
    """

    ret = (math.exp(-lamb1*t1) - math.exp(-lamb1*t2))/lamb1 + (math.exp(-lamb2*t2) - math.exp(-lamb2*t1))/lamb2
    ret = ret * branch12 * lamb2 / ((lamb2-lamb1)*(t2-t1))
    return ret


def test_method():
    thalf1 = 66  # * 3600. # Mo-99
    thalf2 = 6  # * 3600.  # Tc-99m
    lamb1 = get_lambda(thalf1)
    lamb2 = get_lambda(thalf2)

    print lamb1, lamb2

    branch = 0.9  # 0.1 goes directly to Tc-99

    timestep = 0.1  # time step in hours or seconds (*3600)
    dimx = 1000  # number of time steps

    a1 = numpy.ones(dimx)     # how much parent nuclide is present?
    a2 = numpy.ones(dimx)*0.  # how much A2 is already present?
    a1_dec = numpy.zeros(dimx)
    a2_dec = numpy.zeros(dimx)

    for t in range(dimx):
        a2_dec[t] = a1[t] * decay_2(t*timestep, (t+1)*timestep, lamb1, lamb2, branch)  # decay of A1 to A2 and to stable
        a2_dec[t] += a2[t] * decay(t*timestep, (t+1)*timestep, lamb2)  # decay of already present A2

        a1_dec[t] = a1[t] * decay(t*timestep, (t+1)*timestep, lamb1)  # decay of already present A1

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.step(range(2,dimx+2), a1_dec, label="parent")
    ax.step(range(2,dimx+2), a2_dec, label="daughter")  # we shist the support to have the value valid the following interval, not preceeding

    ax.set_xlabel("Time step")
    ax.set_ylabel("Activity concentration")
    #plt.ylim(-0.1,1.1)
    ax.set_xlim(0,dimx+1)
    plt.grid()
    plt.legend(loc="best")
    #plt.yscale('log')
    plt.show()

if __name__ == "__main__":
    test_method()