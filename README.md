docker run --name mysql -v /mysql_data:/var/lib/mysql -e "MYSQL_ROOT_PASSWORD=123456" -p 3306:3306 -d mysql

# Data source
<https://www.kaggle.com/datasets/malaiarasugraj/global-health-statistics>

Requirements

- Install Postgresql
  - Add pg_admin to the path, (environment variables)

## NOTEPAD

x-airflow-common:

# In order to add custom dependencies or upgrade provider packages you can use your extended image

# Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml

# and uncomment the "build" line below, Then run `docker-compose build` to build the images

&airflow-common
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.3}

# build:

environment: &airflow-common-env
AIRFLOW**CORE**EXECUTOR: CeleryExecutor
AIRFLOW**DATABASE**SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW**CELERY**RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW**CELERY**BROKER_URL: redis://:@redis:6379/0
AIRFLOW**CORE**FERNET_KEY: ''
AIRFLOW**CORE**DAGS_ARE_PAUSED_AT_CREATION: 'true'
AIRFLOW**CORE**LOAD_EXAMPLES: 'true'
AIRFLOW**API**AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session' # yamllint disable rule:line-length # Use simple http server on scheduler for health checks # See <https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/check-health.html#scheduler-health-check-server> # yamllint enable rule:line-length
AIRFLOW**SCHEDULER**ENABLE_HEALTH_CHECK: 'true' # WARNING: Use \_PIP_ADDITIONAL_REQUIREMENTS option ONLY for a quick checks # for other purpose (development, test and especially production usage) build/extend Airflow image.
\_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
    # The following line can be used to set a custom config file, stored in the local config folder
    # If you want to use it, outcomment it and replace airflow.cfg with the name of your config file
    # AIRFLOW_CONFIG: '/opt/airflow/config/airflow.cfg'
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
  user: "${AIRFLOW_UID:-50000}:0"
depends_on: &airflow-common-depends-on
redis:
condition: service_healthy
postgres:
condition: service_healthy

services:
postgres:
image: postgres:13
environment:
POSTGRES_USER: airflow
POSTGRES_PASSWORD: airflow
POSTGRES_DB: airflow
volumes: - postgres-db-volume:/var/lib/postgresql/data
healthcheck:
test: [ "CMD", "pg_isready", "-U", "airflow" ]
interval: 10s
retries: 5
start_period: 5s
restart: always

redis: # Redis is limited to 7.2-bookworm due to licencing change # <https://redis.io/blog/redis-adopts-dual-source-available-licensing/>
image: redis:7.2-bookworm
expose: - 6379
healthcheck:
test: [ "CMD", "redis-cli", "ping" ]
interval: 10s
timeout: 30s
retries: 50
start_period: 30s
restart: always

airflow-webserver:
<<: *airflow-common
command: webserver
ports: - "8080:8080"
healthcheck:
test: [ "CMD", "curl", "--fail", "http://localhost:8080/health" ]
interval: 30s
timeout: 10s
retries: 5
start_period: 30s
restart: always
depends_on:
<<:*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully

airflow-scheduler:
<<: *airflow-common
command: scheduler
healthcheck:
test: [ "CMD", "curl", "--fail", "http://localhost:8974/health" ]
interval: 30s
timeout: 10s
retries: 5
start_period: 30s
restart: always
depends_on:
<<:*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully

airflow-worker:
<<: *airflow-common
command: celery worker
healthcheck: # yamllint disable rule:line-length
test: - "CMD-SHELL" - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}" || celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
interval: 30s
timeout: 10s
retries: 5
start_period: 30s
environment:
<<:*airflow-common-env # Required to handle warm shutdown of the celery workers properly # See <https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation>
DUMB_INIT_SETSID: "0"
restart: always
depends_on:
<<: \*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully

airflow-triggerer:
<<: *airflow-common
command: triggerer
healthcheck:
test: [ "CMD-SHELL", 'airflow jobs check --job-type TriggererJob --hostname "$${HOSTNAME}"' ]
interval: 30s
timeout: 10s
retries: 5
start_period: 30s
restart: always
depends_on:
<<:*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully

airflow-init:
<<: _airflow-common
entrypoint: /bin/bash # yamllint disable rule:line-length
command: - -c - |
if [[-z "${AIRFLOW_UID}"]]; then
echo
echo -e "\033[1;33mWARNING!!!: AIRFLOW_UID not set!\e[0m"
echo "If you are on Linux, you SHOULD follow the instructions below to set "
echo "AIRFLOW_UID environment variable, otherwise files will be owned by root."
echo "For other operating systems you can get rid of the warning with manually created .env file:"
echo " See: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user"
echo
fi
one_meg=1048576
mem_available=$$(($$(getconf \_PHYS_PAGES) _ $$(getconf PAGE_SIZE) / one_meg))
        cpus_available=$$(grep -cE 'cpu[0-9]+' /proc/stat)
disk_available=$$(df / | tail -1 | awk '{print $$4}')
        warning_resources="false"
        if (( mem_available < 4000 )) ; then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough memory available for Docker.\e[0m"
          echo "At least 4GB of memory required. You have $$(numfmt --to iec $$((mem_available * one_meg)))"
          echo
          warning_resources="true"
        fi
        if (( cpus_available < 2 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough CPUS available for Docker.\e[0m"
          echo "At least 2 CPUs recommended. You have $${cpus_available}"
echo
warning_resources="true"
fi
if (( disk_available < one_meg _ 10 )); then
echo
echo -e "\033[1;33mWARNING!!!: Not enough Disk space available for Docker.\e[0m"
echo "At least 10 GBs recommended. You have $$(numfmt --to iec $$((disk_available _ 1024 )))"
echo
warning_resources="true"
fi
if [[$${warning_resources} == "true"]]; then
echo
echo -e "\033[1;33mWARNING!!!: You have not enough resources to run Airflow (see above)!\e[0m"
echo "Please follow the instructions to increase amount of resources available:"
echo " https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#before-you-begin"
echo
fi
mkdir -p /sources/logs /sources/dags /sources/plugins
chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}
exec /entrypoint airflow version # yamllint enable rule:line-length
environment:
<<: \*airflow-common-env
\_AIRFLOW_DB_MIGRATE: 'true'
\_AIRFLOW_WWW_USER_CREATE: 'true'
\_AIRFLOW_WWW_USER_USERNAME: ${\_AIRFLOW_WWW_USER_USERNAME:-airflow}
\_AIRFLOW_WWW_USER_PASSWORD: ${\_AIRFLOW_WWW_USER_PASSWORD:-airflow}
\_PIP_ADDITIONAL_REQUIREMENTS: ''
user: "0:0"
volumes: - ${AIRFLOW_PROJ_DIR:-.}:/sources

airflow-cli:
<<: *airflow-common
profiles: - debug
environment:
<<:*airflow-common-env
CONNECTION_CHECK_MAX_COUNT: "0" # Workaround for entrypoint issue. See: <https://github.com/apache/airflow/issues/16252>
command: - bash - -c - airflow

# You can enable flower by adding "--profile flower" option e.g. docker-compose --profile flower up

# or by explicitly targeted on the command line e.g. docker-compose up flower

# See: <https://docs.docker.com/compose/profiles/>

flower:
<<: *airflow-common
command: celery flower
profiles: - flower
ports: - "5555:5555"
healthcheck:
test: [ "CMD", "curl", "--fail", "http://localhost:5555/" ]
interval: 30s
timeout: 10s
retries: 5
start_period: 30s
restart: always
depends_on:
<<:*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully

volumes:
postgres-db-volume:
