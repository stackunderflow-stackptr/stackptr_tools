set -euxo pipefail

PG_CONF_PATH=/etc/postgresql/9.5/main/

sed -i -e"s/^#max_connections = .*$/max_connections = 250/" $PG_CONF_PATH/postgresql.conf
sed -i -e"s/^#shared_buffers = .*$/shared_buffers = 1GB/" $PG_CONF_PATH/postgresql.conf
sed -i -e"s/^#work_mem = .*$/work_mem = 512MB/" $PG_CONF_PATH/postgresql.conf
sed -i -e"s/^#fsync = .*$/fsync = off/" $PG_CONF_PATH/postgresql.conf
sed -i -e"s/^#synchronous_commit = .*$/synchronous_commit = off/" $PG_CONF_PATH/postgresql.conf
sed -i -e"s/^#checkpoint_completion_target = .*$/checkpoint_completion_target = 0.9/" $PG_CONF_PATH/postgresql.conf

service postgresql restart