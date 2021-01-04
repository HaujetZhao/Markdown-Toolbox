# coding=utf-8
'''
====================================================
打包上传命令

先打包：
python setup.py sdist build

再上传：
twine upload "dist/Markdown-Toolbox-1.0.0.tar.gz"

====================================================
测试命令

python setup.py sdist –formats = gztar,zip

====================================================
打包注意事项

打包文件夹里一定不能有中文名的文件，文件名只能用 ascii 码
因为 python 默认使用 utf-8 编码，但是安装到 windows 上的包信息文件
里面的编码是系统的 gbk 编码，读取编码冲突，会出错
导致升级卸载旧包的时候无法查看旧包的文件信息，
无法卸载和升级
'''


from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Markdown-Toolbox',
    version='1.0.0',
    description=(
        '一Markdown 工具箱，是我为 Markdown 笔记管理做的一个工具集。'
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
        'src/misc':['Docs/*.*', '*.ico', '*.icns', '*.jpg', 'style.css']},
    
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