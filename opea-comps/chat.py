from flask import Flask, request, jsonify
import os
import requests
from comps import MicroService, ServiceOrchestrator, ServiceType

# Set default environment variables
EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 8008)

app = Flask(__name__)

import requests


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.megaservice = ServiceOrchestrator()  # The orchestrator that manages services
        self.services = {}  # Dictionary to store service references

    def add_remote_service(self):
        """Define and add remote services to the orchestrator."""
        embedding = MicroService(
            name="embedding",
            host=EMBEDDING_SERVICE_HOST_IP,
            port=EMBEDDING_SERVICE_PORT,
            endpoint="/v1/embeddings",
            use_remote_service=True,
            service_type=ServiceType.EMBEDDING,
        )
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )

        # Add services to orchestrator
        self.megaservice.add(embedding).add(llm)
        self.megaservice.flow_to(embedding, llm)

        # Store references to the services for later access
        self.services["embedding"] = embedding
        self.services["llm"] = llm

    def start_services(self):
        """Start all the services in the orchestrator."""
        if not self.services:
            self.add_remote_service()  # Add services if not already added

        # Start services in the orchestrator
        for service_name, service in self.services.items():
            print(f"Starting service: {service_name}")
            service.start()  # Assuming MicroService has a start method

        print("All services started.")

    def stop_services(self):
        """Stop all services in the orchestrator."""
        if not self.services:
            print("No services are added or available to stop.")
            return

        # Stop services in the orchestrator
        for service_name, service in self.services.items():
            print(f"Stopping service: {service_name}")
            service.stop()  # Assuming MicroService has a stop method

        print("All services stopped.")

    def chat(self, prompt):
        """Interact with the LLM service to generate a response."""
        try:
            # Ensure that the LLM service is stored correctly
            llm_service = self.services.get("llm")
            if not llm_service:
                raise ValueError("LLM service not found in orchestrator.")

            # Build the valid payload structure with the model
            messages = [{"role": "user", "content": prompt}]  # LLM expects 'messages' in this structure
            model = "llama3.2:1b"  # Or any other model name you need, e.g., "gpt-4"

            # Send prompt to the LLM service
            response = requests.post(
                f"http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}/v1/chat/completions",
                json={
                    "model": model,  # Include the model field
                    "messages": messages,  # Include the messages
                },
            )

            if response.status_code == 200:
                result = response.json()
                # Directly return the response content to the user
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0].get('message', 'No message field found.')
                else:
                    return 'No valid response from LLM service.'
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Error in chatting with LLM service: {e}")
            return "An error occurred while trying to chat with the LLM service."


# Initialize service
service = ExampleService()


@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """Handle incoming chat requests."""
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided."}), 400

    prompt = data['prompt']

    # Call chat method
    response = service.chat(prompt)

    # Return the response to the client
    return jsonify({"response": response})


@app.route('/api/connect', methods=['GET'])
def check_services():
    """Check if the remote services (LLM and embedding) are reachable."""
    if service.create_connection():
        return jsonify({"status": "success", "message": "Connected to all services."}), 200
    else:
        return jsonify({"status": "failure", "message": "Failed to connect to one or more services."}), 500


@app.route('/api/start', methods=['GET'])
def start_services():
    """Start services."""
    try:
        service.start_services()
        return jsonify({"status": "success", "message": "Services started."}), 200
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)}), 500


@app.route('/api/stop', methods=['GET'])
def stop_services():
    """Stop services."""
    try:
        service.stop_services()
        return jsonify({"status": "success", "message": "Services stopped."}), 200
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)}), 500


if __name__ == '__main__':
    # Add remote services before starting the Flask app
    service.add_remote_service()
    app.run(host='0.0.0.0', port=8000, debug=True)