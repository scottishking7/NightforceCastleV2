import subprocess

VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
RADIO_URL = "https://radio.midnightradio.cloud/listen/midnight-radio/radio.mp3"

radio_process = None


def play_radio():

    global radio_process

    if radio_process is not None and radio_process.poll() is None:

        print()
        print("Midnight Radio is already playing.")
        print()
        return

    print()
    print("=" * 70)
    print("📻 MIDNIGHT RADIO")
    print("=" * 70)
    print()

    print("Starting Midnight Radio...")
    print()

    radio_process = subprocess.Popen(
        [
            VLC_PATH,
            "--no-video",
            RADIO_URL
        ]
    )

    print("Midnight Radio is playing.")
    print()


def stop_radio():

    global radio_process

    if radio_process is None or radio_process.poll() is not None:

        print()
        print("Midnight Radio is not currently playing.")
        print()
        return

    radio_process.terminate()
    radio_process = None

    print()
    print("Midnight Radio stopped.")
    print()


def midnight_radio():

    while True:

        print()
        print("=" * 70)
        print("📻 MIDNIGHT RADIO")
        print("=" * 70)
        print()

        print("1 - Play Midnight Radio")
        print("2 - Stop Radio")
        print("3 - Return")
        print()

        choice = input("Choose: ")

        if choice == "1":

            play_radio()

        elif choice == "2":

            stop_radio()

        elif choice == "3":

            stop_radio()
            return

        else:

            print()
            print("Invalid choice.")
