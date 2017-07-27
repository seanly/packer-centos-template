RELEASE=`rpm -q --qf "%{VERSION}" $(rpm -q --whatprovides redhat-release)`
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${RELEASE}.noarch.rpm
yum -y install gcc make gcc-c++ kernel-devel-`uname -r` perl wget bzip2
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget http://mirrors.163.com/.help/CentOS${RELEASE}-Base-163.repo -O /etc/yum.repos.d/CentOS-Base.repo
yum -y update
timedatectl  set-timezone Asia/Shanghai
reboot
sleep 60
