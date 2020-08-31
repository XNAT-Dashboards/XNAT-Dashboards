import setuptools

long_description = 'This project is a responsive dashboard'\
     ' framework for extensive exploration, monitoring, and reviewing large '\
     'neurological imaging datasets present on the XNAT server instance. '\
     'This dashboard fetches data from any XNAT instance servers and '\
     'generates highly-visualized, summarized representations of complex '\
     'scientific data present on the servers and facilitate user navigation '\
     'through large cohorts. This dashboard is a light-weight, flexible'\
     'and modular framework'

setuptools.setup(
     name='XNAT Dashboards',
     version='0.3.0',
     summary='XNAT data visualization',
     author='Mohammad Asif Hashmi',
     author_email='hashmi.masif@gmail.com',
     url='https://pypi.org/project/xnat-dashboards/',
     include_package_data=True,
     package_data={
          'static': ['xnat_dashboards/app/static/*'],
          'templates': ['xnat_dashboards/app/templates/*']},
     packages=setuptools.find_packages(exclude=('tests')),
     description='XNAT data visualization using Flask and Pyxnat',
     long_description=long_description,
     license='MIT',
     scripts=[
          'bin/run_dashboards.py', 'bin/download_data.py'],
     classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities',
          'Topic :: Internet :: WWW/HTTP',
          'Programming Language :: Python :: 3.6',
     ],
     install_requires=[
          'flask',
          'flask-wtf',
          'pandas',
          'pyxnat',
          'tqdm'
     ],
     platforms='any',
     )