import torch
print(torch.cuda.is_available())  # Should return True if GPU is available
print(torch.cuda.device_count())  # Should return the number of GPUs available (e.g., 1)
print(torch.cuda.current_device())  # Should return the current device ID
print(torch.cuda.get_device_name(0))  # Should return the name of your GPU
