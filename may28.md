To pull an image from a private repository using a Helm chart, you need to ensure that Kubernetes has the credentials required to access the private Docker repository. This is typically done by creating a Kubernetes Secret with the Docker credentials and then referencing that Secret in your Helm chart. Here are the steps to achieve this:

### Step 1: Create a Docker Registry Secret
First, create a Kubernetes Secret with your Docker credentials. You can do this using the following command:

```bash
kubectl create secret docker-registry myregistrykey \
    --docker-server=repository.image.myimage \
    --docker-username=<your-username> \
    --docker-password=<your-password> \
    --docker-email=<your-email>
```

### Step 2: Reference the Secret in Your Helm Chart
In your Helm chart, you need to update the deployment template to use the created Secret. This is done by adding the `imagePullSecrets` field to the `spec` section of your `Deployment` resource. Here's an example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: repository.image.myimage/my-app:latest
        ports:
        - containerPort: 80
      imagePullSecrets:
      - name: myregistrykey
```

### Step 3: Install or Upgrade the Helm Chart
After making these changes, install or upgrade your Helm chart:

```bash
helm install my-release ./my-chart
# or, if the release already exists
helm upgrade my-release ./my-chart
```

### Step 4: Verify the Configuration
Check if the Secret is correctly referenced in the deployed pods:

```bash
kubectl get pods -o=jsonpath="{.items[*].spec.imagePullSecrets}"
```

You should see the Secret `myregistrykey` listed.

### Common Pitfalls
- **Incorrect Secret Name**: Ensure the name of the Secret matches exactly in both the `kubectl create secret` command and the Helm chart.
- **Namespace Issues**: Make sure the Secret is created in the same namespace as the deployment. If your deployment is in a different namespace, specify it using `-n <namespace>` in both the `kubectl create secret` command and your Helm chart configuration.
- **Helm Values Override**: If you use Helm values files, you can parameterize the image and `imagePullSecrets` fields in your `values.yaml` and reference them in your templates.

By following these steps, Kubernetes should be able to pull the image from your private Docker repository, resolving the `ImagePullBackOff` error.


########
The error "can’t locate revision identified by" from Alembic typically indicates that Alembic is unable to find a specific migration revision in the database's migration history. This often happens when there is a mismatch or missing migration file in your Alembic migrations.

Here are some steps to troubleshoot and resolve this issue:

### 1. Check Database Connection
Ensure that your Helm charts are correctly configured to connect to the PostgreSQL database. Verify the connection details such as hostname, port, username, and password.

### 2. Verify Migration Files
Ensure that all Alembic migration files are present in your deployment package. Compare the migrations in your local environment (where `helm template` works) to those in the Kubernetes environment.

### 3. Database Initialization
Ensure that the database has been properly initialized with the Alembic migrations. If it’s a fresh database, you might need to run the initial migrations to set up the schema.

### 4. Helm Chart Values
Check the Helm chart values being used during `helm install`. Ensure that these values correctly set up the environment for Alembic to locate the migrations.

### 5. Volume Mounts
If your Helm charts include volume mounts for the database or migration files, ensure that these mounts are correctly set up and accessible.

### 6. Logging and Debugging
Increase the logging level for Alembic to get more detailed output. This can help identify where the issue is occurring.

### 7. Comparing Environments
Since `helm template` works, there might be a difference in the environment or configuration between the templated YAML and the direct Helm deployment. Compare the outputs of `helm template` and the actual deployed resources.

### Example Debugging Steps

1. **Check Database Connection:**
   Ensure the connection string in your Helm values file is correct.
   ```yaml
   postgresql:
     host: your-postgres-host
     port: 5432
     username: your-username
     password: your-password
     database: your-database
   ```

2. **Verify Migrations:**
   Ensure all migration files are present and correctly referenced in your application.

3. **Database Initialization:**
   Run the initial migrations if the database is new.
   ```sh
   alembic upgrade head
   ```

4. **Increase Alembic Logging:**
   Modify Alembic configuration to increase logging verbosity.
   ```ini
   [loggers]
   keys = root,sqlalchemy,alembic

   [handlers]
   keys = console

   [formatters]
   keys = generic

   [logger_root]
   level = WARN
   handlers = console
   qualname =

   [logger_sqlalchemy]
   level = WARN
   handlers = console
   qualname = sqlalchemy.engine
   propagate = 0

   [logger_alembic]
   level = INFO
   handlers = console
   qualname = alembic
   propagate = 0
   ```

5. **Compare Outputs:**
   Compare the output of `helm template` and the actual deployed resources.
   ```sh
   helm template your-chart
   kubectl get all -n your-namespace -o yaml
   ```

### Conclusion
By following these steps, you should be able to pinpoint the cause of the Alembic revision error and resolve it. If you need further assistance, please provide more details on your Helm charts, values, and the exact error messages you’re encountering.

#########
To run `alembic upgrade head`, you need to execute it in an environment where your application and Alembic are set up correctly. This is typically done in the container or pod where your application is running. Here’s how you can do it:

### Steps to Run `alembic upgrade head` in Kubernetes

1. **Access Your Pod:**
   First, identify the pod running your application. You can use `kubectl get pods` to list the pods in your namespace.
   ```sh
   kubectl get pods -n your-namespace
   ```

2. **Execute Command Inside the Pod:**
   Once you have identified the pod, you can execute the `alembic upgrade head` command inside the pod. Replace `your-pod-name` with the actual name of your pod.
   ```sh
   kubectl exec -it your-pod-name -n your-namespace -- alembic upgrade head
   ```

3. **Automate in Deployment:**
   To automate this process, you can add an `initContainer` to your Kubernetes deployment configuration. This `initContainer` will run the Alembic migration before starting your main application container.

### Example of Using an InitContainer

Here is an example of how to add an `initContainer` to your deployment YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-api-server
  namespace: your-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: your-api-server
  template:
    metadata:
      labels:
        app: your-api-server
    spec:
      initContainers:
      - name: migrate-db
        image: your-application-image
        command: ["alembic", "upgrade", "head"]
        envFrom:
        - configMapRef:
            name: your-config
        - secretRef:
            name: your-secret
      containers:
      - name: your-api-server
        image: your-application-image
        ports:
        - containerPort: 80
        envFrom:
        - configMapRef:
            name: your-config
        - secretRef:
            name: your-secret
```

### Points to Note:
1. **Ensure Alembic is Installed:**
   Make sure Alembic is installed in the image used for your application.

2. **Environment Variables:**
   Ensure all necessary environment variables (like database connection details) are available to the initContainer. This can be done via ConfigMaps or Secrets.

3. **Image and Command:**
   Ensure the image used in the `initContainer` has Alembic installed and the command to run Alembic is correctly specified.

By following these steps, you can ensure that Alembic migrations are run correctly, and your database schema is up to date before your application starts. If you encounter any issues during these steps, please provide the specific error messages or logs for further assistance.

#####
You should run the `alembic upgrade head` command as part of your job (db-migration). Since you mentioned that you have a separate job for running database migrations, this is the appropriate place to run your Alembic migrations. Here’s how you can set it up:

### Running Alembic Migrations in a Kubernetes Job

1. **Ensure Job Configuration:**
   Make sure your job configuration includes the necessary environment variables and commands to run Alembic.

2. **Job YAML Example:**
   Below is an example of how to configure your Kubernetes job to run `alembic upgrade head`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  namespace: your-namespace
spec:
  template:
    spec:
      containers:
      - name: db-migration
        image: your-application-image
        command: ["alembic", "upgrade", "head"]
        envFrom:
        - configMapRef:
            name: your-config
        - secretRef:
            name: your-secret
      restartPolicy: Never
  backoffLimit: 4
```

### Steps to Deploy and Run the Job

1. **Create or Update the Job Configuration:**
   Save the above YAML configuration to a file, for example, `db-migration-job.yaml`.

2. **Deploy the Job:**
   Apply the job configuration using `kubectl`.
   ```sh
   kubectl apply -f db-migration-job.yaml
   ```

3. **Check Job Status:**
   Monitor the job to ensure it runs successfully.
   ```sh
   kubectl get jobs -n your-namespace
   kubectl logs job/db-migration -n your-namespace
   ```

### Troubleshooting the Error

If you still encounter the error "can’t locate revision identified by," follow these steps:

1. **Check Logs:**
   Inspect the logs of the migration job to get more details about the error.
   ```sh
   kubectl logs job/db-migration -n your-namespace
   ```

2. **Verify Environment:**
   Ensure that the job has access to the correct environment variables, such as database connection details.

3. **Migration Files:**
   Verify that all migration files are included in the image used for the job. Ensure there are no missing migration files.

4. **Database State:**
   Check the state of your database. If it's a fresh database, ensure it has the initial schema and no conflicts with existing migrations.

By running the `alembic upgrade head` command in your db-migration job, you ensure that your database schema is up to date before your application starts. This setup also isolates the migration process, making it easier to troubleshoot and manage. If issues persist, providing the specific error logs from the job will help in further diagnosing the problem.

######
The hostname for the PostgreSQL database in your Kubernetes cluster will not be `localhost` because the database is running in a separate pod. Instead, it will be the name of the PostgreSQL service you have set up in Kubernetes. This service name is used to connect to the database within the cluster.

### Example Configuration

1. **PostgreSQL Service Hostname:**
   If your PostgreSQL service is named `postgres-service` in the `default` namespace, the hostname will be `postgres-service.default.svc.cluster.local`.

2. **Helm Chart Values Configuration:**
   Since your two API Helm charts have different database names, you can set the values accordingly.

Here is an example of how you might configure your Helm chart values:

### API Server 1 (server-db)

```yaml
postgresql:
  host: postgres-service.default.svc.cluster.local
  port: 5432
  username: your-username
  password: your-password
  database: server-db
```

### API Server 2 (picker-db)

```yaml
postgresql:
  host: postgres-service.default.svc.cluster.local
  port: 5432
  username: your-username
  password: your-password
  database: picker-db
```

### Full Example of Helm Chart Values

You need to ensure that your Helm charts for both API servers are configured to use these values. Here’s a more detailed example for both charts:

#### Values for API Server 1

```yaml
# values.yaml for API Server 1
postgresql:
  host: postgres-service.default.svc.cluster.local
  port: 5432
  username: your-username
  password: your-password
  database: server-db
```

#### Values for API Server 2

```yaml
# values.yaml for API Server 2
postgresql:
  host: postgres-service.default.svc.cluster.local
  port: 5432
  username: your-username
  password: your-password
  database: picker-db
```

### Deploying Your Helm Charts

1. **API Server 1:**
   ```sh
   helm install api-server-1 ./api-server-1-chart -f values.yaml
   ```

2. **API Server 2:**
   ```sh
   helm install api-server-2 ./api-server-2-chart -f values.yaml
   ```

### Running Alembic Migrations

Since you have a separate job for running Alembic migrations, ensure it is configured correctly to run against each database as needed.

1. **Job Configuration for server-db:**
   ```yaml
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: db-migration-server-db
     namespace: your-namespace
   spec:
     template:
       spec:
         containers:
         - name: db-migration
           image: your-application-image
           command: ["alembic", "upgrade", "head"]
           env:
           - name: POSTGRES_HOST
             value: "postgres-service.default.svc.cluster.local"
           - name: POSTGRES_PORT
             value: "5432"
           - name: POSTGRES_USER
             value: "your-username"
           - name: POSTGRES_PASSWORD
             value: "your-password"
           - name: POSTGRES_DB
             value: "server-db"
         restartPolicy: Never
     backoffLimit: 4
   ```

2. **Job Configuration for picker-db:**
   ```yaml
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: db-migration-picker-db
     namespace: your-namespace
   spec:
     template:
       spec:
         containers:
         - name: db-migration
           image: your-application-image
           command: ["alembic", "upgrade", "head"]
           env:
           - name: POSTGRES_HOST
             value: "postgres-service.default.svc.cluster.local"
           - name: POSTGRES_PORT
             value: "5432"
           - name: POSTGRES_USER
             value: "your-username"
           - name: POSTGRES_PASSWORD
             value: "your-password"
           - name: POSTGRES_DB
             value: "picker-db"
         restartPolicy: Never
     backoffLimit: 4
   ```

Apply these jobs similarly to how you apply other Kubernetes resources:

```sh
kubectl apply -f db-migration-server-db.yaml
kubectl apply -f db-migration-picker-db.yaml
```

By ensuring that the correct PostgreSQL host and database names are used in each configuration, you can resolve connectivity issues and ensure that your migrations run successfully.

#####
To create a PostgreSQL resource with two databases in Kubernetes, you can use a custom PostgreSQL configuration or an init script that creates both databases when the PostgreSQL container starts. Here’s how you can set this up:

### PostgreSQL Deployment with Two Databases

1. **PostgreSQL Deployment:**
   Create a deployment for PostgreSQL with an init script to create the two databases.

2. **PostgreSQL Service:**
   Create a service to expose the PostgreSQL database.

### Example Kubernetes Configuration

#### PostgreSQL Deployment with Init Script

Create an init script that will create both `server-db` and `picker-db` databases.

```sql
-- init-db.sql
CREATE DATABASE "server-db";
CREATE DATABASE "picker-db";
```

#### Kubernetes ConfigMap for Init Script

Create a ConfigMap to hold the init script.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

#### PostgreSQL Deployment

Create the PostgreSQL deployment that uses the init script.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: your-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:14.3
        env:
        - name: POSTGRES_USER
          value: "your-username"
        - name: POSTGRES_PASSWORD
          value: "your-password"
        - name: POSTGRES_DB
          value: "postgres"
        volumeMounts:
        - name: initdb
          mountPath: /docker-entrypoint-initdb.d
      volumes:
      - name: initdb
        configMap:
          name: postgres-initdb
```

#### PostgreSQL Service

Create a service to expose the PostgreSQL deployment.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: your-namespace
spec:
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
```

### Apply the Configuration

1. **Create the ConfigMap:**
   ```sh
   kubectl apply -f postgres-initdb-configmap.yaml
   ```

2. **Create the PostgreSQL Deployment:**
   ```sh
   kubectl apply -f postgres-deployment.yaml
   ```

3. **Create the PostgreSQL Service:**
   ```sh
   kubectl apply -f postgres-service.yaml
   ```

### Summary

This setup creates a PostgreSQL instance with two databases (`server-db` and `picker-db`) using an init script stored in a ConfigMap. The deployment mounts this init script and runs it when the container starts, ensuring both databases are created.

With this setup, your two API Helm charts can now connect to their respective databases using the same PostgreSQL service endpoint but different database names. This ensures they have isolated databases while sharing the same PostgreSQL instance.


#####


Here's the full set of Kubernetes resources needed to create a PostgreSQL deployment with two databases (`server-db` and `picker-db`) using an init script. 

### Step 1: Create the ConfigMap for the Init Script

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

Save this to a file named `postgres-initdb-configmap.yaml`.

### Step 2: Create the Persistent Volume and Persistent Volume Claim

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
  namespace: your-namespace
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data/postgres
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: your-namespace
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

Save this to a file named `postgres-pv-pvc.yaml`.

### Step 3: Create the PostgreSQL Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: your-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:14.3
        env:
        - name: POSTGRES_USER
          value: "your-username"
        - name: POSTGRES_PASSWORD
          value: "your-password"
        - name: POSTGRES_DB
          value: "postgres"
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        - name: initdb
          mountPath: /docker-entrypoint-initdb.d
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-pvc
      - name: initdb
        configMap:
          name: postgres-initdb
```

Save this to a file named `postgres-deployment.yaml`.

### Step 4: Create the PostgreSQL Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: your-namespace
spec:
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
```

Save this to a file named `postgres-service.yaml`.

### Step 5: Apply the Configuration

1. **Create the ConfigMap:**
   ```sh
   kubectl apply -f postgres-initdb-configmap.yaml
   ```

2. **Create the Persistent Volume and Persistent Volume Claim:**
   ```sh
   kubectl apply -f postgres-pv-pvc.yaml
   ```

3. **Create the PostgreSQL Deployment:**
   ```sh
   kubectl apply -f postgres-deployment.yaml
   ```

4. **Create the PostgreSQL Service:**
   ```sh
   kubectl apply -f postgres-service.yaml
   ```

### Summary

This setup will create a PostgreSQL instance with two databases (`server-db` and `picker-db`) using an init script stored in a ConfigMap. The PostgreSQL deployment mounts this init script and runs it when the container starts, ensuring both databases are created. The service exposes PostgreSQL on port 5432, allowing your API servers to connect to the databases.


######

To use the Bitnami PostgreSQL Helm chart with an init script to create two databases, you can customize the values file for the Bitnami PostgreSQL Helm chart. Here’s how you can do it:

### Step 1: Create the Init Script

Create an init script that will create both `server-db` and `picker-db` databases.

```sql
-- init-db.sql
CREATE DATABASE "server-db";
CREATE DATABASE "picker-db";
```

### Step 2: Create a ConfigMap for the Init Script

Create a ConfigMap to hold the init script.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

Save this to a file named `postgres-initdb-configmap.yaml`.

### Step 3: Customize the Values File for the Bitnami PostgreSQL Chart

Create a values file for the Bitnami PostgreSQL Helm chart, referencing the init script.

```yaml
global:
  postgresql:
    postgresqlDatabase: postgres
    postgresqlUsername: your-username
    postgresqlPassword: your-password

primary:
  initdbScriptsConfigMap: postgres-initdb

persistence:
  enabled: true
  storageClass: "your-storage-class"
  accessModes:
    - ReadWriteOnce
  size: 1Gi

# Service exposure parameters
service:
  type: ClusterIP
  port: 5432
```

Save this to a file named `values.yaml`.

### Step 4: Deploy the PostgreSQL Using the Bitnami Helm Chart

Add the Bitnami repository and deploy the PostgreSQL instance using the customized values file.

1. **Add the Bitnami Repository:**
   ```sh
   helm repo add bitnami https://charts.bitnami.com/bitnami
   ```

2. **Update the Repository:**
   ```sh
   helm repo update
   ```

3. **Create the ConfigMap:**
   ```sh
   kubectl apply -f postgres-initdb-configmap.yaml
   ```

4. **Deploy the PostgreSQL Instance:**
   ```sh
   helm install my-postgres bitnami/postgresql -f values.yaml -n your-namespace
   ```

### Full Configuration Example

1. **postgres-initdb-configmap.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

2. **values.yaml**

```yaml
global:
  postgresql:
    postgresqlDatabase: postgres
    postgresqlUsername: your-username
    postgresqlPassword: your-password

primary:
  initdbScriptsConfigMap: postgres-initdb

persistence:
  enabled: true
  storageClass: "your-storage-class"
  accessModes:
    - ReadWriteOnce
  size: 1Gi

service:
  type: ClusterIP
  port: 5432
```

### Deploying the Configuration

1. **Create the ConfigMap:**
   ```sh
   kubectl apply -f postgres-initdb-configmap.yaml
   ```

2. **Deploy the PostgreSQL Instance:**
   ```sh
   helm install my-postgres bitnami/postgresql -f values.yaml -n your-namespace
   ```

This setup uses the Bitnami PostgreSQL Helm chart and includes an init script that creates the `server-db` and `picker-db` databases. The PostgreSQL instance is configured to use persistent storage, and the init script is referenced via a ConfigMap. Make sure to adjust the values like `your-username`, `your-password`, and `your-storage-class` to fit your specific environment.

#####

In the Bitnami PostgreSQL Helm chart, the `postgresqlDatabase` parameter under `global.postgresql` is used to define the default database that is created during the initial setup. This database is often used for administrative purposes and is different from the additional databases you might want to create using the init script.

### Explanation:

1. **postgresqlDatabase**: 
   - This is the default database created by the Helm chart. It's a single database defined in the values file and used for initial setup.
   - For instance, this can be `postgres` or another default database name you prefer.

2. **Additional Databases**:
   - These are created using the init script provided via the ConfigMap.
   - In this example, `server-db` and `picker-db` are additional databases created using the init script.

### Steps with Local Storage

1. **Modify the ConfigMap**:
   The ConfigMap will hold the SQL script to create the additional databases.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

2. **Modify the values.yaml for Local Storage**:
   Ensure you set the persistence storage class to use local storage.

```yaml
global:
  postgresql:
    postgresqlDatabase: postgres
    postgresqlUsername: your-username
    postgresqlPassword: your-password

primary:
  initdbScriptsConfigMap: postgres-initdb

persistence:
  enabled: true
  storageClass: ""  # Leave empty or specify local storage class
  accessModes:
    - ReadWriteOnce
  size: 1Gi

service:
  type: ClusterIP
  port: 5432
```

### Complete Example

1. **postgres-initdb-configmap.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-initdb
  namespace: your-namespace
data:
  init-db.sql: |
    CREATE DATABASE "server-db";
    CREATE DATABASE "picker-db";
```

2. **values.yaml**

```yaml
global:
  postgresql:
    postgresqlDatabase: postgres  # Default database created by the Helm chart
    postgresqlUsername: your-username
    postgresqlPassword: your-password

primary:
  initdbScriptsConfigMap: postgres-initdb  # Reference to the ConfigMap for additional databases

persistence:
  enabled: true
  storageClass: ""  # Using local storage
  accessModes:
    - ReadWriteOnce
  size: 1Gi

service:
  type: ClusterIP
  port: 5432
```

### Deployment Steps

1. **Create the ConfigMap**:

   ```sh
   kubectl apply -f postgres-initdb-configmap.yaml
   ```

2. **Deploy the PostgreSQL Instance**:

   ```sh
   helm install my-postgres bitnami/postgresql -f values.yaml -n your-namespace
   ```

### Summary

- The `postgresqlDatabase` parameter sets up a default database (`postgres` in this case).
- The ConfigMap with the init script creates additional databases (`server-db` and `picker-db`).
- Ensure the persistence storage class is set to use local storage.

This setup ensures you have the default PostgreSQL database for administrative tasks and additional databases for your application needs, all managed through the Bitnami Helm chart and Kubernetes resources.




