# Content Knowledge Miner (Youtube PoC)

A Proof of Concept for mining knowledge from YouTube videos using AI agents.

## Project Structure

- **backend/**
  - `app.py`: Main backend application file.
  - `agents/`: Contains agent configurations and code.
  - `models/`: Data models.
  - `services/`: Service modules for API integrations.
  - `tests/`: Unit tests for backend components.
  - `requirements.txt`: Backend dependencies.
- **frontend/**
  - `app.py`: Main frontend application file.
  - `templates/`: HTML templates.
  - `static/`: Static files like CSS and JavaScript.
    - `css/`
    - `js/`
- **docs/**: Project documentation.

## Testing

To run the backend unit tests, execute:

```bash
python -m unittest discover -s backend/tests


## Getting Started

Instructions on setting up the project will be added as development progresses.

#########################################################
1. IN Task 2.3: Integrate Google Cloud Speech-to-Text we had following outstanding task:
Handle Fetching of Available Captions (Optional)
Note: Implementing the retrieval of captions from YouTube is optional at this stage due to complexity. For now, you can leave a placeholder or return a message indicating that this feature is not yet implemented.

Question - do you believe its good moment to implement that outstanding feature?


#############
Update README.md

Include instructions on setting up Airtable and any necessary configurations.


## Airtable Setup

1. Create a new base in Airtable.
2. Create a new table named `Videos`.
3. Create a new table named `UserInputs`.
4. Expose tables via API.
5. Update `.env` with the base ID and API key.
6. Run `python backend/airtable_test.py` to verify the connection.
7. Airtable model definition:
Table: Videos

Fields (Columns):

Video ID (Primary Field)

Field Type: Single line text

Description: Unique identifier for each video (YouTube Video ID).

Title

Field Type: Single line text
Description

Field Type: Long text
Tags

Field Type: Multiple select

Options: You can leave this empty for now and add tags as needed.

Duration

Field Type: Duration

Format: Choose the appropriate format (e.g., h:mm
).

Published At

Field Type: Date

Include time field: Yes

View Count

Field Type: Number

Format: Integer

Like Count

Field Type: Number

Format: Integer

Dislike Count

Field Type: Number

Format: Integer

Comment Count

Field Type: Number

Format: Integer

Transcript Text

Field Type: Long text
Summary Text

Field Type: Long text
Key Topics

Field Type: Multiple select

Options: Add key topics as needed.

Table: UserInputs

Fields (Columns):

Record ID (Primary Field)

Field Type: Auto number
Video ID

Field Type: Link to another record

Linked Table: Videos

Description: Associates the user input with a video.

Category

Field Type: Single select

Options: You can define categories such as "AI Automation", "Machine Learning", etc.

Comments

Field Type: Long text
Highlights

Field Type: Long text
Quality Rating

Field Type: Rating

Style: Stars

Maximum: 5


7. Update Documentation

Update README.md

Include instructions on how to specify different models when making requests.
Document any prerequisites for using Anthropic's API.

7. Update Documentation

Update README.md

Document the addition of the raw_data field in the VideoMetadata data model.
Explain the purpose of storing raw JSON data.
Provide instructions on how to access and interpret the Raw Data field in Airtable.