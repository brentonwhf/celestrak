import os
import glob
from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize, build_ext
import numpy as np

from src.config import SOURCE_DIRECTORY


if __name__ == "__main__":
    ext_modules = []

    # find all pyx files in subdirectories
    for dir, _, _ in os.walk(SOURCE_DIRECTORY):
        if 'cache' in dir:
            continue
        path_files = glob.glob(os.path.join(dir, '*.pyx'), recursive=False)
        if not path_files:
            continue
        for path_file in path_files:
            # define the relative location of the *.so file
            path_so = os.path.relpath(dir, os.getcwd())
            name_so = os.path.basename(os.path.normpath(path_file))
            name_so = os.path.splitext(name_so)[0]
            path_so = os.path.join(path_so, name_so)
            path_so = path_so.replace(os.sep, ".")
            if path_so[0] == ".":
                path_so = path_so[1:]
            # define the relative location of the pyx files that are to by cythonised
            extension = Extension(
                path_so,
                [os.path.relpath(path_file, os.getcwd())]
            )
            ext_modules.append(extension)
            # assert True

    setup(
        name='package',
        packages=find_packages(),
        cmdclass={'build_ext': build_ext},
        ext_modules=cythonize(ext_modules),
        include_dirs=[np.get_include()]
        # language="c++"
    )


    # parent_time_container = os.path.join(SOURCE_DIRECTORY, "solution")
    # path_time_container = os.path.join(parent_time_container, "time_container.pyx")  # the time container
    # path_time_container_rel = os.path.relpath(path_time_container, os.getcwd())
    # # setup(
    # #     ext_modules=cythonize(
    # #         path_time_container,
    # #     )
    # # )
    #
    # # path_so = parent_time_container
    # # if path_so[0] == os.sep:
    # #     path_so = path_so[1:]
    #
    # # get the relative path between the time container parent path and the current working directory
    #
    #
    #
    # ext_modules = [
    #     Extension(
    #         path_so,    # location of the resulting .so
    #         [path_time_container_rel],
    #     )
    # ]
    #
    #
    # setup(
    #     name='package',
    #     packages=find_packages(),
    #     cmdclass={'build_ext': build_ext},
    #     ext_modules=cythonize(ext_modules),
    #     language="c++"
    #  )
