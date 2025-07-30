from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="roblox-nickname-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Telegram бот для генерации никнеймов для Roblox с помощью ИИ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/roblox-nickname-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "roblox-nickname-bot=bot:main",
        ],
    },
    keywords="telegram bot roblox nickname generator ai openrouter",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/roblox-nickname-bot/issues",
        "Source": "https://github.com/yourusername/roblox-nickname-bot",
    },
)