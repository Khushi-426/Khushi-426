<!--
  KHUSHI.OS profile README
  Regenerate art:  python scripts/make_khushios_assets.py
                   python scripts/make_ascii_svg.py source-prepped.png assets/portrait-ascii.svg
                   python scripts/make_wordmark_svg.py --mode rock --out assets/wordmark.svg
                   python scripts/make_pixel_sprite.py <photo> assets/pixel-sprite.gif
                   python scripts/generate_streak_svg.py Khushi-426 assets/contrib-heatmap.svg
-->
<div align="center">

<img src="assets/boot.svg" width="860" alt="KHUSHI.OS boot sequence. It types out loading lines for B.Tech Computer Engineering at PICT, the backend and AI-agent stack, then says Hello, World. I'm Khushi. Backend developer building reliable systems and practical AI-driven apps." />

<br><br>

<table>
<tr>
<td valign="top"><img src="assets/portrait-ascii.svg" width="330" alt="Khushi Chakke, ASCII portrait that types itself in" /></td>
<td valign="top"><img src="assets/wordmark.svg" width="540" alt="KHUSHI, extruded 3D ASCII wordmark that rocks side to side" /></td>
</tr>
</table>

<p><b>Backend Developer · Agentic AI Builder · Computer Engineering @ PICT</b></p>

<p>
  <code>khushi@os:~$</code>
  <a href="#whoami">whoami</a> &nbsp;·&nbsp;
  <a href="#skills">skills</a> &nbsp;·&nbsp;
  <a href="#quests">quests</a> &nbsp;·&nbsp;
  <a href="#projects">projects</a> &nbsp;·&nbsp;
  <a href="#activity">activity</a> &nbsp;·&nbsp;
  <a href="#achievements">achievements</a> &nbsp;·&nbsp;
  <a href="#contact">contact</a>
</p>

</div>

<br>

<a name="whoami"></a>

### `khushi@os ~ $ whoami`

<div align="center">
<table>
<tr>
<td valign="top"><img src="assets/pixel-sprite.gif" width="340" alt="Pixel-art character of Khushi in a retro window, bobbing and blinking" /></td>
<td valign="top"><img src="assets/about-card.svg" width="520" alt="Character card: backend developer and AI-agent builder, based in Pune, B.Tech Computer Engineering at PICT, CGPA 9.87 out of 10" /></td>
</tr>
</table>
</div>

Computer Engineering undergraduate at PICT (9.87/10 CGPA) with six months of backend development experience building features for live products. Skilled in Java, C++, Python, Node.js and PostgreSQL, with hands-on experience in AI-agent orchestration, database optimization and CI/CD. I'm interested in building reliable backend systems and practical AI-driven applications.

**Experience: Research Intern (In-House), Software Development, Dec 2025 – May 2026**

- Designed and delivered 12+ features for a live application serving 200+ active users, building REST APIs backed by a relational SQL database, with zero post-release rollbacks across Agile sprints.
- Ran feature delivery end to end: requirement analysis, design discussions with senior engineers, implementation, code reviews, regression testing and root-cause analysis before release.
- Took part in discussions and testing of a gated CI/CD pipeline for a 5-microservice system, with approval checks and rollback support, as part of an initiative that cut release time from days to under 2 hours.

<br>

<a name="skills"></a>

### `khushi@os ~ $ ls skills/`

<div align="center">
<img src="assets/tech-inventory.svg" width="860" alt="Tech inventory grouped into languages (C, C++, Java, Python, JavaScript, SQL), frontend (React.js), backend (Node.js, Express.js, FastAPI, REST APIs, WebSockets), databases (PostgreSQL, MySQL, MongoDB), AI and agents (LangGraph, multi-agent orchestration, stateful workflows, conditional routing), and tools (Git, GitHub, GitHub Actions, Docker, Linux, CI/CD, Agile, OOP, DSA, DBMS, testing)" />
</div>

<br>

<a name="quests"></a>

### `khushi@os ~ $ cat quests.md`

These are learning goals I'm actively working on, not completed achievements.

- **Database performance.** Go further on query and index optimization, building on the compound indexing and pagination work behind CampusTrade's feed.
- **Stateful AI-agent systems.** Move from a working LangGraph prototype toward reliable, resumable multi-agent workflows, building on ReconEngine's shared state and conditional routing.
- **Release engineering.** Keep sharpening gated CI/CD and rollback practice across services.
- **Problem solving.** Keep practicing DSA on LeetCode and CodeChef, where I've solved 400+ problems so far.
- **German.** Progress past Goethe A1.

<br>

<a name="projects"></a>

### `khushi@os ~ $ ls -l projects/`

<div align="center">
<table>
<tr>
<td valign="top"><img src="assets/project-reconengine.svg" width="420" alt="Pixel illustration of reconciliation: ledger rows matched across two columns, with one exception flagged in peach" /></td>
<td valign="top"><img src="assets/project-campustrade.svg" width="420" alt="Pixel illustration of a campus marketplace: item tiles in a feed, with a pulsing chat bubble" /></td>
</tr>
</table>
</div>

#### ReconEngine: Agentic Financial Reconciliation Platform

**Stack:** Node.js · PostgreSQL · Python · FastAPI · LangGraph · React · Docker

Matches transactions between internal ledgers and external settlement records, then coordinates the investigation of whatever doesn't match.

- **Matching:** processes 10,000+ records with four strategies (exact, tolerance, reference and composite) and raises exceptions for unmatched transactions.
- **Agents:** a FastAPI service where LangGraph coordinates 4 specialized agents through shared state and conditional routing, covering discrepancy investigation, evidence gathering and resolution recommendations.
- **Workers:** asynchronous PostgreSQL-backed workers using `FOR UPDATE SKIP LOCKED`, with automatic retries, dead-letter handling and stalled-job recovery to prevent duplicate job claims.
- **Reliability:** validated through 35 test cases, with data integrity enforced by transactions, unique constraints and trigger-based audit logging.

Repository: [github.com/Khushi-426/reconengine](https://github.com/Khushi-426/reconengine)

#### CampusTrade: Peer-to-Peer Campus Marketplace

**Stack:** React.js · Node.js · Express.js · MongoDB · REST APIs · WebSockets

A full-stack marketplace for campus buying and selling.

- **Marketplace:** searchable, filterable listings, with distinct user and administrator workflows across the listing lifecycle.
- **Messaging and security:** real-time buyer–seller messaging over WebSockets, JWT authentication, role-based authorization, ownership checks, server-side input validation and rate limiting.
- **Performance:** compound indexing, pagination, response compression and connection pooling cut documents examined per feed query from 10,000 to 12 (99.88%) and feed payload from 3.0 MB to 6 KB. Verified with functional and benchmark test suites.

Repository: [github.com/Khushi-426/campus](https://github.com/Khushi-426/campus)

<br>

<a name="activity"></a>

### `khushi@os ~ $ ./contributions.sh`

<div align="center">
<img src="assets/contrib-heatmap.svg" width="860" alt="GitHub contribution graph for Khushi-426, refreshed daily with real data" />
</div>

<br>

<a name="achievements"></a>

### `khushi@os ~ $ cat achievements.log`

- **Finalist, SEBI Securities Market TechSprint 2026:** top 8 among 2,664 teams, for an AI-driven SME IPO disclosure solution.
- **Finalist, Compute n Compete 2025:** top 20 among 100 teams at PICT ACM Student Chapter (PASC).
- **Problem solving:** 400+ DSA problems solved across LeetCode and CodeChef.
- **Goethe-Zertifikat A1, Goethe-Institut:** certified German A1 proficiency. [View certificate](https://drive.google.com/file/d/1ot8kmhaAbhVZia2JMqYNuzHXZMtLf9L8/view)

<br>

<a name="contact"></a>

### `khushi@os ~ $ connect`

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-khushichakke-382F4A?style=for-the-badge&logo=linkedin&logoColor=FFF9EE&labelColor=786A91)](https://www.linkedin.com/in/khushichakke/)
[![GitHub](https://img.shields.io/badge/GitHub-Khushi--426-382F4A?style=for-the-badge&logo=github&logoColor=FFF9EE&labelColor=786A91)](https://github.com/Khushi-426)
[![LeetCode](https://img.shields.io/badge/LeetCode-KhushiChakke-382F4A?style=for-the-badge&logo=leetcode&logoColor=FFF9EE&labelColor=786A91)](https://leetcode.com/u/KhushiChakke/)
[![Email](https://img.shields.io/badge/Email-khushichakke%40gmail.com-382F4A?style=for-the-badge&logo=gmail&logoColor=FFF9EE&labelColor=786A91)](mailto:khushichakke@gmail.com)

<br>

<sub>KHUSHI.OS · process exited 0 · thanks for stopping by</sub>

</div>
