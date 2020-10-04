# coding=utf-8
# python setup.py sdist build
# python setup.py sdist –formats = gztar,zip
# twine upload "dist/Markdown-Toolbox-0.0.01.tar.gz"
# 这是用于上传 pypi 前打包用的


from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Markdown-Toolbox',
    version='0.0.01',
    description=(
        '一款轻量、强大、好用的视频处理软件。'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HaujetZhao/Markdown-Toolbox',
    author='Haujet Zhao',
    author_email='1292756898@qq.com',
    maintainer='Haujet Zhao',
    maintainer_email='1292756898@qq.com',
    license='MPL-2.0 License',
    install_requires=[ # 需要额外安装的包
        'PySide2'
        ],
    packages=['src',
              'src/misc',
              'src/moduels/component',
              'src/moduels/function',
              'src/moduels/gui',
              'src/moduels/thread'], # 需要打包的本地包（package）
    package_data={ # 每个本地包中需要包含的另外的文件
        'src': ['*.md',
                'style.css', 
                'requirements.txt'],
        'src/misc':['Docs/*.*', '*.ico', '*.icns', '*.jpg']},
    
    entry_points={  # Optional console gui
        'gui_scripts': [
            'Markdown-Toolbox=src.__init__:main',
            'MarkdownToolbox=src.__init__:main'
        ]},
    
    
    platforms=["all"],
    
    classifiers=[  
        # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        
        # Indicate who your project is intended for     https://pypi.org/classifiers/
        'Intended Audience :: End Users/Desktop',
        'Topic :: Documentation',

        # Pick your license as you wish
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        ],
    python_requires='>=3.5, <4',
    
)