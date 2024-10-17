:: reset
docker kill c1nodo1 c1nodo2 
docker rm c1nodo1 c1nodo2 
 
:: cluster 1
docker run -d --cap-add sys_resource --name c1nodo1 -p 127.0.0.1:8443:8443 -p 127.0.0.1:9443:9443 -p 127.0.0.1:12000:12000 redislabs/redis
docker run -d --cap-add sys_resource --name c1nodo2 -p 127.0.0.1:8444:8443 -p 127.0.0.1:9444:9443 -p 127.0.0.1:12001:12000 redislabs/redis
 
timeout /t 5
 
docker exec -it c1nodo1 rladmin cluster create addr 172.17.0.2 username mail@mail.com password 123 name cluster1.local
docker exec -it c1nodo2 rladmin cluster join nodes 172.17.0.2 addr 172.17.0.3 username mail@mail.com password 123

docker exec -it c1nodo1 rladmin tune cluster default_sharded_proxy_policy all-nodes
docker exec -it c1nodo1 rladmin tune cluster slave_ha_grace_period 1

::docker exec -it c1nodo1 curl -X POST https://localhost:9443/v1/bdbs -k -u mail@mail.com:123 -H 'Content-type: application/json' -d '{"name":"test", "memory_size":107374182,"port":12000,"replication":true}'

 
:: GUI
start chrome "https://localhost:8443"
 
:: Configure DB
echo "Crear la base de datos"
pause
docker exec -it c1nodo1 rladmin bind db db:1 endpoint 1:1 policy all-nodes
docker exec -it c1nodo1 rladmin tune db db:1 slave_ha enabled


:: #########
@echo off

:: reset 
docker kill rdinode postgresql debezium rsnode
docker rm rdinode postgresql debezium rsnode
rmdir /s /q %CD%\Postgres
mkdir %CD%\Postgres
pause

echo --- Creando Instancia PostgreSQL ---
docker run -itd -e POSTGRES_USER=redis_user -e POSTGRES_PASSWORD=post123 -p 5432:5432 --name postgresql postgres
echo --- Instancia de Postgresql Creada ---
pause
echo.
:: Crear DB en Postgres
echo --- CREAR LA BASE DE DATOS EN POSTGRES ---
echo Copia y ejecuta estos comando linea a linea
echo Comandos:
echo createdb -h localhost -p 5432 -U redis_user redis
echo PGPASSWORD=post123 psql -U redis_user redis
echo ALTER SYSTEM SET wal_level = logical;
docker exec -it postgresql bash
echo --- BASE DE DATOS CREADA ---
pause 
echo.
:: se necesita reiniciar Postgres
echo --- Reiniciando Postgres... ---
docker restart postgresql
pause
echo.
echo --- CREAR EL SCHEMA Y LA TABLA EN POSTGRES ---
echo Copia y ejecuta estos comando linea a linea
echo Comandos:
echo PGPASSWORD=post123 psql -U redis_user redis
echo CREATE SCHEMA IF NOT EXISTS test AUTHORIZATION redis_user;
echo CREATE TABLE IF NOT EXISTS test.tesis (id INT PRIMARY KEY, name TEXT, value NUMERIC);
docker exec -it postgresql bash
echo --- SCHEMA Y TABLA CREADOS ---
echo.
pause