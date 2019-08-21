import pip
# pip V10.0.0以上版本需要导入下面的包
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call
from time import sleep
 
for dist in get_installed_distributions():
    # 执行后，pip默认为Python3版本
    # 双版本下需要更新Python2版本的包，使用py2运行，并将pip修改成pip2
    call("pip install --upgrade " + dist.project_name, shell=True)
