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

### Sequence for RansomHub Scripts and Explanation

1. Ransomhub_Scrapper.py
    - This script automates data scraping from the Play onion site on the Tor Browser within a Kali Linux environment. It extracts victim names, country, the date of the documented exploit, navigates to the subpage URL, and retrieves descriptions, description of company, links to the data and password for the files.
2. Industry_Play.py
    - This script utilizes the Jigsawstack prompt engine, based on the scraped descriptions, to generate potential sectors or business industries the victim may belong to. This is then further manually checked through with each victims' domain.

</details>

## References

https://www.ransomlook.io/
https://github.com/fastfire/deepdarkCTI/blob/main/ransomware_gang.md
https://ransomwatch.telemetry.ltd/#/profiles
