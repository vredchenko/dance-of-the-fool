#!/bin/bash

# MamayLM System Requirements Checker for PopOS/Linux
# This script checks if your system meets the requirements to run MamayLM locally

echo "=================================================="
echo "  MamayLM System Requirements Checker"
echo "=================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. GPU Information
print_section "GPU Information"
if command_exists nvidia-smi; then
    echo -e "${GREEN}✓ NVIDIA GPU detected${NC}"
    nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader 2>/dev/null || nvidia-smi

    # Extract VRAM
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1)
    if [ -n "$VRAM" ]; then
        VRAM_GB=$((VRAM / 1024))
        echo ""
        echo "GPU VRAM: ${VRAM} MB (~${VRAM_GB} GB)"

        # Provide recommendation based on VRAM
        if [ "$VRAM_GB" -ge 24 ]; then
            echo -e "${GREEN}✓ Excellent! You can run MamayLM 12B at full precision${NC}"
        elif [ "$VRAM_GB" -ge 20 ]; then
            echo -e "${GREEN}✓ Good! You can run MamayLM 9B at full precision${NC}"
        elif [ "$VRAM_GB" -ge 12 ]; then
            echo -e "${YELLOW}⚠ Adequate. You can run MamayLM with 4-bit quantization${NC}"
        elif [ "$VRAM_GB" -ge 8 ]; then
            echo -e "${YELLOW}⚠ Limited. You can run smaller MamayLM 4B model with quantization${NC}"
        else
            echo -e "${RED}✗ Insufficient VRAM for comfortable MamayLM usage${NC}"
        fi
    fi
else
    echo -e "${RED}✗ NVIDIA GPU not detected or nvidia-smi not installed${NC}"
    echo "  MamayLM requires an NVIDIA GPU with CUDA support"

    # Check for AMD GPU
    if command_exists lspci && lspci | grep -i vga | grep -i amd >/dev/null; then
        echo -e "${YELLOW}⚠ AMD GPU detected - ROCm may work but is not officially supported${NC}"
    fi
fi

# 2. CUDA Information
print_section "CUDA Toolkit"
if command_exists nvcc; then
    CUDA_VERSION=$(nvcc --version | grep "release" | sed -n 's/.*release \([0-9.]*\).*/\1/p')
    echo -e "${GREEN}✓ CUDA Toolkit installed${NC}"
    echo "CUDA Version: $CUDA_VERSION"

    if [[ $(echo "$CUDA_VERSION >= 11.8" | bc -l 2>/dev/null) -eq 1 ]] || [[ "$CUDA_VERSION" > "11.8" ]]; then
        echo -e "${GREEN}✓ CUDA version is compatible (11.8+ required)${NC}"
    else
        echo -e "${YELLOW}⚠ CUDA 11.8 or higher recommended (you have $CUDA_VERSION)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ CUDA Toolkit not found (nvcc command not available)${NC}"
    echo "  You may still have CUDA runtime if nvidia-smi works"

    # Check for CUDA runtime
    if [ -d /usr/local/cuda ]; then
        echo "  CUDA directory found at /usr/local/cuda"
        if [ -f /usr/local/cuda/version.txt ]; then
            cat /usr/local/cuda/version.txt
        elif [ -f /usr/local/cuda/version.json ]; then
            cat /usr/local/cuda/version.json
        fi
    fi
fi

# 3. CPU Information
print_section "CPU Information"
if [ -f /proc/cpuinfo ]; then
    CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -n1 | cut -d: -f2 | xargs)
    CPU_CORES=$(grep -c "^processor" /proc/cpuinfo)

    echo "CPU Model: $CPU_MODEL"
    echo "CPU Cores: $CPU_CORES"

    if [ "$CPU_CORES" -ge 8 ]; then
        echo -e "${GREEN}✓ Good number of CPU cores (8+ recommended)${NC}"
    elif [ "$CPU_CORES" -ge 4 ]; then
        echo -e "${YELLOW}⚠ Adequate CPU cores, but 8+ recommended${NC}"
    else
        echo -e "${YELLOW}⚠ Limited CPU cores${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Could not read CPU information${NC}"
fi

# 4. RAM Information
print_section "System RAM"
if command_exists free; then
    TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    AVAILABLE_RAM=$(free -g | awk '/^Mem:/{print $7}')

    echo "Total RAM: ${TOTAL_RAM} GB"
    echo "Available RAM: ${AVAILABLE_RAM} GB"

    if [ "$TOTAL_RAM" -ge 48 ]; then
        echo -e "${GREEN}✓ Excellent RAM for MamayLM (48GB+ ideal)${NC}"
    elif [ "$TOTAL_RAM" -ge 32 ]; then
        echo -e "${GREEN}✓ Good RAM for MamayLM${NC}"
    elif [ "$TOTAL_RAM" -ge 24 ]; then
        echo -e "${YELLOW}⚠ Adequate RAM, but 32GB+ recommended${NC}"
    else
        echo -e "${YELLOW}⚠ Limited RAM - may have issues with larger models${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Could not determine RAM${NC}"
fi

# 5. Storage Space
print_section "Storage Space"
AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
echo "Available space in current directory: ${AVAILABLE_SPACE} GB"

if [ "$AVAILABLE_SPACE" -ge 100 ]; then
    echo -e "${GREEN}✓ Plenty of storage space${NC}"
elif [ "$AVAILABLE_SPACE" -ge 50 ]; then
    echo -e "${GREEN}✓ Adequate storage space (50GB recommended)${NC}"
elif [ "$AVAILABLE_SPACE" -ge 30 ]; then
    echo -e "${YELLOW}⚠ Minimum storage space (30GB needed for model files)${NC}"
else
    echo -e "${RED}✗ Insufficient storage space${NC}"
fi

# Check if SSD or HDD
ROOT_DISK=$(df . | awk 'NR==2 {print $1}' | sed 's/[0-9]*$//' | sed 's|/dev/||')
if [ -n "$ROOT_DISK" ] && [ -f "/sys/block/$ROOT_DISK/queue/rotational" ]; then
    ROTATIONAL=$(cat /sys/block/$ROOT_DISK/queue/rotational)
    if [ "$ROTATIONAL" -eq 0 ]; then
        echo -e "${GREEN}✓ SSD detected (recommended for faster model loading)${NC}"
    else
        echo -e "${YELLOW}⚠ HDD detected (SSD recommended for better performance)${NC}"
    fi
fi

# 6. Python Installation
print_section "Python Environment"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python3 installed${NC}"
    echo "Python Version: $PYTHON_VERSION"

    # Check if version is 3.8+
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        echo -e "${GREEN}✓ Python version is compatible (3.8+ required)${NC}"
    else
        echo -e "${YELLOW}⚠ Python 3.8 or higher recommended${NC}"
    fi
else
    echo -e "${RED}✗ Python3 not found${NC}"
fi

# Check pip
if command_exists pip3; then
    echo -e "${GREEN}✓ pip3 installed${NC}"
    pip3 --version
else
    echo -e "${YELLOW}⚠ pip3 not found${NC}"
fi

# 7. PyTorch Installation
print_section "PyTorch & CUDA Support"
if command_exists python3; then
    TORCH_CHECK=$(python3 -c "import torch; print(f'PyTorch {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'Device Count: {torch.cuda.device_count()}'); print(f'Device Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" 2>/dev/null)

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PyTorch installed${NC}"
        echo "$TORCH_CHECK"

        # Check if CUDA is available in PyTorch
        if echo "$TORCH_CHECK" | grep -q "CUDA Available: True"; then
            echo -e "${GREEN}✓ PyTorch has CUDA support enabled${NC}"
        else
            echo -e "${RED}✗ PyTorch installed but CUDA support not available${NC}"
            echo "  You may need to reinstall PyTorch with CUDA support:"
            echo "  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
        fi
    else
        echo -e "${YELLOW}⚠ PyTorch not installed${NC}"
        echo "  Install with: pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
    fi
else
    echo -e "${YELLOW}⚠ Cannot check PyTorch (Python3 not available)${NC}"
fi

# 8. Transformers Library
print_section "Hugging Face Libraries"
if command_exists python3; then
    # Check transformers
    TRANSFORMERS_VERSION=$(python3 -c "import transformers; print(transformers.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ transformers installed (version $TRANSFORMERS_VERSION)${NC}"
    else
        echo -e "${YELLOW}⚠ transformers not installed${NC}"
        echo "  Install with: pip3 install transformers"
    fi

    # Check accelerate
    ACCELERATE_VERSION=$(python3 -c "import accelerate; print(accelerate.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ accelerate installed (version $ACCELERATE_VERSION)${NC}"
    else
        echo -e "${YELLOW}⚠ accelerate not installed${NC}"
        echo "  Install with: pip3 install accelerate"
    fi

    # Check huggingface-hub
    HF_HUB_VERSION=$(python3 -c "import huggingface_hub; print(huggingface_hub.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ huggingface-hub installed (version $HF_HUB_VERSION)${NC}"
    else
        echo -e "${YELLOW}⚠ huggingface-hub not installed${NC}"
        echo "  Install with: pip3 install huggingface-hub"
    fi
fi

# 9. Optional Libraries
print_section "Optional Performance Libraries"
if command_exists python3; then
    # Check bitsandbytes
    BNB_VERSION=$(python3 -c "import bitsandbytes; print(bitsandbytes.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ bitsandbytes installed (version $BNB_VERSION) - for quantization${NC}"
    else
        echo -e "${YELLOW}⚠ bitsandbytes not installed (optional, for quantization)${NC}"
    fi

    # Check flash-attn
    FLASH_VERSION=$(python3 -c "import flash_attn; print(flash_attn.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ flash-attn installed (version $FLASH_VERSION) - for faster inference${NC}"
    else
        echo -e "${YELLOW}⚠ flash-attn not installed (optional, for faster inference)${NC}"
    fi

    # Check vllm
    VLLM_VERSION=$(python3 -c "import vllm; print(vllm.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ vllm installed (version $VLLM_VERSION) - for production serving${NC}"
    else
        echo -e "${YELLOW}⚠ vllm not installed (optional, for production serving)${NC}"
    fi
fi

# 10. Summary
print_section "Summary"
echo ""
echo "System Summary:"
echo "---------------"

# Create a simple readiness score
READINESS=0

# Check critical components
if command_exists nvidia-smi; then ((READINESS+=25)); fi
if [ -n "$VRAM_GB" ] && [ "$VRAM_GB" -ge 12 ]; then ((READINESS+=25)); fi
if [ -n "$TOTAL_RAM" ] && [ "$TOTAL_RAM" -ge 24 ]; then ((READINESS+=15)); fi
if command_exists python3; then ((READINESS+=10)); fi
if [ -n "$TORCH_CHECK" ] && echo "$TORCH_CHECK" | grep -q "CUDA Available: True"; then ((READINESS+=25)); fi

echo "Readiness Score: ${READINESS}/100"
echo ""

if [ "$READINESS" -ge 85 ]; then
    echo -e "${GREEN}✓ Your system is well-suited for running MamayLM!${NC}"
    echo "  You should be able to run MamayLM comfortably."
elif [ "$READINESS" -ge 60 ]; then
    echo -e "${YELLOW}⚠ Your system can run MamayLM with some limitations${NC}"
    echo "  Consider using quantized models (4-bit/8-bit) for better performance."
elif [ "$READINESS" -ge 35 ]; then
    echo -e "${YELLOW}⚠ Your system may struggle with MamayLM${NC}"
    echo "  You may need to use heavily quantized models or upgrade hardware."
else
    echo -e "${RED}✗ Your system does not meet minimum requirements${NC}"
    echo "  Consider upgrading GPU (24GB+ VRAM recommended) or using cloud services."
fi

echo ""
echo "=================================================="
echo "For detailed analysis, share this output with an AI assistant"
echo "=================================================="
