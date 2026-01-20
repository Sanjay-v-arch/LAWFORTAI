from fastapi import APIRouter

router = APIRouter(
    prefix="/api/universal",
    tags=["Universal Actions"]
)
@router.get("/emergency-helpline")
def emergency_helpline():
    return {

        "title": "National Cyber Emergency Helpline Directory",
        "description": "Verified government, law enforcement, banking and cyber safety escalation channels for fraud, identity theft, UPI scams, ransomware, harassment, and cybercrime recovery.",

        # 🚨 CRITICAL & NATIONAL HELPLINES
        "critical_hotlines": [
            {"name": "Cyber Crime Emergency Helpline", "number": "1930", "type": "Financial Fraud"},
            {"name": "Cyber Crime National Portal", "url": "https://cybercrime.gov.in"},
            {"name": "Police Emergency", "number": "112", "type": "Emergency Response"},
            {"name": "Women Cyber Safety Helpline", "number": "181", "type": "Harassment / Abuse"},
            {"name": "Child Exploitation & Online Abuse", "url": "https://pocso-cctns.gov.in"},
            {"name": "Senior Citizen Assistance", "number": "14567"},
            {"name": "National Helpline Against Harassment", "number": "155620"},
            {"name": "National Disaster & Emergency Support", "number": "108"},
            {"name": "National Cyber Security Coordination Center", "url": "https://nciipc.gov.in"},
            {"name": "CERT-IN Incident Reporting", "url": "https://cert-in.org.in"}
        ],

        # 💸 DIGITAL PAYMENT FRAUD SUPPORT
        "digital_payment_support": [
            {"service": "UPI NPCI Complaint Portal", "url": "https://upi.npci.org.in"},
            {"service": "RBI Digital Payment Grievance Portal", "url": "https://cms.rbi.org.in"},
            {"service": "PhonePe Fraud Support", "url": "https://support.phonepe.com"},
            {"service": "Google Pay Fraud Support", "url": "https://support.google.com/pay"},
            {"service": "Paytm Support", "url": "https://paytm.com/care"},
            {"service": "Amazon Pay Fraud Support", "url": "https://www.amazon.in/gp/help/customer"},
            {"service": "BHIM App Helpdesk", "url": "https://bhimupi.org.in"},
            {"service": "Razorpay Merchant Fraud Reporting", "url": "https://razorpay.com/support"},
            {"service": "Paypal Unauthorized Transaction Support", "url": "https://www.paypal.com/in/smarthelp"}
        ],

        # 🏦 BANK FRAUD HELPLINES
        "bank_fraud_hotlines": [
            {"bank": "SBI", "number": "1800112211"},
            {"bank": "HDFC", "number": "18002586161"},
            {"bank": "ICICI", "number": "18602677777"},
            {"bank": "Axis Bank", "number": "18604195555"},
            {"bank": "Kotak Bank", "number": "18602662666"},
            {"bank": "Yes Bank", "number": "18001200"},
            {"bank": "Bank of Baroda", "number": "18002584455"},
            {"bank": "Canara Bank", "number": "18001030018"},
            {"bank": "Punjab National Bank", "number": "18001802222"},
            {"bank": "Union Bank", "number": "18002082244"},
            {"bank": "Indian Bank", "number": "180042500000"},
            {"bank": "IDFC First Bank", "number": "18001088888"},
            {"bank": "Federal Bank", "number": "18004251199"}
        ],

        # 🛡️ STATE CYBER CELLS (EXPANDED)
        "state_cyber_cells": [
            {"state": "Tamil Nadu", "portal": "https://tncybercrime.gov.in"},
            {"state": "Karnataka", "portal": "https://cyberpolice.karnataka.gov.in"},
            {"state": "Kerala", "portal": "https://cyber.kerala.gov.in"},
            {"state": "Telangana", "portal": "https://cybercrime.tspolice.gov.in"},
            {"state": "Andhra Pradesh", "portal": "https://cybercrime.ap.gov.in"},
            {"state": "Delhi", "portal": "https://delhipolice.nic.in/cybercell"},
            {"state": "Maharashtra", "portal": "https://cybercell.maharashtra.gov.in"},
            {"state": "Gujarat", "portal": "https://gujaratcybercrime.org"},
            {"state": "Rajasthan", "portal": "https://cyber.rajasthan.gov.in"},
            {"state": "Uttar Pradesh", "portal": "https://uppolice.gov.in"},
            {"state": "Madhya Pradesh", "portal": "https://cybercrime.mp.gov.in"},
            {"state": "Odisha", "portal": "https://citizenportal.odishapolice.gov.in"},
            {"state": "West Bengal", "portal": "https://wbpolice.gov.in"}
        ],

        # 📡 CYBER CRIME ESCALATION PATH
        "escalation_levels": [
            "Step-1: Freeze transaction via bank support",
            "Step-2: Call 1930 within 24 hours",
            "Step-3: File Cyber Crime Complaint online",
            "Step-4: Submit supporting documents",
            "Step-5: Monitor case status & follow-up"
        ],

        # 🌍 INTERNATIONAL SUPPORT (BONUS)
        "international_cyber_reporting": [
            {"country": "USA", "portal": "https://www.ic3.gov"},
            {"country": "UK", "portal": "https://www.actionfraud.police.uk"},
            {"country": "Australia", "portal": "https://www.cyber.gov.au/report"},
            {"country": "Singapore", "portal": "https://www.scamalert.sg"},
            {"country": "EUROPOL Internet Fraud", "portal": "https://www.europol.europa.eu"}
        ],

        # 🧑‍⚖️ LEGAL & DIGITAL RIGHTS
        "legal_support_resources": [
            {"org": "National Human Rights Commission", "url": "https://nhrc.nic.in"},
            {"org": "Data Protection & Privacy Complaints", "url": "https://pdpc.gov.in"},
            {"org": "Online Consumer Court", "url": "https://consumerhelpline.gov.in"},
            {"org": "IT Act & Cyber Law Knowledge Base", "url": "https://meity.gov.in"}
        ]
    }

@router.get("/recovery-steps")
def recovery_steps():
    return {

        "title": "Cyber Incident Recovery & Response Playbook",
        "version": "v2.0 — Extended  Case Library",
        "purpose": "Step-by-step response workflow for cyber fraud, account compromise, financial scams, data loss & device attacks.",

        # 🟢 INCIDENT SCENARIOS — 30+ Playbooks
        "attack_scenarios": {

            # 1 — UPI / PAYMENT FRAUD
            "upi_payment_fraud": [
                "Freeze transaction using bank helpline",
                "Call 1930 within 24 hours",
                "Raise dispute in UPI app",
                "Collect UPI Reference ID & Merchant ID",
                "File complaint on cybercrime.gov.in"
            ],

            # 2 — ATM CARD SKIMMING
            "atm_card_skimming": [
                "Block debit/credit card immediately",
                "Disable international transactions",
                "Freeze linked savings account",
                "Check nearby ATM CCTV logs",
                "Lodge FIR for card cloning"
            ],

            # 3 — ONLINE SHOPPING FRAUD
            "ecommerce_fraud": [
                "Collect order ID & seller ID",
                "Take screenshots of chat & listing",
                "Initiate refund request",
                "Escalate through consumer court portal",
                "Report fake marketplace profile"
            ],

            # 4 — FAKE JOB SCAM
            "job_offer_scam": [
                "Stop all payments immediately",
                "Preserve bank transfer proof",
                "Report recruiter account",
                "Upload email headers as evidence",
                "Report under cyber fraud & cheating"
            ],

            # 5 — LOAN APP HARASSMENT
            "loan_app_blackmail": [
                "Uninstall malicious loan apps",
                "Disable contact & storage permissions",
                "Collect threat & extortion messages",
                "Report under IT Act Section 66E/67",
                "Apply for harassment FIR"
            ],

            # 6 — INSTAGRAM / FACEBOOK ACCOUNT HACKED
            "social_media_hacked": [
                "Reset password immediately",
                "Logout from all active devices",
                "Enable 2-factor authentication",
                "Appeal account recovery",
                "Report impersonation case"
            ],

            # 7 — WHATSAPP IMPERSONATION FRAUD
            "whatsapp_scam": [
                "Block scam number",
                "Save chat logs as PDF",
                "Warn contacts publicly",
                "Report identity misuse",
                "Submit number for fraud analysis"
            ],

            # 8 — EMAIL PASSWORD COMPROMISED
            "email_account_breach": [
                "Reset mailbox & recovery phone",
                "Check unknown forwarding rules",
                "Remove suspicious login sessions",
                "Enable security alerts",
                "Review connected apps & APIs"
            ],

            # 9 — GOOGLE DRIVE DATA DELETED
            "cloud_file_loss": [
                "Restore from Drive Version History",
                "Check Trash & permanently deleted time",
                "Export activity log",
                "Scan for malware interaction",
                "Enable restricted sharing mode"
            ],

            # 10 — RANSOMWARE ATTACK
            "ransomware_infection": [
                "Disconnect internet & LAN",
                "Do not format device",
                "Preserve encrypted samples",
                "Create system image backup",
                "Report to CERT-IN"
            ],

            # 11 — PHISHING LINK CLICKED
            "phishing_link_incident": [
                "Immediately change credentials",
                "Scan device for spyware",
                "Revoke OAuth logins",
                "Block suspicious extensions",
                "Reset banking passwords"
            ],

            # 12 — BANK ACCOUNT UNAUTHORIZED TRANSFER
            "bank_account_compromise": [
                "Freeze account via toll-free helpline",
                "Disable debit transactions",
                "Request account hold memo",
                "Raise RBI grievance ticket",
                "Submit FIR copy to bank"
            ],

            # 13 — PHONE REMOTE ACCESS ATTACK
            "remote_access_controlled": [
                "Turn on Airplane mode",
                "Remove remote control apps",
                "Reset device",
                "Re-login from secure network",
                "Re-enable 2FA"
            ],

            # 14 — ANDROID SPYWARE / STALKERWARE
            "spyware_malware": [
                "Check unknown Device Admin apps",
                "Scan for privilege escalation apps",
                "Backup essential files",
                "Factory reset device",
                "File digital stalking complaint"
            ],

            # 15 — SIM SWAP ATTACK
            "sim_swap_attack": [
                "Block SIM immediately",
                "Disable UPI & auto-debit services",
                "Update bank KYC",
                "Generate new SIM with FIR copy",
                "Review telecom fraud request logs"
            ],

            # 16 — NFT / CRYPTO WALLET DRAIN
            "crypto_wallet_theft": [
                "Revoke exposed wallet permissions",
                "Freeze exchange withdrawal pipes",
                "Export blockchain hash proofs",
                "Notify exchange fraud desk",
                "Escalate to cyber financial crimes wing"
            ],

            # 17 — ONLINE GAMING SCAM
            "gaming_fraud": [
                "Collect gamer tag & server ID",
                "Save payment transaction record",
                "Report platform fraud portal",
                "Block repeat attacker accounts",
                "Register cheating / deception report"
            ],

            # 18 — ONLINE ROMANCE / TRUST SCAM
            "romance_scam": [
                "Preserve chat & money transfer records",
                "Avoid further communication",
                "Flag account as predator",
                "Submit psychological blackmail evidence",
                "File cyber cheating case"
            ],

            # 19 — PERSON DOXED / DATA LEAK
            "identity_exposure": [
                "Request search takedown",
                "Enable privacy lock",
                "Preserve dox URLs",
                "File online harassment case",
                "Notify local cyber police cell"
            ],

            # 20 — ONLINE DEFAMATION / THREAT
            "cyber_bullying_threat": [
                "Archive abusive messages",
                "Collect profile + URL proof",
                "Block offender",
                "Lodge NC / FIR",
                "Submit digital forensic copy"
            ],

            # 21 — BUSINESS EMAIL COMPROMISE
            "invoice_fraud": [
                "Freeze corporate account",
                "Notify vendor teams",
                "Trace spoof email header",
                "Stop invoice disbursal",
                "File economic offence report"
            ],

            # 22 — RDP SERVER COMPROMISE
            "server_breach": [
                "Disable RDP access",
                "Rotate admin credentials",
                "Export security logs",
                "Run endpoint forensic scan",
                "Notify network security team"
            ],

            # 23 — COLLEGE STUDENT CYBER HARASSMENT
            "student_harassment": [
                "Report to IT admin",
                "Preserve harassment proof",
                "Request academic grievance action",
                "Contact cyber awareness cell",
                "File formal safety case"
            ],

            # 24 — FAKE INVESTMENT TRADING SCAM
            "investment_scam": [
                "Stop further transfers",
                "Collect website domain & IDs",
                "Submit wallet trace request",
                "File financial cyber crime report",
                "Raise RBI dispute escalation"
            ],

            # 25 — SOCIAL ENGINEERING PHONE CALL
            "vishing_call": [
                "Do not share OTP / PIN",
                "Save call recording / number",
                "Block caller",
                "Submit telecom fraud report",
                "Initiate account security audit"
            ],

            # 26 — ONLINE EXAM / RESULT MANIPULATION
            "academic_portal_abuse": [
                "Record unauthorized access logs",
                "Restore previous records",
                "Notify academic cyber cell",
                "Request forensic validation",
                "Escalate disciplinary investigation"
            ],

            # 27 — ONLINE BLACKMAIL & EXTORTION
            "blackmail_case": [
                "Do not make payment",
                "Store all threat messages",
                "Preserve account trace IDs",
                "Report under IPC 384 / IT 67",
                "Request emergency legal protection"
            ],

            # 28 — DIGITAL IDENTITY FORGERY
            "id_theft": [
                "Freeze SIM & bank accounts",
                "Document fraudulent KYC",
                "Issue identity theft legal notice",
                "File cyber forgery FIR",
                "Notify data protection authority"
            ],

            # 29 — WORKPLACE CYBER MISCONDUCT
            "corporate_policy_violation": [
                "Audit device access logs",
                "Restrict policy breach account",
                "Report via HR grievance cell",
                "Escalate compliance review",
                "Issue official misconduct report"
            ],

            # 30 — AI GENERATED DEEPFAKE MISUSE
            "deepfake_abuse": [
                "Collect manipulated content evidence",
                "Upload hash & metadata proof",
                "Notify hosting platform",
                "File identity & defamation complaint",
                "Request takedown order"
            ]
        },

        # 📂 EVIDENCE COLLECTION CHECKLIST
        "evidence_to_collect": [
            "Screenshots of chats & scam messages",
            "Bank transaction ID & UPI Reference",
            "UPI handle / wallet / merchant ID",
            "Call recordings & timestamps",
            "Email headers & phishing links",
            "Device logs or malware traces",
            "Suspect social media profile URLs",
            "Bank dispute proof receipt"
        ],

        # 🔐 ACCOUNT SECURITY ACTIONS
        "secure_your_accounts": [
            "Reset banking & email passwords",
            "Enable 2-factor authentication",
            "Remove unknown login devices",
            "Disable auto-saved payment cards",
            "Update recovery phone & email",
            "Review connected apps & permissions"
        ],

        # 🛠 FILE & DATA RECOVERY TOOLS
        "file_recovery_tools": [
            {"tool": "Windows File History", "type": "Local Data Restore"},
            {"tool": "Google Drive Version Restore", "type": "Cloud Recovery"},
            {"tool": "PhotoRec", "type": "Deleted File Recovery"},
            {"tool": "Recuva", "type": "Accidental Deletion"},
            {"tool": "Disk Drill", "type": "Partition Recovery"}
        ],

        # 🔗 IMPORTANT SECURITY LINKS
        "important_links": [
            {"title": "Cyber Crime FIR Portal", "url": "https://cybercrime.gov.in"},
            {"title": "CERT-IN Incident Reporting", "url": "https://cert-in.org.in"},
            {"title": "RBI Banking Fraud Portal", "url": "https://cms.rbi.org.in"},
            {"title": "Consumer Grievance Portal", "url": "https://consumerhelpline.gov.in"},
            {"title": "Google Account Security", "url": "https://myaccount.google.com/security"},
            {"title": "Microsoft Security Center", "url": "https://account.live.com"}
        ]
    }

@router.get("/cyber-awareness")
def cyber_awareness():
    return {

        "title": "Cyber Safety & Fraud Awareness Intelligence Center",
        "version": "v2.0 — Scam Awareness Dataset",

        # 🌍 Trending Cyber Scams — India Focused
        "trending_scams": [
            "UPI QR Code Refund Scam",
            "Fake Investment / Stock Trading Scam",
            "Crypto Romance Scam (USDT Mining)",
            "Fake Job / Internship Scam",
            "Loan App Extortion Scam",
            "E-commerce Marketplace Buyer Scam",
            "SIM Swap Banking Fraud",
            "ATM Card Skimming",
            "Fake KYC Update Message Scam",
            "Telegram Investment Community Fraud"
        ],

        # 🚩 Red Flag Behaviour Indicators
        "red_flags": [
            "Person insists on quick payment",
            "Unknown number claiming to be bank employee",
            "QR code sent instead of UPI request",
            "Profile with no real identity proof",
            "Requests for OTP, PIN or CVV",
            "Threatening / emotional blackmail language",
            "Fake government or RBI warning messages",
            "APK file download request on WhatsApp"
        ],

        # 🟢 Safe Banking & UPI Usage Practices
        "safe_banking_practices": [
            "Never approve unknown collect requests",
            "Avoid scanning QR codes from strangers",
            "Disable auto-debit for unknown apps",
            "Avoid public WiFi for banking transactions",
            "Do not store card details in shopping apps",
            "Use a dedicated payment mobile device",
            "Keep SIM lock enabled",
            "Enable UPI transaction alerts"
        ],

        # 🟦 Phishing & Fraud Detection Checklist
        "phishing_detection_guide": [
            "Check sender email domain",
            "Look for grammar & spelling errors",
            "Avoid clicking shortened URLs",
            "Verify website lock / HTTPS status",
            "Hover over link before clicking",
            "Beware of urgency keywords like — ‘limited time’, ‘account blocked’",
            "Do not download attachments from strangers"
        ],

        # 🟣 Online Shopping Scam Awareness
        "online_shopping_scam_patterns": [
            "Seller refuses COD",
            "Price too good to be true",
            "Asks for advance booking fee",
            "Asks to chat outside marketplace",
            "Fake courier tracking links",
            "Refund scams via QR code"
        ],

        # 🟥 Social Engineering Attack Types
        "social_engineering_tactics": [
            "Impersonation of authority figure",
            "Emotional manipulation",
            "Urgency pressure scam",
            "Fear-based scam messages",
            "Romance / trust-building scam",
            "Fake reward & lottery scam"
        ],

        # 🟢 Workplace Cyber Safety Cases
        "corporate_cyber_risks": [
            "Fake vendor email fraud",
            "CEO email spoof attack",
            "Invoice redirection fraud",
            "Corporate credential leak",
            "BYOD policy misuse"
        ],

        # 🟡 Student & Youth Cyber Risks
        "student_cyber_threats": [
            "Exam paper leak scam",
            "Fake internship letters",
            "Gaming fraud top-up scam",
            "Online harassment / doxxing",
            "Scholarship phishing scam"
        ],

        # 🧒 Child Internet Safety Awareness
        "child_safety_guidelines": [
            "Avoid sharing personal photos",
            "Do not chat with unknown gamers",
            "Report cyber bullying immediately",
            "Enable parental control filters",
            "Avoid installing apps outside Play Store"
        ],

        # 🟢 Digital Privacy Protection Tips
        "privacy_protection_steps": [
            "Disable auto media download in WhatsApp",
            "Restrict profile visibility",
            "Avoid linking bank to multiple apps",
            "Do not share Aadhaar images online",
            "Use strong password + 2FA"
        ],

        # 🟥 Common Fake Job Scam Signs
        "fake_job_offer_signals": [
            "No official HR domain email",
            "Asks payment before joining",
            "Offers very high salary",
            "Interview only on WhatsApp",
            "Fake joining letter"
        ],

        # 🟩 Cryptocurrency & NFT Scam Awareness
        "crypto_scam_patterns": [
            "Guaranteed profit return offers",
            "USDT mining fake apps",
            "Fake investment group channels",
            "Wallet seed phrase theft",
            "Pump & dump fraud communities"
        ],

        # 🟦 Banking & Debit Card Scam Awareness
        "banking_fraud_patterns": [
            "Unknown international transactions",
            "Multiple micro-debits",
            "Auto debit malware apps",
            "POS cloning transactions"
        ],

        # 🟧 Mobile & SIM Security Awareness
        "sim_and_mobile_security": [
            "Enable SIM card lock",
            "Disable call forwarding",
            "Check unknown SMS permissions",
            "Avoid eSIM transfer via unknown links"
        ],

        # 🟣 Online Relationship Fraud Warning Signs
        "romance_scam_indicators": [
            "Sudden emotional bonding",
            "Requests money for emergencies",
            "Claims to be NRI or military officer",
            "Avoids video call verification"
        ],

        # 🟥 Harassment & Blackmail Awareness
        "cyber_harassment_patterns": [
            "Threat to leak photos",
            "Demanding money to delete content",
            "Identity impersonation",
            "Group extortion harassment"
        ],

        # 🟢 Cyber Safety Best Practices Library (General)
        "safety_best_practices": [
            "Use different passwords for every app",
            "Avoid third-party APK downloads",
            "Verify unknown callers before responding",
            "Check Google account login alerts",
            "Keep device updated",
            "Back up important files"
        ],

        # 📚 Learning & Awareness Resources
        "learning_resources": [
            {"title": "CERT-IN Cyber Guidelines", "url": "https://cert-in.org.in"},
            {"title": "National Cyber Crime Portal", "url": "https://cybercrime.gov.in"},
            {"title": "Google Safety Center", "url": "https://safety.google"},
            {"title": "RBI Financial Fraud Awareness", "url": "https://cms.rbi.org.in"},
            {"title": "UNICEF Online Child Safety", "url": "https://www.unicef.org/child-online-protection"}
        ]
    }
# ---------- Cyber Awareness Intelligence ----------
@router.get("/cyber-awareness")
def cyber_awareness():
    return {
        "status": "success",
        "section": "cyber_awareness",
        "data": CYBER_AWARENESS_DATA
    }


# ---------- Cyber Incident Recovery ----------
@router.get("/recovery-steps")
def recovery_steps():
    return {
        "status": "success",
        "section": "recovery_steps",
        "data": RECOVERY_PLAYBOOK
    }


# ---------- National Emergency Helpline ----------
@router.get("/emergency-helpline")
def emergency_helpline():
    return {
        "status": "success",
        "section": "emergency_helpline",
        "data": EMERGENCY_DIRECTORY
    }