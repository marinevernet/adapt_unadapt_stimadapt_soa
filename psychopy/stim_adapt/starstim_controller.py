import socket
import time


class StarstimController:

    PORT = 1235

    # Command codes
    CMD_QUERY_STATUS = 128
    CMD_VERSION = 131
    CMD_LOAD_PROTOCOL = 135
    CMD_UNLOAD_PROTOCOL = 136
    CMD_START_PROTOCOL = 137
    CMD_ABORT_PROTOCOL = 138

    # Status codes
    STATUS_REMOTE_CONTROL_ALLOWED = 200
    STATUS_REMOTE_CONTROL_REJECTED = 201
    STATUS_VERSION_RECEIVED = 202
    STATUS_SYNCHRONIZING = 203
    STATUS_IDLE = 204
    STATUS_PROTOCOL_NOT_LOADED = 205
    STATUS_PROTOCOL_LOADING = 206
    STATUS_PROTOCOL_LOADED = 207
    STATUS_PROTOCOL_RUNNING = 208
    STATUS_PROTOCOL_ERROR = 209
    STATUS_PROTOCOL_ABORTED = 212
    STATUS_PROTOCOL_ABORTING = 213
    STATUS_CHECK_IMPEDANCE = 221

    MATNIC_VERSION = "04.07"

    def __init__(self, host):
        self.host = host
        # self.host - 'localhost'
        self.sock = None

    # =========================
    # LOW LEVEL
    # =========================

    def _send_byte(self, value):
        self.sock.sendall(bytes([value]))

    def _send_string(self, text):
        self.sock.sendall(text.encode("ascii"))
        self.sock.sendall(b"\x00")

    def _read_status(self):
        data = self.sock.recv(1)
        if not data:
            raise RuntimeError("No response from NIC server")

        signed = int.from_bytes(data, byteorder='big', signed=True)
        return 256 + signed

    # =========================
    # CONNECTION
    # =========================

    def connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect((self.host, self.PORT))

        # Send version
        self._send_byte(self.CMD_VERSION)
        self._send_string(self.MATNIC_VERSION)

        status = self._read_status()

        print(status)

        # if status != self.STATUS_VERSION_RECEIVED:
        if status != self.STATUS_IDLE:
            raise RuntimeError("Version rejected by NIC")

        # Wait for idle
        for _ in range(25):
            status = self.query_status()
            if status == self.STATUS_IDLE:
                break
            time.sleep(1)

        # Wait for remote control confirmation
        print("Confirm remote control in NIC2...")
        for _ in range(20):
            status = self.query_status()

            if status == self.STATUS_REMOTE_CONTROL_ALLOWED:
                print("Remote control granted")
                return

            if status == self.STATUS_REMOTE_CONTROL_REJECTED:
                raise RuntimeError("Remote control rejected")

            time.sleep(1)

        raise RuntimeError("Remote control timeout")

    def close(self):
        if self.sock:
            self.sock.close()

    # =========================
    # STATUS
    # =========================

    def query_status(self):
        self._send_byte(self.CMD_QUERY_STATUS)
        return self._read_status()

    # =========================
    # PROTOCOL CONTROL
    # =========================

    def load_protocol(self, protocol_name):

        status = self.query_status()
        if status == self.STATUS_PROTOCOL_RUNNING:
            raise RuntimeError("Protocol already running")

        self._send_byte(self.CMD_LOAD_PROTOCOL)
        self._send_string(protocol_name)

        for _ in range(20):
            status = self.query_status()

            if status == self.STATUS_PROTOCOL_LOADED:
                return

            if status == self.STATUS_PROTOCOL_ERROR:
                raise RuntimeError("Protocol load error")

            time.sleep(1)

        raise RuntimeError("Load timeout")

    def start_protocol(self):

        status = self.query_status()
        if status != self.STATUS_PROTOCOL_LOADED:
            raise RuntimeError("Protocol not loaded")

        self._send_byte(self.CMD_START_PROTOCOL)

        for _ in range(20):
            status = self.query_status()

            if status == self.STATUS_PROTOCOL_RUNNING:
                return

            if status == self.STATUS_PROTOCOL_ERROR:
                raise RuntimeError("Protocol start error")

            time.sleep(1)

        raise RuntimeError("Start timeout")

    def abort_protocol(self):
        """
        Exact MATLAB equivalent of MatNICAbortProtocol
        """

        status = self.query_status()

        if status != self.STATUS_PROTOCOL_RUNNING:
            print("NIC is not running a Protocol.")
            return -2

        self._send_byte(self.CMD_ABORT_PROTOCOL)

        retries = 0
        max_retries = 20

        while True:

            status = self.query_status()

            if retries >= max_retries:
                return -3

            if status == self.STATUS_PROTOCOL_RUNNING:
                print("Protocol still running")

            elif status == self.STATUS_PROTOCOL_ABORTING:
                print("Protocol aborting")

            elif status == self.STATUS_PROTOCOL_ABORTED:
                print("Protocol aborted")
                return 0

            elif status == self.STATUS_PROTOCOL_ERROR:
                print("Protocol error during abort")
                return 0

            time.sleep(1)
            retries += 1

    def unload_protocol(self):
        """
        Exact MATLAB equivalent of MatNICUnloadProtocol
        """

        status = self.query_status()

        if status == self.STATUS_PROTOCOL_NOT_LOADED:
            return -6

        if status == self.STATUS_CHECK_IMPEDANCE:
            return -7

        if status == self.STATUS_PROTOCOL_RUNNING:
            return -8

        self._send_byte(self.CMD_UNLOAD_PROTOCOL)

        while True:
            time.sleep(1)
            status = self.query_status()
            if status == self.STATUS_PROTOCOL_NOT_LOADED:
                return 0