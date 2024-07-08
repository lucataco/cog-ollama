from cog import BasePredictor, Input, ConcatenateIterator
import os
import json
import time
import requests
import subprocess

MODEL_NAME = "llama3:8b"
OLLAMA_API = "http://127.0.0.1:11434"
OLLAMA_GENERATE = OLLAMA_API + "/api/generate"
MODEL_CACHE = "/usr/share/ollama/.ollama/models/blobs"
MODEL_URL = "https://weights.replicate.delivery/default/ollama/llama3/8b.tar"

def download_weights(url, dest):
    start = time.time()
    print("downloading url: ", url)
    print("downloading to: ", dest)
    subprocess.check_call(["pget", "-xf", url, dest], close_fds=False)
    print("downloading took: ", time.time() - start)

class Predictor(BasePredictor):
    def setup(self):
        """Setup necessary resources for predictions"""
        # Start server
        print("Starting ollama server")
        subprocess.Popen(["ollama", "serve"])
        # Download weights
        print("Downloading weights")
        if not os.path.exists(MODEL_CACHE):
            download_weights(MODEL_URL, MODEL_CACHE)
        # Load model
        print("Running model")
        subprocess.check_call(["ollama", "run", MODEL_NAME], close_fds=False)

    def predict(self,
            prompt: str = Input(description="Input text for the model"),
    ) -> ConcatenateIterator[str]:
        """Run a single prediction on the model and stream the output"""
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        start_time = time.time()
        
        with requests.post(
            OLLAMA_GENERATE,
            headers=headers,
            data=json.dumps(payload),
            stream=True,
            timeout=60
        ) as response:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            yield chunk['response']
                    except json.JSONDecodeError:
                        print("Failed to parse response chunk as JSON")
        
        end_time = time.time()
        total_time = end_time - start_time
        print("Total runtime:", total_time)