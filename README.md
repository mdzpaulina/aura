# AURA - Adaptive Usage and Resource Agent

## Project Title & Description

**AURA** (Adaptive Usage and Resource Agent) is an intelligent Kubernetes resource optimization tool that leverages AI to analyze container consumption metrics and generate optimized resource configurations. 

AURA connects to your OCI Kubernetes clusters, extracts real-time metrics from your running pods, and uses Google's Gemini AI to recommend optimal CPU and memory settings. This helps reduce cloud infrastructure costs while maintaining system stability and performance.

### Why AURA?

- **Cost Optimization**: Intelligent resource recommendations to optimize cloud infrastructure spending
- **AI-Powered Analysis**: Leverages Google Gemini for intelligent decision-making
- **Safety-First Approach**: Implements safety margins over current consumption to prevent system crashes
- **CLI Interface**: Easy-to-use command-line tool for quick analysis

---

## Installation Instructions

### Prerequisites

- Python 3.10 or higher
- Access to an OCI Kubernetes cluster
- Google Gemini API key
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mdzpaulina/aura.git
   cd aura
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   nano .env
   ```

   Add the following to your `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Verify your setup:**
   ```bash
   python src/main.py status
   ```

### Docker Setup

1. **Build the Docker image:**
   ```bash
   docker build -t aura-cli .
   ```

2. **Run AURA in a container:**
   ```bash
   docker run -e GEMINI_API_KEY="your_key_here" \
     -v ~/.kube/config:/app/.kube/config:ro \
     aura-cli analyze default --save
   ```

---

## Usage Examples

### Analyze a Kubernetes Namespace

Analyze the `production` namespace and get AI-powered resource recommendations:

```bash
python src/main.py analyze production
```

**Output:**
```
Initializing AURA...
Connecting to OCI cluster to scan the namespace: production

Obtaining cluster metrics...
Sending metrics to AI for analysis...
Analysis complete. Recommendations:
{
  "recommendations": [
    {
      "container": "api-service",
      "new_cpu_limit": "optimized value",
      "new_memory_limit_mb": "optimized value",
      "reasoning": "Analysis based on current consumption patterns with safety margin applied."
    }
  ]
}
```

### Save Recommendations as YAML

Generate and automatically save optimized resource configurations:

```bash
python src/main.py analyze production --save
```

This creates an `optimized_resources.yaml` file ready to apply to your cluster.

### Check Connection Status

Verify that AURA can connect to your Kubernetes cluster and AI API:

```bash
python src/main.py status
```

**Output:**
```
Checking connection status...
Checking Kubernetes cluster...
Kubernetes connection: OK
Checking AI API...
AI API connection: OK
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **CLI Framework** | Typer | Command-line interface with rich formatting |
| **AI Engine** | Google Generative AI (Gemini) | Resource analysis and recommendations |
| **Kubernetes Client** | Python Kubernetes Client | Cluster metrics extraction |
| **Containerization** | Docker | Easy deployment and distribution |
| **Environment Management** | python-dotenv | Secure credential management |

---

## Troubleshooting / FAQ

### Q: "GEMINI_API_KEY environment variable is not set!"

**A:** Ensure your `.env` file exists in the project root and contains your API key:
```bash
cat .env  # Should show: GEMINI_API_KEY=your_key_here
```

### Q: "Error connecting to cluster: No clusters configured"

**A:** Make sure your Kubernetes config file is accessible:
```bash
cat ~/.kube/config  # Verify the file exists
export KUBECONFIG=~/.kube/config  # Set explicitly if needed
```

### Q: "Error connecting to AI API"

**A:** Verify your Gemini API key is valid and has the required permissions at [Google AI Studio](https://aistudio.google.com).

### Q: Docker: "Cannot connect to the Docker daemon"

**A:** Start Docker Desktop (Mac/Windows) or the Docker service (Linux):
```bash
# Mac
open /Applications/Docker.app

# Linux
sudo systemctl start docker
```

---

## Project Status / Roadmap

### ⚠️ Current Status: ALPHA (Not Yet Tested)

**Important Note:** AURA is currently in active development. The core functionality has been implemented, but **it has not yet been tested in a real Kubernetes cluster** due to no available nodes in the OCI cluster. All features are theoretical and require validation with actual cluster metrics.

**What this means:**
- ✅ Code structure and logic are in place
- ✅ API integrations (Kubernetes client, Gemini AI) are configured
- ✅ CLI interface is functional
- ❌ Real-world testing with actual pod metrics is pending
- ❌ Production readiness cannot be confirmed

**Before using AURA in production, you should:**
1. Test with a non-critical Kubernetes cluster
2. Validate that metrics extraction works correctly
3. Verify AI recommendations are accurate
4. Test the YAML generation and deployment process
5. Monitor actual cost savings over time

### Current Features (v1.0)
- ✅ Kubernetes cluster metrics extraction (not yet tested)
- ✅ AI-powered resource analysis (not yet tested)
- ✅ YAML recommendations generation (not yet tested)
- ✅ CLI interface with Typer
- ✅ Environment variable validation
- ✅ Docker support
- ✅ Error handling and logging

### Planned Features (Roadmap)
- 🔄 **GitHub Copilot Integration**: Native plugin for VS Code and IntelliJ IDEs
- 🔄 **Kubernetes RBAC Support**: ServiceAccount with minimal privileges (least privilege principle)
- 🔄 **Multi-cluster Support**: Analyze multiple OCI clusters simultaneously
- 🔄 **Historical Analysis**: Track resource recommendations over time
- 🔄 **Webhook Integration**: Automatic cluster analysis on scheduled intervals
- 🔄 **Web Dashboard**: Visual interface for monitoring and recommendations
- 🔄 **Cost Calculator**: Real-time cost savings estimation

### Next Priority: Security & Integration

1. **The Principle of Least Privilege (Kubernetes RBAC)**
   - Currently, AURA uses your personal `~/.kube/config` which may have admin permissions
   - **Solution**: Implement a dedicated Kubernetes ServiceAccount with read-only permissions
   - AURA will only be able to `get` and `list` pods and metrics, preventing accidental cluster damage
   - If AURA is compromised, the cluster automatically blocks unauthorized operations

2. **GitHub Copilot Extensions Integration**
   - Embed AURA directly into GitHub Copilot Chat in VS Code and IntelliJ
   - **Example usage**: `@aura analyze the frontend namespace and generate optimized YAML`
   - Architecture: Copilot Chat → AURA Backend → OCI Cluster → Gemini AI → Results in IDE
   - Seamless experience without leaving your development environment

---

## Author / Credits

**Developed by:** Paulina Méndez  
**GitHub:** [@mdzpaulina](https://github.com/mdzpaulina)  
**Repository:** [aura](https://github.com/mdzpaulina/aura)

### Acknowledgments

- Google Gemini AI for intelligent resource analysis
- Oracle OCI for Kubernetes infrastructure
- Open source community for amazing tools (Typer, kubernetes-client, etc.)

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

**MIT License Summary:**
- ✅ You can use, modify, and distribute this software
- ✅ Commercial and private use is allowed
- ✅ Must include the license and copyright notice
- ❌ No warranty is provided

For full license text, visit [MIT License](https://opensource.org/licenses/MIT)

---

## Quick Start Checklist

- [ ] Clone the repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Set up `.env` with GEMINI_API_KEY
- [ ] Run `python src/main.py status` to verify setup
- [ ] Analyze your first namespace: `python src/main.py analyze default`

---

## Support

For issues, questions, or suggestions:
- 📝 Open an issue on [GitHub Issues](https://github.com/mdzpaulina/aura/issues)
- 💬 Start a discussion on [GitHub Discussions](https://github.com/mdzpaulina/aura/discussions)
- 📧 Contact: mdzlopezp@gmail.com

---

**Made with ❤️ for Kubernetes optimization**
