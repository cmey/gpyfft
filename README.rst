gpyfft
======

A Python wrapper for the OpenCL FFT library clFFT from AMD

Introduction
------------

AMD has created a open source FFT library for GPU devices based on OpenCL,  called `clFFT
<https://github.com/clMathLibraries/clFFT>`_
(released under Apache 2.0 license).

This python wrapper is designed to tightly integrate with pyopencl. It
consists of a low-level cython based wrapper with an interface similar
to the underlying C library. On top of that it offers a easy-to-use high-level
interface designed to work on data contained in instances of
pyopencl.array.Array, a numpy work-alike array class. The high-level
interface is similar to that of `pyFFTW
<https://github.com/hgomersall/pyFFTW>`_, a python wrapper for the FFTW
library. For details of the high-level interface see `fft.py <gpyfft/fft.py>`_.

Compared to `pyfft <http://github.com/Manticore/pyfft>`_, a python
implementation of Apple's FFT library, AMD's FFT library offers some
additional features such as transform sizes that are powers of 2,3 and
5, and real-to-complex transforms. And on AMD hardware a better
performance can be expected, e.g., gpyfft: 280 Gflops compared to
pyfft: 63 GFlops (for single precision, accurate math,
inplace, transform size 1024x1024, batch size 4, on AMD Cayman, HD6950).


Status
------

This wrapper is functional, the high-level interface is not completely settled.

work done
~~~~~~~~~

-  low level wrapper (mostly) completed
-  high level wrapper: complex (single precision), interleaved data, in
   and out of place (some tests and benchmarking available)
-  creation of pyopencl Events for synchronization

missing features
~~~~~~~~~~~~~~~~

-  debug mode to output generated kernels
-  documentation for low level wrapper (instead refer to library doc)
-  define API for high level interface
-  high-level interface: double precision data, planar data,
   real<->complex transforms
-  high-level interface: tests for non-contiguous data
-  handling of batched transforms in the general case, e.g. shape
   (4,5,6), axes = (1,), i.e., more than one axes where no transform is
   performed. (not always possible with single call for arbitrary
   strides, need to figure out when possible)
-  high-level interface: implement some strategy to deliver optimal performance 
   (e.g. order of transforms along axes for 2D, 3D transforms depending on memory layout)
   
Performance Notes
-----------------

* the memory order and axes order is important, especially for 2d or 3d batched transforms. Benchmarking with AMD GPUs (see `fft.py <gpyfft/fft.py>`_) gives you some hints. As a typical example, a batch of 4 two-dimensional transforms of size 1024x1024 is best performed with a C-contiguous input and output array of shape (4, 1024, 1024), and axes=(2,1) (argument for the gpyfft.FFT). The equivalent (same result) call with axes=(1,2) is 4-5 times slower!

* for other sizes, e.g. batch of 4 1000x1000 transforms, these rule-of-thumb does not hold, so experimenting and benchmarking is necessary to achieve best performance.

Requirements
------------

- python (tested with 2.7, works also with 3.x), with packages

  * pyopencl
  * distribute
  * cython

- clFFT

Building and Installation
-------------------------

1. Install the AMD clFFT library: either use the prebuilt `binaries <https://github.com/clMathLibraries/clFFT/releases>`_, (recommended), or build clFFT from source (see below for some hints.)

2. edit `setup.py` to point to clFFT directory

Then, either:

3. `python setup.py install`

   or for developing::
   
        python bootstrap.py


Detailed build instructions for Windows (64bit), Python 2.7
-----------------------------------------------------------

Requirements
~~~~~~~~~~~~

* C/C++ Compiler. Tested with free compilers (64bit) from Microsoft Windows SDK v7.0, or Microsoft Visual C++ Compiler Package for Python 2.7
* OpenCL environment (tested with AMD APP SDK, 2.9)
* cmake (3.0), only needed if clFFT is built from source

How to build clFFT from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Download clFFT from github::

	git checkout https://github.com/clMathLibraries/clFFT.git

* in `.../clFFT/src`, open SDK command shell (Start - Programs - Microsoft Windows SDK v7.1 - CMD Shell)::

	setenv /Release
	cmake -G "NMake Makefile"
	nmake
	
  or use `cmake-gui`, with source code `.../clFFT/src`, build dir `.../clFFT/src`,
  manually change `CMAKE/CMAKE_BUILD_TYPE` to `Release`
	
  In `.../clFFT/src/staging` should contain `clFFT.dll`.

How to build gpyfft
~~~~~~~~~~~~~~~~~~~

* In `gpyfft/setup.py` check that in setup.py `CLFFT_DIR` points to the clFFT folder, and
  `CL_INCL_DIRS` to the OpenCL headers. Note that the setup script copies the clFFT
  binary libs (clFFT.dll, ...) to the package directory. In case, edit adjust the path settings for the clFFT
  libraries and include files. Path settings are prepared for using the binary distributions on Windows.

* Build and install the wrapper. For Python 2.7 and the free Microsoft compiler, use::
	
	set MSSDK=1
	set DISTUTILS_USE_SDK=1
	python setup.py build
	python setup.py install


Testing
-------

For some basic testing, run in the base directory of this wrapper::

	python bootstrap.py 
   import gpyfft.test
   gpyfft.test.run()

or for some benchmarking::

	python bootstrap.py
   import gpyfft.benchmark 
   gpyfft.benchmark.run()


License:
--------

LGPL

Tested Platforms
----------------

This wrapper has been tested with Python 2.7 both on Windows 7 (64bit) with AMD Radeon
6950 and 285, and OS X 10.7-10.11 with Nvidia GT330M, GT750M, and Intel Iris Pro. 
Should also work with Python 3, thanks to contribution by Nevada Sanchez.

Tested on Linux debian-8 with Intel, AMD and POCL drivers on CPU, Beignet and Nvidia drivers on GPU.

Success reports for more recent systems are welcome!

Contributors
------------

* Gregor Thalhammer
* Keith Brafford
* Nevada Sanchez
* Jerome Kieffer

(C) Gregor Thalhammer 2015
