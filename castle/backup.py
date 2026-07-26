import os
import shutil
from datetime import datetime


def backup_vault():

    if not os.path.exists("backups"):
        os.mkdir("backups")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_name = f"backups/vault_backup_{timestamp}.txt"

    shutil.copy("vault.txt", backup_name)

    print()
    print("✅ Backup created successfully!")
    print()
    print(f"Saved as:")
    print(backup_name)

    input("\nPress Enter to continue...")