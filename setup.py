import os
from setuptools import setup, find_packages, Command

class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info /tmp/gonullu/* /tmp/varpisi/*')

setup(
    name='Gonullu',
    version='1.1.6',
    description='Pisi Linux gonullu paket derleme uygulamasi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PisiLinuxNew/gonullu',
    author='Ilker Manap',
    author_email='ilkermanap@gmail.com',
    maintainer='Muhammet Dilmac',
    maintainer_email='iletisim@muhammetdilmac.com.tr',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'docker>=5.0.0',
        'psutil',
        'colorama',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'gonullu=gonullu.gonullu:main',
        ],
    },
    include_package_data=True,
    package_data={
        'gonullu': ['config/*.yml']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False,
    cmdclass={
        'clean': CleanCommand,
    }
)
