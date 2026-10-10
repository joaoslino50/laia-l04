# Tutorial 2: Reflection Questions & Answers

## 1. What happens when the container starts?
When you start the container (`docker run -p 8000:8000 ml-flask-app`), Docker creates an isolated container instance and executes the command defined by `CMD ["bash", "run.sh"]` in the `Dockerfile`:
1. **`python train.py` executes first:** It loads the Iris dataset, trains a Logistic Regression classifier, and saves the trained weights to `/app/model.pkl`.
2. **`python app.py` executes next:** It loads `/app/model.pkl` into memory and launches the Flask web server listening on `0.0.0.0:8000`. The container is now ready to receive prediction requests at the `/predict` endpoint.

---

## 2. Why do we need to install dependencies inside the image?
* **Isolation:** A Docker container runs in an isolated Linux environment and does not have access to Python packages installed on the host machine or in local virtual environments.
* **Reproducibility & Portability:** Installing dependencies during the image build (`RUN pip install -r requirements.txt`) guarantees that the application runs identically on any operating system (macOS, Windows, Linux, cloud servers) without requiring external setup or encountering version conflicts.

---

## 3. Why do we expose port 8000:8000 (`-p 8000:8000`)?
* Container network interfaces are isolated by default. Applications running inside the container cannot be reached directly from the host network without explicit port mapping.
* The `-p <host_port>:<container_port>` flag bridges the host and container network:
  * The first `8000` is the port opened on your **host machine** (`localhost:8000`).
  * The second `8000` is the port inside the **container** where Flask is listening.
* This allows network traffic sent to `http://localhost:8000` on the host to be forwarded into port `8000` inside the container.

---

## 4. Where is `model.pkl` stored? What happens if we delete the container?
* **Location:** `model.pkl` is saved in the container's writable layer at `/app/model.pkl`.
* **Container Lifecycle & Ephemerality:** Container filesystems are ephemeral by default. Any changes or files created inside a container's writable layer exist only while that specific container exists.
* **If the container is deleted (`docker rm`):** The writable layer is destroyed and `model.pkl` is **permanently lost**. Starting a new container from the image will create a fresh container where `run.sh` will train the model again.

---

## 5. How could we persist the model using a volume?
Volumes store data outside the container's temporary writable layer, persisting files on the host machine even when containers are stopped or deleted.

### Approach A: Host Bind Mount
Map a directory from your host machine into the container using the `-v` flag:
```bash
docker run -p 8000:8000 -v $(pwd)/models:/app/models ml-flask-app
```
*(If `train.py` and `app.py` use `/app/models/model.pkl`, the model will be written directly to `./models/` on your host system).*

### Approach B: Docker Named Volume
Create a managed Docker volume independent of the host filesystem paths:
```bash
# 1. Create a named volume
docker volume create ml_models

# 2. Run the container mounting the named volume
docker run -p 8000:8000 -v ml_models:/app/models ml-flask-app
```
Even if the container is removed, `ml_models` retains the trained model so other containers can reuse it without retraining.
