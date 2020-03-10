#!/usr/bin/env python3
from setuptools import setup, find_packages
import versioneer
import os
import shutil
import distutils.cmd
import distutils.log
import sys

try:
    import requests
except ImportError:
    pass

name = 'covidfefe'
description = 'Visualizing COVID-19 data. A perfect image'
version = versioneer.get_version()
sphinx_version = '.'.join(version.split('.')[:3])

cmd_classes = versioneer.get_cmdclass()

if 'requests' in sys.modules:
    class HydraPostCommand(distutils.cmd.Command):
        description = 'upload sphinx documentation to Hydra'
        user_options = []

        def initialize_options(self):
            self.metadata = {
                    'name': name,
                    'version': sphinx_version,
                    'description': description,
            }
            self.address = 'https://docs.stl.gtri.org/hmfd'

        def finalize_options(self):
            pass

        def run(self):
            zippath = 'archive.zip'
            shutil.make_archive('archive', 'zip', root_dir='doc/build/html/')
            filename = os.path.basename(zippath)
            r = requests.post(
                    self.address,
                    data=self.metadata,
                    files={zippath: (filename, open(zippath, 'rb'))})
            r.raise_for_status()
            if r.json()['success']:
                print('Upload of {}-{} to {} successful.'.format(
                    self.metadata['name'],
                    self.metadata['version'],
                    self.address))
            os.remove(zippath)

    cmd_classes['upload_docs'] = HydraPostCommand

    class HydraDeleteCommand(distutils.cmd.Command):
        description = 'deletes a documentation version on Hydra'
        user_options = [
            ('version=', 'v', 'Specify the version to delete or "all" to delete project.')
        ]

        def initialize_options(self):
            self.version = sphinx_version
            self.project_name = name
            self.address = 'https://docs.stl.gtri.org//hmfd'
            self.tmpl = "{}?name={}&{}={}"

        def finalize_options(self):
            assert self.version is not None, 'Invalid version!'

        def run(self):
            if self.version == 'all':
                r = requests.delete(self.tmpl.format(
                    self.address, self.project_name, 'entire_project', True))
            else:
                r = requests.delete(self.tmpl.format(
                    self.address, self.project_name, 'version', self.version))

            r.raise_for_status()
            if r.json()['success']:
                if self.version == 'all':
                    print(
                        'Delete of entire project from {} successful.'.format(
                            self.address
                        )
                    )
                else:
                    print('Delete of {}-{} from {} successfull.'.format(
                        self.project_name, self.version, self.address))

    cmd_classes['delete_docs'] = HydraDeleteCommand

setup(
    name=name,
    version=version,
    cmdclass=cmd_classes,
    packages=find_packages(exclude=['tests']),
    description=description,
    author='Christopher Howard',
    author_email='christopher.howard@gtri.gatech.edu',
    license='Copyright 2020 Christopher Howard',
    python_requires='>=3.4',
    setup_requires=[
    ],
    install_requires=[
        'plotly',
        'pandas',
        'matplotlib',
        'dash',
        'dash_core_components',
        'dash_html_components'
    ],
    entry_points={
        'console_scripts': [
        ]
    },
)
