from setuptools import find_packages, setup

import djangocms_tools


INSTALL_REQUIREMENTS = [
    'Django>=1.11,<2.1',
    'django-cms>=3.4.0',
]


setup(
    name='djangocms-tools',
    packages=find_packages(),
    include_package_data=True,
    version=djangocms_tools.__version__,
    description=djangocms_tools.__doc__,
    long_description=open('README.rst').read(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    install_requires=INSTALL_REQUIREMENTS,
    author='Divio AG',
    author_email='info@divio.ch',
    url='http://github.com/divio/djangocms-tools',
    license='BSD',
)
