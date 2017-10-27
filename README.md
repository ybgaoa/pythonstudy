# 项目介绍

# 开发环境准备---
### 安装python包管理和虚拟环境管理器
```
sudo apt-get install -y python-pip
sudo pip install virtualenv virtualenvwrapper
```
### 修改~/.profile或其它环境变量相关文件(如.bashrc)，添加以下语句
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/workspace
source /usr/local/bin/virtualenvwrapper.sh
```
### 修改后使之立即生效(也可以重启终端使之生效)
```
source ~/.profile
```
### 创建项目的python虚拟环境,名称是pythonstudy
```
mkvirtualenv pythonstudy
workon pythonstudy
```
### virtualenv的其它操作示例
```
mkvirtualenv pythonstudy：创建运行环境pythonstudy
workon pythonstudy: 工作在 pythonstudy 环境 或 从其它环境切换到 pythonstudy 环境
deactivate: 退出终端环境
rmvirtualenv pythonstudy：删除运行环境cloudgo
mkproject mic：创建mic项目和运行环境mic
mktmpenv：创建临时运行环境
lsvirtualenv: 列出可用的运行环境
lssitepackages: 列出当前环境安装了的包
```
### 安装项目依赖的Django环境和其它依赖包，在项目路径下执行
```
sudo apt-get install -y libmysqlclient-dev libjpeg-dev
pip install -r requirements.txt
```
### 启动项目，通过Django启动server
```
./manage.py runserver
```

# 依赖项目安装
```
1、进入你的env环境：source activate
2、clone 依赖的项目：比如 git clone -b stable/ocata https://github.com/openstack/python-novaclient.git
3、安装：
   1) cd python-novaclient
   2) 如果文件夹下存在requirements.txt，请执行 pip install -r requirements.txt
   3) python setup.py install
```
