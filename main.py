#!/usr/bin/env python3
import datetime
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

GEMINI_API_KEY = "gemini-api-key"  # Replace with your key
GMAIL_USER = "myemail@gmail.com"  # Replace with your Gmail
GMAIL_APP_PASSWORD = "XX"  # Replace with app password
RECIPIENT_EMAIL = "xx"  # Where to send the horoscope
ZODIAC_SIGN = "Sagittarius"  # Your zodiac sign

def get_horoscope(sign, api_key, date_str=None):
    """Get horoscope using Gemini API"""
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%B %d")
    
    date_year = datetime.datetime.now().strftime("%Y") 
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Create a GenerativeModel object
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Create prompt
    prompt = f"You are a helpful assistant that provides daily horoscopes. Give me a horoscope for {sign} for {date_str} year {date_year}. Don't reply with any confirmation like 'Okay, here is your horoscope' or mention the year just answer. Break into sections: General Outlook, Career & Finances, Love & Relationships, Health & Well-being, Chinese Horoscope, Lucky Numbers, Lucky Colors, Affirmation for the day."
    
    # Generate content
    response = model.generate_content(prompt)
    
    # Extract and return the horoscope text
    return response.text

def format_html_email(sign, date_str, horoscope_text):
    """Format the horoscope as an email-client friendly HTML email with platform-adaptive design."""
    
    # Get zodiac sign emoji and color scheme based on sign
    zodiac_data = {
        "Aries": {"emoji": "♈", "color": "#FF5C5C"},
        "Taurus": {"emoji": "♉", "color": "#7CB07C"}, 
        "Gemini": {"emoji": "♊", "color": "#FFD166"},
        "Cancer": {"emoji": "♋", "color": "#6CCCF0"},
        "Leo": {"emoji": "♌", "color": "#FF9966"},
        "Virgo": {"emoji": "♍", "color": "#9FC2CC"},
        "Libra": {"emoji": "♎", "color": "#C6A4DB"},
        "Scorpio": {"emoji": "♏", "color": "#9D5C63"},
        "Sagittarius": {"emoji": "♐", "color": "#7B68EE"},
        "Capricorn": {"emoji": "♑", "color": "#5E7F5E"},
        "Aquarius": {"emoji": "♒", "color": "#5BA4CF"},
        "Pisces": {"emoji": "♓", "color": "#8F78B8"}
    }
    
    # Default in case the sign is not in our dictionary
    sign_data = zodiac_data.get(sign, {"emoji": "✨", "color": "#7B68EE"})
    
    # Clean the horoscope content and format sections
    formatted_content = clean_and_format_horoscope(horoscope_text, sign_data["color"])
    
    # Use a colored background with contrasting text for better visibility across email clients
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Horoscope for {sign}</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; font-size: 16px; line-height: 1.6; color: #333333;">
    <center>
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="100%" style="max-width: 600px;">
            <!-- Header with colored background -->
            <tr>
                <td style="text-align: center; padding: 20px; background-color: {sign_data["color"]};">
                    <div style="font-size: 36px; margin-bottom: 10px;">{sign_data["emoji"]}</div>
                    <div style="font-size: 28px; font-weight: bold; color: #FFFFFF; margin-bottom: 5px;">Daily Horoscope for {sign}</div>
                    <div style="font-size: 18px; color: #FFFFFF;">{date_str}</div>
                </td>
            </tr>
            
            <!-- Content -->
            <tr>
                <td style="padding: 20px;">
                    {formatted_content}
                </td>
            </tr>
        </table>
    </center>
</body>
</html>"""
    return html_content

def clean_and_format_horoscope(text, theme_color):
    """Clean and format the horoscope text using a design that works on any background."""
    # Remove any extra asterisks or formatting marks
    text = re.sub(r'\*+', '', text)
    
    # Initialize variables to hold each section's content
    sections = {
        "General Outlook": "",
        "Career & Finances": "",
        "Love & Relationships": "",
        "Health & Well-being": "",
        "Chinese Horoscope": "",
        "Lucky Numbers": "",
        "Lucky Colors": "",
        "Affirmation for the day": ""
    }
    
    # Define section emojis
    section_emojis = {
        "General Outlook": "🔎",
        "Career & Finances": "💰",
        "Love & Relationships": "💘",
        "Health & Well-being": "🩺",
        "Chinese Horoscope": "🥠",
        "Lucky Numbers": "🔢",
        "Lucky Colors": "🎨",
        "Affirmation for the day": "✨"
    }
    
    # Define the pattern to match section headers
    pattern = r"(General Outlook|Career & Finances|Love & Relationships|Health & Well-being|Chinese Horoscope|Lucky Numbers|Lucky Colors|Affirmation for the day)[:\s]*"

    # Split the text into sections
    parts = re.split(pattern, text)
    
    # Remove any empty strings
    parts = [part.strip() for part in parts if part.strip()]
    
    # Extract the content for each section
    current_section = None
    for part in parts:
        if part in sections:
            current_section = part
        elif current_section:
            sections[current_section] = part.strip()
    
    # Build the HTML with a design that works on any background
    html = ""
    
    # Add the regular sections with colored borders instead of backgrounds
    for section in ["General Outlook", "Career & Finances", "Love & Relationships", "Health & Well-being", "Chinese Horoscope"]:
        if sections[section]:
            html += f"""
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 20px;">
                <tr>
                    <td style="border-left: 4px solid {theme_color}; padding-left: 15px;">
                        <div style="color: #000000; font-size: 18px; font-weight: bold; margin-bottom: 8px;">
                            {section_emojis[section]} {section}
                        </div>
                        <div style="color: #333333;">
                            {sections[section]}
                        </div>
                    </td>
                </tr>
            </table>
            """
    
    # Add the lucky numbers and colors with borders
    if sections["Lucky Numbers"] or sections["Lucky Colors"]:
        html += '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 20px;"><tr>'
        
        if sections["Lucky Numbers"]:
            html += f"""
            <td width="50%" style="padding-right: 5px; vertical-align: top;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="border: 2px solid {theme_color}; padding: 15px; text-align: center;">
                            <div style="font-size: 16px; color: #000000; margin-bottom: 5px;">{section_emojis["Lucky Numbers"]} Lucky Numbers</div>
                            <div style="font-size: 18px; color: {theme_color}; font-weight: bold;">{sections["Lucky Numbers"]}</div>
                        </td>
                    </tr>
                </table>
            </td>
            """
        
        if sections["Lucky Colors"]:
            html += f"""
            <td width="50%" style="padding-left: 5px; vertical-align: top;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="border: 2px solid {theme_color}; padding: 15px; text-align: center;">
                            <div style="font-size: 16px; color: #000000; margin-bottom: 5px;">{section_emojis["Lucky Colors"]} Lucky Colors</div>
                            <div style="font-size: 18px; color: {theme_color}; font-weight: bold;">{sections["Lucky Colors"]}</div>
                        </td>
                    </tr>
                </table>
            </td>
            """
        
        html += '</tr></table>'
    
    # Add the affirmation with border
    if sections["Affirmation for the day"]:
        html += f"""
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-top: 20px;">
            <tr>
                <td style="text-align: center;">
                    <div style="color: #000000; font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                        {section_emojis["Affirmation for the day"]} Affirmation for the day {section_emojis["Affirmation for the day"]}
                    </div>
                    <div style="border: 2px solid {theme_color}; padding: 15px; font-style: italic; color: {theme_color};">
                        {sections["Affirmation for the day"]}
                    </div>
                </td>
            </tr>
        </table>
        """
    
    return html

def send_email_via_smtp(user, password, recipient, subject, body_html):
    """Send email using Gmail SMTP with App Password."""
    msg = MIMEMultipart('alternative')
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Create a plain text version (simplified from HTML)
    plain_text = re.sub('<.*?>', '', body_html)
    plain_text = plain_text.replace('&nbsp;', ' ')
    plain_text = re.sub(r'\s+', ' ', plain_text)
    
    # Attach both plain text and HTML versions
    part1 = MIMEText(plain_text, 'plain')
    part2 = MIMEText(body_html, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    
def main():
    """Main function to run the script."""
    # Get today's date for the subject and email
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    formatted_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    try:
        # Get horoscope
        horoscope = get_horoscope(ZODIAC_SIGN, GEMINI_API_KEY)
        print("Successfully retrieved horoscope")
        
        # Format as HTML email
        html_email = format_html_email(ZODIAC_SIGN, formatted_date, horoscope)
        
        # Format email subject
        subject = f"Daily {ZODIAC_SIGN} Horoscope for {today_date}"
        
        # Send email
        success = send_email_via_smtp(
            GMAIL_USER, 
            GMAIL_APP_PASSWORD, 
            RECIPIENT_EMAIL, 
            subject, 
            html_email
        )
        
        if success:
            print(f"Successfully sent horoscope to {RECIPIENT_EMAIL}")
        else:
            print("Failed to send email")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
