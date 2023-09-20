# qrdano wallet generator by _SiCk (@encrypted_past)
# QR function inspired by Jean Lupin (@xrp_goku)


import tkinter as tk
import hashlib
import webbrowser
from bip_utils import Bip39MnemonicGenerator, Bip44Changes, CardanoShelley, Cip1852Coins, Cip1852
import tkinter.messagebox
import qrcode

# Initialize a hash object for SHA-384
hash_obj = hashlib.sha3_384()

# Function to update hash object with mouse coordinates
def mouse_motion(event):
    x, y = event.x, event.y
    hash_obj.update(f"{x},{y}".encode('utf-8'))
    
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='blue')
    
    current_hash = hash_obj.copy().digest()[:32].hex()
    hash_label.config(text=f"Current Hash: {current_hash}")

# Function to generate seed when button is clicked
def generate_seed():
    hashed_bytes = hash_obj.digest()
    random_seed = hashed_bytes[:32]
    root.destroy()
    
    print("Generated random seed:", random_seed.hex())
    
    cip1852_mst_ctx = Cip1852.FromSeed(random_seed, Cip1852Coins.CARDANO_ICARUS)
    
    print("\nGenerated Seed Phrase:")
    seed_phrase = Bip39MnemonicGenerator().FromEntropy(random_seed)
    print(seed_phrase)

    # Generate and save QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(seed_phrase)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('seed_phrase_qr.png')
    print("QR code has been saved as 'seed_phrase_qr.png' in the working directory.")

    # Print the master keys
    print("\nMaster Keys:")
    print("Private Key:", cip1852_mst_ctx.PrivateKey().Raw().ToHex())
    print("Public Key:", cip1852_mst_ctx.PublicKey().RawCompressed().ToHex())

    # Print the staking keys and addresses
    cip1852_acc_ctx = cip1852_mst_ctx.Purpose().Coin().Account(0)
    shelley_acc_ctx = CardanoShelley.FromCip1852Object(cip1852_acc_ctx)

    print("\nStaking Keys:")
    print("Private Key:", shelley_acc_ctx.StakingObject().PrivateKey().Raw().ToHex())
    print("Public Key:", shelley_acc_ctx.StakingObject().PublicKey().RawCompressed().ToHex())
    print("Staking Address:", shelley_acc_ctx.StakingObject().PublicKey().ToAddress())

    # Derive and print external chain keys and first 5 addresses
    shelley_chg_ctx = shelley_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    print("\nDerive and Print First 5 Keys and Addresses:")
    for i in range(5):
        shelley_addr_ctx = shelley_chg_ctx.AddressIndex(i)

        print("\nAddress", i)
        print("Private Key:", shelley_addr_ctx.PrivateKeys().AddressKey().Raw().ToHex())
        print("Public Key:", shelley_addr_ctx.PublicKeys().AddressKey().RawCompressed().ToHex())
        print("Address:", shelley_addr_ctx.PublicKeys().ToAddress())
        print("Staking Address:", shelley_addr_ctx.PublicKeys().ToStakingAddress())
        print("Reward Address:", shelley_addr_ctx.PublicKeys().ToRewardAddress())

# Function to show 'About' information
def show_about():
    tk.messagebox.showinfo("About", "Written by _SiCk for the Cardano Community @ afflicted.sh")

# Function to open the donation link
def donate():
    webbrowser.open("https://handle.me/hardforks")

# Create a Tkinter window
root = tk.Tk()
root.title("Random Seed Generator")

canvas = tk.Canvas(root, bg="white", height=400, width=400)
canvas.pack()
canvas.bind("<Motion>", mouse_motion)

hash_label = tk.Label(root, text="Current Hash: ")
hash_label.pack()

# Generate Seed Button
button_generate = tk.Button(root, text="Generate Seed", command=generate_seed)
button_generate.pack()

# About Button
button_about = tk.Button(root, text="About", command=show_about)
button_about.pack()

# Donate Button
button_donate = tk.Button(root, text="Donate", command=donate)
button_donate.pack()

root.mainloop()
