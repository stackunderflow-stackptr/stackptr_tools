set -euxo pipefail

if [ $EUID -ne 0 ]
	then su -c "bash $0"
	exit
fi

apt-get -y install git

git clone https://github.com/stackunderflow-stackptr/stackptr_tools.git

cd stackptr_tools/tileserver-2/

bash master.sh