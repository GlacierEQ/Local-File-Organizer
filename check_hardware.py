import torch

def check_hardware():
    # Check for CUDA GPU availability
    if torch.cuda.is_available():
        print("CUDA GPU is available:", torch.cuda.get_device_name(0))
    else:
        print("CUDA GPU not detected.")

    # Check for NPU availability (example for vendor-specific NPUs; adjust based on your platform)
    try:
        if hasattr(torch, "npu") and torch.npu.is_available():
            print("NPU is available!")
        else:
            print("NPU not detected. Verify your NPU configuration and drivers.")
    except Exception as e:
        print("Error checking NPU:", e)

if __name__ == "__main__":
    check_hardware()
