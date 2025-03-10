from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def profile():
    my_info = {
        "name": "Madhuban Sahani",
        "email": "madhuban.sahani@gmail.com",
        "about":"I’m a Python developer with a strong foundation in AWS and SQL. I specialize in building efficient solutions, optimizing workflows, and tackling technical challenges. Always eager to learn and improve my skills in the ever-evolving tech world.",
        "education": ["Master's in Information Technology - Ramniranjan Jhunjhunwala College (2023 - Present)",
                "Bachelor's in Information Technology - Ramniranjan Jhunjhunwala College (2020 - 2023)",
                "HSC - Sheth N.K.T.T Junior College | 72.30%",
                "SSC - Shree Vibuti Prakashanand Ji Vidyalay | 87.40%"
        ],
        "skills": ["AWS", "Python", "SQL", "Django"],
        "projects": [
            "E-commerce Website",
            "Expense Tracker",
            "Automated Document Conversion System",
            "Automated Text-to-Speech System",
            "CI/CD Pipeline Automation with AWS"
        ],
        "internship": [
            {
                "title": "AWS re/START - Magic Bus India Foundation (May '24 - Aug '24)",
                "tasks": [
                    "Completed hands-on training in key AWS services.",
                    "Assisted in cloud infrastructure deployment (EC2, S3, RDS).",
                    "Configured LAMP stack & deployed WordPress on Ubuntu.",
                    "Deployed web applications using Nginx & Apache servers."
                ]
            }
        ],
        "certifications": [
            {
                "name": "AWS Certified Cloud Practitioner",
                "link": "https://cp.certmetrics.com/amazon/en/public/verify/credential/8840190ca628426ca111878ce56fca55"
            },
            {"name": "System Admin Course - LinkedIn"},
            {"name": "Implementing DevOps with AWS - Infosys Springboard"}
        ],
        "contact": {
            "email": "madhuban.sahani@gmail.com",
            "linkedin": "https://www.linkedin.com/in/madhuban-sahani-a2982624b",
            "phone": "+91 8928734900",
            "location": "Thane, Maharashtra"
        }
    }
    return render_template('index.html', my_info=my_info)


if __name__ == '__main__':
    app.run(debug=True)
