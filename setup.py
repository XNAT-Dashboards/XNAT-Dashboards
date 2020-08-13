import setuptools

long_description = 'This project is about creating a responsive dashboard'
' framework for extensive exploration, monitoring, and reviewing large '
'neurological imaging datasets present on the XNAT server instance. '
'This dashboard will fetch data from any XNAT instance servers and '
'will generate highly-visualized, summarized representations of complex '
'scientific data present on the servers and facilitate user navigation '
'through large cohorts. This dashboard will be a light-weight, flexible and '
'modular framework'

setuptools.setup(
     name='xnat_dashboards',
     version='0.0.1',
     summary='XNAT data visualization',
     author='Grégory Operto, Jordi Huguet, Mohammad Asif Hashmi',
     author_email='goperto@barcelonabeta.org,\
          jhuguet@barcelonabeta.org, hashmi.masif@gmail.com',
     url='',
     include_package_data=True,
     package_data={
          'static': ['xnat_dashboards/app/static/*'],
          'templates': ['xnat_dashboards/app/templates/*']},
     packages=setuptools.find_packages(exclude=('tests')),
     description='XNAT data visualization using Flask',
     long_description=long_description,
     license='MIT',
     classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: OSI Approved :: BSD License',
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
          'tqdm'
     ],
     platforms='any',
     )