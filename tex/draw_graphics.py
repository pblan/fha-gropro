import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt


def plot_three_phases():
    # function to draw a plot with three phases
    # phase 1: acceleration
    # phase 2: constant velocity
    # phase 3: deceleration

    # create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    # make ratio of the subplots equal
    fig.set_size_inches(21, 3)

    # set the x and y labels
    ax1.set_xlabel("t")
    ax2.set_xlabel("t")
    ax3.set_xlabel("t")

    # set the title
    ax1.set_title("Acceleration $a(t)$")
    ax2.set_title("Velocity $v(t)$")
    ax3.set_title("Distance $s(t)$")

    # set the grid
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)

    t1 = np.arange(0, 5.1, 0.1)
    t2 = np.arange(5, 25.1, 0.1)
    t3 = np.arange(25, 30.1, 0.1)

    # phase 1: acceleration
    a1 = np.ones(len(t1))
    v1 = a1 * t1
    s1 = a1 * t1**2 / 2

    # phase 2: constant velocity
    a2 = np.zeros(len(t2))
    v2 = v1[-1] * np.ones(len(t2))
    s2 = s1[-1] + v2 * (t2 - t2[0])

    # phase 3: deceleration
    a3 = -np.ones(len(t3))
    v3 = v2[-1] + a3 * (t3 - t2[-1])
    s3 = s2[-1] + v2[-1] * (t3 - t2[-1]) + a3 * (t3 - t2[-1]) ** 2 / 2

    # plot the data
    ax1.plot(t1, a1, "r", t2, a2, "r", t3, a3, "r")
    ax2.plot(t1, v1, "b", t2, v2, "b", t3, v3, "b")
    ax3.plot(t1, s1, "g", t2, s2, "g", t3, s3, "g")

    # ax1: show $a_max$ and $-a_max$ in the plot instead of 1 and -1
    ax1.set_yticks([1, 0, -1])
    ax1.set_yticklabels(["$a_{max}$", 0, "$-a_{max}$"])

    # ax2: show $v_{max}$ in the plot instead of 5
    ax2.set_yticks([0, 5])
    ax2.set_yticklabels([0, "$v_{max}$"])

    # ax3: show no ticks
    ax3.set_yticks([0])
    ax3.set_yticklabels([0])
    ax3.set_xticks([])
    ax3.set_xticklabels([])

    # no x ticks
    ax1.set_xticks([])
    ax2.set_xticks([])
    ax3.set_xticks([])

    # vertical lines at the end of each phase
    ax1.axvline(x=5, color="k", linestyle="--")
    ax1.axvline(x=25, color="k", linestyle="--")
    ax1.axvline(x=30, color="k", linestyle="--")

    ax2.axvline(x=5, color="k", linestyle="--")
    ax2.axvline(x=25, color="k", linestyle="--")
    ax2.axvline(x=30, color="k", linestyle="--")

    ax3.axvline(x=5, color="k", linestyle="--")
    ax3.axvline(x=25, color="k", linestyle="--")
    ax3.axvline(x=30, color="k", linestyle="--")

    # $t_a$ and $t_b$ in the plot as xticks
    ax1.set_xticks([5, 25, 30])
    ax1.set_xticklabels(["$t_a$", "$t_b$", "$t_c$"])
    ax2.set_xticks([5, 25, 30])
    ax2.set_xticklabels(["$t_a$", "$t_b$", "$t_c$"])
    ax3.set_xticks([5, 25, 30])
    ax3.set_xticklabels(["$t_a$", "$t_b$", "$t_c$"])

    # draw pattern in the background under the curves
    ax1.fill_between(t1, a1, 0, color="blue", alpha=0.1)
    ax1.fill_between(t2, a2, 0, color="blue", alpha=0.1)
    ax1.fill_between(t3, a3, 0, color="blue", alpha=0.1)

    ax2.fill_between(t1, v1, 0, color="green", alpha=0.1)
    ax2.fill_between(t2, v2, 0, color="green", alpha=0.1)
    ax2.fill_between(t3, v3, 0, color="green", alpha=0.1)

    # save the figure to file_dir + figures + three_phases.png
    plt.savefig("figures/three_phases.png", bbox_inches="tight", dpi=300)


def plot_two_phases():
    # function to draw a plot with two phases
    # phase 1: acceleration
    # phase 2: deceleration

    # create a figure with two subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    # make ratio of the subplots equal
    fig.set_size_inches(21, 3)

    # set the x and y labels
    ax1.set_xlabel("t")
    ax2.set_xlabel("t")
    ax3.set_xlabel("t")

    # set the title
    ax1.set_title("Acceleration $a(t)$")
    ax2.set_title("Velocity $v(t)$")
    ax3.set_title("Distance $s(t)$")

    # set the grid
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)

    t1 = np.arange(0, 10.1, 0.1)
    t2 = np.arange(10, 20.1, 0.1)

    # phase 1: acceleration
    a1 = np.ones(len(t1))
    v1 = a1 * t1
    s1 = a1 * t1**2 / 2

    # phase 2: deceleration
    a2 = -np.ones(len(t2))
    v2 = v1[-1] + a2 * (t2 - t1[-1])
    s2 = s1[-1] + v1[-1] * (t2 - t1[-1]) + a2 * (t2 - t1[-1]) ** 2 / 2

    # plot the data
    ax1.plot(t1, a1, "r", t2, a2, "r")
    ax2.plot(t1, v1, "b", t2, v2, "b")
    ax3.plot(t1, s1, "g", t2, s2, "g")

    # ax1: show $a_max$ and $-a_max$ in the plot instead of 1 and -1
    ax1.set_yticks([1, 0, -1])
    ax1.set_yticklabels(["$a_{max}$", 0, "$-a_{max}$"])

    # ax2: show $v_{max}$ in the plot instead of 10
    ax2.set_yticks([0, 10])
    ax2.set_yticklabels([0, "$v_{max}$"])

    # ax3: show no ticks
    ax3.set_yticks([0])
    ax3.set_yticklabels([0])
    ax3.set_xticks([])
    ax3.set_xticklabels([])

    # no x ticks
    ax1.set_xticks([0])
    ax2.set_xticks([0])

    # vertical lines at the end of each phase
    ax1.axvline(x=10, color="k", linestyle="--")
    ax1.axvline(x=20, color="k", linestyle="--")
    ax2.axvline(x=10, color="k", linestyle="--")
    ax2.axvline(x=20, color="k", linestyle="--")
    ax3.axvline(x=10, color="k", linestyle="--")
    ax3.axvline(x=20, color="k", linestyle="--")

    # $t_a$ in the plot as xticks
    ax1.set_xticks([10, 20])
    ax1.set_xticklabels(["$t_x$", "$2t_x$"])
    ax2.set_xticks([10, 20])
    ax2.set_xticklabels(["$t_x$", "$2t_x$"])
    ax3.set_xticks([10, 20])
    ax3.set_xticklabels(["$t_x$", "$2t_x$"])

    # draw pattern in the background under the curves
    ax1.fill_between(t1, a1, 0, color="blue", alpha=0.1)
    ax1.fill_between(t2, a2, 0, color="blue", alpha=0.1)

    ax2.fill_between(t1, v1, 0, color="green", alpha=0.1)
    ax2.fill_between(t2, v2, 0, color="green", alpha=0.1)

    # save the figure to file_dir + figures + two_phases.png
    plt.savefig("figures/two_phases.png", bbox_inches="tight", dpi=300)


def draw_forced_deceleration():
    # function to draw a plot with three phases
    # phase 1: acceleration
    # phase 2: constant velocity
    # phase 3: deceleration

    # create a figure with three subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # make ratio of the subplots equal
    fig.set_size_inches(14, 3)

    # set the x and y labels
    ax1.set_xlabel("t")
    ax2.set_xlabel("t")

    # set the title
    ax1.set_title("Forced Deceleration in Constant Velocity")
    ax2.set_title("Forced Deceleration in Acceleration")

    # set the grid
    ax1.grid(True)
    ax2.grid(True)

    t1 = np.arange(0, 10.1, 0.1)  # acceleration
    t2 = np.arange(
        10, 30.1, 0.1
    )  # constant velocity until 30, gets forced to decelerate
    t3 = np.arange(15, 25.1, 0.1)  # forced deceleration

    t4 = np.arange(0, 25.1, 0.1)  # acceleration until 30, gets forced to decelerate
    t5 = np.arange(10, 20.1, 0.1)  # forced deceleration

    # phase 1: acceleration
    a1 = np.ones(len(t1))
    v1 = a1 * t1

    a4 = np.ones(len(t4))
    v4 = a4 * t4

    # phase 2: constant velocity
    a2 = np.zeros(len(t2))
    v2 = v1[-1] * np.ones(len(t2))

    # phase 3: deceleration
    a3 = -np.ones(len(t3))
    v3 = v1[-1] + a3 * (t3 - 15)
    v3_2 = v1[-1] * np.ones(len(t3))  # old velocity

    a5 = -np.ones(len(t5))
    v5 = 10 + a5 * (t5 - 10)  # forced deceleration
    v5_2 = v4[-1] - a5 * (t5 - t4[-1])  # old velocity

    # plot the data, t3 and t5 red
    ax1.plot(t1, v1, "b", t2, v2, "b", t3, v3, "r", t3, v3_2, "b--")
    ax2.plot(t4, v4, "b", t5, v5, "r", t5, v5_2, "b--")

    # ax1: show $v_{max}$ in the first plot instead of 10
    ax1.set_yticks([0, 10])
    ax1.set_yticklabels([0, "$v_{max}$"])

    # ax2: show $v_{x}$ in the second plot instead of 15
    ax2.set_yticks([0, 10])
    ax2.set_yticklabels([0, "$v_{x}$"])

    # no x ticks
    # ax1.set_xticks([])
    # ax2.set_xticks([])

    # vertical lines at the end of each phase
    ax1.axvline(x=10, color="k", linestyle="--")
    ax1.axvline(x=15, color="r", linestyle="--")
    ax1.axvline(x=25, color="r", linestyle="--")
    ax2.axvline(x=10, color="r", linestyle="--")
    ax2.axvline(x=20, color="r", linestyle="--")

    # $t_a$ in the plot as xticks
    ax1.set_xticks([10, 15, 25])
    ax1.set_xticklabels(["$t_a$", "$t_b$", "$t_c$"])
    ax2.set_xticks([10, 20])
    ax2.set_xticklabels(["$t_x$", "$2t_x$"])

    # draw pattern in the background under the curves
    # ax1.fill_between(t1, v1, 0, color="blue", alpha=0.1)
    # ax1.fill_between(t2, v2, 0, color="blue", alpha=0.1)
    # ax1.fill_between(t3, v3_2, 0, color="blue", alpha=0.05)
    ax1.fill_between(t3, v3, 0, color="red", alpha=0.1)

    # ax2.fill_between(t4, v4, 0, color="blue", alpha=0.1)
    # ax2.fill_between(t5, v5_2, 0, color="blue", alpha=0.5)
    ax2.fill_between(t5, v5, 0, color="red", alpha=0.1)

    plt.savefig("figures/forced_deceleration.png", bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    plot_three_phases()
    plot_two_phases()
    draw_forced_deceleration()
