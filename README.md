# CS445 (Cyber Threat Intelligence) Group Project

## Group Project Description

With the rise in data exfiltration during ransomware attacks came a rise in "shaming" websites, which are leverage by threat actors to extort victims into paying the ransom.
Shaming websites are used by threat actors as a tool to publicly name victims and post stolen data in an effort to extort them into paying the ransom demand.

## Focus Period

> Jan 2024 to Aug 2024

## Contributors

| APT Group  | Contributor Name |
| ---------- | ---------------- |
| BlackBasta | Dexter           |
| Inc Ransom | Enqi             |
| Play       | Chee Kiat        |
| Ransomhub  | Wai Soon         |

## Project Setup

<details>

<summary>Virtual Environment Setup</summary>

### Virtual Environment Setup Steps

-   On Windows, invoke the venv command as follows:

```python
   puts "python -m venv /path/to/new/virtual/environment
```

</details>

<details>

<summary>Pre-requisites</summary>

### Download needed libraries from Requirements.txt

-   Invoke the following command to download libraries specified in Requirements.txt

```python
   puts "pip install -r /path/to/requirements.txt
```

</details>

<details>

<summary>RansomHub Walkthrough</summary>

### Sequence for RansomHub Scripts and Explanation

1. Ransomhub_Scrapper.py
    - This script leverages Selenium to automate data scraping from the RansomHub onion site on the Tor Browser within a Kali Linux environment. It extracts victim names, the date of the documented exploit, navigates to the subpage URL, and retrieves both the description and the exploited link.
2. Prompt_Sector.py
    - This script utilizes the Jigsawstack prompt engine, based on the scraped descriptions, to generate potential sectors or business industries the victim may belong to. This is then further manually checked through with each victims' domain.
3. Prompt_Countries.py
    - This script utilizes the Jiwsawstack prompt engine, based on the scraped descriptions, to generate potential countries the victim may belong to. This is then further manually checked through with tools such as shodan and whoisxmlapi, and manually checked through with each victim's domain.
4. cleanRansomhub.py
    - This script helps to clean up the data in our scraped file. It drops the unnecessary any errors contained row from the prompt scripts and remove the description column which is not needed for further analysis in Tableau.

</details>

<details>

<summary>Play Walkthrough</summary>

### Sequence for Play Scripts and Explanation

1. Play_Scrapper.py
    - This script automates data scraping from the Play onion site on the Tor Browser within a Kali Linux environment. It extracts victim names, country, the date of the documented exploit, navigates to the subpage URL, and retrieves descriptions, description of company, links to the data and password for the files.
2. Industry_Play.py
    - This script utilizes the Jigsawstack prompt engine, based on the scraped descriptions, to generate potential sectors or business industries the victim may belong to. This is then further manually checked through with each victims' domain.

</details>

<details>

<summary>Inc Ransom Walkthrough</summary>

### Sequence for Inc Ransom Scripts and Explanation

1. IncRansom_Scrapper.py
    - This script is designed to scrape victim data from a .onion website on the Tor browser, by using Selenium to automate the browsing and data extraction. The script extracts the subpage URL of each victim and navigates to each of these child webpage to retrieve the details.
2. cleanIncRansom.py
    - This script is designed to clean and enhance the dataset extracted from the website. It applies data validation and industry inference, before exporting the cleaned data into an Excel file. The industry inference is then manually validated to ensure accuracy.

</details>

<details>

<summary>Blackbasta Walkthrough</summary>

### Sequence for Blackbasta Scripts and Explanation

1. BlackBasta.py
    - This script scrapes a .onion site on the Tor network, extracting victim details, descriptions, and disclosed links from multiple pages. It uses Selenium to automate the browser actions and BeautifulSoup to parse the page content. The extracted data is then saved into a CSV file.
2. Prompt_Countries.py
    - This script reads the descriptions from the saved CSV file and uses the JigsawStack API to identify the country of the victims based on the description. It processes each description, adds the identified country to the data, and updates the CSV file with the new information. Any rows with errors are skipped or marked as errors in the output.
3. Prompt_Sector.py
    - This script also reads the descriptions from the CSV file and uses the JigsawStack API to identify the business sector or industry based on the description provided. It then updates these rows with the identified sector and writes the results to a new CSV file. Any errors encountered during the processing are logged.

</details>

## References

[RansomLook](https://www.ransomlook.io/)  
[DeepDarkCTI GitHub](https://github.com/fastfire/deepdarkCTI/blob/main/ransomware_gang.md)  
[RansomWatch](https://ransomwatch.telemetry.ltd/#/profiles)

