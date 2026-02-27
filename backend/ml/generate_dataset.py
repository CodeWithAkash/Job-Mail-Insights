import random
import csv

selection_templates = [
    "Congratulations! We are pleased to move forward with your application for the {position} role.",
    "You have been shortlisted for the next round of interviews.",
    "We are excited to inform you that you have been selected.",
    "Your profile has been approved for the final interview.",
    "We are delighted to offer you the position of {position}.",
    "You have successfully cleared the technical round.",
    "Our team was impressed and would like to proceed further.",
    "You have been selected for the upcoming interview stage.",
]

rejection_templates = [
    "We regret to inform you that we will not be moving forward.",
    "Unfortunately, we have chosen another candidate.",
    "Your application was not selected this time.",
    "We appreciate your interest but cannot proceed further.",
    "The position has been filled by another applicant.",
    "After careful review, we are unable to continue.",
    "We will not be progressing your application.",
    "Thank you for applying, but we are moving ahead with others.",
]

pending_templates = [
    "Your application is currently under review.",
    "We are still evaluating your profile.",
    "Our team will get back to you soon.",
    "The hiring process is ongoing.",
    "We have received your application.",
    "Your profile is being considered.",
    "We are reviewing all applications carefully.",
    "The position is still open and under evaluation.",
]

positions = [
    "Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Python Developer",
    "Full Stack Developer",
]

def generate_samples(templates, label, count):
    data = []
    for _ in range(count):
        template = random.choice(templates)
        position = random.choice(positions)
        text = template.format(position=position)
        data.append([text, label])
    return data


data = []
data += generate_samples(selection_templates, "Selection", 100)
data += generate_samples(rejection_templates, "Rejection", 100)
data += generate_samples(pending_templates, "Pending", 100)

random.shuffle(data)

with open("ml/training_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(data)

print("✅ 300 realistic training samples generated successfully!")