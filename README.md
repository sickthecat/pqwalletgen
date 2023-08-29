# pqwalletgen

Make sure to install bip-utils and tk via pip. :)

```python
hashed_bytes = hash_obj.digest()
random_seed = hashed_bytes[:32]

# ... Cryptographic operations using the random seed ...
```

Here, `hashed_bytes` contains the digest of the hash object (SHA-3-384) computed from mouse coordinates. The first 32 bytes of this digest are extracted to create a `random_seed`. This random seed will be used for various cryptographic operations involving Cardano.

```python
cip1852_mst_ctx = Cip1852.FromSeed(random_seed, Cip1852Coins.CARDANO_ICARUS)
```

`Cip1852` is a class provided by the `bip_utils` library for working with BIP-1852, which is Cardano's hierarchical deterministic (HD) key derivation scheme. This line creates a master context (`cip1852_mst_ctx`) by deriving it from the `random_seed` using the BIP-1852 scheme. `CARDANO_ICARUS` specifies the specific coin type for the derivation.

```python
seed_phrase = Bip39MnemonicGenerator().FromEntropy(random_seed)
```

The script uses `Bip39MnemonicGenerator` from the `bip_utils` library to generate a mnemonic (seed phrase) from the `random_seed`. A mnemonic is a human-readable representation of the seed that can be used to recover the seed and its associated keys. The generated mnemonic is stored in the `seed_phrase` variable.

```python
cip1852_acc_ctx = cip1852_mst_ctx.Purpose().Coin().Account(0)
shelley_acc_ctx = CardanoShelley.FromCip1852Object(cip1852_acc_ctx)
```

Here, the script derives an account context (`cip1852_acc_ctx`) from the master context. This account context is then used to create a `shelley_acc_ctx` object using the `CardanoShelley` class. The `CardanoShelley` class provides methods for working with Cardano's Shelley era features.

```python
shelley_chg_ctx = shelley_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
```

An address change context (`shelley_chg_ctx`) is derived from the account context using the `Change` method with the change type `Bip44Changes.CHAIN_EXT`. This is used to generate external chain keys for addresses.

```python
for i in range(5):
    shelley_addr_ctx = shelley_chg_ctx.AddressIndex(i)
    
    # ... Printing keys and addresses for the derived index ...
```

A loop is used to derive and print the details for the first 5 addresses. The script derives an address context (`shelley_addr_ctx`) using the `AddressIndex` method from the change context. This address context provides methods for working with the keys and addresses associated with the specified index.

The cryptographic operations involve generating a random seed, deriving hierarchical deterministic keys, generating a mnemonic from the seed, and using these keys to generate addresses and associated keys. The script leverages the `bip_utils` library to work with the BIP-1852 key derivation scheme and Cardano's cryptographic operations. The derived keys and addresses can be used for various purposes within the Cardano ecosystem, such as securing wallets and performing transactions.
