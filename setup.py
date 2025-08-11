from setuptools import setup, find_packages

setup(
    name='ninpost',
    version='0.0.1',
    packages=find_packages(),
    description='',
    long_description='''''',
    url='https://github.com/uesseu/ninpost',
    author='Shoichiro Nakanishi',
    author_email='sheepwing@kyudai.jp',
    license='MIT',
    zip_safe=False,
    install_requires=["openai"],
    entry_points={
        "console_scripts": [
            "ninpost=ninpost.ninpost:main",
        ]
    },
)
