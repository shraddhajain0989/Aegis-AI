import random

TASKS = {
    "easy_1": {"message": "You won ₹10 lakh lottery! Click now!", "is_scam": True, "verification_info": "The sender's email address is weird-lottery-xyz123@gmail.com."},
    "easy_2": {"message": "Free gift card waiting! Claim now!", "is_scam": True, "verification_info": "The link goes to a suspicious domain: fre-giftz.info."},
    "easy_3": {"message": "Congratulations! You have been selected for a free trip. Click here.", "is_scam": True, "verification_info": "Domain is misspelled like trips-for-fRee.com."},
    "medium_1": {"message": "Your bank account needs verification. Enter details.", "is_scam": True, "verification_info": "Your actual bank app shows no such alerts. The link is HTTP only."},
    "medium_2": {"message": "Update your KYC immediately to avoid suspension.", "is_scam": True, "verification_info": "The message was sent from a personal 10-digit mobile number, not a bank shortcode."},
    "medium_3": {"message": "Dear customer, your electricity will be disconnected tonight at 9 PM. Call this number.", "is_scam": True, "verification_info": "Official electricity boards do not send disconnection notices via personal numbers."},
    "hard_1": {"message": "Hi, I am from your company HR. Share OTP for salary verification.", "is_scam": True, "verification_info": "The sender refuses to send an email from the official company domain."},
    "hard_2": {"message": "Your order failed. Please confirm payment using this secure link.", "is_scam": True, "verification_info": "Your shopping app confirms the order is actually fine and fully paid."},
    "hard_3": {"message": "This is police. A case is registered against you. Pay fine immediately via this link.", "is_scam": True, "verification_info": "Police never ask for fine payments via random links or phone calls."},
}

def get_task(task_name):
    if task_name not in TASKS:
        task_name = "easy_1"
    return TASKS[task_name]