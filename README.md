# AI Learning Data Format (.aidata)

The `.aidata` format is a robust, future-proof file format designed to preserve AI learning data, especially for free-tier environments with resource constraints. It enables seamless knowledge continuity across AI systems, allowing models to save and resume learnings efficiently. This repository includes the format specification, CLI tools for managing `.aidata` files, and a validation script.

## Features
- **Structured Knowledge Preservation**: Stores AI learnings with metadata, evolution tracking, and ML-specific sections.
- **Security and Privacy**: Supports AES-256 encryption and integrity hashing for sensitive data.
- **Free-Tier Friendly**: Automated checkpointing and deduplication for resuming workflows under quota limits.
- **Interoperability**: Structured JSON output and integration protocols (REST/GraphQL) for compatibility with AI systems.
- **Extensibility**: Supports advanced features like bias detection, visualization, and multilingual metadata.

## Getting Started

### Prerequisites
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt` (e.g., `cryptography`, `psutil`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/drsiranjeevi/aidata-format.git
   cd aidata-format
   ```
2. Install required packages:
   ```bash
   pip install cryptography psutil
   ```

### Usage
- **Create/Edit `.aidata` Files**:
  ```bash
  python scripts/aidata_cli.py create base.aidata
  python scripts/aidata_cli.py add base.aidata "New learning entry"
  ```
- **Encrypt/Decrypt Files**:
  ```bash
  python scripts/aidata_crypto_cli.py encrypt base.aidata base.aidata.enc --password
  python scripts/aidata_crypto_cli.py decrypt base.aidata.enc base.aidata.dec --password
  ```
- **Validate Files**:
  ```bash
  python scripts/validate_aidata.py base.aidata
  ```

### Example
A sample `.aidata` file for trading strategies is included in `examples/sample_trading.aidata`. It demonstrates how to document AI-driven trading decisions using the format.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please read `CONTRIBUTING.md` for details and ensure your changes align with the format's goals.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact
For questions or feedback, open an issue or contact the maintainer at [your-email@example.com].