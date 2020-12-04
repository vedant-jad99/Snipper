from bs4 import BeautifulSoup as bs
import json
from webbrowser import open_new_tab

def show():
    html = """<!DOCTYPE html>
        <html lang="en">

        <head>
            <title>
                Activity Report
            </title>
            <link rel="stylesheet" href="styles/tabledesign.css">
            <meta charset="UTF-8">
        </head>

        <body>
            <div id="title">
                <img src="images/Activity Report.png" id="image">
            </div>
            <table id="activityReport">
                <thead>
                    <tr>
                        <th id="timestamp">Timestamp</th>
                        <th id="activity">Activity</th>
                        <th id="location">Location</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>

            <script type="module" src="scripts/activity.js"></script>
        </body>

        </html>"""
    
    html = bs(html, "html.parser")
    m = html.find('tbody')

    with open("activity_and_logs/activities.json") as f:
        data = json.load(f)
        f.close()

    for i in data[::-1]:
        new = html.new_tag("tr")
        for key in i:
            child = html.new_tag("td")
            child.string = i[key]
            new.append(child)
        m.append(new)

    with open("show_report/report.html", "w") as f:
        f.write(str(html))
        f.close()

    open_new_tab("show_report/report.html")