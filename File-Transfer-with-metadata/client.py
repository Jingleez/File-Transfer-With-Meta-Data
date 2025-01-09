from socket import *
from struct import pack, unpack
import os, time, sys, logging, hashlib, struct

class FileTransferClient:
    def __init__(self, host, port, hash_length=8):
        # Do not modify this logger code. You can continue to use print() commands for your code.
        # The logger is in place to ensure that you receive proper output and debugging messages from the tester
        self.logger = logging.getLogger("CLIENT")
        self.handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False
        self.logger.info("Initializing client...")
        # End of logger code

        self.host = host
        self.port = port
        self.client_socket = None
        self.hash_length = hash_length


    def start(self):
        """
        Initiates a connection to the server and marks the client as running. This function
        does not attempt to send or receive any messages to or from the server.

        This method is responsible for establishing a socket connection to the specified
        server using the host and port attributes set during the client's initialization.
        It creates a TCP socket object, attempts to connect to the server, and sets the
        self.is_running attribute to True upon a successful connection. It logs
        the connection attempt and reports any errors encountered during the process.

        Returns: 
            True or false depending on whether the connection was successful.

        Exceptions:
            - OSError: Raised if the socket encounters a problem (e.g., network
              issue, invalid host/port).

        Usage Example:
            client = FileTransferClient(host='192.168.1.10', port=12345, hash_length=8)
            if client.start():
                ... do something ...

        Note:
            - It is important to call this method before attempting to send or receive
              messages using the client.
            - Ensure that the server is up and running at the specified host and port
              before calling this method.
        """
        # TODO: Implement the functionality described in this function's docstring
        try:
            self.logger.info(f"Starting client with host={self.host} and port={self.port}")
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.logger.info(f"Connected to server at {self.host}:{self.port}")
            self.is_running = True
            return True
        except OSError as e:
            print(f"Failed to start client: {e}")
            return False


    def read_file(self, filepath):
        """
        Reads the contents of a file and returns the data as a byte object.

        This is a helper function. You do not need to modify it. You can use it in the send_file
        method to read the contents of a file and return the data as a byte object.
        """
        with open(filepath, "rb") as file:
            data = file.read()
            return data
        

    def send_file(self, filepath):
        """
        Sends a file to the server using the established connection.

        File Transfer Protocol:
        1. Pack the metadata into a bytes object using the format below, up to but not including 
           the file data.
        2. Concatenate the file data to the metadata bytes object (e.g. metadata + file_data).
        3. Compute the hash of the metadata + file data and append it to the bytes object 
           containing the metadata and the file data (metadata + file data + hash).
        4. Send the bytes object (i.e. metadata + file data + hash) to the server.
        5. Wait for a response from the server containing the hash of the data the server received.
        6. If the server's hash matches the hash of the data sent, the file was sent successfully. 
           Return whether the file was sent successfully or not.

        Parameters:
            filepath (str): The path to the file to be sent.

        Returns:
            bool: True if the file was sent successfully, False otherwise.
        
        Exceptions:
            - TimeoutError: Raised if the socket times out while waiting for a response.
            - ConnectionResetError: Raised if the server resets the connection.
            - ConnectionAbortedError: Raised if the server aborts the connection.
            - OSError: Raised if the socket encounters a problem (e.g., network
              issue, invalid host/port).
              
        Usage Example:
            client = FileTransferClient("localhost", 5000)
            if client.start():
                client.send_file("source/test1.jpg")
        """
        # TODO: Implement the functionality described in this function's docstring
        try:
            file_content = self.read_file(filepath)
            hash_value = self.compute_hash(file_content, self.hash_length)
            file_metadata = self.encode_metadata(filepath)
            complete_message = file_metadata + file_content + hash_value
            self.client_socket.sendall(complete_message)
            print(f"File {filepath} sent successfully!")
            return True
        except Exception as error_exception:
            print(f"Error sending the file: {error_exception}")
        return False


    def encode_metadata(self, filepath):
        """
        Encodes file metadata into a byte format for transmission.

        Extracts and packs file metadata, including the name, extension, creation date,
        and size, into a structured byte format. This metadata precedes the file data
        in the transmission to the server, allowing the server to reconstruct and
        verify the file upon receipt.

        Packed Data Format:
            [filename_length(ushort)] - the length of the filename
            [file_extension_length(ubyte)] - the length of the file extension
            [created_length(ubyte)] - the length of the created time string
            [filename(varchar)] - a variable length string with the name of the file
            [file_extension(varchar)] - a variable length string with the file extension
            [created(varchar)] - a variable length string with the created time string
            [file_size(uint)]  - a variable length string with the unit type being requested
            [hash_length(ubyte)]  - a variable length string with the unit type being requested
            [file_data(varchar)] - a variable length string with the file data
            [hash(varchar)] - a variable length string with the hash of the file data

        Parameters:
            filepath (str): The path to the file for which metadata is being encoded.

        Returns:
            bytes: The encoded metadata in bytes format ready for transmission.

        Note:
            The encoded format is designed to be unpacked by the corresponding server
            method which expects the same structure.
        """
        # The following code gets the various file information you need to complete this function
        filename = os.path.basename(filepath)
        file_type = os.path.splitext(filename)[1].replace(".", "")
        created_date = time.ctime(os.path.getctime(filepath))
        file_size = os.path.getsize(filepath)

        # TODO: Implement the functionality described in this function's docstring
        fileNameSize = len(filename)
        fileExtensionSize = len(file_type)
        createdDateSize = len(created_date)
        format_string = f"!HBB{fileNameSize}s{fileExtensionSize}s{createdDateSize}sIB"
        data_encode = pack(format_string, fileNameSize, fileExtensionSize, createdDateSize, filename.encode(), file_type.encode(), created_date.encode(), file_size, self.hash_length)
        return data_encode

    def compute_hash(self, data, hash_length):
        """
        Computes a hash for given data using the SHAKE-128 algorithm.

        In this assignment, we'll use the hashlib library to compute a hash of the data
        being shared between the client and the server. A hash is a fixed-length string
        generated based on arbitrary input data. The same data will result in the same
        hash, and any change to the data will result in a different hash.  We're using this 
        very simplistically to introduce the idea of hashing and integrity checking, which 
        we'll be exploring in more detail later in the semester.

        1. Import hashlib and call hashlib.shake_128() to create a new SHAKE-128 hash object.
        2. Use the update() method to add the data to the hash object.
        3. Use the digest() method to retrieve the hash value and return it.

        The shake_128 algorithm is convenient for us since we can specify the length of the
        hash it produces. This allows us to generate a short hash for use in our tests.
        
        Parameters:
            data (bytes): The data to be hashed.
            hash_length (int): The desired length of the hash output.

        Returns:
            bytes: The computed hash.
        """
        # TODO: Implement the functionality described in this function's docstring
        shake = hashlib.shake_128()
        shake.update(data)
        hash_value = shake.digest(hash_length)
        return hash_value

    def shutdown(self):
        """
        Shuts down the client by stopping its operation and closing the socket.

        This method is responsible for cleanly terminating the client's operation.
        It indicates that the client is no longer in operation. If the client has an 
        active socket connection, it closes the socket to ensure proper release of 
        resources and network cleanup.

        The method logs the shutdown process, providing visibility into the client's
        state transitions. It's designed to be safely callable even if the socket is
        already closed or not initialized, preventing any unexpected exceptions during
        the shutdown process.

        Usage Example:
            client = FileTransferClient('192.168.1.10', 12345)
            if client.start():
                client.run()
                client.shutdown()

        Note:
            - Call this method to cleanly shut down the client after use or in case of an error.
            - Do NOT set client_socket to None in this method. The autograder will examine
                client_socket to ensure it is closed properly.
        """
        self.logger.info("Client is shutting down...")

         # TODO: Implement the functionality described in this function's docstring
        self.logger.removeHandler(self.handler)
        self.client_socket.close()
        print("Client shutdown complete.")

if __name__ == "__main__":
    client = FileTransferClient("localhost", 8005)
    if client.start():
        client.send_file("source/test1.jpg")
        client.send_file("source/test2.jpg")
        client.shutdown()
