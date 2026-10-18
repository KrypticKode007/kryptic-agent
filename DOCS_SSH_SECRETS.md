# Technical Wiki: SSH Key Generation & GitHub Repository Secrets Provisioning

This guide outlines how to generate a secure, isolated SSH Deploy Key locally and configure it as an encrypted GitHub Action Repository Secret to facilitate automated, passwordless remote code synchronizations.

## Step 1: Generate the SSH Key Pair Locally

Execute the following commands within an isolated secure local shell terminal environment.

```bash
# 1. Navigate to your local secure user directory structure
mkdir -p ~/.ssh
cd ~/.ssh

# 2. Generate a high-entropy RSA 4096-bit key pair using open key signature layouts
ssh-keygen -t rsa -b 4096 -C "mark.brandonwilson@gmail.com" -f id_rsa_kryptic_deploy -N ""
```

This creates two distinct tracking configuration assets inside your directory:
*   `id_rsa_kryptic_deploy`: Your **Private Key**. Keep this absolute secret. **Never** upload this to an open file index.
*   `id_rsa_kryptic_deploy.pub`: Your **Public Key**. This can be safely published.

---

## Step 2: Provision the Public Key to Your GitHub Repository Secrets

1. Open your web browser interface and navigate directly to your target framework homepage:
   `https://github.com/KrypticKode007/kryptic-agent`
2. Click on the **Settings** menu asset across the top navigation bar.
3. In the left-hand column menu, look for the **Security** grouping sub-section and select **Deploy keys**.
4. Click the **Add deploy key** button block in the upper right.
5. Configure the target parameter metadata fields as follows:
   *   **Title:** `KRYPTIC_AUTOMATION_RUNNER_KEY`
   *   **Key:** Copy and paste the *entire* textual payload found inside your local public key file (`id_rsa_kryptic_deploy.pub`).
   *   **Allow write access:** Check this option box to ensure the automation pipelines can push tracking history data logs.
6. Click **Add key** to register the cryptographic layer block.

---

## Step 3: Register the Private Key into GitHub Actions Environment Scope

1. From the same repository **Settings** page dashboard context layout, look at the left sidebar menu list.
2. Select the **Secrets and variables** dropdown grouping layer, then click **Actions**.
3. Select the **Repository secrets** tab view asset and click the **New repository secret** action.
4. Input the precise variable parameter properties to match your pipeline configurations:
   *   **Name:** `KRYPTIC_AGENT_DEPLOY_KEY`
   *   **Secret:** Copy and paste the *exact* multiline plaintext block string found inside your local private key file (`id_rsa_kryptic_deploy`). Ensure zero spaces or characters are clipped.
5. Select **Add secret** to finalize environmental injection.
