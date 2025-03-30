## Liberando Productos - Práctica Final.
Este proyecto es una API desarrollada con FastAPI y desplegada en Kubernetes, monitorizada con Prometheus + Alertmanager + Grafana, e integrada con un pipeline de CI/CD usando GitHub Actions.
Incluye pruebas automatizadas, métricas personalizadas, alertas configuradas y un dashboard completo para visualización.


 ## Índice
 
- Estructura del proyecto.

- Ejecución local del servidor.

- Código para el nuevo endpoint y tests unitarios.

- CI/CD (GitHub Actions).

- Construcción de la imagen Docker.

- Despliegue y monitorización.

- Cómo reproducir paso a paso.





## Estructura del proyecto


```bash

LIBERANDO-PRODUCTOS-PRACTICA-RAMON-MEZA/
├── .github/                        # Configuración de workflows de GitHub Actions
│   └── workflows/
│       ├── release.yaml            # Workflow de despliegue (release)
│       └── test.yaml               # Workflow de tests automatizados
├── .pytest_cache/                 # Caché generada por pytest (puede ignorarse)
│   ├── v/
│   ├── .gitignore
│   └── CACHEDIR.TAG
├── README.md                      # Documentación principal del proyecto
├── helm-values/                   # Archivos de configuración personalizados para Helm
│   ├── additional-rules.yaml          # Reglas de alertas Prometheus personalizadas
│   ├── alertmanager-config.yaml       # Configuración de Alertmanager (webhook, rutas)
│   ├── alertmanager-secret.yaml       # Secret con el webhook de Slack
│   ├── kube-state-values.yaml         # Valores para desplegar kube-state-metrics
│   └── prometheus-persistence.yaml    # Configuración de persistencia para Prometheus
├── htmlcov/                       # Reportes de cobertura generados por pytest-cov
├── k8s/                           # Manifiestos Kubernetes para desplegar la app
│   ├── cpu-test-app.yaml              # Manifiesto para test de carga de CPU
│   ├── deployment.yaml                # Deployment de la app FastAPI
│   ├── fastapi-servicemonitor.yaml   # ServiceMonitor para Prometheus
│   └── service.yaml                  # Service que expone la app FastAPI
├── src/                           # Código fuente de la aplicación FastAPI
├── venv/                          # Entorno virtual de Python (excluido por git)
├── .coverage                      # Archivo de cobertura de tests
├── .gitignore                     # Archivos/Directorios excluidos del repo
├── Dockerfile                     # Imagen Docker para contenerizar la app
├── grafana-fastapi-dashboard.json # Dashboard de Grafana exportado (JSON)
├── Makefile                       # Comandos útiles para test, build, lint, etc.
├── pytest.ini                     # Configuración de pytest
├── requirements.txt               # Dependencias del proyecto


```




## Ejecución local del servidor.

**Verifica tu versión de Python**

Asegúrate de tener Python 3 instalado:

```sh
python3 --version
```

**Crear entorno virtual (virtualenv)**

En la raíz del proyecto, crea un entorno virtual:

```sh
python3 -m venv venv
```

**Activar el entorno virtual**

Activa el entorno.

```sh
source venv/bin/activate
```

**Instalar dependencias**

Instala las librerías necesarias:

```sh
pip install -r requirements.txt
```

**Ejecutar la aplicación**

```sh
python3 src/app.py
```


## Código para el nuevo endpoint y tests unitario.

- La app está escrita con FastAPI y expone varios endpoints (/, /bye, /health, /metrics).

- Se han añadido métricas personalizadas con prometheus_client:

- main_requests_total, bye_requests_total, healthcheck_requests_total, fastapi_app_starts_total

- Incluye tests con Pytest y cobertura:

📂 [Ver código App](./src/application/app.py)


[Endpoints](./imagenes/endpoint.png)


📂 [Ver código Test](./src/tests/app_test.py)


[Test Unitario](./imagenes/test_unitaria.png)


## CI/CD (GitHub Actions)

Workflows definidos:

### Testing: github/workflows/test.yaml
Este workflow se ejecuta automáticamente en cada push o pull request sobre ramas como main o develop. 

Su función es:
- Ejecutar tests unitarios de la aplicación (usando pytest).
- Generar un informe de cobertura de código.
- Validar que el código subido cumple con los estándares.
  
📂 Ver código en Test [código de tests](./.github/workflows/test.yaml)

[Workflows Test](./imagenes/cicd-test.png)

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
📂 Ver código en: Release [Código release](./.github/workflows/release.yaml)

 [Workflows Release Build & Push Image](./imagenes/cicd-release.png)

- La imagen se publica como: (**docker.io/ramon1743/liberando-productos-practica-final-ramon-meza:3.0.0)**

[Repositorio DockerHub](./imagenes/repo-imagendh.png)


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


**Subimo la imagen a DockerHu**

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

- Se crear el Webhook de Slack

- Se creó una app de Slack y se activó la opción de Incoming Webhooks.

- Se generó un webhook para el canal #ramon-prometheus-alarms.

- Con la url obtenida: 'https://hooks.slack.com/services/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'

- Se agrega la configuración del webhook en helm-values/alertmanager-config.yaml.

- Esto permite que todas las alertas activas y resueltas lleguen directamente a #ramon-prometheus-alarms


[Canla de alerta](./imagenes/slack.png)



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



[Alerta CPU ](./imagenes/test-cpu.png)



**Resultado**
Cada vez que se cumpla una condición de alerta:
- Slack recibe una notificación clara y estructurada en el canal #ramon-prometheus-alarms.
- Así nos actuar de forma inmediata ante problemas de infraestructura o aplicación.





## Dashboard de Grafana 
Se ha creado un dashboard desde cero en Grafana, el cual muestra:

- Número de llamadas a los endpoints.

- Número de veces que la aplicación ha arrancado.

Archivo JSON [grafana-fastapi-dashboard](./grafana-fastapi-dashboard.json)




**Acceso a Grafana**

Grafana está expuesto en el clúster de Kubernetes en el puerto 30000, por lo tanto, puedes acceder desde tu navegador con:



```bash
http://localhost:3000
```





**Login Grafana**


- Usuario: **admin**

- Contraseña: **prom-operator**


[Dashboard-Grafana/](./imagenes/metricas.png)




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

[Pods](./imagenes/pods.png)


**Validar de que todos los pods estén en estado Running, tanto de la app como del stack monitoring.**

**Verificar servicios**

```bash
kubectl get svc
```

[Servicios/](./imagenes/svc.png)


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












