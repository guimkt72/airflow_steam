FROM quay.io/astronomer/astro-runtime:12.7.1

# Install git as root user first
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Switch back to astro user
USER astro

# Install dbt and requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir dbt-core==1.9.3 dbt-postgres==1.9.0

# Create dbt directory structure
RUN mkdir -p /usr/local/airflow/dbt && \
    mkdir -p /home/astro/.dbt

    # Set working directory to dbt project
WORKDIR /usr/local/airflow/airflow_steam