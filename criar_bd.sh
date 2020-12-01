sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo su - postgres
createuser -s cloud -W

createdb -O cloud tasks

##nano /etc/postgresql/10/main/postgresql.conf
sed 's /listen_addresses = 'localhost'/listen_addresses = '*'/g /etc/postgresql/10/main/postgresql.conf
## nano /etc/postgresql/10/main/pg_hba.conf
echo host all all 192.168.0.0/20 trust >> /etc/postgresql/10/main/pg_hba.conf