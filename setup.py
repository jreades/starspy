#/usr/bin/env python

from numpy.distutils.misc_util import Configuration
from numpy.distutils.core import setup

DESCRIPTION = "Cross-section, time series, and panel data analysis and visualization toolkit"
LONG_DESCRIPTION = """
"""

DISTNAME = 'starspy'
LICENSE = 'BSD'
MAINTAINER = "Sergio J. Rey"
MAINTAINER_EMAIL = "sjsrey@gmail.com"
URL = "http://starspy.googlecode.com"
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console :: GUI',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research :: Education',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: GIS',
]

MAJOR = 1
MINOR = '0beta'

def get_version():
    return '%s.%s' % (MAJOR, MINOR)


def configuration(parent_package='', top_path=None):
    config = Configuration(None, parent_package, top_path,
                           version=get_version())
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('starspy')
    return config

if __name__ == '__main__':
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          platforms='any',
          configuration=configuration)
