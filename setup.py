from setuptools import setup

setup(
    name="gemini",
    version="0.1",
    description="A simple container scheduler",
    author="PacketFire",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: DevOps",
        "Topic :: Containers :: Scheduler",
        "Programming Language :: Python :: 3",
    ],

    keywords="gemini scheduler container",
    packages=["gemini"],

    install_requires=[
        'PyYAML>=3.13'
    ]
)
