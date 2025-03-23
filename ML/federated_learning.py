import torch
import torch.nn as nn
import torch.optim as optim
import syft as sy  # Import PySyft for Federated Learning

# Create the hook for PySyft (this is no longer TorchHook in newer versions)
hook = sy.TorchHook(torch)  # This still works in some versions of PySyft

# Create two virtual clients (workers)
client1 = sy.VirtualWorker(hook, id="client1")
client2 = sy.VirtualWorker(hook, id="client2")

# Sample training data for the clients
data_client1 = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True).send(client1)
target_client1 = torch.tensor([[2.0], [4.0], [6.0]]).send(client1)

data_client2 = torch.tensor([[4.0], [5.0], [6.0]], requires_grad=True).send(client2)
target_client2 = torch.tensor([[8.0], [10.0], [12.0]]).send(client2)

# Define a simple linear model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

# Initialize the global model
global_model = SimpleModel()

# Function to train the model on the clients
def train_on_client(model, data, target, client):
    model.send(client)  # Send model to the client

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    for _ in range(10):  # Train for 10 epochs
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    model.get()  # Get the model back from the client
    return model

# Train the model on client1
model_client1 = train_on_client(global_model, data_client1, target_client1, client1)
# Train the model on client2
model_client2 = train_on_client(global_model, data_client2, target_client2, client2)

# Federated Averaging: average the model parameters from both clients
def federated_average(models):
    global_dict = models[0].state_dict()  # Get the first model's state dict
    for key in global_dict.keys():
        global_dict[key] = torch.mean(torch.stack([m.state_dict()[key] for m in models]), dim=0)

    global_model.load_state_dict(global_dict)

# Aggregate the models from both clients
federated_average([model_client1, model_client2])

print("Global model trained using Federated Learning with PySyft 0.7+!")
