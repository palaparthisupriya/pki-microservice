# PKI-Based Auth Microservice

A secure, enterprise-grade microservice for TOTP (Time-based One-Time Password) generation and verification. This project implements RSA/OAEP decryption, persistent storage using Docker volumes, and automated background logging via Cron.

## 🚀 Features

* **Asymmetric Decryption**: Decrypts seeds using RSA-OAEP with SHA-256 and MGF1.
* **TOTP Engine**: Generates and verifies 6-digit codes based on RFC 6238.
* **Persistent Storage**: Utilizes named Docker Volumes to ensure the decrypted seed and logs persist across container restarts.
* **Automated Logging**: A background Cron job logs the current TOTP code every minute to a shared volume.
* **Enterprise Dockerization**: Multi-stage build for a slim, secure, and production-ready container.

## 📁 Project Structure

```text
├── app/
│   ├── main.py            # FastAPI Application & Endpoints
│   ├── crypto_utils.py    # RSA Decryption Utility
│   ├── totp_utils.py      # TOTP Generation & Verification
│   └── cron_job.py        # Logic for background tasks
├── cron/
│   └── 2fa-cron           # Cron schedule configuration (LF line endings)
├── scripts/
│   └── log_2fa_cron.py    # Script executed by Cron daemon
├── student_private.pem    # RSA Private Key (Student)
├── student_public.pem     # RSA Public Key (Student)
├── instructor_public.pem  # RSA Public Key (Instructor)
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Volume and Port orchestration
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

## Installation & Setup1. Build and Start the ContainerBashdocker-compose up --build -d
2. Decrypt the Seed (Initialization)Before generating codes, initialize the service with your encrypted seed:Bashcurl -X POST http://localhost:8080/decrypt-seed \
-H "Content-Type: application/json" \
-d "{\"encrypted_seed\": \"YOUR_BASE64_ENCRYPTED_SEED\"}"
##🔌 API EndpointsMethodEndpointDescriptionPOST/decrypt-seedDecrypts and saves the hex seed to /data/seed.txt.GET/generate-2faReturns a 6-digit TOTP code and its remaining validity.POST/verify-2faVerifies a 6-digit code against the stored seed.
## 📊 Monitoring & PersistenceCron Logs: The service automatically logs a code every minute. Verify this at:docker-compose exec app cat /cron/last_code.txtPersistence Test: Restarting the container with docker-compose restart will not lose the decrypted seed, as it is stored in the seed-data named volume.🔒 Security SpecificationsAsymmetric Algorithm: RSA-OAEPHashing: SHA-256Mask Generation Function: MGF1 (SHA-256)Timezone: UTC (Internal Container Clock)TOTP Interval: 30 Seconds
POST/verify-2faVerifies a 6-digit code against the stored seed.
## 📊 Monitoring & PersistenceCron Logs: The service automatically logs a code every minute. Verify this at:docker-compose exec app cat /cron/last_code.txtPersistence Test: Restarting the container with docker-compose restart will not lose the decrypted seed, as it is stored in the seed-data named volume.
##🔒 Security SpecificationsAsymmetric Algorithm:
 RSA-OAEPHashing: SHA-256Mask Generation Function: MGF1 (SHA-256)Timezone: UTC (Internal Container Clock)TOTP Interval: 30 Seconds
