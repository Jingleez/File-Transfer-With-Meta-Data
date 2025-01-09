# File Transfer with Metadata

This project demonstrates a basic client-server application for secure file transfer using Python sockets. The application allows a client to send files to a server, where they are saved and verified for integrity using cryptographic hashing.

---

## Features

### **Server**
- Accepts multiple file transfers from clients.
- Saves received files in the `received_files` directory.
- Verifies file integrity using SHAKE-128 hashing.
- Sends a computed hash back to the client for validation.
- Handles multiple client connections in sequence.

### **Client**
- Connects to the server and sends files.
- Encodes file metadata (name, type, creation date, size) for structured transmission.
- Computes and appends a SHAKE-128 hash of the file for integrity checking.
- Receives hash verification from the server to confirm successful transfer.

---

## File Structure

### **Server (`server.py`)**
- **`FileTransferServer` Class**
  - Initializes the server with logging and file storage setup.
  - Starts a TCP server to accept client connections.
  - Handles file reception, metadata unpacking, and hash validation.
  - Writes received files to the `received_files` directory.

### **Client (`client.py`)**
- **`FileTransferClient` Class**
  - Connects to the server using TCP.
  - Reads files and sends them with encoded metadata.
  - Appends a cryptographic hash for integrity verification.
  - Validates server responses to ensure successful file transmission.

---

## Requirements

- Python 3.6+
- Modules: `socket`, `struct`, `hashlib`, `logging`, `os`, `time`, `sys`
