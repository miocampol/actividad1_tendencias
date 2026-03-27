# Actividad 1 - Tendencias

Este proyecto consiste en una aplicación web completa y "dockerizada" que cumple con todos los requisitos de arquitectura estructurada mediante contenedores. Incluye base de datos (PostgreSQL), su administrador (pgAdmin), backend (API Flask) y frontend (Nginx).

## Requisitos Previos (Entorno de Trabajo)

Para ejecutar este entorno local de forma exitosa, tu sistema operativo debe cumplir con:
1. Tener habilitado **WSL 2** (Windows Subsystem for Linux).
2. Tener instalada una distribución de Linux en WSL (Se recomienda fervientemente **Debian** o Ubuntu).
3. **Docker Desktop** instalado en Windows y configurado activando la integración con tu distro de WSL (Ej: Settings > Resources > WSL Integration > habilitar 'Debian').

## Guía de Ejecución Paso a Paso (Desde WSL)

Abre la terminal de tu distribución de WSL (Ej: Debian) y sigue estrictamente el orden de los siguientes comandos:

### 1. Clonar el repositorio
Descarga los archivos del proyecto directamente en el directorio deseado y entra en su carpeta:
```bash
git clone https://github.com/miocampol/actividad1_tendencias.git
cd actividad1_tendencias
```

### 2. Entrar a la ruta del Ecosistema
El `docker-compose.yml` base se encuentra dentro de la carpeta contenida del proyecto:
```bash
cd app
```

### 3. Compilar y Levantar el Proyecto Completo
Procederemos a descargar las imágenes (PostgreSQL, pgAdmin, Nginx) y compilar la de nuestro backend Flask para arrancar todos los servicios en segundo plano (`-d`):
```bash
docker-compose up -d --build
```
*(Nota: dependiendo de tu versión, puede que el comando aceptado sea sin el guion, es decir, `docker compose up -d --build`).*

### 4. Verificación de Salud (Healthcheck)
Comprueba el listado global de los 4 servicios. Debes cerciorarte de que estén todos en estado **`running`**, y de manera muy importante, que la base de datos de PostgreSQL reporte el estado **`healthy`**:
```bash
docker-compose ps
```

---

## URLs de Acceso a los Servicios

Una vez que todos los contenedores están arriba y operando, puedes interactuar navegando a los siguientes enlaces mediante el navegador de tu computadora Windows local:

* **Panel Frontend (Nginx):** [http://localhost:3000](http://localhost:3000)
* **API Backend (Flask):** [http://localhost:5000/](http://localhost:5000/) (Raíz) ó [http://localhost:5000/users](http://localhost:5000/users)
* **Administrador de BD (pgAdmin):** [http://localhost:8080](http://localhost:8080)
  * *Usuario:* `admin@admin.com`
  * *Contraseña:* `admin`

*(Para interactuar con la Base de Datos internamente, agrega el Server en pgAdmin ingresando Host: `db`, Port: `5432`, DB: `actividad_db`, Pass: `admin`).*

---

## Evidencias de Ejecución (Capturas de Pantalla)

A continuación se evidencian las 4 pruebas de validación requeridas en la rúbrica:

### 1. Estado de los contenedores (`docker compose ps`)
> **Nota:** Aquí se muestran los 4 servicios montados correctamente en estado "running" y la BD en estado "healthy".
<img width="1885" height="189" alt="image" src="https://github.com/user-attachments/assets/7f968aff-745b-4ea2-b73f-a65eb99ff784" />


### 2. Respuesta de la API (Navegador)
> **Nota:** Aquí se evidencia el consumo exitoso del GET hacia la API Flask y los datos devueltos en formato JSON.
<img width="756" height="899" alt="image" src="https://github.com/user-attachments/assets/904a3c41-e0ed-42e3-9945-287834398f21" />



### 3. Frontend funcionando en el navegador
> **Nota:** Aquí se muestra la tabla renderizada por el front-end en el puerto 3000, consumiendo los endpoints.
<img width="1913" height="1018" alt="image" src="https://github.com/user-attachments/assets/f87ba33d-32ab-4dae-ab93-7b88b4a79005" />



### 4. pgAdmin conectado y mostrando las tablas
> **Nota:** Aquí se aprecia pgAdmin enlazado al servicio `db`, desplegando el Schema `public` y las tablas generadas por `init.sql`.
<img width="1912" height="883" alt="image" src="https://github.com/user-attachments/assets/a3a7f2aa-cd61-4e30-bff9-90484ce04111" />

