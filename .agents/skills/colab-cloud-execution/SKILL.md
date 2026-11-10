---
name: colab-cloud-execution
description: Provision remote Google Colab GPU/TPU/CPU runtimes and execute Python scripts, notebooks, or shell workloads headlessly via the official Google Colab CLI (`colab`).
metadata:
  origin: AGYOS
---

# Google Colab CLI (`colab`) Cloud Execution Runbook

This runbook guides running notebooks and heavy computational workloads remotely on Google Colab hardware accelerators (T4, L4, A100, H100 GPUs, v5e1/v6e1 TPUs) using the official Google Colab CLI (`google-colab-cli`).

## 1. Overview & Core Model

The official Google Colab CLI connects your local terminal and agent workflows directly to Colab cloud virtual machines without needing an open browser tab:
- **Session Lifecycle**: `colab new` provisions a cloud VM; `colab stop` releases it.
- **Kernel Persistence**: State (imports, defined variables, functions) persists across separate `colab exec` calls within the same session.
- **Default Directory**: Working directory defaults to `/content`.
- **Ephemeral Jobs**: `colab run` provisions a fresh accelerator VM, executes a local script, captures output, and tears down the VM automatically.

## 2. Authentication

The CLI supports two authentication modes:

### Mode A: OAuth2 Flow (Interactive / First Use)
```bash
colab --auth=oauth2 sessions
```
Prompts for Google account consent in your default browser on first invocation and caches credentials locally at `~/.config/colab-cli/token.json`.

### Mode B: Application Default Credentials (ADC)
For headless environments using `gcloud`:
```bash
gcloud auth application-default login \
  --scopes=openid,\
https://www.googleapis.com/auth/cloud-platform,\
https://www.googleapis.com/auth/userinfo.email,\
https://www.googleapis.com/auth/colaboratory
```
Verify authentication with:
```bash
colab sessions
```

## 3. Command Reference

### Provisioning Compute
```bash
# Provision standard CPU session
colab new -s my-session

# Provision GPU sessions (T4, L4, A100, H100)
colab new -s gpu-session --gpu T4
colab new -s train-run --gpu A100

# Provision TPU sessions (v5e1, v6e1)
colab new -s tpu-run --tpu v6e1
```
*Always specify `-s <name>` to give the session a deterministic reference.*

### Remote Execution
```bash
# Execute a local Python file on the remote Colab VM
colab exec -s my-session -f train.py

# Execute inline Python snippets
echo "import torch; print(torch.cuda.get_device_name(0))" | colab exec -s my-session

# Run an entire Jupyter Notebook (.ipynb) and produce output notebook
colab exec -s my-session -f analysis.ipynb

# Install packages on the remote VM
colab install -s my-session torch torchvision torchaudio
```

### Ephemeral One-Shot Jobs (`colab run`)
Provisions compute, runs script, streams output, and automatically terminates the VM:
```bash
# Run script on a T4 GPU and auto-cleanup
colab run --gpu T4 train_model.py

# Run script with CLI arguments
colab run --gpu A100 train.py --epochs 50 --batch-size 32
```

### File Synchronization
```bash
# Upload local dataset or script to remote Colab
colab upload -s my-session ./data.csv /content/data.csv

# Download trained model weights or outputs
colab download -s my-session /content/model.pth ./model.pth

# List files on remote VM
colab ls -s my-session /content
```

### Resource Teardown (Mandatory)
Always terminate sessions when work is complete to prevent consuming compute quota:
```bash
# Check status and active sessions
colab sessions
colab status -s my-session

# Stop and release VM
colab stop -s my-session
```

## 4. Verification & Diagnostics

- **Inspect Execution History**: `colab log -s my-session -n 20`
- **Restart Wedged Kernel**: `colab restart-kernel -s my-session`
- **Inspect Compute Unit Balance**: `colab usage`
