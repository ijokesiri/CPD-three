import csv
import glob
import re
import os
from urllib.parse import quote

def generate_meets_list_page():
    """Generate a meets list page with links to all meet pages."""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meets List</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to Main Content</a>
    <header>
        <h1>Meets List</h1>
        <div class="topnav">
            <a href="index.html">Home</a></li>
            <a href="athletes.html">Athletes List</a></li>
        </div>
    </header>
    <div id="main-content">
        <h2>List of Meets</h2>
        <ul>
'''

    # Use a set to track unique meet names and avoid duplicates
    meets_folder = 'meets'
    meet_files = set(f for f in os.listdir(meets_folder) if f.endswith('.html'))
    for meet_file in sorted(meet_files):
        meet_name = os.path.splitext(meet_file)[0]
        # Encode the meet name for the URL
        meet_name_encoded = quote(meet_name)
        html_content += f'<li><a href="{meets_folder}/{meet_name_encoded}.html">{meet_name}</a></li>\n'

    html_content += '''
        </ul>
    </div>
    <footer>
        <p>Skyline High School</p>
    </footer>
</body>
</html>
'''

    with open('meets.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Meets list page generated successfully.")

def process_athlete_data(file_path):
    # Extracting athlete stats by year
    records = []

    # Extracting athlete races
    races = []           

    athlete_name = ""
    athlete_id = ""
    comments = ""

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

        athlete_name = data[0][0]
        athlete_id = data[1][0]
        print(f"The athlete id for {athlete_name} is {athlete_id}")

        for row in data[5:-1]:
            if row[2]:
                records.append({"year": row[2], "sr": row[3]})
            else:
                races.append({
                    "finish": row[1],
                    "time": row[3],
                    "meet": row[5],
                    "url": row[6],
                    "comments": row[7]
                })

    return {
        "name": athlete_name,
        "athlete_id": athlete_id,
        "season_records": records,
        "race_results": races,
        "comments": comments
    }    

def gen_athlete_page(data, outfile):
    # Start building the HTML structure
    html_content = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- FontAwesome (Replace YOUR_ID with your own) -->
        <script src="https://kit.fontawesome.com/YOUR_ID.js" crossorigin="anonymous"></script>
        
        <link rel="stylesheet" href="css/reset.css">
        <link rel="stylesheet" href="css/style.css">
        
        <title>{data["name"]}</title>
    </head>
    <body>
        <a href="#main">Skip to Main Content</a>
        <nav>
            <ul>
                <li><a href="/index.html">Home Page</a></li>
            </ul>
        </nav>
        <header>
            <h1>{data["name"]}</h1>
            <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200">
        </header>
        <main id="main">
            <section id="athlete-sr-table" class="table-container">
                <h2>Athlete's Seasonal Records (SR) per Year</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Year</th>
                            <th>Season Record (SR)</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    # Loop to add each season record
    for sr in data["season_records"]:
        html_content += f'''
                        <tr>
                            <td data-label="Year">{sr["year"]}</td>
                            <td data-label="Season Record (SR)">{sr["sr"]}</td>
                        </tr>
        '''

    html_content += '''
                    </tbody>
                </table>
            </section>
            <section id="athlete-result-table" class="table-container">
                <h2>Race Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Race</th>
                            <th>Athlete Time</th>
                            <th>Athlete Place</th>
                            <th>Race Comments</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    # Loop to add each race result
    for race in data["race_results"]:
        html_content += f'''
                        <tr class="result-row">
                            <td data-label="Race">
                                <a href="{race["url"]}">{race["meet"]}</a>
                            </td>
                            <td data-label="Athlete Time">{race["time"]}</td>
                            <td data-label="Athlete Place">{race["finish"]}</td>
                            <td data-label="Race Comments">{race["comments"]}</td>
                        </tr>
        '''
    
    html_content += '''
                    </tbody>
                </table>
            </section>
            <section id="gallery">
                <h2>Gallery</h2>
            </section>
        </main>
        <footer>
            <p>Skyline High School<br>
            <address>2552 North Maple Road<br>Ann Arbor, MI 48103</address><br>
            <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
            Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/"><i class="fa-brands fa-instagram" aria-label="Instagram"></i></a>
        </footer>
    </body>
    </html>
    '''
    
    with open(outfile, 'w') as output:
        output.write(html_content)


def generate_index_page():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Athlete Website: Home Page</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to Main Content</a>
    <header>
        <h1>Athlete Website</h1>
        <div class="topnav">
            <a href="athletes.html">Athletes</a></li>
            <a href="meets.html">Meets</a></li>
        </div>
    </header>
    <div id="main-content">
        <h2>Welcome to the Athlete Information Site</h2>
        <p>This website provides information about athletes, their records, and upcoming meets.</p>
    </div>
    <footer>
        <p>Skyline High School</p>
    </footer>
</body>
</html>
'''
    with open('index.html', 'w') as f:
        f.write(html_content)

def generate_athletes_list_page(men_athletes, women_athletes):
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Athletes List</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to Main Content</a>
    <header>
        <h1>Athletes List</h1>
        <div class="topnav">
            <a href="index.html">Home</a></li>
            <a href="meets.html">Meets</a></li>
        </div>
    </header>
    <div id="main-content">
        <h2>Men's Athletes</h2>
        <ul>
'''

    # Add men's athletes to the list with correct links
    for athlete in men_athletes:
        athlete_name = athlete["name"]
        athlete_id = athlete["athlete_id"]
        # Create the correct filename
        filename = f"{athlete_name}{athlete_id}.html"
        html_content += f'<li><a href="mens_team/{filename}">{athlete_name} (ID: {athlete_id})</a></li>'

    html_content += '''
        </ul>
        <h2>Women's Athletes</h2>
        <ul>
'''

    # Add women's athletes to the list with correct links
    for athlete in women_athletes:
        athlete_name = athlete["name"]
        athlete_id = athlete["athlete_id"]
        # Create the correct filename
        filename = f"{athlete_name}{athlete_id}.html"
        html_content += f'<li><a href="womens_team/{filename}">{athlete_name} (ID: {athlete_id})</a></li>'

    html_content += '''
        </ul>
    </div>
    <footer>
        <p>Skyline High School</p>
    </footer>
</body>
</html>
'''

    with open('athletes.html', 'w') as f:
        f.write(html_content)



def main():
    # Store athlete data for both teams
    men_athletes = []
    women_athletes = []

    # Process men's team CSV files
    folder_path = 'mens_team/'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    for file in csv_files:
        athlete_data = process_athlete_data(file)
        men_athletes.append(athlete_data)  # Add athlete data to the list
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

    # Process women's team CSV files
    folder_path = 'womens_team/'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    for file in csv_files:
        athlete_data = process_athlete_data(file)
        women_athletes.append(athlete_data)  # Add athlete data to the list
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

    generate_index_page()  # Generate the home page
    generate_athletes_list_page(men_athletes, women_athletes)  # Generate the athletes list page
    generate_meets_list_page()

if __name__ == "__main__":
    main()

