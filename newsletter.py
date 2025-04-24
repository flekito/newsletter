import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from time import sleep
import os
import traceback
import cairosvg
import io
import subprocess
import tempfile

# Load recipient emails from CSV
try:
    df = pd.read_csv("newsletter_emails.csv")
    print(f"Successfully loaded {len(df)} email addresses from newsletter_emails.csv")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

# Mailgun SMTP Configuration
SMTP_SERVER = "smtp.mailgun.org"
SMTP_PORT = 587  # Use 465 for SSL
SMTP_USERNAME = "info@malda.xyz"
SMTP_PASSWORD = "bee9cc73e0c2ae15ef94a16bc2539f5d-e298dd8e-30795570"

# Sender Email
FROM_EMAIL = '"Malda" <info@malda.xyz>'
SUBJECT = "Malda Alpha - Newsletter #1"

# Email Body Templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malda Alpha</title>
    <style>
        body {
            font-family: Verdana, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            color: #0A3A28 !important;
        }
        * {
            color: #0A3A28 !important;
            box-sizing: border-box;
        }
        .container {
            max-width: 650px; /* Container for content */
            margin: auto;
            padding: 0 20px;
        }
        .full-width-container {
            width: 100%;
            max-width: 800px; /* Wider container for header */
            margin: auto;
            padding: 0;
            overflow: hidden; /* Prevent horizontal scroll */
        }
        a {
            color: #0A3A28 !important;
            text-decoration: underline;
        }
        
        /* Header and title */
        .header-title {
            font-family: Verdana, sans-serif;
            font-weight: 400;
            font-size: 32px;
            line-height: 100%;
            text-align: center;
            margin: 0;
            white-space: nowrap;
        }
        .divider {
            width: 320px; /* Wider waves */
            height: auto;
            display: block;
            margin: 0 10px; /* Add horizontal margin */
        }
        .green-line {
            width: 180px;
            height: 4px; /* Fixed height for the green line */
            display: block;
        }
        
        /* Section styles */
        .section {
            margin: 40px 0;
            padding-left: 20px; 
        }
        
        /* Heading styles - Less bold (reduced from 700 to 600) */
        h2 {
            font-family: Verdana, sans-serif;
            font-weight: 550;
            font-size: 28px;
            line-height: 100%;
            margin: 0 0 20px 0;
            color: #0A3A28 !important;
        }
        h3 {
            font-family: Verdana, sans-serif;
            font-weight: 550;
            font-size: 28px;
            line-height: 100%;
            margin: 0 0 20px 0;
            color: #0A3A28 !important;
        }
        .emoji {
            margin-right: 10px;
            font-size: 32px;
        }
        
        /* Content typography */
        p {
            font-family: Verdana, sans-serif;
            font-size: 16px;
            line-height: 150%;
            margin: 0 0 20px 0;
            max-width: 590px;
        }
        ul {
            padding-left: 20px;
            margin: 0;
            max-width: 590px;
        }
        li {
            font-family: Verdana, sans-serif;
            font-size: 16px;
            line-height: 150%;
            margin-bottom: 10px;
        }
        
        /* Tokenomics section */
        .tokenomics-table {
            width: 100%;
            margin-top: 20px;
        }
        .tokenomics-image-cell {
            width: 35%;
            padding-right: 20px;
            vertical-align: top;
            position: relative;
            top: -20px;
            left: -20px;
        }
        .tokenomics-bullet-cell {
            width: 65%;
            vertical-align: top;
        }
        .tokenomics-image {
            width: 140%; 
            max-width: none;
            height: auto;
            display: block;
        }
        
        /* Ecosystem header - Remove bold */
        .ecosystem-header {
            font-family: Verdana, sans-serif;
            font-weight: 400; /* Changed from 600 to 400 (normal weight) */
            font-size: 22px; 
            line-height: 100%;
            text-align: center;
            margin: 0;
            white-space: nowrap;
            color: #0A3A28 !important;
        }
        
        /* Social icons */
        .social-icon {
            width: 40px;
            height: 40px;
            display: block;
        }
        
        /* Footer styles (Minimal - Privacy Policy Only, Main Text Color) */
        .footer {
            text-align: center;
            margin-top: 40px; /* Add some space above the footer */
            padding-top: 20px;
            border-top: 1px solid #cccccc; /* Add a top border */
            font-size: 9px; /* Adjusted font size */
            color: #0A3A28 !important; /* Main text color */
        }
        .footer p {
            font-size: 9px; /* Adjusted font size */
            color: #0A3A28 !important; /* Main text color */
            line-height: 1.4;
            margin: 5px 0;
        }
        .footer a {
            color: #0A3A28 !important; /* Main text color */
            text-decoration: underline;
            font-size: 9px; /* Ensure link also uses adjusted size */
        }
        
        /* Media queries */
        @media only screen and (max-width: 480px) {
            /* Hide desktop header completely */
            .desktop-header {
                display: none !important;
            }
            
            /* Show mobile header */
            .mobile-header {
                display: block !important;
                width: 100% !important;
            }
            
            /* Ensure the mobile header table is properly sized */
            .mobile-header table {
                width: 100% !important;
                table-layout: fixed !important;
            }
            
            /* Ensure the waves are sized appropriately */
            .mobile-header img {
                width: 200px !important;
                height: auto !important;
            }
            
            /* Tokenomics image fix */
            table[style*="margin-top: 20px"] td:first-child {
                width: 100% !important;
                display: block !important;
                text-align: center !important;
                position: static !important;
                top: 0 !important;
                left: 0 !important;
                margin-bottom: 20px !important;
            }
            
            table[style*="margin-top: 20px"] td:first-child img {
                width: 120px !important;
                max-width: 120px !important;
                margin: 0 auto !important;
                display: block !important;
            }
            
            /* Adjust cell widths to give more space to the waves */
            .mobile-header table td:first-child,
            .mobile-header table td:last-child {
                width: 40% !important;
            }
            
            .mobile-header table td:nth-child(2) {
                width: 20% !important;
            }
            
            /* Header layout */
            .full-width-container table {
                width: 100% !important;
                table-layout: fixed !important;
            }
            
            /* Title cell */
            .full-width-container table td:nth-child(2) {
                width: 60% !important;
            }
            
            /* Wave cells */
            .full-width-container table td:first-child,
            .full-width-container table td:last-child {
                width: 35% !important;
            }
            
            /* Smaller waves that won't overlap */
            .divider {
                width: 60px !important;
                height: auto !important;
            }
            
            /* Make title smaller to fit */
            .header-title {
                font-size: 18px !important;
            }
            
            /* Remaining styles unchanged */
            .container {
                padding: 0 10px !important;
            }
            .section {
                padding-left: 10px !important;
                margin: 30px 0 !important;
            }
            .green-line {
                width: 100px !important;
            }
            h2 {
                font-size: 24px !important;
            }
            h3 {
                font-size: 20px !important;
            }
            .emoji {
                font-size: 24px !important;
            }
            p, li {
                font-size: 15px !important;
            }
            .ecosystem-header {
                font-size: 18px !important;
            }
            .social-icon {
                width: 32px !important;
                height: 32px !important;
            }
            .ecosystem-line-left, .ecosystem-line-right {
                width: 100px !important;
            }
            
            /* Make the title a bit smaller to fit between larger waves */
            .mobile-header span {
                font-size: 18px !important;
            }

            /* Footer mobile styles (Main Text Color) */
            .footer {
                margin-top: 30px !important;
                padding-top: 15px !important;
                font-size: 9px !important; /* Adjusted font size */
                color: #0A3A28 !important; /* Main text color */
            }
             .footer p {
                font-size: 9px !important; /* Adjusted font size */
                 color: #0A3A28 !important; /* Main text color */
            }
            .footer a {
                font-size: 9px !important; /* Ensure link also uses adjusted size */
                 color: #0A3A28 !important; /* Main text color */
            }
        }
    </style>
</head>
<body>
    <!-- Desktop header (hidden on mobile) -->
    <div class="full-width-container desktop-header">
        <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 40px; margin-top: 20px;">
            <tr>
                <td style="text-align: right; width: 50%;" valign="middle">
                    <img src="cid:green_divider_left" alt="" class="divider" style="margin-top: 4px;">
                </td>
                <td style="text-align: center; white-space: nowrap;" valign="middle">
                    <div class="header-title">Malda Alpha</div>
                </td>
                <td style="text-align: left; width: 50%;" valign="middle">
                    <img src="cid:green_divider_right" alt="" class="divider">
                </td>
            </tr>
        </table>
    </div>

    <!-- Mobile header with much bigger waves (200px) -->
    <div class="mobile-header" style="display: none; text-align: center; white-space: nowrap; margin: 25px 0;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
            <tr>
                <td width="40%" style="text-align: right; padding-right: 10px;">
                    <img src="cid:green_divider_left" alt="" style="width: 200px; display: inline-block;">
                </td>
                <td width="20%" style="text-align: center; vertical-align: middle;">
                    <span style="font-family: Verdana, sans-serif; font-weight: 400; font-size: 18px; line-height: 32px;">Malda Alpha</span>
                </td>
                <td width="40%" style="text-align: left; padding-left: 10px;">
                    <img src="cid:green_divider_right" alt="" style="width: 200px; display: inline-block;">
                </td>
            </tr>
        </table>
    </div>

    <!-- Main content container -->
    <div class="container">
        <!-- Welcome Section -->
        <div class="section">
            <h2><span class="emoji">🕊️</span>Welcome anon</h2>
            <p>
                GMalda, we're excited to kick off the first GMalda Newsletter! Catch exclusive alpha, hot takes on current events and find Malda's latest updates.
            </p>
        </div>

        <!-- Tokenomics Section -->
        <div class="section">
            <h2><span class="emoji">🗞️</span>Tokenomics, Release 1</h2>
            <p>
                Can't wait for Malda's tokenomics release? We will be releasing bits of the tokenomics leading up to mainnet. Check out an exclusive first look into <a href="https://mirror.xyz/0x4Da818DD3aAfb9D042a76B5037cdBa61533C7692/TKvUiRV7ClDEoXmELEwVDmsQ6q3R0rJ7yjBv3aT8NWs">Part 1</a>!
            </p>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 20px;">
                <tr>
                    <td style="width: 35%; padding-right: 5px; vertical-align: top; position: relative; top: -40px; left: -15px;">
                        <img src="cid:tokenomics_image" alt="Tokenomics Graphic" style="width: 70%; max-width: none; height: auto; display: block;">
                    </td>
                    <td style="width: 65%; vertical-align: top;">
                        <ul style="padding-left: 0px; margin: 0; max-width: 590px;">
                            <li style="font-family: Verdana, sans-serif; font-size: 16px; line-height: 150%; margin-bottom: 10px;">Malda will earn revenue from a multiple source (spread between borrows and supplies, liquidation fees + OEV and POL)</li>
                            <li style="font-family: Verdana, sans-serif; font-size: 16px; line-height: 150%; margin-bottom: 10px;">Malda will have unified interest rate for each asset, regardless of chain</li>
                            <li style="font-family: Verdana, sans-serif; font-size: 16px; line-height: 150%; margin-bottom: 10px;">Liquidators of the global pool can pay back debt on any chain</li>
                            <li style="font-family: Verdana, sans-serif; font-size: 16px; line-height: 150%; margin-bottom: 10px;">Setting up a Stability Module to add an extra layer of security for depositors against bad debt</li>
                            <li style="font-family: Verdana, sans-serif; font-size: 16px; line-height: 150%; margin-bottom: 10px;">Rebalancing within the global pool will be done predictively using estimates from historical data</li>
                        </ul>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Malda's Approach Section -->
        <div class="section">
            <h2><span class="emoji">🪙</span>Malda's Approach to Tokenomics</h2>
            <p>
                We designed the tokenomics in partnership with quants from TAU Labs in order to bring out the most out of it, who've helped us with creative ideas and financial modeling.
            </p>
            <p>
                Throughout our design process, the priority in our mind was to create a fair and sustainable structure which favors both the old (Mendi) community and new community, while having a catalyst for significant growth.
            </p>
            <p>
                A core tenet was to create a token with utility for the long run and can withstand multiple cycles. You'll be happy to hear that the real yield mechanism is a prime output of this ideology that will be making a return for $MALDA staking.
            </p>
            <p>
                On top of this, we're excited to unveil new mechanisms that align with the global ethos. Global liquidations will allow liquidators to repay debt from any supported chain, allowing us to safely deploy assets globally even on low DEX liquidity chains. We are building Malda to be infinitely scalable.
            </p>
            <p>
                Security still remains our top priority, and we have fresh additions to bolster economic security. The "Stability Module" give another layer of security to depositors against bad debt.
            </p>
            <p>
                Malda Points has the goal attracting liquidity and increasing brand awareness by valuing all contributors in a fair way. We will also be maximizing engagement throughout the points campaign to keep users interested and excited all throughout.
            </p>
            <p>
                This is just the beginning. While we begin sharing tokenomics, some details must remain private until TGE. However, expect many exciting details in future publications about Malda Points, position migration, token migration and more!
            </p>
            <p>
                Stay in the loop, see you on the next one.
            </p>
        </div>

        <!-- Ecosystem Updates with green lines from the middle -->
        <div style="text-align: center; margin: 60px 0 40px;">
            <table cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto; width: auto;">
                <tr>
                    <td style="text-align: right; padding-right: 20px; vertical-align: middle;">
                        <img src="cid:green_line" alt="" class="ecosystem-line-left" style="width: 160px; height: 3px; display: inline-block; vertical-align: middle;">
                    </td>
                    <td style="text-align: center; vertical-align: middle;">
                        <div class="ecosystem-header">Ecosystem Updates</div>
                    </td>
                    <td style="text-align: left; padding-left: 20px; vertical-align: middle;">
                        <img src="cid:green_line" alt="" class="ecosystem-line-right" style="width: 160px; height: 3px; display: inline-block; vertical-align: middle;">
                    </td>
                </tr>
            </table>
        </div>

        <!-- Ecosystem Subsections -->
        <div class="section">
            <h3><span class="emoji">⛓️</span>Will All Lending be Decentralized?</h3>
            <p>
                Data from <a href="https://www.galaxy.com/insights/research/the-state-of-crypto-lending/">Galaxy Research</a> certainly shows a bullish future! DeFi lending has grown over 950% since 2022 reaching $19billion while CeFi lending like Tether, Galaxy and Ledn have dropped by 68%. With crypto becoming more mainstream, it is expected that demand rises in its core use case. Malda is geared to take this on, and much more through our infinitely scalable foundations set in ZK.
            </p>
        </div>

        <div class="section">
            <h3><span class="emoji">🌐</span>Scaling ETH Throughput by 1000x</h3>
            <p>
                <a href="https://x.com/drakefjustin/status/1911689366730158409">Justin Drake suggested</a> that zkvms combined with SNARKs can make TPS go from 10 to 10,000 by verifying a SNARK for every block, rather than re-executing them. He still believes that most activity will remain on L2s where TPS can reach 10mil. Malda will also run on a zkVM, and will soon have a customizable interest rate curve for users in order to ensure optimal utilization rates and yields regardless of market conditions.
            </p>
        </div>

        <div class="section">
            <h3><span class="emoji">❄️</span>Everclear Goes to Mainnet</h3>
            <p>
                Everclear has officially <a href="https://x.com/EverclearOrg/status/1912128922902516082">launched to mainnet</a> after surpassing $125mil monthly volume in March! Since their beta in September, they expanded from 5 chains to the current 20 chains and target 40+ by the end of Q2 2025. Everclear is an intent-based settlement protocols, and one of the protocols in charge of rebalancing assets across Malda's Global Pool to ensure sufficient liquidity for borrows and withdraws - a cornerstone enabling the unified lending experience.
            </p>
        </div>

        <!-- Social Section with green lines starting from middle of icons -->
        <table cellspacing="0" cellpadding="0" border="0" style="width: 100%; margin: 60px auto 30px;">
            <tr>
                <td style="width: 35%; text-align: right;">
                    <img src="cid:green_line" alt="" style="width: 180px; height: 4px; display: inline-block; margin-right: -20px;">
                </td>
                <td style="width: 30%; text-align: center;">
                    <table cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                        <tr>
                            <td style="padding: 0 8px;">
                                <a href="https://x.com/malda_xyz">
                                    <img src="cid:social_twitter" alt="Twitter" class="social-icon">
                                </a>
                            </td>
                            <td style="padding: 0 8px;">
                                <a href="https://discord.com/invite/G3vWy8cbnK">
                                    <img src="cid:social_discord" alt="Discord" class="social-icon">
                                </a>
                            </td>
                            <td style="padding: 0 8px;">
                                <a href="https://malda.xyz/">
                                    <img src="cid:social_website" alt="Website" class="social-icon">
                                </a>
                            </td>
                            <td style="padding: 0 8px;">
                                <a href="https://t.me/malda_xyz">
                                    <img src="cid:social_telegram" alt="Telegram" class="social-icon">
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
                <td style="width: 35%; text-align: left;">
                    <img src="cid:green_line" alt="" style="width: 180px; height: 4px; display: inline-block; margin-left: -20px;">
                </td>
            </tr>
        </table>

        <!-- Footer Section (Minimal - Privacy Policy Only) -->
        <div class="footer">
            <p>
                Read our <a href="https://malda.xyz/newsletter-privacy-policy/" target="_blank">Privacy Policy</a> to learn how we handle your data.
            </p>
        </div>

    </div> <!-- End .container -->
</body>
</html>
"""

TEXT_TEMPLATE = """
Malda Alpha - Newsletter #1

Welcome anon
GMalda, we're excited to kick off the first GMalda Newsletter! Catch exclusive alpha, hot takes on current events and find Malda's latest updates.

Tokenomics, Release 1
Can't wait for Malda's tokenomics release? We will be releasing bits of the tokenomics leading up to mainnet. Check out an exclusive first look into Part 1!
* Malda will earn revenue from a multiple source (spread between borrows and supplies, liquidation fees + OEV and POL)
* Malda will have unified interest rate for each asset, regardless of chain
* Liquidators of the global pool can pay back debt on any chain
* Setting up a Stability Module to add an extra layer of security for depositors against bad debt
* Rebalancing within the global pool will be done predictively using estimates from historical data

Malda's Approach to Tokenomics
We designed the tokenomics in partnership with quants from TAU Labs... Throughout our design process, the priority was a fair and sustainable structure... A core tenet was to create a token with utility for the long run... On top of this, new mechanisms align with the global ethos... Security still remains our top priority... Malda Points has the goal attracting liquidity... This is just the beginning... Stay in the loop, see you on the next one.

Ecosystem Updates

Will All Lending be Decentralized?
Data from Galaxy Research shows a bullish future! DeFi lending has grown over 950% since 2022... Malda is geared to take this on...

Scaling ETH Throughput by 1000x
Justin Drake suggested that zkvms combined with SNARKs can make TPS go from 10 to 10,000... Malda will also run on a zkVM...

Everclear Goes to Mainnet
Everclear has officially launched to mainnet after surpassing $125mil monthly volume... Everclear is an intent-based settlement protocols...

---
Follow us:
Twitter: https://x.com/malda_xyz
Discord: https://discord.com/invite/G3vWy8cbnK
Website: https://malda.xyz/
Telegram: https://t.me/malda_xyz

---
Read our Privacy Policy: https://malda.xyz/newsletter-privacy-policy/
"""

# Updated image paths
IMAGE_PATHS = {
    # Header
    'green_divider_left': 'NEW_images/lines_from_left.svg',
    'green_divider_right': 'NEW_images/lines_from_right.svg',
    # Content image
    'tokenomics_image': 'NEW_images/tallcoins_2.svg',
    # Green line for dividers
    'green_line': 'NEW_images/green line.svg',
    # Social icons
    'social_twitter': 'NEW_images/Twitter.svg',
    'social_discord': 'NEW_images/Discord.svg',
    'social_website': 'NEW_images/Malda.svg',
    'social_telegram': 'NEW_images/Telegram.svg'
}

# Check if images exist
for img_name, img_path in IMAGE_PATHS.items():
    if not os.path.exists(img_path):
        print(f"⚠️ Warning: Image file {img_path} not found in {os.getcwd()}")
    else:
        print(f"✅ Image file found: {img_path}")

# Function to send an email - let's fix the SVG handling
def send_email(to_email):
    try:
        msg = MIMEMultipart("related")
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = SUBJECT

        # This is essential for Mailgun to process the unsubscribe link
        msg["X-Mailgun-Variables"] = '{"disable_footer": "yes"}' # <--- THIS IS THE KEY
        msg["X-Mailgun-Track"] = "no"
        msg["X-Mailgun-Track-Clicks"] = "no"
        msg["X-Mailgun-Track-Opens"] = "no"
        msg["X-Mailgun-Drop-Message"] = "no"
        msg["List-Unsubscribe"] = "<%unsubscribe_url%>"

        # Attach HTML and Text parts
        msgAlternative = MIMEMultipart("alternative")
        msg.attach(msgAlternative)
        msgAlternative.attach(MIMEText(TEXT_TEMPLATE, "plain"))
        msgAlternative.attach(MIMEText(HTML_TEMPLATE, "html")) # Ensure HTML_TEMPLATE is clean

        # Log which files we're processing
        print(f"Processing images from: {os.getcwd()}")
        for cid, img_path in IMAGE_PATHS.items():
            print(f"Attaching image: {img_path} (CID: {cid})")
        
        # Attach all the images
        for cid, img_path in IMAGE_PATHS.items():
            if os.path.exists(img_path):
                # Log file found
                print(f"✓ Found: {img_path}")
                
                if img_path.lower().endswith('.svg'):
                    try:
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            tmp_png = tmp_file.name
                        
                            # Improved error handling for conversion
                            # Use a more robust approach with cairosvg directly
                            try:
                                # First try rsvg-convert (usually better quality)
                                subprocess.run(['rsvg-convert', '-o', tmp_png, '-d', '1200', '-p', '1200', img_path], 
                                              check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                                print(f"  ✓ Converted with rsvg-convert: {img_path}")
                            except Exception as e:
                                print(f"  ⚠ rsvg-convert failed ({e}), trying cairosvg...")
                                # Fallback to cairosvg
                                with open(img_path, 'rb') as svg_file:
                                    svg_data = svg_file.read()
                                cairosvg.svg2png(bytestring=svg_data, write_to=tmp_png, dpi=300)
                                print(f"  ✓ Converted with cairosvg: {img_path}")
                            
                            # Verify the output file exists and has content
                            if os.path.exists(tmp_png) and os.path.getsize(tmp_png) > 0:
                                with open(tmp_png, 'rb') as img_file:
                                    img = MIMEImage(img_file.read())
                                    print(f"  ✓ Read converted PNG: {tmp_png}")
                            else:
                                raise ValueError(f"Empty or missing output file: {tmp_png}")
                            
                    except Exception as e:
                        print(f"  ❌ ERROR converting {img_path}: {e}")
                        print(f"  ⚠ Attaching original SVG as fallback")
                        # Attach the original SVG as a fallback
                        with open(img_path, 'rb') as img_file:
                            img = MIMEImage(img_file.read())
                    finally:
                        # Clean up temp file
                        if 'tmp_png' in locals() and os.path.exists(tmp_png):
                            try:
                                os.unlink(tmp_png)
                                print(f"  ✓ Cleaned up: {tmp_png}")
                            except:
                                print(f"  ⚠ Failed to clean up: {tmp_png}")
                else:
                    # Direct attachment for non-SVG files
                    with open(img_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        print(f"  ✓ Read directly: {img_path}")
                
                # Set content ID and ensure it matches the HTML reference
                img.add_header('Content-ID', f'<{cid}>')
                img.add_header('Content-Disposition', 'inline')
                img.add_header('Content-Type', 'image/png')  # Force PNG type for better compatibility
                msg.attach(img)
                print(f"  ✓ Attached with CID: <{cid}>")
            else:
                print(f"❌ File NOT found: {img_path}")

        # Connect to Mailgun SMTP
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print("Starting TLS...")
            server.starttls()
            print(f"Logging in as {SMTP_USERNAME}...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print(f"Sending email from {FROM_EMAIL} to {to_email}...")
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")
        print("Detailed error:")
        traceback.print_exc()
        return False

def main():
    # Test with a single email first
    test_email = "balint@cryptopicnic.io"  # Replace with your email
    print(f"Sending test email to {test_email}...")
    success = send_email(test_email)

    if not success:
        print("Test email failed. Please fix the issues before continuing.")
        exit(1)

    print("Test email sent successfully. Press Enter to continue with the full list, or Ctrl+C to cancel.")
    input()

    # Sending emails with batch processing
    batch_size = 50  # Mailgun recommends sending in batches
    delay = 10  # Delay in seconds to prevent rate limits

    for index, row in df.iterrows():
        success = send_email(row["email"])
        
        # Pause every 50 emails to avoid Mailgun rate limiting
        if (index + 1) % batch_size == 0:
            print(f"⏳ Pausing for {delay} seconds to prevent rate limits...")
            sleep(delay)

    print("✅ All emails sent!")

if __name__ == "__main__":
    main()

