from setuptools import setup

requirements = [
    'requests', 'PyQt5', 'pytest', 'PyQtWebEngine', 'pygments'
]

setup(
    name='AMDA_SciQLop_Speed_tester',
    version='0.0.1',
    description="A simple program to check link speed of both AMDA and SciQLop server from anywhere",
    author="AMDA_SciQLop_Speed_tester",
    author_email='alexis.jeandet@member.fsf.org',
    url='https://github.com/jeandet/AMDA_SciQLop_Speed_tester',
    packages=['amda_sciqlop_speed_tester', 'amda_sciqlop_speed_tester.images',
              'amda_sciqlop_speed_tester.tests', 'amda_sciqlop_speed_tester.amda_tester',
              'amda_sciqlop_speed_tester.network_probes', 'amda_sciqlop_speed_tester.sciqlop_tester',
              'amda_sciqlop_speed_tester.simple_downloads', 'amda_sciqlop_speed_tester.speed_teser_sequence',
              'amda_sciqlop_speed_tester.time_measurement'
              ],
    package_data={'amda_sciqlop_speed_tester.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'AMDA_SciQLop_Speed_tester=amda_sciqlop_speed_tester.speed_tester:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='AMDA_SciQLop_Speed_tester',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
