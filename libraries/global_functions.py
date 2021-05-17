#############################################################################################################################
######################################################## Global stuff #######################################################
#############################################################################################################################

# Imports
import matplotlib
import matplotlib.pyplot as pyplot
import numpy
import os
import IPython.display as display
import pygsp
import collections.abc as abc
import cProfile
import pyprof2calltree
import scipy.signal
from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.rcParams.update({'font.size': 14.0, 'figure.titlesize':18.0, 'axes.labelsize':16.0, 'xtick.labelsize': 14.0,
                            'ytick.labelsize': 14.0, 'axes.titlesize':18.0, 'image.cmap':'viridis', 'text.color': 'black',
                            'axes.labelcolor': 'black', 'xtick.color': 'black', 'ytick.color': 'black'})

#############################################################################################################################
###################################################### Utlity functions #####################################################
#############################################################################################################################

"""
    Starts profiling execution times in the code.
    --
    In:
        * None.
    Out:
        * None.
"""

def start_profiling () :
    
    # Create global object
    global profiler
    profiler = cProfile.Profile()
    profiler.enable()

#############################################################################################################################

"""
    Stops profiling execution times in the code, and shows results.
    --
    In:
        * None.
    Out:
        * None.
"""

def stop_profiling () :
    
    # Get stats and visualize
    global profiler
    profiler.create_stats()
    pyprof2calltree.visualize(profiler.getstats())

#############################################################################################################################

"""
    Creates the directory for the given file name if it does not exist.
    --
    In:
        * file_name: Directory to create, or file for which we want to create a directory.
    Out:
        * None.
"""

def create_directory_for (file_name) :
    
    # Creates the corresponding directory
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)
    
#############################################################################################################################
####################################################### Plot functions ######################################################
#############################################################################################################################

"""
    Plots multiple curves.
    --
    In:
        * xs: X coordinates (one per curve, or one for all curves).
        * ys: Y coordinates (one per curve).
        * legends: Legends to associate with the curve (one per curve, or nothing).
        * xlabel: X axis label.
        * ylabel: Y axis label.
        * ylabel: Title of the plot.
        * title: Figure title.
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_curves (xs, ys, legends=[], xlabel="", ylabel="", title="", file_name=None) :
    
    # Plot
    figure = pyplot.figure(figsize=(20, 10))
    figure.patch.set_facecolor('white')
    for i in range(len(ys)) :
        actual_legend = "" if len(legends) == 0 else legends[i]
        pyplot.plot(xs[i], ys[i], label=actual_legend)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    if len(legends) > 0 :
        pyplot.legend()
    pyplot.title(title)
    figure.gca().spines["right"].set_visible(False)
    figure.gca().spines["top"].set_visible(False)
    pyplot.tight_layout()
    pyplot.show()
    
    # Save
    if file_name is not None :
        create_directory_for(file_name)
        figure.savefig(file_name, bbox_inches="tight", facecolor = 'white')
        
#############################################################################################################################

"""
    Plots a single curve.
    --
    In:
        * xs: X coordinates.
        * ys: Y coordinates.
        * legend: Legends to associate with the curve.
        * xlabel: X axis label.
        * ylabel: Y axis label.
        * ylabel: Title of the plot.
        * title: Figure title.
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_curve (xs, ys, legend="", xlabel="", ylabel="", title="", file_name=None) :
        
    # Plot
    actual_legend = [] if legend == "" else [legend]
    plot_curves([xs], [ys], actual_legend, xlabel, ylabel, title, file_name)

#############################################################################################################################

"""
    Plots a stem.
    --
    In:
        * values: Values to plot.
        * xticks: Labels associated with the values.
        * ylabel: Y axis label.
        * ylabel: Title of the plot.
        * title: Figure title.
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_stem (values, xticks="", ylabel="", title="", file_name=None, x_lim = None) :
        
    # Plot
    figure = pyplot.figure(figsize=(20, 10))
    figure.patch.set_facecolor('white')
    if x_lim is not None: 
        values = values[x_lim[0]:x_lim[1]]
        
    pyplot.stem(range(len(values)), values, use_line_collection=True)
    pyplot.xticks(range(len(values)), xticks)
    pyplot.ylabel(ylabel)
    pyplot.title(title)
    figure.gca().set_frame_on(False)
    pyplot.tight_layout()
    pyplot.grid(True, linewidth = 0.2)
    pyplot.show()
    
    # Save
    if file_name is not None :
        create_directory_for(file_name)
        figure.savefig(file_name, bbox_inches="tight", facecolor = 'white')

#############################################################################################################################

"""
    Plots a matrix.
    --
    In:
        * matrix: Matrix to plot.
        * rows_labels: Labels associated with the rows.
        * cols_labels: Labels associated with the columns.
        * title: Figure title.
        * colorbar: Set to True to plot a colorbar.
        * round_values: Set to >= 0 to plot values in matrix cells.
        * limits: colorbar limits (by default [min, max])
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_matrix (matrix, rows_labels="", cols_labels="", rows_title="", cols_title="", title="", colorbar=False, round_values=None, limits = None, interpolate = True, file_name=None) :

    # Plot matrix
    if interpolate: interp = 'hanning'
    else: interp = None
    figure, axis = pyplot.subplots(figsize=(20, 20))
    figure.patch.set_facecolor('white')
    if limits is None: cax = axis.matshow(matrix, interpolation = interp)
    else: cax = axis.matshow(matrix, vmin = limits[0], vmax = limits[1], interpolation = interp)
    
    # Add values
    if round_values is not None :
        color_change_threshold = 0.5 * (numpy.max(matrix) + numpy.min(matrix))
        for i in range(matrix.shape[0]) :
            for j in range(matrix.shape[1]) :
                value = round(matrix[i, j], round_values) if round_values > 0 else int(matrix[i, j])
                color = "black" if matrix[i, j] > color_change_threshold else "white"
                axis.text(j, i, str(value), va="center", ha="center", color=color)
    
    # Plot
    pyplot.title(title)
    pyplot.yticks(range(matrix.shape[0]))
    pyplot.ylabel(rows_title)
    pyplot.gca().set_yticklabels(rows_labels)
    pyplot.xticks(range(matrix.shape[1]))
    pyplot.xlabel(cols_title)
    pyplot.gca().set_xticklabels(cols_labels)
    pyplot.tight_layout()
    pyplot.grid(False)
    
    # Add colorbar
    if colorbar:
        divider = make_axes_locatable(axis).append_axes("right", size="5%", pad=0.1)
        pyplot.colorbar(cax, cax = divider)
    
    # Save
    if file_name is not None :
        create_directory_for(file_name)
        figure.savefig(file_name, bbox_inches="tight", facecolor = 'white')

    pyplot.show()

#############################################################################################################################

"""
    Plots a PyGSP graph.
    --
    In:
        * graph: Graph to plot.
        * signal: Signal to plot on vertices.
        * title: Figure title.
        * limits: colorbar limits (by default [min, max])
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_graph (graph, signal=None, title="", file_name=None, limits = None, **kwargs) :
    
    # With or without signal
    figure = pyplot.figure(figsize=(20, 10))
    figure.patch.set_facecolor('white')
    if signal is None:
        if limits is None: graph.plot(ax=figure.gca(), **kwargs)
        else: graph.plot(ax=figure.gca(), limits = limits, **kwargs)
    else :
        if limits is None: graph.plot_signal(signal, ax=figure.gca(), **kwargs)
        else: 
            graph.plot_signal(signal, ax=figure.gca(), limits = limits, **kwargs)
    
    # Plot
    pyplot.title(title)
    pyplot.axis("off")
    pyplot.tight_layout()
    pyplot.show()
    
    # Save
    if file_name is not None :
        create_directory_for(file_name)
        figure.savefig(file_name, bbox_inches="tight", facecolor = 'white')

#############################################################################################################################

"""
    Plots a distribution.
    --
    In:
        * values: Values to analyze.
        * min_x: Minimum value for domain definition (defaults to min observed value).
        * max_x: Maximum value for domain definition (defaults to max observed value).
        * nb_bins: Number of bins for the histogram.
        * xlabel: X axis label to plot.
        * file_name: Where to save the results.
    Out:
        * None.
"""

def plot_distribution (values, min_x=None, max_x=None, nb_bins=100, xlabel="", file_name=None) :
        
    # Compute distribution
    if min_x is None :
        min_x = min(values)
    if max_x is None :
        max_x = max(values)
    bins, probas = to_distribution(values, min_x, max_x, nb_bins=nb_bins)
    
    # Plot histogram
    figure = pyplot.figure(figsize=(20, 10))
    figure.patch.set_facecolor('white')
    pyplot.bar(bins[:-1], probas, width=(bins[1] - bins[0]), align="edge")
    pyplot.xlabel(xlabel)
    pyplot.ylabel("%")
    pyplot.ylim([0, 1])
    pyplot.xlim([min_x, max_x])
    pyplot.tight_layout()
    pyplot.show()
    
    # Save
    if file_name is not None :
        create_directory_for(file_name)
        figure.savefig(file_name, bbox_inches="tight", facecolor = 'white')

#############################################################################################################################
############################################# Graph signal processing functions #############################################
#############################################################################################################################

"""
    Creates a graph with weight matrix.
    --
    In:
        * W: weight matrix.
    Out:
        * graph: A PyGSP sensor graph.
"""

def create_graph (W) :
    
    # PyGSP function
    graph = pygsp.graphs.Graph(W)
    graph.compute_fourier_basis()
    graph.set_coordinates()
    return graph
    
#############################################################################################################################

"""
    Creates a sensor graph.
    --
    In:
        * graph_order: Number of vertices.
    Out:
        * graph: A PyGSP sensor graph.
"""

def create_sensor_graph (graph_order) :
    
    # PyGSP function
    graph = pygsp.graphs.Sensor(graph_order, seed=numpy.random.randint(2**32))
    graph.compute_fourier_basis()
    return graph
    
#############################################################################################################################

"""
    Creates a ring graph.
    --
    In:
        * graph_order: Number of vertices.
    Out:
        * graph: A PyGSP ring graph.
"""

def create_ring_graph (graph_order) :
    
    # PyGSP function
    graph = pygsp.graphs.Ring(graph_order)
    graph.compute_fourier_basis()
    return graph

#############################################################################################################################

"""
    Creates a path graph.
    --
    In:
        * graph_order: Number of vertices.
    Out:
        * graph: A PyGSP path graph.
"""

def create_path_graph (graph_order) :
    
    # PyGSP function
    graph = pygsp.graphs.Path(graph_order)
    graph.compute_fourier_basis()
    return graph

#############################################################################################################################

"""
    Creates a stochastic graph.
    --
    In:
        * *args: StochasticBlockModel positional arguments
        * **kwargs: StochasticBlockModel arguments.
    Out:
        * graph: A PyGSP stochastic graph.
"""

def create_stochastic_graph(*args, **kwargs):
    
    # PyGSP function
    graph = pygsp.graphs.StochasticBlockModel(*args, **kwargs)
    graph.set_coordinates(kind="spring", seed=numpy.random.randint(2**32))
    graph.compute_fourier_basis()
    return graph

#############################################################################################################################

"""
    Returns the neighbors of a vertex in a graph.
    --
    In:
        * graph: PyGSP graph.
        * vertex: Vertex for which to get neighbors.
    Out:
        * neighbors: A list of neighbors of the give vertex.
"""

def get_neighbors (graph, vertex) :
    
    # We get the neighbors in the graph
    neighbors = list(graph.W[vertex].nonzero()[1])
    return neighbors

#############################################################################################################################

"""
    Creates a heat kernel h = exp(-tau*lambda) on a graph.
    --
    In:
        * graph: PyGSP graph.
        * scale: Tau in kernel formula.
    Out:
        * kernel: PyGSP heat kernel.
"""

def create_heat_kernel (graph, scale, normalize = True) :

    # PyGSP kernel
    kernel = pygsp.filters.Heat(graph, scale, normalize = normalize)
    return kernel

#############################################################################################################################

"""
    Computes the spectrogram of a graph signal using a given kernel to generate the window.
    --
    In:
        * graph: PyGSP graph.
        * signal: Signal to analyze.
        * window_kernel: PyGSP Kernel to define the window.
    Out:
        * spectrogram: Spectrogram matrix.
"""

def compute_graph_spectrogram (graph, signal, window_kernel) :
    
    # We localize the window everywhere and report the frequencies
    spectrogram = numpy.zeros((graph.N, graph.N))
    for i in range(graph.N) :
        window = window_kernel.localize(i)
        # print(window)
        windowed_signal = window * signal
        spectrogram[:, i] = graph.gft(windowed_signal) ** 2
    return spectrogram

#############################################################################################################################

"""
    Computes the joint Fourier transform of a signal on multiple graphs.
    --
    In:
        * graphs: List of PyGSP graphs used for the JFT, in order.
        * signal: Signal to transport to spectral domain.
    Out:
        * spectrum: Spectrum of the signal as obtained by JFT.
"""

def compute_jft (graphs, signal) :
    
    # We apply GFTs in order
    spectrum = signal
    transpose_order = [numpy.roll(range(len(graphs)), -i) for i in range(len(graphs))]
    for i in range(len(graphs)) :
        spectrum = numpy.transpose(spectrum, transpose_order[i])
        spectrum = graphs[i].gft(spectrum)
        spectrum = numpy.transpose(spectrum, numpy.argsort(transpose_order[i]))
    return spectrum
    
#############################################################################################################################

"""
    Computes the inverse joint Fourier transform of a spectrum on multiple graphs.
    --
    In:
        * graphs: List of PyGSP graphs used for the IJFT, in order.
        * spectrum: Spectrum to transport to jont graph domain.
    Out:
        * signal: Signal as obtained by IJFT.
"""

def compute_ijft(graphs, spectrum) :
    
    # We apply IGFTs in order
    signal = spectrum
    transpose_order = [numpy.roll(range(len(graphs)), -i) for i in range(len(graphs))]
    for i in range(len(graphs)) :
        signal = numpy.transpose(signal, transpose_order[i])
        signal = graphs[i].igft(signal)
        signal = numpy.transpose(signal, numpy.argsort(transpose_order[i]))
    return signal
    
#############################################################################################################################

"""
    Creates a joint heat kernel on a joint graph.
    --
    In:
        * graphs: List of PyGSP graphs used for the JFT, in order.
        * scales: Scales of the kernel along each dimension
    Out:
        * kernel: PyGSP heat kernel.
"""

def create_joint_heat_kernel (graphs, scales, normalize = True) :
    window_kernel = []
    for i_graph in range(len(graphs)):
        window_kernel.append(pygsp.filters.Heat(graphs[i_graph], scales[i_graph], normalize = normalize))
    return window_kernel #numpy.random.rand(*[graphs[i].N for i in range(len(graphs))])
    
#############################################################################################################################

"""
    Localizes a joint heat kernel on a joint graph.
    --
    In:
        * graphs: List of PyGSP graphs used for the JFT, in order.
        * kernel: Kernel to localize.
        * locations: Where to localize the kernel.
    Out:
        * localized_kernel: Localized kernel in the joint graph domain.
"""

def localize_joint_heat_kernel (graphs, kernel, locations, normalize = False):
    window = numpy.array(1)
    for t in range(len(graphs)):
        window = window*kernel[t].localize(locations[t])
        if t < len(graphs) - 1:
            window = numpy.expand_dims(window, axis = -1) #  Expand dimension
    norm = numpy.linalg.norm(window)
    if numpy.abs(norm) > 1e-6 and normalize: window /= norm
    return window #numpy.random.rand(*[graphs[i].N for i in range(len(graphs))])

#############################################################################################################################

"""
    Computes the spectrogram of a multi-graph signal using a given kernel to generate the window and JFT.
    --
    In:
        * graphs: PyGSP graphs in a list, in order.
        * signal: Signal to analyze.
        * window_kernels: PyGSP Kernel to define the window in a list, in order.
    Out:
        * spectrogram: Spectrogram matrix.
"""

def compute_joint_graph_spectrogram(graphs, signal, window_kernels, normalize = False):
    # We localize the window everywhere and report the frequencies
    spectrogram = numpy.zeros((graphs[0].N, graphs[1].N, graphs[0].N, graphs[1].N))
    for i in range(graphs[0].N) :
        for j in range(graphs[1].N):
            window = localize_joint_heat_kernel(graphs, window_kernels, [i,j], normalize = False)
            windowed_signal = window * signal
            spectrogram[:, :, i, j] = compute_jft(graphs, windowed_signal)**2
    if normalize: spectrogram /= numpy.linalg.norm(spectrogram)
    return spectrogram

#############################################################################################################################
################################################### Complement functions ####################################################
#############################################################################################################################

"""
    Computes the normalization with the thresholded Gaussian kernel weighting function
    --
    In:
        * W: graph to be normalized
        * theta: magnitud 
        * k: threshold
    Out:
        * W_normal: Matrix normalized
"""

def Norm_W(W,Theta,k):
    W_normal = numpy.exp(-(W**2/(2*Theta**2)))
    column = W_normal.columns.to_list()
    W_normal[column] = W_normal[column].where(~(W[column]>k),other=0)
    return W_normal

#############################################################################################################################

"""
    Modify adjoining matrix to maintain a maximum of k neighbors per vertex.
    --
    In:
        * S: Adjacent normalized matrix ( 0 - 1 )
        * n_neigh : Number of neighbors
    Out:
        * A: Matrix with k neighbors per vertex
"""

def Neighboors(S, n_neigh ):
    N = len(S)
    if n_neigh >=  N : 
        A = S
    else :
        A = numpy.zeros((N,N))
        for i in range(N):
            Best_simil = -numpy.sort(-S[i])[0:n_neigh]
            for m in Best_simil :
                j = numpy.where(S[i,] == m)
                A[i,j] = S[i,j]
                A[j,i] = S[i,j]
    return A

#############################################################################################################################

"""
    Create a brownian motion in one signal inside a signals-matrix: X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)
    For more info: https://scipy-cookbook.readthedocs.io/items/BrownianMotion.html
    --
    In:
        * x0: Initial value or numpy array with intial values
        * n: Steps number
        * delta: "Speed" of Wiener process. delta**2*t is the variance in normal distribution
        * dt: Time step
        * out: Array to save the results
    Out:
        * A: Matrix with original signals and brownian motion
"""

def brownian(x0, n, delta, dt = 1, out = None):
    x0 = numpy.asarray(x0)
    r = numpy.random.normal(0.0, delta, x0.shape + (n,))*numpy.sqrt(dt)
    if out is None: out = numpy.empty(r.shape)
    numpy.cumsum(r, axis=-1, out = out)
    out += numpy.expand_dims(x0, axis=-1)
    return out

#############################################################################################################################

"""
    Create a set of signals according to space-temporal graphs eigenvectors.
    --
    In:
        * graphs: PyGSP graphs in a list, in order.
        * sgropus: List of numbers of the desired eigenvectors in spatial graph, for each vertex. By default is choosing one randomly.
        * tgropus: List of numbers of the desired eigenvectors in temporal graph, for each instant. By default is choosing one randomly.
        * ln: Level noisy
        * normalize: Apply (or not) time_series /= numpy.linalg.norm(time_series)
    Out:
        * time_series: Signal matrix in time-space domains.
"""

def eigen_signal(graph, groups = None):
    N = graph.N
    groups = numpy.array(groups)
    if groups is None or len(groups) != N: # Time and space offset same-frequency sinusoidals
        if hasattr(groups, "__iter__"): groups = groups[0]
        if groups is not None: print("[WARNING] len(groups) != graph.N. Groups ignored.")
        if groups is None: groups = numpy.random.choice(range(N))
        signal = graph.U[:,groups]
    else:
        signal = numpy.array([graph.U[i, int(groups[i])] for i in range(N)])
    return signal[:,None] # signal with shape (N,1)

def time_space_signal_gen(graphs, sgroups = None, tgroups = None, ln = 0.0, normalize = True):
    time_series = eigen_signal(graphs[0], sgroups) * eigen_signal(graphs[1], tgroups).T # (V,1) X (1,T) => (V,T)
    if normalize: time_series /= numpy.linalg.norm(time_series) # Signals normalize
    time_series += ln * numpy.random.randn(*time_series.shape) # Add noise
    return time_series
