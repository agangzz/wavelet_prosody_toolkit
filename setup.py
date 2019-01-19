#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AUTHOR
    - Antti Suni <antti.suni@helsinki.fi>
    - Sébastien Le Maguer <slemaguer@coli.uni-saarland.de>

DESCRIPTION
    Setup script file

LICENSE
    See https://github.com/seblemaguer/wavelet_prosody_toolkit/blob/master/LICENSE.txt
"""

# Needed imports
from setuptools import setup, find_packages


# Define meta-informations variable
REQUIREMENTS = [
    # Configuration
    "pyyaml",

    # Math
    "pycwt", "matplotlib", "numpy", "scipy",

    # Audio/speech
    "soundfile", "tgt", "wavio",

    # Rendering
    "pyqt5"
]

EXTRA_REQUIREMENTS = {
    'reaper': ["pyreaper"]
}

NAME = 'wavelet-prosody-toolkit'
VERSION = '1.0b1'
RELEASE = '1.0'
DESCRIPTION = 'Prosody wavelet analysis toolkit'
AUTHOR = 'Antti Suni'


# If sphinx available, enable documentation building
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'build_sphinx': BuildDoc}
    command_options = {
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', VERSION),
            'release': ('setup.py', RELEASE)
        }
    }
except Exception:
    cmdclass = {}
    command_options = {}

# The actual setup
setup(
    # Project info.
    name=NAME,
    version=RELEASE,

    # Author info.
    author=AUTHOR,
    author_email='antti.suni@helsinki.fi',

    # Install requirements
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,

    # Documentation generation
    cmdclass=cmdclass,
    command_options=command_options,

    # Packaging
    packages=find_packages(),  # FIXME: see later to exclude the test (which will be including later)
    package_data={'': ['configs/default.yaml', 'configs/synthesis.yaml']},
    include_package_data=True,

    # Meta information to sort the project
    classifiers=[
        'Development Status :: 4 - Beta',

        # Audience
        'Intended Audience :: Science/Research',

        # Topics
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Python version (FIXME: fix the list of python version based on travis results)
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    # "Executable" to link
    entry_points={
        'console_scripts': [
            'prosody_labeller = wavelet_prosody_toolkit.prosody_labeller:main',
            'cwt_analysis_synthesis = wavelet_prosody_toolkit.cwt_analysis_synthesis:main',
        ],
        'gui_scripts': [
            'wavelet_gui = wavelet_prosody_toolkit.wavelet_gui:main'
        ]
    }
)
