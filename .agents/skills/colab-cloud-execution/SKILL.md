---
name: colab-cloud-execution
description: Provision remote Google Colab GPU/TPU/CPU runtimes and execute Python scripts, notebooks, or shell workloads headlessly via the official Google Colab CLI (`colab`).
metadata:
  origin: AGYOS
prompt-source: prompt.toon
---
skill: "colab-cloud-execution"
sections[13]:
  - "\n"
  - "# Google Colab CLI (`colab`) Cloud Execution Runbook\n\nThis runbook guides running notebooks and heavy computational workloads remotely on Google Colab hardware accelerators (T4, L4, A100, H100 GPUs, v5e1/v6e1 TPUs) using the official Google Colab CLI (`google-colab-cli`).\n\n"
  - "## 1. Overview & Core Model\n\nThe official Google Colab CLI connects your local terminal and agent workflows directly to Colab cloud virtual machines without needing an open browser tab:\n- **Session Lifecycle**: `colab new` provisions a cloud VM; `colab stop` releases it.\n- **Kernel Persistence**: State (imports, defined variables, functions) persists across separate `colab exec` calls within the same session.\n- **Default Directory**: Working directory defaults to `/content`.\n- **Ephemeral Jobs**: `colab run` provisions a fresh accelerator VM, executes a local script, captures output, and tears down the VM automatically.\n\n"
  - "## 2. Authentication\n\nThe CLI supports two authentication modes:\n\n"
  - "### Mode A: OAuth2 Flow (Interactive / First Use)\n```bash\ncolab --auth=oauth2 sessions\n```\nPrompts for Google account consent in your default browser on first invocation and caches credentials locally at `~/.config/colab-cli/token.json`.\n\n"
  - "### Mode B: Application Default Credentials (ADC)\nFor headless environments using `gcloud`:\n```bash\ngcloud auth application-default login \\\n  --scopes=openid,\\\nhttps://www.googleapis.com/auth/cloud-platform,\\\nhttps://www.googleapis.com/auth/userinfo.email,\\\nhttps://www.googleapis.com/auth/colaboratory\n```\nVerify authentication with:\n```bash\ncolab sessions\n```\n\n"
  - "## 3. Command Reference\n\n"
  - "### Provisioning Compute\n```bash\n# Provision standard CPU session\ncolab new -s my-session\n\n# Provision GPU sessions (T4, L4, A100, H100)\ncolab new -s gpu-session --gpu T4\ncolab new -s train-run --gpu A100\n\n# Provision TPU sessions (v5e1, v6e1)\ncolab new -s tpu-run --tpu v6e1\n```\n*Always specify `-s <name>` to give the session a deterministic reference.*\n\n"
  - "### Remote Execution\n```bash\n# Execute a local Python file on the remote Colab VM\ncolab exec -s my-session -f train.py\n\n# Execute inline Python snippets\necho \"import torch; print(torch.cuda.get_device_name(0))\" | colab exec -s my-session\n\n# Run an entire Jupyter Notebook (.ipynb) and produce output notebook\ncolab exec -s my-session -f analysis.ipynb\n\n# Install packages on the remote VM\ncolab install -s my-session torch torchvision torchaudio\n```\n\n"
  - "### Ephemeral One-Shot Jobs (`colab run`)\nProvisions compute, runs script, streams output, and automatically terminates the VM:\n```bash\n# Run script on a T4 GPU and auto-cleanup\ncolab run --gpu T4 train_model.py\n\n# Run script with CLI arguments\ncolab run --gpu A100 train.py --epochs 50 --batch-size 32\n```\n\n"
  - "### File Synchronization\n```bash\n# Upload local dataset or script to remote Colab\ncolab upload -s my-session ./data.csv /content/data.csv\n\n# Download trained model weights or outputs\ncolab download -s my-session /content/model.pth ./model.pth\n\n# List files on remote VM\ncolab ls -s my-session /content\n```\n\n"
  - "### Resource Teardown (Mandatory)\nAlways terminate sessions when work is complete to prevent consuming compute quota:\n```bash\n# Check status and active sessions\ncolab sessions\ncolab status -s my-session\n\n# Stop and release VM\ncolab stop -s my-session\n```\n\n"
  - "## 4. Verification & Diagnostics\n\n- **Inspect Execution History**: `colab log -s my-session -n 20`\n- **Restart Wedged Kernel**: `colab restart-kernel -s my-session`\n- **Inspect Compute Unit Balance**: `colab usage`\n"
