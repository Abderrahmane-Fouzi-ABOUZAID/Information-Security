# TP : Cryptography in Action: An OpenSSL Lab — Investigation Sheet

**Course:** Information Security (UM6P)  
**Instructor:** Imane Fouad  
**Evidence Intercepted:** `classified.enc`  
**Lab Directory:** `C:\Users\abder\S7 Folder\Information security\TP_OPENSSL`  

---

## Mission 1 — The RSA Password Challenge

### Briefing & Evidence
- **Prime 1 ($p$):** 5
- **Prime 2 ($q$):** 11
- **Public Exponent ($e$):** 3
- **Intercepted Ciphertext ($C$):** 23

---

### Challenge 1.1 — Reconstruct the RSA System

#### 1. Determine Public and Private Keys
- **RSA Modulus ($n$):**
  $$n = p \times q = 5 \times 11 = 55$$
- **Euler's Totient ($\phi(n)$):**
  $$\phi(n) = (p - 1)(q - 1) = (5 - 1)(11 - 1) = 4 \times 10 = 40$$
- **Private Exponent ($d$):**
  $$e \cdot d \equiv 1 \pmod{\phi(n)} \implies 3d \equiv 1 \pmod{40}$$
  Testing values:
  - $3 \times 13 = 39 \equiv -1 \pmod{40}$
  - $3 \times 27 = 81 = (2 \times 40) + 1 \equiv 1 \pmod{40}$
  - Therefore, **$d = 27$**
- **RSA Public Key:** $(n = 55, e = 3)$
- **RSA Private Key:** $(n = 55, d = 27)$

#### 2. Decrypt Ciphertext $C = 23$
Using RSA decryption formula $m = C^d \pmod n$:
$$m = 23^{27} \pmod{55}$$
- Modular arithmetic breakdown:
  - $23^1 \equiv 23 \pmod{55}$
  - $23^2 = 529 = 9 \times 55 + 34 \equiv -21 \pmod{55}$
  - $23^4 \equiv (-21)^2 = 441 = 8 \times 55 + 1 \equiv 1 \pmod{55}$
  - Since $23^4 \equiv 1 \pmod{55}$, $23^{24} = (23^4)^6 \equiv 1^6 \equiv 1 \pmod{55}$
  - $23^{27} = 23^{24} \times 23^3 \equiv 1 \times (23^2 \times 23) \equiv (-21) \times 23 = -483 \pmod{55}$
  - $-483 + 9 \times 55 = -483 + 495 = 12$
- **Original Message (Password):** **`12`**

#### 3. Verification
$$m^e \pmod n = 12^3 \pmod{55} = 1728 \pmod{55}$$
$$1728 = 31 \times 55 + 23 = 1705 + 23 = 1728 \implies 1728 \equiv 23 \pmod{55}$$
- **Observation:** Re-encrypting $m = 12$ with the public key $(55, 3)$ yields $C = 23$, which matches the intercepted ciphertext.

---

## Mission 2 — Break the Image, Not AES!

### Challenge 1 — Investigate the Evidence

Inspection of the first 64 bytes of `classified.enc` using `xxd -l 64 classified.enc`:
```text
00000000: 53 61 6c 74 65 64 5f 5f 57 5a b8 cf 60 19 ac 39   Salted__WZ..`..9
00000010: 77 75 1c 07 8d df 54 b3 8a 26 b7 f6 f4 a9 ce f0   wu....T..&......
00000020: 77 75 1c 07 8d df 54 b3 8a 26 b7 f6 f4 a9 ce f0   wu....T..&......
00000030: 77 75 1c 07 8d df 54 b3 8a 26 b7 f6 f4 a9 ce f0   wu....T..&......
```

#### Question 1 Findings:
1. **OpenSSL Signature:** The first 8 bytes correspond to the ASCII string `Salted__` (`53 61 6c 74 65 64 5f 5f`).
2. **Salt:** The next 8 bytes (`57 5a b8 cf 60 19 ac 39`) represent the random salt used during key derivation.
3. **Bytes Excluded:** Exactly **16 bytes** ($8\text{ bytes header} + 8\text{ bytes salt}$) must be stripped before analyzing the raw ciphertext payload.

---

### Challenge 2 — The Encrypted Image Mystery (ECB Mode)

- **Input Specifications:** $432 \times 475$ grayscale pixels = $205,200\text{ bytes}$ ($12,825\text{ AES blocks}$ of 16 bytes each).
- **Program:** `patternECB.py` (reads ciphertext skipping 16-byte header, maps identical 16-byte blocks to identical grayscale values, and outputs `pattern_ecb.png`).
- **Statistical Findings:**
  - Total 16-byte blocks: $12,825$
  - Unique ciphertext blocks: only **$739$**
  - Repetitions of most common block (uniform background): **$8,023$ times**
- **Visual Recognition:** The outline, body, head, flippers, and feet of the Linux penguin (Tux) are clearly identifiable. Identical plaintext blocks produce identical ciphertext blocks under the same key ($C_i = E_K(P_i)$).

---

### Challenge 3 — Unlock the Original

Decryption command using password `12`:
```bash
openssl enc -d -aes-256-ecb -pbkdf2 -p -pass pass:12 -in classified.enc -out recovered.raw
```
- Derived Key: `103518D2C327E91924A746FA172211D62AC098CD2BA94E2270CC1D3612D6F877`
- Salt: `575AB8CF6019AC39`
- Reconstructed PNG: `recovered.png` ($432 \times 475$ grayscale image).

#### Checkpoint Finding:
- **What was hidden that ECB could not fully reveal?**  
  While ECB revealed the high-level outline of the penguin, it could not reveal:
  1. The secret text banner in the upper-right corner: **`YOU WIN`**.
  2. Fine internal facial details: sparkling eyes, reflections, detailed beak contour, and delicate shading gradients.

---

### Challenge 4 — Repair with CBC

Encryption command using AES-256-CBC:
```bash
openssl enc -aes-256-cbc -pbkdf2 -p -pass pass:12 -in recovered.raw -out classified_cbc.enc
```

Modified analysis program applied to CBC ciphertext (`pattern_cbc.png`):
- Total 16-byte blocks: $12,825$
- Unique ciphertext blocks: **$12,825$** ($100\%$ unique)
- Most frequent block count: **$1$** (Zero block repetition)

#### Comparison & Cryptographic Explanation:
- **ECB ($C_i = E_K(P_i)$):** Encrypts each block in isolation. Patterns and repetition in the plaintext directly leak into the ciphertext.
- **CBC ($C_i = E_K(P_i \oplus C_{i-1})$):** Each plaintext block is XORed with the previous ciphertext block (or the Initialization Vector $IV$ for the first block). Because $C_{i-1}$ is pseudorandom, even identical plaintext blocks produce radically distinct ciphertext blocks, providing semantic security and producing an image indistinguishable from pure white noise.

---

## Mission 3 — RSA: Keys, and Encryption

### Part A — Key Generation & Factorization

#### 5.1 & 5.2 Small 512-bit RSA Key
```bash
openssl genrsa -out mySmall.pem 512
openssl rsa -in mySmall.pem -text -noout
```
- Modulus length: 512 bits (2 primes)
- Public exponent: 65537 (`0x10001`)

#### 5.3 Security of `mySmall.pem`
- **Is the private key encrypted?**  
  No. The file begins with `-----BEGIN PRIVATE KEY-----` and stores the raw DER/ASN.1 structures in Base64 without any encryption passphrase.
- **Is it safely stored?**  
  No. Any user or process with read permissions can extract the modulus, exponents, and prime factors directly.

#### 3.4 Breaking the 50-bit RSA Key (`otherSmall_pub.pem`)
Intercepted Public Key:
```text
-----BEGIN PUBLIC KEY-----
MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHAtcS9BRJHQIDAQAB
-----END PUBLIC KEY-----
```
- **Extracted Modulus ($n$):** `799426357774621` (Hex: `0x02d712f414491d`, 50 bits)
- **Public Exponent ($e$):** `65537`
- **Factorization (Divisors up to $\sqrt{n} \approx 28,274,128$):**
  - **$p = 26,489,357$**
  - **$q = 30,179,153$**
  - Check: $p \times q = 26489357 \times 30179153 = 799,426,357,774,621 = n$
- **Euler's Totient:**
  $$\phi(n) = (p - 1)(q - 1) = 26489356 \times 30179152 = 799,426,301,106,112$$
- **Private Exponent ($d$):**
  $$d = e^{-1} \pmod{\phi(n)} = 65537^{-1} \pmod{799426301106112} = \mathbf{562,161,229,729,409}$$

#### 5.4 Factorization of the 512-bit Modulus
- **Can we recover the prime factors in reasonable time with the same approach?**  
  **No.** A 512-bit integer is approximately $1.34 \times 10^{154}$, with $\sqrt{n} \approx 1.16 \times 10^{77}$. Naive trial division would take billions of billions of years. While 512-bit RSA has been factored historically by specialized academic clusters using the General Number Field Sieve (GNFS), it cannot be broken in reasonable time on standard hardware or by simple trial division.

#### 5.6–5.8 2048-bit RSA Keys & Protection
1. Unencrypted key:
   ```bash
   openssl genrsa -out private1.pem 2048
   ```
2. Encrypted key with AES-256-CBC:
   ```bash
   openssl genrsa -aes256 -out private2.pem 2048
   ```
3. Extracting public keys:
   ```bash
   openssl rsa -in private1.pem -pubout -out public1.pem
   openssl rsa -in private2.pem -pubout -out public2.pem
   ```

#### 5.9 Should a public key be stored in plaintext?
**Yes.** By cryptographic design, public keys require confidentiality: zero. They are intended to be freely distributed to any communicating party. Only their **integrity and authenticity** must be assured (typically via Public Key Infrastructure / X.509 digital certificates).

---

### Part B — Encryption, Decryption, and Hybrid Cryptography

#### 5.11 Short Message Encryption and Decryption
```bash
openssl pkeyutl -encrypt -pubin -inkey public1.pem -in short_message.txt -out message.enc
openssl pkeyutl -decrypt -inkey private1.pem -in message.enc -out message_dec.txt
```
- Original text: `"Secret password is UM6P-CyberSecurity-2026!"`
- Recovered text: `"Secret password is UM6P-CyberSecurity-2026!"` (Verified exact match).

#### 5.12 Encrypting Large Files with RSA
When attempting to encrypt a 1024-byte file using `openssl pkeyutl`:
```text
Public Key operation error
2CC10000:error:0200006E:rsa routines:ossl_rsa_padding_add_PKCS1_type_2_ex:data too large for key size
```
- **Why RSA is unsuitable for direct bulk encryption:**
  1. **Payload Size Limit:** RSA operates on numbers modulo $n$. Plaintext size must be strictly smaller than the key size minus padding overhead. For a 2048-bit key (256 bytes) with PKCS#1 v1.5 padding (11 bytes overhead), the maximum encryptable payload is only **245 bytes**.
  2. **Computational Overhead:** Asymmetric modular exponentiation is orders of magnitude slower and more CPU-intensive than symmetric algorithms like AES.

#### 5.14 & 5.15 Hybrid Encryption Implementation
Hybrid encryption combines symmetric and asymmetric cryptography:
1. **Generate ephemeral AES key & IV:**
   ```bash
   openssl rand -out aes_session.key 32
   openssl rand -hex 16 > iv.hex
   ```
2. **Bulk Encrypt with AES-256-CBC:**
   ```bash
   openssl enc -aes-256-cbc -in large_file.txt -out large_file_cbc.enc -pass file:aes_session.key -iv <IV_HEX>
   ```
3. **Key Encapsulation with RSA:**
   ```bash
   openssl pkeyutl -encrypt -pubin -inkey partner_public.pem -in aes_session.key -out aes_session.key.enc
   ```
4. **Decapsulation & Bulk Decryption:**
   - Partner recovers AES key:
     ```bash
     openssl pkeyutl -decrypt -inkey partner_private.pem -in aes_session.key.enc -out recovered_aes.key
     ```
   - Partner decrypts message:
     ```bash
     openssl enc -d -aes-256-cbc -in large_file_cbc.enc -out recovered_large.txt -pass file:recovered_aes.key -iv <IV_HEX>
     ```
- **Why this combination is optimal:**
  - **AES (Symmetric):** Delivers blazing fast, hardware-accelerated bulk data encryption without payload size restrictions.
  - **RSA (Asymmetric):** Solves the key-distribution problem by securely transmitting the small, fixed-size 256-bit symmetric key without requiring a pre-shared secret.
