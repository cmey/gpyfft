import os
import platform
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py
from Cython.Build import cythonize

CLFFT_DIR = r'/Users/gregor/Devel/clFFT'

CL_INCL_DIRS = []
if 'Windows' in platform.system():
    CL_DIR = os.getenv('AMDAPPSDKROOT')
    CL_INCL_DIRS = [os.path.join(CL_DIR, 'include')]

import Cython.Compiler.Options
Cython.Compiler.Options.generate_cleanup_code = 2

cmdclass = {}
PROJECT = "gpyfft"
# TODO: see https://github.com/matthew-brett/du-cy-numpy

extensions = [
    Extension("gpyfft.gpyfftlib",
              [os.path.join('gpyfft', 'gpyfftlib.pyx')],
              include_dirs=[os.path.join(CLFFT_DIR, 'src', 'include'), ] + CL_INCL_DIRS,
              extra_compile_args=[],
              extra_link_args=[],
              libraries=['clFFT'],
              library_dirs=[os.path.join(CLFFT_DIR, 'src', 'library'), ],
              )
    ]

def copy_clfftdll_to_package():
    import shutil
    shutil.copy(
        os.path.join(CLFFT_DIR, 'src', 'staging', 'clFFT.dll'),
        'gpyfft')

    shutil.copy(
        os.path.join(CLFFT_DIR, 'src', 'staging', 'StatTimer.dll'),
        'gpyfft')
    print("copied clFFT.dll, StatTimer.dll")

package_data = {}
if 'Windows' in platform.system():
    copy_clfftdll_to_package()
    package_data.update({'gpyfft': ['clFFT.dll', 'StatTimer.dll']},)

class build_py(_build_py):
    """
    Enhanced build_py which copies version to the built
    """
    def build_package_data(self):
        """Copy data files into build directory
        Patched in such a way version.py -> silx/_version.py"""
        _build_py.build_package_data(self)
        for package, src_dir, build_dir, filenames in self.data_files:
            if package == PROJECT:
                filename = "version.py"
                target = os.path.join(build_dir, "_" + filename)
                self.mkpath(os.path.dirname(target))
                self.copy_file(os.path.join(filename), target,
                               preserve_mode=False)
                break
cmdclass['build_py'] = build_py


def get_version():
    import version
    return version.strictversion


def get_readme():
    dirname = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dirname, "README.rst"), "r") as fp:
        long_description = fp.read()
    return long_description


install_requires = ["numpy", "pyopencl"]
setup_requires = ["numpy", "cython"]


setup(
    name='gpyfft',
    version=get_version(),
    description='A Python wrapper for the OpenCL FFT library clFFT by AMD',
    url=r"https://github.com/geggo/gpyfft",
    maintainer='Gregor Thalhammer',
    maintainer_email='gregor.thalhammer@gmail.com',
    license='LGPL',
    packages=['gpyfft', "gpyfft.test"],
    ext_modules=cythonize(extensions),
    package_data=package_data,
    long_description=get_readme(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    cmdclass=cmdclass,
    )

