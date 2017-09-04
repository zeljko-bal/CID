from setuptools import setup, find_packages

setup(name='cid',
    version='0.0.1',
    description='Command Interface Description Language',
    url='hhttps://github.com/zeljko-bal',
    author='Zeljko Bal',
    author_email='zeljko.bal@gmail.com',
    license='MIT',
    keywords="cid dsl command gui cli generator",
    packages=find_packages(),
    install_requires=[
        'textX ==1.5.1', 
        'Jinja2 ==2.9.6', 
        'Js2Py ==0.50'
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'cid_generator=cid.bin.runner:run_cid_generator_cli', 
            'cid_generator_gui=cid.bin.runner:run_cid_generator_gui'
        ],
    },
    zip_safe=False)