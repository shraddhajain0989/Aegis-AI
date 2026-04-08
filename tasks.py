import random

TASKS = {
    "easy": [
        {"message": "You won ₹10 lakh lottery! Click now!", "is_scam": True, "verification_info": "The sender's email address is weird-lottery-xyz123@gmail.com."},
        {"message": "Free gift card waiting! Claim now!", "is_scam": True, "verification_info": "The link goes to a suspicious domain: fre-giftz.info."},
    ],
    "medium": [
        {"message": "Your bank account needs verification. Enter details.", "is_scam": True, "verification_info": "Your actual bank app shows no such alerts. The link is HTTP only."},
        {"message": "Update your KYC immediately to avoid suspension.", "is_scam": True, "verification_info": "The message was sent from a personal 10-digit mobile number, not a bank shortcode."},
    ],
    "hard": [
        {"message": "Hi, I am from your company HR. Share OTP for salary verification.", "is_scam": True, "verification_info": "The sender refuses to send an email from the official company domain."},
        {"message": "Your order failed. Please confirm payment using this secure link.", "is_scam": True, "verification_info": "Your shopping app confirms the order is actually fine and fully paid."},
    ],
    "normal": [
        {"message": "Reminder: Meeting at 5 PM.", "is_scam": False, "verification_info": "You check your work calendar and indeed, there is a meeting at 5 PM."},
        {"message": "Your Amazon order has been shipped.", "is_scam": False, "verification_info": "You check your app and the tracking status perfectly matches this SMS."},
    ]
}

def get_task(task_name):
    if task_name not in TASKS:
        task_name = "easy"
    return random.choice(TASKS[task_name])