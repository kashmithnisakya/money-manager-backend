## Instructions to Use
1. Save the file as docker-compose.yml in the root of your project.

2. Start PostgreSQL with the following command:

```bash
docker-compose up -d
```

3. Verify the PostgreSQL container is running:

```bash
docker ps
```

4. Connect to PostgreSQL:

* From your application, use the following connection details in application.properties:
```
spring.datasource.url=jdbc:postgresql://localhost:5432/moneymanager
spring.datasource.username=your_username
spring.datasource.password=your_password
```
5. Access the Database:

* Use psql or a database client like pgAdmin, DBeaver, or DataGrip to interact with the database.
* Example psql command:
```bash
psql -h localhost -p 5432 -U your_username -d moneymanager
```

6. Stop and Remove Containers
* To stop and remove the containers, use:

```bash
docker-compose down
```
This will safely stop the database while preserving the data in the postgres_data volume.