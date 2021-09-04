from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='services',
    url='https://github.com/flight-visualizer/common_dependencies',
    author='Michael Clark',
    author_email='michaeldavidclark13@gmail.com',
    # Needed to actually package something
    # Needed for dependencies
    install_requires=['pydantic', 'requests'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    packages=find_packages(),
    py_modules=['DynamoService', 'RequestService']
)