from setuptools import setup

setup(
	name="blackjack-environment",
	version="0.1.0",
	description="Simple Blackjack simulation environment with pluggable player strategies",
	author="Florian Krellner",
	license="MIT",
	url="https://github.com/Krellner/blackjack_environment",
	python_requires=">=3.9",
	py_modules=["blackjack", "blackjack_strategies"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Topic :: Games/Entertainment :: Simulation",
	],
	install_requires=[],  # Add dependencies here when strategies require them
)

