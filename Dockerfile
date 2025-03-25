FROM quay.io/astronomer/astro-runtime:12.7.1

# Atualiza pip antes da instalação
RUN pip install --upgrade pip

# Instala protobuf antes dos outros pacotes
RUN pip install protobuf==4.24.4

# Instala os pacotes do projeto
COPY requirements.txt .
RUN pip install -r requirements.txt