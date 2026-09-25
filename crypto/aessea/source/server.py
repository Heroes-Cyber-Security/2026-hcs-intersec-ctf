import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


KEY = os.urandom(16)
FLAG = os.environ.get("FLAG")


def main():
    while True:
        print("1. Make ticket\n2. Redeem ticket\n3. Exit")
        try:
            choice = input(">> ")
            if choice == "1":
                try:
                    name = bytes.fromhex(input("Name (hex): "))
                    if len(name) > 64:
                        raise ValueError
                except ValueError:
                    print("Invalid name")
                    continue
                ticket = pad(b"name=" + name + b";role=user", 16)
                print(f"Ticket: {AES.new(KEY, AES.MODE_ECB).encrypt(ticket).hex()}")
            elif choice == "2":
                try:
                    ticket = bytes.fromhex(input("Ticket (hex): "))
                    if not ticket or len(ticket) % 16 or len(ticket) > 128:
                        raise ValueError
                    data = unpad(AES.new(KEY, AES.MODE_ECB).decrypt(ticket), 16)
                except ValueError:
                    print("Invalid ticket")
                    continue
                role = data.rsplit(b";role=", 1)[-1]
                print(FLAG if data.startswith(b"name=") and role == b"admin" else "Access denied")
            elif choice == "3":
                return
            else:
                print("Invalid choice")
        except EOFError:
            return


if __name__ == "__main__":
    main()
