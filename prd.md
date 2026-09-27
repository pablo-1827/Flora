# Master Product Requirements Document (PRD)

![AI Powered Opportunity Discovery Platform for Students | Devpost](https://images.openai.com/static-rsc-4/rv0k3AameaawzJunlTp1YVw8aNUad6d6hKZvuMjlr5oyjijfLBWuco8nN-6rr-wxU_YN_EyD81JRIIH5MiQFTjeJfWV213V3v9oFUosqA00zxS8dRnMqC90_EsYQTt8ENR0aA-ZSioytzOKXa8nx87opRbtY_fTWQIWZfVidzxQ?purpose=inline)

# OpportunityHub

Hackathon Project · Flora Institute of Technology

Backend-first development

Python + FastAPI

PostgreSQL

Product tagline: One platform. Every opportunity. A future within reach.

## 1. Executive summary

OpportunityHub is a student-centric opportunity discovery platform that brings internships, hackathons, scholarships, certifications, competitions, workshops, courses, and research opportunities into one place.

Students create a profile containing their education, skills, interests, and preferences. The platform uses this information to discover, filter, and rank opportunities relevant to each student.

The goal is not simply to build another listing website. It is to create a personalized opportunity discovery system that helps students find opportunities they might otherwise miss.

### The core value proposition

> Every student should have access to the right opportunities, regardless of how widely scattered the information is.

## 2. Problem statement

Students frequently miss valuable opportunities because:

* Information is distributed across college groups, social media, websites, and newsletters.

* Opportunities are difficult to discover without already knowing where to look.

* Eligibility requirements vary by year, degree, skills, location, and other criteria.

* Application deadlines are easy to overlook.

* Generic listings contain many opportunities irrelevant to an individual student.

### Proposed solution

A centralized platform that combines opportunity collection, structured information, profile-based matching, powerful filters, and deadline tracking.

## 3. Product objectives

|
Objective

|

Expected outcome

|
| --- | --- |
|

Centralize discovery

|

One place to explore multiple opportunity categories

|
|

Personalize results

|

Relevant opportunities ranked against student profiles

|
|

Reduce missed deadlines

|

Clear deadlines and urgency indicators

|
|

Improve discoverability

|

Search, filters, and category browsing

|
|

Build trust

|

Source links, eligibility details, and verified information

|
|

Support growth

|

Modular backend and scalable database design

|

## 4. Target users

![What Should a Software Engineering Degree India Look Like Today? | SST](https://images.openai.com/static-rsc-4/Sniha5D_nuM9_8azRjntSanwEGV7c56VpdvVqeZxHL3Zsl4_FMZt6zz4K-DZkmVDnk0fCMqwFxyYjko9HUu_QTDUvl5_aC6KCMBaQHQHTzZlCDP0yjaMHEuf7IrSSbEpmnFqDPnVLUYqVjXipgsVh4XKe6JYRE-NB82xXUasofg?purpose=inline)

Primary: College students

Diploma, undergraduate, and postgraduate students looking for internships, competitions, scholarships, courses, and other academic or career opportunities.

![Our Team](https://images.openai.com/static-rsc-4/67VZaxaeXxl59uhhrPv79MWpMl2MLxrq8Sr6YLvEKQNRoHwq4bQ8iiVzAm7-mtqGTl2JSIqj3M7HXtS56DCb0bc6o6anoIMVSjT5_e3yhalU3oXg3oMAp2DsDgIcHVNZF7WjG74SPgIAhVaTNChXt6Mx9sgTzBN9HzSJHGUJPNs?purpose=inline)

Secondary: College administrators

Placement cells, faculty coordinators, and student clubs who want to share relevant opportunities with students.

![Gençleri uzayla buluşturan "Astro Hackathon" etkinliği Nevşehir'de başladı](https://images.openai.com/static-rsc-4/_aRrPwPZaZa3DjK8nBuZ9P2vNUse41IrBTuwUkSpMda_ThyV9Fpl4W2xMvItekNulvTapR9PpNFaUWRyAOizZvhQfcfc-2La0UVujPh_9dGKrHuIbTVDD8qQkQMEtvTK1iTGSAJ7_79MYU91QFHSbYU8FOPrjdeeAoLr34jYuo8?purpose=inline)

Future: Opportunity providers

Companies, event organizers, scholarship providers, and educational institutions.

For the hackathon MVP, the student experience is the priority. An administrator interface will support opportunity management.

## 5. Scope and priorities

P0

Essential MVP

Authentication, student profiles, opportunity listings, search, filters, recommendation scoring, bookmarks, and deadline visibility.

P1

Enhanced experience

Admin dashboard, CSV imports, application tracking, personalized alerts, and improved opportunity ingestion.

P2

Future expansion

Semantic search, automated source aggregation, email notifications, organizer accounts, and advanced analytics.


## 6. Functional requirements

### 6.1 Student registration and authentication

Students must be able to create accounts and securely access their profiles.

Requirements

* Register using name, email, and password.

* Log in and log out.

* Validate email format and enforce password requirements.

* Prevent duplicate accounts for the same email.

* Retrieve the authenticated student's account.

* Protect profile, bookmark, and application data from other users.

* Support secure password hashing and token-based authentication.

Acceptance criteria: A registered student can log in, access their own profile, and use protected APIs. Invalid credentials must not grant access.

### 6.2 Student profile

The profile is the foundation of the recommendation engine.

|
Field

|

Requirement

|
| --- | --- |
|

Full name

|

Required

|
|

Email

|

Required; obtained from account

|
|

College

|

Required

|
|

Degree

|

Required

|
|

Branch / stream

|

Required

|
|

Current academic year

|

Required

|
|

Graduation year

|

Required

|
|

Skills

|

Multiple selections

|
|

Interests

|

Multiple selections

|
|

Preferred categories

|

Multiple selections

|
|

Preferred mode

|

Online, offline, hybrid, or any

|
|

Preferred location

|

Optional

|
|

Resume URL

|

Optional, future-ready

|

Students must be able to create, view, and update their profiles.

Important: The profile should support incomplete setup. Students can browse opportunities before completing every optional field, but recommendations should improve as the profile becomes more complete.

### 6.3 Opportunity management

Each opportunity must contain structured information.

|
Field

|

Description

|
| --- | --- |
|

Title

|

Name of the opportunity

|
|

Organization

|

Company, institution, or organizer

|
|

Description

|

Overview and details

|
|

Category

|

Internship, hackathon, scholarship, etc.

|
|

Skills

|

Relevant skills

|
|

Eligibility

|

Who can participate

|
|

Eligible degrees / branches

|

Applicable academic streams

|
|

Eligible years

|

Applicable academic years

|
|

Location

|

City, state, or country, if applicable

|
|

Mode

|

Online, offline, or hybrid

|
|

Start date

|

Optional event or program start

|
|

Deadline

|

Last application date and time

|
|

Benefits

|

Stipend, prize, certificate, or other benefits

|
|

Application URL

|

Official application page

|
|

Source name

|

Where the information originated

|
|

Source URL

|

Original announcement

|
|

Status

|

Draft, published, expired, or archived

|

Each published opportunity should have a unique ID, creation timestamp, and last-updated timestamp.

The backend must distinguish between an application deadline and an event's start or end date.

### 6.4 Opportunity discovery

The discovery endpoint must support:

* Browsing all published opportunities.

* Category-based browsing.

* Keyword search.

* Filtering by skills, location, mode, and eligibility.

* Filtering by upcoming or expired deadlines.

* Sorting by relevance, newest, and deadline.

* Pagination.

* Viewing complete opportunity details.

Expired opportunities should not appear in the default active results, but may be accessible through an explicit filter or historical view.

### 6.5 Personalized recommendations

The platform should calculate a relevance score for each opportunity based on the student's profile.

Each recommendation should provide:

* A relevance score from 0 to 100.

* A ranked list of matching opportunities.

* A short explanation of why an opportunity matches.

* Eligibility information.

* Deadline information.

Example:

92% match

Hackathon

## National Student AI Challenge

Example opportunity · Illustrative data

Python

Machine Learning

Online

Why this matches

* Matches your AI and hackathon interests.

* Uses skills listed in your profile.

* Matches your preferred participation mode.

The score must represent profile relevance, not the probability of winning or being selected.

### 6.6 Bookmarks

Students can:

* Save an opportunity.

* Remove a saved opportunity.

* View all saved opportunities.

* See whether a saved opportunity has expired.

A student must not be able to access or modify another student's bookmarks.

### 6.7 Application tracking

For the MVP, application tracking is a personal record. The platform does not submit applications on behalf of students.

Supported statuses:

* Interested

* Planning to apply

* Applied

* Shortlisted

* Selected

* Rejected

* Withdrawn

Students can update the status and optionally add a note.

### 6.8 Deadline tracking

The system should calculate deadline urgency using the opportunity's deadline and the current time.

|
Status

|

Rule

|
| --- | --- |
|

Closing soon

|

Within 48 hours

|
|

Upcoming

|

More than 48 hours away

|
|

Expired

|

Deadline has passed

|
|

No deadline

|

No deadline supplied

|

Use the appropriate timezone when interpreting deadlines. Store timestamps consistently in UTC and display them in the user's local timezone.

### 6.9 Admin management

An administrator can:

* Create and edit opportunities.

* Publish, archive, or remove listings.

* Import opportunities through CSV.

* Review source links and required fields.

* Identify duplicate listings.

* View basic platform statistics.

Admin privileges must be enforced by the backend, not merely hidden in the frontend.

## 7. Backend technology stack

Python 3.12

Primary programming language

FastAPI

REST API framework

PostgreSQL

Primary relational database

SQLAlchemy 2.x

Database ORM

Alembic

Database schema migrations

Pydantic

Request and response validation

JWT

Access-token authentication

Argon2

Password hashing

Pytest

Automated testing

### Why this stack?

* FastAPI provides automatic API documentation and request validation.

* PostgreSQL supports relational data, constraints, transactions, and flexible queries.

* SQLAlchemy keeps database access organized and maintainable.

* Alembic enables controlled database schema changes.

* Pytest allows us to test each backend module before frontend integration.

Database decision: PostgreSQL is the sole primary database. We will not introduce MySQL or MongoDB into the initial MVP.

## 8. System architecture

Frontend

HTML · CSS · JavaScript

FastAPI REST API

Authentication · Validation · Authorization

Service layer

Search · Matching · Deadlines

SQLAlchemy

Models · Queries · Transactions

PostgreSQL

Persistent application data

The frontend communicates with the backend through JSON-based HTTP APIs. The backend owns business logic, authorization, validation, recommendation scoring, and database access.

The frontend must never connect directly to PostgreSQL.

## 9. Database design

The database will be relational, normalized, and designed around the student's profile and the opportunity catalog.

### 9.1 Core entities

|
Table

|

Purpose

|
| --- | --- |
|

`users`

|

Account credentials, email, role

|
|

`student_profiles`

|

Education and preferences

|
|

`skills`

|

Reusable skill catalog

|
|

`student_skills`

|

Student-to-skill relationship

|
|

`interests`

|

Reusable interest catalog

|
|

`student_interests`

|

Student-to-interest relationship

|
|

`categories`

|

Opportunity categories

|
|

`student_categories`

|

Preferred categories

|
|

`opportunities`

|

Main opportunity records

|
|

`opportunity_skills`

|

Opportunity-to-skill relationship

|
|

`opportunity_eligibility`

|

Degree, branch, and year requirements

|
|

`bookmarks`

|

Saved opportunities

|
|

`applications`

|

Student application tracking

|
|

`sources`

|

Source and provenance information

|

### 9.2 Relationships

users

One account per student

student_profiles

One profile per user

student_skills

student_interests

student_categories

opportunities

Listings, eligibility, deadlines, and sources

bookmarks

applications

### 9.3 Database constraints

* Unique email addresses.

* Unique student profile per user.

* Unique student-skill and student-interest pairs.

* Unique bookmark per student and opportunity.

* Unique application record per student and opportunity.

* Foreign keys for all relationships.

* Appropriate indexes on opportunity category, deadline, publication status, and relationship keys.

* Consistent timestamps and explicit handling of nullable fields.

The schema should avoid storing comma-separated skills or interests in a single text column. Many-to-many relationships should use junction tables.

## 10. Recommendation engine specification

The first version will use a deterministic, explainable scoring algorithm. No external AI service is required.

### 10.1 Weighted score

### Opportunity relevance score

Initial weights — configurable during testing

Skill match

30%

Interest match

25%

Category preference

20%

Education eligibility

15%

Mode and location

10%

The initial formula is:

S=0.30K+0.25I+0.20C+0.15E+0.10PS = 0.30K + 0.25I + 0.20C + 0.15E + 0.10PS=0.30K+0.25I+0.20C+0.15E+0.10P

Where:

* KKK = skill match percentage.

* III = interest match percentage.

* CCC = preferred category match.

* EEE = education and eligibility match.

* PPP = location and participation-mode match.

Each component is normalized to a value from 0 to 100.

### 10.2 Eligibility handling

Eligibility must be handled separately from relevance.

An opportunity with a hard eligibility requirement that the student does not meet should be excluded from the eligible recommendations, or explicitly marked as ineligible.

Missing eligibility data must not automatically mean the student is ineligible. It should be marked as unknown.

### 10.3 Ranking rules

1. Exclude unpublished and expired opportunities from the default recommendation feed.

2. Evaluate known hard eligibility requirements.

3. Calculate the relevance score.

4. Sort eligible opportunities by score.

5. Apply a consistent tie-breaker, such as deadline and publication date.

6. Return a concise explanation of the matched attributes.

The system must not claim that a student is eligible when the source information is incomplete.

### 10.4 Cold-start behavior

For students with incomplete profiles:

* Show recent opportunities.

* Allow browsing by category.

* Ask the student to add skills and interests.

* Use only available profile fields for scoring.

* Avoid treating missing preferences as negative preferences.

## 11. API specification

All routes will use the `/api/v1` prefix to support future API evolution.

### 11.1 Authentication

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

POST

|

`/api/v1/auth/register`

|

Register

|
|

POST

|

`/api/v1/auth/login`

|

Authenticate

|
|

POST

|

`/api/v1/auth/refresh`

|

Refresh token, if implemented

|
|

GET

|

`/api/v1/auth/me`

|

Get current user

|

### 11.2 Student profile

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

GET

|

`/api/v1/profile/me`

|

Retrieve profile

|
|

PUT

|

`/api/v1/profile/me`

|

Create or update profile

|
|

PUT

|

`/api/v1/profile/me/skills`

|

Replace skill selections

|
|

PUT

|

`/api/v1/profile/me/interests`

|

Replace interest selections

|
|

PUT

|

`/api/v1/profile/me/preferences`

|

Update preferences

|

### 11.3 Opportunities

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

GET

|

`/api/v1/opportunities`

|

Browse and filter

|
|

GET

|

`/api/v1/opportunities/{id}`

|

Get details

|
|

GET

|

`/api/v1/opportunities/search`

|

Search

|
|

POST

|

`/api/v1/opportunities`

|

Create, admin only

|
|

PATCH

|

`/api/v1/opportunities/{id}`

|

Update, admin only

|
|

DELETE

|

`/api/v1/opportunities/{id}`

|

Archive or remove, admin only

|

Example discovery request:

http

```
GET /api/v1/opportunities?category=hackathon&mode=online&page=1&page_size=20
```

Example search request:

http

```
GET /api/v1/opportunities/search?q=python%20internship
```

### 11.4 Recommendations

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

GET

|

`/api/v1/recommendations`

|

Personalized feed

|
|

GET

|

`/api/v1/recommendations/{id}/explanation`

|

Match explanation

|

The recommendation endpoint should support pagination and an optional category filter.

### 11.5 Bookmarks and applications

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

GET

|

`/api/v1/bookmarks`

|

List saved opportunities

|
|

PUT

|

`/api/v1/bookmarks/{opportunity_id}`

|

Save opportunity

|
|

DELETE

|

`/api/v1/bookmarks/{opportunity_id}`

|

Remove bookmark

|
|

GET

|

`/api/v1/applications`

|

List tracked applications

|
|

PUT

|

`/api/v1/applications/{opportunity_id}`

|

Create or update tracking

|
|

DELETE

|

`/api/v1/applications/{opportunity_id}`

|

Remove tracking record

|

Using `PUT` for bookmark creation and application upserts makes repeated requests easier to handle safely.

### 11.6 Administrative APIs

|
Method

|

Endpoint

|

Purpose

|
| --- | --- | --- |
|

GET

|

`/api/v1/admin/opportunities`

|

Manage listings

|
|

POST

|

`/api/v1/admin/opportunities/import`

|

Import CSV

|
|

GET

|

`/api/v1/admin/statistics`

|

View platform statistics

|
|

PATCH

|

`/api/v1/admin/opportunities/{id}/status`

|

Publish or archive

|

### 11.7 API conventions

* JSON request and response bodies.

* Consistent error response structure.

* HTTP status codes used appropriately.

* Pagination metadata.

* Server-side validation.

* UTC timestamps in API responses.

* OpenAPI documentation available through FastAPI Swagger UI.

## 12. Opportunity data collection

A centralized discovery platform needs a reliable supply of opportunities. This is a core product requirement, not an optional implementation detail.

### Phase 1: Seed data and admin entry

* Add curated opportunities through the admin API.

* Include realistic sample data for demonstrations.

* Preserve the original source URL.

* Label demonstration records clearly in development environments.

### Phase 2: Bulk import

* Import records from CSV.

* Validate required fields and dates.

* Report rejected rows and validation errors.

* Detect likely duplicates.

### Phase 3: External data sources

Integrate suitable official APIs, RSS feeds, or permitted public data sources.

Each connector should normalize incoming data into the same opportunity schema.

### Phase 4: Automated aggregation

Add scheduled ingestion, source monitoring, duplicate detection, and expiration updates.

Important: Do not rely on indiscriminate scraping. Respect website terms, robots policies where applicable, rate limits, and source attribution. Never invent application links or present unverified listings as confirmed.

## 13. Security and privacy

Security is part of the MVP.

* Hash passwords using Argon2 or another appropriately configured password-hashing algorithm.

* Keep secrets in environment variables.

* Never commit `.env` files or database credentials.

* Use short-lived access tokens and validate token signatures and expiry.

* Enforce authorization on every protected endpoint.

* Restrict administrative APIs by role.

* Validate and constrain all user input.

* Use SQLAlchemy parameterized queries rather than constructing SQL from user input.

* Configure CORS for approved frontend origins.

* Apply sensible request-size limits and rate limits to sensitive endpoints.

* Avoid exposing passwords, token secrets, or unnecessary personal information in logs.

* Collect only the personal information required for the product.

If deployed publicly, use HTTPS and secure production configuration.

## 14. Non-functional requirements

|
Area

|

Requirement

|
| --- | --- |
|

Performance

|

Target p95 API response time below 500 ms for ordinary database-backed requests under the demo workload

|
|

Reliability

|

Consistent database transactions and graceful error handling

|
|

Scalability

|

Stateless API design and indexed database queries

|
|

Maintainability

|

Separate routers, services, models, and schemas

|
|

Usability

|

Clear API errors and predictable response structures

|
|

Security

|

Authentication, authorization, input validation

|
|

Data quality

|

Source attribution, duplicate checks, deadline validation

|
|

Accessibility

|

Frontend supports keyboard navigation and readable contrast

|
|

Portability

|

Local development setup documented and reproducible

|

Performance targets should be validated through testing; they are goals, not assumed results.

## 15. Backend project structure

The backend will be developed independently before connecting the frontend.

```
opportunity-hub/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   ├── skill.py
│   │   │   ├── category.py
│   │   │   ├── opportunity.py
│   │   │   ├── bookmark.py
│   │   │   └── application.py
│   │   ├── schemas/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── opportunities.py
│   │   │   ├── recommendations.py
│   │   │   ├── bookmarks.py
│   │   │   ├── applications.py
│   │   │   └── admin.py
│   │   ├── services/
│   │   │   ├── recommendation.py
│   │   │   ├── opportunity_service.py
│   │   │   ├── search.py
│   │   │   └── ingestion.py
│   │   └── dependencies/
│   │       ├── auth.py
│   │       └── permissions.py
│   ├── tests/
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── opportunities.html
│   ├── opportunity.html
│   ├── saved.html
│   ├── css/
│   └── js/
│
├── .gitignore
└── README.md
```

This structure is intentionally modular without introducing microservices. A single FastAPI application is sufficient for the hackathon.

## 16. Testing and acceptance criteria

The backend will be considered ready for frontend integration when the following checks pass.

### Backend readiness checklist

0/19 verified

Database and setup

Application connects to PostgreSQL using environment configuration.

Database migrations create the required schema.

Foreign keys and uniqueness constraints work correctly.

Authentication and profile

Registration rejects duplicate emails.

Passwords are securely hashed.

Login and protected endpoints work correctly.

Students cannot access another student's profile.

Opportunity discovery

Listings support pagination and filtering.

Search returns relevant keyword matches.

Expired and unpublished records are excluded by default.

Opportunity details include source and eligibility information.

Recommendations

Scores remain within 0–100.

Matching results are deterministic for the same inputs.

Hard eligibility mismatches are handled correctly.

Missing profile fields do not break recommendations.

Student actions and administration

Bookmarks are unique per student and opportunity.

Application status can be created and updated.

Non-admin users cannot access admin operations.

CSV import reports invalid records.

Reset checklist

The checklist is a planning aid; items should only be marked complete after they have actually been tested.

## 17. Backend development roadmap

The implementation order is deliberately backend-first.

1. Phase 1 — Project foundation

   First

   Set up Python, FastAPI, PostgreSQL, SQLAlchemy, configuration, database connectivity, and health-check endpoints.

   Deliverable: Running API connected to PostgreSQL.

2. Phase 2 — Database schema

   Create models, relationships, constraints, indexes, and Alembic migrations.

   Deliverable: Complete initial database schema.

3. Phase 3 — Authentication

   Implement registration, login, token validation, password hashing, and access control.

   Deliverable: Secure authentication APIs.

4. Phase 4 — Student profiles

   Implement education, skills, interests, and preferences.

   Deliverable: Persistent student profiles.

5. Phase 5 — Opportunity APIs

   Implement opportunity CRUD, source metadata, search, filters, pagination, and seed data.

   Deliverable: Functional opportunity catalog.

6. Phase 6 — Recommendation engine

   Implement scoring, eligibility handling, ranking, and explanations.

   Deliverable: Personalized recommendations.

7. Phase 7 — Bookmarks and tracking

   Implement saved opportunities, application records, and deadline status.

   Deliverable: Student opportunity management.

8. Phase 8 — Testing and integration

   Run automated tests, fix edge cases, document APIs, and connect the HTML/CSS/JS frontend.

   Deliverable: End-to-end working MVP.

## 18. Hackathon demonstration plan

The final demonstration should tell a clear story rather than simply show a collection of pages.

![Connexus Help](https://images.openai.com/static-rsc-4/gRFWY-yCEfes3ebZurAPk5Lg9kdDPCt6sjMlZaxUOk3PZhtWXISl4GDDSEtjk4rkzmxPrJo3v9pR8D-QT_E68bYKMeHP2_mU0XS8VIG0eHuyHDPMiJWKklOLLk5DvjOlmHXuellnFyftSBmxuof9V9XDytA2lAg6pV1dcnjmvR8?purpose=inline)

Scene 1 — The student

Create or log in to a student account and show the education, skills, and interests profile.

![TieOpp | AI-Powered Career Readiness & job Platform](https://images.openai.com/static-rsc-4/kt8StQcWrBjZ8Zi4eoQku0BokXRNrGgI_nvvqS6Tp2iBKCgYG3R7ZYgDvQpFCHq5fR3yH-h2q_JVTfEhk5v_TGgu6IiYCXJJUVLoxkqSVqCWXJRqLSwAMSARrjO9TeZzJY993V75zKOr8jiyRxuKKx8dvaDRldjawaPatfswBmA?purpose=inline)

Scene 2 — The problem solved

Browse opportunities from different categories in one place.

![AI Job Recommendations | Personalized Job Matches | GenZCareer | GenZCareer](https://images.openai.com/static-rsc-4/dhTvgcdZda7TjpetX49Ys4KwAgdxYV6FkOCKFkn9VFumDIiuG8UtonWExZXWvjuXtBbnBGrVmq7Vz_Bg5c7ksT3ceIXiVQYGIyWhLndJn1I7ql2nBxoFisJ97uFTx-Pt0G38FHIKrBAYsfVmeOseVEBR4t7HFXdYhrDegDHJz-Q?purpose=inline)

Scene 3 — Personalization

Show how changing a student's skills or interests changes the recommendation results.

![TrackUrApp | Your Guide to College Applications](https://images.openai.com/static-rsc-4/mduDkzB2O_lKy762NWVEh3gqdIszVU3jQr1o27HJOjn2_KmGZKqEP_eiabJWKC16E9D-dlFce_5c1UEq6WX5gcr7TqCuQ55FVpn5ChCdRLUpw4Zzq3Jox9y1L40V3oSAQKVZSa_at57flYThbMhlmQ9jfxbEEhaG8c21UVNE2ms?purpose=inline)

Scene 4 — Taking action

Save an opportunity, track an application, and show its deadline.

The most important technical demonstration is to show that recommendations are genuinely derived from the profile and database, not hardcoded into the frontend.

## 19. Risks and mitigations

|
Risk

|

Mitigation

|
| --- | --- |
|

Not enough real opportunities

|

Start with curated listings and admin entry

|
|

Incorrect or expired information

|

Store sources, timestamps, and expiry status

|
|

Poor recommendations

|

Use explainable scoring and test with sample profiles

|
|

Duplicate listings

|

Normalize URLs and implement duplicate checks

|
|

Scope becoming too large

|

Prioritize P0 features and defer automation

|
|

External source restrictions

|

Prefer official APIs, RSS, and permitted sources

|
|

Database setup problems

|

Document PostgreSQL setup and provide environment templates

|
|

Security vulnerabilities

|

Test authorization, validation, and authentication early

|

## 20. Success metrics

The following are proposed evaluation metrics, not existing results.

* Discovery: Number of published opportunities available to students.

* Relevance: Percentage of recommendations judged relevant in a test set.

* Coverage: Number of opportunity categories represented.

* Usability: Time required for a new student to reach their recommendations.

* Engagement: Bookmarks and application-tracking actions.

* Freshness: Percentage of active listings with valid source and deadline information.

* Reliability: API test pass rate and measured response times.

For the hackathon, we should prioritize a working end-to-end flow, correct matching behavior, and credible opportunity data over raw listing counts.

## 21. Final technology and product decisions

### Confirmed project baseline

Agreed

Product

OpportunityHub

Backend language

Python

Backend framework

FastAPI

Database

PostgreSQL

ORM

SQLAlchemy

Migrations

Alembic

Frontend

HTML + CSS + JavaScript

Architecture

Modular monolith + REST API

Recommendation

Explainable weighted scoring

Development order

Backend first

## 22. Immediate next step: initialize the backend

We should now start implementing Phase 1, not build the frontend yet.

The first milestone is a running FastAPI application that connects to PostgreSQL, reads configuration from environment variables, and exposes a health endpoint. Once that works, we can create the schema and proceed module by module.

Definition of done for Phase 1:

* Python virtual environment created.

* Dependencies installed.

* PostgreSQL database and application user configured.

* FastAPI application starts successfully.

* Database connection verified.

* Health endpoint responds successfully.

* Swagger documentation opens.

* Project structure and Git ignore rules established.

That gives us a stable foundation for every subsequent feature in the PRD.
