import requests

# 1. Single sample prediction
url_single = "http://localhost:8000/predict"
payload_single = {"features": [5.1, 3.5, 1.4, 0.2]}
response_single = requests.post(url_single, json=payload_single)
print("Single prediction:", response_single.json())

# 2. Batch sample prediction
url_batch = "http://localhost:8000/prediction-batch"
payload_batch = {
    "features": [
        [5.1, 3.5, 1.4, 0.2],
        [6.7, 3.0, 5.2, 2.3]
    ]
}
response_batch = requests.post(url_batch, json=payload_batch)
print("Batch predictions:", response_batch.json())

