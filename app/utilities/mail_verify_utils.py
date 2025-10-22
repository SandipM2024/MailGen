import re
import socket
import smtplib
import dns.resolver
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------------------
# Email Verification Utilities
# ------------------------------
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def is_syntax_valid(email: str) -> bool:
    """Check basic email syntax."""
    return bool(EMAIL_REGEX.match(email))


# Cache MX lookups to avoid repeated queries
mx_cache: Dict[str, List[str]] = {}

def mx_lookup(domain: str) -> List[str]:
    """Check if the domain has valid MX records and cache results."""
    if domain in mx_cache:
        return mx_cache[domain]
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_hosts = [r.exchange.to_text() for r in sorted(answers, key=lambda r: r.preference)]
        mx_cache[domain] = mx_hosts
        return mx_hosts
    except Exception:
        mx_cache[domain] = []
        return []

# SMTP_PORTS = [25, 587, 465]

# def smtp_check(email: str, from_address="sandip69690@gmail.com", timeout=5) -> bool:
#     """
#     Verify email existence via SMTP with TLS support and multiple ports.
#     """
#     try:
#         domain = email.split("@", 1)[1]
#         mx_hosts = mx_lookup(domain)
#         if not mx_hosts:
#             print(f"No MX record for {domain}")
#             return False

#         for mx in mx_hosts:
#             for port in SMTP_PORTS:
#                 try:
#                     print(f"Trying {mx}:{port}")
#                     with smtplib.SMTP(mx, port, timeout=timeout) as server:
#                         server.ehlo()
#                         try:
#                             server.starttls()
#                             server.ehlo()
#                         except smtplib.SMTPException:
#                             print(f"STARTTLS not supported on {mx}:{port}")

#                         server.mail(from_address)
#                         code, _ = server.rcpt(email)
#                         print(f"Response from {mx}:{port} -> {code}")

#                         if 200 <= code < 300:
#                             return True
#                         elif code == 550:
#                             return False
#                 except (socket.timeout, smtplib.SMTPConnectError) as e:
#                     print(f"Timeout or connect error {mx}:{port} -> {e}")
#                     continue
#                 except Exception as e:
#                     print(f"Error {mx}:{port} -> {e}")
#                     continue
#     except Exception as e:
#         print(f"General SMTP check error: {e}")
#         return False
#     return False


# ------------------------------
# Main Parallel Verification
# ------------------------------
def verify_email_task(email: str) -> str:
    """Task for verifying a single email."""
    email = email.strip()
    if not is_syntax_valid(email):
        return None

    domain = email.split('@')[1]
    if  mx_lookup(domain):
        return email

    # if smtp_check(email):
    #     return email
    return None


def verify_emails(emails: List[str], max_workers: int = 10) -> List[str]:
    """Verify a list of emails in parallel and return only valid ones."""
    valid_emails = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(verify_email_task, email): email for email in emails}
        for future in as_completed(futures):
            result = future.result()
            if result:
                valid_emails.append(result)
    return valid_emails

