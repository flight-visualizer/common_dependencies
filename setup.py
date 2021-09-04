from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AWS Services',
    url='',
    author='Michael Clark',
    author_email='michaeldavidclark13@gmail.com',
    # Needed to actually package something
    packages=['aws_services'],
    # Needed for dependencies
    install_requires=['pydantic'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)