# Termius login password

- **Session ID:** `ses_e20859175ffel0ykBe6zIiX3qc`
- **Created:** 2026-11-15 20:51  |  **Last activity:** 2026-11-15 20:53
- **Model:** `opencode-go/muse-spark-1.3-contributor`  |  **Agent:** `build`
- **Tokens:** 21,853 in / 342 out / 1,494 reasoning
- **Messages:** 3

---

### User - 2026-11-15 20:51

In termius i m trying to connect the pc what would be the password beacause it dosent work with my pin

### Assistant - 2026-11-15 20:51 | opencode-go/muse-spark-1.3-contributor | build

Your PIN will never work in Termius. SSH does not accept Windows Hello PIN, only the account password.

1. You need OpenSSH running on the PC first, otherwise password is irrelevant. On the PC check: `Settings > System > Optional features > OpenSSH Server`, then in Services start `OpenSSH SSH Server`. Allow port 22 in firewall.

2. Determine what password Termius wants:
   * `whoami` in cmd gives you `PC-NAME\Username`. Use `Username` as Termius username.
   * If you sign into Windows with a Microsoft account: use your Microsoft account password, not PIN. Reset at account.microsoft.com if you don't know it.
   * If local account: use `Settings > Accounts > Sign-in options > Password`. If you only ever set a PIN, you may have no / forgotten password - you must `Add` / `Change` one there. Empty passwords are rejected by SSH.

3. In Termius: Host = PC's LAN IP (`ipconfig` -> IPv4, e.g. 192.168.1.x), Port 22, Username from step 2, Password from step 2.

If it still fails, you likely have wrong account type or `PasswordAuthentication no` in `C:\ProgramData\ssh\sshd_config`.

<details><summary>Reasoning</summary>

Analyzing Termius SSH connection issue and distinguishing Windows Hello PIN from password for authentication.

</details>

<details><summary>Reasoning</summary>

Outlining steps to enable OpenSSH on Windows and set a compatible password for SSH authentication.

</details>

<details><summary>Reasoning</summary>

Extending the setup with password requirements and security considerations for SSH on Windows.

</details>
