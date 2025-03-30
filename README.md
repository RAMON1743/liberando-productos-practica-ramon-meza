## Liberando Productos - Práctica Final.
Este proyecto es una API desarrollada con FastAPI y desplegada en Kubernetes, monitorizada con Prometheus + Alertmanager + Grafana, e integrada con un pipeline de CI/CD usando GitHub Actions.
Incluye pruebas automatizadas, métricas personalizadas, alertas configuradas y un dashboard completo para visualización.


 ## Índice
- Código para el nuevo endpoint y tests unitario

- CI/CD (GitHub Actions)
  
- Construcción de la imagen Docker
  
- Despliegue y monitorización
  
- Dashboard Grafana (JSON)
  
- Estructura del proyecto
  
- Cómo reproducir paso a paso



## Código para el nuevo endpoint y tests unitario.

- La app está escrita con FastAPI y expone varios endpoints (/, /bye, /health, /metrics).

- Se han añadido métricas personalizadas con prometheus_client:

- main_requests_total, bye_requests_total, healthcheck_requests_total, fastapi_app_starts_total

- Incluye tests con Pytest y cobertura:

📂 Ver código en: src/ https://github.com/RAMON1743/liberando-productos-practica-ramon-meza/tree/main/src/application
imgen endpoint

📂 Ver tests en: tests/ https://github.com/RAMON1743/liberando-productos-practica-ramon-meza/tree/main/src/tests

imagen del test unitario pasado

## CI/CD (GitHub Actions)

Workflows definidos:

### Testing: github/workflows/test.yaml
Este workflow se ejecuta automáticamente en cada push o pull request sobre ramas como main o develop. 

Su función es:
- Ejecutar tests unitarios de la aplicación (usando pytest).
- Generar un informe de cobertura de código.
- Validar que el código subido cumple con los estándares.
  
📂 Ver código en: test/ [código de tests](./.github/workflows/test.yaml)


### Build & Push (Release): github/workflows/release.yaml
Este segundo workflow se ejecuta automáticamente cuando se crea un tag con formato vX.X.X (por ejemplo: v3.0.0). Sus pasos:
- Construye una imagen Docker de la aplicación.
- La empaqueta con la versión correspondiente (:3.0.0).
- La sube a DockerHub usando las credenciales almacenadas como secrets del repositorio.
Los secrets utilizados para autenticación son:
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
Para lanzar este workflow, simplemente se corre:
```sh
git tag v3.0.0
git push origin v3.0.0
```
📂 Ver código en: Release/ [código release](./.github/workflows/release.yaml)

imagen action 

- La imagen se publica como: (**docker.io/ramon1743/liberando-productos-practica-final-ramon-meza:3.0.0)**


imagen Dockerhub


**Esta implementación cumple con los requisitos de:**
- Pruebas automáticas con cobertura (Testing)
- Build & Push de imagen Docker (Release)
- Uso de GitHub Actions como plataforma de CI/CD
- Uso de tags para gestionar releases
- Publicación en un registry válido (DockerHub)



## Construcción de la imagen Docker

**Construir la imagen**

```sh
docker build -t ramon1743/simple-server:0.0.2 
```

Esto genera una imagen Docker etiquetada como simple-server:0.0.2 basada en el Dockerfile del proyecto.



Subimo la imagen a DockerHu

```sh
docker push ramon1743/simple-server:0.0.2
```

**Este paso requiere que estés logueado previamente en DockerHub:**

```sh
docker login
```

**Probamos localmente la imagen Docker**

```sh
docker run -d -p 8000:8000 -p 8081:8081 --name simple-server ramon1743/simple-server:0.0.2

```

Permite lenvantar la app en segundo plano con los puertos necesarios para acceder a los endpoints (/) y a las métricas Prometheus (/metrics).

## Despliegue y Monitorización
Se ha desplegado un entorno completo de observabilidad y monitorización basado en Prometheus y Grafana, cumpliendo con los requisitos de la práctica. También se ha realizado el despliegue de la aplicación en Kubernetes y se han integrado métricas personalizadas y alertas.


## Prometheus + Grafana desplegados con Helm
Se ha utilizado el chart kube-prometheus-stack para instalar Prometheus, Grafana, y los componentes relacionados:


```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  -f helm-values/kube-state-values.yaml \
  -f helm-values/alertmanager-config.yaml \
  -f helm-values/additional-rules.yaml \
  -f helm-values/prometheus-persistence.yaml
```


**Los valores definidos permiten:**
- Configurar el acceso y scraping de métricas del cluster.
- Incluir reglas de alerta personalizadas.
- Integrar alertas con Slack.
- Habilitar persistencia para Prometheus.

## Despliegue de la Aplicación
La aplicación FastAPI ha sido desplegada en Kubernetes con los siguientes manifiestos:

```bash

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/fastapi-servicemonitor.yaml

```

**Esto asegura que:**
- La app se ejecuta como un Deployment.
- Se expone vía un Service.
- Está registrada ante Prometheus mediante un ServiceMonitor.

Esto cumple con el despliegue completo de la app + monitorización Prometheus a través de ServiceMonitor.


## Métricas personalizadas disponibles

La aplicación expone métricas personalizadas accesibles en el endpoint /metrics, incluyendo:

- main_requests_total: número de llamadas al endpoint principal.
- healthcheck_requests_total: número de llamadas al endpoint del estado de la app.
- bye_requests_total: número de llamadas al endpoint de despedida.
- fastapi_app_starts_total: número de veces que la app ha arrancado.

Cumple con el requisito de tener métricas personalizadas útiles para monitorización y alertas.



## Reglas de alerta personalizadas

Se han definido reglas en helm-values/additional-rules.yaml, como por ejemplo:

- CPU > 80% durante más de 1 minuto, lo cual permite detectar sobrecarga.

Para probarlas, se puede simular carga con:

```bash
kubectl apply -f k8s/cpu-test-app.yaml
```


## Integración de Alertas con Slack
Las alertas se integran con Slack mediante un **webhook configurado en alertmanager-config.yaml**. Esto permite notificar a un canal específico cuando se cumple una regla.
-Se crear el Webhook de Slack
-Se creó una app de Slack y se activó la opción de Incoming Webhooks.
-Se generó un webhook para el canal #ramon-prometheus-alarms.
-Con la url obtenida: 'https://hooks.slack.com/services/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'
-Se agrega la configuración del webhook en helm-values/alertmanager-config.yaml.
-Esto permite que todas las alertas activas y resueltas lleguen directamente a #ramon-prometheus-alarms



**imagen de las alerta slack****



## Desplegar con Helm
La configuración se aplica al instalar o actualizar Prometheus con:

```bash

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  -f helm-values/alertmanager-config.yaml \
  -f helm-values/additional-rules.yaml \
  -f [...otros archivos...]
```


## Probar las alertas

Se puede simular una alerta (por ejemplo de alto uso de CPU) aplicando:

```bash

kubectl apply -f k8s/cpu-test-app.yaml

```


**Acceso vía navegador**

Está expuesto en el clúster de Kubernetes en el puerto 9090, por lo tanto, puedes acceder desde tu navegador con:

```bash
http://localhost:9090
```



**Imagen de prometheus**



**Resultado**
Cada vez que se cumpla una condición de alerta:
- Slack recibe una notificación clara y estructurada en el canal #ramon-prometheus-alarms.
- Así nos actuar de forma inmediata ante problemas de infraestructura o aplicación.



## Dashboard de Grafana 
Se ha creado un dashboard desde cero en Grafana, el cual muestra:

- Número de llamadas a los endpoints.

- Número de veces que la aplicación ha arrancado.

Archivo JSON [Archivo Json](https://fastapi.tiangolo.com/)



**Acceso a Grafana**

Grafana está expuesto en el clúster de Kubernetes en el puerto 30000, por lo tanto, puedes acceder desde tu navegador con:



```bash
http://localhost:3000
```



**Login Grafana**


- Usuario: **admin**

- Contraseña: **prom-operator**




## Estructura del proyecto


```bash

LIBERANDO-PRODUCTOS-PRACTICA-RAMON-MEZA/
├── .github/                        # Workflows de CI/CD
│   └── workflows/
│       ├── release.yaml
│       └── test.yaml
├── .pytest_cache/
│   ├── v/
│   ├── .gitignore
│   └── CACHEDIR.TAG
├── README.md
├── helm-values/                     # Configuración para Prometheus stack
│   ├── additional-rules.yaml
│   ├── alertmanager-config.yaml
│   ├── alertmanager-secret.yaml
│   ├── kube-state-values.yaml
│   └── prometheus-persistence.yaml
├── htmlcov/
├── k8s/                            # Manifiestos de Kubernetes
│   ├── cpu-test-app.yaml
│   ├── deployment.yaml
│   ├── fastapi-servicemonitor.yaml
│   └── service.yaml
├── src/                            # Código fuente de la app
├── venv/
├── .coverage
├── .gitignore
├── Dockerfile
├── grafana-fastapi-dashboard.json  # Dashboard exportado a JSON
├── Makefile
├── pytest.ini
├── README.md
└── requirements.txt

```



## Cómo reproducir paso a paso


**Clona el repo y entra en la carpeta:**

```bash

git clone git@github.com:RAMON1743/liberando-productos-practica-ramon-meza.git

```

**Iniciamos el cluster Minikube:**

```bash
minikube start --cpus=4 --memory=6g --disk-size=20g

```


**Habilita addons:**

```bash
minikube addons enable metrics-server
minikube addons enable ingress

```

## Validar que todo está funcionando correctamente

**Verificar pods**

```bash
kubectl get pods
```

**Validar de que todos los pods estén en estado Running, tanto de la app como del stack monitoring.**

**Verificar servicios**

```bash
kubectl get svc
```

**Confirma que existen y están expuestos los servicios:**

- Monitoring-grafana
- Monitoring-prometheus
- Monitoring-alertmanager
- Fastapi

  
**Verificar targets en Prometheus**

En Prometheus (una vez abierto), ve a Status > Targets y revisa que tu ServiceMonitor esté UP.


## Acceder a los servicios vía navegador

```bash
kubectl port-forward svc/monitoring-grafana 3000:80
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090
kubectl port-forward svc/monitoring-kube-prometheus-alertmanager 9093

```


**Accede en el navegador:**

- **Grafana**: http://localhost:3000

- **Prometheus**: http://localhost:9090

- **Alertmanager**: http://localhost:9093












El proyecto inicial es un servidor que realiza lo siguiente:

- Utiliza [FastAPI](https://fastapi.tiangolo.com/) para levantar un servidor en el puerto `8081` e implementa inicialmente dos endpoints:
  - `/`: Devuelve en formato `JSON` como respuesta `{"health": "ok"}` y un status code 200.
  - `/health`: Devuelve en formato `JSON` como respuesta `{"message":"Hello World"}` y un status code 200.

- Se han implementado tests unitarios para el servidor [FastAPI](https://fastapi.tiangolo.com/)

- Utiliza [prometheus-client](https://github.com/prometheus/client_python) para arrancar un servidor de métricas en el puerto `8000` y poder registrar métricas, siendo inicialmente las siguientes:
  - `Counter('server_requests_total', 'Total number of requests to this webserver')`: Contador que se incrementará cada vez que se haga una llamada a alguno de los endpoints implementados por el servidor (inicialmente `/` y `/health`)
  - `Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/health`.
  - `Counter('main_requests_total', 'Total number of requests to main endpoint')`: Contador que se incrementará cada vez que se haga una llamada al endpoint `/`.

## Software necesario

Es necesario disponer del siguiente software:

- `Python` en versión `3.11.8` o superior, disponible para los diferentes sistemas operativos en la [página oficial de descargas](https://www.python.org/downloads/release/python-3118/)

- `virtualenv` para poder instalar las librerías necesarias de Python, se puede instalar a través del siguiente comando:

    ```sh
    pip3 install virtualenv
    ```

    En caso de estar utilizando Linux y el comando anterior diera fallos se debe ejecutar el siguiente comando:

    ```sh
    sudo apt-get update && sudo apt-get install -y python3.11-venv
    ```

- `Docker` para poder arrancar el servidor implementado a través de un contenedor Docker, es posible descargarlo a [través de su página oficial](https://docs.docker.com/get-docker/).

## Ejecución de servidor

### Ejecución directa con Python

1. Instalación de un virtualenv, **realizarlo sólo en caso de no haberlo realizado previamente**:
   1. Obtener la versión actual de Python instalada para crear posteriormente un virtualenv:

        ```sh
        python3 --version
        ```

        El comando anterior mostrará algo como lo mostrado a continuación:ç

        ```sh
        Python 3.11.8
        ```

   2. Crear de virtualenv en la raíz del directorio para poder instalar las librerías necesarias:

      ```sh
      python3 -m venv venv
      ```

2. Activar el virtualenv creado en el directorio `venv` en el paso anterior:

     ```sh
     source venv/bin/activate
     ```

3. Instalar las librerías necesarias de Python, recogidas en el fichero `requirements.txt`, **sólo en caso de no haber realizado este paso previamente**. Es posible instalarlas a través del siguiente comando:

    ```sh
    pip3 install -r requirements.txt
    ```

4. Ejecución del código para arrancar el servidor:

    ```sh
    python3 src/app.py
    ```

5. La ejecución del comando anterior debería mostrar algo como lo siguiente:

    ```sh
    [2022-04-16 09:44:22 +0000] [1] [INFO] Running on http://0.0.0.0:8081 (CTRL + C to quit)
    ```

### Ejecución a través de un contenedor Docker

1. Crear una imagen Docker con el código necesario para arrancar el servidor:

    ```sh
    docker build -t simple-server:0.0.1 .
    ```

2. Arrancar la imagen construida en el paso anterior mapeando los puertos utilizados por el servidor de FastAPI y el cliente de prometheus:

    ```sh
    docker run -d -p 8000:8000 -p 8081:8081 --name simple-server simple-server:0.0.1
    ```

3. Obtener los logs del contenedor creado en el paso anterior:

    ```sh
    docker logs -f simple-server
    ```

4. La ejecución del comando anterior debería mostrar algo como lo siguiente:

    ```sh
    [2022-04-16 09:44:22 +0000] [1] [INFO] Running on http://0.0.0.0:8081 (CTRL + C to quit)
    ```

## Comprobación de endpoints de servidor y métricas

Una vez arrancado el servidor, utilizando cualquier de las formas expuestas en los apartados anteriores, es posible probar las funcionalidades implementadas por el servidor:

- Comprobación de servidor FastAPI, a través de llamadas a los diferentes endpoints:

  - Realizar una petición al endpoint `/`

      ```sh
      curl -X 'GET' \
      'http://0.0.0.0:8081/' \
      -H 'accept: application/json'
      ```

      Debería devolver la siguiente respuesta:

      ```json
      {"message":"Hello World"}
      ```

  - Realizar una petición al endpoint `/health`

      ```sh
      curl -X 'GET' \
      'http://0.0.0.0:8081/health' \
      -H 'accept: application/json' -v
      ```

      Debería devolver la siguiente respuesta.

      ```json
      {"health": "ok"}
      ```

- Comprobación de registro de métricas, si se accede a la URL `http://0.0.0.0:8000` se podrán ver todas las métricas con los valores actuales en ese momento:

  - Realizar varias llamadas al endpoint `/` y ver como el contador utilizado para registrar las llamadas a ese endpoint, `main_requests_total` ha aumentado, se debería ver algo como lo mostrado a continuación:

    ```sh
    # TYPE main_requests_total counter
    main_requests_total 4.0
    ```

  - Realizar varias llamadas al endpoint `/health` y ver como el contador utilizado para registrar las llamadas a ese endpoint, `healthcheck_requests_total` ha aumentado, se debería ver algo como lo mostrado a continuación:

    ```sh
    # TYPE healthcheck_requests_total counter
    healthcheck_requests_total 26.0
    ```

  - También se ha credo un contador para el número total de llamadas al servidor `server_requests_total`, por lo que este valor debería ser la suma de los dos anteriores, tal y como se puede ver a continuación:

    ```sh
    # TYPE server_requests_total counter
    server_requests_total 30.0
    ```

## Tests

Se ha implementado tests unitarios para probar el servidor FastAPI, estos están disponibles en el archivo `src/tests/app_test.py`.

Es posible ejecutar los tests de diferentes formas:

- Ejecución de todos los tests:

    ```sh
    pytest
    ```

- Ejecución de todos los tests y mostrar cobertura:

    ```sh
    pytest --cov
    ```

- Ejecución de todos los tests y generación de report de cobertura:

    ```sh
    pytest --cov --cov-report=html
    ```

## Practica a realizar

A partir del ejemplo inicial descrito en los apartados anteriores es necesario realizar una serie de mejoras:

Los requirimientos son los siguientes:

- Añadir por lo menos un nuevo endpoint a los existentes `/` y `/health`, un ejemplo sería `/bye` que devolvería `{"msg": "Bye Bye"}`, para ello será necesario añadirlo en el fichero [src/application/app.py](./src/application/app.py)

- Creación de tests unitarios para el nuevo endpoint añadido, para ello será necesario modificar el [fichero de tests](./src/tests/app_test.py)

- Opcionalmente creación de helm chart para desplegar la aplicación en Kubernetes, se dispone de un ejemplo de ello en el laboratorio realizado en la clase 3

- Creación de pipelines de CI/CD en cualquier plataforma (Github Actions, Jenkins, etc) que cuenten por lo menos con las siguientes fases:

  - Testing: tests unitarios con cobertura. Se dispone de un [ejemplo con Github Actions en el repositorio actual](./.github/workflows/test.yaml)

  - Build & Push: creación de imagen docker y push de la misma a cualquier registry válido que utilice alguna estrategia de release para los tags de las vistas en clase, se recomienda GHCR ya incluido en los repositorios de Github. Se dispone de un [ejemplo con Github Actions en el repositorio actual](./.github/workflows/release.yaml)

- Configuración de monitorización y alertas:

  - Configurar monitorización mediante prometheus en los nuevos endpoints añadidos, por lo menos con la siguiente configuración:
    - Contador cada vez que se pasa por el/los nuevo/s endpoint/s, tal y como se ha realizado para los endpoints implementados inicialmente

  - Desplegar prometheus a través de Kubernetes mediante minikube y configurar alert-manager para por lo menos las siguientes alarmas, tal y como se ha realizado en el laboratorio del día 3 mediante el chart `kube-prometheus-stack`:
    - Uso de CPU de un contenedor mayor al del límite configurado, se puede utilizar como base el ejemplo utilizado en el laboratorio 3 para mandar alarmas cuando el contenedor de la aplicación `fast-api` consumía más del asignado mediante request

  - Las alarmas configuradas deberán tener severity high o critical

  - Crear canal en slack `<nombreAlumno>-prometheus-alarms` y configurar webhook entrante para envío de alertas con alert manager

  - Alert manager estará configurado para lo siguiente:
    - Mandar un mensaje a Slack en el canal configurado en el paso anterior con las alertas con label "severity" y "critical"
    - Deberán enviarse tanto alarmas como recuperación de las mismas
    - Habrá una plantilla configurada para el envío de alarmas

    Para poder comprobar si esta parte funciona se recomienda realizar una prueba de estres, como la realizada en el laboratorio 3 a partir del paso 8.

  - Creación de un dashboard de Grafana, con por lo menos lo siguiente:
    - Número de llamadas a los endpoints
    - Número de veces que la aplicación ha arrancado

## Entregables

Se deberá entregar mediante un repositorio realizado a partir del original lo siguiente:

- Código de la aplicación y los tests modificados
- Ficheros para CI/CD configurados y ejemplos de ejecución válidos
- Ficheros para despliegue y configuración de prometheus de todo lo relacionado con este, así como el dashboard creado exportado a `JSON` para poder reproducirlo
- `README.md` donde se explique como se ha abordado cada uno de los puntos requeridos en el apartado anterior, con ejemplos prácticos y guía para poder reproducir cada uno de ellos
