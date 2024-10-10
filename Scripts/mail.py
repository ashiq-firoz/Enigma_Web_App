import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


def create_article_html(article, content_template):
    new_article = BeautifulSoup(str(content_template), "html.parser")

    # Set the title and make it a hyperlink
    title = new_article.find('h2')
    title_link = new_article.new_tag('a', href=article['article_url'])
    title_link.string = article['article_title'][:300]
    title.clear()
    title.append(title_link)

    # Set the subtitle/content in the p tag with class 'subtitle'
    subtitle = new_article.find('p', class_='subtitle')
    subtitle.string = article['content'][:200] + "..."

    # Remove the "Read more" link if it exists
    link = new_article.find('a')
    if link and link.string == "Read more":
        link.decompose()

    return str(new_article).strip()



def make_email(news, research):
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the template path using current directory
    template_path = os.path.join(current_dir, 'New_email.html')

    # Load the template HTML
    with open(template_path, 'r', encoding='utf-8') as template_file:
        soup = BeautifulSoup(template_file.read(), "html.parser")

    # Extract the header and footer
    header = soup.find('div', class_='newsletter-header')
    footer = soup.find('div', class_='newsletter-footer')

    # Extract content templates for Research and News sections
    research_section = soup.find('div', class_='newsletter-content')
    news_section = research_section.find_next('div', class_='newsletter-content')

    # Extract CSS styles
    css = str(soup.head.style)

    # Initialize the newsletter content
    research_content = ""
    news_content = ""

    # Populate research content
    for article in research:
        research_content += create_article_html(article, research_section)

    # Populate news content
    for article in news:
        news_content += create_article_html(article, news_section)

    # Format the final email content
    email_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css" />
            {css}
        </head>
        <body>
            <section class="section">
                <div class="column is-half center-align">
                    <!-- Header Section -->
                    <div class="newsletter-header" style="background-color: #7449D6; color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td align="left" style="padding: 0; margin: 0; vertical-align: middle;">
                                    <h1 style="font-size: 2rem; margin: 0;">The Weekly Epoch</h1>
                                    <p style="font-size: 1rem; margin: 0; margin-top: 5px;">by Enigma ♡</p>
                                </td>
                                <td align="right" style="padding: 0; margin: 0; text-align: right; vertical-align: middle;">
                                    <img
                                      src="https://i.postimg.cc/nzkZW3xv/mascots.png"
                                      alt="Header Image"
                                      style="max-width: 100px; height: auto; display: block; margin: 0 auto;"
                                    />
                                </td>
                            </tr>
                        </table>
                    </div>

                    <!-- Latest Research Section -->
                    <div class="newsletter-content center-align">
                        <h2>Latest Research</h2>
                        {research_content}
                    </div>

                    <!-- Latest News Section -->
                    <div class="newsletter-content center-align">
                        <h2>News</h2>
                        {news_content}
                    </div>

                    <!-- Banner Section -->
                    <div class="banner-section" style="text-align: center;">
                        <img
                          src="https://i.postimg.cc/nhg97QYV/Enigma-Email-Banner-V1.png"
                          alt="Enigma Banner"
                          class="banner-image"
                          style="display: block; margin: 0 auto; max-width: 100%;"
                        />
                    </div>

                    <!-- Footer -->
                    <div class="newsletter-footer center-align" style="padding: 0.5rem; text-align: center;">
                        <p>Stay connected with us!</p>
                        <a href="https://example.com/unsubscribe" style="color: #3273dc; font-weight: bold; text-decoration: none;">Unsubscribe</a> |
                        <a href="https://enigma.iiitkottayam.ac.in/contact" style="color: #3273dc; font-weight: bold; text-decoration: none;">Contact Us</a>
                    </div>
                </div>
            </section>
        </body>
    </html>
    """

    # Save the email content to an output file
    output_path = os.path.join(current_dir, 'output_email.html')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(email_content)

    return email_content



def send_email(email_content):
    sender_email = "spaceluvr03@gmail.com"
    # List of recipient emails
    receiver_emails = ["tanya22bcd10@iiitkottayam.ac.in"] # , "aditya22bcs54@iiitkottayam.ac.in"]
    password = "zxtspibybsomcmia"

    # Create the plain-text and HTML version of your message
    text = "Hi, I've found some articles that you might find interesting"
    html = email_content

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.ehlo()
        server.login(sender_email, password)

        # Send email to each recipient in the list
        for receiver_email in receiver_emails:
            # Create a new MIMEMultipart message for each recipient
            message = MIMEMultipart("alternative")
            message["Subject"] = "Your weekly dose of goodness"
            message["From"] = sender_email
            message["To"] = receiver_email

            # Attach plain-text and HTML versions of the message
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)

            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
    return True
