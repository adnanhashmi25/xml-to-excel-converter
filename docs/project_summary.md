Project Title: Development of an XML to Excel Converter for Enhanced Data Management
Project Overview: 
Developed a tool to convert XML data into Excel spreadsheets, streamlining data sharing and enabling batch updates of network parameters. The tool was designed to handle varied XML structures from multiple network types, each with their own hierarchies, where mandatory parameters (acting as both parent and child elements) needed to be processed cohesively.
Role and Responsibilities:

•	Project Lead: Oversaw the entire development lifecycle, from requirements gathering to deployment.
•	System Architect: Designed the converter's architecture, ensuring scalability and integration with existing systems.
•	Developer: Implemented core functionalities, including XML parsing and Excel file generation.
•	Collaborator: Coordinated with cross-functional teams to align the tool with user needs and organizational objectives.

Technologies Used:

•	Programming Language: Python
•	Data Structures: Employed Python dictionaries, lists, and sets to efficiently parse and organize XML data while maintaining a minimal executable size.
•	Data Structures: Employed Python dictionaries, lists, and sets to efficiently parse and organize XML data while maintaining a minimal executable size.

Challenges and Solutions:

•	Diverse Data Structures:
Faced with XML files containing different hierarchies (for example, one file might include a model object for IPv6 configurations that aggregates data from multiple sites), I developed a parsing solution that groups data by model object while preserving the parent-child relationships. 
•	Handling Mandatory Parameters:
Some XML elements functioned as both mandatory parameters and as part of a hierarchical structure. I implemented logic to correctly interpret these dual roles without disclosing specific internal formats.
•	Reverse Engineering for Bulk XML Generation:
o	After developing the XML-to-Excel converter, I designed a reverse-engineering mechanism that could take an Excel file and regenerate change-ready XML files for bulk updates. 
o	This allowed batch modifications of network parameters, which could be inserted directly into the OSS GUI, bypassing the need for manual, one-by-one changes.
•	Handling Large Input Files Efficiently:
o	Previously, the tool processed entire XML backups (which could be large and slow to process).
o	Solution: Added filtering mechanisms using user-defined CSV files to allow targeted extraction, making the tool faster, more efficient, and adaptable to user needs.
•	Optimizing Processing Speed & Scalability:
o	Problem: Initially, the tool extracted the entire tar file before processing, which was inefficient for large backups.
o	Solution 1: Instead of extracting all files, the tool first scanned filenames inside the tar and only extracted relevant files if a site list was provided—reducing unnecessary disk operations.
o	Problem: XML parsing for multiple sites was originally sequential, leading to delays.
o	Solution 2: Introduced parallel processing, allowing multiple XML files to be processed simultaneously.
o	Default 8 parallel processes were used based on local system constraints.
o	Designed for scalability, allowing higher parallelization when deployed on a multi-core server.
•	Handling Large Excel Outputs Without Data Loss:
o	Problem: Some MOs produced extremely large datasets, exceeding Excel’s 1,048,576 row limit, causing data loss.
o	Solution: Designed a dictionary-based tracking system to monitor MO file sizes. 
o	If an MO’s output exceeded 900,000 rows, the tool automatically created a new file (e.g., mo_1.csv, mo_2.csv) to ensure all data remained accessible.
o	This dynamic naming mechanism prevented data corruption and allowed users to work with massive datasets without breaking Excel’s limitations.

Outcomes and Impact:

•	Improved Data Sharing: 
o	Transformed complex XML data into user-friendly Excel formats, allowing operations teams to access complete site data instantly without the 1 lakh line limit of OSS. 
o	Eliminated manual GUI-based navigation, enabling bulk extraction of unlimited network data in a structured format.
•	Automation Achievements: 
o	Enabled batch processing of parameter changes, reducing manual intervention and minimizing errors. 
o	Allowed operations teams to modify network configurations across multiple sites in one go, which was previously impossible with OSS limitations.
o	First, enabled automated extraction of XML into Excel for better data access. 
o	Then, reverse-engineered the process to allow Excel inputs to generate change-ready XML files. 
o	This allowed bulk updates to network configurations—something previously restricted by OSS manual limitations
•	Efficiency Gains: 
o	Cut data retrieval time from hours (manual OSS queries) to minutes (automated processing via input ZIP files).
o	Decreased the time required for data processing tasks by 50%, leading to faster decision-making and improved network troubleshooting speed.
•	Operational Impact:
o	Previously: Changes had to be entered one-by-one in OSS, making bulk modifications impossible. 
o	Now: Engineers can modify parameters for multiple sites at once and generate XML files that are ready to be inserted into OSS GUI, saving hours of manual work.
•	Increased Flexibility & User Control:
•	Users are no longer forced to process large backups; instead, they can extract only the relevant sites, MOs, or parameters, reducing time and resource usage.
•	Engineers can now perform targeted troubleshooting or modifications instead of dealing with bulk data dumps.
•	Significant Performance Gains
o	Reduced unnecessary disk operations → No longer extracts the full tar, improving efficiency for large backups. 
o	Parallel processing improved speed → On an 8-core system, batch processing was up to 8x faster compared to sequential execution. 
o	Designed for scalability → Performance could scale further when deployed on a high-core server
•	Improved Data Integrity & Accessibility
o	No more data loss due to Excel row limits → Large files are automatically split for seamless access. 
o	Users can still work with Excel files without issues, avoiding crashes or truncated data. 
o	Automated handling of large datasets → No manual intervention needed; the tool intelligently manages file splitting.

Features & Functionality:

Selective Data Extraction for Better Usability:
•	Introduced custom filtering options to allow users to extract only the necessary data instead of converting the entire input file.
•	Users can now control data extraction with two additional input files: 
o	site_list.csv → Converts only the specified sites (if empty, converts all sites).
o	MO_list.csv → Converts only the specified Model Objects (if empty, converts all MOs).
o	If an MO is provided without parameters, the tool extracts all parameters for that MO.
