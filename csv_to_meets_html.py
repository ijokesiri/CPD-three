import csv
import os

import os
import csv
import re


def csv_to_html(csv_filename, output_folder):
    """Convert a CSV file to an HTML file for meets, updating if content has changed."""
    meet_name = os.path.splitext(os.path.basename(csv_filename))[0]
    html_filename = os.path.join(output_folder, f"{meet_name}.html")

    try:
        # Read CSV file content
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            # Ensure there are at least 5 rows for valid HTML generation
            if len(rows) < 5:
                print("CSV file must have at least 5 rows.")
                return

            # Extract values from the first five rows
            link_text = rows[0][0]
            h2_text = rows[1][0]
            link_url = rows[2][0]
            summary_text = rows[3][0]

            # Generate HTML content
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header>
    <h1><a href="{link_url}">{link_text}</a></h1>
    <h2>{h2_text}</h2>
</header>
<a href="#main">Skip to Main Content</a>
<div class="topnav">
    <a href="../index.html">Home Page</a></li>
    <a href="#team-results">Team Results</a></li>
    <a href="#individual-results">Individual Results</a></li>
    <a href="#gallery">Gallery</a></li>
</div>
<main id="main">
<section class="summary" id="summary">
    <h2>Race Summary</h2>
    {summary_text}
</section>
"""

            # Team results section
            html_content += """<section id="team-results">
            <h2>Team Results</h2>
            <table>\n"""

            for row in rows[4:]:
                if len(row) == 3:
                    if row[0] == "Place":
                        html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"
                    else:
                        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"
                elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                    html_content += "</table></section><section id='individual-results'><h2>Individual Results</h2>"
                    place, grade, name, time, profile_pic = row[0], row[1], row[2], row[4], row[7]
                    html_content += f"""
<div class="athlete">
    <figure> 
        <img src="../images/profiles/{profile_pic}" width="200" alt="Profile picture of {name}"> 
        <figcaption>{name}</figcaption>
    </figure>
    <dl>
        <dt>Place</dt><dd>{place}</dd>
        <dt>Time</dt><dd>{time}</dd>
        <dt>Grade</dt><dd>{grade}</dd>
    </dl>
</div>
"""

            # Gallery section
            html_content += """</section><section id="gallery"><h2>Gallery</h2>"""
            html_content += create_meet_image_gallery(link_url)  # Assuming this function exists

            # Closing HTML tags
            html_content += """
   </section>
   </main>   
   <footer>
       <p>
       Skyline High School<br>
       <address>
       2552 North Maple Road<br>
       Ann Arbor, MI 48103<br><br>
       </address>
       <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
       Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
   </footer>
   </body>
</html>
"""

            # Check if the HTML file exists and if the content has changed
            if os.path.exists(html_filename):
                with open(html_filename, 'r', encoding='utf-8') as existing_file:
                    existing_content = existing_file.read()
                    if existing_content == html_content:
                        print(f"HTML file '{html_filename}' is up-to-date. No update needed.")
                        return

            # Write new or updated HTML content to the file
            with open(html_filename, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)

            print(f"HTML file '{html_filename}' created or updated successfully.")

    except Exception as e:
        print(f"Error processing file: {e}")

def process_meet_files():
    meets_folder = os.path.join(os.getcwd(), "meets")
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        csv_to_html(csv_file_path, meets_folder)


import re
import os
import random

# Step 1: Extract the meet ID from the URL
def extract_meet_id(url):
    # Regex to extract the meet ID, which is the number right after '/meet/'
    match = re.search(r"/meet/(\d+)", url)
    print(f"The meet id is {match}")
    if match:
        print(f"REturning {match.group(1)}")
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

# Step 2: Select 12 random photos from the folder
def select_random_photos(folder_path, num_photos=25):
    # List all files in the folder
    print(f"Checking {folder_path}")
    all_files = os.listdir(folder_path)
    # Filter out non-image files if necessary (assuming .jpg, .png, etc.)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Ensure we have enough images to select
    if len(image_files) < num_photos:
        return ""
        raise ValueError(f"Not enough images in the folder. Found {len(image_files)} images.")
    
    # Select 12 random images
    return random.sample(image_files, num_photos)

# Step 3: Generate HTML image tags
def generate_image_tags(image_files, folder_path):
    img_tags = []
    for img in image_files:
        img_path = os.path.join(folder_path, img)
        # print(f"The image_path is {img_path}")
        img_tags.append(f'<img src=../{img_path} width = "200" alt="">')
    return "\n".join(img_tags)

# Putting it all together
def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    # Define the folder path for images based on the meet ID
    folder_path = f'images/meets/{meet_id}/'

    # print(f"The folder path is {folder_path}")
    
    if not os.path.exists(folder_path):
        return ""
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")
    
    # Select 12 random photos
    selected_photos = select_random_photos(folder_path)
    
    # Generate image tags
    html_image_tags = generate_image_tags(selected_photos, folder_path)
    
    return html_image_tags

# Example usage
url = "https://www.athletic.net/CrossCountry/meet/235827/results/943367"
html_gallery = create_meet_image_gallery(url)
print(html_gallery)


if __name__ == "__main__":
    # Check if meets folder exists
    meets_folder = os.path.join(os.getcwd(), "meets")
    if not os.path.exists(meets_folder):
        print(f"Folder '{meets_folder}' does not exist.")
    else:
        process_meet_files()