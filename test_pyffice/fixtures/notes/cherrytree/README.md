# cr1pt

`cr1pt` is a helper module designed to combine various encryption, decryption, signing, and hashing libraries into a convenient package for Python applications. This module aims to simplify the integration and usage of multiple cryptographic tools by providing a unified interface.

## Features

- **Encryption and Decryption:** Support for various encryption algorithms, making data protection straightforward and secure.
- **Digital Signing:** Create and verify digital signatures to ensure the authenticity and integrity of data.
- **Hashing:** Generate secure hashes for data verification and password storage.
- **Convenient Interface:** A streamlined API that abstracts away the complexities of underlying cryptographic libraries, making it easy to use even if you're not a cryptography expert.

## Installation

You can install `cr1pt` via pip:

```bash
pip install cr1pt
```

## Usage

Here are some examples of how to use the key features of `cr1pt`:

### Encryption and Decryption

Encrypting and decrypting data is straightforward with `cr1pt`.

```python
import cr1pt

# Encrypt data
encrypted_data = cr1pt.encrypt("my_secret_data", key="my_secret_key")

# Decrypt data
decrypted_data = cr1pt.decrypt(encrypted_data, key="my_secret_key")
print(decrypted_data)  # Output: my_secret_data
```

### Digital Signing

Sign data to ensure its authenticity, and verify the signatures.

```python
import cr1pt

# Sign data
signature = cr1pt.sign("important_message", private_key="my_private_key")

# Verify signature
is_valid = cr1pt.verify("important_message", signature, public_key="my_public_key")
print(is_valid)  # Output: True or False
```

### Hashing

Generate secure hashes to verify the integrity of data or store passwords safely.

```python
import cr1pt

# Generate a hash
data_hash = cr1pt.hash("sensitive_data")
print(data_hash)

# Verify a hash
is_match = cr1pt.verify_hash("sensitive_data", data_hash)
print(is_match)  # Output: True or False
```

## Supported Libraries

`cr1pt` integrates with several popular cryptographic libraries, including:

- `PyCryptodome` for encryption and decryption.
- `cryptography` for digital signatures and various cryptographic utilities.
- `hashlib` for hashing functions.

## Contributing

We welcome contributions from the community! If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature_branch`).
3. Commit your changes (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature_branch`).
5. Open a Pull Request.

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

`cr1pt` is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or suggestions, feel free to reach out to us at [contact@example.com](mailto:contact@example.com).