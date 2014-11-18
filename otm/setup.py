from setuptools import setup

setup(
    name='otm',
    version='0.1',
    description='One, two, many. Deploy jobs on HPC',
    author='Brian McFee',
    author_email='brian.mcfee@nyu.edu',
    url='http://github.com/bmcfee/nyu-hpc',
    download_url='http://github.com/bmcfee/nyu-hpc/releases',
    long_description="""\
        One, two, many. Deploy jobs on HPC
    """,
    scripts=['otm'],
    classifiers=[
        "License :: OSI Approved :: ISC",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Text Processing :: Markup",
    ],
    keywords='web template',
    license='ISC',
    install_requires=[
        'jinja2',
    ],
    package_data={'': ['templates/*']},
)
