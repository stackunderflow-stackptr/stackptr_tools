set -euxo pipefail

OPTIONS=(	1 "Update Debian and install required utilities"
			2 "Postgres - apply import tuning"
			3 "Postgres - create database"
			4 "Download OSM data"
			5 "Setup internal net for Vultr hosts"
			6 "Install imposm"
			7 "Imposm initial read"
			8 "Imposm import into database"
			9 "Imposm optimise and deploy"
			)

CHOICE=0

while true
do
	CHOICE=$(dialog --clear --backtitle "StackPtr Deploy" --menu "Choose a task:" --default-item $((CHOICE+1)) 20 80 11 "${OPTIONS[@]}" 2>&1 >/dev/tty)
	clear

	case $CHOICE in
		1) bash scripts/01-update-debian.sh ;;
		2) bash scripts/02-postgres-tune.sh ;;
		3) bash scripts/03-postgres-createdb.sh ;;
		4) bash scripts/04-osm-download.sh ;;
		5) bash scripts/05-vultr-net.sh ;;
		6) bash scripts/06-imposm3-install.sh ;;
		7) bash scripts/07-imposm3-read.sh ;;
		8) bash scripts/08-imposm3-import.sh ;;
		9) bash scripts/09-imposm3-deploy.sh ;;
	esac

	read -p 'press enter to return to menu...'
done